# Showing hotspot shift direction without arrows

Research note for the Borneo prototype (`docs/research/prototypes/borneo.PROTOTYPE.html`, `computeVectors`). Date: 2026-11-15.

Source-tool labels: **[WS]** = native WebSearch, **[DS]** = donsetch `web_search`. Full texts were not fetched in this pass. Every Evidence line rests on a search snippet or search-tool summary, never on a read of the full paper. Read the full text before quoting these externally.

## Summary

- **Evidence:** Fire products that track spread encode it as **progression in time**, not as glyphs. FEDS draws 12-hourly perimeters of each fire event. The Global Fire Atlas splits daily growth into speed, fire-line length and direction of spread, and publishes them as gridded layers. FIRED keeps one polygon per day of each event.
- **Evidence:** In Holten & van Wijk (CHI 2009), standard arrowheads did worse than alternatives. Tapered edges did best.
- **Reasoning:** Our data is sparse (about 350 segments in a peak window) and event-based. Particle flow-field layers (leaflet-velocity, earth.nullschool) need a dense u/v grid, so they would invent motion between events. That is dishonest for our data.
- **Ranked recommendation:** (1) tapered gradient trails per segment, (2) arrival-window colouring of the existing cells (a discrete isochrone), (3) an FRP-weighted centroid track per Fire Event. Per-cell rose wedges are a useful option for the aggregated zoom-≤10 view.

## Techniques

### 1. Tapered or gradient-fade segments (comet trails)
- **How it encodes direction:** A line goes from thin to thick, or faint to opaque, from the older cluster to the newer one. No arrowhead is drawn.
- **Evidence:** Holten & van Wijk, CHI 2009 study of directed-edge representations (doi:10.1145/1518701.1519054), pp. 2299–2308. Snippets say the standard arrowhead depiction is "less effective" than alternatives. https://dl.acm.org/doi/pdf/10.1145/1518701.1519054 [DS]; author PDF https://www.researchgate.net/publication/221515079 [DS]; summary at https://en.wikipedia.org/wiki/Jack_van_Wijk [DS]. Per our recollection of the paper (not re-read here), tapered edges were fastest and most accurate, and intensity or colour gradients came next. The tapered direction was wide at the source and narrow at the target.
- **Fit:** High. One segment maps to one `{from, to}` pair. Width can still carry FRP: scale the wide end by `to.frp`. Missed windows can stay dashed or use lower opacity.
- **Cost:** Low. Draw a filled quadrilateral (a trapezoid) per segment on the canvas renderer, or use `createLinearGradient` for opacity. About 350 polygons per frame is trivial.
- **Note:** The direction convention, wide→narrow or narrow→wide, must be stated in the legend. Readers have no built-in default for it.

### 2. Animated particles and flow lines (leaflet-velocity, earth.nullschool, Windy)
- **How it encodes direction:** Particles advect along an interpolated vector field. Fading trails show heading and speed.
- **Evidence:** leaflet-velocity is a canvas Leaflet layer for "direction and intensity" of wind or ocean currents. It is built on WindJS, and its input is grib2json-style gridded u/v data. https://github.com/onaci/leaflet-velocity [WS]; README https://unpkg.com/leaflet-velocity@2.1.4/README.md [WS].
- **Fit:** Poor. The input is a continuous gridded field, and our segments are discrete event hops. Turning ~350 hops into a field means interpolating motion where no fire was. **Reasoning:** That misleads.
- **Cost:** Medium. Data must be rasterised to a u/v grid, and the animation runs continuously.
- **Variant that is honest:** Animate dots *along real segments only*, one per segment, moving from `from` to `to`. Animation should be opt-in. Static encodings stay primary, because animated encodings are hard to compare and can't be printed in the report or exports.

### 3. Fire progression, arrival time and isochrone maps
- **How it encodes direction:** Areas are coloured by when they first burned, from early to late. The direction of spread is the colour gradient, and spacing between contours shows speed.
- **Evidence:** FEDS tracks "growth and intensity of individual fires every 12 hours" as discrete event objects with alpha-shape perimeters. https://gis.earthdata.nasa.gov/portal/home/item.html?id=fac8f2ba3f054ff8ab5231e511e5dacd [DS]; https://earth-information-system.github.io/fireatlas/docs/data_overview.html [DS]; NRT perimeters every 12 h https://earth-information-system.github.io/fireatlas/docs/nrt.html [DS].
- **Evidence:** The Global Fire Atlas (Andela et al. 2019, ESSD 11:529–552) splits daily expansion into speed, fire-line length and direction of spread. Data is at DOI 10.3334/ORNLDAAC/1642. https://essd.copernicus.org/articles/11/529/2019/ [WS]. Its direction layer is a per-pixel categorical direction. Per our recollection it uses 8 classes; that was not verified in this pass.
- **Evidence:** FIRED (Balch et al. 2020, Remote Sensing 12:3498) produces event polygons plus per-day polygons with shared IDs, "to calculate fire spread rate". https://earthlab.colorado.edu/blog/fired-fire-event-dilineation [WS].
- **Evidence:** GOFER tracks hourly progression and compares it with FEDS. https://essd.copernicus.org/preprints/essd-2023-389/essd-2023-389.pdf [DS]. GlobFire (Artés et al. 2019): verified, see Verification pass below.
- **Fit:** High. This is the domain-standard form, and our 3-state underlay is already a 3-step version of it. Use about 0.1° cells with 12 h windows. Contours from cells would be blocky, so a sequential colour ramp on the cells is better.
- **Cost:** Low. Recolour the existing cells by `win`.

### 4. Directional wedges or rose glyphs per cell
- **How it encodes direction:** Each cell gets a small polar histogram of segment bearings. Sector length shows count or summed FRP.
- **Evidence:** This is the GFA's own approach of per-pixel spread direction (above). No dedicated perception study was retrieved. **Reasoning:** Roses at about 10 px get unreadable beyond 4–8 sectors.
- **Fit:** Medium. It suits the zoom-≤10 aggregation, which already groups by 0.1° cell, and it shows *mixed* directions honestly where an averaged arrow would cancel them out.
- **Cost:** Low to medium. It is a few `arc` calls per cell, after binning `bearing` into 8 sectors.

### 5. Flow-map aggregation (flowmap.blue / flowmap.gl)
- **How it encodes direction:** Locations are clustered by zoom and origin–destination flows are aggregated. flowmap.gl draws direction with a half-arrow, tapered-style flow.
- **Evidence:** The flowmap.gl clustering docs say it clusters locations by zoom level. https://flowmap.gl/docs/api/clustering/ [DS]. It is a deck.gl WebGL layer for movement between locations. https://github.com/visgl/flowmap.gl [DS]. A Flowmapper.org paper notes that curved flows are not available in flowmap.blue, and that it clusters locations. https://www.geo-social.com/docs/Koylu_Tian_Windsor_2021_FlowMapper.pdf [DS].
- **Fit:** Medium to low. It is built for many repeated OD pairs. Our hops are short, mostly one cell to a neighbour, so aggregated flows collapse into stubs.
- **Cost:** High. It needs deck.gl alongside Leaflet. Borrow the clustering idea, not the library.

### 6. Vector-field streamlines
- **Reasoning:** These have the same problem as technique 2. Streamlines need a continuous field, and integrating through gaps invents a path. Reject.

### 7. FRP-weighted centroid track per Fire Event
- **How it encodes direction:** For each event, compute the FRP-weighted centroid per `win`, then draw a polyline through them, with an optional taper (as in technique 1). The track shows the event's net drift.
- **Evidence:** No product publishes exactly this. FEDS and FIRED provide per-step event geometry from which such a centroid follows. **Reasoning:** This is a derivation, not a cited product.
- **Fit:** High for a summary view. One line per event is far fewer marks than ~350 segments. It hides splits and merges, so offer it as a mode, not as the only view.
- **Cost:** Low.

## Ranked recommendation (Reasoning)

1. **Tapered gradient segments**, replacing arrows. For each segment, draw a trapezoid from `from.lat/lon` (width ~1 px, alpha 0.25) to `to.lat/lon` (width ∝ √`to.frp`, alpha 0.9). Segments with `missed > 0` get reduced alpha or a dash. At zoom ≤10, sum the cell-grouped segments into one taper per cell pair. Confirm with a quick A/B where users name the direction of 10 segments.
2. **Arrival-window ramp on the underlay.** Replace the "ember earlier-burned" state with a sequential ramp on the first `win` each cell burned in the month, early dim to late bright, and keep the current 12 h window outlined. This gives direction for every cell without glyphs and matches FEDS and GFA practice.
3. **FRP-weighted centroid track per event**, as a toggle. Group clusters by event and `win`, take the centroid Σ(frp·lat)/Σfrp and the same for lon, and draw a tapered polyline (as in technique 1). Use it for the overview and the report image.

Optional: show 8-sector rose glyphs at zoom ≤10 where cell bearings are mixed. Opt-in animated dots along real segments only. Do not use leaflet-velocity or streamlines.

## Assumptions
- The fields `from`, `to`, `km`, `bearing`, missed windows, `win`, `frp` and event membership exist as the brief describes. The source was not read in this pass.
- Leaflet's canvas renderer is the drawing target. deck.gl is not already in the page.

## Verification pass (2026-11-15)

Full texts were read for the claims below. [DS] = donsetch `web_fetch`/`web_search`, [WS] = native WebSearch.

| Claim | Status | Source |
|---|---|---|
| Tapered directed edges beat standard arrowheads | **Verified (by the same authors)**. The 2009 CHI PDF was blocked (ResearchGate 403), but the 2011 follow-up by the same authors lists "(a) standard arrow" and "tapered" among those tested and says of their 2009 study "[15]" that "we found that a tapered representation" "outperformed all other techniques". The 2011 study also tested animated and textured variants, with tapered and compressed patterns doing well | Holten, Isenberg, van Wijk, Fekete, PacificVis 2011, https://inria.hal.science/inria-00548180/PDF/PacificVis2011.pdf [DS]; secondary confirmation [WS] |
| Global Fire Atlas encodes spread direction in 8 classes | **Verified**. Direction is taken from the next grid cell on the "fire path", giving eight directions (N, NE, E, SE, S, SW, W, NW). Single-day and single-pixel fires get no direction. Where paths overlap, the earliest arrival or fastest speed wins | Andela et al. 2019, ESSD 11:529, section 2.2, https://essd.copernicus.org/articles/11/529/2019/essd-11-529-2019.html [DS] |
| GlobFire stores daily burned areas per event | **Verified**. Each event has a start date, end date, final multipolygon, and a second table of daily burned areas keyed by the same event ID. In the paper's Chile example, the daily burned areas share their event's colour | Artés et al. 2019, Sci Data 6:296, https://www.nature.com/articles/s41597-019-0312-2 [DS]; GEE catalog [DS] |
| FEDS gives 12-hourly perimeters and fire lines | **Verified**. FEDS-MTBS gives "12-hourly fire perimeters, active fire lines and newly detected fire pixels with their fire radiative power (FRP)" | UCI-UBC-NASA fire tracking page, https://www.ess.uci.edu/~uci-nasa-firetracking/ [DS]; FIRMS FEDS page is JS-only, not readable |
| FIRED has one polygon per day per event | **Verified via secondary sources only**. The event product has one polygon per event; the daily product has separate polygons per date with the same event ID | Earth Lab and CU Scholar dataset pages [WS]; Balch et al. 2020, Remote Sens. 12:3498 not read |

Implications for the ranking (Reasoning):
- Rank 1 (tapered segments) stands, now on a primary source. The 2011 paper also suggests combining taper with other cues, which supports keeping a dash or lower opacity for missed windows.
- Rank 2 (colour cells by first-burn window) matches how GlobFire, FIRED and FEDS show progression: per-time-step burned areas within one event.
- GFA-style 8-sector direction is an established, published encoding. That makes the optional per-cell rose glyph at low zoom defensible: bin `bearing` into 8 sectors the way GFA does.
