"""
SQL exploration of the New York energy data.
"""

import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path("data/processed/ny_energy.db")

def run_query(sql):
    """Helper function to run a SQL query and return a DataFrame."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(sql, conn)
    conn.close()
    return df


# --------------------------------------------------
# 1. Basic overview
# --------------------------------------------------
print("=== 1. Overview by city ===")
print(run_query("""
    SELECT 
        city,
        COUNT(*) as days,
        ROUND(AVG(avg_demand_mw), 1) as avg_demand,
        ROUND(AVG(temp_max_f), 1) as avg_max_temp,
        ROUND(MIN(temp_min_f), 1) as coldest,
        ROUND(MAX(temp_max_f), 1) as hottest
    FROM daily_data
    GROUP BY city
"""))
print()


# --------------------------------------------------
# 2. Highest demand days
# --------------------------------------------------
print("=== 2. Top 10 highest demand days ===")
print(run_query("""
    SELECT 
        date,
        city,
        ROUND(avg_demand_mw, 1) as demand_mw,
        temp_max_f,
        temp_min_f
    FROM daily_data
    ORDER BY avg_demand_mw DESC
    LIMIT 10
"""))
print()


# --------------------------------------------------
# 3. Demand vs temperature relationship (simple)
# --------------------------------------------------
print("=== 3. Average demand by temperature range ===")
print(run_query("""
    SELECT 
        CASE 
            WHEN temp_max_f < 40 THEN 'Cold (<40°F)'
            WHEN temp_max_f BETWEEN 40 AND 60 THEN 'Mild (40-60°F)'
            WHEN temp_max_f BETWEEN 60 AND 80 THEN 'Warm (60-80°F)'
            ELSE 'Hot (>80°F)'
        END as temp_range,
        COUNT(*) as days,
        ROUND(AVG(avg_demand_mw), 1) as avg_demand
    FROM daily_data
    GROUP BY temp_range
    ORDER BY avg_demand DESC
"""))