#!/usr/bin/env python3
"""
Script to find all table files with VALUATION_DATE = 20240501
"""

import pandas as pd
import os
import re
from pathlib import Path

def find_files_with_date(target_date="20240501"):
    """Find all table files with VALUATION_DATE = target_date"""
    
    correct_folder = "data/correct"
    table_files = []
    matching_files = []
    
    # Find all CSV files that look like table files
    for file in os.listdir(correct_folder):
        if file.endswith(".csv") and file.startswith("table_"):
            table_files.append(os.path.join(correct_folder, file))
    
    print(f"🔍 Searching {len(table_files)} table files for VALUATION_DATE = {target_date}")
    print("=" * 80)
    
    for file_path in sorted(table_files):
        filename = os.path.basename(file_path)
        
        try:
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Check if VALUATION_DATE column exists
            if 'VALUATION_DATE' not in df.columns:
                continue
            
            # Check if any row has the target date
            if len(df) > 0:
                first_date = str(df.iloc[0]['VALUATION_DATE'])
                
                if first_date == target_date:
                    matching_files.append({
                        'filename': filename,
                        'file_path': file_path,
                        'product_type': df.iloc[0]['PRODUCT_TYPE'] if 'PRODUCT_TYPE' in df.columns else 'Unknown',
                        'row_count': len(df)
                    })
                    print(f"✅ Found: {filename}")
                    print(f"   📅 Date: {first_date}")
                    print(f"   🏷️  Product: {df.iloc[0]['PRODUCT_TYPE'] if 'PRODUCT_TYPE' in df.columns else 'Unknown'}")
                    print(f"   📊 Rows: {len(df)}")
                    print()
                    
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
            continue
    
    print("=" * 80)
    print(f"📊 Summary:")
    print(f"   🔍 Files searched: {len(table_files)}")
    print(f"   ✅ Files with VALUATION_DATE = {target_date}: {len(matching_files)}")
    
    if matching_files:
        print(f"\n📋 List of matching files:")
        for i, file_info in enumerate(matching_files, 1):
            print(f"   {i:2d}. {file_info['filename']} ({file_info['product_type']}, {file_info['row_count']} rows)")
    
    return matching_files

def show_file_details(file_path):
    """Show detailed information about a specific file"""
    try:
        df = pd.read_csv(file_path)
        filename = os.path.basename(file_path)
        
        print(f"\n📄 File Details: {filename}")
        print("=" * 60)
        print(f"📊 Shape: {df.shape}")
        print(f"📅 VALUATION_DATE: {df.iloc[0]['VALUATION_DATE'] if len(df) > 0 else 'N/A'}")
        print(f"🏷️  PRODUCT_TYPE: {df.iloc[0]['PRODUCT_TYPE'] if len(df) > 0 else 'N/A'}")
        
        print(f"\n📋 First few rows:")
        print(df.head().to_string(index=False))
        
        print(f"\n📋 All RISK_TYPE values:")
        if 'RISK_TYPE' in df.columns:
            risk_types = df['RISK_TYPE'].unique()
            for risk_type in sorted(risk_types):
                print(f"   - {risk_type}")
        
    except Exception as e:
        print(f"❌ Error showing details for {file_path}: {e}")

def main():
    """Main function"""
    target_date = "20240501"
    
    print(f"🎯 Finding all table files with VALUATION_DATE = {target_date}")
    print("=" * 80)
    
    # Find matching files
    matching_files = find_files_with_date(target_date)
    
    # Ask if user wants to see details of any specific file
    if matching_files:
        print(f"\n💡 To see details of a specific file, run:")
        print(f"   show_file_details('data/correct/filename.csv')")
        
        # Show details of first file as example
        if matching_files:
            print(f"\n📄 Example - Details of first matching file:")
            show_file_details(matching_files[0]['file_path'])

if __name__ == "__main__":
    main() 