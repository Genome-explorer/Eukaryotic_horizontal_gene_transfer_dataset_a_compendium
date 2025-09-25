import pandas as pd
import os

def process_csv_with_metadata():
    """
    Script to collect PMCID/PMID/DOI, publish year, and paper name from the user,
    then update the CSV file by writing the values into columns 18, 19, and 20
    for a specified number of rows.
    """
    # Get identifier
    identifier = input("Please enter the PMCID, PMID, or DOI: ").strip()
    if not identifier:
        print("Identifier cannot be empty.")
        return
    
    # Get publish year
    while True:
        publish_year = input("Please enter the publish year (e.g., 2024): ").strip()
        if publish_year.isdigit() and len(publish_year) == 4:
            break
        else:
            print("Please enter a valid 4-digit year.")
    
    # Get paper name and format it
    paper_name = input("Please enter the paper name: ").strip()
    formatted_paper_name = paper_name.replace(" ", "_")
    
    # Get row number to stop at
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
    
    # Check for file existence
    if not os.path.isfile(csv_file):
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    
    try:
        # Load the CSV file
        df = pd.read_csv(csv_file, dtype=str)
        
        # Ensure the DataFrame has at least 20 columns
        if len(df.columns) < 20:
            for i in range(len(df.columns), 20):
                column_name = f"column_{i+1}"
                df[column_name] = ""
        
        # Determine number of rows to update
        rows_to_process = min(stop_row, len(df))
        
        # Update values in respective columns
        for idx in range(rows_to_process):
            df.iloc[idx, 15] = identifier            # Column 16
            df.iloc[idx, 16] = publish_year          # Column 17
            df.iloc[idx, 17] = formatted_paper_name  # Column 18
        
        # Save the updated CSV
        df.to_csv(csv_file, index=False)
        
        print(f"Successfully updated {rows_to_process} rows in {csv_file}")
        print(f"Identifier '{identifier}' written to column 18")
        print(f"Publish year '{publish_year}' written to column 19")
        print(f"Paper name '{formatted_paper_name}' written to column 20")
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")

if __name__ == "__main__":
    process_csv_with_metadata()

