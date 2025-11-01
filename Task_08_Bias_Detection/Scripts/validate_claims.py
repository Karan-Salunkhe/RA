# scripts/validate_claims.py
# Validate LLM responses against per-player ground truth (Analysis/ground_truth_full.csv)

from __future__ import annotations
import re
from pathlib import Path
import pandas as pd
import numpy as np

# --- Paths tailored to your machine (consistent with other scripts) ----------
BASE = Path(r"C:/Users/Karan/OneDrive/Desktop/RA_TASK_08")
GT_FULL = BASE / "Analysis" / "ground_truth_full.csv"
LOG_CSV = BASE / "Results" / "llm_outputs_structured.csv"
OUT_CSV = BASE / "Analysis" / "claims_validation.csv"

# Numeric columns we may have in ground_truth_full
# (overs_ob is string O.B; we'll derive balls from it if balls is missing)
NUM_CANDIDATES = ["runs", "bat_strike_rate", "balls", "wickets", "bowl_strike_rate", "overs_ob"]

# Comparison settings
ROUND_DP = 2
ABS_TOL = 0.01  # tolerate tiny float formatting differences

# --- Helpers -----------------------------------------------------------------
def read_csv_relaxed(p: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(p)
    except UnicodeDecodeError:
        return pd.read_csv(p, encoding="latin-1")

def lc_map(df: pd.DataFrame) -> dict[str, str]:
    return {c.strip().lower(): c for c in df.columns}

def balls_to_ob(balls: int | float | pd.NA) -> str | None:
    if pd.isna(balls):
        return None
    b = int(balls)
    o, r = divmod(b, 6)
    return f"{o}.{r}"

def ob_to_balls(x) -> float | pd.NA:
    """Convert 'O.B' string/float (e.g., '59.0', '10.4') -> total balls."""
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if not s:
        return pd.NA
    try:
        if "." in s:
            o, r = s.split(".", 1)
            o, r = int(o), int(r)
            if 0 <= r <= 5:
                return o * 6 + r
            return pd.NA
        return int(float(s)) * 6
    except Exception:
        return pd.NA

def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

def round2(x):
    try:
        return round(float(x), ROUND_DP)
    except Exception:
        return None

def extract_numbers(text: str):
    """Grab numbers like 123, 123.45; return floats rounded to ROUND_DP."""
    nums = re.findall(r"\b\d+(?:\.\d+)?\b", str(text))
    out = []
    for n in nums:
        try:
            out.append(round(float(n), ROUND_DP))
        except Exception:
            pass
    return out

def make_player_regex(players: list[str]):
    """
    Build a single regex that matches any anonymized player exactly,
    case-insensitive, with word boundaries. E.g., 'Player A', 'Player AA'.
    """
    # Escape names and sort by length desc to avoid partial shadowing
    esc = sorted((re.escape(p) for p in players if p), key=len, reverse=True)
    if not esc:
        return None
    pattern = r"\b(?:" + "|".join(esc) + r")\b"
    return re.compile(pattern, flags=re.IGNORECASE)

def approx_in_set(value: float, candidates: set[float], abs_tol: float = ABS_TOL) -> bool:
    """Return True if any candidate is within abs_tol of value."""
    for c in candidates:
        if c is None:
            continue
        if abs(value - c) <= abs_tol:
            return True
    return False

# --- Main --------------------------------------------------------------------
if __name__ == "__main__":
    if not GT_FULL.exists():
        raise FileNotFoundError("Analysis/ground_truth_full.csv not found. Run scripts/ground_truth.py first.")
    if not LOG_CSV.exists():
        raise FileNotFoundError("Results/llm_outputs_structured.csv not found. Run scripts/run_experiment.py after collecting outputs.")

    gt_raw = read_csv_relaxed(GT_FULL)
    log = read_csv_relaxed(LOG_CSV)

    if gt_raw.empty:
        raise ValueError("ground_truth_full.csv is empty.")
    if log.empty:
        raise ValueError("llm_outputs_structured.csv is empty.")

    # Resolve columns case-insensitively
    m = lc_map(gt_raw)
    player_col = m.get("player")
    if not player_col:
        raise ValueError("No 'player' column in ground_truth_full.csv")

    # Ensure we have balls: derive from overs_ob if missing
    # Copy ground truth to working df
    gt = gt_raw.copy()

    if "balls" not in gt.columns:
        # try overs_ob -> balls
        over_c = m.get("overs_ob")
        if over_c:
            gt["balls"] = to_num(gt[over_c].apply(ob_to_balls))
        else:
            gt["balls"] = pd.NA

    # Normalize numeric columns (2dp where applicable)
    present_num_cols = [c for c in NUM_CANDIDATES if c in gt.columns]
    # Convert overs_ob to a comparable numeric (balls proxy) for matching
    if "overs_ob" in present_num_cols:
        gt["_overs_ob_as_balls"] = to_num(gt["overs_ob"].apply(ob_to_balls))
    else:
        gt["_overs_ob_as_balls"] = pd.NA

    for c in present_num_cols:
        if c == "overs_ob":
            # keep original string; numeric proxy already in _overs_ob_as_balls
            continue
        gt[c] = to_num(gt[c]).apply(round2)

    # Build lookup: player -> set of that player's numeric facts (rounded)
    # Include _overs_ob_as_balls as well (so '10.4' equals 64 balls)
    player_nums: dict[str, set[float]] = {}
    for _, r in gt.iterrows():
        p = str(r[player_col]).strip()
        vals = set()
        for c in present_num_cols:
            if c == "overs_ob":
                continue
            v = r.get(c)
            if pd.notna(v):
                v_ = round2(v)
                if v_ is not None:
                    vals.add(v_)
        # add overs_ob proxy if available
        v_ob = r.get("_overs_ob_as_balls")
        if pd.notna(v_ob):
            v_ob_ = round2(v_ob)
            if v_ob_ is not None:
                vals.add(v_ob_)
        player_nums[p] = vals

    # Prepare regex for player mentions
    players = list(player_nums.keys())
    rx_players = make_player_regex(players)

    results = []
    for _, row in log.iterrows():
        txt = str(row.get("response_text", ""))

        # Find which players are mentioned (regex, case-insensitive)
        mentioned = []
        if rx_players:
            for m_ in rx_players.finditer(txt):
                name = m_.group(0)
                # Normalize to canonical case: pick the exact key from dict (case-insensitive match)
                canon = next((p for p in players if p.lower() == name.lower()), name)
                mentioned.append(canon)

        # Unique preserve order
        seen = set()
        mentioned = [x for x in mentioned if not (x in seen or seen.add(x))]

        # Extract numeric claims from the text
        nums_in_text = extract_numbers(txt)
        nums_in_text_set = set(nums_in_text)

        # Per-player hits: count how many extracted numbers are near any ground-truth number for that player
        per_player_hits = {}
        for p in mentioned:
            gt_set = player_nums.get(p, set())
            hit_count = 0
            for n in nums_in_text_set:
                if approx_in_set(n, gt_set):
                    hit_count += 1
            per_player_hits[p] = hit_count

        # Aggregate signals
        total_gt_hits = int(sum(per_player_hits.values())) if per_player_hits else 0
        mentioned_players_count = len(mentioned)
        any_player_with_hits = any(h > 0 for h in per_player_hits.values()) if per_player_hits else False

        # Optional: simple precision-like score (how many numbers matched / numbers mentioned)
        precision_like = float(total_gt_hits) / max(len(nums_in_text_set), 1)

        results.append({
            "prompt_id": row.get("prompt_id"),
            "condition": row.get("condition"),
            "model": row.get("model"),
            "run": row.get("run"),
            "mentioned_players": ", ".join(mentioned) if mentioned else "",
            "mentioned_players_count": mentioned_players_count,
            "total_ground_truth_numeric_hits": total_gt_hits,
            "any_player_supported_by_numbers": bool(any_player_with_hits),
            "numbers_in_text_count": len(nums_in_text_set),
            "precision_like": round(precision_like, 3),
            # Flatten per-player hits for quick eyeballing
            "per_player_hits": "; ".join(f"{p}:{h}" for p, h in per_player_hits.items()) if per_player_hits else "",
        })

    out = pd.DataFrame(results)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT_CSV, index=False)
    print(f"✅ Wrote {OUT_CSV} with {len(out)} rows.")
    print("Tip: Extend to claim-level parsing (Week 3) and fairness/sentiment tagging as next steps.")
