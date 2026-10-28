# What Does Airport Data Tell Us?

**Team Name:** Weatherboys
**Contributors:** Jego Osorio, Gavin White, Seth Leland
**Course:** ENGR 315 Computational Methods in Engineering

---

## Objective and Motivation

Weather affects flights, energy use and safety. We want to see how weather variables (pressure, temperature, rain) move together, and measure how much they differ or change, not just yes/no.

### Dataset

| | |
|---|---|
| **Name** | NOAA Local Climatological Data (LCD) |
| **What it is** | Hourly and daily readings from airport weather stations |
| **Download** | [data.gov listing](https://catalog.data.gov/dataset/u-s-local-climatological-data-lcd?from_hint=eyJxIjoibG9jYWwgY2xpbWF0b2xvZ2ljYWwifQ%3D%3D), [NOAA NCEI LCD v2](https://www.ncei.noaa.gov/access/search/datasets/local-climatological-data-v2/) |
| **How it was collected** | NOAA sensors and observers at airports, for aviation, forecasting and climate records |
| **Format / size** | Public CSV, one file per station per year, so easy to handle |
| **Useful columns** | `HourlyDryBulbTemperature`, `HourlyStationPressure`, `HourlyPrecipitation`, `DATE` |
| **Station used** | Luray Caverns Airport, VA (station ID USW00000416), 2015–2025, one CSV per year (about 15 MB each) |
| **Units in the files** | Temperature in °C, pressure in hPa, precipitation in mm |
| **Early look** | We first looked at a 3-month Asheville, NC sample (Jan–Mar 2017) to plan the questions, then switched to Luray for 11 years of data |

**Data quirks we found:** this station has only hourly rows (about 3 per hour); the `Daily...` columns are all empty, so we build daily values ourselves from the hourly readings. `HourlyPrecipitation` is blank when there was no precipitation. Station pressure is missing for some hours (about 36% of 2025 rows). Temperatures are whole °C.

### Questions We Are Asking

| # | Question | Expected form of the answer | Potential benefit |
|---|---|---|---|
| Q1 | Is air pressure lower on wet days than dry days? | Two average pressures (wet vs dry) and how big the gap is | Pressure could help signal incoming rain |
| Q2 | Is the daily temperature range (max − min) smaller on wet days? | Two average ranges (°C) and how big the gap is | Helps plan for energy use and comfort on rainy days |
| Q3 | How does air pressure change with temperature? | A fitted line and how strong the trend is | Shows whether temperature alone says anything about pressure |

**Other candidate questions we looked at (not selected):** 
Q4 winter vs summer high temperatures, 
Q5 size of the 24-hour temperature cycle by season, 
Q6 snow depth vs night-time low (not possible: snow depth is mostly blank).

**Why Q1–Q3:** we are interested in how wet and dry days compare, and in how pressure relates to temperature.

---

## Introduction / Context

- A **wet day** is a day where the station reported any precipitation (greater than 0 mm) in at least one hourly reading. All other days are dry.
- **Daily values** are made from the hourly rows: daily max and min temperature, average temperature, and average station pressure. Days with fewer than 18 readings are skipped.
- **Daily temperature range** = daily max temp − daily min temp.
- **Station pressure** is the pressure measured at the station's own elevation (Luray is at about 275 m elevation), so values are lower than sea-level pressure.

---

## Implementation Details

All three questions use daily values from the same cleaned table (one row per day), so the cleaning step is shared.

**Shared cleaning steps**
1. Load the 11 yearly CSVs with pandas (`scripts/make_daily_table.py`).
2. Convert the hourly columns to numbers. Blank precipitation means none.
3. Group by day to get max/min/average temperature and average pressure. Skip days with fewer than 18 readings.
4. Make a `wet` column (any precipitation > 0 mm) and a `temp_range` column (max − min).

**Python packages:** `pandas`, `numpy`, `scipy` (t-test, linear fit), `matplotlib` (plots). Nothing else is needed.

### Q1: Pressure on wet vs dry days
- **Method:** two-sample (Welch) t-test.
- **Metrics:** average pressure (hPa) for wet days and dry days, difference of the averages, t-statistic, p-value.
- **Tools:** `pandas` (group by wet/dry), `scipy.stats.ttest_ind(..., equal_var=False)`.
- **Plot:** bar chart of the two averages (or a box plot), labeled in hPa.
- **Expected:** wet days have lower average pressure.
- **Early result (Luray, 2015–2025, 3,823 days):** wet 982.4 vs dry 986.2 hPa (1,191 wet and 2,632 dry days).

### Q2: Temperature range on wet vs dry days
- **Method:** two-sample (Welch) t-test.
- **Metrics:** daily range (max − min, °C) for wet and dry days, difference of the averages, t-statistic, p-value.
- **Tools:** `pandas`, `scipy.stats.ttest_ind(..., equal_var=False)`.
- **Plot:** bar chart of the two averages (or a box plot), labeled in °C.
- **Expected:** wet days have a smaller range, because clouds block sunlight in the day and trap heat at night.
- **Early result (3,998 days):** wet 10.3 vs dry 13.7 °C (1,236 wet and 2,762 dry days).

### Q3: Pressure vs temperature
- **Method:** linear fit (straight line) plus a correlation test.
- **Metrics:** slope (hPa per °C), intercept, correlation r, p-value.
- **Tools:** `scipy.stats.linregress` (or `numpy.polyfit`), `scipy.stats.pearsonr`.
- **Plot:** scatter plot of daily avg pressure (y) vs daily avg temperature (x) with the fitted line, axes labeled with units.
- **Expected:** little or no trend, so the line should be nearly flat.
- **Early result:** slope about −0.15 hPa per °C, r = −0.22. The trend is real but weak (temperature explains about 5% of the pressure changes).

> These are early results from our first pass. Final numbers may change after we double check the cleaning (for example, how we decide a day is wet).

### Planned additions (later phases)
- Screenshots: block diagram of the workflow, key code snippets, top-level code.

---

## Results (Answers to the Questions)

*To be added in Phase 2/3.*

## Conclusions

*To be added in Phase 3.*

## Actions That Need to Be Completed

*Checklist to be filled in (steps for someone who wants to repeat the project, plus any issues we run into).*

- [x] Download the station CSVs (2015–2025)
- [ ] Put them in a `data/` folder and run `scripts/make_daily_table.py`
- [ ] Double check the wet-day rule
- [ ] Q1 analysis and plot
- [ ] Q2 analysis and plot
- [ ] Q3 analysis and plot
- [ ] Write conclusions

## References / Source Files

- Luray Caverns Airport, VA, station USW00000416, from the dataset below.
- NOAA NCEI, Local Climatological Data (LCD) v2: https://www.ncei.noaa.gov/access/search/datasets/local-climatological-data-v2/
- Data.gov listing: https://catalog.data.gov/dataset/u-s-local-climatological-data-lcd
- SciPy documentation (`ttest_ind`, `linregress`): https://docs.scipy.org/doc/scipy/
