#!/usr/bin/env python3
"""
Script that:
1. Takes a FASTA file as input
2. Extracts accession numbers from the FASTA headers
3. Calculates the length of each protein sequence (EXCLUDING '*' and non-letter chars)
4. Updates the horizontal_gene_transfer_dataset.csv file:
   - Accession numbers in the 3rd column (starting from the second row)
   - Protein lengths in the 8th column (Amino_Acid_sequence_length)
"""

import csv
import os
import re

# Amino acids to count; includes common ambiguous ones
_VALID_AA = set("ACDEFGHIKLMNPQRSTVWYBJOUXZ")

def protein_length(seq: str, include_stop: bool = False) -> int:
    """
    Count amino acids in a protein sequence.
    - Ignores whitespace, digits, punctuation, and gaps.
    - Excludes '*' by default.
    """
    # Keep only letters and optional '*'
    cleaned = re.sub(r'[^A-Za-z\*]', '', seq).upper()
    if not include_stop:
        cleaned = cleaned.replace('*', '')
    return sum(1 for ch in cleaned if ch in _VALID_AA)

def extract_accession_and_lengths(fasta_file):
    """
    Extract accession numbers and sequence lengths from a FASTA file.

    Returns list of tuples: (accession_number, sequence_length)
    """
    data = []
    pattern = r'^>([^|\s]+)'
    current_id = None
    current_seq = []

    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith('>'):
                if current_id is not None:
                    seq = ''.join(current_seq)
                    data.append((current_id, protein_length(seq)))
                match = re.search(pattern, line)
                current_id = match.group(1) if match else None
                current_seq = []
            else:
                current_seq.append(line)

        # flush last record
        if current_id is not None:
            seq = ''.join(current_seq)
            data.append((current_id, protein_length(seq)))

    print(f"Extracted {len(data)} protein IDs and lengths from {fasta_file}")
    return data

def update_csv(csv_file, fasta_data):
    """
    Update CSV file with accession numbers in column 3 and lengths in column 8.
    """
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return False

    try:
        with open(csv_file, 'r', newline='') as csvfile:
            rows = list(csv.reader(csvfile))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

    if len(rows) < 1:
        print("Error: CSV file is empty")
        return False

    for i, row in enumerate(rows):
        if len(row) < 8:
            print(f"Error: Row {i+1} has fewer than 8 columns")
            return False

    data_rows = len(rows) - 1
    update_count = min(len(fasta_data), data_rows)

    for i in range(update_count):
        accession, length = fasta_data[i]
        row_index = i + 1  # skip header
        rows[row_index][2] = accession            # column 3 (index 2)
        rows[row_index][7] = str(length)          # column 8 (index 7)

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)

        print(f"Successfully updated {update_count} rows with accession numbers and lengths in {csv_file}")
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False

def main():
    print("FASTA Processor and CSV Updater")
    print("===============================")

    fasta_file = input("Enter the path to your protein.fasta FASTA file: ").strip()
    while not os.path.exists(fasta_file):
        print(f"Error: The file '{fasta_file}' does not exist.")
        fasta_file = input("Please enter a valid path to your protein.fasta FASTA file (or type 'exit' to quit): ").strip()
        if fasta_file.lower() == 'exit':
            return 1

    use_default = input("Use default CSV file (horizontal_gene_transfer_dataset.csv)? [Y/n]: ").strip().lower()
    if use_default in ('n', 'no'):
        csv_file = input("Enter the path to your CSV file: ").strip()
        while not os.path.exists(csv_file):
            print(f"Error: The file '{csv_file}' does not exist.")
            csv_file = input("Please enter a valid path to your CSV file (or type 'default' to use the default): ").strip()
            if csv_file.lower() == 'default':
                csv_file = 'horizontal_gene_transfer_dataset.csv'
                break
    else:
        csv_file = 'horizontal_gene_transfer_dataset.csv'

    print(f"\nProcessing FASTA file: {fasta_file}")
    fasta_data = extract_accession_and_lengths(fasta_file)

    if not fasta_data:
        print("No valid protein data found. Exiting.")
        return 1

    print("\nUpdating CSV file...")
    success = update_csv(csv_file, fasta_data)

    print("\nOperation completed successfully!" if success else "\nOperation failed. Please check the error messages above.")
    return 0

if __name__ == "__main__":
    main()

