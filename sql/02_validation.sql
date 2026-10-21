-- =====================================================================
-- SQL SCRIPT 02: VALIDATION & RECONCILIATION AUDIT
-- =====================================================================

-- Audit 1: Referential Integrity Check (Orphaned Transactions)
SELECT
  'Orphaned Transactions Check' AS audit_name,
  COUNT(t.transaction_id) AS violation_count
FROM
  `driiiportfolio.loyalty_analytics.fact_transactions` t
LEFT JOIN
  `driiiportfolio.loyalty_analytics.dim_members` m ON t.member_id = m.member_id
WHERE
  m.member_id IS NULL
  AND t.transaction_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY);

-- Audit 2: Financial Reconciliation (Invalid Net Spend)
SELECT
  'Invalid Net Spend Check' AS audit_name,
  COUNT(transaction_id) AS violation_count
FROM
  `driiiportfolio.loyalty_analytics.fact_transactions`
WHERE
  net_spend <= 0;
