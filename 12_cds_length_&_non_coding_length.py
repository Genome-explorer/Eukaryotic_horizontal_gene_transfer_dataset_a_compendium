#!/usr/bin/env python3
"""
Combined Script:
1. Reads gene sequences from a FASTA file
2. Updates column 6 (Coding_Sequence_length) in horizontal_gene_transfer_dataset.csv with lengths from FASTA (ignoring Ns)
3. Calculates non-coding sequence length (Full_Gene_Length - Coding_Sequence_Length)
4. Updates column 7 with the calculated non-coding sequence length
"""

import os
import re
import csv

def extract_accession_numbers(fasta_file):
    pattern = r'^>([^|\s]+)'
    accession_numbers = []
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                match = re.search(pattern, line.strip())
                if match:
                    accession_numbers.append(match.group(1))
    return accession_numbers

def get_gene_lengths(fasta_file):
    accession_numbers = extract_accession_numbers(fasta_file)
    gene_data = []
    current_seq = []
    current_id_index = 0

    with open(fasta_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_seq and current_id_index > 0:
                    sequence = ''.join(current_seq)
                    length = len(sequence) - sequence.upper().count('N')
                    gene_data.append((accession_numbers[current_id_index-1], length))
                if current_id_index < len(accession_numbers):
                    current_seq = []
                    current_id_index += 1
            else:
                current_seq.append(line)
        if current_seq and current_id_index > 0 and current_id_index <= len(accession_numbers):
            sequence = ''.join(current_seq)
            length = len(sequence) - sequence.upper().count('N')
            gene_data.append((accession_numbers[current_id_index-1], length))
    return gene_data

def update_csv_with_gene_lengths(csv_file, gene_data):
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

    data_rows = len(rows) - 1
    rows_to_update = min(data_rows, len(gene_data))

    for i in range(len(rows)):
        while len(rows[i]) < 6:
            rows[i].append("")

    for i in range(1, rows_to_update + 1):
        _, length = gene_data[i-1]
        rows[i][5] = str(length)

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False

def calculate_non_coding_lengths(csv_file):
    updated_rows = []

    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            updated_rows.append(header)

            for row_index, row in enumerate(reader, start=2):
                if len(row) < 7:
                    row.extend([''] * (7 - len(row)))

                try:
                    full_length = int(row[4].strip())
                    coding_length = int(row[5].strip())
                    non_coding_length = full_length - coding_length
                    row[6] = str(non_coding_length)
                except ValueError:
                    print(f"Row {row_index}: Invalid integer in columns 5 or 6")
                updated_rows.append(row)

    except Exception as e:
        print(f"Error reading CSV file for non-coding update: {e}")
        return []

    return updated_rows

def write_updated_csv(csv_file, updated_rows):
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(updated_rows)
        return True
    except Exception as e:
        print(f"Error writing final CSV file: {e}")
        return False

def main():
    print("Combined Gene Length Updater and Non-Coding Calculator")
    print("=======================================================")

    fasta_file = input("Enter the path to your CDS_gene.fasta FASTA file: ").strip()
    while not os.path.exists(fasta_file):
        fasta_file = input("File not found. Enter a valid FASTA file path: ").strip()

    csv_file = "horizontal_gene_transfer_dataset.csv"
    if not os.path.exists(csv_file):
        csv_file = input("Default CSV not found. Enter your CSV file path: ").strip()
        if not os.path.exists(csv_file):
            print("CSV file not found. Exiting.")
            return 1

    print("\nStep 1: Updating coding sequence lengths from FASTA...")
    gene_data = get_gene_lengths(fasta_file)
    if not gene_data:
        print("No gene data extracted. Exiting.")
        return 1

    success = update_csv_with_gene_lengths(csv_file, gene_data)
    if not success:
        print("Failed to update coding lengths. Exiting.")
        return 1
    print("Step 1 completed.")

    print("\nStep 2: Calculating non-coding sequence lengths...")
    updated_rows = calculate_non_coding_lengths(csv_file)
    if not updated_rows:
        print("Failed to calculate non-coding lengths. Exiting.")
        return 1

    confirm = input("Update CSV file with non-coding sequence lengths? [Y/n]: ").strip().lower()
    if confirm in ('n', 'no'):
        print("Operation cancelled.")
        return 0

    success = write_updated_csv(csv_file, updated_rows)
    if success:
        print("All updates completed successfully!")
    else:
        print("Failed to write final updated CSV.")

    return 0

if __name__ == "__main__":
    main()

