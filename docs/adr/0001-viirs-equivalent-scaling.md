# Harmonize to VIIRS-equivalent counts by Overlap Period scaling

MODIS (1 km, from 2002) and VIIRS (375 m, from 2012) count Hotspots differently, so their records cannot be compared directly. We express every Harmonized Hotspot Count as the count VIIRS would have recorded: over the Overlap Period we fit one scaling factor per calendar month between the two sensors and apply it to the MODIS-only years, and we report its error on held-out years. VIIRS is the current and future sensor, so recent years stay as observed.

The factors are fitted once on the whole Coverage Area and applied to every Area of Interest, however small. Between-year swings in the factor (3.8 in 2024 to 5.4 in 2025) are larger than the spread between provinces and states (3.99 Sarawak to 5.40 South Kalimantan), so regional factors buy almost nothing ([k-regional-analysis.md](../research/k-regional-analysis.md)).

## Considered Options

- **Factors per province or state**: 10.6% annual error against 11.3% for Borneo-wide, but off-season factors swing between 2.9 and 11.75 on a few dozen MODIS Hotspots, and Brunei has too few to fit at all.
- **Regional factors shrunk toward the Borneo factor**: lost to Borneo-wide under nested cross-validation (11.7%). A later refinement worth keeping in mind: one constant multiplier per province on top of the Borneo factors, which mainly helps South Kalimantan and Sarawak.

- **Detection-probability model** from same-overpass Aqua × S-NPP pairs: more faithful, but too much work for the hackathon deadline (Sun 15 Nov 2026, 9pm). A candidate upgrade later.
- **No conversion, sensors side by side**: rejected because the challenge asks for one harmonized record.
- **MODIS-equivalent counts**: rejected because it would degrade the more detailed recent VIIRS years.
