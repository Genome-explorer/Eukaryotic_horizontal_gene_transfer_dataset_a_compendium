#!/usr/bin/env python3
"""
Script that:
1. Takes a FASTA file containing gene sequences as input
2. Calculates the GC content of each gene sequence (ignoring N characters)
3. Updates the 9th column (G+C_content) of the CSV file sequentially without matching
"""

import os
import re
import csv

def extract_accession_numbers(fasta_file):
    """
    Extract accession numbers from a FASTA file.
    
    Assumes the accession number is at the beginning of each FASTA header line
    (lines starting with '>'), typically followed by a space or pipe.
    
    Args:
        fasta_file (str): Path to the FASTA file
        
    Returns:
        list: List of accession numbers in the order they appear in the FASTA file
    """
    accession_numbers = []
    
    # Common patterns for accession numbers in FASTA headers
    pattern = r'^>([^|\s]+)'
    
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                match = re.search(pattern, line.strip())
                if match:
                    # Extract just the accession number from the FASTA header
                    accession = match.group(1)
                    accession_numbers.append(accession)
    
    print(f"Found {len(accession_numbers)} gene accession numbers in {fasta_file}")
    return accession_numbers


def calculate_gc_content(dna_sequence):
    """
    Calculate the GC content of a DNA sequence, ignoring 'N' bases.

    Parameters:
    dna_sequence (str): The DNA sequence.

    Returns:
    float: The GC content as a percentage.
    """
    # Convert the sequence to uppercase and remove 'N' bases
    dna_sequence = dna_sequence.upper().replace('N', '')

    # Count the number of G and C bases
    g_count = dna_sequence.count('G')
    c_count = dna_sequence.count('C')

    # Total length of the sequence (excluding 'N')
    total_length = len(dna_sequence)

    # Avoid division by zero if the sequence is empty
    if total_length == 0:
        return 0.0

    # Calculate GC content
    gc_content = round(((g_count + c_count) / total_length) * 100, 2)
    
    return gc_content


def get_gene_gc_contents(fasta_file):
    """
    Calculate the GC content of gene sequences in a FASTA file,
    ignoring 'N' characters in the calculation.
    
    Args:
        fasta_file (str): Path to the FASTA file
        
    Returns:
        list of tuples: Each tuple contains (accession_number, gc_content)
    """
    # First, extract the accession numbers
    accession_numbers = extract_accession_numbers(fasta_file)
    
    # Now parse the file to get sequences and calculate GC content
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
                    # Save the previous sequence if it exists
                    if current_seq and current_id_index > 0:
                        sequence = ''.join(current_seq)
                        # Calculate GC content
                        gc_content = calculate_gc_content(sequence)
                        gene_data.append((accession_numbers[current_id_index-1], gc_content))
                    
                    # Move to the next ID
                    if current_id_index < len(accession_numbers):
                        current_seq = []
                        current_id_index += 1
                    else:
                        print("Warning: More sequences in file than extracted accession numbers")
                else:
                    # Add this line to the current sequence
                    current_seq.append(line)
            
            # Don't forget the last sequence
            if current_seq and current_id_index > 0 and current_id_index <= len(accession_numbers):
                sequence = ''.join(current_seq)
                # Calculate GC content
                gc_content = calculate_gc_content(sequence)
                gene_data.append((accession_numbers[current_id_index-1], gc_content))
                
        print(f"Calculated GC content for {len(gene_data)} gene sequences")
        return gene_data
        
    except Exception as e:
        print(f"Error parsing FASTA file: {e}")
        return []


def update_csv_with_gc_content_sequentially(csv_file, gene_data):
    """
    Update the CSV file with GC content in the 9th column sequentially,
    without checking for matches between accessions.
    
    Args:
        csv_file (str): Path to the CSV file
        gene_data (list): List of tuples (accession_number, gc_content)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        return False
    
    # Read the current CSV data
    try:
        rows = []
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False
    
    # Check if we have a header row
    if len(rows) < 1:
        print("Error: CSV file is empty")
        return False
    
    # Calculate how many rows to update (excluding header)
    data_rows = len(rows) - 1  # Exclude header
    gc_data_count = len(gene_data)
    rows_to_update = min(data_rows, gc_data_count)
    
    print(f"\nUpdate information:")
    print(f"- CSV data rows (excluding header): {data_rows}")
    print(f"- Available GC content values: {gc_data_count}")
    print(f"- Rows that will be updated: {rows_to_update}")
    
    if rows_to_update < data_rows:
        print(f"Warning: Not enough GC content values to update all rows (missing {data_rows - rows_to_update})")
    elif gc_data_count > data_rows:
        print(f"Warning: {gc_data_count - data_rows} GC content values will not be used")
    
    # Ensure each row has at least 9 columns
    for i in range(len(rows)):
        while len(rows[i]) < 9:
            rows[i].append("")
    
    # Update the 9th column (index 8) with GC content sequentially
    print("\nUpdating GC content in CSV file sequentially...")
    
    for i in range(1, rows_to_update + 1):  # Skip the header row
        # Get the GC content for this index
        _, gc_content = gene_data[i-1]
        rows[i][8] = str(gc_content)
    
    # Write the updated data back to the CSV file
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
        print(f"Successfully updated {rows_to_update} rows with GC content in {csv_file}")
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False


def main():
    """
    Main function to get user input and run the script.
    """
    print("GC Content Calculator for HGT Dataset")
    print("====================================")
    
    # Ask user for FASTA file path
    fasta_file = input("Enter the path to your full_gene.fasta FASTA file: ").strip()
    
    # Validate that the file exists
    while not os.path.exists(fasta_file):
        print(f"Error: The file '{fasta_file}' does not exist.")
        fasta_file = input("Please enter a valid path to your full_gene.fasta FASTA file (or type 'exit' to quit): ").strip()
        if fasta_file.lower() == 'exit':
            return 1
    
    # Ask user for CSV file path or use default
    use_default = input("Use default CSV file (horizontal_gene_transfer_dataset.csv)? [Y/n]: ").strip().lower()
    
    if use_default == 'n' or use_default == 'no':
        csv_file = input("Enter the path to your CSV file: ").strip()
        # Validate that the CSV file exists
        while not os.path.exists(csv_file):
            print(f"Error: The file '{csv_file}' does not exist.")
            csv_file = input("Please enter a valid path to your CSV file (or type 'default' to use the default): ").strip()
            if csv_file.lower() == 'default':
                csv_file = 'horizontal_gene_transfer_dataset.csv'
                break
    else:
        csv_file = 'horizontal_gene_transfer_dataset.csv'
    
    # Parse the FASTA file and get gene data with GC content
    print(f"\nProcessing FASTA file: {fasta_file}")
    gene_data = get_gene_gc_contents(fasta_file)
    
    if not gene_data:
        print("No gene sequences found in the FASTA file. Exiting.")
        return 1
    
    # Print some sample data
    print("\nSample of GC content values:")
    for i, (gene_id, gc_content) in enumerate(gene_data[:5]):
        print(f"{gene_id}: {gc_content}% GC content")
    if len(gene_data) > 5:
        print(f"... and {len(gene_data) - 5} more")
    
    # Update the CSV file with GC content values sequentially
    print(f"\nUpdating CSV file: {csv_file}")
    success = update_csv_with_gc_content_sequentially(csv_file, gene_data)
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation failed. Please check the error messages above.")
    
    return 0


if __name__ == "__main__":
    main()
