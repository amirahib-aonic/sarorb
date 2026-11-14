# IGNIS UI/UX Pattern Library

Synthesized from all 13 audits in this folder (each audited 2026-11-14; see [README.md](README.md) for the index and takeaways). IGNIS domain terms follow [../../GLOSSARY.md](../../GLOSSARY.md) exactly: Hotspot, Harmonized Hotspot Count, Burning Calendar, Typical Year, Burning Phase, Overlap Period, Coverage Area, Area of Interest. The four audience labels come from section 1 of the research plan, not the glossary; **haze-impact audience** is defined here as *everyone in the Coverage Area exposed to haze — both downwind (Sarawak/Kuching) and source-side (Kalimantan, breathing the smoke where it starts)*, and is a candidate addition to GLOSSARY.md. Where this library specifies numbers (Burning Phase cutoffs, Typical Year statistics, performance budget, record scope), it draws on the repo's own [harmonization analysis](../../docs/research/harmonization-analysis.md) and [ADR 0001](../../docs/adr/0001-viirs-equivalent-scaling.md).

Each pattern names its source app(s), links a screenshot when one exists under `img/`, carries one verdict — **inherit** (take as-is), **adapt** (take with the named changes), **avoid** (a demonstrated failure) — and names the user it serves: first responder, scientist, land manager, or the haze-impact audience. Where source apps disagree, the entry says which approach to take.

## Ground rules

Cross-cutting decisions that every pattern below assumes. They live here so they are stated once, not re-invented per view.

- **Performance budget.** First useful answer in ≤ 3 s and ≤ ~1 MB transferred, with the Burning Calendar grid server-rendered in the first HTML paint. Basis: the audits' own measurements — FIRMS (3.5 s / 0.5 MB) and SiPongi+ (~2.8 s / 87 resources) scored 2/2/2 and were marked inherit, while GNW ex-GFW (12.5 s / 2 MB), ASMC (~18 s / 2.4 MB) and Worldview (15.6 s / 6.5 MB) were marked avoid for exactly this. A first responder on mobile data in rural Borneo is the design case.
- **Linked-views contract (both directions).** (1) Clicking a Burning Calendar cell, or a day in the recent-days strip, filters the heatmap to that period in the current Area of Interest. (2) Selecting an Area of Interest on the heatmap (preset click or drawn shape), or scrubbing a date there, recomputes the Burning Calendar for that Area of Interest and highlights the period. (3) Both views share one URL state, so the compare picker, calendar and heatmap never disagree. Evidence: GFW verified date-range → widgets and Area of Interest → panel linkage, Watch Duty links list ↔ map both ways, SiPongi+ refetches the map live from filters; GWIS and ASMC are the disconnected failure mode. No audited app links a calendar to a map in both directions — that link is IGNIS's own build, specified here.
- **Record scope.** The Burning Calendar shows **2002–present**: 2002–2011 are harmonized MODIS months (VIIRS-equivalent, ±12% uncertainty, labelled as estimates), 2012–present are observed VIIRS months, per the [harmonization formula](../../docs/research/harmonization-analysis.md) — H(y,m) = k(m) × M(y,m) for MODIS-only months. "No data" means only what is outside that span (or a month FIRMS has no rows for); zero Hotspots is a real value, not a gap.

---

## Burning Calendar

### Year-by-month grid under a Typical Year
- **Sources:** GWIS (fire-season month×year heatmap), D3 calendar notebooks (week-aligned year rows), GitHub contribution graph (year strip).
- **Screenshots:** [GWIS month×year grid](img/gwis/04-country-charts-multiyear-kalimantan-barat.png) · [D3 year rows](img/d3-calendar/01-d3-calendar-overview-weekdays-only.png) · [GitHub grid](img/github-contrib-graph/01-first-screen-calendar-heatmap.png)
- **Verdict:** adapt
- **Serves:** land manager, scientist
- **Why:** Rows of years on a shared month axis make the burning season and anomalous years readable with zero interaction — the direct ancestor of the Burning Calendar's year-by-month grid of Harmonized Hotspot Counts — and the grid should ship server-rendered in the first HTML paint the way GitHub's does, so no control stands between the user and the first answer.

### Pre-aggregated historical envelope band
- **Sources:** Global Nature Watch ex-GFW (shaded "Normal Range" band + Above/Below markers), GWIS (min–max + 10–90th percentile envelopes + average), Climate Reanalyzer (all-years gray mass + 2 highlight colors).
- **Screenshots:** [GNW Normal Range band](img/global-forest-watch/03-dashboard-weekly-fire-alerts-vs-normal-range.png) · [GWIS envelope vs chosen year](img/gwis/05-charts-2023-vs-historical.png) · [Climate Reanalyzer 90-series overlay](img/climate-stripes/02-t2-daily-default-all-years.png)
- **Verdict:** adapt
- **Serves:** all three users
- **Why:** Shading the Typical Year's expected range and marking above/below cells answers "is this year unusual?" without any math.
- **Where apps disagree:** GNW/GWIS pre-aggregate the band and stay fast, while Climate Reanalyzer's 90 live per-year series repeatedly stalled the main thread 8–30 s — take the pre-aggregated band (computed server-side from the whole archive), keep at most two highlighted years, and never ship one live series per year. Among the band statistics the sources ship, **take GWIS's 10–90th percentile band and drop min–max**: over a 25-year Borneo record the min–max span reaches from a near-zero drought-free year to a severe El Niño year and swamps the band.
- **Typical Year parameters (specified here, once):** the Typical Year is the **median** Harmonized Hotspot Count for each calendar month over the **full harmonized record, 2002–present** (per the Ground rules' record scope), with the 10–90th percentile of the same distribution as its envelope. Median, not mean, because the severe El Niño years the harmonization doc calls out (2002, 2006, 2009, 2015, 2019) would drag a mean above what any normal year looks like. Pre-2012 months entering this average are the ±12% harmonized estimates; show that uncertainty on the band's pre-2012 portion, exactly as the [harmonization analysis](../../docs/research/harmonization-analysis.md) prescribes for the calendar. If the architect later prefers an observed-only baseline, the fallback is 2012–present — but then say so on the chart, GWIS-style, in the subtitle.

### First-class any-two-year compare — one control, two projections
- **Sources:** GitHub (year links that swap the grid, each a shareable URL), NASA Worldview (A\|B compare with an independent date per side), Global Nature Watch ex-GFW and ASMC (manual year re-picking), Climate Reanalyzer (per-series toggles that failed in practice).
- **Screenshots:** [GitHub year swap](img/github-contrib-graph/03-year-navigation-2023.png) · [Worldview A\|B 2023 vs 2019](img/nasa-worldview/04-task3-ab-compare-2023-vs-2019.png)
- **Verdict:** adapt
- **Serves:** scientist, land manager
- **Why:** "Is 2023 worse than 2019?" is a core IGNIS question and every audited app makes it expensive — GFW needed ~18 manual interactions, ASMC 5 clicks per year, GitHub holds one year in memory, and Climate Reanalyzer's year-pair toggles were covered by a sticky header and never landed.
- **Relationship to the heatmap's A\|B compare (specified once):** there is **one** two-year picker, and it drives **both** projections — the Burning Calendar highlights those two year rows against the Typical Year envelope, and the heatmap's swipe/side-by-side mode binds year A to side A and year B to side B (see *A\|B compare modes with an independent date per side*). Setting years in either view updates the same shared URL state, so the calendar and the map can never show different year pairs. Do not build two compare systems.

### Burning Phase encoding — the single source of truth
- **Sources:** GitHub (5-step single-hue ramp + distinct empty color), D3 calendar (`@d3/calendar/2` outlier-capped domain; pinned domain across views), Windy (verbal tiers "Very low → Extreme" over a green→red ramp), APIMS (ranges printed on every tier card; shape-per-tier encoding), GWIS (threshold legend table with numeric cutoffs).
- **Screenshots:** [GitHub 5-step ramp](img/github-contrib-graph/01-first-screen-calendar-heatmap.png) · [Windy verbal-tier legend](img/windy/02-fire-danger-layer-pontianak.png) · [APIMS tier cards with ranges](img/apims-iqair/01-apims-dashboard-tier-cards.png)
- **Verdict:** adapt — the ramp, verbal-tier and printed-threshold mechanics are inherited; the four-tier mapping below is IGNIS's own and no source ships it.
- **Serves:** all three users plus the haze-impact audience
- **Why:** One quantized scale that every calendar cell, tier card and legend shares, so a color always means the same thing.
- **The encoding (this entry is the specification; every other pattern defers to it):**
    - **Four tiers, not five or six.** GLOSSARY.md fixes the labels — Peak burning, Active burning, Moderate, Low — and they supersede the sources' counts: GitHub's fifth visual step is repurposed as the separate **no-data** color (a month with no record is not a Low month), and APIMS's six cards and Windy's six verbal tiers contribute the *mechanisms* (printed ranges, words on the legend), not the tier count.
    - **Basis: each month's share of the Typical Year's annual Harmonized Hotspot Count** (the glossary's own definition of Burning Phase), computed **per Area of Interest** — so a Kalimantan province's Peak and Brunei's Peak each mean "this area's biggest month," which absolute counts could never make comparable. Because the basis is a share, the same numeric cutoffs apply to every Area of Interest: pinned globally, fair locally.
    - **Proposed cutoffs:** Low < 3%, Moderate 3–10%, Active burning 10–25%, Peak burning ≥ 25% of the Typical Year's annual total. Sanity check on the only full monthly series in the audits (SiPongi national MODIS 2019: Sep 56.7%, Oct 15.5%, Aug 12.6%, Nov 7.0% of the annual total) → Sep Peak, Aug+Oct Active, Nov Moderate, rest Low — the intended reading. These numbers are proposals: the architect tunes them when the Borneo-wide data the [harmonization analysis](../../docs/research/harmonization-analysis.md) says is still to be refit arrives, and prints whatever is final next to the colors (APIMS/GWIS discipline).
    - **Shape per tier** (from the *Colour + shape dual encoding* pattern): Peak burning ● filled circle, Active burning ▲ filled triangle, Moderate ■ filled square, Low ○ open circle; no-data keeps the distinct empty color and no shape.
    - **Outlier cap:** where a continuous scale is needed (the recent-days strip, heatmap density), cap the color domain at a high quantile as `@d3/calendar/2` does, so one El Niño September does not wash out every other month.

### One-click re-binning radios
- **Sources:** D3 calendar (`discovering-date-patterns` facet radios), NASA Worldview (YEAR/MONTH/DAY interval chips), IQAir (Hourly/Daily/Monthly history tabs).
- **Screenshots:** [D3 facet radios](img/d3-calendar/09-date-patterns-facet-rebin-1-click.png) · [IQAir granularity tabs](img/apims-iqair/08-iqair-kuching-monthly-history.png)
- **Verdict:** adapt
- **Serves:** all three users
- **Why:** Radios that rebuild the whole grid at day/week/month granularity in one click — with the control label naming the axis it changes — answer the granularity question far more cheaply than a zoom, and let the Burning Calendar default to monthly cells while still drilling to a single week.

### Play-the-season playback with GIF export
- **Sources:** Windy (one-click film-style player: play/pause, timecode badge, scrub bar, day strip), NASA Worldview (animation widget with start/end dates, speed, loop, GIF export).
- **Screenshots:** [Windy timeline](img/windy/02-fire-danger-layer-pontianak.png) · [Worldview animation widget](img/nasa-worldview/05-animation-widget-sep2023.png)
- **Verdict:** adapt
- **Serves:** first responder, land manager
- **Why:** One click that sweeps the heatmap across a season of Harmonized Hotspot Count frames — with Worldview's GIF export for briefings — communicates when burning happens better than any static view, provided IGNIS precomputes the frames so playback never stalls like Worldview's "Determining buffer size…" dialog did.

### Explicit data-availability marks
- **Sources:** Sentinel Hub EO Browser → Copernicus Browser (the successor **dropped** EO Browser's per-day availability timeline), NASA FIRMS (greyed-out layer row "DATA ONLY AVAILABLE - 2015-11-24 TO 2026-11-02"), D3 calendar (TWO-N keeps month labels over empty months).
- **Screenshots:** [Copernicus plain calendar, no marks](img/sentinel-hub/04-date-picker-calendar-sept2026.png) · [FIRMS S-NPP availability row](img/nasa-firms/01-first-screen-default-view.png) · [TWO-N labeled empty months](img/d3-calendar/08-two-n-calendar-mode-holdtime.png)
- **Verdict:** adapt
- **Serves:** scientist
- **Why:** EO Browser's sunset proves availability marks are the first thing a successor loses, and without them users pick blind dates and wait — so every Burning Calendar cell must visibly distinguish three states: zero Hotspots (a real value), no data (only months outside the 2002–present record, per the Ground rules), and **harmonized estimates** — the 2002–2011 cells carry the ±12% uncertainty band and an "estimate" label the [harmonization analysis](../../docs/research/harmonization-analysis.md) itself prescribes, so users can tell converted months from observed ones across the 2012 Overlap Period boundary.

### Read-then-drill ladder with a real tooltip
- **Sources:** GitHub (annual total → year shape → hover for exact count → click filters a detail feed), D3 calendar (multi-line aggregated tooltip; **avoid** its native `<title>` hover and its clickable-looking cells that do nothing).
- **Screenshots:** [GitHub day-click drill-down](img/github-contrib-graph/02-day-click-filters-activity-feed.png)
- **Verdict:** adapt
- **Serves:** all three users
- **Why:** The ladder — headline count, year shape, hover for "12 Hotspots on Aug 3", click to filter the detail list and heatmap to that date — is the Burning Calendar's interaction spine, but it needs a styled tooltip component (the browser-default `<title>` never photographed in the D3 audit) and cells that visibly respond on click, never a pointer cursor over a dead cell.

### Recent-days strip
- **Sources:** APIMS (rolling 24-hour table: tier-coloured chips, one row per station), Windy (15-day day strip above the timeline, today highlighted), ASMC Haze Information Portal (rolling 10-day date-chip strip + prev/next-day steppers).
- **Screenshots:** [APIMS hourly chip table](img/apims-iqair/02-apims-hourly-table-tier-legend.png) · [ASMC 10-day chips](img/asmc/10-haze-information-portal.png) · [Windy day strip](img/windy/02-fire-danger-layer-pontianak.png)
- **Verdict:** adapt
- **Serves:** first responder
- **Why:** A monthly-default Burning Calendar cannot answer "is it burning now," so a strip of the last 10–15 days as day cells — colored by the Burning Phase encoding's continuous scale, count in the cell, one click to filter the heatmap to that day (per the Ground-rules linkage contract) — gives the responder their daily surface without leaving the calendar view.

### Sparse, responsive axis labels with a width budget
- **Sources:** GitHub (day labels thinned to Mon/Wed/Fri, month labels only where a month starts, full + abbreviated names in the DOM), D3 calendar (ticks collapse to single letters under 600 px; December truncates at 928 px).
- **Screenshots:** [GitHub sparse labels](img/github-contrib-graph/01-first-screen-calendar-heatmap.png) · [D3 December clipping](img/d3-calendar/03-d3-calendar2-current-example.png)
- **Verdict:** adapt
- **Serves:** all three users
- **Why:** A 53-column grid stays legible with thinned labels and no rotated text, but the D3 notebooks' reproduced December clipping shows IGNIS needs an explicit width budget (or horizontal scroll) for 12-month rows on phones.

### Colour + shape dual encoding
- **Sources:** APIMS (a distinct shape per tier, stated "for people with color vision deficiency").
- **Screenshots:** [APIMS shape-encoded infographic](img/apims-iqair/04-apims-api-infographic.png)
- **Verdict:** inherit
- **Serves:** all three users plus the haze-impact audience
- **Why:** Giving every Burning Phase both a color and a marker shape keeps the Burning Calendar and heatmap legends readable for color-blind users — a stated, shipped practice at a national authority, not a heuristic. The shapes themselves are assigned in *Burning Phase encoding — the single source of truth* (Peak ●, Active ▲, Moderate ■, Low ○, no-data: color only); this pattern is the mechanism, that one is the specification.

---

## Heatmap

### Map-first landing over the Coverage Area
- **Sources:** NASA FIRMS (last-24-h Hotspots drawn on load), Watch Duty (map + freshness-ranked incident list at zero clicks), Windy (full-screen map, instant answer), ASMC (map-first home).
- **Screenshots:** [FIRMS default load](img/nasa-firms/01-first-screen-default-view.png) · [Watch Duty first screen](img/watch-duty/01-first-screen-map-and-incident-list.png) · [ASMC home map](img/asmc/01-home-regional-haze-situation-map.png)
- **Verdict:** adapt — the map-first shell is taken as the sources ship it; the named changes are IGNIS's own: open on the Borneo Coverage Area (not FIRMS's whole-globe default that forced every task to start with search-and-zoom) and keep the Burning Calendar beside the map per the Ground-rules linkage contract, not behind a tab.
- **Serves:** first responder
- **Why:** Every responder-grade reference lands map-first with live data already drawn, and the first screen must obey the Ground-rules performance budget — ≤ 3 s / ≤ 1 MB — that FIRMS (0.5 MB) meets and GNW/ASMC/Worldview fail.

### A\|B compare modes with an independent date per side
- **Sources:** NASA Worldview (side-by-side, Swipe, Opacity, Spy; per-side dates and layers; **avoid** its mode exclusivity — compare locks out animation and download).
- **Screenshots:** [Side-by-side 2023 vs 2019](img/nasa-worldview/04-task3-ab-compare-2023-vs-2019.png) · [Swipe mode](img/nasa-worldview/07-swipe-mode-type-buttons.png)
- **Verdict:** adapt — the swipe/side-by-side/opacity/spy mechanic is taken as Worldview ships it; the named changes are IGNIS's own: the two sides' dates are **driven by the single two-year picker** specified in *First-class any-two-year compare — one control, two projections* (year A → side A, year B → side B, one shared URL state), and compare composes with playback instead of copying Worldview's rule that entering compare disables every other tool.
- **Serves:** land manager, scientist
- **Why:** A draggable swipe divider with an independent date on each side answered "is 2023 worse than 2019" in one screen — the strongest spatial comparison pattern audited.

### Hotspot age ramp scaled to the window
- **Sources:** NASA FIRMS ("Time since detection" 12-bucket ramp; on a 30-day window every dot collapses to the oldest pale-yellow bucket).
- **Screenshots:** [FIRMS age-ramp legend](img/nasa-firms/03-time-based-week-legend.png)
- **Verdict:** adapt
- **Serves:** first responder
- **Why:** Recoloring Hotspot dots by hours/days since observation answers "is it burning now?" at a glance, provided IGNIS scales the buckets to the active window length so a month-long view does not flatten the ramp to one color as FIRMS's does.

### Sensor-explicit layers with capability one-liners and freshness stamps
- **Sources:** Watch Duty ("VIIRS: Detects large and small fires, including cooler ones"; per-layer "Recent: 24 Hours Ago"), NASA Worldview ("Fires and Thermal Anomalies (Day and Night, 375m) Suomi NPP / VIIRS"), NASA FIRMS ("VIIRS (NOAA-20 & NOAA-21) [375m]"), Windy (source chips "ECMWF 9km / GFS 22km").
- **Screenshots:** [Watch Duty sensor cards](img/watch-duty/03-satellite-hotspots-layer-options.png) · [Worldview fire layers](img/nasa-worldview/02-task1-west-kalimantan-sep2026-fire-layers.png)
- **Verdict:** inherit
- **Serves:** all three users
- **Why:** One plain sentence per layer saying what a sensor can and cannot detect, plus its resolution and data age on the toggle itself, lets a non-scientist choose MODIS vs VIIRS vs the Harmonized Hotspot Count without knowing the instruments — the best sensor communication in the whole audit set.

### Per-sensor counts beside the Harmonized Hotspot Count
- **Sources:** SiPongi+ (per-satellite low/medium/high count strip, never merged), Global Nature Watch ex-GFW (high-confidence split beside every total), GWIS (MODIS and VIIRS chart pairs on a common 2012–2025 baseline), GitHub (one count in the cell, per-source breakdown one click down).
- **Screenshots:** [SiPongi per-satellite counts](img/sipongi/02-peta-province-picker-overlay.png) · [GWIS sensor-paired charts](img/gwis/07-seasonal-trend-indonesia.png)
- **Verdict:** adapt
- **Serves:** scientist
- **Why:** IGNIS's headline number is the Harmonized Hotspot Count, but scientists must see the raw MODIS and VIIRS counts beside it to know what harmonization did. **Where apps disagree:** SiPongi and Watch Duty never merge (honest but leaves no comparable series), FIRMS merges with no per-sensor toggles at all, and GitHub's shape is the one to take — one harmonized number in the cell, per-sensor breakdown one click down.

### Place-chain Hotspot popup
- **Sources:** SiPongi+ (village → district → regency → province chain, satellite, confidence, lat/lon, timestamp).
- **Screenshots:** [SiPongi Hotspot popup](img/sipongi/08-hotspot-popup-village-detail.png)
- **Verdict:** adapt — the mechanism is inherited; the chain must be **per-country**, because SiPongi's desa → kecamatan → kabupaten → provinsi hierarchy is Indonesia's and the Coverage Area also spans Malaysia and Brunei: Sarawak/Sabah need division → district → sub-district/kampung, Brunei needs district → mukim. That admin-boundary GIS for all three countries is a named data dependency (GNW ex-GFW's "Political boundaries" preset layer is the audited proof such data exists as a product).
- **Serves:** first responder
- **Why:** A click on a Hotspot that names the full local place chain is what a responder in Borneo actually dispatches to — the per-point detail FIRMS's merged canvas notably failed to deliver in four verified click attempts.

### One tabbed context-overlay panel
- **Sources:** SiPongi+ (Hotspot/Overlays/FDRS tabs: cloud, wind, air quality, rain, fire-danger indices), ASMC (2500 ft winds, rainfall, satellite image toggles), IQAir ("Fires", "Wind", "Air quality stations" side by side).
- **Screenshots:** [ASMC Haze Portal overlays](img/asmc/10-haze-information-portal.png) · [SiPongi layer panel](img/sipongi/03-peta-layer-panel-province-filter.png) · [IQAir fires + wind controls](img/apims-iqair/09-iqair-map-legend-fires-wind-controls.png)
- **Verdict:** adapt
- **Serves:** first responder, scientist
- **Why:** Optional meteorological context (wind, rain, haze) in one tabbed panel keeps the heatmap uncluttered while making Hotspots legible as smoke transport — but no layer may swallow clicks aimed at the panel beneath it, the bug that broke SiPongi's own map drill-down.

### Mobile-first shell with bottom-sheet drawers
- **Sources:** Watch Duty (at 390 px only map + floating buttons remain; search/list as modal sheets; one drawer component reused on desktop; **avoid** ASMC's squeezed desktop layout and Windy's clipped timeline at the same width).
- **Screenshots:** [Watch Duty phone layout](img/watch-duty/05-mobile-first-screen.png) · [Watch Duty modal search](img/watch-duty/06-mobile-search-list-modal.png) · [ASMC squeezed layout](img/asmc/09-mobile-390px-home.png)
- **Verdict:** adapt — the sheet-and-drawer mechanism is taken as Watch Duty ships it; the named change is IGNIS's own: the Burning Calendar becomes one more drawer in that system (see below), which no source ships.
- **Serves:** first responder
- **Why:** The strongest phone layout in the audit set — everything collapses into modal sheets and bottom drawers over the map — and the only one that was actually verified at 390 px rather than squeezed.
- **Where the Burning Calendar lives on a phone (specified, so this pattern and the map-first landing cannot conflict):** at 390 px the calendar is a bottom-sheet drawer opened from a persistent Calendar button in the floating stack, with the recent-days strip kept visible above the map's timeline so the responder's daily surface survives without opening the drawer.

### Full state in the shareable URL
- **Sources:** NASA FIRMS (`#d:2026-09-01..2026-09-30;@111.12,-0.09,10.00z`), NASA Worldview (extent, layers, date, compare flag), Windy (`?fwi,-0.704,109.345,8,p:firespots` — round-trip verified), Watch Duty (`/@lat,lng,z/pin?search=…`), Copernicus Browser (every control serialized), GitHub (year windows as `from=/to=`).
- **Screenshots:** [FIRMS SHARE dialog](img/nasa-firms/04-share-url-state.png)
- **Verdict:** inherit
- **Serves:** all three users
- **Why:** Six independent apps converged on the same mechanic — Area of Interest, Burning Calendar month/year selection and heatmap state in the address bar — because it makes every answer a responder builds linkable to their team with no server work.

### Export beside the data, filename encoding the state
- **Sources:** SiPongi+ (XLSX / TXT / KMZ one-click menu on the table), NASA FIRMS (screenshot export whose filename reconstructs the view), Climate Reanalyzer (one menu: PNG/JPEG/PDF/SVG/print + raw JSON), GitHub (**gap:** no export at all).
- **Screenshots:** [SiPongi export menu](img/sipongi/06-sebaran-table-export-xlsx-txt-kmz.png)
- **Verdict:** adapt
- **Serves:** scientist, land manager
- **Why:** Export controls belong next to the data they export — a CSV of the visible Harmonized Hotspot Count series and an image whose filename carries the Area of Interest and date range, not a separate download portal like FIRMS's archived-data flow.

### Flagship data one click from the top
- **Sources:** Windy (**avoid:** "Active fires" buried ~90 % down a 58-item settings list), Global Nature Watch ex-GFW (**avoid:** fire layer two menus deep under three default forest layers).
- **Screenshots:** [Windy buried fire layer](img/windy/01-layers-menu-display-on-map-active-fires.png)
- **Verdict:** avoid
- **Serves:** first responder
- **Why:** Both apps hide the exact layer their fire question needs behind defaults and deep menus — IGNIS's Hotspot and Harmonized Hotspot Count layers must sit at the top of the first panel, not beneath other data or inside generic settings.

### No blocking modal before the first answer
- **Sources:** NASA FIRMS (**avoid:** first-load NOTIFICATIONS modal covering the map), Global Nature Watch ex-GFW (**avoid:** announcement modal whose overlay blocked its own dismiss button), Copernicus Browser (**avoid:** anonymous-token gate that stalled twice).
- **Screenshots:** [FIRMS modal over the map](img/nasa-firms/01-first-screen-default-view.png) · [FIRMS modal at 390 px](img/nasa-firms/06-mobile-390px.png)
- **Verdict:** avoid
- **Serves:** first responder
- **Why:** Three separate apps put a modal between the user and the map on first load — whatever IGNIS needs to announce (including the Overlap Period story) belongs in a dismissible banner that never covers the data.

---

## Region panel

### Named Areas of Interest: click-a-shape, presets, draw
- **Sources:** Global Nature Watch ex-GFW (click province → name + area → ANALYZE), SiPongi+ (province dropdown → map refilters one admin level down), GWIS (country → province tree, two clicks, URL-encoded), Copernicus Browser (named tools for drawing an Area of Interest, a line, a point, or a measurement); NASA Worldview as the **avoid** case (place search centers a pin, never the province polygon — 7 wasted zoom clicks).
- **Screenshots:** [GNW click-a-shape analysis](img/global-forest-watch/02-map-analysis-panel-fire-widgets.png) · [GWIS province drill-down](img/gwis/03-country-overview-kalimantan-barat.png)
- **Verdict:** adapt
- **Serves:** land manager
- **Why:** The fastest Area of Interest picker audited is clicking a province shape and getting its statistics instantly, with drawn shapes and search as complements — and unlike Watch Duty's invisible 300-mile implicit selection, IGNIS must always show the chosen Area of Interest by name and zoom to its boundary extent.

### Auto-verdict sentences
- **Sources:** Global Nature Watch ex-GFW ("the peak fire season typically begins in mid-July and lasts around 13 weeks"; "unusually high compared to previous years going back to 2012").
- **Screenshots:** [GNW peak-season sentence widget](img/global-forest-watch/03-dashboard-weekly-fire-alerts-vs-normal-range.png)
- **Verdict:** inherit
- **Serves:** all three users
- **Why:** Stating the chart's conclusion in one plain sentence — an auto-computed Typical Year distilled to Burning Phase language — is the cheapest possible answer to "when does burning happen here," generated per Area of Interest.

### Burning Phase tier cards with counts and ranges
- **Sources:** APIMS (six cards: tier name + value range + live station count, zero clicks to "how bad is it overall").
- **Screenshots:** [APIMS tier cards](img/apims-iqair/01-apims-dashboard-tier-cards.png)
- **Verdict:** adapt
- **Serves:** first responder, land manager, haze-impact audience
- **Why:** A strip of tier cards over the Burning Calendar — each Burning Phase with its share cutoff, count of months in the current year, and shape, exactly as specified in *Burning Phase encoding — the single source of truth* — answers "how is this year shaped" before any interaction.

### Haze-impact panel with health actions and a Typical Year anchor
- **Sources:** IQAir (one number + tier + dominant pollutant + "1.4× the WHO guideline" + tier-specific actions), ASMC (daily prose narrative translating Hotspots into haze and air quality under the map), APIMS (dated "Transboundary Haze" references and a Malay advisory).
- **Screenshots:** [IQAir Kuching dashboard](img/apims-iqair/07-iqair-kuching-dashboard-aqi39-good.png) · [ASMC narrative under map](img/asmc/01-home-regional-haze-situation-map.png)
- **Verdict:** adapt
- **Serves:** haze-impact audience, first responder
- **Why:** Pairing the current air-quality tier and a health action with the Harmonized Hotspot Count and a Typical Year anchor ("3× a Typical March") is what makes burning in the Coverage Area legible as haze — IGNIS's clearest differentiator for the audience no fire app in this audit serves directly.
- **Data dependency, stated honestly:** no audited source exposes a free, downloadable Sarawak/Kuching air-quality feed — APIMS's pages are authoritative but static (no export, state not in the URL), IQAir shows the data but publishes no public CSV, and ASMC's WIS2 catalog link covers Hotspot coordinates, not AQ. Candidates for IGNIS: APIMS/MyEQMS as the authoritative Malaysian feed, IQAir as the design-and-possibly-API partner, ASMC's haze portal for regional context. Which feed ships — and on what terms — is an **open dependency for the architect**; until it is settled, the panel degrades to linking out (IQAir city page / APIMS tab) rather than fabricating a tier.

### Ranked Areas-of-Interest table
- **Sources:** GWIS (ranked table: area, historical average, current year, in absolute and %), Global Nature Watch ex-GFW ("regions with the most fire alerts"), IQAir (live city ranking).
- **Screenshots:** [GWIS ranked comparison table](img/gwis/08-estimates-country-comparison.png)
- **Verdict:** adapt
- **Serves:** land manager
- **Why:** A ranked list of provinces or districts inside the Coverage Area — current Harmonized Hotspot Count against each one's Typical Year — makes cross-place comparison instant where map gazing is not.

### Scrollable, responsive dashboard
- **Sources:** APIMS (**avoid:** page height locked to the viewport, half its own content unreachable at 768p and 1080p, right side clipped at 1282 px, state filter invisible to the accessibility layer).
- **Screenshots:** [APIMS clipped laptop viewport](img/apims-iqair/05-apims-laptop-viewport-clipped.png)
- **Verdict:** avoid
- **Serves:** all three users
- **Why:** A dashboard that scrolls and reflows is not optional — APIMS's fixed-viewport layout physically hid its ranking, chart and references from real users, the single most consequential layout defect in the audit set.

---

## About / method

### Methodology one click from every number
- **Sources:** GitHub ("Learn how we count contributions" directly under the grid), Global Nature Watch ex-GFW (per-dataset metadata modal with citation + DOI + licence), NASA FIRMS (Layer Information modal: temporal coverage, latency, overpass times), GWIS (ⓘ per metric + envelope footnotes), Climate Reanalyzer (dataset + version + DOIs + license below the chart).
- **Screenshots:** [GNW metadata modal](img/global-forest-watch/04-dataset-metadata-modal.png) · [GitHub grid with method link](img/github-contrib-graph/01-first-screen-calendar-heatmap.png)
- **Verdict:** inherit
- **Serves:** scientist
- **Why:** Every app trusted by scientists puts the method one click from the data — for IGNIS that means the Harmonized Hotspot Count definition and the Overlap Period calibration linked under the grid and beside every headline number, not parked on an unvisited page.
- **IGNIS already has the target pages — link them:** the formula, its per-month factors and its ±12% error live in [docs/research/harmonization-analysis.md](../../docs/research/harmonization-analysis.md) and the decision behind it in [ADR 0001](../../docs/adr/0001-viirs-equivalent-scaling.md); every "how is this counted?" affordance in the app should land on those (or an app-rendered summary of them), not on text yet to be written.

### Inline caveat under every chart
- **Sources:** ASMC (same five-bullet caveat block under every map and chart), Global Nature Watch ex-GFW (sampling note under the numbers; "be cautious comparing before/after 2015"), Watch Duty (provenance on every update; "reporters are not actively monitoring this incident"), APIMS (averaging rule stated under the data).
- **Screenshots:** [Watch Duty provenance banner](img/watch-duty/02-incident-detail-updates.png)
- **Verdict:** inherit
- **Serves:** scientist
- **Why:** Never show a Hotspot count without its caveats in the same breath — cloud-cover misses, reprocessing, and the harmonization approximation are part of the number, and repeating the block on every view (ASMC's discipline) beats a single FAQ entry.

### Sensor-era honesty: transition notices and record-aware periods
- **Sources:** SiPongi+ (dated banner: NOAA-21 replaces retired SNPP, "coverage unchanged"), NASA FIRMS (first-load data-cessation notice + greyed-out layer rows), ASMC ("2019 onwards NOAA-20; 2013–2018 Suomi-NPP"), GWIS (period slider auto-clamps to each sensor's record).
- **Screenshots:** [SiPongi transition notice](img/sipongi/01-homepage-information-section.png) · [FIRMS S-NPP cessation row](img/nasa-firms/01-first-screen-default-view.png)
- **Verdict:** inherit
- **Serves:** scientist, land manager
- **Why:** Three national-scale authorities independently prove users need the sensor record's breaks stated where the data lives — IGNIS states the Overlap Period (2012 onward) and what the Harmonized Hotspot Count did about it, as a dated banner plus an about/method explanation, not silence.

### English + Bahasa Indonesia + Bahasa Malaysia from day one, Iban next
- **Sources:** SiPongi+ (full ID/EN toggle translating every string), Global Nature Watch ex-GFW (six languages including Bahasa Indonesia), APIMS (BM advisory PDFs); NASA FIRMS, ASMC and GWIS as the **avoid** cases (English-only despite Borneo audiences).
- **Screenshots:** none (no screenshot of a language switcher was captured).
- **Verdict:** adapt — the one-click full-string-table toggle is inherited from SiPongi+ as-is; the named change is that no audited app ships this particular combination, so EN + ID + MS in one string table is IGNIS's own scope decision.
- **Serves:** all three users plus the haze-impact audience
- **Why:** The Coverage Area spans Bahasa Indonesia-speaking Kalimantan (including the source-side of the haze-impact audience this library defines) and Bahasa Malaysia-speaking Sarawak, Sabah and Brunei, SiPongi+ proves a complete bilingual toggle is cheap, and every English-only predecessor is a demonstrated gap.
- **Iban (team decision, not audit evidence):** Iban is the language of Sarawak's largest ethnic group, and many longhouse and rural communities sit closest to recurring burning, so it reaches the land managers and residents the Malay locales miss. No audited app ships Iban, and terms like Hotspot, Harmonized Hotspot Count and Burning Phase have no settled Iban wording, so the strings need a native-speaker reviewer. Plan the string table for a fourth locale from the start; ship Iban at launch only if that reviewer signs off, otherwise as the first post-launch locale.
