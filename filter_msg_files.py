#!/usr/bin/env python3
"""
Script to filter Daily Hedging P&L .msg files by keeping only the latest file
for each product and date combination.
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import extract_msg
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('msg_filter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MSGFilter:
    def __init__(self, source_dir: str, target_dir: str):
        """
        Initialize the MSG filter.
        
        Args:
            source_dir: Directory containing the .msg files
            target_dir: Directory to save the filtered files
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        # Pattern to match Daily Hedging P&L files
        self.file_pattern = re.compile(
            r'.*Daily Hedging P&L Summary for (WB|DBIB) (\d{4}_\d{2}_\d{2})\.msg$',
            re.IGNORECASE
        )
    
    def extract_date_and_product(self, filename: str) -> Tuple[str, str, str]:
        """
        Extract date and product from filename.
        
        Args:
            filename: The filename to parse
            
        Returns:
            Tuple of (product, date, full_filename)
        """
        match = self.file_pattern.match(filename)
        if match:
            product = match.group(1).upper()
            date = match.group(2)
            return product, date, filename
        return None, None, filename
    
    def get_msg_send_time(self, msg_file_path: Path) -> datetime:
        """
        Extract the send time from a .msg file.
        
        Args:
            msg_file_path: Path to the .msg file
            
        Returns:
            datetime object representing the send time
        """
        try:
            with extract_msg.Message(msg_file_path) as msg:
                # Try to get the send time from the message
                if hasattr(msg, 'date') and msg.date:
                    return msg.date
                elif hasattr(msg, 'header') and msg.header:
                    # Try to extract from header
                    date_header = msg.header.get('date')
                    if date_header:
                        # Parse the date string
                        try:
                            return datetime.strptime(date_header, '%a, %d %b %Y %H:%M:%S %z')
                        except ValueError:
                            pass
                
                # If we can't get the send time, use file modification time
                logger.warning(f"Could not extract send time from {msg_file_path.name}, using file modification time")
                return datetime.fromtimestamp(msg_file_path.stat().st_mtime)
                
        except Exception as e:
            logger.error(f"Error reading {msg_file_path.name}: {e}")
            # Fallback to file modification time
            return datetime.fromtimestamp(msg_file_path.stat().st_mtime)
    
    def group_files_by_product_and_date(self) -> Dict[str, Dict[str, List[Path]]]:
        """
        Group files by product and date.
        
        Returns:
            Dictionary with structure: {product: {date: [file_paths]}}
        """
        grouped_files = {}
        
        for file_path in self.source_dir.glob("*.msg"):
            product, date, filename = self.extract_date_and_product(file_path.name)
            
            if product and date:
                if product not in grouped_files:
                    grouped_files[product] = {}
                
                if date not in grouped_files[product]:
                    grouped_files[product][date] = []
                
                grouped_files[product][date].append(file_path)
                logger.info(f"Found file: {filename} - Product: {product}, Date: {date}")
            else:
                logger.warning(f"Skipping file that doesn't match pattern: {file_path.name}")
        
        return grouped_files
    
    def find_latest_file_for_each_group(self, grouped_files: Dict[str, Dict[str, List[Path]]]) -> List[Path]:
        """
        Find the latest file for each product and date combination.
        
        Args:
            grouped_files: Dictionary of grouped files
            
        Returns:
            List of paths to the latest files
        """
        latest_files = []
        
        for product, dates in grouped_files.items():
            for date, file_paths in dates.items():
                if len(file_paths) == 1:
                    # Only one file for this product and date
                    latest_files.append(file_paths[0])
                    logger.info(f"Single file for {product} on {date}: {file_paths[0].name}")
                else:
                    # Multiple files, find the latest one
                    latest_file = None
                    latest_time = None
                    
                    for file_path in file_paths:
                        send_time = self.get_msg_send_time(file_path)
                        
                        if latest_time is None or send_time > latest_time:
                            latest_time = send_time
                            latest_file = file_path
                    
                    if latest_file:
                        latest_files.append(latest_file)
                        logger.info(f"Latest file for {product} on {date}: {latest_file.name} (sent at {latest_time})")
        
        return latest_files
    
    def copy_latest_files(self, latest_files: List[Path]) -> None:
        """
        Copy the latest files to the target directory.
        
        Args:
            latest_files: List of file paths to copy
        """
        copied_count = 0
        
        for file_path in latest_files:
            try:
                target_path = self.target_dir / file_path.name
                shutil.copy2(file_path, target_path)
                logger.info(f"Copied: {file_path.name} to {target_path}")
                copied_count += 1
            except Exception as e:
                logger.error(f"Error copying {file_path.name}: {e}")
        
        logger.info(f"Successfully copied {copied_count} files to {self.target_dir}")
    
    def run(self) -> None:
        """
        Run the complete filtering process.
        """
        logger.info(f"Starting MSG file filtering from {self.source_dir} to {self.target_dir}")
        
        # Group files by product and date
        grouped_files = self.group_files_by_product_and_date()
        
        if not grouped_files:
            logger.warning("No matching files found!")
            return
        
        # Find the latest file for each group
        latest_files = self.find_latest_file_for_each_group(grouped_files)
        
        # Copy the latest files to the target directory
        self.copy_latest_files(latest_files)
        
        logger.info("MSG file filtering completed!")


def main():
    """Main function to run the MSG filter."""
    # Source directory containing the .msg files
    source_directory = r"\\crdcr150\invpas$\ALM\HedgeP&L\InputMsg"
    
    # Target directory to save the filtered files
    target_directory = r"C:\dev\AI_repo\Libra-AI\data\input"
    
    # Check if source directory exists
    if not os.path.exists(source_directory):
        logger.error(f"Source directory does not exist: {source_directory}")
        return
    
    # Create and run the filter
    msg_filter = MSGFilter(source_directory, target_directory)
    msg_filter.run()


if __name__ == "__main__":
    main() 