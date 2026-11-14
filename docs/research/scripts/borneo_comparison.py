import json
from pathlib import Path

import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "firms_borneo"
BOUNDARY = ROOT / "data" / "geoBoundaries-IDN-ADM1_simplified.geojson"
WK_MONTHLY = ROOT / "output" / "west_kalimantan" / "monthly_by_sensor.csv"
OUT = ROOT / "output" / "borneo"

SENSORS = {
    "M-C61": "MODIS",
    "SV-C2": "VIIRS S-NPP",
    "J1V-C2": "VIIRS NOAA-20",
    "J2V-C2": "VIIRS NOAA-21",
}
COLS = ["latitude", "longitude", "acq_date", "confidence", "frp", "daynight", "type"]
KALIMANTAN = ["West Kalimantan", "Central Kalimantan", "South Kalimantan", "East Kalimantan", "North Kalimantan"]
MALAYSIA_BRUNEI = "Sarawak + Sabah + Brunei"
AREA_KM2 = {
    "West Kalimantan": 147307,
    "Central Kalimantan": 153565,
    "South Kalimantan": 38744,
    "East Kalimantan": 127347,
    "North Kalimantan": 75468,
    MALAYSIA_BRUNEI: 204210,
}
BORNEO_BOX = (108.0, -4.6, 119.4, 7.5)


def provinces():
    features = json.loads(BOUNDARY.read_text(encoding="utf-8"))["features"]
    return {f["properties"]["shapeName"]: shape(f["geometry"]) for f in features}


def assign_region(df, shapes):
    region = np.full(len(df), None, dtype=object)
    x, y = df.longitude.values, df.latitude.values
    for name in KALIMANTAN:
        region[shapely.contains_xy(shapes[name], x, y)] = name
    other_idn = np.zeros(len(df), dtype=bool)
    for name, geom in shapes.items():
        if name not in KALIMANTAN:
            other_idn |= shapely.contains_xy(geom, x, y)
    minx, miny, maxx, maxy = BORNEO_BOX
    in_box = (x >= minx) & (x <= maxx) & (y >= miny) & (y <= maxy)
    region[pd.isna(region) & ~other_idn & in_box & (y > 0.8)] = MALAYSIA_BRUNEI
    return region


def load_sensor(code, shapes):
    frames = []
    for kind in ("archive", "nrt"):
        path = next(RAW.glob(f"fire_{kind}_{code}_*.csv"), None)
        if path is None:
            continue
        df = pd.read_csv(path, usecols=lambda c: c in COLS, dtype={"confidence": str})
        df["source"] = kind
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["acq_date"] = pd.to_datetime(df.acq_date)
    archive_end = df.loc[df.source == "archive", "acq_date"].max()
    df = df[(df.source == "archive") | (df.acq_date > archive_end)]
    if "type" in df:
        df = df[df["type"].isna() | (df["type"] == 0)]
    if code == "M-C61":
        df = df[pd.to_numeric(df.confidence, errors="coerce") >= 30]
    else:
        df = df[df.confidence.str.lower() != "l"]
    df = df.copy()
    df["region"] = assign_region(df, shapes)
    df = df[df.region.notna()]
    df["sensor"] = SENSORS[code]
    df["year"] = df.acq_date.dt.year
    df["month"] = df.acq_date.dt.month
    return df[["acq_date", "year", "month", "region", "frp", "sensor"]]


def per_month_factors(monthly, region=None):
    d = monthly if region is None else monthly[monthly.region == region]
    p = d.pivot_table(index=["year", "month"], columns="sensor", values="hotspots", aggfunc="sum").fillna(0)
    p = p[p.index.get_level_values("year").isin(range(2012, 2026))]
    g = p.groupby(level="month")[["MODIS", "VIIRS S-NPP"]].sum()
    return (g["VIIRS S-NPP"] / g["MODIS"]).rename("k")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    shapes = provinces()
    hotspots = pd.concat([load_sensor(c, shapes) for c in SENSORS], ignore_index=True)
    print("date range:", hotspots.acq_date.min().date(), "to", hotspots.acq_date.max().date())

    monthly = hotspots.groupby(["region", "sensor", "year", "month"]).size().rename("hotspots").reset_index()
    monthly.to_csv(OUT / "monthly_by_region_sensor.csv", index=False)

    wk_old = pd.read_csv(WK_MONTHLY)
    wk_new = monthly[monthly.region == "West Kalimantan"].drop(columns="region")
    check = wk_old.merge(wk_new, on=["sensor", "year", "month"], how="inner", suffixes=("_old", "_new"))
    check = check[check.year <= 2025]
    agree = check.groupby("sensor")[["hotspots_old", "hotspots_new"]].sum()
    agree["diff_pct"] = (agree.hotspots_new / agree.hotspots_old - 1) * 100
    print("\n== West Kalimantan: new Borneo pull vs existing WK data (matching months to 2025) ==")
    print(agree.round(2).to_string())

    full_years = hotspots[hotspots.year.between(2012, 2025)]
    annual = full_years.groupby(["region", "sensor"]).size().unstack("sensor").fillna(0)
    annual = annual / 14
    annual["S-NPP per 1000 km2/yr"] = annual["VIIRS S-NPP"] / pd.Series(AREA_KM2) * 1000
    annual["S-NPP/MODIS"] = annual["VIIRS S-NPP"] / annual["MODIS"]
    total = full_years[full_years.sensor == "VIIRS S-NPP"].groupby("region").size()
    annual["share of Borneo S-NPP"] = total / total.sum() * 100
    print("\n== Mean hotspots per year 2012-2025 by region ==")
    print(annual.round(2).to_string())
    annual.to_csv(OUT / "region_summary_2012_2025.csv")

    snpp = full_years[full_years.sensor == "VIIRS S-NPP"]
    season = snpp.groupby(["region", "month"]).size().unstack("month").fillna(0)
    season = season.div(season.sum(axis=1), axis=0) * 100
    print("\n== Seasonality: % of S-NPP hotspots per calendar month, 2012-2025 ==")
    print(season.round(1).to_string())
    season.to_csv(OUT / "seasonality_share.csv")

    k_wk = per_month_factors(monthly, "West Kalimantan")
    k_borneo = per_month_factors(monthly)
    k = pd.DataFrame({"k West Kalimantan": k_wk, "k all Borneo": k_borneo})
    for r in [*KALIMANTAN, MALAYSIA_BRUNEI]:
        k[f"k {r}"] = per_month_factors(monthly, r)
    print("\n== MODIS-to-VIIRS factor k(m) by region (2012-2025) ==")
    print(k.round(2).to_string())
    k.to_csv(OUT / "factors_by_region.csv")

    p = monthly.pivot_table(index=["region", "year", "month"], columns="sensor", values="hotspots", aggfunc="sum").fillna(0).reset_index()
    rows = []
    for r in [*KALIMANTAN, MALAYSIA_BRUNEI]:
        d = p[(p.region == r) & p.year.between(2012, 2025)]
        for label, kk in (("own k", k[f"k {r}"]), ("WK k", k_wk)):
            pred = d.MODIS * d.month.map(kk)
            yr = pd.DataFrame({"year": d.year, "pred": pred, "obs": d["VIIRS S-NPP"]}).groupby("year").sum()
            err = (yr.pred / yr.obs - 1).abs().median() * 100
            rows.append({"region": r, "factors": label, "median annual abs error %": err})
    transfer = pd.DataFrame(rows).pivot(index="region", columns="factors", values="median annual abs error %")
    print("\n== Does the West Kalimantan k(m) transfer? Median |error| of annual VIIRS-equivalent totals ==")
    print(transfer.round(1).to_string())

    back = p[p.year.between(2001, 2011)].copy()
    back["viirs_eq_wk_k"] = back.MODIS * back.month.map(k_wk)
    back["viirs_eq_own_k"] = [m * k[f"k {r}"].get(mo, np.nan) for m, r, mo in zip(back.MODIS, back.region, back.month)]
    ext = back.groupby("region")[["MODIS", "viirs_eq_wk_k", "viirs_eq_own_k"]].sum() / 11
    print("\n== Extrapolated 2001-2011 VIIRS-equivalent mean hotspots per year ==")
    print(ext.round(0).to_string())

    yearly = p.groupby(["region", "year"])[["MODIS", "VIIRS S-NPP"]].sum().reset_index()
    yearly.to_csv(OUT / "yearly_by_region.csv", index=False)
    corr = yearly[yearly.year.between(2001, 2025)].pivot(index="year", columns="region", values="MODIS").corr()["West Kalimantan"]
    print("\n== Correlation of annual MODIS counts with West Kalimantan, 2001-2025 ==")
    print(corr.round(3).to_string())
    top = yearly[yearly.region == "West Kalimantan"].nlargest(5, "MODIS")[["year", "MODIS"]]
    print("\nWest Kalimantan top-5 MODIS years:", top.year.tolist())
    print("Borneo top-5 MODIS years:", yearly.groupby("year").MODIS.sum().nlargest(5).index.tolist())


if __name__ == "__main__":
    main()
