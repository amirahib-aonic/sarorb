# MODIS–VIIRS harmonization analysis

How IGNIS turns MODIS and VIIRS Hotspot counts into one Harmonized Hotspot Count, and how accurate that is. Decision record: [ADR 0001](../adr/0001-viirs-equivalent-scaling.md). Terms follow [GLOSSARY.md](../../GLOSSARY.md).

## Summary

- Over the Overlap Period, VIIRS S-NPP records **4.2× as many Hotspots as MODIS** in West Kalimantan, and the two move together closely (Pearson r = 0.978 on log monthly counts).
- Four candidate scaling methods all predict a held-out year's VIIRS total within **about 12–13% on average (median 7–10%)**. The differences between methods are small.
- **Recommendation for the hackathon:** one scaling factor per calendar month, fitted over the Overlap Period. It has the best median annual error (7.1%), stays explainable in one sentence, and keeps the seasonal shape that the Burning Calendar depends on.
- VIIRS S-NPP and NOAA-20 agree almost exactly (NOAA-20 / S-NPP = 1.01, r = 0.987), so they can be treated as one VIIRS record.
- The worst year is 2020 (around 40% under-prediction for every method), a very low-fire year in which MODIS missed relatively more small fires.

## The harmonization formula

The settled rule. The direction is **VIIRS = k × MODIS**: MODIS counts are scaled up to what VIIRS would have recorded, never the other way round.

### Harmonized Hotspot Count

For an Area of Interest, year *y* and calendar month *m*:

```
         ┌ S(y,m)                     if VIIRS S-NPP observed that month
H(y,m) = ┤ N(y,m) / r                 else if only VIIRS NOAA-20 observed it
         └ k(m) × M(y,m)              else (MODIS only, 2002–2011)
```

| Symbol | Meaning |
|---|---|
| H(y,m) | Harmonized Hotspot Count, in VIIRS-equivalent Hotspots |
| M(y,m) | MODIS Hotspots (Terra + Aqua) observed in that month |
| S(y,m) | VIIRS S-NPP Hotspots observed in that month |
| N(y,m) | VIIRS NOAA-20 Hotspots observed in that month |
| k(m) | MODIS-to-VIIRS scaling factor for calendar month *m* |
| r | NOAA-20 to S-NPP ratio, 1.01 |

### Fitting k(m)

Each factor is the ratio of total VIIRS S-NPP Hotspots to total MODIS Hotspots in that calendar month, summed over every year of the Overlap Period:

```
k(m) = Σ S(y,m) / Σ M(y,m)      summed over y = 2012 … 2026
```

Using totals rather than an average of monthly ratios stops near-empty months (for example 2 MODIS against 15 VIIRS Hotspots) from swinging the factor.

Fitted values for West Kalimantan:

| m | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| k(m) | 4.87 | 5.15 | 5.37 | 5.12 | 4.01 | 4.01 | 3.65 | 4.20 | 4.15 | 4.72 | 4.41 | 5.68 |

The single all-year factor, used as a fallback when a month has too few Overlap Period Hotspots to fit its own k(m), is:

```
k = Σ S / Σ M = 4.21
```

### Uncertainty

Harmonized months (the k(m) × M branch) carry an uncertainty of **±12%** on annual totals, the leave-one-year-out average error. Observed VIIRS months carry none from harmonization.

### Worked example

August 2006, MODIS only: M = 10,000 Hotspots (illustrative).

```
H = k(Aug) × M = 4.20 × 10,000 = 42,000 VIIRS-equivalent Hotspots (±12%)
```

August 2019, S-NPP observed: H = S(2019, Aug) as recorded, no scaling.

## Why harmonization is needed

| | MODIS (Terra + Aqua) | VIIRS (S-NPP, NOAA-20) |
|---|---|---|
| Product | FIRMS MCD14 Collection 6.1 | FIRMS VNP14IMG / VJ114IMG, 375 m |
| Pixel size at nadir | 1 km | 375 m |
| Record starts | 2000 (Terra), 2002 (Aqua) | Jan 2012 (S-NPP), Apr 2018 (NOAA-20) |
| Typical effect | Misses small and short-lived fires | Detects many more, smaller fires |

A raw count from one sensor is not comparable with a raw count from the other. A year-by-month grid that switches from MODIS to VIIRS in 2012 would show a fourfold jump in burning that never happened. The challenge asks for one consistent record, so every month must be expressed in a common unit. We chose **VIIRS-equivalent counts** (ADR 0001): VIIRS is the current and future sensor, so recent years stay as observed and only the MODIS-only years (2002–2011) are converted.

## Data

- Source: `docs/research/output/west_kalimantan/monthly_by_sensor.csv`, monthly Hotspot counts per sensor for West Kalimantan, produced by `docs/research/scripts/burning_calendar.py` from NASA FIRMS archive and NRT downloads (request IDs 843314–843316).
- Coverage: MODIS Feb 2002 – Nov 2026; VIIRS S-NPP Jan 2012 – Nov 2026; VIIRS NOAA-20 Apr 2018 – Nov 2026.
- Months with no rows inside a sensor's active span are counted as zero Hotspots.
- **Overlap Period used for fitting:** Jan 2012 – Nov 2026 (179 months). Validation uses only the 14 complete years, 2012–2025; 2026 is partial and partly near-real-time data.

## Overlap Period: how the sensors compare

Annual totals for West Kalimantan:

| Year | MODIS | VIIRS S-NPP | Ratio S-NPP / MODIS |
|---|---:|---:|---:|
| 2012 | 10,030 | 38,332 | 3.82 |
| 2013 | 6,058 | 26,071 | 4.30 |
| 2014 | 12,129 | 55,882 | 4.61 |
| 2015 | 13,055 | 55,442 | 4.25 |
| 2016 | 3,588 | 16,036 | 4.47 |
| 2017 | 2,029 | 8,948 | 4.41 |
| 2018 | 6,757 | 29,817 | 4.41 |
| 2019 | 10,503 | 41,434 | 3.94 |
| 2020 | 1,326 | 9,690 | **7.31** |
| 2021 | 2,337 | 10,915 | 4.67 |
| 2022 | 1,786 | 8,541 | 4.78 |
| 2023 | 7,155 | 25,228 | 3.53 |
| 2024 | 4,325 | 14,736 | 3.41 |
| 2025 | 3,778 | 21,198 | 5.61 |
| 2026 (to Nov) | 20,179 | 79,386 | 3.93 |

Overall S-NPP / MODIS ratio: **4.21**.

What the table shows:

1. **The ratio is stable in big fire years** (3.5–4.6 in 2012–2015, 2019, 2023, 2026). Large fires are seen by both sensors.
2. **The ratio rises in quiet years** (7.3 in 2020, 5.6 in 2025). When burning is light, a larger share of fires are small, and MODIS misses them. A single constant therefore under-predicts quiet years.
3. **No steady drift over time.** Late-period ratios do not climb in a straight line, so there is no strong sign yet of the Terra and Aqua orbit drift (both satellites began drifting to later overpass times around 2020–2022) distorting MODIS. This should be rechecked when the Borneo data arrives.

Ratio by calendar month (all overlap years pooled):

| Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4.87 | 5.15 | 5.37 | 5.12 | 4.01 | 4.01 | 3.65 | 4.20 | 4.15 | 4.72 | 4.41 | 5.68 |

The ratio is lowest at the start of the dry season (Jul) and highest in the wet months, the same "small fires favour VIIRS" pattern seen across years.

## Methods compared

Each method predicts the VIIRS S-NPP monthly count from the MODIS monthly count.

| Method | Formula | Fitted on full Overlap Period |
|---|---|---|
| **Global ratio** | VIIRS = k × MODIS | k = 4.21 |
| **Per-month ratio** | VIIRS = k(month) × MODIS | twelve factors, table above |
| **Dry/wet ratio** | VIIRS = k(season) × MODIS, dry = Jul–Oct | k(dry) = 4.15, k(wet) = 4.75 |
| **Log-log regression** | log(1+VIIRS) = a + b·log(1+MODIS) | a = 1.664, b = 0.967 |

A slope below 1 in the log-log model (b = 0.967) says the same thing as the quiet-year finding: the MODIS-to-VIIRS multiplier shrinks slightly as burning grows.

## Validation: leave one year out

For each complete year from 2012 to 2025, every method is fitted on the other 13 years and then predicts that year's twelve VIIRS monthly counts from MODIS alone. This is the honest test of how well a 2005 MODIS month would be converted, since that year was never seen during fitting.

| Method | Monthly MAE | Monthly median abs. error | Log RMSE | Annual MAPE | Annual median APE | Worst year |
|---|---:|---:|---:|---:|---:|---|
| Global ratio | 317 | 44 | 0.449 | 13.2% | 10.0% | 2020, 43% |
| **Per-month ratio** | 328 | 46 | 0.438 | 12.4% | **7.1%** | 2020, 41% |
| Dry/wet ratio | 304 | 46 | 0.437 | 12.8% | 7.9% | 2020, 43% |
| Log-log regression | **295** | 52 | **0.412** | **12.1%** | 8.4% | 2020, 40% |

Monthly MAE is dominated by peak months (August and September can hold more than 20,000 Hotspots), so the annual percentage errors are the more useful figures for the pitch.

**Reading the result:** all four methods sit within about one percentage point of each other on annual error. The data supports a simple multiplier; extra complexity buys little. The remaining error is year-to-year variation in fire size that no MODIS-only method can recover.

## Recommendation

**Use the per-month ratio for the hackathon build.**

- It has the best typical (median) annual error, 7.1%.
- It is a 12-number lookup table that anyone on the team can explain to judges in one sentence.
- It preserves the seasonal pattern, which matters directly for the Typical Year and Burning Phase labels.
- The log-log model is marginally better on average error but harder to explain and adds non-linear behaviour near zero.

Pitch line: *"We calibrated MODIS against VIIRS over 14 overlapping years. Tested on years the model never saw, harmonized MODIS predicts the annual VIIRS total within 7% in a typical year and 12% on average."*

### Effect on the MODIS-only years

Applying the per-month factors to 2002–2011 gives VIIRS-equivalent annual totals for West Kalimantan:

| Year | MODIS observed | Harmonized (VIIRS-equivalent) |
|---|---:|---:|
| 2002 | 17,472 | 72,942 |
| 2003 | 7,637 | 31,749 |
| 2004 | 13,378 | 56,369 |
| 2005 | 5,887 | 24,868 |
| 2006 | 18,458 | 78,716 |
| 2007 | 5,250 | 22,517 |
| 2008 | 5,166 | 21,672 |
| 2009 | 16,615 | 68,428 |
| 2010 | 2,238 | 9,822 |
| 2011 | 7,826 | 32,710 |

2002 and 2006 come out comparable to 2026, the largest year since VIIRS began, which matches their reputation as severe El Niño haze years.

### Combining sensors once harmonized

- **2002–2011:** harmonized MODIS (the only record).
- **2012 onward:** VIIRS S-NPP as observed.
- **NOAA-20:** NOAA-20 / S-NPP = 1.01 with r = 0.987 over 104 shared months. Use it to fill gaps in S-NPP, not to add to it, because both satellites see the same fires and adding them would double count.
- Show an uncertainty band of ±12% on harmonized years in the Burning Calendar, labelled as an estimate, so users can tell converted months from observed ones.

## Limitations and open questions

1. **One region only.** Every factor here is fitted on West Kalimantan. The Coverage Area is now all of Borneo, and the ratio may differ in Sarawak and Sabah, where land use and fire size differ. Refit when the Borneo data arrives and check whether one Borneo-wide table is enough or whether factors are needed per region.
2. **Quiet years are under-predicted.** In low-fire years (2020, 2025) every method under-predicts by 25–43%. A model with a fire-size or burning-level term could fix this, but it is out of scope for the deadline.
3. **Confidence filtering.** Counts depend on which detections `burning_calendar.py` kept (for example, low-confidence VIIRS or MODIS detections below a cut-off). The factors are only valid for the same filter, so the filter must stay fixed between fitting and the app.
4. **Terra and Aqua orbit drift.** Both MODIS satellites drift to later overpass times from roughly 2020 onward, which can change what they detect. Not visible yet in this data; worth rechecking.
5. **Pixels are not fires.** Both sensors count Hotspots (pixels), not separate fires. One large fire produces many more VIIRS Hotspots than MODIS ones, which is part of what the ratio captures.
6. **2026 is partial.** It is included in fitting but excluded from validation, and part of it is near-real-time data that FIRMS later replaces with archive data.
7. **Upgrade path.** The detection-probability model from same-overpass Aqua × S-NPP pairs (rejected for now in ADR 0001) remains the way to remove limits 2 and 5.

## Reproducing

```bash
python docs/research/scripts/harmonization_analysis.py docs/research/output/west_kalimantan/monthly_by_sensor.csv
```

The script pivots the counts to one row per month, fits the four methods, runs the leave-one-year-out test and prints every figure in this document. In the app pipeline it becomes a harmonization step that writes the twelve per-month factors to a small JSON file.
