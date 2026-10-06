"""
Load the clean daily dataset into a SQLite database.
"""

from pathlib import Path
import pandas as pd
import sqlite3

# Paths
CSV_PATH = Path("data/processed/daily_demand_temperature.csv")
DB_PATH = Path("data/processed/ny_energy.db")


def load_to_sqlite():
    print("Loading data into SQLite...")

    # Read the clean CSV
    df = pd.read_csv(CSV_PATH)
    df["date"] = pd.to_datetime(df["date"])

    # Create / connect to the database
    conn = sqlite3.connect(DB_PATH)

    # Write the data into a table called "daily_data"
    df.to_sql("daily_data", conn, if_exists="replace", index=False)

    # Quick check
    row_count = pd.read_sql("SELECT COUNT(*) as rows FROM daily_data", conn)
    print(f"Loaded {row_count['rows'][0]} rows into table 'daily_data'")
    print(f"Database saved at: {DB_PATH}")

    conn.close()
    print("Done.")


if __name__ == "__main__":
    load_to_sqlite()