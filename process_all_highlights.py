#!/usr/bin/env python3
"""
Script to add PRODUCT_TYPE column to all highlights CSV files in the correct folder
"""

import pandas as pd
import os
import re
from pathlib import Path

def add_product_type_column(file_path):
    """Add PRODUCT_TYPE column to a highlights CSV file"""
    
    # Extract product type from filename
    filename = os.path.basename(file_path)
    match = re.search(r'highlights_\d{8}_(WB|DBIB)\.csv', filename)
    if not match:
        print(f"Could not extract product type from filename: {filename}")
        return False
    
    product_type = match.group(1)
    
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        
        # Check if PRODUCT_TYPE column already exists
        if 'PRODUCT_TYPE' in df.columns:
            print(f"⏭️  {filename} already has PRODUCT_TYPE column, skipping...")
            return True
        
        # Insert PRODUCT_TYPE column after Date column
        if 'Date' in df.columns:
            # Get the index of the Date column
            date_idx = df.columns.get_loc('Date')
            
            # Insert PRODUCT_TYPE column right after Date
            df.insert(date_idx + 1, 'PRODUCT_TYPE', product_type)
            
            # Save the modified file
            df.to_csv(file_path, index=False)
            print(f"✅ Added PRODUCT_TYPE column to {filename}")
            return True
        else:
            print(f"❌ No 'Date' column found in {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def process_all_highlights():
    """Process all highlights files in the correct folder"""
    
    correct_folder = "data/correct"
    highlights_files = []
    
    # Find all highlights files
    for file in os.listdir(correct_folder):
        if file.startswith("highlights_") and file.endswith(".csv"):
            highlights_files.append(os.path.join(correct_folder, file))
    
    print(f"Found {len(highlights_files)} highlights files to process")
    print("=" * 50)
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for file_path in sorted(highlights_files):
        result = add_product_type_column(file_path)
        if result:
            if 'already has PRODUCT_TYPE column' in str(result):
                skip_count += 1
            else:
                success_count += 1
        else:
            error_count += 1
    
    print("=" * 50)
    print(f"📊 Processing Summary:")
    print(f"   ✅ Successfully processed: {success_count}")
    print(f"   ⏭️  Skipped (already processed): {skip_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Total files: {len(highlights_files)}")

if __name__ == "__main__":
    process_all_highlights() 