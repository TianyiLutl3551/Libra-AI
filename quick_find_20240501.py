#!/usr/bin/env python3
"""
Quick script to find all table files with VALUATION_DATE = 20240501
"""

import pandas as pd
import os

def find_20240501_files():
    """Find all table files with VALUATION_DATE = 20240501"""
    
    correct_folder = "data/correct"
    matching_files = []
    
    # Find all CSV files that look like table files
    for file in os.listdir(correct_folder):
        if file.endswith(".csv") and file.startswith("table_"):
            file_path = os.path.join(correct_folder, file)
            
            try:
                df = pd.read_csv(file_path)
                
                # Check if VALUATION_DATE column exists and has the target value
                if 'VALUATION_DATE' in df.columns and len(df) > 0:
                    first_date = str(df.iloc[0]['VALUATION_DATE'])
                    
                    if first_date == "20240501":
                        product_type = df.iloc[0]['PRODUCT_TYPE'] if 'PRODUCT_TYPE' in df.columns else 'Unknown'
                        matching_files.append((file, product_type, len(df)))
                        
            except Exception as e:
                continue
    
    print(f"Found {len(matching_files)} table files with VALUATION_DATE = 20240501:")
    print("=" * 60)
    
    for i, (filename, product, rows) in enumerate(matching_files, 1):
        print(f"{i:2d}. {filename} ({product}, {rows} rows)")
    
    return matching_files

if __name__ == "__main__":
    find_20240501_files() 