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

Analysis of daily NYISO electricity demand and temperature data from **January 2022 to October 2026** reveals a clear relationship between weather extremes and electricity demand in New York State.

### 1. Temperature Extremes Are the Primary Driver of Demand Spikes

Electricity demand shows a strong **U-shaped relationship with temperature**, with demand increasing during both hot and cold weather.

- **Hot days** (maximum temperature > 80°F): Average demand ≈ **19,858 MW**
- **Cold days** (maximum temperature < 40°F): Average demand ≈ **18,349 MW**
- **Mild/Warm days** (40–80°F): Average demand ≈ **16,100–16,200 MW**

Demand rises significantly during both **summer heatwaves**, driven primarily by air-conditioning load, and **winter cold snaps**, when heating demand increases.

### 2. Highest Demand Days Occurred During Summer Heatwaves

The peak demand day in the dataset was **June 25, 2025**, when average system demand reached **26,554 MW**.

On that day:

- **New York City:** 96°F
- **Albany:** 92°F
- **Buffalo:** 85°F

Other high-demand days, including **June 24, 2025** and **July 3, 2026**, followed the same pattern: exceptionally high temperatures across New York coincided with some of the highest system demand levels.

### 3. Mild Weather Produces the Lowest Demand

Days with maximum temperatures between **40°F and 80°F** consistently show the lowest average electricity demand, at approximately **16,100–16,200 MW**.

These conditions represent the **shoulder seasons**, when neither heating nor cooling loads are dominant.

### Operational Takeaway

The analysis suggests that **temperature extremes should be a primary variable for monitoring electricity demand risk**. In particular, widespread summer heat events can create the highest system loads, while severe winter cold can also substantially increase demand.
