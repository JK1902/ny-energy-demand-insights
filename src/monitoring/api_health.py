"""
API Health Monitor for the NY Energy Demand project.

Checks EIA and NOAA APIs, validates responses, logs results,
and prints a summary alert.
"""

import os
import json
import logging
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Setup
# --------------------------------------------------
load_dotenv()

EIA_API_KEY = os.getenv("EIA_API_KEY")
NOAA_TOKEN = os.getenv("NOAA_TOKEN")

LOG_FOLDER = Path("logs")
LOG_FOLDER.mkdir(exist_ok=True)

LOG_FILE = LOG_FOLDER / "api_health.log"
STATUS_FILE = LOG_FOLDER / "last_health_status.json"

# Configure logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Also print to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger().addHandler(console)


# --------------------------------------------------
# Helper: check one API
# --------------------------------------------------
def check_eia():
    """Check EIA Open Data API (NYISO demand endpoint)."""
    name = "EIA"
    url = "https://api.eia.gov/v2/electricity/rto/region-data/data/"

    if not EIA_API_KEY:
        return {"name": name, "status": "FAIL", "reason": "Missing EIA_API_KEY"}

    params = {
        "api_key": EIA_API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[respondent][]": "NYIS",
        "facets[type][]": "D",
        "start": "2024-01-01",
        "end": "2024-01-02",
        "length": 5
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        # Basic validation
        if "response" not in data or "data" not in data["response"]:
            return {"name": name, "status": "FAIL", "reason": "Unexpected response structure"}

        records = data["response"]["data"]
        if not records:
            return {"name": name, "status": "FAIL", "reason": "No data returned"}

        return {
            "name": name,
            "status": "OK",
            "records_returned": len(records),
            "sample_period": records[0].get("period")
        }

    except requests.exceptions.Timeout:
        return {"name": name, "status": "FAIL", "reason": "Timeout"}
    except requests.exceptions.RequestException as e:
        return {"name": name, "status": "FAIL", "reason": str(e)}
    except Exception as e:
        return {"name": name, "status": "FAIL", "reason": f"Unexpected error: {e}"}


def check_noaa():
    """Check NOAA CDO API (Central Park station)."""
    name = "NOAA"
    url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"

    if not NOAA_TOKEN:
        return {"name": name, "status": "FAIL", "reason": "Missing NOAA_TOKEN"}

    headers = {"token": NOAA_TOKEN}
    params = {
        "datasetid": "GHCND",
        "stationid": "GHCND:USW00094728",  # Central Park
        "startdate": "2024-01-01",
        "enddate": "2024-01-05",
        "datatypeid": "TMAX,TMIN",
        "units": "standard",
        "limit": 10
    }

    try:
        response = requests.get(url, headers=headers, params=params, timeout=20)
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return {"name": name, "status": "FAIL", "reason": "No data returned"}

        return {
            "name": name,
            "status": "OK",
            "records_returned": len(results),
            "sample_date": results[0].get("date")
        }

    except requests.exceptions.Timeout:
        return {"name": name, "status": "FAIL", "reason": "Timeout"}
    except requests.exceptions.RequestException as e:
        return {"name": name, "status": "FAIL", "reason": str(e)}
    except Exception as e:
        return {"name": name, "status": "FAIL", "reason": f"Unexpected error: {e}"}


# --------------------------------------------------
# Main monitoring function
# --------------------------------------------------
def run_health_check():
    print("=" * 50)
    print("NY Energy Pipeline – API Health Check")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    results = []

    # Check both APIs
    eia_result = check_eia()
    noaa_result = check_noaa()
    results.extend([eia_result, noaa_result])

    # Log each result
    for r in results:
        if r["status"] == "OK":
            logging.info(f"{r['name']} → OK | records={r.get('records_returned')}")
        else:
            logging.error(f"{r['name']} → FAIL | reason={r.get('reason')}")

    # Summary
    ok_count = sum(1 for r in results if r["status"] == "OK")
    fail_count = len(results) - ok_count

    print("\n----- SUMMARY ALERT -----")
    for r in results:
        status_icon = "✅" if r["status"] == "OK" else "❌"
        print(f"{status_icon} {r['name']}: {r['status']}", end="")
        if r["status"] == "FAIL":
            print(f" → {r.get('reason')}")
        else:
            print(f" (records: {r.get('records_returned')})")

    print(f"\nTotal: {ok_count} OK, {fail_count} FAIL")

    if fail_count > 0:
        print("ACTION NEEDED: One or more data sources are unhealthy.")
    else:
        print("All monitored data sources are healthy.")

    # Save status to JSON (useful for later automation)
    status = {
        "checked_at": datetime.now().isoformat(),
        "results": results,
        "ok_count": ok_count,
        "fail_count": fail_count
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=2)

    print(f"\nStatus saved to: {STATUS_FILE}")
    print(f"Full log: {LOG_FILE}")
    print("=" * 50)

    return status

if __name__ == "__main__":
    run_health_check()