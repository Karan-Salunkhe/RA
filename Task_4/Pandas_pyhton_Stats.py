import pandas as pd
import ast
import os
from shutil import get_terminal_size


def banner(text):
    print("\n" + "—" * (len(text) + 4))
    print(f"| {text} |")
    print("—" * (len(text) + 4))


def detect_non_flat_columns(df):
    """Return a list of column names that appear to contain JSON/dict structures."""
    bad_cols = []
    for col in df.columns:
        if df[col].astype(str).str.contains(r'^\s*{.*}\s*$', na=False).any():
            bad_cols.append(col)
    return bad_cols


def load_and_unpack(file_path):
    """
    Load a CSV file and unpack JSON-like columns, while preserving all other columns.
    """
    df = pd.read_csv(file_path)
    unpacked_cols = []

    for col in df.columns:
        if df[col].astype(str).str.contains(r'^\s*{.*}\s*$', na=False).any():
            try:
                parsed = df[col].dropna().apply(ast.literal_eval)
                if parsed.apply(lambda x: isinstance(x, dict)).all():
                    normalized = pd.json_normalize(parsed)
                    normalized.columns = [
                        f"{col}_{sub.replace(' ', '_').replace('.', '_')}" for sub in normalized.columns
                    ]
                    df = pd.concat([df.drop(columns=[col]), normalized], axis=1)
                    unpacked_cols.append(col)
            except Exception:
                continue

    return df, unpacked_cols


def display_numeric_summary(df):
    """Show side-by-side summary stats for numeric columns."""
    numeric_df = df.select_dtypes(include='number')
    if numeric_df.empty:
        print("No numeric columns found.")
        return

    desc = numeric_df.describe().transpose()
    desc = desc[["count", "mean", "min", "max", "std"]].round(2)
    desc.reset_index(inplace=True)
    desc.columns = ["Column", "Count", "Mean", "Min", "Max", "StdDev"]

    col_widths = [max(len(str(x)) for x in desc[col]) + 2 for col in desc.columns]
    row_format = "".join([f"{{:<{w}}}" for w in col_widths])

    print("\n" + "=" * get_terminal_size((80, 20)).columns)
    print(row_format.format(*desc.columns))
    print("-" * get_terminal_size((80, 20)).columns)

    for _, row in desc.iterrows():
        print(row_format.format(*row))


def display_text_summary(df):
    """Show summary stats for non-numeric columns."""
    text_cols = df.select_dtypes(include='object')

    for col in text_cols.columns:
        print(f"\n {col}")
        count = text_cols[col].count()
        unique = text_cols[col].nunique()
        top_val = text_cols[col].value_counts().idxmax()
        top_freq = text_cols[col].value_counts().max()

        print(f" ↳ Count: {count}")
        print(f" ↳ Unique: {unique}")
        print(f" ↳ Top: {top_val} ({top_freq}x)")


def summarize_dataframe(df):
    """Print stats for both numeric and text columns."""
    banner(" SUMMARY STATISTICS")
    display_numeric_summary(df)
    display_text_summary(df)


def group_dataframe(df):
    """Prompt for grouping columns and return aggregated DataFrame."""
    choice = input("\n Do you want to group (aggregate) the data? (yes/no): ").strip().lower()
    if choice not in ["yes", "y"]:
        print(" Skipping aggregation.")
        return None

    try:
        while True:
            try:
                n = int(input(" How many columns do you want to group by? "))
                if n < 1:
                    raise ValueError
                break
            except ValueError:
                print(" Please enter a number greater than 0.")

        group_cols = []
        for i in range(n):
            while True:
                col = input(f" Enter column name #{i + 1} to group by: ").strip()
                if col not in df.columns:
                    print(f" Column '{col}' not found. Try again.")
                else:
                    group_cols.append(col)
                    break

        print(f"\n Grouping by: {', '.join(group_cols)}")

        numeric_cols = df.select_dtypes(include='number').columns.difference(group_cols)
        if numeric_cols.empty:
            print(" No numeric columns to aggregate.")
            return None

        grouped_df = df.groupby(group_cols)[numeric_cols].mean().reset_index()

        banner(" AGGREGATED DATA ANALYSIS")
        summarize_dataframe(grouped_df)
        return grouped_df

    except Exception as e:
        print(f" Grouping failed: {e}")
        return None


def main():
    banner(" PANDAS CSV ANALYZER")

    file_path = input(" Enter path to your CSV file: ").strip().strip('"')

    if not os.path.isfile(file_path):
        print(" File not found. Please check the path.")
        return

    try:
        banner(" ANALYZING COLUMN FORMATS")
        raw_df = pd.read_csv(file_path)
        bad_cols = detect_non_flat_columns(raw_df)

        if bad_cols:
            print(f" Non-flat (possibly JSON) columns detected: {', '.join(bad_cols)}")
        else:
            print(" All columns appear flat (CSV-friendly).")

        banner(" LOADING + UNPACKING DATA")
        df, unpacked = load_and_unpack(file_path)
        print(f" Data loaded: {df.shape[0]} rows × {df.shape[1]} columns")

        if unpacked:
            print(f" Unpacked columns: {', '.join(unpacked)}")
        else:
            print("ℹ No JSON-like columns were unpacked.")

        summarize_dataframe(df)
        group_dataframe(df)

    except Exception as e:
        print(f" Something went wrong: {e}")


if __name__ == "__main__":
    main()
