# scripts/sanitize_players.py
import pandas as pd
from pathlib import Path

DATA = Path(r"C:/Users/Karan/OneDrive/Desktop/RA_TASK_08/Dataset")
BAT_SRC = DATA / "ipl_batting.csv"
BOW_SRC = DATA / "ipl_bowling.csv"
BAT_OUT = DATA / "ipl_batting_anon.csv"
BOW_OUT = DATA / "ipl_bowling_anon.csv"

# Candidate column names for player field (check in order)
PLAYER_CANDIDATES = [
    "player", "player name", "name", "batter", "batsman", "striker",
    "non_striker", "bowler"
]

def read_csv_relaxed(path: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(path)
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")

def find_name_col(df: pd.DataFrame) -> str:
    cols = {c.strip().lower(): c for c in df.columns}
    for cand in PLAYER_CANDIDATES:
        if cand in cols:
            return cols[cand]
    raise KeyError(
        f"Could not find a player-name column. "
        f"Looked for any of: {PLAYER_CANDIDATES}. "
        f"Available columns: {list(df.columns)}"
    )

def excel_letters(n: int) -> str:
    """1->A, 26->Z, 27->AA ..."""
    s = ""
    while n > 0:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s

def build_mapping(*series) -> dict:
    # Union of unique non-null names across provided Series, sorted for determinism
    names = set()
    for s in series:
        names.update(pd.Series(s).dropna().unique().tolist())
    names = sorted(names)
    return {name: f"Player {excel_letters(i+1)}" for i, name in enumerate(names)}

if __name__ == "__main__":
    DATA.mkdir(exist_ok=True)

    # Load raw (LOCAL) datasets
    bat = read_csv_relaxed(BAT_SRC)
    bow = read_csv_relaxed(BOW_SRC)

    # Detect the player column in each file
    bat_name_col = find_name_col(bat)
    bow_name_col = find_name_col(bow)

    # Build one consistent mapping across both files
    mapping = build_mapping(bat[bat_name_col], bow[bow_name_col])

    # Apply mapping
    bat[bat_name_col] = bat[bat_name_col].map(mapping)
    bow[bow_name_col] = bow[bow_name_col].map(mapping)

    # Save anonymized copies (LOCAL)
    bat.to_csv(BAT_OUT, index=False)
    bow.to_csv(BOW_OUT, index=False)

    print(f"Anonymized:\n  {BAT_OUT}\n  {BOW_OUT}")
    print("NOTE: Keep source CSVs and these anonymized files local; do NOT commit raw data to git.")
