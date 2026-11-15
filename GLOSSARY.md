# IGNIS

Integrated Geospatial Network for Ignition Surveillance: a web app that brings MODIS and VIIRS fire Hotspots into one consistent view, with a burning calendar (when) and a heatmap (where). Built by Sarawak Orbiters for NASA Space Apps 2026, "Harmonization of MODIS and VIIRS Hot Spots".

## Language

### Places

**Coverage Area**:
The island of Borneo (Kalimantan, Sarawak, Sabah and Brunei), the whole region IGNIS holds a Hotspot record for. Every Area of Interest lies inside it.
_Avoid_: Fire Area, study area, region

**Area of Interest**:
Any region a user selects to examine, either drawn on the map as a shape or picked from a preset: a province, state or country, or a district or division within one. Only one is active at a time, and only the part inside the Coverage Area counts.
_Avoid_: AOI, selection, bounding box, study area

**Drawn Area**:
An Area of Interest the user shaped on the map. It can be moved and reshaped. Copying a Preset Area makes a Drawn Area.
_Avoid_: draw area, polygon, custom area

**Preset Area**:
An Area of Interest that follows an official boundary. It cannot be reshaped.
_Avoid_: admin area, boundary

### Fire record

**Hotspot**:
A single satellite detection of active fire at a location and time, from either MODIS or VIIRS.
_Avoid_: Fire, fire point, detection

**Harmonized Hotspot Count**:
The monthly number of Hotspots in an Area of Interest, expressed as the count VIIRS would have recorded, whichever sensor actually observed it.
_UI label_: Combined count (visible label; the "i" names the Harmonized Hotspot Count)
_Avoid_: merged count, raw count

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
How a month's Harmonized Hotspot Count compares with the median of the same calendar month across every other year, said in plain words such as "3.2 times the usual September" or "Half the usual March". For a Date Range, it is the Range Total against those medians added up for the same months. The median keeps a few extreme fire years from making ordinary years look quiet.
_UI label_: Compared with the usual
_Avoid_: Departure, deviation, Times Normal, normal

### Views

**Map View**:
What the heatmap shows for an Area of Interest, one at a time: a single Month, the Range Total, the Typical Year for a calendar month, or the Anomaly for a month.
_Avoid_: Mode, layer, map mode

**Date Range**:
The period a user picks to filter the heatmap and downloads. The Burning Calendar always shows the full history, with the Date Range outlined on it.
_Avoid_: Time window, period, filter

**Range Total**:
The Harmonized Hotspot Count summed over every month the Date Range touches.
_Avoid_: Range sum, cumulative count, season total

### Calibration

**Overlap Period**:
The years when MODIS and VIIRS both observed the Coverage Area (2012 onward), used to calibrate one sensor against the other.
_Avoid_: Calibration window, shared years
