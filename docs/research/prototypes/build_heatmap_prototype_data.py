import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1] / "output" / "west_kalimantan"
OUT = Path(__file__).resolve().parent / "heatmap-calendar.PROTOTYPE.data.js"
CELL = 0.1
R = 1.01

df = pd.read_csv(ROOT / "hotspots_filtered.csv.gz", parse_dates=["acq_date"])
df["y"] = df.acq_date.dt.year
df["m"] = df.acq_date.dt.month
df["gx"] = (df.longitude // CELL).astype(int)
df["gy"] = (df.latitude // CELL).astype(int)

counts = df.groupby(["sensor", "y", "m"]).size().unstack("sensor", fill_value=0)
overlap = counts[counts.index.get_level_values("y") >= 2012]
k = {}
for m in range(1, 13):
    rows = overlap[overlap.index.get_level_values("m") == m]
    k[m] = float(rows["VIIRS S-NPP"].sum() / max(rows["MODIS"].sum(), 1))

grid = df.groupby(["sensor", "y", "m", "gx", "gy"]).size().rename("n").reset_index()
months = {}
for (y, m), row in counts.iterrows():
    if row.get("VIIRS S-NPP", 0) > 0:
        src, w = "VIIRS S-NPP", 1.0
    elif row.get("VIIRS NOAA-20", 0) > 0:
        src, w = "VIIRS NOAA-20", 1 / R
    else:
        src, w = "MODIS", k[m]
    g = grid[(grid.sensor == src) & (grid.y == y) & (grid.m == m)]
    cells = [[int(a), int(b), round(n * w, 1)] for a, b, n in zip(g.gx, g.gy, g.n)]
    months[f"{y}-{m:02d}"] = {
        "src": src,
        "raw": int(row.get(src, 0)),
        "h": round(float(row.get(src, 0)) * w, 1),
        "cells": cells,
    }

payload = {"cell": CELL, "k": k, "r": R, "months": months}
OUT.write_text("window.PROTO_DATA=" + json.dumps(payload, separators=(",", ":")) + ";")
print(OUT, OUT.stat().st_size, len(months), file=sys.stderr)
