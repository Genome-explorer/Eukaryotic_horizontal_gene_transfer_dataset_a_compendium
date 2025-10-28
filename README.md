

# Eukaryotic_horizontal_gene_transfer_dataset_a_compendium
***All the code used to create the dataset for this project***

### 1 ) This script creates 3 directories (folders) to store your full gene fasta files, Coding sequence fasta files, and protein sequence fasta files
1_make_new_directories.py
### To run this file make sure you have python installed
    python3 1_make_new_directories.py
***Move all full gene fasta files to full_gene directory(folder), move all Coding Sequence fasta files to CDS directory(folder), and move all protein fasta files to proteins** 

### 2 ) This script adds full gene at the end of each of the fasta files in the full gene directory
2_add_full_gene_at_the_end_of_each_fasta_file.sh
### To run this file make sure the file is executable
    chmod +x 2_add_full_gene_at_the_end_of_each_fasta_file.sh
### Next run the file
    ./2_add_full_gene_at_the_end_of_each_fasta_file.sh
***Then provide the path to full gene directory (folder), Example (Ex): /home/name/full_gene***


### 3 ) This script adds CDS at the end of each of the fasta files in the full gene directory
3_add_CDS_gene_at_the_end_of_each_fasta_file.sh
To run 3_add_CDS_gene_at_the_end_of_each_fasta_file.sh
    
    chmod +x 3_add_CDS_gene_at_the_end_of_each_fasta_file.sh
### Next run the file
    ./3_add_CDS_gene_at_the_end_of_each_fasta_file.sh
***Then provide the path to Coding sequence directory (folder), Example (Ex): /home/name/CDSS***


### 4 ) This script adds protein at the end of each of the fasta files in the proteins directory
4_add_protein_at_the_end_of_each_fasta_file.sh
To run 4_add_protein_at_the_end_of_each_fasta_file.sh
    
    chmod +x 4_add_protein_at_the_end_of_each_fasta_file.sh
### Next run the file
    ./4_add_protein_at_the_end_of_each_fasta_file.sh
***Then provide the path to protein directory (folder), Example (Ex): /home/name/proteins***

### 5 ) Combing all full gene fasta files into one file full_gene.fasta

To run 5_combine_all_full_gene_fasta_files_to_full_gene_fasta.py
    
    python3 5_combine_all_full_gene_fasta_files_to_full_gene_fasta.py
***Next paste the full path to the full gene directory (folder)***


### 6 ) Combing all coding sequence fasta files into one file CDS_gene.fasta

To run 6_combine_all_CDS_fasta_files_to_CDS_gene_fasta.py

    python3 6_combine_all_CDS_fasta_files_to_CDS_gene_fasta.py
***Next paste the full path to the Coding sequence directory (folder)***


### 7 ) Combing all protein sequence fasta files into one file protein.fasta

To run 7_combine_all_protein_fasta_files_to_protein_fasta.py
    
    python3 7_combine_all_protein_fasta_files_to_protein_fasta.py
***Next paste the full path to the protein sequence directory (folder)***

### 8 ) Copying the full_gene.fasta file, CDS_gene.fasta file, and protein.fasta file to the current directory (that contains all the python scripts)

8_moves_group_fasta_sequences.py

***The full_gene, CDS, and protein directory must be in your current directory (folder)***

To run 8_moves_group_fasta_sequences.py
    
    python3 8_moves_group_fasta_sequences.py


### 9 ) Making the empty HGT dataset in the current working directory (folder)
9_make_hgt_dataset_csv_file_script.py

To run 9_make_hgt_dataset_csv_file_script.py
    
    python3 9_make_hgt_dataset_csv_file_script.py
***The empty HGT dataset csv file (horizontal_gene_transfer_dataset.csv) should be in your current working directory (folder)***

### 10 ) Copying the protein accession number and calculating the amino acid number for each protein sequence and
### pasting the output in the HGT dataset
10_protein_accession_&_amino_acid_count.py
To run 10_protein_accession_&_amino_acid_count.py

    python3 10_protein_accession_\&_amino_acid_count.py
***Enter the path to the protein.fasta file, so it should be in the current directory followed by the name. Ex: protein.fasta***

### 11 ) Copying the gene accession and calculating the number of "GACTs" for each full gene sequence and
### pasting the output in the HGT dataset
To run 11_gene_accesion_&_full_gene_length_count.py

    python3 11_gene_accesion_&_full_gene_length_count.py
***Enter the path to the full_gene.fasta file, so it should be in the current directory followed by the name. Ex: full_gene.fasta***

### 12 ) Calculating the number of "GACTs" for each full gene sequence and number of non-coding sequences (by taking the difference between full gene and CDS) and
### pasting the output in the HGT dataset
To run 12_cds_length_&_non_coding_length.py (When you run this code the terminal outputs the following "Invalid integer in columns 5 or 6", ignore the output and just type y to update the non-coding sequence length)
    
    python3 12_cds_length_&_non_coding_length.py
***Enter the path to the CDS_gene.fasta file, so it should be in the current directory followed by the name. Ex: CDS_gene.fasta***

### 13 ) Calculating number of G's and C's in the for each gene in full_gene.fasta and
### pasting the output in the HGT dataset
To run 13_GC_content_full_gene_calculator_script.py
    
    python3 13_GC_content_full_gene_calculator_script.py
### Enter the path to the full_gene.fasta file, so it should be in the current directory followed by the name. Ex: full_gene.fasta


### 14 ) Calculating number of G's and C's in the for each gene in CDS_gene.fasta and
### pasting the output in the HGT dataset
To run 14_GC_content_CDS_calculator_script.py

    python3 14_GC_content_CDS_calculator_script.py
***Enter the path to the CDS_gene.fasta file, so it should be in the current directory followed by the name. Ex: CDS_gene.fasta***

### 15 ) Requests paper identifier(PMCID or PMID) for HGT paper, taking publishing year, taking paper name and
## pasting the output in the HGT dataset
    python3 15_paper_identifer_publish_year_paper_name.py

### 16 ) Gets the gene name (function) by using the protein.fasta and
## pasting the output in the HGT dataset

    python3 16_gene_name.py
***Enter the path to the protein.fasta file, so it should be in the current directory followed by the name. Ex: protein.fasta***


# Optional section

### Transfers the information from the current HGT dataset paper to the Global dataset (with all the HGT dataset papers)
17_transfer_to_combined_dataset_csv.py
    
    python3 17_transfer_to_combined_dataset_csv.py

### Adds a single genus species to HGT dataset
genus_species.py
    
    python3 genus_species.py

### Adds single value to any of the columns for x amount of rows
input_values_automatically_in_rows.py
    
    python3 input_values_automatically_in_rows.py
Once you run the code it will request which csv file to edit so enter:horizontal_gene_transfer_dataset.csv and then press enter.

Next enter the column number you want to add to. Ex:2 

Next type in what you want to add to each row.

Then state which row you want stop at.













