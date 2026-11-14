import json
from pathlib import Path

import numpy as np
import pandas as pd
import shapely
from shapely.geometry import shape
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "firms_borneo"
GB = ROOT / "data" / "geoboundaries"
OUT = ROOT / "output" / "borneo"
COLS = ["latitude", "longitude", "acq_date", "confidence", "type"]
YEARS = range(2012, 2026)
UNITS = {
    "IDN": ["West Kalimantan", "Central Kalimantan", "South Kalimantan", "East Kalimantan", "North Kalimantan"],
    "MYS": ["Sarawak", "Sabah", "Labuan"],
    "BRN": None,
}
TAUS = [0, 10, 30, 100, 300, 1000, 3000, 10000, 30000, 1e9]


def load_units():
    units = {}
    for iso, names in UNITS.items():
        feats = json.loads((GB / f"{iso}.geojson").read_text(encoding="utf-8"))["features"]
        geoms = {f["properties"]["shapeName"]: shape(f["geometry"]).buffer(0) for f in feats}
        if names is None:
            units["Brunei"] = unary_union(list(geoms.values()))
        else:
            for n in names:
                units[n] = geoms[n]
    units["Sabah"] = unary_union([units.pop("Sabah"), units.pop("Labuan")])
    return units


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
    return df[df.acq_date.dt.year.isin(YEARS)]


def assign(df, units):
    df = df.copy()
    df["unit"] = None
    x, y = df.longitude.values, df.latitude.values
    for name, geom in units.items():
        hit = shapely.contains_xy(geom, x, y) & df.unit.isna().values
        df.loc[hit, "unit"] = name
    df = df.dropna(subset=["unit"])
    return df.groupby([df.unit, df.acq_date.dt.year.rename("year"), df.acq_date.dt.month.rename("month")]).size()


def table(units):
    m = assign(load_sensor("M-C61"), units).rename("modis")
    v = assign(load_sensor("SV-C2"), units).rename("snpp")
    idx = pd.MultiIndex.from_product([list(units), YEARS, range(1, 13)], names=["unit", "year", "month"])
    return pd.concat([m, v], axis=1).reindex(idx).fillna(0).reset_index()


def factors(t):
    u = t.groupby(["unit", "month"])[["modis", "snpp"]].sum()
    b = t.groupby("month")[["modis", "snpp"]].sum()
    ku = (u.snpp / u.modis.replace(0, np.nan)).rename("k_unit")
    kb = (b.snpp / b.modis).rename("k_borneo")
    return u.modis.rename("n"), ku, kb


def predict(train, test, tau):
    n, ku, kb = factors(train)
    f = pd.concat([n, ku], axis=1).reset_index().merge(kb.reset_index(), on="month")
    f["k_unit"] = f.k_unit.fillna(f.k_borneo)
    w = f.n / (f.n + tau) if tau > 0 else (f.n > 0).astype(float)
    f["k_shrunk"] = w * f.k_unit + (1 - w) * f.k_borneo
    tr = train.merge(kb.reset_index(), on="month")
    r = (tr.groupby("unit").snpp.sum() / (tr.k_borneo * tr.modis).groupby(tr.unit).sum()).rename("r")
    f = f.merge(r.reset_index(), on="unit")
    f["k_scaled"] = f.k_borneo * f.r
    d = test.merge(f, on=["unit", "month"])
    for c in ("k_borneo", "k_unit", "k_shrunk", "k_scaled"):
        d["p_" + c[2:]] = d[c] * d.modis
    return d


def cv(t, tau):
    return pd.concat([predict(t[t.year != y], t[t.year == y], tau) for y in YEARS], ignore_index=True)


def scores(d, by=None):
    rows = []
    groups = d.groupby(by) if by else [("ALL", d)]
    for key, g in groups:
        ann = g.groupby(["unit", "year"])[["snpp", "p_borneo", "p_unit", "p_shrunk", "p_scaled"]].sum()
        r = {"unit": key}
        for m in ("borneo", "unit", "shrunk", "scaled"):
            r[f"ann_wape_{m}"] = (ann["p_" + m] - ann.snpp).abs().sum() / ann.snpp.sum()
            r[f"mon_wape_{m}"] = (g["p_" + m] - g.snpp).abs().sum() / g.snpp.sum()
        rows.append(r)
    return pd.DataFrame(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t = table(load_units())
    t.to_csv(OUT / "k_regional_unit_month_counts.csv", index=False)
    n, ku, kb = factors(t)
    k = pd.concat([n, ku], axis=1).reset_index().pivot(index="month", columns="unit")
    k_tab = k["k_unit"].round(2)
    k_tab["Borneo"] = kb.round(2)
    k_tab.to_csv(OUT / "k_regional_factors.csv")
    k["n"].astype(int).to_csv(OUT / "k_regional_modis_counts.csv")
    print(k_tab.to_string())
    print(k["n"].astype(int).to_string())
    print(t.groupby("unit")[["modis", "snpp"]].sum().assign(k=lambda x: (x.snpp / x.modis).round(2)).to_string())
    tau_rows = []
    for tau in TAUS:
        s = scores(cv(t, tau)).iloc[0]
        tau_rows.append({"tau": tau, "ann": s.ann_wape_shrunk, "mon": s.mon_wape_shrunk})
    tr = pd.DataFrame(tau_rows)
    print(tr.to_string())
    tr.to_csv(OUT / "k_regional_tau_cv.csv", index=False)
    best = tr.loc[tr.mon.idxmin(), "tau"]
    nested = []
    for y in YEARS:
        inner = t[t.year != y]
        errs = []
        for tau in TAUS:
            d = pd.concat([predict(inner[inner.year != z], inner[inner.year == z], tau) for z in YEARS if z != y])
            errs.append((d.p_shrunk - d.snpp).abs().sum())
        nested.append(predict(inner, t[t.year == y], TAUS[int(np.argmin(errs))]).assign(tau=TAUS[int(np.argmin(errs))]))
    nd = pd.concat(nested, ignore_index=True)
    print("nested taus", sorted(nd.groupby("year").tau.first().tolist()))
    res = pd.concat([scores(nd), scores(nd, "unit")]).round(3)
    d_best = cv(t, best)
    res_best = pd.concat([scores(d_best), scores(d_best, "unit")]).round(3)
    res.to_csv(OUT / "k_regional_cv_nested.csv", index=False)
    res_best.to_csv(OUT / "k_regional_cv_besttau.csv", index=False)
    print("best tau", best)
    print(res.to_string())
    print(res_best.to_string())


if __name__ == "__main__":
    main()
