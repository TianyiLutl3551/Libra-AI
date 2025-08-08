#!/usr/bin/env python3
"""
Fixed concatenation utility for highlights data from data/correct folder.
Properly handles multi-line text and ensures Excel compatibility.
"""

import os
import pandas as pd
import glob
import csv

def concatenate_highlights_fixed():
    """
    Concatenate all highlights CSV files from data/correct into a single file, sorted by date.
    Fixed to handle multi-line text properly for Excel compatibility.
    """
    # Use data/correct directory
    output_dir = "data/correct"
    output_file = "combined_all_highlights.csv"
    
    print("🔄 Starting highlights CSV concatenation process from data/correct...")
    print("=" * 60)
    
    # Step 1: Discover highlights CSV files
    csv_pattern = os.path.join(output_dir, "highlights_*.csv")
    highlights_files = glob.glob(csv_pattern)
    
    if not highlights_files:
        print("❌ No highlights CSV files found in data/correct directory!")
        return
    
    print(f"📁 Found {len(highlights_files)} highlights CSV files:")
    for file in sorted(highlights_files):
        print(f"  - {os.path.basename(file)}")
    print()
    
    # Step 2: Read and concatenate highlights CSV files
    dataframes = []
    file_stats = []
    
    for file_path in sorted(highlights_files):
        try:
            print(f"📖 Reading: {os.path.basename(file_path)}")
            
            # Read CSV with proper handling of quoted fields
            df = pd.read_csv(file_path, quoting=csv.QUOTE_ALL, keep_default_na=False)
            
            # Show the columns for the first file to understand structure
            if not dataframes:
                print(f"   📋 Columns found: {list(df.columns)}")
            
            # Validate expected columns (flexible structure)
            if 'Date' not in df.columns:
                print(f"⚠️  Warning: {os.path.basename(file_path)} missing 'Date' column: {list(df.columns)}")
            
            # Add source file information for tracking
            df['SOURCE_FILE'] = os.path.basename(file_path)
            
            dataframes.append(df)
            
            # Get date range info
            if 'Date' in df.columns:
                date_range = f"{df['Date'].min()} - {df['Date'].max()}"
            else:
                date_range = "No Date column"
            
            file_stats.append({
                'file': os.path.basename(file_path),
                'rows': len(df),
                'date_range': date_range
            })
            
            print(f"   ✅ Loaded {len(df)} rows")
            
        except Exception as e:
            print(f"❌ Error reading {os.path.basename(file_path)}: {e}")
            continue
    
    if not dataframes:
        print("❌ No valid highlights CSV files could be loaded!")
        return
    
    print()
    
    # Step 3: Concatenate all dataframes (preserving row order within each file)
    print("🔗 Concatenating all highlights...")
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"   ✅ Combined dataset has {len(combined_df)} total rows")
    
    # Step 4: Sort by Date
    if 'Date' in combined_df.columns:
        print("📅 Sorting by Date...")
        # Convert to numeric for proper sorting (in case it's stored as string)
        combined_df['Date'] = pd.to_numeric(combined_df['Date'], errors='coerce')
        combined_df = combined_df.sort_values('Date')
        combined_df = combined_df.reset_index(drop=True)
        print(f"   ✅ Sorted by date range: {combined_df['Date'].min()} - {combined_df['Date'].max()}")
    else:
        print("⚠️  Date column not found - skipping date sorting")
    
    # Step 5: Save the combined file with proper CSV formatting for Excel
    output_path = os.path.join(output_dir, output_file)
    print(f"💾 Saving combined file to: {output_path}")
    
    # Save with proper CSV formatting that Excel can handle
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        # Use csv.writer to ensure proper quoting and escaping
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        
        # Write header
        writer.writerow(combined_df.columns.tolist())
        
        # Write data rows
        for _, row in combined_df.iterrows():
            # Convert all values to strings and handle None/NaN
            row_data = []
            for value in row:
                if pd.isna(value) or value is None:
                    row_data.append("")
                else:
                    row_data.append(str(value))
            writer.writerow(row_data)
    
    # Step 6: Display summary statistics
    print()
    print("📊 Summary Statistics:")
    print("=" * 40)
    print(f"📁 Total files processed: {len(file_stats)}")
    print(f"📊 Total rows combined: {len(combined_df)}")
    
    if 'Date' in combined_df.columns:
        print(f"📅 Date range: {combined_df['Date'].min()} - {combined_df['Date'].max()}")
    
    if 'PRODUCT_TYPE' in combined_df.columns:
        print(f"🏷️  Product types: {sorted(combined_df['PRODUCT_TYPE'].unique())}")
    
    print()
    print("📋 File-by-file breakdown:")
    for stat in file_stats:
        print(f"  - {stat['file']}: {stat['rows']} rows ({stat['date_range']})")
    
    print()
    print("✅ Highlights concatenation completed successfully!")
    print("💡 Note: File saved with proper CSV formatting for Excel compatibility")

if __name__ == "__main__":
    concatenate_highlights_fixed() 