#!/usr/bin/env python3
"""
Script to generate a CSV file for horizontal gene transfer data with specified columns:
- Gene_accession_number(Genome_assembly_accession_number/Database_accession_number)
- Genome_assembly_ID
- Protein_accession_number
- Gene_Name/Function
- Full_Gene_Length
- Coding_Sequence_length(CDS)
- Non_Coding_sequence_length(5'UTR,3'UTR,intron)
- Amino_Acid_sequence_length(aa)
- G+C_content_Full_Gene
- G+C_content_CDS
- Phylogenetic_support(n/a=not_tested, N= no, Y=Yes)
- level_of_certainty
- Taxon_Donor(Bacteria,Protist,Fungi,Archaea,Unknown)
- Taxon_receiver(By_Phylum)
- Receiver_Genus_species
- PMCID/PMID/DOI
- Publish_Year
- Paper
"""
import csv
import os
from datetime import datetime

def create_csv_with_empty_rows(filename="horizontal_gene_transfer_dataset.csv", num_rows=5000):
    """Create a CSV file with headers and specified number of empty data rows."""
    
    # Define the column order
    columns = [
        "Gene_accession_number(Genome_assembly_accession_number/Database_accession_number)",
        "Genome_assembly_ID",
        "Protein_accession_number",
        "Gene_Name/Function",
        "Full_Gene_Length",
        "Coding_Sequence_length(CDS)",
        "Non_Coding_sequence_length(5'UTR,3'UTR,intron)",
        "Amino_Acid_sequence_length(aa)",
	"G+C_content_Full_Gene",
	"G+C_content_CDS",
	"Phylogenetic_support(n/a=not_tested, N= no, Y=Yes)",
        "level_of_certainty",
        "Taxon_Donor(Bacteria,Protist,Fungi,Archaea,Unknown)",
        "Taxon_receiver(By_Phylum)",
        "Receiver_Genus_species",
        "PMCID/PMID/DOI",
        "Publish_Year",
	"Paper",
    ]
    
    # Write the headers and empty rows to the CSV file
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the header row
        writer.writerow(columns)
        
        # Write empty data rows
        empty_row = [''] * len(columns)
        for _ in range(num_rows):
            writer.writerow(empty_row)
    
    return filename

def main():
    """Main function to run the script."""
    
    # Name of the output dataset
    filename = "horizontal_gene_transfer_dataset.csv"
    
    # Number of empty data rows to create
    num_rows = 5000
    
    print(f"Creating CSV file with headers and {num_rows} empty data rows...")
    
    # Create the CSV file with headers and empty rows
    output_file = create_csv_with_empty_rows(filename, num_rows)
    
    print(f"CSV file created successfully: {output_file}")
    print(f"File contains headers plus {num_rows} empty data rows ({num_rows + 1} rows total)")
    
    # Display file size information
    file_size = os.path.getsize(output_file)
    print(f"File size: {file_size / 1024:.2f} KB")

if __name__ == "__main__":
    main()
