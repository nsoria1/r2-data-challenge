"""Utility functions for CSV data processing."""

import re


def detect_header(filepath: str) -> bool:
    """
    Check if CSV file has a header row.
    A header is detected if the first row contains 'store_token' or 'transaction_id'.
    
    Args:
        filepath: Path to CSV file
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip().lower()
            return 'store_token' in first_line or 'transaction_id' in first_line
    except Exception as e:
        print(f"Warning: Could not detect header for {filepath}: {e}")
        return False


def extract_batch_date(filename: str) -> str:
    """
    Parse YYYYMMDD batch date from filename.
    
    Args:
        filename: Name of the file (e.g., 'stores_20240115.csv')
        
    Returns:
        Batch date in YYYYMMDD format, or None if not found
    """
    match = re.search(r'(\d{8})', filename)
    return match.group(1) if match else None


def get_file_type(filename: str) -> str:
    """
    Determine file type from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        'stores' if stores file, 'sales' if sales file, None otherwise
    """
    filename_lower = filename.lower()
    if 'store' in filename_lower:
        return 'stores'
    elif 'sale' in filename_lower:
        return 'sales'
    return None
