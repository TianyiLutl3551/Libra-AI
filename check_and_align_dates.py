#!/usr/bin/env python3
"""
Script to check and align dates and product types between highlights and table files
"""

import pandas as pd
import os
import re
from pathlib import Path
from datetime import datetime

def extract_date_and_product_from_filename(filename):
    """Extract date and product type from filename"""
    
    # Pattern for highlights files: highlights_YYYYMMDD_PRODUCT.csv
    highlights_match = re.search(r'highlights_(\d{8})_(WB|DBIB)\.csv', filename)
    if highlights_match:
        date_str = highlights_match.group(1)
        product = highlights_match.group(2)
        # Convert YYYYMMDD to YYYY_MM_DD for comparison
        date_formatted = f"{date_str[:4]}_{date_str[4:6]}_{date_str[6:8]}"
        return date_formatted, product, "highlights"
    
    # Pattern for table files: table_*_YYYY_MM_DD.csv
    table_match = re.search(r'table_.*?(\d{4}_\d{2}_\d{2})\.csv', filename)
    if table_match:
        date_str = table_match.group(1)
        # Extract product type from the filename content
        if "DBIB" in filename:
            product = "DBIB"
        elif "WB" in filename:
            product = "WB"
        else:
            product = None
        return date_str, product, "table"
    
    return None, None, None

def convert_date_format(date_str, from_format, to_format):
    """Convert date between different formats"""
    try:
        if from_format == "YYYYMMDD":
            # Convert YYYYMMDD to YYYY_MM_DD
            return f"{date_str[:4]}_{date_str[4:6]}_{date_str[6:8]}"
        elif from_format == "YYYY_MM_DD":
            # Convert YYYY_MM_DD to YYYYMMDD
            return date_str.replace("_", "")
        else:
            return date_str
    except:
        return date_str

def check_and_fix_file(file_path):
    """Check and fix date/product alignment in a single file"""
    
    filename = os.path.basename(file_path)
    print(f"\n🔍 Checking: {filename}")
    
    # Extract date and product from filename
    filename_date, filename_product, file_type = extract_date_and_product_from_filename(filename)
    
    if not filename_date or not filename_product:
        print(f"❌ Could not extract date/product from filename: {filename}")
        return False
    
    print(f"   📅 Filename date: {filename_date}")
    print(f"   🏷️  Filename product: {filename_product}")
    
    try:
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        if file_type == "highlights":
            # Check highlights file
            if 'Date' not in df.columns:
                print(f"❌ No 'Date' column found in highlights file")
                return False
            
            if 'PRODUCT_TYPE' not in df.columns:
                print(f"❌ No 'PRODUCT_TYPE' column found in highlights file")
                return False
            
            # Get the actual values from the file
            actual_date = str(df.iloc[0]['Date']) if len(df) > 0 else None
            actual_product = df.iloc[0]['PRODUCT_TYPE'] if len(df) > 0 else None
            
            print(f"   📅 Content date: {actual_date}")
            print(f"   🏷️  Content product: {actual_product}")
            
            # Convert filename date to YYYYMMDD for comparison
            filename_date_compact = convert_date_format(filename_date, "YYYY_MM_DD", "YYYYMMDD")
            
            needs_fix = False
            fixes = []
            
            # Check date alignment
            if actual_date != filename_date_compact:
                print(f"   ⚠️  Date mismatch: filename={filename_date_compact}, content={actual_date}")
                needs_fix = True
                fixes.append(f"Update content date from {actual_date} to {filename_date_compact}")
            
            # Check product alignment
            if actual_product != filename_product:
                print(f"   ⚠️  Product mismatch: filename={filename_product}, content={actual_product}")
                needs_fix = True
                fixes.append(f"Update content product from {actual_product} to {filename_product}")
            
            if needs_fix:
                print(f"   🔧 Applying fixes...")
                if len(df) > 0:
                    df.iloc[0, df.columns.get_loc('Date')] = filename_date_compact
                    df.iloc[0, df.columns.get_loc('PRODUCT_TYPE')] = filename_product
                    df.to_csv(file_path, index=False)
                    print(f"   ✅ Fixed: {', '.join(fixes)}")
                return True
            else:
                print(f"   ✅ File is already aligned")
                return True
                
        elif file_type == "table":
            # Check table file
            if 'VALUATION_DATE' not in df.columns:
                print(f"❌ No 'VALUATION_DATE' column found in table file")
                return False
            
            if 'PRODUCT_TYPE' not in df.columns:
                print(f"❌ No 'PRODUCT_TYPE' column found in table file")
                return False
            
            # Get the actual values from the file (check first row)
            actual_date = str(df.iloc[0]['VALUATION_DATE']) if len(df) > 0 else None
            actual_product = df.iloc[0]['PRODUCT_TYPE'] if len(df) > 0 else None
            
            print(f"   📅 Content date: {actual_date}")
            print(f"   🏷️  Content product: {actual_product}")
            
            # Convert filename date to YYYYMMDD for comparison
            filename_date_compact = convert_date_format(filename_date, "YYYY_MM_DD", "YYYYMMDD")
            
            needs_fix = False
            fixes = []
            
            # Check date alignment
            if actual_date != filename_date_compact:
                print(f"   ⚠️  Date mismatch: filename={filename_date_compact}, content={actual_date}")
                needs_fix = True
                fixes.append(f"Update content date from {actual_date} to {filename_date_compact}")
            
            # Check product alignment
            if actual_product != filename_product:
                print(f"   ⚠️  Product mismatch: filename={filename_product}, content={actual_product}")
                needs_fix = True
                fixes.append(f"Update content product from {actual_product} to {filename_product}")
            
            if needs_fix:
                print(f"   🔧 Applying fixes...")
                if len(df) > 0:
                    # Update all rows with the correct date and product
                    df['VALUATION_DATE'] = filename_date_compact
                    df['PRODUCT_TYPE'] = filename_product
                    df.to_csv(file_path, index=False)
                    print(f"   ✅ Fixed: {', '.join(fixes)}")
                return True
            else:
                print(f"   ✅ File is already aligned")
                return True
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def process_all_files():
    """Process all highlights and table files in the correct folder"""
    
    correct_folder = "data/correct"
    all_files = []
    
    # Find all CSV files
    for file in os.listdir(correct_folder):
        if file.endswith(".csv"):
            all_files.append(os.path.join(correct_folder, file))
    
    print(f"Found {len(all_files)} CSV files to check")
    print("=" * 60)
    
    success_count = 0
    error_count = 0
    fixed_count = 0
    
    for file_path in sorted(all_files):
        result = check_and_fix_file(file_path)
        if result:
            success_count += 1
            if "Fixed:" in str(result):
                fixed_count += 1
        else:
            error_count += 1
    
    print("=" * 60)
    print(f"📊 Processing Summary:")
    print(f"   ✅ Successfully processed: {success_count}")
    print(f"   🔧 Files fixed: {fixed_count}")
    print(f"   ❌ Errors: {error_count}")
    print(f"   📁 Total files: {len(all_files)}")

if __name__ == "__main__":
    process_all_files() 