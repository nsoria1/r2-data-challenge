# Architecture

## Data Flow

```
┌──────────────────┐
│  CSV Files       │
│  (data/inbox/)   │
└────────┬─────────┘
         │
         ▼
┌────────────────────┐
│  Python Loader     │──────▶ Moves processed files to data/processed/
└─────────┬──────────┘
          │
          │ Load to Snowflake
          ▼
┌────────────────────┐
│    RAW Layer       │
│  (landing tables)  │
└─────────┬──────────┘
          │
          │ dbt transformations
          ▼
┌────────────────────┐
│  STAGING Layer     │
│  (validation)      │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│   CORE Layer       │
│  (deduplicated)    │
└─────────┬──────────┘
          │
          ▼
┌────────────────────┐
│ REPORTING Layer    │
│  (3 outputs)       │
└────────────────────┘
```

## Layers

| Layer | Purpose | Materialization |
|-------|---------|-----------------|
| **RAW** | Landing zone, no transformations | Tables |
| **STAGING** | Parse, validate, flag invalid records | Views |
| **CORE** | Business entities, deduplicated | Incremental tables |
| **REPORTING** | Final outputs per spec | Views |

## Processing Steps

1. **Python Loader** (`src/loader.py`)
   - Scans `data/inbox/` for CSV files
   - Detects file type (stores vs sales) from filename
   - Handles files with or without headers
   - Adds metadata: `_batch_date`, `_loaded_at`, `_source_file`
   - Loads to RAW tables
   - Moves processed files to `data/processed/`

2. **dbt Staging**
   - Parses `transaction_time` string to timestamp
   - Parses `amount` (removes `$`, converts to decimal)
   - Validates key fields (see Validation section)
   - Sets `is_valid` flag on each record

3. **dbt Core**
   - `dim_stores`: Latest version of each store
   - `fact_sales`: Deduplicated transactions (unique on `store_token` + `transaction_id`, keeps latest by `_loaded_at`)

4. **dbt Reporting**
   - Generates the three required outputs

## Validation

We validate the critical fields that affect data quality:

| Field | Validation |
|-------|------------|
| `store_name` | Not empty, less than 200 chars |
| `transaction_time` | Parses to valid timestamp |
| `amount` | Parses to valid decimal |

Records failing validation are flagged `is_valid = FALSE` and excluded from CORE, but counted in Output 1.

## Deduplication

Duplicate transactions (same `store_token` + `transaction_id`) are resolved by keeping the record with the latest `_loaded_at` timestamp.

```sql
ROW_NUMBER() OVER (
    PARTITION BY store_token, transaction_id 
    ORDER BY _loaded_at DESC
) = 1
```

## Configuration

1. Copy `.env.example` to `.env` and fill in your Snowflake credentials
2. Run `scripts/setup_snowflake.sql` in Snowflake to create database and schemas

## Future Improvements

- Add alerting when invalid record percentage exceeds threshold
- Support timezone configuration for transaction dates
- Add SCD Type 2 for store dimension if history tracking is needed
- More granular validation rules per field
- Data quality dashboard
