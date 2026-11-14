"""Build a static monthly calendar from NASA FIRMS archive CSVs."""

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/firms_raw"
OUTPUT = ROOT / "web/public/data/burning-calendar.json"
SENSORS = {"modis": "M-C61", "snpp": "SV-C2", "noaa20": "J1V-C2"}


def monthly_counts(code, boundary):
    paths = list(RAW.rglob(f"fire_archive_{code}_*.csv"))
    if len(paths) != 1:
        raise ValueError(f"Expected one {code} archive CSV, found {len(paths)}")

    columns = {"latitude", "longitude", "acq_date", "confidence", "type"}
    data = pd.read_csv(
        paths[0], usecols=lambda column: column in columns, dtype={"confidence": "string"}
    )
    months = pd.to_datetime(data.acq_date, format="%Y-%m-%d").dt.to_period("M")
    # Interior months approximate archive coverage. Edge months can be partial.
    first, last = months.min() + 1, months.max() - 1
    if pd.isna(first) or first > last:
        raise ValueError(f"{paths[0].name} has no interior archive months")

    if code == SENSORS["modis"]:
        keep = pd.to_numeric(data.confidence, errors="coerce").ge(30)
    else:
        keep = data.confidence.str.lower().isin(["n", "h"])
    if "type" in data:
        keep &= data["type"].isna() | data["type"].eq(0)
    if boundary is not None:
        from shapely import contains_xy

        keep &= contains_xy(boundary, data.longitude, data.latitude)

    counts = months[keep].value_counts()
    return counts.reindex(pd.period_range(first, last, freq="M"), fill_value=0)


def fit_monthly_factors(counts):
    paired = counts.loc["2012-01":"2025-12", ["modis", "snpp"]].dropna()
    if (paired.sum() <= 0).any():
        raise ValueError("No usable MODIS and S-NPP overlap for calibration")
    pooled = paired.snpp.sum() / paired.modis.sum()
    totals = paired.groupby(paired.index.month).sum().reindex(range(1, 13))
    ratios = totals.snpp / totals.modis.where(totals.modis.gt(0))
    return {int(month): float(k) for month, k in ratios.fillna(pooled).items()}


def fit_noaa20_ratio(counts):
    paired = counts.loc["2018-04":"2025-12", ["snpp", "noaa20"]].dropna()
    totals = paired.sum()
    if (totals <= 0).any():
        return None
    return float(totals.noaa20 / totals.snpp)


def calendar_value(month, row, factors, noaa20_ratio):
    if pd.notna(row.snpp):
        return int(row.snpp), "snpp-observed"
    if noaa20_ratio is not None and pd.notna(row.noaa20):
        return round(row.noaa20 / noaa20_ratio), "noaa20-adjusted"
    if month.year < 2012 and pd.notna(row.modis):
        return round(row.modis * factors[month.month]), "modis-estimated"
    return None, "no-coverage"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    area = parser.add_mutually_exclusive_group(required=True)
    area.add_argument("--boundary", type=Path, help="Borneo GeoJSON Polygon feature")
    area.add_argument("--download-area", action="store_true", help="Use the FIRMS download rectangle")
    args = parser.parse_args()
    boundary = None
    region = "Borneo FIRMS download area"
    if args.boundary:
        from shapely.geometry import shape

        feature = json.loads(args.boundary.read_text(encoding="utf-8"))
        boundary = shape(feature["geometry"])
        if boundary.geom_type not in {"Polygon", "MultiPolygon"} or not boundary.is_valid or boundary.is_empty:
            parser.error("Expected a valid, non-empty Polygon or MultiPolygon")
        region = "Borneo"

    counts = pd.concat(
        {name: monthly_counts(code, boundary) for name, code in SENSORS.items()},
        axis=1,
    ).sort_index()
    first = max(counts.index.min(), pd.Period("2002-01", freq="M"))
    counts = counts.reindex(pd.period_range(first, counts.index.max(), freq="M"))
    factors = fit_monthly_factors(counts)
    noaa20_ratio = fit_noaa20_ratio(counts)

    cells = []
    for month, row in counts.iterrows():
        count, source = calendar_value(month, row, factors, noaa20_ratio)
        cells.append({"year": month.year, "month": month.month, "count": count, "source": source})

    payload = {
        "region": region,
        "unit": "VIIRS-equivalent hotspot detections",
        "calibration": "Archive only, UTC, paired months in 2012–2025",
        "monthly_k": factors,
        "noaa20_ratio": noaa20_ratio,
        "cells": cells,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(cells)} months to {OUTPUT.relative_to(ROOT)}")
    print("Monthly k:", {month: round(k, 3) for month, k in factors.items()})


if __name__ == "__main__":
    main()
