#!/usr/bin/env python3
"""
Script that:
1. Prompts for source and target CSV files
2. Reads both (skipping header in source)
3. Appends source data after target data
4. Preserves NaN / N/A values as visible "N/A" in output
5. Writes result to new CSV using target's header
"""

import os
import pandas as pd

def read_data_excluding_header(csv_path):
    """
    Read CSV excluding the header row, keeping NaN/N/A values intact.
    """
    try:
        df = pd.read_csv(csv_path, skiprows=1, header=None, keep_default_na=True)
        return df
    except Exception as e:
        print(f"Error reading {csv_path}: {e}")
        return pd.DataFrame()

def merge_csvs_preserve_na(source_path, target_path, output_path):
    """
    Appends source CSV data to target CSV, preserving all missing values
    and writing them as 'N/A' in the output CSV.
    """
    try:
        # Read target with header
        target_df = pd.read_csv(target_path, keep_default_na=True)
        source_df = read_data_excluding_header(source_path)

        target_cols = len(target_df.columns)
        source_cols = len(source_df.columns)

        # Adjust column count
        if source_cols > target_cols:
            source_df = source_df.iloc[:, :target_cols]
            print(f"Note: Truncated {source_cols - target_cols} extra column(s) from source.")
        elif source_cols < target_cols:
            for i in range(source_cols, target_cols):
                source_df[i] = pd.NA
            print(f"Note: Added {target_cols - source_cols} empty column(s) to source.")

        # Match column names
        source_df.columns = target_df.columns

        # Combine target + source (target first)
        merged_df = pd.concat([target_df, source_df], ignore_index=True)

        # Write CSV with visible 'N/A' for missing values
        merged_df.to_csv(output_path, index=False, na_rep="N/A")

        print(f"\n✅ Merged CSV written to: {output_path}")
        print(f"→ Original target rows: {len(target_df)}")
        print(f"→ Appended source rows: {len(source_df)}")
        print(f"→ Total rows in output: {len(merged_df)}")

        return True
    except Exception as e:
        print(f"Merge failed: {e}")
        return False

def main():
    print("📎 CSV Merger — Append + Preserve Missing Values")
    print("===============================================")

    source_path = input("Enter path to source CSV (new data): ").strip()
    while not os.path.isfile(source_path):
        print("Invalid file. Try again.")
        source_path = input("Re-enter path to source CSV: ").strip()

    target_path = input("Enter path to target CSV (existing data): ").strip()
    while not os.path.isfile(target_path):
        print("Invalid file. Try again.")
        target_path = input("Re-enter path to target CSV: ").strip()

    output_name = input("Enter name for output CSV (e.g., merged.csv): ").strip()
    if not output_name.endswith(".csv"):
        output_name += ".csv"

    output_dir = os.path.dirname(target_path) or os.getcwd()
    output_path = os.path.join(output_dir, output_name)

    if os.path.exists(output_path):
        overwrite = input(f"{output_path} exists. Overwrite? [y/N]: ").strip().lower()
        if overwrite not in ['y', 'yes']:
            print("Cancelled.")
            return

    merge_csvs_preserve_na(source_path, target_path, output_path)

if __name__ == "__main__":
    main()

