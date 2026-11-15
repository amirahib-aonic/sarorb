# Challenge objectives

Source: NASA Space Apps 2026, "MODIS and VIIRS Hot Spots", https://www.spaceappschallenge.org/2026/challenges/modis-and-viirs-hot-spots/ (retrieved 2026-11-14), plus the Sarawak Space Challenge submission briefing of 13 Nov 2026.

`scripts/check-objectives.sh` reads this file. Each line under a level heading is one objective:

```
- [ ] ID: text | evidence: path/one, path/two
```

Tick `[x]` only once every listed evidence path exists. The script fails if a ticked item's evidence is missing, or if any **Must** item is still unticked when run with `--strict` (the pre-submission gate).

## Must

- [x] O1-HARMONIZE: MODIS and VIIRS hotspots are harmonized so the sensor of origin no longer matters | evidence: docs/adr/0001-viirs-equivalent-scaling.md, docs/research/k-regional-analysis.md, docs/research/prototypes/build_borneo_prototype_data.py
- [x] O2-WEBAPP: A web application takes the harmonized hotspot data as input | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] O3-REGION: The user can select a region | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] O4-DATERANGE: The user can select a date range | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] O5-CALENDAR: A burning calendar shows hotspot counts from the early 2000s to the present | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] O6-DOWNLOAD: Analytics and visualizations of fire activity can be downloaded | evidence: docs/research/prototypes/borneo.PROTOTYPE.html, docs/DEPLOYMENT.md
- [x] S1-NASA-DATA: At least one NASA resource from the challenge Resources tab is used and listed (FIRMS MODIS/VIIRS) | evidence: docs/research/RESOURCE.md
- [x] S2-DEPLOYED: A deployed link judges can use | evidence: docs/DEPLOYMENT.md
- [ ] S3-VIDEO: A ~30 s demo video on YouTube, no under-18s on camera | evidence:
- [ ] S4-AI-USE: Use of superintelligence (SI) is described, SI images labelled | evidence:
- [ ] S5-PLAIN-LANGUAGE: Non-technical judges can follow the app, video, summary and project details: jargon (MODIS, VIIRS, FRP, harmonization, anomaly) is replaced or explained in plain words on first use | evidence:

## Should

- [x] C1-COLOR-RAMP: Color ramps show differences in hotspot counts across months | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] C2-CSV: A CSV of hotspots detected in a search can be downloaded | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] C3-HISTORY: Seasonality, busiest years, and how a current fire compares with previous ones | evidence: docs/research/prototypes/borneo.PROTOTYPE.html, docs/adr/0002-map-anomaly-neighbourhood-shrinkage.md

## Could

- [x] P1-DRAW-AOI: Draw the area of interest on a map | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] P2-LATLON: Enter latitude and longitude | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] P3-ACCESSIBLE: Accessible color ramps | evidence: docs/research/prototypes/borneo.PROTOTYPE.html
- [x] P4-ANOMALY: Anomalies against multi-year averages | evidence: docs/research/prototypes/borneo.PROTOTYPE.html, docs/adr/0002-map-anomaly-neighbourhood-shrinkage.md
- [ ] P5-AUDIENCE: Fits early warning, emergency responders, scientists, land managers, firefighters | evidence:

## Prohibited

`scripts/check-objectives.sh` scans tracked files for these and fails on any hit.

- No NASA logo ("meatball"/"worm"), flags or mission identifiers, even modified.
