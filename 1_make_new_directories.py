#!/usr/bin/env python3
import os

# List of directories to create
dirs = ["full_gene", "CDS", "proteins"]

for d in dirs:
    try:
        os.makedirs(d, exist_ok=True)  # Create dir if not exists
        print(f"Directory created or already exists: {d}")
    except Exception as e:
        print(f"Error creating {d}: {e}")
