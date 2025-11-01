# scripts/ground_truth.py
# Produces TWO artifacts:
#  1) Analysis/ground_truth_full.csv    -> per-player truth table (for validation later)
#  2) Analysis/ground_truth_metrics.csv -> anchor metrics summary (3 KPIs + extras)
#
# Tailored to IPL CSVs:
#   Batting:  Player Name, Runs, SR
#   Bowling:  Player Name, OVR (overs in O.B), WKT, SR

from __future__ import annotations
from pathlib import Path
import pandas as pd

# ---- Paths (tailored to your machine) ---------------------------------------
BASE = Path(r"C:/Users/Karan/OneDrive/Desktop/RA_TASK_08")
DATA = BASE / "Dataset"
ANALYSIS = BASE / "Analysis"
ANALYSIS.mkdir(parents=True, exist_ok=True)

BAT_FILE = DATA / "ipl_batting_anon.csv"
BOW_FILE = DATA / "ipl_bowling_anon.csv"

FULL_OUT = ANALYSIS / "ground_truth_full.csv"
METRICS_OUT = ANALYSIS / "ground_truth_metrics.csv"

# ---- Column candidates (case-insensitive) -----------------------------------
BAT_MAP = {
    "player": ["player name", "player", "name"],
    "runs":   ["runs", "r"],
    "bat_sr": ["sr", "strike_rate", "strike rate"],
}
BOW_MAP = {
    "player":  ["player name", "player", "name"],
    "overs":   ["ovr", "overs", "o"],   # IPL bowling has OVR (O.B notation)
    "wkts":    ["wkt", "wkts", "wickets"],
    "bowl_sr": ["sr", "strike_rate", "strike rate"],
}

# ---- Helpers ----------------------------------------------------------------
def read_csv_relaxed(p: Path) -> pd.DataFrame:
    try:
        return pd.read_csv(p)
    except UnicodeDecodeError:
        return pd.read_csv(p, encoding="latin-1")

def lc_map(df: pd.DataFrame) -> dict[str, str]:
    return {c.strip().lower(): c for c in df.columns}

def resolve_col(df: pd.DataFrame, candidates: list[str]) -> str | None:
    m = lc_map(df)
    for c in candidates:
        if c in m:
            return m[c]
    return None

def pick_cols(df: pd.DataFrame, spec: dict[str, list[str]]) -> dict[str, str | None]:
    return {k: resolve_col(df, v) for k, v in spec.items()}

def to_num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")

def ob_to_balls(x) -> float | pd.NA:
    """Convert overs in O.B form (e.g., '59.0', '10.4') to total balls (e.g., 354, 64)."""
    if pd.isna(x):
        return pd.NA
    s = str(x).strip()
    if not s:
        return pd.NA
    try:
        if "." in s:
            o_str, r_str = s.split(".", 1)
            o, r = int(o_str), int(r_str)
            if 0 <= r <= 5:
                return o * 6 + r
            return pd.NA
        return int(float(s)) * 6
    except Exception:
        return pd.NA

def balls_to_ob(balls: int | float | pd.NA) -> str | None:
    if pd.isna(balls):
        return None
    b = int(balls)
    o, r = divmod(b, 6)
    return f"{o}.{r}"

def infer_role(row: pd.Series) -> str:
    has_bat = not (pd.isna(row.get("runs")) and pd.isna(row.get("bat_strike_rate")))
    has_bowl = not (pd.isna(row.get("overs_ob")) and pd.isna(row.get("balls")) and pd.isna(row.get("wickets")) and pd.isna(row.get("bowl_strike_rate")))
    if has_bat and has_bowl:
        return "allrounder"
    if has_bat:
        return "batter"
    if has_bowl:
        return "bowler"
    return "unknown"

# ---- Main -------------------------------------------------------------------
if __name__ == "__main__":
    # Load
    bat_raw = read_csv_relaxed(BAT_FILE)
    bow_raw = read_csv_relaxed(BOW_FILE)

    # Resolve columns against actual headers
    bat_cols = pick_cols(bat_raw, BAT_MAP)
    bow_cols = pick_cols(bow_raw, BOW_MAP)

    # ---- Standardize BAT ----
    bat = pd.DataFrame()
    if all(bat_cols.get(k) for k in ["player", "runs", "bat_sr"]):
        bat["player"] = bat_raw[bat_cols["player"]].astype(str)
        bat["runs"] = to_num(bat_raw[bat_cols["runs"]])
        bat["bat_strike_rate"] = to_num(bat_raw[bat_cols["bat_sr"]])
    elif bat_cols.get("player"):
        bat["player"] = bat_raw[bat_cols["player"]].astype(str)

    # ---- Standardize BOW ----
    bow = pd.DataFrame()
    if bow_cols.get("player"):
        bow["player"] = bow_raw[bow_cols["player"]].astype(str)

    # Overs in O.B (OVR) -> balls + canonical O.B back for display
    if bow_cols.get("overs"):
        overs_series = bow_raw[bow_cols["overs"]]
        bow["balls"] = overs_series.apply(ob_to_balls)
        bow["overs_ob"] = bow["balls"].apply(balls_to_ob)
    if bow_cols.get("wkts"):
        bow["wickets"] = to_num(bow_raw[bow_cols["wkts"]])
    if bow_cols.get("bowl_sr"):
        bow["bowl_strike_rate"] = to_num(bow_raw[bow_cols["bowl_sr"]])

    # ---- FULL TRUTH TABLE (per player) ----
    full = pd.merge(bat, bow, on="player", how="outer")
    full["role"] = full.apply(infer_role, axis=1)

    # Order & save
    ordered_cols = ["player", "role", "runs", "bat_strike_rate", "overs_ob", "balls", "wickets", "bowl_strike_rate"]
    full = full.reindex(columns=[c for c in ordered_cols if c in full.columns]).sort_values("player").reset_index(drop=True)
    full.to_csv(FULL_OUT, index=False)
    print(f"✅ Wrote full truth table: {FULL_OUT}  (rows={len(full)})")

    # ---- METRICS SUMMARY (anchor KPIs + extras) ----
    rows = []

    # Highest strike rate among batters with > 500 runs
    if set(["player", "runs", "bat_strike_rate"]).issubset(bat.columns):
        filt = bat[(bat["runs"] > 500) & bat["bat_strike_rate"].notna()]
        if not filt.empty:
            top = filt.sort_values("bat_strike_rate", ascending=False).head(1).squeeze()
            rows.append({
                "metric": "highest_sr_over_500_runs",
                "player": top["player"],
                "runs": int(top["runs"]),
                "strike_rate": float(top["bat_strike_rate"]),
            })

    # Most overs bowled (compare using balls)
    if set(["player", "balls"]).issubset(bow.columns) and bow["balls"].notna().any():
        top = bow.loc[bow["balls"].idxmax()]
        rows.append({
            "metric": "most_overs",
            "player": top["player"],
            "overs_ob": balls_to_ob(top["balls"]),
            "balls": int(top["balls"]),
        })

    # Young bowler potential: max wickets, tie-break by lower bowling SR
    if set(["player", "wickets"]).issubset(bow.columns):
        tmp = bow[["player", "wickets"]].copy()
        if "bowl_strike_rate" in bow.columns:
            tmp = bow[["player", "wickets", "bowl_strike_rate"]].copy()
            tmp["bowl_strike_rate"] = to_num(tmp["bowl_strike_rate"])
            best = tmp.sort_values(["wickets", "bowl_strike_rate"], ascending=[False, True]).head(1).squeeze()
        else:
            best = tmp.sort_values("wickets", ascending=False).head(1).squeeze()
        rows.append({
            "metric": "young_bowler_potential",
            "player": best["player"],
            "wickets": int(best["wickets"]) if pd.notna(best["wickets"]) else None,
            "bowl_strike_rate": float(best["bowl_strike_rate"]) if "bowl_strike_rate" in best and pd.notna(best["bowl_strike_rate"]) else None,
        })

    # Extras: Top 5 by runs
    if set(["player", "runs"]).issubset(bat.columns):
        top5_runs = bat.dropna(subset=["runs"]).sort_values("runs", ascending=False).head(5)[["player", "runs"]]
        for i, r in top5_runs.reset_index(drop=True).iterrows():
            rows.append({"metric": f"top_runs_rank_{i+1}", "player": r["player"], "runs": int(r["runs"])})

    # Extras: Top 5 by wickets
    if set(["player", "wickets"]).issubset(bow.columns):
        top5_wkts = bow.dropna(subset=["wickets"]).sort_values("wickets", ascending=False).head(5)[["player", "wickets"]]
        for i, r in top5_wkts.reset_index(drop=True).iterrows():
            rows.append({"metric": f"top_wickets_rank_{i+1}", "player": r["player"], "wickets": int(r["wickets"])})

    pd.DataFrame(rows).to_csv(METRICS_OUT, index=False)
    print(f"✅ Wrote metrics summary: {METRICS_OUT}  (rows={len(rows)})")
