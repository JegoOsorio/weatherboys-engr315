"""Shared helper: builds one row per day from the hourly Luray Caverns Airport CSVs.

Put the 11 CSV files (LCD_USW00000416_2015.csv ... 2025.csv) in a folder called data/
and run all scripts from the main repo folder (the one that has README.md).

Units in the NOAA files: temperature in deg C, pressure in hPa, precipitation in mm.
"""
import glob
import pandas as pd

MIN_READINGS = 18   # skip a day if it has fewer than 18 temperature (or pressure) readings

def build_daily(data_glob="data/*.csv"):
    files = sorted(glob.glob(data_glob))
    if not files:
        raise SystemExit("No CSV files found in data/. Put the 11 yearly CSVs in a folder called data "
                         "and run this from the main repo folder.")
    cols = ["DATE", "HourlyDryBulbTemperature", "HourlyStationPressure", "HourlyPrecipitation"]
    df = pd.concat([pd.read_csv(f, usecols=cols, dtype=str, low_memory=False) for f in files],
                   ignore_index=True)
    df["day"] = pd.to_datetime(df["DATE"]).dt.date
    df["temp"] = pd.to_numeric(df["HourlyDryBulbTemperature"], errors="coerce")
    df["press"] = pd.to_numeric(df["HourlyStationPressure"], errors="coerce")
    df["precip"] = pd.to_numeric(df["HourlyPrecipitation"], errors="coerce")   # blank = no precipitation

    g = df.groupby("day")
    daily = pd.DataFrame({
        "n_temp": g["temp"].count(),
        "n_press": g["press"].count(),
        "temp_max": g["temp"].max(),
        "temp_min": g["temp"].min(),
        "temp_avg": g["temp"].mean(),
        "press_avg": g["press"].mean(),
        "precip_max": g["precip"].max(),
    })
    daily["wet"] = daily["precip_max"].fillna(0) > 0        # wet day = any hourly precipitation > 0 mm
    daily["temp_range"] = daily["temp_max"] - daily["temp_min"]
    return daily

if __name__ == "__main__":
    d = build_daily()
    d.to_csv("luray_daily.csv")
    print("Days in files:", len(d), "| wet days:", int(d["wet"].sum()))
    print("Saved luray_daily.csv")
