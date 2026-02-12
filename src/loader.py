"""CSV data loader for Snowflake ingestion."""

import os
import glob
import shutil
from datetime import datetime, timezone
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas

from src import config
from src.utils import detect_header, extract_batch_date, get_file_type


def get_snowflake_connection():
    """Create and return Snowflake connection."""
    return snowflake.connector.connect(
        account=config.SNOWFLAKE_ACCOUNT,
        user=config.SNOWFLAKE_USER,
        password=config.SNOWFLAKE_PASSWORD,
        database=config.SNOWFLAKE_DATABASE,
        schema=config.SNOWFLAKE_SCHEMA,
        warehouse=config.SNOWFLAKE_WAREHOUSE,
        role=config.SNOWFLAKE_ROLE
    )


def load_csv_to_snowflake(filepath: str, conn):
    """
    Load a single CSV file to Snowflake RAW layer.
    
    Args:
        filepath: Path to CSV file
        conn: Snowflake connection
    """
    filename = os.path.basename(filepath)
    file_type = get_file_type(filename)
    
    if not file_type:
        print(f"Skipping {filename}: cannot determine file type")
        return False
    
    table_name = f"raw_{file_type}"
    has_header = detect_header(filepath)
    
    if has_header:
        df = pd.read_csv(filepath, header=0)
    else:
        # Define column names based on file type
        if file_type == 'stores':
            columns = ['store_group', 'store_token', 'store_name']
        else:  # sales
            columns = ['store_token', 'transaction_id', 'receipt_token', 
                      'transaction_time', 'amount', 'user_role']
        df = pd.read_csv(filepath, header=None, names=columns)
    
    batch_date = extract_batch_date(filename)
    df['_batch_date'] = batch_date
    df['_loaded_at'] = datetime.now(timezone.utc)
    df['_source_file'] = filename
    
    df.columns = [col.upper() for col in df.columns]
    
    try:
        write_pandas(
            conn=conn,
            df=df,
            table_name=table_name.upper(),
            schema=config.SNOWFLAKE_SCHEMA,
            database=config.SNOWFLAKE_DATABASE,
            auto_create_table=True,
            overwrite=False
        )
        print(f"✓ Loaded {len(df)} rows from {filename} to {table_name}")
        return True
    except Exception as e:
        print(f"✗ Error loading {filename}: {e}")
        return False


def move_to_processed(filepath: str):
    """Move processed file to processed directory."""
    os.makedirs(config.PROCESSED_DIR, exist_ok=True)
    filename = os.path.basename(filepath)
    dest_path = os.path.join(config.PROCESSED_DIR, filename)
    shutil.move(filepath, dest_path)
    print(f"  Moved to {dest_path}")


def run_dbt():
    """Run dbt transformations."""
    print("\n=== Running dbt transformations ===")
    # Use venv dbt to avoid conflict with dbt Cloud CLI
    venv_dbt = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.venv', 'bin', 'dbt')
    os.system(f"cd {config.DBT_PROJECT_DIR} && {venv_dbt} run --profiles-dir .")


def main(load_only: bool = False):
    """Main loader process."""
    print("=== Starting CSV ingestion ===\n")
    
    # Find all CSV files in inbox
    pattern = os.path.join(config.INBOX_DIR, '*.csv')
    csv_files = glob.glob(pattern)
    
    if not csv_files:
        print(f"No CSV files found in {config.INBOX_DIR}")
        return
    
    print(f"Found {len(csv_files)} CSV file(s)\n")
    
    # Connect to Snowflake
    conn = get_snowflake_connection()
    
    # Process each file
    processed_count = 0
    for filepath in csv_files:
        if load_csv_to_snowflake(filepath, conn):
            move_to_processed(filepath)
            processed_count += 1
    
    # Close connection
    conn.close()
    
    print(f"\n=== Completed: {processed_count}/{len(csv_files)} files processed ===")
    
    # Run dbt if any files were processed (unless load_only)
    if processed_count > 0 and not load_only:
        run_dbt()


if __name__ == '__main__':
    import sys
    load_only = '--load-only' in sys.argv
    main(load_only=load_only)
