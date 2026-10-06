"""
Data quality checks for the combined dataset.
"""

from pathlib import Path
import pandas as pd

FILE_PATH = Path("data/processed/daily_demand_temperature.csv")


def run_checks():
    print("Running data quality checks...\n")
    
    df = pd.read_csv(FILE_PATH)
    df["date"] = pd.to_datetime(df["date"])

    print(f"Total rows: {len(df)}")
    print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"Cities: {df['city'].unique().tolist()}")
    print()

    # 1. Missing values
    print("1. Missing values:")
    print(df.isnull().sum())
    print()

    # 2. Basic statistics
    print("2. Demand statistics (MW):")
    print(df["avg_demand_mw"].describe().round(1))
    print()

    print("3. Temperature statistics (°F):")
    print(df[["temp_max_f", "temp_min_f"]].describe().round(1))
    print()

    # 3. Check for duplicates
    duplicates = df.duplicated(subset=["date", "city"]).sum()
    print(f"4. Duplicate date + city combinations: {duplicates}")

    # 4. Simple range checks
    weird_temp = df[(df["temp_max_f"] > 110) | (df["temp_min_f"] < -20)]
    print(f"5. Extreme temperature values: {len(weird_temp)}")

    weird_demand = df[(df["avg_demand_mw"] < 5000) | (df["avg_demand_mw"] > 40000)]
    print(f"6. Extreme demand values: {len(weird_demand)}")

    print("\nChecks completed.")


if __name__ == "__main__":
    run_checks()