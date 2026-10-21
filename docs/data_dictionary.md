# Data Dictionary: Starbucks Loyalty Strategy Analytics

| Table Name | Field Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `dim_members` | `member_id` | STRING | Unique surrogate key for loyalty members. |
| `dim_members` | `signup_date` | TIMESTAMP | Date of initial Starbucks Rewards registration. |
| `dim_members` | `current_tier` | STRING | Loyalty tier classification (Green, Gold, Reserve). |
| `dim_stores` | `store_id` | STRING | Unique store identifier in the Seattle market. |
| `dim_stores` | `store_format` | STRING | Format type (Reserve Roastery, Pickup, Drive-Thru). |
| `fact_transactions`| `transaction_id` | STRING | Unique transaction identifier. |
| `fact_transactions`| `transaction_date`| TIMESTAMP | Timestamp of purchase (Partitioned). |
| `fact_transactions`| `net_spend` | FLOAT | Final dollar amount paid after discounts/modifications. |
| `fact_star_ledgers`| `stars_earned` | INTEGER | Number of Stars credited to member account. |
| `fact_tier_mig` | `migration_event`| STRING | Indicator of tier upgrade or downgrade transition. |
