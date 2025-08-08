#!/usr/bin/env python3
"""
Test script to verify the MSG filter functionality with sample files.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from filter_msg_files import MSGFilter
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_with_temp_data():
    """Test the MSG filter with files from the temp data directory."""
    
    # Use the temp data directory as source
    source_directory = r"\\crdcr150\invpas$\ALM\HedgeP&L\InputMsg"
    
    # Use a test output directory
    target_directory = r"C:\dev\AI_repo\Libra-AI\data\input"
    
    # Check if source directory exists
    if not os.path.exists(source_directory):
        logger.error(f"Source directory does not exist: {source_directory}")
        return
    
    logger.info(f"Testing with files from: {source_directory}")
    logger.info(f"Output will be saved to: {target_directory}")
    
    # Create and run the filter
    msg_filter = MSGFilter(source_directory, target_directory)
    msg_filter.run()

if __name__ == "__main__":
    test_with_temp_data() 