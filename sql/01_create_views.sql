-- =====================================================================
-- SQL SCRIPT 01: CREATE ANALYTICAL VIEWS
-- Project: driiiportfolio
-- =====================================================================

CREATE OR REPLACE VIEW `driiiportfolio.loyalty_analytics.vw_customer_loyalty_cube` AS
SELECT
  m.member_id,
  m.current_tier,
  s.store_format,
  DATE_TRUNC(CAST(t.transaction_date AS DATE), MONTH) AS transaction_month,
  COUNT(DISTINCT t.transaction_id) AS monthly_transaction_count,
  SUM(t.net_spend) AS monthly_total_spend,
  AVG(t.net_spend) AS average_ticket_size,
  SUM(sl.stars_earned) AS monthly_stars_earned
FROM
  `driiiportfolio.loyalty_analytics.dim_members` m
JOIN
  `driiiportfolio.loyalty_analytics.fact_transactions` t ON m.member_id = t.member_id
JOIN
  `driiiportfolio.loyalty_analytics.dim_stores` s ON CAST(t.store_id AS STRING) = CAST(s.store_id AS STRING)
LEFT JOIN
  `driiiportfolio.loyalty_analytics.fact_star_ledgers` sl ON t.transaction_id = sl.transaction_id
GROUP BY 1, 2, 3, 4;

CREATE OR REPLACE VIEW `driiiportfolio.loyalty_analytics.vw_promotional_incrementality` AS
SELECT
  p.promotion_id,
  p.promo_category,
  t.member_id,
  COUNT(t.transaction_id) AS promo_period_transactions,
  SUM(t.net_spend) AS promo_period_spend
FROM
  `driiiportfolio.loyalty_analytics.fact_transactions` t
JOIN
  `driiiportfolio.loyalty_analytics.dim_promotions` p ON t.promotion_id = p.promotion_id
GROUP BY 1, 2, 3;
