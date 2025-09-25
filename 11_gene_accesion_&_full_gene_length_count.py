#!/usr/bin/env python3
"""
Combined script that:
1. Takes a FASTA file containing gene sequences as input
2. Extracts accession numbers from the FASTA headers
3. Sequentially updates the 1st column of the CSV file with these accession numbers
4. Calculates the length of each gene sequence (ignoring N characters)
5. Updates the 5th column (Full_Gene_Length) of the CSV file where matches are found
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

    print(f"Found {len(accession_numbers)} gene accession numbers in {fasta_file}")
    return accession_numbers

def update_csv_sequentially(csv_file, gene_accessions):
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return False

    try:
        with open(csv_file, 'r', newline='') as csvfile:
            rows = list(csv.reader(csvfile))
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

    if not rows:
        print("Error: CSV file is empty.")
        return False

    data_rows = len(rows) - 1
    accessions_available = len(gene_accessions)
    rows_to_update = min(data_rows, accessions_available)

    print(f"\nUpdating CSV accessions:")
    print(f"- Rows to update: {rows_to_update}")
    if rows_to_update < data_rows:
        print(f"Warning: Missing {data_rows - rows_to_update} accession numbers.")
    elif accessions_available > data_rows:
        print(f"Warning: {accessions_available - data_rows} accessions will be unused.")

    for i in range(1, rows_to_update + 1):
        rows[i][0] = gene_accessions[i - 1]

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            csv.writer(csvfile).writerows(rows)
        print(f"Updated {rows_to_update} accession numbers in {csv_file}")
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False

def get_gene_lengths(fasta_file):
    accession_numbers = extract_accession_numbers(fasta_file)
    gene_data = []
    current_seq = []
    current_id_index = 0

    try:
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

        print(f"Calculated lengths for {len(gene_data)} sequences")
        return gene_data

    except Exception as e:
        print(f"Error parsing FASTA: {e}")
        return []

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
        print("Error: CSV is empty")
        return False

    for i, row in enumerate(rows):
        if len(row) < 5:
            print(f"Error: Row {i+1} has fewer than 5 columns")
            return False

    if len(rows) > 1 and not rows[1][0].strip():
        print("Error: Empty accession number in column 1, row 2")
        return False

    gene_length_dict = {acc: length for acc, length in gene_data}
    num_rows_to_process = min(len(rows) - 1, len(gene_data))

    print(f"\nMatching gene accessions to update lengths for {num_rows_to_process} rows")
    update_count = 0
    not_found_count = 0

    for i in range(1, num_rows_to_process + 1):
        csv_acc = rows[i][0].strip()
        if csv_acc in gene_length_dict:
            rows[i][4] = str(gene_length_dict[csv_acc])
            update_count += 1
        else:
            not_found_count += 1
            print(f"No match for accession '{csv_acc}' at row {i+1}")

    print(f"\nUpdated {update_count} rows with gene lengths")
    if not_found_count > 0:
        confirm = input("Proceed with partial update? [Y/n]: ").strip().lower()
        if confirm == 'n' or confirm == 'no':
            print("Cancelled by user.")
            return False

    try:
        with open(csv_file, 'w', newline='') as csvfile:
            csv.writer(csvfile).writerows(rows)
        print(f"Successfully updated gene lengths in {csv_file}")
        return True
    except Exception as e:
        print(f"Error writing CSV: {e}")
        return False

def main():
    print("Combined Gene Accession + Length Updater")
    print("========================================")

    fasta_file = input("Enter path to your gene FASTA file: ").strip()
    while not os.path.exists(fasta_file):
        fasta_file = input("Invalid FASTA file path. Try again or type 'exit': ").strip()
        if fasta_file.lower() == 'exit':
            return

    use_default = input("Use default CSV file (horizontal_gene_transfer_dataset.csv)? [Y/n]: ").strip().lower()
    if use_default in ['n', 'no']:
        csv_file = input("Enter the path to your CSV file: ").strip()
        while not os.path.exists(csv_file):
            csv_file = input("Invalid CSV file path. Try again or type 'default': ").strip()
            if csv_file.lower() == 'default':
                csv_file = 'horizontal_gene_transfer_dataset.csv'
                break
    else:
        csv_file = 'horizontal_gene_transfer_dataset.csv'

    print(f"\nExtracting accession numbers from {fasta_file}...")
    gene_accessions = extract_accession_numbers(fasta_file)

    if not gene_accessions:
        print("No accessions found. Exiting.")
        return

    print(f"\nUpdating accession numbers in CSV file: {csv_file}")
    if not update_csv_sequentially(csv_file, gene_accessions):
        return

    print(f"\nCalculating gene lengths from {fasta_file}...")
    gene_data = get_gene_lengths(fasta_file)

    print(f"\nUpdating gene lengths in CSV file: {csv_file}")
    update_csv_with_gene_lengths(csv_file, gene_data)

if __name__ == "__main__":
    main()

