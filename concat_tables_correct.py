#!/usr/bin/env python3
"""
Concatenation utility for table data from data/correct folder.
Concatenates all table CSV files in the data/correct directory, preserves row order within each table,
and sorts all data by VALUATION_DATE for chronological analysis.
"""

import os
import pandas as pd
import glob

def concatenate_tables_correct():
    """
    Concatenate all table CSV files from data/correct into a single file, sorted by VALUATION_DATE.
    """
    # Use data/correct directory
    output_dir = "data/correct"
    output_file = "combined_all_tables.csv"
    
    print("🔄 Starting CSV concatenation process from data/correct...")
    print("=" * 60)
    
    # Step 1: Discover CSV files (exclude highlights)
    csv_pattern = os.path.join(output_dir, "*.csv")
    all_csv_files = glob.glob(csv_pattern)
    
    # Filter out highlights files and combined files - only include table files
    table_files = [f for f in all_csv_files if 
                   (os.path.basename(f).startswith("table_") or 
                    os.path.basename(f).startswith("combined_llm_output_Dynamic Hedging PNL")) and 
                   "highlights_" not in os.path.basename(f) and
                   not os.path.basename(f).startswith("combined_all_")]
    
    if not table_files:
        print("❌ No table CSV files found in data/correct directory!")
        return
    
    print(f"📁 Found {len(table_files)} table CSV files:")
    for file in sorted(table_files):
        print(f"  - {os.path.basename(file)}")
    print()
    
    # Step 2: Read and concatenate CSV files
    dataframes = []
    file_stats = []
    
    for file_path in sorted(table_files):
        try:
            print(f"📖 Reading: {os.path.basename(file_path)}")
            df = pd.read_csv(file_path)
            
            # Validate expected columns
            expected_columns = ['VALUATION_DATE', 'PRODUCT_TYPE', 'RISK_TYPE', 'GREEK_TYPE', 'RIDER_VALUE', 'ASSET_VALUE']
            if not all(col in df.columns for col in expected_columns):
                print(f"⚠️  Warning: {os.path.basename(file_path)} has unexpected columns: {list(df.columns)}")
                print(f"   Expected: {expected_columns}")
            
            # Add source file information for tracking
            df['SOURCE_FILE'] = os.path.basename(file_path)
            
            dataframes.append(df)
            file_stats.append({
                'file': os.path.basename(file_path),
                'rows': len(df),
                'date_range': f"{df['VALUATION_DATE'].min()} - {df['VALUATION_DATE'].max()}" if 'VALUATION_DATE' in df.columns else "N/A"
            })
            
            print(f"   ✅ Loaded {len(df)} rows")
            
        except Exception as e:
            print(f"❌ Error reading {os.path.basename(file_path)}: {e}")
            continue
    
    if not dataframes:
        print("❌ No valid CSV files could be loaded!")
        return
    
    print()
    
    # Step 3: Concatenate all dataframes (preserving row order within each file)
    print("🔗 Concatenating all tables...")
    combined_df = pd.concat(dataframes, ignore_index=True)
    print(f"   ✅ Combined dataset has {len(combined_df)} total rows")
    
    # Step 4: Sort by VALUATION_DATE
    if 'VALUATION_DATE' in combined_df.columns:
        print("📅 Sorting by VALUATION_DATE...")
        # Convert to numeric for proper sorting (in case it's stored as string)
        combined_df['VALUATION_DATE'] = pd.to_numeric(combined_df['VALUATION_DATE'], errors='coerce')
        combined_df = combined_df.sort_values('VALUATION_DATE')
        combined_df = combined_df.reset_index(drop=True)
        print(f"   ✅ Sorted by date range: {combined_df['VALUATION_DATE'].min()} - {combined_df['VALUATION_DATE'].max()}")
    else:
        print("⚠️  VALUATION_DATE column not found - skipping date sorting")
    
    # Step 5: Save the combined file
    output_path = os.path.join(output_dir, output_file)
    print(f"💾 Saving combined file to: {output_path}")
    combined_df.to_csv(output_path, index=False)
    
    # Step 6: Display summary statistics
    print()
    print("📊 Summary Statistics:")
    print("=" * 40)
    print(f"📁 Total files processed: {len(file_stats)}")
    print(f"📊 Total rows combined: {len(combined_df)}")
    
    if 'VALUATION_DATE' in combined_df.columns:
        print(f"📅 Date range: {combined_df['VALUATION_DATE'].min()} - {combined_df['VALUATION_DATE'].max()}")
    
    if 'PRODUCT_TYPE' in combined_df.columns:
        print(f"🏷️  Product types: {sorted(combined_df['PRODUCT_TYPE'].unique())}")
    
    print()
    print("📋 File-by-file breakdown:")
    for stat in file_stats:
        print(f"  - {stat['file']}: {stat['rows']} rows ({stat['date_range']})")
    
    print()
    print("✅ Tables concatenation completed successfully!")

if __name__ == "__main__":
    concatenate_tables_correct() 