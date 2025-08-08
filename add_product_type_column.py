#!/usr/bin/env python3
"""
Script to add PRODUCT_TYPE column to highlights CSV files
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
    print(f"Processing {filename} -> Product Type: {product_type}")
    
    # Read the CSV file
    try:
        df = pd.read_csv(file_path)
        print(f"Original columns: {list(df.columns)}")
        
        # Insert PRODUCT_TYPE column after Date column
        if 'Date' in df.columns:
            # Get the index of the Date column
            date_idx = df.columns.get_loc('Date')
            
            # Insert PRODUCT_TYPE column right after Date
            df.insert(date_idx + 1, 'PRODUCT_TYPE', product_type)
            
            print(f"New columns: {list(df.columns)}")
            
            # Save the modified file
            df.to_csv(file_path, index=False)
            print(f"✅ Successfully added PRODUCT_TYPE column to {filename}")
            return True
        else:
            print(f"❌ No 'Date' column found in {filename}")
            return False
            
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def test_single_file():
    """Test the function on a single file"""
    test_file = "data/correct/highlights_20230901_DBIB.csv"
    
    if os.path.exists(test_file):
        print(f"Testing on file: {test_file}")
        success = add_product_type_column(test_file)
        if success:
            print("✅ Test completed successfully!")
        else:
            print("❌ Test failed!")
    else:
        print(f"❌ Test file not found: {test_file}")

if __name__ == "__main__":
    test_single_file() 