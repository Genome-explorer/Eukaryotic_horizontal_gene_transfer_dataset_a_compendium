#!/bin/bash
# Print welcome message
echo "======================================"
echo "FASTA File Renaming Tool"
echo "This script will rename FASTA files"
echo "with '_CDS_gene' added to their filenames."
echo "======================================"
# Ask the user for the directory path
read -p "Please enter the path to the directory containing FASTA files: " FASTA_DIR
# Check if directory exists
if [ ! -d "$FASTA_DIR" ]; then
  echo "Error: Directory '$FASTA_DIR' does not exist."
  exit 1
fi
# Counter for processed files
processed=0
# Create a log file
log_file="fasta_rename_log.txt"
echo "FASTA File Renaming Log - $(date)" > "$log_file"
echo "--------------------------------------" >> "$log_file"
# Process each FASTA file in the directory
echo "Searching for FASTA files..."
for fasta_file in "$FASTA_DIR"/*.fa "$FASTA_DIR"/*.fasta "$FASTA_DIR"/*.fna; do
  # Skip if no files match the pattern
  [ -e "$fasta_file" ] || continue
  
  # Get file information
  filename=$(basename -- "$fasta_file")
  extension="${filename##*.}"
  filename_noext="${filename%.*}"
  
  # Create new filename with "CDS_gene" added
  new_filename="${filename_noext}_CDS_gene.${extension}"
  new_filepath="$FASTA_DIR/$new_filename"
  
  # Rename the file (replace original)
  mv "$fasta_file" "$new_filepath"
  
  # Log the operation
  echo "Renamed: $filename to $new_filename" >> "$log_file"
  echo "Renamed: $filename to $new_filename"
  
  # Increment counter
  ((processed++))
done
# Output summary
if [ $processed -eq 0 ]; then
  echo "No FASTA files found in $FASTA_DIR."
else
  echo "======================================"
  echo "Successfully renamed $processed FASTA files."
  echo "Files now have '_CDS_gene' suffix."
  echo "See $log_file for details."
  echo "======================================"
fi

