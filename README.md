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
| **Useful columns** | temperature (°F), precipitation (in), pressure (in. Hg), wind speed (MPH), date |
| **Sample we checked** | Asheville Airport, NC, Jan–Mar 2017 (86 days; March data stops on the 27th) |

**Data stuff to handle:** `T` = trace precipitation, `s` = suspect value, `M` = missing, and some cells are blank.

### Questions We Are Asking

| # | Question | Expected form of the answer | Potential benefit |
|---|---|---|---|
| Q1 | Is air pressure lower on wet days than dry days? | Two average pressures (wet vs dry) and how big the gap is | Pressure could help signal incoming rain |
| Q2 | Is the daily temperature range (max − min) smaller on wet days? | Two average ranges (°F) and how big the gap is | Helps plan for energy use and comfort on rainy days |
| Q3 | How does air pressure change with temperature? | A fitted line and how strong the trend is | Shows whether temperature alone says anything about pressure |

**Other candidate questions we looked at (not selected):** 
Q4 winter vs summer high temperatures, 
Q5 size of the 24-hour temperature cycle by season, 
Q6 snow depth vs night-time low (not possible: snow depth is mostly blank).

**Why Q1–Q3:** we are interested in how wet and dry days compare, and in how pressure relates to temperature.

---

## Introduction / Context

- A **wet day** is a day with at least 0.01 in of precipitation. Trace amounts (`T`) count as dry.
- **Daily temperature range** = daily max temp − daily min temp.
- **Station pressure** is the pressure measured at the station's own elevation (Asheville is at 2117 ft), so values are lower than sea-level pressure.

---

## Implementation Details

All three questions use daily values from the same cleaned table (one row per day), so the cleaning step is shared.

**Shared cleaning steps**
1. Load the station CSV with pandas and keep the daily rows.
2. Convert columns to numbers. Treat `T` as 0.0 for precipitation, and drop or flag `s` (suspect) and `M` (missing) values.
3. Make a `wet` column (precipitation ≥ 0.01 in) and a `temp_range` column (max − min).

**Python packages:** `pandas`, `numpy`, `scipy` (t-test, linear fit), `matplotlib` (plots). Nothing else is needed.

### Q1: Pressure on wet vs dry days
- **Method:** two-sample (Welch) t-test.
- **Metrics:** average pressure (in. Hg) for wet days and dry days, difference of the averages, t-statistic, p-value.
- **Tools:** `pandas` (group by wet/dry), `scipy.stats.ttest_ind(..., equal_var=False)`.
- **Plot:** bar chart of the two averages (or a box plot), labeled in in. Hg.
- **Expected:** wet days have lower average pressure.
- **Sample preview (Asheville, Jan–Mar 2017):** wet 27.73 vs dry 27.86 in. Hg.

### Q2: Temperature range on wet vs dry days
- **Method:** two-sample (Welch) t-test.
- **Metrics:** daily range (max − min, °F) for wet and dry days, difference of the averages, t-statistic, p-value.
- **Tools:** `pandas`, `scipy.stats.ttest_ind(..., equal_var=False)`.
- **Plot:** bar chart of the two averages (or a box plot), labeled in °F.
- **Expected:** wet days have a smaller range, because clouds block sunlight in the day and trap heat at night.
- **Sample preview:** wet 16.9 vs dry 25.0 °F.

### Q3: Pressure vs temperature
- **Method:** linear fit (straight line) plus a correlation test.
- **Metrics:** slope (in. Hg per °F), intercept, correlation r, p-value.
- **Tools:** `scipy.stats.linregress` (or `numpy.polyfit`), `scipy.stats.pearsonr`.
- **Plot:** scatter plot of daily avg pressure (y) vs daily avg temperature (x) with the fitted line, axes labeled with units.
- **Expected:** little or no trend, so the line should be nearly flat.
- **Sample preview:** slope about −0.003 in. Hg per °F, r = −0.15, p = 0.16 (weak and not significant on 3 months).

### Planned additions (later phases)
- Screenshots: block diagram of the workflow, key code snippets, top-level code.

---

## Results (Answers to the Questions)

*To be added in Phase 2/3.*

## Conclusions

*To be added in Phase 3.*

## Actions That Need to Be Completed

*Checklist to be filled in (steps for someone who wants to repeat the project, plus any issues we run into).*

- [ ] Download the station CSV(s)
- [ ] Clean the data
- [ ] Q1 analysis and plot
- [ ] Q2 analysis and plot
- [ ] Q3 analysis and plot
- [ ] Write conclusions

## References / Source Files

- NOAA NCEI, Local Climatological Data (LCD) v2: https://www.ncei.noaa.gov/access/search/datasets/local-climatological-data-v2/
- Data.gov listing: https://catalog.data.gov/dataset/u-s-local-climatological-data-lcd
- SciPy documentation (`ttest_ind`, `linregress`): https://docs.scipy.org/doc/scipy/
