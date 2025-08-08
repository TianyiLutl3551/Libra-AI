#!/usr/bin/env python3
"""
Script to copy original input files that failed validation
"""

import os
import re
import shutil
from pathlib import Path

def parse_validation_log(log_path):
    """Parse the validation log to find failed files"""
    failed_files = []
    
    with open(log_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '| wrong' in line:
                # Extract filename from line like: [timestamp] filename.msg | wrong
                match = re.search(r'\] (.+\.msg) \| wrong', line)
                if match:
                    filename = match.group(1)
                    failed_files.append(filename)
    
    return failed_files

def copy_wrong_input_files():
    """Main function to copy failed input files"""
    
    # Paths
    validation_log_path = r"C:\dev\AI_repo\Libra-AI\log\validation_log.txt"
    input_dir = r"C:\dev\AI_repo\Libra-AI\data\input"
    input_wrong_dir = r"C:\dev\AI_repo\Libra-AI\data\input_wrong"
    
    # Create input_wrong directory if it doesn't exist
    os.makedirs(input_wrong_dir, exist_ok=True)
    
    # Parse validation log
    print("Parsing validation log for failed files...")
    failed_files = parse_validation_log(validation_log_path)
    print(f"Found {len(failed_files)} failed files")
    
    # Process each failed file
    copied_count = 0
    skipped_count = 0
    
    for filename in failed_files:
        print(f"\nProcessing: {filename}")
        
        # Source file path
        source_path = os.path.join(input_dir, filename)
        
        # Check if source file exists
        if not os.path.exists(source_path):
            print(f"  Skipped: Source file not found: {filename}")
            skipped_count += 1
            continue
        
        # Destination file path
        dest_path = os.path.join(input_wrong_dir, filename)
        
        try:
            shutil.copy2(source_path, dest_path)
            print(f"  Copied: {filename}")
            copied_count += 1
        except Exception as e:
            print(f"  Error copying {filename}: {e}")
            skipped_count += 1
    
    print(f"\nSummary:")
    print(f"  Total failed files: {len(failed_files)}")
    print(f"  Files copied: {copied_count}")
    print(f"  Files skipped: {skipped_count}")
    print(f"  Output directory: {input_wrong_dir}")

if __name__ == "__main__":
    copy_wrong_input_files() 