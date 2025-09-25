#!/usr/bin/env python3
"""
Script that:
1. Reads accession numbers from column 1 of horizontal_gene_transfer_dataset.csv
2. Selects the first 5, middle 5, and last 5 accession numbers
3. Extracts these sequences from a user-specified FASTA file
4. Calculates GC content for each sequence
5. Creates a new FASTA file with these sequences (including GC content in headers), separated by ###############
"""

import os
import re
import csv

def extract_accessions_from_csv(csv_file):
    """
    Extract accession numbers from the first column of a CSV file, 
    starting from the second row.
    
    Args:
        csv_file (str): Path to the CSV file
        
    Returns:
        list: List of accession numbers in the order they appear in the CSV file
    """
    accession_numbers = []
    
    try:
        with open(csv_file, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            # Skip the header row
            next(reader, None)
            # Extract accession numbers from column 1
            for row in reader:
                if row and row[0].strip():
                    accession_numbers.append(row[0].strip())
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []
    
    print(f"Found {len(accession_numbers)} accession numbers in {csv_file}")
    return accession_numbers


def select_accessions(accession_numbers):
    """
    Select the first 5, middle 5, and last 5 accession numbers from a list.
    
    Args:
        accession_numbers (list): List of accession numbers
        
    Returns:
        dict: Dictionary with three lists: first_5, middle_5, and last_5
    """
    if len(accession_numbers) < 15:
        print(f"Error: Not enough accession numbers ({len(accession_numbers)}) to select 15 total")
        return None
    
    # Select first 5
    first_5 = accession_numbers[:5]
    
    # Select middle 5
    mid_point = len(accession_numbers) // 2
    start_index = mid_point - 2
    middle_5 = accession_numbers[start_index:start_index+5]
    
    # Select last 5
    last_5 = accession_numbers[-5:]
    
    result = {
        "first_5": first_5,
        "middle_5": middle_5,
        "last_5": last_5
    }
    
    print("\nSelected accession numbers:")
    print(f"First 5: {', '.join(first_5)}")
    print(f"Middle 5: {', '.join(middle_5)}")
    print(f"Last 5: {', '.join(last_5)}")
    
    return result


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


def create_fasta_index(fasta_file):
    """
    Create an index of a FASTA file for faster sequence retrieval.
    Also calculates GC content for each sequence.
    
    Args:
        fasta_file (str): Path to the FASTA file
        
    Returns:
        dict: Dictionary mapping accession numbers to sequences with GC content info
    """
    index = {}
    pattern = r'^>([^|\s]+)'
    
    try:
        with open(fasta_file, 'r') as f:
            # Read the whole file and process line by line
            current_accession = None
            current_header = None
            current_sequence_lines = []
            sequence_content = []
            
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    # If we were collecting a sequence, calculate GC content and save it
                    if current_accession and current_header and sequence_content:
                        # Join all sequence parts
                        complete_sequence = ''.join(sequence_content)
                        # Calculate GC content
                        gc_content = calculate_gc_content(complete_sequence)
                        # Add GC content to header
                        modified_header = f"{current_header} GC Content: {gc_content}%"
                        # Store header and sequence
                        combined_lines = [modified_header] + current_sequence_lines
                        index[current_accession] = '\n'.join(combined_lines)
                    
                    # Start a new sequence
                    match = re.search(pattern, line)
                    if match:
                        current_accession = match.group(1)
                        current_header = line
                        current_sequence_lines = []
                        sequence_content = []
                elif current_accession:
                    # Add this line to the current sequence lines
                    current_sequence_lines.append(line)
                    # Also keep track of the actual sequence content for GC content calculation
                    sequence_content.append(line)
            
            # Don't forget the last sequence
            if current_accession and current_header and sequence_content:
                # Join all sequence parts
                complete_sequence = ''.join(sequence_content)
                # Calculate GC content
                gc_content = calculate_gc_content(complete_sequence)
                # Add GC content to header
                modified_header = f"{current_header} GC Content: {gc_content}%"
                # Store header and sequence
                combined_lines = [modified_header] + current_sequence_lines
                index[current_accession] = '\n'.join(combined_lines)
    
    except Exception as e:
        print(f"Error creating FASTA index: {e}")
        return {}
    
    print(f"Created index with {len(index)} entries from {fasta_file}")
    return index


def extract_sequence(fasta_file, accession, index):
    """
    Get a sequence from the index.
    
    Args:
        fasta_file (str): Path to the FASTA file (not used, kept for compatibility)
        accession (str): Accession number to extract
        index (dict): Dictionary mapping accession numbers to sequences
        
    Returns:
        str: FASTA entry (header + sequence) or None if not found
    """
    if accession not in index:
        return None
    
    return index[accession]


def create_output_fasta(selected_accessions, fasta_file, output_file):
    """
    Create a new FASTA file with selected sequences,
    separated by delimiter lines.
    
    Args:
        selected_accessions (dict): Dictionary with first_5, middle_5, and last_5 lists
        fasta_file (str): Path to the input FASTA file
        output_file (str): Path to the output FASTA file
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Create an index that stores the sequences with GC content
    index = create_fasta_index(fasta_file)
    
    # Check if index creation was successful
    if not index:
        print("Failed to create FASTA index")
        return False
    
    try:
        with open(output_file, 'w') as out_f:
            # Process each group
            for group_name, accessions in [
                ("First 5", selected_accessions["first_5"]),
                ("Middle 5", selected_accessions["middle_5"]),
                ("Last 5", selected_accessions["last_5"])
            ]:
                out_f.write(f"# {group_name}\n")
                
                # Extract and write each sequence in the group
                for i, acc in enumerate(accessions):
                    sequence = extract_sequence(fasta_file, acc, index)
                    if sequence:
                        out_f.write(f"{sequence}\n")
                    else:
                        out_f.write(f"# Sequence {acc} not found in FASTA file\n")
                
                # Add delimiter after each group of 5
                out_f.write("#################\n\n")
        
        print(f"Successfully created {output_file}")
        return True
    
    except Exception as e:
        print(f"Error creating output FASTA file: {e}")
        return False


def main():
    """
    Main function to run the script.
    """
    print("Selective FASTA Sequence Extractor with GC Content")
    print("=================================================")
    
    # Default input CSV file
    csv_file = "horizontal_gene_transfer_dataset.csv"
    
    # Verify CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: Default CSV file '{csv_file}' not found.")
        csv_file = input("Please enter the path to your CSV file: ").strip()
        if not os.path.exists(csv_file):
            print(f"Error: File '{csv_file}' not found. Exiting.")
            return 1
    
    # Extract accession numbers from CSV
    accession_numbers = extract_accessions_from_csv(csv_file)
    
    if not accession_numbers:
        print("No accession numbers found in the CSV file. Exiting.")
        return 1
    
    # Select first 5, middle 5, and last 5 accession numbers
    selected_accessions = select_accessions(accession_numbers)
    
    if not selected_accessions:
        print("Failed to select accession numbers. Exiting.")
        return 1
    
    # Ask user for FASTA file path
    fasta_file = input("Enter the path to your FASTA file: ").strip()
    
    # Validate that the file exists
    while not os.path.exists(fasta_file):
        print(f"Error: The file '{fasta_file}' does not exist.")
        fasta_file = input("Please enter a valid path to your FASTA file (or type 'exit' to quit): ").strip()
        if fasta_file.lower() == 'exit':
            return 1
    
    # Default output file name
    output_file = "Test_GC_content_Fulll_Gene_calculated_sequences.fasta"
    
    # Create the output FASTA file
    print(f"\nExtracting sequences from {fasta_file}")
    success = create_output_fasta(selected_accessions, fasta_file, output_file)
    
    if success:
        print("\nOperation completed successfully!")
        print(f"Selected sequences have been saved to {output_file}")
    else:
        print("\nOperation failed. Please check the error messages above.")
    
    return 0


if __name__ == "__main__":
    main()
