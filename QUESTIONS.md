# Questions for Product Team

These are questions that came up during the initial analysis. For each one, I've documented a default assumption so we can move forward.

---

### Q1: Transaction Time Format
The spec shows `20211001T174600.000` as example.

**Question**: Should we expect other formats like ISO 8601 (`2021-10-01T17:46:00Z`) or with spaces?

**Default assumption**: Support the documented format plus common ISO 8601 variants. Flag anything else as invalid.

---

### Q2: Amount Format
Example shows `$63.98`.

**Questions**:
- Always with `$` prefix?
- Negative amounts for refunds?
- Thousand separators like `$1,234.56`?

**Default assumption**: Strip `$` and `,` before parsing. Accept negatives as refunds.

---

### Q3: Column `source_id` vs `user_role`
The spec lists 6 columns ending with `user_role`, but the sample shows `source_id` as an extra column.

**Question**: 6 or 7 columns?

**Default assumption**: Follow the spec (6 columns). If we see 7, treat column 6 as `source_id` (ignore) and column 7 as `user_role`.

---

### Q4: Header Detection
Files may or may not have headers.

**Question**: How to reliably detect headers when data could look like column names?

**Default assumption**: If first row contains `store_token` or `transaction_id`, treat as header.

---

### Q5: "Latest Received" for Duplicates
Spec says keep "latest received" for duplicate transactions.

**Question**: Latest by processing time, batch date, or transaction time?

**Default assumption**: Latest by processing timestamp (when our system loaded it).

---

### Q6: Top Store Definition
Output 2 asks for "top sales store".

**Question**: Top by total amount or transaction count?

**Default assumption**: Top by total amount. Ties broken by store_token alphabetically.

---

### Q7: Multiple Files Same Day
Partner may upload multiple files per day.

**Question**: Should we wait for all files or process as they arrive?

**Default assumption**: Process all files in inbox whenever pipeline runs. No ordering guarantees.

---

### Q8: Empty Dates in Reports
Reports show "last 40 dates with transactions".

**Question**: Skip dates with no transactions, or show zeros?

**Default assumption**: Skip empty dates.

---

### Q9: Validation Threshold
Some records will have invalid formats.

**Question**: Should we alert if too many records are invalid?

**Default assumption**: Accept partial files. Track counts in Output 1. No automatic rejection.
