import json
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import shapely
from shapely.geometry import mapping, shape
from shapely.ops import unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "data" / "firms_borneo"
GB = ROOT / "data" / "geoboundaries"
OUT = HERE / "borneo.PROTOTYPE.data.js"
COLS = ["latitude", "longitude", "acq_date", "confidence", "type"]
CELL = 0.1
R = 1.01
ADM1 = {
    "IDN": ["West Kalimantan", "Central Kalimantan", "South Kalimantan", "East Kalimantan", "North Kalimantan"],
    "MYS": ["Sarawak", "Sabah", "Labuan"],
    "BRN": None,
}
ADM2_URL = "https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/gbOpen/{iso}/ADM2/geoBoundaries-{iso}-ADM2_simplified.geojson"


def adm1():
    units = {}
    for iso, names in ADM1.items():
        feats = json.loads((GB / f"{iso}.geojson").read_text(encoding="utf-8"))["features"]
        geoms = {f["properties"]["shapeName"]: shape(f["geometry"]).buffer(0) for f in feats}
        if names is None:
            units["Brunei"] = unary_union(list(geoms.values()))
        else:
            for n in names:
                units[n] = geoms[n]
    units["Sabah"] = unary_union([units.pop("Sabah"), units.pop("Labuan")])
    return units


def adm2(units):
    out = {}
    for iso in ("IDN", "MYS"):
        path = GB / f"{iso}_ADM2.geojson"
        if not path.exists():
            urllib.request.urlretrieve(ADM2_URL.format(iso=iso), path)
        for f in json.loads(path.read_text(encoding="utf-8"))["features"]:
            g = shape(f["geometry"]).buffer(0)
            c = g.representative_point()
            parent = next((n for n, u in units.items() if u.contains(c)), None)
            if parent:
                out[f"{f['properties']['shapeName']} ({parent})"] = (parent, g)
    return out


def load_sensor(code):
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
    return df


def geo(g, tol):
    return mapping(shapely.set_precision(g.simplify(tol, preserve_topology=True), 0.001))


units = adm1()
borneo = unary_union(list(units.values()))
sensors = {"MODIS": "M-C61", "VIIRS S-NPP": "SV-C2", "VIIRS NOAA-20": "J1V-C2"}
frames = []
for name, code in sensors.items():
    d = load_sensor(code)
    d = d[shapely.contains_xy(borneo, d.longitude.values, d.latitude.values)]
    d["sensor"] = name
    frames.append(d[["acq_date", "latitude", "longitude", "sensor"]])
    print(name, len(d), file=sys.stderr)
df = pd.concat(frames, ignore_index=True)
df["y"] = df.acq_date.dt.year
df["m"] = df.acq_date.dt.month
df["d"] = df.acq_date.dt.day
df["gx"] = np.floor(df.longitude / CELL).astype(int)
df["gy"] = np.floor(df.latitude / CELL).astype(int)

last = df.acq_date.max()
cur_key = (last.year, last.month)
cut_day = last.day

counts = df.groupby(["y", "m", "sensor"]).size().unstack("sensor", fill_value=0)
ov = counts[(counts.index.get_level_values("y") >= 2012) & (counts.index != cur_key)]
k = {m: float(ov.xs(m, level="m")["VIIRS S-NPP"].sum() / ov.xs(m, level="m")["MODIS"].sum()) for m in range(1, 13)}

cells = df[["gx", "gy"]].drop_duplicates().sort_values(["gy", "gx"]).reset_index(drop=True)
cid = {(a, b): i for i, (a, b) in enumerate(zip(cells.gx, cells.gy))}
df["c"] = [cid[(a, b)] for a, b in zip(df.gx, df.gy)]

grid = df.groupby(["y", "m", "sensor", "c"]).size()
grid_part = df[df.d <= cut_day].groupby(["y", "m", "sensor", "c"]).size()
months = {}
for (y, m), row in counts.iterrows():
    if row.get("VIIRS S-NPP", 0) > 0:
        src, w = "VIIRS S-NPP", 1.0
    elif row.get("VIIRS NOAA-20", 0) > 0:
        src, w = "VIIRS NOAA-20", 1 / R
    else:
        src, w = "MODIS", k[m]
    g = grid.loc[(y, m, src)]
    rec = {"s": src, "w": round(w, 4), "c": [[int(c), int(n)] for c, n in g.items()]}
    if m == cur_key[1]:
        try:
            gp = grid_part.loc[(y, m, src)]
            rec["p"] = [[int(c), int(n)] for c, n in gp.items()]
        except KeyError:
            rec["p"] = []
    months[f"{y}-{m:02d}"] = rec

a2 = adm2(units)
presets = [{"name": n, "level": 1, "parent": None, "geom": geo(g, 0.01)} for n, g in units.items()]
presets += [{"name": n, "level": 2, "parent": p, "geom": geo(g, 0.01)} for n, (p, g) in sorted(a2.items())]
payload = {
    "cell": CELL,
    "k": k,
    "r": R,
    "cells": cells[["gx", "gy"]].values.tolist(),
    "months": months,
    "current": f"{cur_key[0]}-{cur_key[1]:02d}",
    "cutDay": int(cut_day),
    "lastDate": str(last.date()),
    "presets": presets,
}
OUT.write_text("window.PROTO_DATA=" + json.dumps(payload, separators=(",", ":")) + ";", encoding="utf-8")
print(OUT.stat().st_size, len(cells), len(months), len(presets), last.date(), file=sys.stderr)
