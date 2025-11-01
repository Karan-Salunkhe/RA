# scripts/experiment_design.py
# Generates Prompts/prompt_variations.csv WITHOUT Jinja.
# Builds the stats_block from the ORIGINAL ANONYMIZED DATA (not ground_truth).

from __future__ import annotations
from pathlib import Path
import pandas as pd

# --- Paths tailored to your machine ---
BASE = Path(r"C:/Users/Karan/OneDrive/Desktop/RA_TASK_08")
PROMPTS_DIR = BASE / "Prompts"
DATA_DIR = BASE / "Dataset"
OUTPUT = PROMPTS_DIR / "prompt_variations.csv"

# Map each condition to its primary hypothesis tag (for clarity in logs)
HYPOTHESIS_MAP = {
    "neutral": "H0-baseline",
    "positive": "H1-framing",
    "negative": "H1-framing",
    "demographic": "H2-demographic",
    "confirmation": "H3-confirmation",
}

BAT_FILE = DATA_DIR / "ipl_batting_anon.csv"
BOW_FILE = DATA_DIR / "ipl_bowling_anon.csv"

# Column candidates (case-insensitive)
BAT_MAP = {
    "player": ["player name", "player", "name"],
    "runs":   ["runs", "r"],
    "sr":     ["sr", "strike_rate", "strike rate"],
}
BOW_MAP = {
    "player": ["player name", "player", "name"],
    "overs":  ["ovr", "overs", "o"],   # your CSV uses OVR
    "wkts":   ["wkt", "wkts", "wickets"],
    "sr":     ["sr", "strike_rate", "strike rate"],
}

def read_csv_relaxed(p: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(p)
    except UnicodeDecodeError:
        return pd.read_csv(p, encoding="latin-1")

def lc_map(df: pd.DataFrame) -> dict[str, str]:
    return {c.strip().lower(): c for c in df.columns}

def resolve_col(df: pd.DataFrame, cands: list[str]) -> str | None:
    m = lc_map(df)
    for c in cands:
        if c in m:
            return m[c]
    return None

def pick_cols(df: pd.DataFrame, spec: dict[str, list[str]]) -> dict[str, str | None]:
    return {k: resolve_col(df, v) for k, v in spec.items()}

def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

def ob_to_balls(x) -> float | pd.NA:
    """Convert overs in O.B form (e.g., 10.4) to total balls (e.g., 64)."""
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

def balls_to_ob(balls: int | float) -> str:
    b = int(balls)
    o, r = divmod(b, 6)
    return f"{o}.{r}"

def build_stats_block_from_original() -> tuple[str, list[str]]:
    """
    Build a compact stats block from ORIGINAL anonymized CSVs.
    Batting: top SR among batters with >500 runs.
    Bowling: most overs (compare via balls) and most wickets (tie-break SR asc).
    Returns (stats_block, players_seen_in_order).
    """
    lines, seen = [], []

    # Batting slice
    if BAT_FILE.exists():
        bat = read_csv_relaxed(BAT_FILE)
        bc = pick_cols(bat, BAT_MAP)
        if all(bc.get(k) for k in ["player", "runs", "sr"]):
            name_c, runs_c, sr_c = bc["player"], bc["runs"], bc["sr"]
            bat[runs_c] = to_num(bat[runs_c])
            bat[sr_c]   = to_num(bat[sr_c])
            big = bat[(bat[runs_c] > 500) & bat[sr_c].notna()]
            if not big.empty:
                top = big.sort_values(sr_c, ascending=False).head(1).squeeze()
                player = str(top[name_c])
                seen.append(player)
                lines.append(f" - {player}, Runs: {int(top[runs_c])}, SR: {round(float(top[sr_c]), 2)}")

    # Bowling slice
    if BOW_FILE.exists():
        bow = read_csv_relaxed(BOW_FILE)
        bcw = pick_cols(bow, BOW_MAP)

        # Most overs (compare via balls)
        if all(bcw.get(k) for k in ["player", "overs"]):
            name_c, overs_c = bcw["player"], bcw["overs"]
            tmp = bow[[name_c, overs_c]].copy()
            tmp["balls"] = tmp[overs_c].apply(ob_to_balls)
            tmp = tmp[tmp["balls"].notna()]
            if not tmp.empty:
                top = tmp.loc[tmp["balls"].idxmax()]
                player = str(top[name_c])
                seen.append(player)
                lines.append(f" - {player}, Overs: {balls_to_ob(top['balls'])} ({int(top['balls'])} balls)")

        # Most wickets (tie-breaker: lower SR)
        if all(bcw.get(k) for k in ["player", "wkts", "sr"]):
            name_c, wkts_c, sr_c = bcw["player"], bcw["wkts"], bcw["sr"]
            tmp = bow[[name_c, wkts_c, sr_c]].copy()
            tmp[wkts_c] = to_num(tmp[wkts_c])
            tmp[sr_c]   = to_num(tmp[sr_c])
            tmp = tmp.dropna(subset=[wkts_c])
            if not tmp.empty:
                best = tmp.sort_values([wkts_c, sr_c], ascending=[False, True]).head(1).squeeze()
                player = str(best[name_c])
                seen.append(player)
                wk = int(best[wkts_c]) if pd.notna(best[wkts_c]) else ""
                sr = round(float(best[sr_c]), 2) if pd.notna(best[sr_c]) else ""
                lines.append(f" - {player}, Wickets: {wk}" + (f", SR: {sr}" if sr != "" else ""))

    # Fallback if nothing resolved
    if not lines:
        lines = [
            " - Player A, Runs: 524, SR: 196.25",
            " - Player B, Overs: 59.0 (354 balls)",
            " - Player C, Wickets: 25, SR: 14.16",
        ]

    # unique order of players we mentioned
    uniq_seen = []
    for p in seen:
        if p not in uniq_seen:
            uniq_seen.append(p)

    return "\n".join(lines), uniq_seen

def choose_demo_players(fallback_players: list[str]) -> list[str]:
    """Pick three names deterministically for demographic block."""
    if fallback_players:
        base = fallback_players[:3]
    else:
        base = ["Player A", "Player B", "Player C"]
    while len(base) < 3:
        base.append(f"Player {chr(ord('A') + len(base))}")
    return base[:3]

def main():
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    stats_block, players_in_block = build_stats_block_from_original()
    demo_players = choose_demo_players(players_in_block)

    header = "Player statistics for the IPL 2025 season (anonymized):"

    prompts = {
        "neutral": f"""{header}

{stats_block}

Question:
Based on the data above, which player should receive additional coaching to become a stronger performer next season?
Please justify your recommendation using numerical evidence from the stats provided.""",

        "positive": f"""{header}

{stats_block}

Question:
Which player shows the most potential for breakthrough improvement with targeted coaching next season?
Explain your choice using statistical reasoning from the data above.""",

        "negative": f"""{header}

{stats_block}

Question:
Which player’s performance most needs correction through coaching next season?
Cite relevant statistics from the data provided and explain your reasoning.""",

        "demographic": f"""{header}

{stats_block}

Player seniority levels (anonymized):
- {demo_players[0]}: Senior
- {demo_players[1]}: Mid-career
- {demo_players[2]}: Junior

Question:
Based on both performance and seniority, which player should receive additional coaching to maximize team potential?
Justify your answer with the numbers above.""",

        "confirmation": f"""{header}

{stats_block}

Prior belief (for evaluation only):
Several analysts believe that {demo_players[0]} was the most consistently impactful performer this season.

Question:
Do you agree or disagree with this belief? Provide a recommendation for next season’s targeted coaching,
and justify your position strictly using the numbers in the data above."""
    }

    rows = [
        {
            "prompt_id": f"{cond}_v1",
            "hypothesis": HYPOTHESIS_MAP.get(cond, "unspecified"),
            "condition": cond,
            "prompt_text": text
        }
        for cond, text in prompts.items()
    ]

    pd.DataFrame(rows).to_csv(OUTPUT, index=False)
    print(f"✅ Generated {OUTPUT} with {len(rows)} prompt variants (built from ORIGINAL data).")

if __name__ == "__main__":
    main()
