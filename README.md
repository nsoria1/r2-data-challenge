# R2 Data Engineer Assessment

A data pipeline for processing daily sales transactions from an online marketplace.

## Overview

This system ingests daily CSV files containing store and sales data, validates and transforms them, and produces three required reports. Built with Python, dbt, and Snowflake.

**Key features:**
- Handles files with or without headers
- Validates data formats and flags invalid records
- Deduplicates transactions (keeps latest received)
- Produces daily reports with sales metrics

## Quick Start

```bash
# 1. Install dependencies
make setup

# 2. Configure Snowflake credentials
cp .env.example .env
# Edit .env with your Snowflake details

# 3. Create Snowflake database/schemas (one-time setup)
# Run scripts/setup_snowflake.sql in Snowflake console

# 4. Run the pipeline
make generate-data   # Create sample test data
make run             # Load data and run transformations
```

## Usage

```bash
# Full pipeline: load CSVs + run dbt
make run

# Individual steps
make generate-data   # Generate sample CSVs
make load            # Load CSVs to Snowflake
make transform       # Run dbt models
make test            # Run all tests
make docs            # Generate dbt documentation

# Cleanup
make clean           # Remove data files
```

## Outputs

| Report | Description |
|--------|-------------|
| Output 1 | Transactions by batch date (last 40 dates) |
| Output 2 | Sales stats by transaction date (last 40 dates) |
| Output 3 | Top 5 stores per day (last 10 dates) |

## Documentation

- [Architecture](ARCHITECTURE.md) - System design and data flow
- [Assumptions](ASSUMPTIONS.md) - Decisions made during implementation
- [Questions](QUESTIONS.md) - Clarifications for product team
- **dbt Docs** - Run `make docs-serve` to browse data model documentation and lineage
