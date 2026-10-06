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

## Key Findings

Analysis of daily NYISO electricity demand and temperature data (January 2022 – October 2026) shows that temperature extremes are the main driver of demand variation in New York.

**1. Demand follows a clear U-shaped pattern with temperature**

Average daily demand is highest at both temperature extremes:

- **90°F and above**: 22,860 MW
- **Below 30°F**: 19,279 MW
- **Mild weather (50–70°F)**: ~15,200–15,500 MW (lowest demand)

This U-shape reflects increased air-conditioning load in summer and heating load in winter.

**2. Summer and Winter have the highest average demand**

| Season | Average Demand (MW) |
| ------ | ------------------- |
| Summer | 19,523              |
| Winter | 18,030              |
| Fall   | 16,005              |
| Spring | 15,249              |

**3. Hot days significantly increase demand**

Days with maximum temperature above 80°F average **19,858 MW**, compared to **16,580 MW** on all other days; a difference of roughly 3,300 MW.

**4. Overall linear correlation is low (0.166)**  
Because the relationship is non-linear (U-shaped), a simple correlation understates the true impact of temperature extremes.
