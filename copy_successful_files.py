#!/usr/bin/env python3
"""
Script to copy successful files based on validation log
"""

import os
import re
import shutil
from pathlib import Path

def parse_validation_log(log_path):
    """Parse the validation log to find successful files"""
    successful_files = []
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '| correct' in line:
                # Extract filename from line like: [timestamp] filename.msg | correct
                match = re.search(r'\] (.+\.msg) \| correct', line)
                if match:
                    filename = match.group(1)
                    successful_files.append(filename)
    
    return successful_files

def extract_date_and_product(filename):
    """Extract date and product from filename"""
    # Example: "Daily Hedging P&L Summary for DBIB 2024_03_22.msg"
    # Extract date: 2024_03_22 -> 20240322
    # Extract product: DBIB or WB
    
    # Extract date
    date_match = re.search(r'(\d{4})_(\d{2})_(\d{2})', filename)
    if date_match:
        year, month, day = date_match.groups()
        date_str = f"{year}{month}{day}"
    else:
        return None, None
    
    # Extract product
    if 'DBIB' in filename:
        product = 'DBIB'
    elif 'WB' in filename:
        product = 'WB'
    else:
        return None, None
    
    return date_str, product

def find_output_files(output_dir, date_str, product):
    """Find the corresponding output files for a given date and product"""
    files_to_copy = []
    
    # Look for table file
    table_pattern = f"table_Daily Hedging P&L Summary for {product} {date_str[:4]}_{date_str[4:6]}_{date_str[6:8]}.csv"
    table_path = os.path.join(output_dir, table_pattern)
    if os.path.exists(table_path):
        files_to_copy.append(table_path)
    
    # Look for highlights file
    highlights_pattern = f"highlights_{date_str}_{product}.csv"
    highlights_path = os.path.join(output_dir, highlights_pattern)
    if os.path.exists(highlights_path):
        files_to_copy.append(highlights_path)
    
    # Also look for highlights files with suffixes (like _002, _003, etc.)
    for suffix in range(1, 10):
        highlights_pattern_suffix = f"highlights_{date_str}_{product}_{suffix:03d}.csv"
        highlights_path_suffix = os.path.join(output_dir, highlights_pattern_suffix)
        if os.path.exists(highlights_path_suffix):
            files_to_copy.append(highlights_path_suffix)
            break  # Take the first one found
    
    return files_to_copy

def copy_successful_files():
    """Main function to copy successful files"""
    
    # Paths
    validation_log_path = r"C:\dev\AI_repo\Libra-AI\log\validation_log.txt"
    output_dir = r"C:\dev\AI_repo\Libra-AI\data\output"
    correct_dir = r"C:\dev\AI_repo\Libra-AI\data\correct"
    
    # Create correct directory if it doesn't exist
    os.makedirs(correct_dir, exist_ok=True)
    
    # Parse validation log
    print("Parsing validation log...")
    successful_files = parse_validation_log(validation_log_path)
    print(f"Found {len(successful_files)} successful files")
    
    # Process each successful file
    copied_count = 0
    skipped_count = 0
    
    for filename in successful_files:
        print(f"\nProcessing: {filename}")
        
        # Extract date and product
        date_str, product = extract_date_and_product(filename)
        if not date_str or not product:
            print(f"  Skipped: Could not extract date/product from {filename}")
            skipped_count += 1
            continue
        
        print(f"  Date: {date_str}, Product: {product}")
        
        # Find output files
        output_files = find_output_files(output_dir, date_str, product)
        
        if not output_files:
            print(f"  Skipped: No output files found for {filename}")
            skipped_count += 1
            continue
        
        # Copy files
        for file_path in output_files:
            filename_only = os.path.basename(file_path)
            dest_path = os.path.join(correct_dir, filename_only)
            
            try:
                shutil.copy2(file_path, dest_path)
                print(f"  Copied: {filename_only}")
                copied_count += 1
            except Exception as e:
                print(f"  Error copying {filename_only}: {e}")
                skipped_count += 1
    
    print(f"\nSummary:")
    print(f"  Total successful files: {len(successful_files)}")
    print(f"  Files copied: {copied_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Output directory: {correct_dir}")

if __name__ == "__main__":
    copy_successful_files() 