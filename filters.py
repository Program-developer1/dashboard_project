import pandas as pd
import numpy as np


def load_data():
    df = pd.read_csv("2_5_month.csv")

    df["time"]    = pd.to_datetime(df["time"],    utc=True, errors="coerce")
    df["updated"] = pd.to_datetime(df["updated"], utc=True, errors="coerce")

    df["date"]        = df["time"].dt.date
    df["hour"]        = df["time"].dt.hour
    df["day_of_week"] = df["time"].dt.day_name()
    df["month"]       = df["time"].dt.month_name()

    for col in ["depth", "mag", "latitude", "longitude", "gap", "rms", "nst", "dmin"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["mag_category"] = pd.cut(
        df["mag"],
        bins=[0, 3, 4, 5, 6, 10],
        labels=["Minor (<3)", "Light (3-4)", "Moderate (4-5)", "Strong (5-6)", "Major (6+)"],
    )

    df["depth_category"] = pd.cut(
        df["depth"],
        bins=[0, 70, 300, 10000],
        labels=["Shallow (0-70km)", "Intermediate (70-300km)", "Deep (300+km)"],
    )

    df.dropna(subset=["time", "mag", "latitude", "longitude"], inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df


def apply_filters(df, date_range, mag_range, event_types, networks, search_text):
    filtered = df.copy()

    # date filter — works with both date objects and strings
    try:
        start = pd.Timestamp(date_range[0], tz="UTC")
        end   = pd.Timestamp(date_range[1], tz="UTC") + pd.Timedelta(days=1)
        filtered = filtered[(filtered["time"] >= start) & (filtered["time"] < end)]
    except Exception:
        pass

    # magnitude slider
    try:
        filtered = filtered[(filtered["mag"] >= mag_range[0]) & (filtered["mag"] <= mag_range[1])]
    except Exception:
        pass

    # event type multiselect — empty means all
    if event_types:
        filtered = filtered[filtered["type"].isin(event_types)]

    # network multiselect — empty means all
    if networks:
        filtered = filtered[filtered["net"].isin(networks)]

    # text search
    if search_text and search_text.strip():
        filtered = filtered[
            filtered["place"].str.contains(search_text.strip(), case=False, na=False)
        ]

    return filtered.reset_index(drop=True)


def get_kpis(df):
    if len(df) == 0:
        return {"total": 0, "avg_mag": 0, "max_mag": 0, "avg_depth": 0, "max_depth": 0, "unique_locations": 0}
    return {
        "total":            len(df),
        "avg_mag":          round(df["mag"].mean(), 2),
        "max_mag":          round(df["mag"].max(), 2),
        "avg_depth":        round(df["depth"].mean(), 2),
        "max_depth":        round(df["depth"].max(), 2),
        "unique_locations": df["place"].nunique(),
    }
