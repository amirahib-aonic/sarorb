# Per-cell Anomaly when most cells have a zero median

Script: `docs/research/scripts/cell_anomaly.py` (reads `prototypes/borneo.PROTOTYPE.data.js`, Harmonized Hotspot Count = raw count × w, 2002–2025, leave-one-year-out baseline per calendar month).

## Summary

- On the 0.1° grid the median of the same calendar month in other years is **non-zero for only 7.2% of cells** (averaged over months; 0.0–0.9% in Nov–Jun, 31–38% in Aug–Sep). So **63% of all burning cell-months get "new fire"** and **83% of burning cell-months are flagged** by "≥2× median or median = 0". That is the red map.
- No tool or paper found shows a per-pixel ratio to a median for active-fire counts. The published tools compare **areas** (admin units, regions) against a mean ± SD band (GFW), or show **counts/density on a coarse grid** (Giglio CMG climatology at 0.5°), and the burned-area/emissions products handle sparse small fires by **pooling to coarse cells and statistical scaling** (GFED4s/GFED5), not by per-cell ratios.
- The standard statistical fix for ratios on sparse counts is **shrinkage** (empirical Bayes, Clayton & Kaldor 1987; BYM 1991): add a prior pseudo-count so a cell with no history is pulled toward the regional rate.

**Recommendation.** Keep the area-wide Anomaly as the headline. For the map:
1. Compute the cell Anomaly on a **0.1° cell with 5×5 neighbourhood sums (≈0.5° window, still drawn at 0.1°)**, and
2. Express it as a **shrunk ratio** `(x + μ̄) / (m + μ̄)` where `m` is the cell's mean for that calendar month in other years and `μ̄` is the Borneo-wide per-cell mean for that month (empirical-Bayes-style pseudo-count), flag at ≥2.
3. Draw cells with no history in a neutral "fire where none is usual" style, not red, and say so in the legend.

Combined, this drops the flagged share of burning cells from **83% to ~11%**, keeps the 0.1° display, costs one 5×5 box sum and one division (precomputable in the build script), and is as stable as the current method (≈2.5% of burning cells change flag when one baseline year is dropped).

## Numbers on Borneo (means over all 288 leave-one-year-out year-months)

Columns: share of cells with non-zero median; share of burning cells that are "new fire" (median 0); share of burning cells flagged by each rule: current ratio (≥2× median or median 0), percentile rank ≥0.9 among other years, z ≥ 2 on log(1+x), shrunk ratio ≥2; share of cells passing a burn-frequency mask (fire in ≥25% / ≥50% of other years, same month); share of burning cells whose current-ratio flag flips when one more baseline year is dropped.

| Grid | Cells | Median ≠ 0 | "New fire" | Ratio flag | Rank ≥0.9 | log z ≥2 | Shrunk ≥2 | Mask 25% | Mask 50% | Flip |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1° | 5394 | 7.2% | 63.1% | 83.1% | 42.9% | 26.2% | 37.2% | 18.8% | 7.2% | 1.6% |
| 0.1° + 3×3 sum | 5394 | 35.6% | 33.4% | 66.2% | 26.3% | 13.7% | 16.6% | 61.3% | 35.6% | 2.4% |
| 0.1° + 5×5 sum | 5394 | 59.2% | 18.7% | 55.5% | 20.6% | 8.5% | 11.2% | 81.3% | 59.2% | 2.6% |
| 0.2° | 1571 | 18.4% | 46.0% | 74.0% | 32.6% | 18.8% | 24.1% | 37.8% | 18.4% | 2.1% |
| 0.25° (approx., 2/3-cell blocks) | 1039 | 23.9% | 40.3% | 70.4% | 29.8% | 16.6% | 20.5% | 45.4% | 23.9% | 2.2% |
| 0.5° | 298 | 48.4% | 21.8% | 57.6% | 22.0% | 9.8% | 12.3% | 69.1% | 48.4% | 2.5% |
| 1.0° | 90 | 70.4% | 9.1% | 44.6% | 17.2% | 5.9% | 8.1% | 82.0% | 70.4% | 2.4% |

Median ≠ 0 by calendar month (Jan→Dec): 0.1°: 0.1, 0.5, 0.9, 0.6, 0.4, 0.7, 5.2, 30.9, 38.1, 15.6, 0.6, 0.0%. With 5×5 sums: 29, 40, 46, 49, 63, 70, 83, 95, 93, 82, 56, 26%. At 0.5°: 22, 31, 39, 40, 49, 57, 69, 84, 81, 68, 43, 20%.

Notes: the 50% mask equals "median ≠ 0" by construction. A truly uninformative rule would flag ~10% at rank 0.9; ties at zero push the rank rule well above that on sparse grids. The ratio rule is stable (flip ≤2.6%) but stable at the wrong answer: the instability lies in what it means, not in its sampling.

## Options compared

| Option | What it shows | Who uses it | Cost / complexity | Behaviour on Borneo |
|---|---|---|---|---|
| Plain ratio to median (current) | x / median, "new" when median 0 | Not found in any primary tool | Trivial | 7% of cells have a baseline; 83% of burning cells flagged |
| Area-level mean ± SD band | Is this area's count unusual this week/month | GFW fire alerts widget (weekly mean and SD of prior years, smoothed) [1][2] | Trivial; already in IGNIS | Works (already confirmed area-wide) |
| Coarser regrid (0.25°/0.5°/1°) | Ratio or count per big cell | Giglio MODIS CMG fire climatology at 0.5° [3]; GFED 0.25° [5] | Trivial; loses detail | 0.5°: 48% have baseline, 58% ratio-flagged, 298 cells |
| Neighbour smoothing (3×3 / 5×5 sum or kernel density) | Local fire activity around the cell, at 0.1° display | Kernel-density hotspot maps in fire-regime literature; GFED pools small fires spatially [4][5] | Low: one box filter at build time | 5×5: 59% baseline, 19% "new" |
| Burn-frequency mask (fire in ≥25/50% of years) | Ratio only where fire is usual; elsewhere "unusual location" | Fire-return / fire-frequency maps (concept); no tool found using it as an anomaly mask | Trivial | 0.1° keeps only 19% / 7% of cells; useless alone, OK with 5×5 (81% / 59%) |
| Percentile rank among other years | "Rank of this month in 23 years" | Climate-style percentile maps; not found for fire counts | Low | Zeros create ties; 43% flagged at 0.1°, 21% with 5×5 |
| z-score on log(1+x) | SDs above the cell's own history | Common in anomaly literature generally | Low | 26% at 0.1°; 8.5% with 5×5; SD = 0 for never-burned cells needs special-casing |
| Empirical-Bayes shrunk ratio (x+μ̄)/(m+μ̄) | Ratio pulled toward the regional rate when history is thin | Disease mapping SMR smoothing (Clayton & Kaldor; BYM) [6][7] | Low (one prior per month); full BYM/INLA is high | 37% at 0.1°; **11% with 5×5**; 12% at 0.5° |
| Probability-of-fire anomaly (fire yes/no vs historical frequency) | "Fire here this month happens in p% of years" | Fire-occurrence probability modelling (e.g. Indonesia fire–climate work [8]) | Low | Equivalent to the frequency mask; good tooltip text |

## Recommendation detail

- Build script: compute `S = 5×5 box sum` of harmonized counts per year-month; per calendar month `m = mean(S over other years)`, `μ̄ = mean(m over all cells)`; ship `A = (S_now + μ̄) / (m + μ̄)` and `p = share of other years with S > 0`.
- Map colour from `A` (diverging, centred on 1); tooltip shows raw count, `A`, and "fire in this area in p of 23 Augusts".
- Keep the 0.1° plain ratio out of the UI; leave "new fire" only for cells where `p = 0`, styled neutrally.
- A 0.5° regrid gives almost the same numbers (12% flagged) and is simpler, but changes the visual grid; use it if per-0.1° display is not needed.

## Citations

1. Global Forest Watch blog, "Tracking Wildfire Trends as Fire Seasons Heat Up": https://www.globalforestwatch.org/blog/data-and-tools/wildfire-trends-gfw-fire-data/ ; "Placing Global Wildfires into Local Context": https://www.globalforestwatch.org/blog/fires/placing-global-wildfires-into-local-context/
2. Vizzuality (GFW design partner), "The Amazon is on fire. Is it worse than normal?" (weekly mean and SD of prior years, smoothed): https://medium.com/vizzuality-blog/the-amazon-is-on-fire-is-it-worse-than-normal-5fa430a7880e . Dated 2019; current GFW method page not found.
3. Giglio, L., Csiszar, I., Justice, C. O. (2006), Global distribution and seasonality of active fires as observed with the Terra and Aqua MODIS sensors, JGR Biogeosciences 111, G02016: https://doi.org/10.1029/2005JG000142 (cited from prior knowledge, not re-fetched this run).
4. Randerson, J. T. et al. (2012), Global burned area and biomass burning emissions from small fires, JGR 117, G04012: https://doi.org/10.1029/2012JG002128 (not re-fetched).
5. Chen, Y. et al. (2023), Multi-decadal trends and variability in burned area from the fifth version of GFED (GFED5), ESSD 15, 5227: https://essd.copernicus.org/articles/15/5227/2023/ ; GFED site: https://globalfiredata.org/
6. Clayton, D., Kaldor, J. (1987), Empirical Bayes estimates of age-standardized relative risks for use in disease mapping, Biometrics 43, 671–681: https://doi.org/10.2307/2532003 (not re-fetched).
7. Besag, J., York, J., Mollié, A. (1991), Bayesian image restoration with two applications in spatial statistics, AISM 43, 1–20: https://doi.org/10.1007/BF00116466 (not re-fetched).
8. Field, R. D. et al. (2016), Indonesian fire activity and smoke pollution in 2015 show persistent nonlinear sensitivity to El Niño-induced drought, PNAS 113, 9204: https://doi.org/10.1073/pnas.1524888113 (not re-fetched).
9. GWIS active fire detection background (FIRMS-sourced; no per-cell anomaly method found): https://gwis.jrc.ec.europa.eu/about-gwis/technical-background/active-fire-detection

Gaps: no primary documentation found for an ASMC, FIRMS or GWIS per-cell count anomaly; ASMC bulletins report hotspot counts by country/region, not per-cell ratios (not verified this run).
