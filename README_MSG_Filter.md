# MSG File Filter

This script filters Daily Hedging P&L .msg files by keeping only the latest file for each product and date combination.

## Overview

The script processes .msg files from the source directory and:
1. Groups files by product (WB or DBIB) and date
2. For each group, compares the send times of all files
3. Keeps only the file with the latest send time
4. Copies the filtered files to the target directory

## Features

- **Automatic Date/Product Extraction**: Uses regex to extract product and date from filenames
- **Send Time Comparison**: Uses the `extract-msg` library to get actual send times from .msg files
- **Fallback Mechanism**: If send time cannot be extracted, uses file modification time
- **Comprehensive Logging**: Logs all operations to both console and file
- **Error Handling**: Gracefully handles file access issues and parsing errors

## Usage

### Main Script

```bash
python filter_msg_files.py
```

This will:
- Read files from: `\\crdcr150\invpas$\ALM\HedgeP&L\InputMsg`
- Save filtered files to: `C:\dev\AI_repo\Libra-AI\data\input`

### Test Script

```bash
python test_msg_filter.py
```

This will test the functionality using files from the `temp data` directory.

## File Pattern Matching

The script looks for files matching this pattern:
```
.*Daily Hedging P&L Summary for (WB|DBIB) (\d{4}_\d{2}_\d{2})\.msg
```

Examples of matching files:
- `Daily Hedging P&L Summary for WB 2024_06_28.msg`
- `Automatic reply_ Daily Hedging P&L Summary for DBIB 2024_06_28.msg`
- `RE_ Daily Hedging P&L Summary for WB 2024_06_28.msg`

## Output

The script will:
1. Create a log file `msg_filter.log` with detailed information
2. Copy the latest files to the target directory
3. Display progress information in the console

## Dependencies

- `extract-msg>=0.41.0` (already included in requirements.txt)
- Standard Python libraries (os, re, shutil, datetime, pathlib, typing, logging)

## Example Output

```
2024-01-15 10:30:00 - INFO - Starting MSG file filtering from \\crdcr150\invpas$\ALM\HedgeP&L\InputMsg to C:\dev\AI_repo\Libra-AI\data\input
2024-01-15 10:30:01 - INFO - Found file: Daily Hedging P&L Summary for WB 2024_06_28.msg - Product: WB, Date: 2024_06_28
2024-01-15 10:30:01 - INFO - Found file: Automatic reply_ Daily Hedging P&L Summary for WB 2024_06_28.msg - Product: WB, Date: 2024_06_28
2024-01-15 10:30:02 - INFO - Latest file for WB on 2024_06_28: Automatic reply_ Daily Hedging P&L Summary for WB 2024_06_28.msg (sent at 2024-06-28 18:00:00)
2024-01-15 10:30:03 - INFO - Copied: Automatic reply_ Daily Hedging P&L Summary for WB 2024_06_28.msg to C:\dev\AI_repo\Libra-AI\data\input
2024-01-15 10:30:04 - INFO - Successfully copied 1 files to C:\dev\AI_repo\Libra-AI\data\input
2024-01-15 10:30:04 - INFO - MSG file filtering completed!
```

## Customization

To modify the source or target directories, edit the `main()` function in `filter_msg_files.py`:

```python
def main():
    source_directory = r"your_source_path_here"
    target_directory = r"your_target_path_here"
    # ... rest of the code
```

## Troubleshooting

1. **Network Path Issues**: Ensure the network path `\\crdcr150\invpas$\ALM\HedgeP&L\InputMsg` is accessible
2. **Permission Issues**: Make sure you have read access to the source directory and write access to the target directory
3. **File Lock Issues**: Ensure .msg files are not being used by other applications
4. **Pattern Matching**: Check the log file to see if files are being skipped due to pattern mismatch 