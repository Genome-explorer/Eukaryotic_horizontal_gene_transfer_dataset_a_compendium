import pandas as pd
import os

def process_csv_with_genus_species():
    """
    Script to get genus and species from user, format the input
    (capitalize genus, lowercase species, join with underscore),
    and update column 17 of the CSV for a specified number of rows.
    """
    # Get genus and species from user
    genus_species = input("Enter genus and species (e.g., Bombyx mori): ").strip()
    parts = genus_species.split()

    if len(parts) != 2:
        print("Error: Please enter exactly two words for genus and species.")
        return

    genus = parts[0].capitalize()
    species = parts[1].lower()
    formatted_genus_species = f"{genus}_{species}"

    print(f"Formatted genus and species: {formatted_genus_species}")
    
    # Get the row to stop at from user
    while True:
        try:
            stop_row = int(input("Enter the row number to stop at: "))
            if stop_row <= 0:
                print("Please enter a positive number.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")
    
    # Path to the CSV file
    csv_file = "horizontal_gene_transfer_dataset.csv"
    
    # Check if the file exists
    if not os.path.isfile(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, dtype=str)
        
        # Ensure the DataFrame has at least 17 columns
        if len(df.columns) < 17:
            for i in range(len(df.columns), 17):
                column_name = f"column_{i+1}"
                df[column_name] = ""
        
        # Determine the number of rows to update
        rows_to_process = min(stop_row, len(df))
        
        # Update column 15 with genus/species
        for idx in range(rows_to_process):
            df.iloc[idx, 14] = formatted_genus_species  # Column 15
        
        # Save the updated CSV
        df.to_csv(csv_file, index=False)
        
        print(f"Successfully updated {rows_to_process} rows in {csv_file}")
        print(f"Genus/species '{formatted_genus_species}' written to column 15")
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")

if __name__ == "__main__":
    process_csv_with_genus_species()

