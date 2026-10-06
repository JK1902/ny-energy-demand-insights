"""
Cleaning and combining script.
Takes the raw EIA demand and NOAA temperature files
and creates one clean daily dataset.
"""

from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------
RAW_EIA = Path("data/raw/eia")
RAW_NOAA = Path("data/raw/noaa")
OUTPUT_FOLDER = Path("data/processed")
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)


def load_demand():
    """Load the EIA demand CSV and convert to daily average."""
    # Find the demand file (there should be only one)
    files = list(RAW_EIA.glob("*.csv"))
    if not files:
        raise FileNotFoundError("No EIA demand CSV found in data/raw/eia/")
    
    print(f"Loading demand from: {files[0].name}")
    df = pd.read_csv(files[0])
    
    # Make sure timestamp is datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    
    # Create a date column (without time)
    df["date"] = df["timestamp"].dt.date
    
    # Calculate daily average demand
    daily = df.groupby("date")["demand_mw"].mean().reset_index()
    daily = daily.rename(columns={"demand_mw": "avg_demand_mw"})
    
    print(f"  → {len(daily)} days of demand data")
    return daily


def load_temperatures():
    """Load all three temperature files and combine them."""
    temp_files = list(RAW_NOAA.glob("*_temperature.csv"))
    if not temp_files:
        raise FileNotFoundError("No temperature CSVs found in data/raw/noaa/")
    
    all_temps = []
    for file in temp_files:
        print(f"Loading temperature from: {file.name}")
        df = pd.read_csv(file)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        all_temps.append(df)
    
    temps = pd.concat(all_temps, ignore_index=True)
    print(f"  → {len(temps)} temperature records")
    return temps


def main():
    print("Starting cleaning and combining...\n")
    
    # 1. Load demand (daily average)
    demand = load_demand()
    
    # 2. Load temperatures
    temps = load_temperatures()
    
    # 3. Merge demand with temperature on date
    # We keep all temperature rows and add the demand for that day
    combined = temps.merge(demand, on="date", how="left")
    
    # 4. Simple cleaning
    combined = combined.sort_values(["city", "date"]).reset_index(drop=True)
    
    # 5. Save the clean file
    output_path = OUTPUT_FOLDER / "daily_demand_temperature.csv"
    combined.to_csv(output_path, index=False)
    
    print("\n===== DONE =====")
    print(f"Saved clean file → {output_path}")
    print(f"Total rows: {len(combined)}")
    print("\nPreview:")
    print(combined.head(10))


if __name__ == "__main__":
    main()