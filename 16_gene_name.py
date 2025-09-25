#!/usr/bin/env python3
"""
Script that:
1. Takes a FASTA file containing protein sequences as input
2. Extracts protein names from the FASTA headers
3. Inserts the protein names into the 4th column of a CSV file (starting from row 1, after header)
"""

import os
import re
import csv

def extract_protein_names(fasta_file):
    """
    Extract protein names from a FASTA file.
    
    This function extracts the descriptive part of the FASTA header (typically
    the protein name/description) that appears after the accession number.
    
    Args:
        fasta_file (str): Path to the FASTA file
        
    Returns:
        list: List of protein names in the order they appear in the FASTA file
    """
    protein_names = []
    
    # Pattern to extract protein name/description after the accession number
    # This assumes accession is followed by space or pipe, then the protein name
    pattern = r'^>[^|\s]+[\s|]+(.+)$'
    
    with open(fasta_file, 'r') as f:
        for line in f:
            if line.startswith('>'):
                match = re.search(pattern, line.strip())
                if match:
                    # Extract the protein name/description
                    protein_name = match.group(1)
                    protein_names.append(protein_name)
                else:
                    # If pattern doesn't match but it's a header line, take everything after '>'
                    protein_names.append(line.strip()[1:])
    
    print(f"Found {len(protein_names)} protein names in {fasta_file}")
    return protein_names


def update_csv_with_protein_names(csv_file, protein_names):
    """
    Update the CSV file by inserting protein names into the 4th column (index 3).
    
    Args:
        csv_file (str): Path to the CSV file
        protein_names (list): List of protein names from FASTA file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found at {csv_file}")
        print(f"Please create the CSV file first and try again.")
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
    
    # Check if the file has at least a header row
    if not rows:
        print("Error: CSV file is empty. Please add at least a header row.")
        return False
    
    # Determine how many rows to update (excluding header)
    data_rows = len(rows) - 1  # Exclude header
    names_available = len(protein_names)
    rows_to_update = min(data_rows, names_available)
    
    print(f"\nUpdate information:")
    print(f"- CSV data rows (excluding header): {data_rows}")
    print(f"- Available protein names: {names_available}")
    print(f"- Rows that will be updated: {rows_to_update}")
    
    if rows_to_update < data_rows:
        print(f"Warning: Not enough protein names to update all rows (missing {data_rows - rows_to_update})")
    elif names_available > data_rows:
        print(f"Warning: {names_available - data_rows} protein names will not be used")
    
    # Make sure each row has enough columns (at least 4)
    for i in range(len(rows)):
        while len(rows[i]) < 4:
            rows[i].append("")
    
    # Update the 4th column (index 3) with protein names sequentially
    for i in range(1, rows_to_update + 1):  # Skip the header row
        rows[i][3] = protein_names[i-1]
    
    # Write the updated data back to the CSV file
    try:
        with open(csv_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
        print(f"Successfully updated {rows_to_update} rows with protein names in {csv_file}")
        return True
    except Exception as e:
        print(f"Error writing to CSV file: {e}")
        return False


def main():
    """
    Main function to get user input and run the script.
    """
    print("FASTA Protein Name to CSV Updater")
    print("=================================")
    print("\nThis script will extract protein names from a FASTA file and add them to the 4th column of your CSV.")
    
    # Explicitly ask user for FASTA file path
    print("\nIMPORTANT: You need to provide the path to your FASTA file.")
    fasta_file = input("Enter the path to your protein FASTA file: ").strip()
    
    # Validate that the file exists
    while not os.path.exists(fasta_file):
        print(f"Error: The file '{fasta_file}' does not exist.")
        fasta_file = input("Please enter a valid path to your FASTA file (or type 'exit' to quit): ").strip()
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
    
    # Extract protein names from FASTA file
    print(f"\nProcessing FASTA file: {fasta_file}")
    protein_names = extract_protein_names(fasta_file)
    
    if not protein_names:
        print("No protein names found in the FASTA file. Exiting.")
        return 1
    
    # Print some sample data
    print("\nSample of protein names:")
    for i, name in enumerate(protein_names[:3]):
        print(f"{i+1}. {name}")
    if len(protein_names) > 3:
        print(f"... and {len(protein_names) - 3} more")
    
    # Update the CSV file with protein names
    print(f"\nUpdating CSV file: {csv_file}")
    success = update_csv_with_protein_names(csv_file, protein_names)
    
    if success:
        print("\nOperation completed successfully!")
    else:
        print("\nOperation failed. Please check the messages above.")
    
    return 0


if __name__ == "__main__":
    main()
