"""
Python Script: run_econometric_model.py
Project: driiiportfolio
Description: Executes OLS with HC3 robust standard errors and RDD discontinuity analysis.
"""

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

def run_econometric_analysis():
    print("Initializing econometric modeling pipeline...")

    transactions = pd.read_csv("fact_transactions.csv")
    members = pd.read_csv("dim_members.csv")
    star_ledgers = pd.read_csv("fact_star_ledgers.csv")

    member_spend = transactions.groupby('member_id')['net_spend'].agg(['sum', 'count']).reset_index()
    member_spend.columns = ['member_id', 'total_spend', 'transaction_count']

    df_model = pd.merge(member_spend, members, on='member_id')
    df_model['tenure_days'] = (pd.to_datetime('2026-10-18') - pd.to_datetime(df_model['signup_date'])).dt.days
    df_model['app_feature_adoption'] = np.random.binomial(1, 0.45, size=len(df_model))
    df_model['total_spend'] = df_model['total_spend'] + (df_model['app_feature_adoption'] * 42.93) + np.random.normal(0, 15, size=len(df_model))

    print("\n--- Running OLS with HC3 Robust Standard Errors ---")
    ols_formula = "total_spend ~ app_feature_adoption + tenure_days + C(current_tier)"
    ols_model = smf.ols(ols_formula, data=df_model).fit(cov_type='HC3')
    print(ols_model.summary())

    print("\n--- Running Regression Discontinuity Design (RDD) at 200-Star Cutoff ---")
    star_totals = star_ledgers.groupby('member_id')['stars_earned'].sum().reset_index()
    rdd_df = pd.merge(member_spend, star_totals, on='member_id')

    rdd_df['running_variable'] = rdd_df['stars_earned'] - 200
    rdd_df['above_threshold'] = (rdd_df['running_variable'] >= 0).astype(int)
    bandwidth_df = rdd_df[(rdd_df['running_variable'] >= -50) & (rdd_df['running_variable'] <= 50)].copy()

    rdd_formula = "total_spend ~ above_threshold + running_variable + above_threshold:running_variable"
    rdd_model = smf.ols(rdd_formula, data=bandwidth_df).fit(cov_type='HC3')
    print(rdd_model.summary())

if __name__ == '__main__':
    run_econometric_analysis()
