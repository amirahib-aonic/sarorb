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
An Area of Interest whose Boundary is set in the app, by drawing on the map, typing or pasting points, or loading a boundary file. It can be moved and reshaped. Copying a Preset Area makes a Drawn Area.
_Avoid_: draw area, polygon, custom area, coordinates area

**Preset Area**:
An Area of Interest whose Boundary is an official one. It cannot be reshaped.
_Avoid_: admin area

**Boundary**:
The outline of an Area of Interest: an ordered ring of latitude, longitude points. A Drawn Area's Boundary is set in the app; a Preset Area's is official.
_Avoid_: polygon, bounding box, coords, shape

### Fire record

**Hotspot**:
A single satellite detection of active fire at a location and time, from either MODIS or VIIRS.
_Avoid_: Fire, fire point, detection

**Harmonized Hotspot Count**:
The monthly number of Hotspots in an Area of Interest, expressed as the count VIIRS would have recorded, whichever sensor actually observed it.
_UI label_: H Count (visible label, as in the Space Apps project summary; the "i" explains it as short for Harmonized Hotspot Count)
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

**Observation Window**:
A fixed 12-hour daytime or night-time block within one day that gathers every Hotspot observed in it, from any sensor.
_UI label_: satellite pass
_Avoid_: Overpass, time step

**Pass Cluster**:
A group of nearby Hotspots within one Observation Window, located at their centre.
_UI label_: Hotspot group
_Avoid_: Group, cluster, fire patch, fire spot

**Fire Event**:
A chain of Pass Clusters in successive Observation Windows judged to be the same burning, counted for an Area of Interest and month when any of its Hotspots fall inside both.
_Avoid_: Fire, event, incident

**Hotspot Shift**:
The observed change in location between the centres of two linked Pass Clusters. It is not a measure of how fast a fire spreads.
_Avoid_: Fire movement, spread, fire direction, move

**Fire Radiative Power**:
How much heat a Hotspot or Pass Cluster gives off, in megawatts (MW). Bigger means a hotter, more intense fire.
_UI label_: Heat given off (FRP)
_Avoid_: intensity, brightness, fire strength

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

### Help

**Guided Tour**:
A step-by-step walk through one task, checking fire in an area, that highlights each control in turn. It runs once on a first visit and can be restarted from the "?" button or the About tab. While it runs it shows a busy demo area, then puts back the user's own Area of Interest and view.
_Avoid_: walkthrough, onboarding, tutorial, coach marks

**Explainer**:
The ⓘ note next to a term or control that says what it means in plain words. It covers what the Guided Tour leaves out.
_Avoid_: tooltip, info icon, help text
