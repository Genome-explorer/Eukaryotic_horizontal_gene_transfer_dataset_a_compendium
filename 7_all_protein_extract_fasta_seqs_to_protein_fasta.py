#!/usr/bin/env python3
"""
Script that:
1. Scans a directory for all FASTA files
2. Extracts all sequences from each FASTA file
3. Combines them in order into a new FASTA file called protein.fasta
"""

import os
import glob
import argparse

def extract_and_combine_fasta(directory_path, output_file="protein.fasta"):
    """
    Extracts sequences from all FASTA files in a directory and combines them.
    
    Args:
        directory_path (str): Path to the directory containing FASTA files
        output_file (str): Name of the output FASTA file
        
    Returns:
        tuple: (success status, count of files processed, count of sequences extracted)
    """
    # Make sure the directory exists
    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' does not exist or is not a directory.")
        return False, 0, 0
    
    # Get all FASTA files in the directory (common extensions: .fa, .fasta, .fna, .ffn, .faa, .frn)
    fasta_files = []
    for ext in ["*.fa", "*.fasta", "*.fna", "*.ffn", "*.faa", "*.frn", "*.fas"]:
        fasta_files.extend(glob.glob(os.path.join(directory_path, ext)))
        # Also check for uppercase extensions
        fasta_files.extend(glob.glob(os.path.join(directory_path, ext.upper())))
    
    # Check if any FASTA files were found
    if not fasta_files:
        print(f"No FASTA files found in '{directory_path}'.")
        print("Supported extensions: .fa, .fasta, .fna, .ffn, .faa, .frn (and uppercase versions)")
        return False, 0, 0
    
    # Sort files for consistent ordering
    fasta_files.sort()
    
    # Process each FASTA file and combine sequences
    sequence_count = 0
    output_path = os.path.join(directory_path, output_file)
    
    try:
        with open(output_path, 'w') as outfile:
            for fasta_file in fasta_files:
                print(f"Processing: {os.path.basename(fasta_file)}")
                
                # Read and write sequences from the current file
                with open(fasta_file, 'r') as infile:
                    in_sequence = False
                    sequence_header = None
                    
                    for line in infile:
                        line = line.strip()
                        
                        # Skip empty lines
                        if not line:
                            continue
                            
                        # Handle sequence headers
                        if line.startswith('>'):
                            # Write the sequence header to the output file
                            outfile.write(f"{line}\n")
                            sequence_count += 1
                            in_sequence = True
                            sequence_header = line
                        elif in_sequence:
                            # Write sequence data to the output file
                            outfile.write(f"{line}\n")
        
        print(f"\nCombination complete!")
        print(f"- Processed {len(fasta_files)} FASTA files")
        print(f"- Extracted {sequence_count} sequences")
        print(f"- Output saved to: {output_path}")
        
        return True, len(fasta_files), sequence_count
    
    except Exception as e:
        print(f"Error processing FASTA files: {e}")
        return False, 0, 0


def main():
    """
    Main function to get user input and run the script.
    """
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(
        description="Combine sequences from all FASTA files in a directory into a single FASTA file."
    )
    parser.add_argument(
        "-d", "--directory", 
        help="Directory containing FASTA files (default: current directory)"
    )
    parser.add_argument(
        "-o", "--output", 
        default="protein.fasta",
        help="Name of output file (default: protein.fasta)"
    )
    args = parser.parse_args()
    
    print("FASTA Sequence Combiner")
    print("======================")
    print("\nThis script will combine all sequences from FASTA files in a directory into a single file called 'protein.fasta'.")
    
    # Always ask for directory path, regardless of command line arguments
    print("\nIMPORTANT: You need to provide the directory(folder) containing your protein FASTA files.")
    default_dir = args.directory if args.directory else os.getcwd()
    print(f"Default directory: {default_dir}")
    directory_path = input("Enter the path to the directory(folder) containing protein FASTA files: ").strip()
    
    # If user didn't provide input, use the default
    if not directory_path:
        directory_path = default_dir
        print(f"Using default directory: {directory_path}")
    
    # Get output filename
    output_file = args.output
    
    # Verify the directory path with the user
    print(f"\nDirectory: {directory_path}")
    print(f"Output file: {output_file}")
    confirm = input("\nContinue with these settings? [Y/n]: ").strip().lower()
    if confirm == 'n' or confirm == 'no':
        print("Operation cancelled by user")
        return 1
    
    # Process FASTA files
    success, file_count, seq_count = extract_and_combine_fasta(directory_path, output_file)
    
    if not success:
        return 1
    else:
        return 0


if __name__ == "__main__":
    main()

