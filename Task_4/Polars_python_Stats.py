import polars as pl
import os
import ast
import json
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from collections import Counter
import pandas as pd


def banner(text):
    print("\n" + "—" * (len(text) + 4))
    print(f"| {text} |")
    print("—" * (len(text) + 4))


def try_parse_json(val):
    try:
        return json.loads(val)
    except:
        try:
            return ast.literal_eval(val)
        except:
            return None


def load_csv():
    banner("POLARS CSV ANALYZER")
    print("Please select a CSV file...")
    root = Tk()
    root.withdraw()
    file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        print("No file selected.")
        exit()
    if not os.path.isfile(file_path):
        print("File not found.")
        exit()

    banner("LOADING DATA")
    df = pl.read_csv(file_path, infer_schema_length=10000)
    print(f"Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def detect_json_columns(df):
    banner("DETECTING JSON-LIKE COLUMNS")
    json_cols = []
    try:
        for col in df.columns:
            sample = df[col].drop_nulls().cast(pl.Utf8).head(10).to_list()
            if any(isinstance(val, str) and val.strip().startswith("{") and val.strip().endswith("}") for val in sample):
                json_cols.append(col)
        if json_cols:
            print(f"JSON-like columns found: {', '.join(json_cols)}")
        else:
            print("No JSON-like columns found.")
    except Exception as e:
        print(f"Error occurred: {e}")
    return json_cols


def unpack_json_columns(df, json_cols):
    banner("UNPACKING JSON COLUMNS")
    new_dfs = []

    for col in json_cols:
        try:
            series = df[col].drop_nulls().cast(pl.Utf8)
            parsed = [try_parse_json(v) for v in series.to_list()]
            parsed = [p if isinstance(p, dict) else {} for p in parsed]
            unpacked_df = pl.DataFrame(parsed)
            unpacked_df.columns = [f"{col}_{c}" for c in unpacked_df.columns]
            new_dfs.append(unpacked_df)
        except Exception as e:
            print(f"Could not unpack column '{col}': {e}")

    if new_dfs:
        df = df.drop(json_cols)
        for part in new_dfs:
            df = df.hstack(part)

    print(f"Final shape: {df.shape[0]} rows × {df.shape[1]} columns")
    return df


def summarize_dataframe(df):
    banner("SUMMARY STATISTICS")
    summary = []

    for col in df.columns:
        dtype = df.schema[col]
        data = df[col]
        info = {"Column": col}

        if dtype in (pl.Int8, pl.Int16, pl.Int32, pl.Int64,
                     pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64,
                     pl.Float32, pl.Float64):
            desc = data.describe().to_dict(as_series=False)
            for stat in desc:
                info[stat] = desc[stat][0]
        else:
            non_nulls = [val for val in data.drop_nulls().to_list()
                         if not isinstance(val, (dict, list, set))]
            if non_nulls:
                try:
                    top_val, top_freq = Counter(non_nulls).most_common(1)[0]
                except:
                    top_val, top_freq = "Uncountable", 0
                info.update({
                    "count": len(non_nulls),
                    "unique": len(set(non_nulls)),
                    "top": f"{top_val} ({top_freq}x)"
                })
            else:
                info.update({
                    "count": 0,
                    "unique": 0,
                    "top": None
                })

        summary.append(info)

    pd_summary = pd.DataFrame(summary)
    print(pd_summary.to_string(index=False))


def main():
    df = load_csv()
    df=df[:10]
    json_cols = detect_json_columns(df)
    df = unpack_json_columns(df, json_cols)
    summarize_dataframe(df)


if __name__ == "__main__":
    main()
