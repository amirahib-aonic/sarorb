import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
s = (ROOT / "prototypes" / "borneo.PROTOTYPE.data.js").read_text(encoding="utf-8")
d = json.loads(s[s.index("=") + 1:].rstrip().rstrip(";"))
cells = np.array(d["cells"])
n = len(cells)
years = list(range(2002, 2026))
X = np.zeros((len(years), 12, n))
for key, rec in d["months"].items():
    y, m = map(int, key.split("-"))
    if y in years:
        for c, v in rec["c"]:
            X[years.index(y), m - 1, c] = v * rec["w"]

gx, gy = cells[:, 0], cells[:, 1]


def regrid(X, f):
    keys = np.floor(gx / f).astype(int) * 100000 + np.floor(gy / f).astype(int)
    u, inv = np.unique(keys, return_inverse=True)
    out = np.zeros((X.shape[0] * 12, len(u)))
    np.add.at(out.T, inv, X.reshape(-1, n).T)
    return out.reshape(X.shape[0], 12, len(u))


def smooth(X, r):
    idx = {(a, b): i for i, (a, b) in enumerate(cells)}
    nb = [[idx[(a + dx, b + dy)] for dx in range(-r, r + 1) for dy in range(-r, r + 1) if (a + dx, b + dy) in idx] for a, b in cells]
    out = np.zeros_like(X)
    for i, js in enumerate(nb):
        out[:, :, i] = X[:, :, js].sum(axis=2)
    return out


def stats(Z, label):
    Y = Z.shape[0]
    med_nz, ratio_flag, newfire, freq25, freq50, rank_flag, eb_flag, z_flag, active = [], [], [], [], [], [], [], [], []
    for t in range(Y):
        o = np.delete(Z, t, axis=0)
        cur = Z[t]
        med = np.median(o, axis=0)
        mean = o.mean(axis=0)
        freq = (o > 0).mean(axis=0)
        act = cur > 0
        active.append(act.sum())
        med_nz.append((med > 0).mean())
        newfire.append(((med == 0) & act).sum() / max(act.sum(), 1))
        ratio_flag.append((((med == 0) & act) | ((med > 0) & (cur >= 2 * med))).sum() / max(act.sum(), 1))
        freq25.append((freq >= 0.25).mean())
        freq50.append((freq >= 0.5).mean())
        pr = ((o < cur).sum(axis=0) + 0.5 * (o == cur).sum(axis=0)) / o.shape[0]
        rank_flag.append(((pr >= 0.9) & act).sum() / max(act.sum(), 1))
        lo = np.log1p(o)
        sd = lo.std(axis=0)
        zz = np.where(sd > 0, (np.log1p(cur) - lo.mean(axis=0)) / np.where(sd > 0, sd, 1), 0)
        z_flag.append(((zz >= 2) & act).sum() / max(act.sum(), 1))
        prior = mean.mean(axis=1, keepdims=True)
        eb = (cur + prior) / (mean + prior)
        eb_flag.append(((eb >= 2) & act).sum() / max(act.sum(), 1))
    f = lambda v: f"{100*np.mean(v):.1f}%"
    return dict(label=label, cells=Z.shape[2], active_cell_months=int(np.sum(active)),
                median_nonzero=f(med_nz), new_fire_share=f(newfire), ratio_flag=f(ratio_flag),
                freq25=f(freq25), freq50=f(freq50), rank90_flag=f(rank_flag),
                logz2_flag=f(z_flag), eb2_flag=f(eb_flag))


def stability(Z):
    rs = []
    Y = Z.shape[0]
    for t in range(Y):
        o = np.delete(Z, t, axis=0)
        cur = Z[t]
        for drop in range(o.shape[0]):
            if drop % 6:
                continue
            o2 = np.delete(o, drop, axis=0)
            a = cur >= 2 * np.median(o, axis=0)
            b = cur >= 2 * np.median(o2, axis=0)
            m = cur > 0
            if m.sum():
                rs.append((a[m] != b[m]).mean())
    return f"{100*np.mean(rs):.1f}%"


def monthly_median_nz(Z):
    return [f"{100*(np.median(Z[:, m], axis=0) > 0).mean():.1f}" for m in range(12)]


variants = {"0.1": X, "0.1 3x3": smooth(X, 1), "0.1 5x5": smooth(X, 2), "0.2": regrid(X, 2), "0.25": regrid(X, 2.5), "0.5": regrid(X, 5), "1.0": regrid(X, 10)}
for k in ["0.1", "0.1 3x3", "0.1 5x5", "0.2", "0.25", "0.5", "1.0"]:
    Z = variants[k]
    r = stats(Z, k)
    r["flip_dropping_one_baseline_year"] = stability(Z)
    r["median_nonzero_by_month"] = monthly_median_nz(Z)
    print(json.dumps(r))
