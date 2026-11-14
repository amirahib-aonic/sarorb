# Harmonize to VIIRS-equivalent counts by Overlap Period scaling

MODIS (1 km, from 2002) and VIIRS (375 m, from 2012) count Hotspots differently, so their records cannot be compared directly. We express every Harmonized Hotspot Count as the count VIIRS would have recorded: over the Overlap Period we fit a scaling factor between the two sensors and apply it to the MODIS-only years, and we report its error on held-out years. VIIRS is the current and future sensor, so recent years stay as observed.

## Considered Options

- **Detection-probability model** from same-overpass Aqua × S-NPP pairs: more faithful, but too much work for the hackathon deadline (Sun 15 Nov 2026, 9pm). A candidate upgrade later.
- **No conversion, sensors side by side**: rejected because the challenge asks for one harmonized record.
- **MODIS-equivalent counts**: rejected because it would degrade the more detailed recent VIIRS years.
