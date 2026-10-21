# Cloud Architecture & Schema Governance
**Platform:** Google Cloud BigQuery (`driiiportfolio`)  

## Data Governance Rules
- **Partitioning:** Daily partitioning on `transaction_date` for all fact tables.
- **Clustering:** Multi-column clustering on `member_id` and `store_id`.
- **Query Cost Control Mandate:** Mandatory partition filter rule:
  ```sql
  WHERE transaction_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
