"""
NOAA temperature downloader
Downloads daily max/min temperature for NYC, Albany, Buffalo
one year at a time.
"""

import os
from pathlib import Path
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

# Load token
load_dotenv()
TOKEN = os.getenv("NOAA_TOKEN")
if not TOKEN:
    raise ValueError("NOAA_TOKEN is missing from .env file")

# Settings
OUTPUT_FOLDER = Path("data/raw/noaa")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

STATIONS = {
    "nyc": "GHCND:USW00094728",
    "albany": "GHCND:USW00014735",
    "buffalo": "GHCND:USW00014733"
}

YEARS = list(range(2022, 2027))   # 2022 to 2026


def download_year(city, station_id, year):
    """Download one year of data for one city."""
    print(f"  {city} - {year}...", end=" ")

    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
    headers = {"token": TOKEN}

    params = {
        "datasetid": "GHCND",
        "stationid": station_id,
        "startdate": f"{year}-01-01",
        "enddate": f"{year}-12-31",
        "datatypeid": "TMAX,TMIN",
        "units": "standard",
        "limit": 1000
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        results = response.json().get("results", [])
    except Exception as e:
        print(f"ERROR → {e}")
        return None

    if not results:
        print("no data")
        return None

    df = pd.DataFrame(results)
    df = df[["date", "datatype", "value"]]
    df["date"] = pd.to_datetime(df["date"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Pivot TMAX and TMIN into columns
    df = df.pivot(index="date", columns="datatype", values="value").reset_index()
    df["city"] = city
    df = df.rename(columns={"TMAX": "temp_max_f", "TMIN": "temp_min_f"})

    print(f"{len(df)} days")
    return df


# --------------------------------------------------
# Main
# --------------------------------------------------
if __name__ == "__main__":
    print("Downloading temperature data (one year at a time)...\n")

    for city, station in STATIONS.items():
        print(f"=== {city.upper()} ===")
        all_years = []

        for year in YEARS:
            df_year = download_year(city, station, year)
            if df_year is not None:
                all_years.append(df_year)

        if all_years:
            final_df = pd.concat(all_years, ignore_index=True)
            final_df = final_df.sort_values("date")

            file_path = OUTPUT_FOLDER / f"{city}_temperature.csv"
            final_df.to_csv(file_path, index=False)
            print(f"  → Saved {len(final_df)} total days to {file_path}\n")
        else:
            print(f"  → No data saved for {city}\n")

    print("Finished.")