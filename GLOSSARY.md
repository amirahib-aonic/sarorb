# IGNIS

Integrated Geospatial Network for Ignition Surveillance: a web app that brings MODIS and VIIRS fire Hotspots into one consistent view, with a burning calendar (when) and a heatmap (where). Built by Sarawak Orbiters for NASA Space Apps 2026, "Harmonization of MODIS and VIIRS Hot Spots".

## Language

### Places

**Coverage Area**:
The island of Borneo (Kalimantan, Sarawak, Sabah and Brunei), the whole region IGNIS holds a Hotspot record for. Every Area of Interest lies inside it.
_Avoid_: Fire Area, study area, region

**Area of Interest**:
Any region a user selects to examine, either drawn on the map as a shape or picked from a preset: a province, state or country, or a district or division within one.
_Avoid_: AOI, selection, bounding box, study area

### Fire record

**Hotspot**:
A single satellite detection of active fire at a location and time, from either MODIS or VIIRS.
_Avoid_: Fire, fire point, detection

**Harmonized Hotspot Count**:
The monthly number of Hotspots in an Area of Interest, expressed as the count VIIRS would have recorded, whichever sensor actually observed it.
_Avoid_: Combined count, merged count, raw count

**Burning Calendar**:
The view of when burning happens in an Area of Interest: a Typical Year on top, and a year-by-month grid of Harmonized Hotspot Counts below for history and unusual years.
_Avoid_: Fire calendar, timeline

**Typical Year**:
The average Harmonized Hotspot Count for each calendar month in an Area of Interest, with each month given a Burning Phase.
_Avoid_: Seasonal profile, climatology

**Burning Phase**:
How much of a Typical Year's burning falls in one month: Peak burning, Active burning, Moderate or Low.
_Avoid_: Season, intensity level, Rising

**Anomaly**:
How a month's Harmonized Hotspot Count compares with the median of the same calendar month across every other year, written as a multiple such as "3.2× normal". The median keeps a few extreme fire years from making ordinary years look quiet.
_Avoid_: Departure, deviation, Times Normal

**Overlap Period**:
The years when MODIS and VIIRS both observed the Coverage Area (2012 onward), used to calibrate one sensor against the other.
_Avoid_: Calibration window, shared years
