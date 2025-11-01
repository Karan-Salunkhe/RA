# scripts/run_experiment.py
# Consolidate manually collected UI outputs into Results/llm_outputs_structured.csv
# - Scans both Results/raw and results/raw (recursively)
# - Accepts .txt and .md
# - Robust filename parsing: <model>_<condition>_runN (hyphens/spaces allowed)
# - Adds file_name, char_len, word_count, response_sha1
# - Deduplicates identical responses

from __future__ import annotations
import re
import time
import hashlib
from pathlib import Path
import pandas as pd

# ----- Paths tailored to your machine (consistent with other scripts) ----------
BASE = Path(r"C:/Users/Karan/OneDrive/Desktop/RA_TASK_08")
PROMPTS_CSV = BASE / "Prompts" / "prompt_variations.csv"

RAW_DIRS = [
    BASE / "Results" / "raw",
    BASE / "results" / "raw",
]

OUT_DIR = BASE / "Results"
OUT_CSV = OUT_DIR / "llm_outputs_structured.csv"

# File types to ingest
RAW_EXTS = {".txt", ".md"}

# ----- Helpers ----------------------------------------------------------------
def read_csv_relaxed(p: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(p)
    except UnicodeDecodeError:
        return pd.read_csv(p, encoding="latin-1")

def sha1_text(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8", errors="ignore")).hexdigest()

def parse_filename(p: Path, valid_conditions: set[str]):
    """
    Parse filenames robustly. Examples:
      gpt4_neutral_run1.txt
      gpt-4o-mini_negative_run02.md
      claude-3.5_confirmation_2025-10-31_run3.txt
      o3  demographic  run7.txt
    Returns (model, condition, run_index) or raises ValueError.
    """
    stem = p.stem  # without extension
    # Normalize: convert spaces/hyphens to underscores, lowercase
    norm = re.sub(r"[\s\-]+", "_", stem.lower())

    # 1) condition token must appear as whole token
    cond = next((c for c in valid_conditions if re.search(rf"(?:^|_){re.escape(c)}(?:_|$)", norm)), None)
    if not cond:
        raise ValueError(f"condition token not found (expected one of {sorted(valid_conditions)})")

    # 2) run index like _runN
    m_run = re.search(r"(?:^|_)run(?P<n>\d+)(?:_|$)", norm)
    if not m_run:
        raise ValueError("missing _runN (e.g., _run1)")
    run_index = m_run.group("n").lstrip("0") or "0"

    # 3) model guessed as everything before first _<condition>
    model = norm.split(f"_{cond}", 1)[0].strip("_") or "unknown_model"
    return model, cond, run_index

# ----- Main -------------------------------------------------------------------
if __name__ == "__main__":
    if not PROMPTS_CSV.exists():
        raise FileNotFoundError("Prompts/prompt_variations.csv not found. Run scripts/experiment_design.py first.")

    # Ensure output dir
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for d in RAW_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    # Load prompt variations and get allowed conditions from the CSV (no hardcoding)
    prompts = read_csv_relaxed(PROMPTS_CSV)
    if prompts.empty or "condition" not in prompts.columns:
        raise ValueError("prompt_variations.csv has no 'condition' column or is empty.")
    by_condition = {str(r.get("condition", "")).strip().lower(): r for _, r in prompts.iterrows() if str(r.get("condition", "")).strip()}
    valid_conditions = set(by_condition.keys())

    # Gather candidate files (recursively) from both raw dirs
    candidates: list[Path] = []
    for d in RAW_DIRS:
        candidates.extend([p for p in d.rglob("*") if p.is_file() and p.suffix.lower() in RAW_EXTS])

    if not candidates:
        print("No raw .txt/.md files found in either:")
        for d in RAW_DIRS:
            print(" -", d)
        print("Add your UI outputs then re-run.")
        raise SystemExit(0)

    print("Scanning files:")
    for p in sorted(candidates):
        print(" -", p)

    rows = []
    for path in sorted(candidates):
        try:
            model, condition, run_index = parse_filename(path, valid_conditions)
        except ValueError as e:
            print(f"Skipping {path.name}: {e}")
            continue

        pr = by_condition.get(condition)
        if pr is None:
            print(f"Skipping {path.name}: condition '{condition}' not present in prompt_variations.csv")
            continue

        # Read response
        try:
            response_text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            response_text = path.read_text(errors="ignore")

        # Safe access
        prompt_id = pr.get("prompt_id", f"{condition}_v1")
        hypothesis = pr.get("hypothesis", "unspecified")
        prompt_text = pr.get("prompt_text", "")

        rows.append({
            "file_name": path.name,
            "prompt_id": prompt_id,
            "hypothesis": hypothesis,
            "condition": condition,
            "model": model,
            "model_version": "ui",
            "temperature": "NA",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "prompt_text": prompt_text,
            "response_text": response_text,
            "run": run_index,
            "char_len": len(response_text),
            "word_count": len(response_text.split()),
            "response_sha1": sha1_text(response_text),
        })

    df = pd.DataFrame(rows)

    if df.empty:
        print("No rows written. Check your raw files and filename pattern: <model>_<condition>_runN (e.g., gpt4_neutral_run1.txt).")
        raise SystemExit(0)

    # Deduplicate exact duplicates (same response, same prompt/run/model)
    df = df.drop_duplicates(subset=["response_sha1", "prompt_id", "run", "model"], keep="first")

    df.to_csv(OUT_CSV, index=False)
    print(f"✅ Wrote {OUT_CSV} with {len(df)} rows.")
