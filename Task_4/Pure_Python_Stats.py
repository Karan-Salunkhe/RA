import csv
import ast
import math
import os
from collections import Counter, defaultdict
from shutil import get_terminal_size


def banner(text):
    print("\n" + "—" * (len(text) + 4))
    print(f"| {text} |")
    print("—" * (len(text) + 4))


def detect_structured_columns(path):
    """Identify columns with JSON-like structure (not proper flat CSV)."""
    with open(path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        first_row = next(reader, None)
        if not first_row:
            return []
        return [col for col, val in first_row.items() if val and "{" in val and "}" in val]


def load_data_loose(path):
    """Load and flatten rows with nested structures."""
    with open(path, encoding='utf-8') as raw:
        scan = csv.DictReader(raw)
        basket = []
        for i, row in enumerate(scan, 1):
            fused = {}
            for label, val in row.items():
                if val and "{" in val and "}" in val:
                    try:
                        obj = ast.literal_eval(val)
                        if isinstance(obj, dict):
                            for reg, stat in obj.items():
                                if isinstance(stat, dict):
                                    for metric, number in stat.items():
                                        fused[f"{reg}_{metric}"] = number
                                else:
                                    fused[f"{label}_{reg}"] = stat
                        else:
                            fused[label] = val
                    except:
                        fused[label] = val
                else:
                    fused[label] = val
            basket.append(fused)
            if i % 200 == 0:
                print(f"Processed {i} rows...")
        print(f"\n Finished unpacking {i} rows.\n")
        return basket


def side_by_side_stats(col_stats):
    """Display numeric stats in side-by-side format."""
    headers = ["Column", "Count", "Mean", "Min", "Max", "StdDev"]
    col_width = max(len(h) for h in headers) + 2
    row_format = "".join([f"{{:<{col_width}}}" for _ in headers])

    print("\n" + "=" * get_terminal_size((80, 20)).columns)
    print(row_format.format(*headers))
    print("-" * get_terminal_size((80, 20)).columns)

    for stat in col_stats:
        print(row_format.format(*stat))


def messy_stats(stack):
    column_map = defaultdict(list)

    for doc in stack:
        for slot, token in doc.items():
            column_map[slot].append(token)

    print(f"\n Total Columns: {len(column_map)}")

    numeric_summary = []
    text_summary = []

    for head, bag in column_map.items():
        nums = []
        texts = []

        for bit in bag:
            try:
                nums.append(float(bit))
            except:
                if bit not in ('', None):
                    texts.append(str(bit))

        if nums:
            c = len(nums)
            m = sum(nums) / c
            s = math.sqrt(sum((x - m) ** 2 for x in nums) / c) if c > 1 else 0
            numeric_summary.append([head, str(c), f"{m:.2f}", str(min(nums)), str(max(nums)), f"{s:.2f}"])
        elif texts:
            cluster = Counter(texts)
            common = cluster.most_common(1)[0]
            text_summary.append((head, len(texts), len(cluster), f"{common[0]} ({common[1]}x)"))

    if numeric_summary:
        banner(" NUMERIC SUMMARY")
        side_by_side_stats(numeric_summary)

    if text_summary:
        banner(" TEXT COLUMNS")
        for head, count, uniq, top in text_summary:
            print(f"\n {head}")
            print(f" ↳ Count: {count}")
            print(f" ↳ Unique: {uniq}")
            print(f" ↳ Top: {top}")


def group_data(data, group_keys):
    grouped = defaultdict(list)

    for row in data:
        key = tuple(row.get(col, "MISSING") for col in group_keys)
        grouped[key].append(row)

    reduced = []

    for key, group_rows in grouped.items():
        agg_row = dict(zip(group_keys, key))  # Group columns

        temp_bucket = defaultdict(list)
        for row in group_rows:
            for k, v in row.items():
                if k not in group_keys:
                    temp_bucket[k].append(v)

        for k, vals in temp_bucket.items():
            try:
                numeric_vals = [float(x) for x in vals if isinstance(x, (int, float)) or str(x).replace('.', '', 1).isdigit()]
                if numeric_vals:
                    agg_row[k] = round(sum(numeric_vals) / len(numeric_vals), 2)
                else:
                    agg_row[k] = Counter([str(v) for v in vals if v not in ('', None)]).most_common(1)[0][0]
            except:
                agg_row[k] = vals[0]

        reduced.append(agg_row)

    return reduced


#  Main logic
if __name__ == "__main__":
    banner("Smart CSV Analyzer")

    user_file = input(" Enter path to your CSV file: ").strip().strip('"')

    if not os.path.isfile(user_file):
        print(" File not found. Please double-check your input.")
    elif not user_file.endswith(".csv"):
        print(" Only .csv files are supported.")
    else:
        try:
            banner(" Detecting malformed columns")
            bad_cols = detect_structured_columns(user_file)
            if bad_cols:
                print(f" Columns with non-flat data: {', '.join(bad_cols)}")
            else:
                print(" All columns are flat CSV-style.")

            banner(" Loading and Flattening Data")
            original_data = load_data_loose(user_file)

            banner("DATA ANALYSIS")
            messy_stats(original_data)

            # Ask about aggregation
            banner("Aggregation Options")
            want_group = input(" Do you want to group (aggregate) the data? (yes/no): ").strip().lower()

            if want_group in ["yes", "y"]:
                while True:
                    try:
                        count = int(input("How many columns do you want to group by? "))
                        if count < 1:
                            raise ValueError
                        break
                    except:
                        print("Please enter a valid number greater than 0.")

                group_columns = []
                for i in range(count):
                    col = input(f"🔹 Enter column name #{i + 1} to group by: ").strip()
                    group_columns.append(col)

                print(f"\n Grouping by: {', '.join(group_columns)}")
                grouped_data = group_data(original_data, group_columns)

                banner("ANALYSIS ON AGGREGATED DATA")
                messy_stats(grouped_data)

            else:
                print("Skipped grouping. Task complete.")

        except Exception as error:
            print(f"Error during execution: {error}")
