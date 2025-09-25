import csv

# Prompt for input CSV file
input_file = input("Enter the CSV file to open: ").strip()

# Read the CSV into memory
with open(input_file, newline="") as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Show column headers and numbers
header = rows[0]
print("\nColumns:")
for idx, colname in enumerate(header, start=1):
    print(f"{idx}: {colname}")

# Prompt for column to fill
while True:
    col_input = input("\nWhich column number would you like to fill? ").strip()
    if col_input.isdigit():
        col_num = int(col_input)
        if 1 <= col_num <= len(header):
            break
    print("Invalid column number. Please try again.")

# Prompt for the value to fill
fill_value = input("\nEnter the value to fill: ").strip()

# Prompt for stop row number
while True:
    stop_input = input("\nWhich row number do you want to stop at? ").strip()
    if stop_input.isdigit():
        stop_row = int(stop_input)
        if stop_row >= 2:
            break
    print("Invalid row number. Must be 2 or higher (since row 1 is the header).")

# Process each row up to the stop row
start_row_idx = 1  # skip header
end_row_idx = min(stop_row, len(rows))

for idx in range(start_row_idx, end_row_idx):
    row = rows[idx]
    row[col_num - 1] = fill_value

# Write back to the same file
with open(input_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

print(f"\n✅ Filled rows 2 to {end_row_idx} in column '{header[col_num - 1]}' with value: '{fill_value}'")
print("✅ All done. File updated successfully.")

