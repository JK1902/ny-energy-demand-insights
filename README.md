# New York Energy Demand & Price Insights

## Business Question

> What drives electricity demand spikes in New York, how do wholesale prices respond, and what should an operations team monitor?

## Project Overview

This project analyzes electricity demand, wholesale electricity prices, and weather conditions across New York State to identify the factors associated with demand and price spikes.

The analysis focuses on the NYISO electricity market and weather observations from New York City, Albany, and Buffalo.

## Scope

- **Geography:** New York State / NYISO
- **Time Range:** January 1, 2022 → Present
- **Weather Stations:** New York City, Albany, Buffalo
- **Primary Data Sources:** EIA, NOAA
- **Additional Source:** NYISO public data

## Objectives

1. Identify patterns and drivers of electricity demand spikes.
2. Analyze the relationship between electricity demand and wholesale prices.
3. Determine how weather conditions affect electricity demand.
4. Identify extreme demand and price events.
5. Develop an operations-focused monitoring dashboard.

## Data Sources

- U.S. Energy Information Administration (EIA)
- National Oceanic and Atmospheric Administration (NOAA)
- New York Independent System Operator (NYISO)

## Project Structure

```text
ny-energy-demand-insights/
│
├── data/
│   ├── raw/
│   │   ├── eia/
│   │   ├── noaa/
│   │   └── nyiso/
│   └── processed/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── cleaning/
│   ├── features/
│   └── analysis/
│
├── dashboard/
│
├── reports/
│   └── figures/
│
├── requirements.txt
└── README.md
```
