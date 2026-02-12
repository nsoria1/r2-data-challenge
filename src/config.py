"""Configuration module for Snowflake data loader."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Snowflake connection parameters
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA', 'RAW')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_ROLE = os.getenv('SNOWFLAKE_ROLE')

# File paths
INBOX_DIR = os.getenv('INBOX_DIR', 'data/inbox')
PROCESSED_DIR = os.getenv('PROCESSED_DIR', 'data/processed')

# DBT configuration
DBT_PROJECT_DIR = os.getenv('DBT_PROJECT_DIR', 'dbt_project')
