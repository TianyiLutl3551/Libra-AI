#!/usr/bin/env python3
"""
Test script to check alignment on a few files first
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

def test_file(file_path):
    """Test alignment check on a single file (read-only)"""
    
    filename = os.path.basename(file_path)
    print(f"\n🔍 Testing: {filename}")
    
    # Extract date and product from filename
    filename_date, filename_product, file_type = extract_date_and_product_from_filename(filename)
    
    if not filename_date or not filename_product:
        print(f"❌ Could not extract date/product from filename: {filename}")
        return False
    
    print(f"   📅 Filename date: {filename_date}")
    print(f"   🏷️  Filename product: {filename_product}")
    print(f"   📄 File type: {file_type}")
    
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
            
            # Check alignment
            date_aligned = actual_date == filename_date_compact
            product_aligned = actual_product == filename_product
            
            print(f"   ✅ Date aligned: {date_aligned}")
            print(f"   ✅ Product aligned: {product_aligned}")
            
            if not date_aligned or not product_aligned:
                print(f"   ⚠️  Would fix: Date={date_aligned}, Product={product_aligned}")
            
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
            
            # Check alignment
            date_aligned = actual_date == filename_date_compact
            product_aligned = actual_product == filename_product
            
            print(f"   ✅ Date aligned: {date_aligned}")
            print(f"   ✅ Product aligned: {product_aligned}")
            
            if not date_aligned or not product_aligned:
                print(f"   ⚠️  Would fix: Date={date_aligned}, Product={product_aligned}")
            
            return True
        
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        return False

def test_few_files():
    """Test on a few files first"""
    
    test_files = [
        "data/correct/highlights_20230901_DBIB.csv",
        "data/correct/table_Re_ Test Daily Hedging P&L Summary for DBIB 2023_09_01.csv"
    ]
    
    print("🧪 Testing alignment check on sample files...")
    print("=" * 60)
    
    for file_path in test_files:
        if os.path.exists(file_path):
            test_file(file_path)
        else:
            print(f"❌ Test file not found: {file_path}")

if __name__ == "__main__":
    test_few_files() 