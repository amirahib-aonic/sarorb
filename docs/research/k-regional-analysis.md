# Regional vs Borneo-wide k(m)

Question: should the monthly MODIS-to-VIIRS factor k(m) = sum S-NPP / sum MODIS (2012-2025) be one Borneo-wide set, one per ADM1 unit, or a compromise?

**Recommendation: keep one Borneo-wide k(m).** Per-unit and shrunk factors improve leave-one-year-out error by under 1 percentage point overall, and the shrinkage method with tau picked inside the CV loop does slightly worse than Borneo-wide. This gain is much smaller than the year-to-year spread in k. Optional refinement: multiply the Borneo k(m) by one per-unit scalar ("scaled" below) for Sarawak (about 0.85x) and South Kalimantan (about 1.1x), where annual error drops noticeably. Do not fit per-unit monthly factors.

## Literature

| Source | Relevant finding |
|---|---|
| Schroeder et al. 2014, RSE 143:85-96, [PDF](https://earthdata.nasa.gov/s3fs-public/imported/Schroeder_et_al_2014b_RSE.pdf) | VIIRS 375 m detects much smaller fires than MODIS 1 km, so the VIIRS/MODIS ratio depends on the fire-size mix. More small fires give a higher ratio. |
| Giglio et al. 2016, RSE 178:31-41, [PDF](https://www.earthdata.nasa.gov/s3fs-public/imported/Giglio2016_C6_Fire.pdf) | MODIS C6 detection probability varies by region, mainly because fire sizes differ by region. C6 also changed false alarms in the tropics. |
| Sofiev & Kouznetsov, GMD 19:10123 (2026), [link](https://gmd.copernicus.org/articles/19/10123/2026/) | Global detection-probability maps: about 78% for MODIS and 88% for VIIRS on strong fires, but below 30% (MODIS) and 40% (VIIRS) in parts of the equatorial belt. |
| Boschetti, Roy, Giglio, MODIS/VIIRS harmonization (MODIS ST 2022/2023), [slides](https://modis.gsfc.nasa.gov/sci_team/meetings/202305/presentations/boschetti.pdf) | The planned 0.25 deg MODIS-VIIRS calibration uses adjustments by region, land cover and tree cover. The slides are preliminary. |
| GFED5 / NRT extension, [ESSD 2023](https://essd.copernicus.org/articles/15/5227/2023/essd-15-5227-2023.pdf) | Converts VIIRS counts with region- and biome-specific factors, so the ratio is treated as varying by biome. |

Physically, the literature expects the ratio to vary with fire size and land cover, for example small agricultural fires versus large peat or forest fires. Global and continental work therefore regionalizes. None of the sources gives Borneo- or peat-specific MODIS:VIIRS count ratios. Note that GFED and Sofiev work at biome or continental scale, not province scale.

## Data and method

- Raw FIRMS archive plus NRT data for Borneo, 2012-2025. MODIS C6.1 hotspots need confidence >= 30. S-NPP hotspots exclude confidence "l". Only type 0 (vegetation fire) is kept. These filters match `burning_calendar.py`.
- Each hotspot is assigned to an ADM1 unit from the simplified geoBoundaries polygons (IDN, MYS, BRN; commit 9469f09). The units are the five Kalimantan provinces, Sarawak, Sabah (with Labuan), and Brunei (four districts merged).
- Leave-one-year-out CV over 14 years. Each method predicts S-NPP counts as k x MODIS for every unit-month of the held-out year. The error is WAPE = sum|pred - obs| / sum obs, computed on annual unit totals and on unit-months.
- Methods:
  - borneo: Borneo k(m).
  - unit: unit k(m).
  - shrunk: w·k_unit + (1-w)·k_borneo, with w = n/(n+tau) and n the unit-month MODIS count in the training years.
  - scaled: k_borneo(m) x r_unit, where r_unit is the unit's overall S-NPP / predicted ratio.
- Tau was chosen on the CV grid {0 ... 30000, inf}. It was also chosen inside a nested CV, which gives an honest error estimate.
- Script: `docs/research/scripts/k_regional.py`. Outputs: `docs/research/output/borneo/k_regional_*.csv`.

## Factors

All-year k (sum S-NPP / sum MODIS): Borneo-wide about 4.8. By unit, Sarawak 3.99, West Kalimantan 4.27, North Kalimantan 4.41, East Kalimantan 4.68, Sabah 5.02, Central Kalimantan 5.06, South Kalimantan 5.40, and Brunei 6.83 (from only 316 MODIS hotspots).

| Month | Borneo | Unit range (excluding Brunei) | Brunei |
|---|---|---|---|
| 1 | 5.08 | 3.99-5.66 | 7.88 |
| 3 | 5.13 | 3.92-9.44 | 6.92 |
| 4 | 4.81 | 3.82-11.75 | 7.59 |
| 6 | 4.36 | 2.86-6.22 | 9.19 |
| 8 | 4.46 | 4.26-5.38 | 7.06 |
| 9 | 4.55 | 4.09-4.93 | 9.82 |
| 10 | 5.55 | 3.81-5.97 | 4.29 |
| 12 | 5.00 | 3.21-7.62 | 7.67 |

During the Aug-Oct peak, when counts are in the tens of thousands, units fall within about ±15% of the Borneo k. The wide spreads, such as South Kalimantan at 9-12 in Mar-Apr, come from cells with 50-200 MODIS hotspots over 14 years.

There is more variation between years than between units. The Borneo annual k ranges from 3.8 (2024) to 5.4 (2025).

## Cross-validated error (WAPE)

The overall rows use the nested tau. The per-unit rows below also come from the nested run.

| Unit | Annual: Borneo | Annual: unit | Annual: shrunk | Annual: scaled | Monthly: Borneo | Monthly: unit | Monthly: shrunk | Monthly: scaled |
|---|---|---|---|---|---|---|---|---|
| **All** | 11.3% | 10.6% | 11.7% | 10.9% | 16.2% | 15.9% | 16.3% | 15.6% |
| Central Kal. | 12.4 | 14.0 | 14.7 | 13.9 | 14.4 | 15.8 | 16.0 | 15.4 |
| East Kal. | 7.1 | 6.2 | 6.1 | 8.0 | 14.3 | 12.2 | 12.9 | 14.4 |
| North Kal. | 11.5 | 12.9 | 12.2 | 11.2 | 27.4 | 28.1 | 26.9 | 26.7 |
| South Kal. | 11.1 | 4.4 | 7.4 | 5.0 | 14.2 | 12.1 | 13.9 | 12.0 |
| West Kal. | 11.1 | 10.1 | 11.4 | 10.2 | 17.5 | 16.4 | 16.7 | 15.2 |
| Sarawak | 14.6 | 10.7 | 14.4 | 10.9 | 22.9 | 19.3 | 22.1 | 20.0 |
| Sabah | 9.9 | 8.4 | 9.1 | 8.5 | 22.6 | 23.3 | 22.0 | 23.2 |
| Brunei | 34.7 | 35.6 | 34.3 | 30.0 | 56.7 | 74.9 | 56.6 | 65.6 |

Tau sweep (non-nested, optimistic): the best monthly result was tau = 300 at 15.7%, and the best annual result was tau = 30 at 10.6%. Tau = inf (Borneo) gives 11.3% / 16.2%. The curve is flat. In the nested CV, the selected tau varied between folds, and shrinkage lost to Borneo-wide (11.7% vs 11.3%).

## Conclusion

- The compromise does not beat Borneo-wide by a meaningful margin. The best case is about 0.5-0.7 pp of overall WAPE, and the honest nested estimate is a loss. Central Kalimantan, which has the most fire, gets worse with any regional factor.
- The residual error, about 11% annual and 16% monthly, comes from year-to-year changes in the fire-size mix, not from geography. This fits Schroeder 2014 and Giglio 2016: the ratio depends on fire size, and in Borneo fire size changes with El Nino and drought years more than with province.
- If IGNIS ever shows provincial VIIRS-equivalent totals for Sarawak or South Kalimantan, use the "scaled" variant with one scalar per unit, not per-unit monthly factors. Monthly factors are too noisy outside the Aug-Oct peak. Brunei is too sparse for any regional factor.
- Report about ±11% (annual) and ±16% (monthly) as the uncertainty on VIIRS-equivalent counts derived from MODIS (ADR 0001).
