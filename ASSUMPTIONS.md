# Assumptions

Decisions made to move forward with implementation. These can be revisited if the product team provides different guidance.

## File Handling

| Assumption | Reasoning |
|------------|-----------|
| Header detection: if first row contains `store_token` or `transaction_id`, treat as header | These column names won't appear as valid data values |
| Files can be processed in any order. Duplicates resolved by processing timestamp | Matches "latest received" requirement literally |
| If processing fails mid-file, re-running is safe due to deduplication in core layer | Idempotency is important for reliability |

## Data Formats

| Assumption | Reasoning |
|------------|-----------|
| Support multiple timestamp formats: `YYYYMMDDTHHMMSS.sss`, ISO 8601, space-separated | Be flexible in parsing, strict in validation |
| Amount parsing: strip `$` and `,`, accept negatives as refunds | Real data has formatting variations |
| Sales files have 6 columns per spec. If 7 columns present, ignore column 6 (`source_id`) | Spec and sample data are inconsistent; follow spec |

## Business Logic

| Assumption | Reasoning |
|------------|-----------|
| "Latest received" = latest by `_loaded_at` timestamp | Most literal interpretation of "received" |
| Store dimension uses SCD Type 1 (keep latest, no history) | Spec says "additive" but doesn't mention tracking changes |
| "Top sales store" = highest total amount, ties broken by store_token | "Sales" typically means revenue |

---

