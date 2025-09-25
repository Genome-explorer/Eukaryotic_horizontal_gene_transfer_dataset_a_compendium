#!/bin/bash
# Print welcome message
echo "======================================"
echo "FASTA File Renaming Tool"
echo "This script will rename FASTA files based on the header/sequence name inside each file"
echo "Skipping information with dashes (e.g., c15666-15013)"
echo "======================================"
# Ask the user for the directory path
read -p "Please enter the path to the directory containing FASTA files: " FASTA_DIR
# Check if directory exists
if [ ! -d "$FASTA_DIR" ]; then
  echo "Error: Directory '$FASTA_DIR' does not exist."
  exit 1
fi
# Create a log file
log_file="fasta_rename_log.txt"
echo "FASTA File Renaming Log - $(date)" > "$log_file"
echo "--------------------------------------" >> "$log_file"
# Counter for processed files
processed=0
skipped=0
# Process each FASTA file in the directory
echo "Searching for FASTA files..."
for fasta_file in "$FASTA_DIR"/*.fa "$FASTA_DIR"/*.fasta "$FASTA_DIR"/*.fna; do
  # Skip if no files match the pattern
  [ -e "$fasta_file" ] || continue
  
  # Get the current filename
  current_filename=$(basename -- "$fasta_file")
  extension="${current_filename##*.}"
  
  # Get the first header line from the FASTA file
  header=$(grep "^>" "$fasta_file" | head -n 1)
  
  if [ -z "$header" ]; then
    echo "Warning: No FASTA header found in $current_filename. Skipping."
    echo "Skipped: $current_filename (no header found)" >> "$log_file"
    ((skipped++))
    continue
  fi
  
  # Extract the sequence identifier - everything after '>' up to the first space or colon
  # For headers like ">KC521546.1:c15666-15013", we only want "KC521546.1"
  seq_id=$(echo "$header" | sed 's/^>//; s/:[^[:space:]]*//; s/ .*$//')
  
  # If the sequence identifier contains path-unfriendly chars, clean it
  clean_seq_id=$(echo "$seq_id" | tr -d ':/\\|?*<>"')
  
  # Construct the new filename
  new_filename="${clean_seq_id}.${extension}"
  
  # Skip if the new filename would be the same as the current one
  if [ "$current_filename" = "$new_filename" ]; then
    echo "Skipped: $current_filename (already has the correct name)" >> "$log_file"
    ((skipped++))
    continue
  fi
  
  # Check if a file with the new name already exists
  if [ -e "$FASTA_DIR/$new_filename" ]; then
    echo "Warning: Cannot rename $current_filename to $new_filename (file exists)"
    echo "Skipped: $current_filename (target file exists: $new_filename)" >> "$log_file"
    ((skipped++))
    continue
  fi
  
  # Rename the file
  mv "$fasta_file" "$FASTA_DIR/$new_filename"
  
  echo "Renamed: $current_filename -> $new_filename"
  echo "Renamed: $current_filename -> $new_filename" >> "$log_file"
  echo "  Original header: $header" >> "$log_file"
  
  # Increment counter
  ((processed++))
done
# Output summary
echo "======================================"
if [ $processed -eq 0 ] && [ $skipped -eq 0 ]; then
  echo "No FASTA files found in $FASTA_DIR."
else
  echo "Summary:"
  echo "  Successfully renamed: $processed files"
  echo "  Skipped: $skipped files"
  echo "  See $log_file for details."
fi
echo "======================================"
