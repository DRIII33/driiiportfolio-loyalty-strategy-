"""
Python Script: generate_synthetic_data.py
Project: driiiportfolio
Description: Generates bounded relational dataset for Starbucks Seattle loyalty ecosystem.
"""

import numpy as np
import pandas as pd

def generate_data():
    np.random.seed(42)
    n_members = 50000

    member_ids = [f"MB_{i:06d}" for i in range(1, n_members + 1)]
    signup_dates = pd.date_range(start="2023-01-01", end="2025-12-31", periods=n_members)
    tiers = np.random.choice(["Green", "Gold", "Reserve"], size=n_members, p=[0.5, 0.4, 0.1])

    dim_members = pd.DataFrame({
        "member_id": member_ids,
        "signup_date": signup_dates,
        "current_tier": tiers
    })

    n_stores = 50
    store_ids = [f"ST_{i:03d}" for i in range(1, n_stores + 1)]
    store_formats = np.random.choice(["Drive-Thru", "Pickup-Only", "Reserve Roastery"], size=n_stores, p=[0.6, 0.3, 0.1])
    dim_stores = pd.DataFrame({
        "store_id": store_ids,
        "store_format": store_formats,
        "city": "Seattle"
    })

    promotions_data = [
        ("PR_001", "BOGO", "Buy One Get One Free"),
        ("PR_002", "Double-Star", "Double Stars on Reserve Blends"),
        ("PR_003", "Discount-LTV", "$2 Off Premium Brews"),
        ("PR_004", "None", "No Active Promotion")
    ]
    dim_promotions = pd.DataFrame(promotions_data, columns=["promotion_id", "promo_category", "promo_name"])

    n_transactions = 500000
    trans_member_ids = np.random.choice(member_ids, size=n_transactions)
    trans_store_ids = np.random.choice(store_ids, size=n_transactions)
    transaction_dates = pd.to_datetime(np.random.choice(pd.date_range(start="2025-01-01", end="2026-10-18"), size=n_transactions))
    trans_promo_ids = np.random.choice(dim_promotions["promotion_id"], size=n_transactions, p=[0.15, 0.15, 0.20, 0.50])

    base_spend = np.random.gamma(shape=2.0, scale=4.0, size=n_transactions) + 5.0
    ticket_noise = np.random.normal(0, base_spend * 0.4, size=n_transactions)
    net_spend = np.clip(base_spend + ticket_noise, 2.0, 75.0)

    fact_transactions = pd.DataFrame({
        "transaction_id": [f"TX_{i:09d}" for i in range(1, n_transactions + 1)],
        "member_id": trans_member_ids,
        "store_id": trans_store_ids,
        "transaction_date": transaction_dates,
        "promotion_id": trans_promo_ids,
        "net_spend": np.round(net_spend, 2)
    })

    member_tier_map = dict(zip(dim_members["member_id"], dim_members["current_tier"]))
    mapped_tiers = [member_tier_map[m_id] for m_id in trans_member_ids]

    stars_earned = []
    for tier, spend, promo in zip(mapped_tiers, net_spend, trans_promo_ids):
        multiplier = 2.0 if tier in ["Gold", "Reserve"] else 1.0
        if promo == "PR_002":
            multiplier *= 2.0
        stars_earned.append(int(spend * multiplier))

    fact_star_ledgers = pd.DataFrame({
        "transaction_id": fact_transactions["transaction_id"],
        "member_id": trans_member_ids,
        "transaction_date": transaction_dates,
        "stars_earned": stars_earned
    })

    migration_events = np.random.choice(["Upgrade to Gold", "Upgrade to Reserve", "Reverted to Green"], size=10000, p=[0.7, 0.2, 0.1])
    fact_tier_migrations = pd.DataFrame({
        "migration_id": [f"MG_{i:06d}" for i in range(1, 10001)],
        "member_id": np.random.choice(member_ids, size=10000),
        "migration_date": pd.to_datetime(np.random.choice(pd.date_range(start="2025-01-01", end="2026-10-18"), size=10000)),
        "migration_event": migration_events
    })

    dim_members.to_csv("dim_members.csv", index=False)
    dim_stores.to_csv("dim_stores.csv", index=False)
    dim_promotions.to_csv("dim_promotions.csv", index=False)
    fact_transactions.to_csv("fact_transactions.csv", index=False)
    fact_star_ledgers.to_csv("fact_star_ledgers.csv", index=False)
    fact_tier_migrations.to_csv("fact_tier_migrations.csv", index=False)
    print("Synthetic data generated successfully.")

if __name__ == '__main__':
    generate_data()
