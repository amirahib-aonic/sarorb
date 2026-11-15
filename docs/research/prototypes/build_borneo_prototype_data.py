import json
import math
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
COLS = ["latitude", "longitude", "acq_date", "acq_time", "confidence", "frp", "satellite", "type"]
CELL = 0.1
R = 1.01
KM_PER_DEG = 111.32
COS_LAT = 0.998
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
    df["acq_time"] = pd.to_numeric(df["acq_time"], errors="coerce").fillna(0).astype(int)
    df["frp"] = pd.to_numeric(df["frp"], errors="coerce").fillna(0.0)
    return df


def geo(g, tol):
    return mapping(shapely.set_precision(g.simplify(tol, preserve_topology=True), 0.001))


def percentile(vals, p):
    s = sorted(vals)
    pos = (len(s) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    return s[lo] + (s[hi] - s[lo]) * (pos - lo)


def build_month_vectors(sub_df, is_modis, cid, cell_xy):
    if is_modis:
        r_km, link_km, max_missed, min_shift_km = 2.0, 5.0, 2, 1.0
        prio = np.where(sub_df.satellite.values == "Aqua", 0, 1)
        qkeys = list(zip(
            sub_df.win.values.tolist(),
            np.floor(sub_df.latitude.values / 0.25).astype(int).tolist(),
            np.floor(sub_df.longitude.values / 0.25).astype(int).tolist(),
        ))
        best = {}
        for k_q, p_q in zip(qkeys, prio):
            if k_q not in best or p_q < best[k_q]:
                best[k_q] = p_q
        sub_df = sub_df[[p_q == best[k_q] for k_q, p_q in zip(qkeys, prio)]]
    else:
        r_km, link_km, max_missed, min_shift_km = 0.75, 5.0, 2, 0.375

    if sub_df.empty:
        return []

    r_deg2 = (r_km / KM_PER_DEG) ** 2
    link_deg2 = (link_km / KM_PER_DEG) ** 2
    min_shift_deg2 = (min_shift_km / KM_PER_DEG) ** 2
    c_deg = (r_km / KM_PER_DEG) / 0.98
    l_deg = (link_km / KM_PER_DEG) / 0.98

    lats = sub_df.latitude.values
    lons = sub_df.longitude.values
    frps = sub_df.frp.values
    wins = sub_df.win.values
    cs_arr = sub_df.c.values
    gx = np.floor(lons / c_deg).astype(int)
    gy = np.floor(lats / c_deg).astype(int)
    order = np.argsort(wins, kind="mergesort")
    lats, lons, frps, wins, cs_arr, gx, gy = (
        lats[order], lons[order], frps[order], wins[order], cs_arr[order], gx[order], gy[order]
    )
    u_wins, idx_start, counts = np.unique(wins, return_index=True, return_counts=True)

    by_win = {}
    for w, s, cnt in zip(u_wins.tolist(), idx_start.tolist(), counts.tolist()):
        if cnt == 1:
            f = float(frps[s]) if frps[s] > 0 else None
            by_win[w] = [(w, float(lats[s]), float(lons[s]), f, int(cs_arr[s]))]
            continue
        parent = list(range(cnt))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        grid = {}
        for i in range(cnt):
            x, y = int(gx[s + i]), int(gy[s + i])
            la, lo = float(lats[s + i]), float(lons[s + i])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for j in grid.get((x + dx, y + dy), ()):
                        dla = la - float(lats[s + j])
                        dlo = (lo - float(lons[s + j])) * COS_LAT
                        if dla * dla + dlo * dlo <= r_deg2:
                            parent[find(i)] = find(j)
            grid.setdefault((x, y), []).append(i)

        grps = {}
        for i in range(cnt):
            rt = find(i)
            g = grps.get(rt)
            if g is None:
                g = grps[rt] = [0.0, 0.0, 0.0, 0, 0, int(cs_arr[s + i])]
            g[0] += float(lats[s + i])
            g[1] += float(lons[s + i])
            g[4] += 1
            if frps[s + i] > 0:
                g[2] += float(frps[s + i])
                g[3] += 1
        by_win[w] = [(w, g[0] / g[4], g[1] / g[4], g[2] if g[3] else None, g[5]) for g in grps.values()]

    events = []
    open_ev = []
    for w in sorted(by_win.keys()):
        open_ev = [e for e in open_ev if w - e[-1][0] - 1 <= max_missed]
        ev_grid = {}
        for ei, e in enumerate(open_ev):
            _, la, lo, _, _ = e[-1]
            ev_grid.setdefault((math.floor(lo / l_deg), math.floor(la / l_deg)), []).append(ei)
        cs = by_win[w]
        pairs = []
        for ci, c in enumerate(cs):
            _, la, lo, _, _ = c
            cx, cy = math.floor(lo / l_deg), math.floor(la / l_deg)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for ei in ev_grid.get((cx + dx, cy + dy), ()):
                        last = open_ev[ei][-1]
                        dla = last[1] - la
                        dlo = (last[2] - lo) * COS_LAT
                        d2 = dla * dla + dlo * dlo
                        if d2 <= link_deg2:
                            pairs.append((d2, ei, ci))
        pairs.sort(key=lambda x: x[0])
        ue, uc = set(), set()
        for _, ei, ci in pairs:
            if ei in ue or ci in uc:
                continue
            ue.add(ei)
            uc.add(ci)
            open_ev[ei].append(cs[ci])
        for ci, c in enumerate(cs):
            if ci not in uc:
                e = [c]
                events.append(e)
                open_ev.append(e)

    peaks = []
    for e in events:
        fs = [c[3] for c in e if c[3] is not None]
        if fs:
            peaks.append(max(fs))
    cutoff = percentile(peaks, 0.75) if len(peaks) >= 4 else 0.0

    encoded = []
    for e in events:
        fs = [c[3] for c in e if c[3] is not None]
        if not fs:
            continue
        pk = max(fs)
        if len(peaks) >= 4 and pk < cutoff - 1e-9:
            continue
        if len(e) < 2:
            continue
        has_shift = any(
            (e[i][1] - e[i - 1][1]) ** 2 + ((e[i][2] - e[i - 1][2]) * COS_LAT) ** 2 >= min_shift_deg2
            for i in range(1, len(e))
        )
        if not has_shift:
            continue
        w0, la0, lo0, f0, fb0 = e[0]
        gx0, gy0 = math.floor(lo0 / CELL), math.floor(la0 / CELL)
        c0 = cid.get((gx0, gy0))
        if c0 is None:
            c0 = fb0
            gx0, gy0 = cell_xy[c0]
        dy0 = int(round((la0 - gy0 * CELL) * 1000))
        dx0 = int(round((lo0 - gx0 * CELL) * 1000))
        enc = [c0, dy0, dx0, int(w0), int(round(f0 or 0))]
        cur_w = int(w0)
        cur_lat = gy0 * CELL + dy0 * 0.001
        cur_lon = gx0 * CELL + dx0 * 0.001
        for wi, lai, loi, fi, _ in e[1:]:
            dw = int(wi) - cur_w
            dlat = int(round((lai - cur_lat) * 1000))
            dlon = int(round((loi - cur_lon) * 1000))
            enc.extend([dw, dlat, dlon, int(round(fi or 0))])
            cur_w = int(wi)
            cur_lat += dlat * 0.001
            cur_lon += dlon * 0.001
        encoded.append(enc)
    return encoded


units = adm1()
borneo = unary_union(list(units.values()))
sensors = {"MODIS": "M-C61", "VIIRS S-NPP": "SV-C2", "VIIRS NOAA-20": "J1V-C2"}
frames = []
for name, code in sensors.items():
    d = load_sensor(code)
    d = d[shapely.contains_xy(borneo, d.longitude.values, d.latitude.values)]
    d["sensor"] = name
    frames.append(d[["acq_date", "acq_time", "latitude", "longitude", "frp", "satellite", "sensor"]])
    print(name, len(d), file=sys.stderr)
df = pd.concat(frames, ignore_index=True)
df["y"] = df.acq_date.dt.year
df["m"] = df.acq_date.dt.month
df["d"] = df.acq_date.dt.day
df["gx"] = np.floor(df.longitude / CELL).astype(int)
df["gy"] = np.floor(df.latitude / CELL).astype(int)
df["win"] = ((df["d"] - 1) * 1440 + (df["acq_time"] // 100) * 60 + (df["acq_time"] % 100) + 120) // 720

last = df.acq_date.max()
cur_key = (last.year, last.month)
cut_day = last.day

counts = df.groupby(["y", "m", "sensor"]).size().unstack("sensor", fill_value=0)
ov = counts[(counts.index.get_level_values("y") >= 2012) & (counts.index != cur_key)]
k = {m: float(ov.xs(m, level="m")["VIIRS S-NPP"].sum() / ov.xs(m, level="m")["MODIS"].sum()) for m in range(1, 13)}

cells = df[["gx", "gy"]].drop_duplicates().sort_values(["gy", "gx"]).reset_index(drop=True)
cell_xy = list(zip(cells.gx.tolist(), cells.gy.tolist()))
cid = {xy: i for i, xy in enumerate(cell_xy)}
df["c"] = [cid[(a, b)] for a, b in zip(df.gx, df.gy)]

grid = df.groupby(["y", "m", "sensor", "c"]).size()
grid_part = df[df.d <= cut_day].groupby(["y", "m", "sensor", "c"]).size()
next_m = cur_key[1] % 12 + 1
daily = df[df.m.isin([cur_key[1], next_m])].groupby(["y", "m", "sensor", "c", "d"]).size()
by_yms = {k_g: grp for k_g, grp in df.groupby(["y", "m", "sensor"], sort=False)}
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
    if m in (cur_key[1], next_m):
        gd = daily.loc[(y, m, src)]
        rec["d"] = [[int(c), int(d), int(n)] for (c, d), n in gd.items()]
    sub_df = by_yms.get((y, m, src))
    if sub_df is not None:
        vecs = build_month_vectors(sub_df, src == "MODIS", cid, cell_xy)
        if vecs:
            rec["v"] = vecs
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
