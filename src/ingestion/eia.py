"""
Simple script to download hourly electricity demand for New York (NYISO)
from the EIA Open Data API (from 2022 until today).

The data is saved as a csv file in: data/raw/eia/
"""

import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

# --------------------------------------------------
# 1. Load the API key from the .env file
# --------------------------------------------------
load_dotenv()
EIA_API_KEY = os.getenv("EIA_API_KEY")

if not EIA_API_KEY:
    raise ValueError("EIA_API_KEY is missing. Please add it to your .env file.")

# --------------------------------------------------
# 2. Settings
# --------------------------------------------------
BASE_URL = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

# Where to save the file
OUTPUT_FOLDER = Path("data/raw/eia")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

# What we want
RESPONDENT = "NYIS"          # New York Independent System Operator
DATA_TYPE = "D"              # D = Demand
START_DATE = "2022-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")


# --------------------------------------------------
# 3. Function to download one page of data
# --------------------------------------------------
def download_one_page(offset=0, length=5000):
    """
    Downloads one page of results from the EIA API.
    """
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": RESPONDENT,
        "facets[type][]": DATA_TYPE,
        "start": START_DATE,
        "end": END_DATE,
        "sort[0][column]": "period",
        "sort[0][direction]": "asc",
        "offset": offset,
        "length": length,
    }

    print(f"Downloading data starting at offset {offset}...")
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()          # Stop if there is an error
    return response.json()


# --------------------------------------------------
# 4. Main function – download everything
# --------------------------------------------------
def download_all_demand_data():
    all_rows = []
    offset = 0
    page_size = 5000

    while True:
        data = download_one_page(offset=offset, length=page_size)

        # Extract the actual records
        records = data.get("response", {}).get("data", [])

        if len(records) == 0:
            print("No more data to download.")
            break

        all_rows.extend(records)

        # Check if we have reached the end
        total = int(data.get("response", {}).get("total", 0))
        print(f"Downloaded so far: {len(all_rows)} / {total} rows")

        if offset + page_size >= total:
            break

        offset += page_size

    # --------------------------------------------------
    # 5. Convert to a clean DataFrame
    # --------------------------------------------------
    df = pd.DataFrame(all_rows)

    if df.empty:
        raise ValueError("No data was returned from the EIA API.")

    # Clean the columns
    df["period"] = pd.to_datetime(df["period"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df = df.rename(columns={
        "period": "timestamp",
        "value": "demand_mw"
    })

    # Keep only useful columns
    df = df[["timestamp", "respondent", "type", "demand_mw"]]
    df = df.sort_values("timestamp").reset_index(drop=True)

    # --------------------------------------------------
    # 6. Save the file
    # --------------------------------------------------
    file_name = f"nyiso_demand_hourly_{START_DATE}_{END_DATE}.csv"
    output_path = OUTPUT_FOLDER / file_name

    df.to_csv(output_path, index=False)

    print("\n===== SUCCESS =====")
    print(f"Saved {len(df):,} rows to:")
    print(output_path)
    print(f"Date range: {df['timestamp'].min()} → {df['timestamp'].max()}")
    print(f"Missing demand values: {df['demand_mw'].isna().sum()}")

    return df


# --------------------------------------------------
# 7. Run the script
# --------------------------------------------------
if __name__ == "__main__":
    download_all_demand_data()