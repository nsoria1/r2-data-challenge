-- Snowflake Setup Script
-- Run this once in Snowflake console to create the required infrastructure

-- Create database
CREATE DATABASE IF NOT EXISTS R2_ASSESSMENT;

-- Create schemas
-- RAW: used directly by the Python loader
CREATE SCHEMA IF NOT EXISTS R2_ASSESSMENT.RAW;
-- dbt schemas: dbt auto-creates them, but defining here for clarity
-- dbt prefixes custom schemas with the profile schema (staging)
CREATE SCHEMA IF NOT EXISTS R2_ASSESSMENT.STAGING_STAGING;
CREATE SCHEMA IF NOT EXISTS R2_ASSESSMENT.STAGING_CORE;
CREATE SCHEMA IF NOT EXISTS R2_ASSESSMENT.STAGING_REPORTING;

-- Grant permissions (adjust role as needed)
GRANT USAGE ON DATABASE R2_ASSESSMENT TO ROLE ACCOUNTADMIN;
GRANT ALL ON SCHEMA R2_ASSESSMENT.RAW TO ROLE ACCOUNTADMIN;
GRANT ALL ON SCHEMA R2_ASSESSMENT.STAGING_STAGING TO ROLE ACCOUNTADMIN;
GRANT ALL ON SCHEMA R2_ASSESSMENT.STAGING_CORE TO ROLE ACCOUNTADMIN;
GRANT ALL ON SCHEMA R2_ASSESSMENT.STAGING_REPORTING TO ROLE ACCOUNTADMIN;

-- Note: RAW tables are created automatically by the Python loader
-- with auto_create_table=True
