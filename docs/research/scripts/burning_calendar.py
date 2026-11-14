import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "firms_raw"
OUT = ROOT / "output" / "west_kalimantan"
BOUNDARY = ROOT / "data" / "geoBoundaries-IDN-ADM1_simplified.geojson"
REGION = sys.argv[1] if len(sys.argv) > 1 else "West Kalimantan"

SENSORS = {
    "M-C61": "MODIS",
    "SV-C2": "VIIRS S-NPP",
    "J1V-C2": "VIIRS NOAA-20",
}
COLS = ["latitude", "longitude", "acq_date", "confidence", "frp", "daynight", "type"]


def region_geometry(name):
    features = json.loads(BOUNDARY.read_text(encoding="utf-8"))["features"]
    match = next(f for f in features if f["properties"]["shapeName"] == name)
    return shape(match["geometry"])


def load_sensor(code, geom):
    frames = []
    for kind in ("archive", "nrt"):
        path = next(RAW.glob(f"fire_{kind}_{code}_*.csv"), None)
        if path is None:
            continue
        df = pd.read_csv(path, usecols=lambda c: c in COLS, dtype={"confidence": str})
        df["source"] = kind
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    minx, miny, maxx, maxy = geom.bounds
    df = df[df.longitude.between(minx, maxx) & df.latitude.between(miny, maxy)]
    df = df[shapely.contains_xy(geom, df.longitude.values, df.latitude.values)].copy()
    df["acq_date"] = pd.to_datetime(df.acq_date)
    archive_end = df.loc[df.source == "archive", "acq_date"].max()
    df = df[(df.source == "archive") | (df.acq_date > archive_end)]
    if "type" in df:
        df = df[df["type"].isna() | (df["type"] == 0)]
    if code == "M-C61":
        df = df[pd.to_numeric(df.confidence, errors="coerce") >= 30]
    else:
        df = df[df.confidence.str.lower() != "l"]
    df["sensor"] = SENSORS[code]
    return df[["acq_date", "latitude", "longitude", "frp", "daynight", "sensor"]]


def classify(share):
    if share >= 0.15:
        return "Peak burning"
    if share >= 0.08:
        return "Active burning"
    if share >= 0.04:
        return "Moderate"
    return "Low"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    geom = region_geometry(REGION)
    hotspots = pd.concat([load_sensor(c, geom) for c in SENSORS], ignore_index=True)
    hotspots.to_csv(OUT / "hotspots_filtered.csv.gz", index=False)

    daily = (
        hotspots.groupby([hotspots.acq_date.dt.date.rename("date"), "sensor"])
        .agg(hotspots=("frp", "size"), frp_sum=("frp", "sum"))
        .reset_index()
    )
    daily.to_csv(OUT / "daily_by_sensor.csv", index=False)

    hotspots["year"] = hotspots.acq_date.dt.year
    hotspots["month"] = hotspots.acq_date.dt.month
    monthly = hotspots.groupby(["sensor", "year", "month"]).size().rename("hotspots").reset_index()
    monthly.to_csv(OUT / "monthly_by_sensor.csv", index=False)

    calendars = []
    for sensor, grp in monthly.groupby("sensor"):
        years = grp.year.unique()
        complete = [y for y in years if grp[grp.year == y].month.nunique() == 12 or y == years.max()]
        full = (
            grp.pivot(index="year", columns="month", values="hotspots")
            .reindex(columns=range(1, 13))
            .fillna(0)
            .loc[complete]
        )
        full.to_csv(OUT / f"year_month_matrix_{sensor.replace(' ', '_')}.csv")
        mean = full.mean()
        cal = pd.DataFrame(
            {
                "sensor": sensor,
                "month": range(1, 13),
                "mean_hotspots": mean.values.round(1),
                "median_hotspots": full.median().values,
                "p90_hotspots": full.quantile(0.9).values,
                "share_of_annual": (mean / mean.sum()).values.round(3),
                "years": f"{full.index.min()}-{full.index.max()}",
            }
        )
        cal["phase"] = cal.share_of_annual.map(classify)
        calendars.append(cal)
    calendar = pd.concat(calendars, ignore_index=True)
    calendar.to_csv(OUT / "burning_calendar.csv", index=False)

    print(hotspots.groupby("sensor").agg(n=("frp", "size"), start=("acq_date", "min"), end=("acq_date", "max")))
    print(calendar.pivot(index="month", columns="sensor", values="share_of_annual"))
    print(calendar.pivot(index="month", columns="sensor", values="phase"))


if __name__ == "__main__":
    main()
