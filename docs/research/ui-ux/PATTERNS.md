# IGNIS UI/UX Pattern Library

Synthesized from all 17 audits in this folder — the 13 core reference apps of [the research plan](../UI-UX-RESEARCH-PLAN.md) plus the 4 Borneo supplement apps of [the supplement brief](../UI-UX-BORNEO-SUPPLEMENT.md), each audited 2026-11-14; see [README.md](README.md) for the index and takeaways. Supplement-informed entries carry the brief's B1–B4 items: tri-country admin-boundary hierarchies (B1), cross-border region comparison (B2), tri-lingual handling (B3 — folded into the language pattern) and cross-source count attribution (B4). IGNIS domain terms follow [../../../GLOSSARY.md](../../../GLOSSARY.md) exactly: Hotspot, Harmonized Hotspot Count, Burning Calendar, Typical Year, Burning Phase, Overlap Period, Coverage Area, Area of Interest. The four audience labels come from section 1 of the research plan, not the glossary; **haze-impact audience** is defined here as *everyone in the Coverage Area exposed to haze — both downwind (Sarawak/Kuching) and source-side (Kalimantan, breathing the smoke where it starts)*, and is a candidate addition to GLOSSARY.md. Where this library specifies numbers (Burning Phase cutoffs, Typical Year statistics, performance budget, record scope), it draws on the repo's own [harmonization analysis](../harmonization-analysis.md) and [ADR 0001](../../../docs/adr/0001-viirs-equivalent-scaling.md).

Each pattern names its source app(s), links a screenshot when one exists under `img/`, carries one verdict — **inherit** (take as-is), **adapt** (take with the named changes), **avoid** (a demonstrated failure) — and names the user it serves: first responder, scientist, land manager, or the haze-impact audience. Where source apps disagree, the entry says which approach to take.

## Ground rules

Cross-cutting decisions that every pattern below assumes. They live here so they are stated once, not re-invented per view.

- **Performance budget.** First useful answer in ≤ 3 s and ≤ ~1 MB transferred, with the Burning Calendar grid server-rendered in the first HTML paint. Basis: the audits' own measurements — FIRMS (3.5 s / 0.5 MB) and SiPongi+ (~2.8 s / 87 resources) scored 2/2/2 and were marked inherit, while GNW ex-GFW (12.5 s / 2 MB), ASMC (~18 s / 2.4 MB) and Worldview (15.6 s / 6.5 MB) were marked avoid for exactly this. A first responder on mobile data in rural Borneo is the design case.
- **Linked-views contract (both directions).** (1) Clicking a Burning Calendar cell, or a day in the recent-days strip, filters the heatmap to that period in the current Area of Interest. (2) Selecting an Area of Interest on the heatmap (preset click or drawn shape), or scrubbing a date there, recomputes the Burning Calendar for that Area of Interest and highlights the period. (3) Both views share one URL state, so the compare picker, calendar and heatmap never disagree. Evidence: GFW verified date-range → widgets and Area of Interest → panel linkage, Watch Duty links list ↔ map both ways, SiPongi+ refetches the map live from filters; GWIS and ASMC are the disconnected failure mode. No audited app links a calendar to a map in both directions — that link is IGNIS's own build, specified here.
- **Record scope.** The Burning Calendar shows **2002–present**: 2002–2011 are harmonized MODIS months (VIIRS-equivalent, ±12% uncertainty, labelled as estimates), 2012–present are observed VIIRS months, per the [harmonization formula](../harmonization-analysis.md) — H(y,m) = k(m) × M(y,m) for MODIS-only months. "No data" means only what is outside that span (or a month FIRMS has no rows for); zero Hotspots is a real value, not a gap.

---

## Burning Calendar

### Year-by-month grid under a Typical Year
- **Sources:** GWIS (fire-season month×year heatmap), D3 calendar notebooks (week-aligned year rows), GitHub contribution graph (year strip).
- **Screenshots:** [GWIS month×year grid](img/gwis/04-country-charts-multiyear-kalimantan-barat.png) · [D3 year rows](img/d3-calendar/01-d3-calendar-overview-weekdays-only.png) · [GitHub grid](img/github-contrib-graph/01-first-screen-calendar-heatmap.png)
- **Verdict:** adapt
- **Serves:** land manager, scientist
- **Why:** Rows of years on a shared month axis make the burning season and anomalous years readable with zero interaction — the direct ancestor of the Burning Calendar's year-by-month grid of Harmonized Hotspot Counts — and the grid should ship server-rendered in the first HTML paint the way GitHub's does, so no control stands between the user and the first answer.

### Pre-aggregated historical envelope band
- **Sources:** Global Nature Watch ex-GFW (shaded "Normal Range" band + Above/Below markers), GWIS (min–max + 10–90th percentile envelopes + average), Climate Reanalyzer (all-years gray mass + 2 highlight colors), Nusantara Atlas (per-land-unit dashboards: worst year, least-affected year, average and current).
- **Screenshots:** [GNW Normal Range band](img/global-forest-watch/03-dashboard-weekly-fire-alerts-vs-normal-range.png) · [GWIS envelope vs chosen year](img/gwis/05-charts-2023-vs-historical.png) · [Climate Reanalyzer 90-series overlay](img/climate-stripes/02-t2-daily-default-all-years.png)
- **Verdict:** adapt
- **Serves:** all three users
- **Why:** Shading the Typical Year's expected range and marking above/below cells answers "is this year unusual?" without any math.
- **Where apps disagree:** GNW/GWIS pre-aggregate the band and stay fast, while Climate Reanalyzer's 90 live per-year series repeatedly stalled the main thread 8–30 s — take the pre-aggregated band (computed server-side from the whole archive), keep at most two highlighted years, and never ship one live series per year. Among the band statistics the sources ship, **take GWIS's 10–90th percentile band and drop min–max**: over a 25-year Borneo record the min–max span reaches from a near-zero drought-free year to a severe El Niño year and swamps the band.
- **Typical Year parameters (specified here, once):** the Typical Year is the **median** Harmonized Hotspot Count for each calendar month over the **full harmonized record, 2002–present** (per the Ground rules' record scope), with the 10–90th percentile of the same distribution as its envelope. Median, not mean, because the severe El Niño years the harmonization doc calls out (2002, 2006, 2009, 2015, 2019) would drag a mean above what any normal year looks like. Pre-2012 months entering this average are the ±12% harmonized estimates; show that uncertainty on the band's pre-2012 portion, exactly as the [harmonization analysis](../harmonization-analysis.md) prescribes for the calendar. If the architect later prefers an observed-only baseline, the fallback is 2012–present — but then say so on the chart, GWIS-style, in the subtitle. **Scope caveat, stated not hidden:** the harmonized record today splits the Indonesian side into provinces but holds Sarawak + Sabah + Brunei as one approximate region — every Hotspot north of 0.8°N outside an Indonesian province — so a Typical Year per Malaysian or Bruneian preset exists only after the boundary refit the analysis's own limitations section calls for; until then the MY/BN side renders one Typical Year at the approximate-region scope and says so in the chart subtitle, GWIS-style.

### First-class any-two-year compare — one control, two projections
- **Sources:** GitHub (year links that swap the grid, each a shareable URL), NASA Worldview (A\|B compare with an independent date per side), Global Nature Watch ex-GFW and ASMC (manual year re-picking), Climate Reanalyzer (per-series toggles that failed in practice).
- **Screenshots:** [GitHub year swap](img/github-contrib-graph/03-year-navigation-2023.png) · [Worldview A\|B 2023 vs 2019](img/nasa-worldview/04-task3-ab-compare-2023-vs-2019.png)
- **Verdict:** adapt
- **Serves:** scientist, land manager
- **Why:** "Is 2023 worse than 2019?" is a core IGNIS question and every audited app makes it expensive — GFW needed ~18 manual interactions, ASMC 5 clicks per year, GitHub holds one year in memory, and Climate Reanalyzer's year-pair toggles were covered by a sticky header and never landed.
- **Relationship to the heatmap's A\|B compare (specified once):** there is **one** two-year picker, and it drives **both** projections — the Burning Calendar highlights those two year rows against the Typical Year envelope, and the heatmap's swipe/side-by-side mode binds year A to side A and year B to side B (see *A\|B compare modes with an independent date per side*). Setting years in either view updates the same shared URL state, so the calendar and the map can never show different year pairs. Do not build two compare systems.

### Burning Phase encoding — the single source of truth
- **Sources:** GitHub (5-step single-hue ramp + distinct empty color), D3 calendar (`@d3/calendar/2` outlier-capped domain; pinned domain across views), Windy (verbal tiers "Very low → Extreme" over a green→red ramp), APIMS (ranges printed on every tier card; shape-per-tier encoding), GWIS (threshold legend table with numeric cutoffs), NEA haze portal (four PSI bands, each carrying range + descriptor + action — a national portal shipping exactly four tiers).
- **Screenshots:** [GitHub 5-step ramp](img/github-contrib-graph/01-first-screen-calendar-heatmap.png) · [Windy verbal-tier legend](img/windy/02-fire-danger-layer-pontianak.png) · [APIMS tier cards with ranges](img/apims-iqair/01-apims-dashboard-tier-cards.png)
- **Verdict:** adapt — the ramp, verbal-tier and printed-threshold mechanics are inherited; the four-tier mapping below is IGNIS's own and no source ships it.
- **Serves:** all three users plus the haze-impact audience
- **Why:** One quantized scale that every calendar cell, tier card and legend shares, so a color always means the same thing.
- **The encoding (this entry is the specification; every other pattern defers to it):**
    - **Four tiers, not five or six.** GLOSSARY.md fixes the labels — Peak burning, Active burning, Moderate, Low — and they supersede the sources' counts: GitHub's fifth visual step is repurposed as the separate **no-data** color (a month with no record is not a Low month), and APIMS's six cards and Windy's six verbal tiers contribute the *mechanisms* (printed ranges, words on the legend), not the tier count.
    - **Basis: each month's share of the Typical Year's annual Harmonized Hotspot Count** (the glossary's own definition of Burning Phase), computed **per Area of Interest** — so a Kalimantan province's Peak and Brunei's Peak each mean "this area's biggest month," which absolute counts could never make comparable. Because the basis is a share, the same numeric cutoffs apply to every Area of Interest: pinned globally, fair locally.
    - **Proposed cutoffs:** Low < 3%, Moderate 3–10%, Active burning 10–25%, Peak burning ≥ 25% of the Typical Year's annual total. Sanity check on the only full monthly series in the audits (SiPongi national MODIS 2019: Sep 56.7%, Oct 15.5%, Aug 12.6%, Nov 7.0% of the annual total) → Sep Peak, Aug+Oct Active, Nov Moderate, rest Low — the intended reading. These numbers are proposals: the architect tunes them when the Borneo-wide data the [harmonization analysis](../harmonization-analysis.md) says is still to be refit arrives, and prints whatever is final next to the colors (APIMS/GWIS discipline). One collision is already documented and must be tuned away: the Malaysian/Bruneian side has no sharp season — March to September each carry 7–19% of that region's annual total, where West Kalimantan concentrates 70% in August–September — so a global ≥ 25% Peak cutoff would classify no MY/BN month as Peak burning and the *Quiet-state vs Peak-state home* would never escalate for Sarawak, Sabah or Brunei users. The resolution is the architect's at refit time — scope-adjusted cutoffs per record scope, or a different escalation trigger for the home — with whichever is chosen printed next to the colors.
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
- **Sources:** Sentinel Hub EO Browser → Copernicus Browser (the successor **dropped** EO Browser's per-day availability timeline), NASA FIRMS (greyed-out layer row "DATA ONLY AVAILABLE - 2015-11-24 TO 2026-11-02"), D3 calendar (TWO-N keeps month labels over empty months), BMKG (**avoid:** fixed image filenames overwritten daily — yesterday's map is simply gone, so any past question is structurally unanswerable).
- **Screenshots:** [Copernicus plain calendar, no marks](img/sentinel-hub/04-date-picker-calendar-sept2026.png) · [FIRMS S-NPP availability row](img/nasa-firms/01-first-screen-default-view.png) · [TWO-N labeled empty months](img/d3-calendar/08-two-n-calendar-mode-holdtime.png)
- **Verdict:** adapt
- **Serves:** scientist
- **Why:** EO Browser's sunset proves availability marks are the first thing a successor loses, and without them users pick blind dates and wait — so every Burning Calendar cell must visibly distinguish three states: zero Hotspots (a real value), no data (only months outside the 2002–present record, per the Ground rules), and **harmonized estimates** — the 2002–2011 cells carry the ±12% uncertainty band and an "estimate" label the [harmonization analysis](../harmonization-analysis.md) itself prescribes, so users can tell converted months from observed ones across the 2012 Overlap Period boundary.

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
- **Why:** A monthly-default Burning Calendar cannot answer "is it burning now," so a strip of the last 10–15 days as day cells — colored by the Burning Phase encoding's continuous scale, count in the cell, one click to filter the heatmap to that day (per the Ground-rules linkage contract) — gives the responder their daily surface without leaving the calendar view. The cells carry **observed per-sensor Hotspot counts** (for example VIIRS 375 m detections in the last 24 hours), not the Harmonized Hotspot Count — harmonization is fitted monthly (H(y,m) = k(m) × M(y,m)), so no harmonized daily number exists to show, and the strip's colors come from the Burning Phase encoding's continuous outlier-capped scale applied to daily counts.

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
- **Sources:** NASA FIRMS (last-24-h Hotspots drawn on load), Watch Duty (map + freshness-ranked incident list at zero clicks), Windy (full-screen map, instant answer), ASMC (map-first home), Nusantara Atlas (one map extent spanning Indonesia + Malaysian Borneo + Brunei — confirmed from its About page, not Indonesia-only).
- **Screenshots:** [FIRMS default load](img/nasa-firms/01-first-screen-default-view.png) · [Watch Duty first screen](img/watch-duty/01-first-screen-map-and-incident-list.png) · [ASMC home map](img/asmc/01-home-regional-haze-situation-map.png) · [BMKG's unlabeled ASEAN map](img/bmkg-fire-potential/09-asean-ffmc-obs-cross-border.png) (the labeling cautionary)
- **Verdict:** adapt — the map-first shell is taken as the sources ship it; the named changes are IGNIS's own: open on the Borneo Coverage Area (not FIRMS's whole-globe default that forced every task to start with search-and-zoom), with all three countries labeled and equally treated — not BMKG's ASEAN FFMC map, which colors Sarawak, Sabah and Brunei but labels none of them ([bmkg-fire-potential.md](bmkg-fire-potential.md) B2), and not NEA's hotspot canvas, which opens facing Myanmar with Borneo off-screen ([nea-haze-portal.md](nea-haze-portal.md) #4) — and keep the Burning Calendar beside the map per the Ground-rules linkage contract, not behind a tab.
- **Serves:** first responder
- **Why:** Every responder-grade reference lands map-first with live data already drawn, and the first screen must obey the Ground-rules performance budget — ≤ 3 s / ≤ 1 MB — that FIRMS (0.5 MB) meets and GNW/ASMC/Worldview fail.

### Cadence-matched time presets, season-to-date included
- **Sources:** Nusantara Atlas (Today / Last 2 / 7 / 14 Days for the daily Hotspot feed; Last Month / 3 / 6 / 12 Months for monthly burn scars — "timeframes adapted to each indicator"), GWIS (Last 1 / 7 / 30 Days plus "Fire Season: from 01/01 to today"), SiPongi+ (12/24/48 Jam chips), NASA FIRMS (TODAY/24HRS/7DAYS), BNPB (Pantauan map defaults to the last 7 days).
- **Screenshots:** [GWIS presets panel](img/gwis/06-current-situation-fire-danger.png)
- **Verdict:** adapt
- **Serves:** first responder, land manager
- **Why:** One preset row per cadence — daily-Hotspot browsing for "is it burning now" and Burning-Calendar months for "when does it burn" — beats a single generic date picker, and GWIS's season-to-date preset is the land manager's default window that no other audited app ships.

### Now-view vs record-view toggle with question-named titles
- **Sources:** NEA haze portal (the 24-hr PSI \| 1-hr PM2.5 tab pair swaps the chart *and* the section's question — "Current Air Quality" vs "Air Quality (Past 24 hours)"), Copernicus Browser (Single Date / Mosaic / Time Range segmented control).
- **Screenshots:** [NEA dual-index tabs](img/nea-haze-portal/01-landing-air-quality-5-region-map.png)
- **Verdict:** adapt
- **Serves:** first responder (now), scientist and land manager (record)
- **Why:** One map, two named questions — "Is it burning now?" (latest Hotspots plus the recent-days strip) and "How does this season compare?" (Burning Calendar plus Typical Year envelope) — each side titled for the question it answers, both projections sharing the Ground-rules URL state. The toggle is also the honest boundary between the two data products: the now side renders observed per-sensor Hotspots (latest detections, age ramp, raw layers), the record side renders the monthly Harmonized Hotspot Count — no harmonized daily number exists to blur that line (see *Recent-days strip*).

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

### Zoom-dependent Hotspot rendering: density, cluster, point
- **Sources:** ASMC (uniform red dots at every zoom — cluttered at region zoom; a separate Hotspot Density Map page renders a Google heatmap with a Low→High gradient legend, and its audit's own verdict is "one heatmap with a display toggle rather than two pages"), BNPB (Leaflet marker-cluster layer — the only clustering observed in all 17 audits), SiPongi+ (confidence-colored points on a fast canvas layer, same style at every zoom), NASA FIRMS (flat square points on one merged layer; a "GRIDDED FIRE HOTSPOTS" product exists only in the catalog, never in the map UI), Windy (**avoid:** tiny canvas dots, near-invisible at country zoom), NEA (**avoid:** uniform red dots on a pan-only canvas with no zoom at all).
- **Screenshots:** [ASMC density map page](img/asmc/08-hotspot-density-map.png) · [ASMC cluttered dots at region zoom](img/asmc/03-zoomed-west-kalimantan.png) · [NEA pan-only dot canvas](img/nea-haze-portal/02-hotspot-section-canvas-legend.png)
- **Verdict:** adapt — each mechanism was observed working somewhere; the zoom ladder composing them is IGNIS's own, because no audited app changes rendering by zoom.
- **Serves:** first responder, land manager
- **Why:** IGNIS's heatmap view is named for the density surface, and the audits show why: points at Coverage-Area zoom are clutter (ASMC) or invisible (Windy), while per-point detail is exactly right at settlement zoom. **The rendering ladder (specified once):** (1) Coverage-Area and province zoom — a pre-aggregated density surface of Hotspots, colored by the Burning Phase encoding's continuous outlier-capped scale and computed server-side so it meets the Ground-rules performance budget (ASMC's density page is the ancestor; keep it one view with a points/density display toggle, that audit's own prescription); (2) district zoom — clustered counts, BNPB-style, with the count in the cluster badge; (3) settlement zoom and finer — individual Hotspot points carrying the age ramp and the place-chain popup. **Where apps disagree:** every app ships exactly one rendering (ASMC dots, BNPB clusters, FIRMS points) — take the ladder, and never a single merged point style at every zoom (the shared FIRMS/ASMC/NEA failure).

### Sensor-explicit layers with capability one-liners and freshness stamps
- **Sources:** Watch Duty ("VIIRS: Detects large and small fires, including cooler ones"; per-layer "Recent: 24 Hours Ago"), NASA Worldview ("Fires and Thermal Anomalies (Day and Night, 375m) Suomi NPP / VIIRS"), NASA FIRMS ("VIIRS (NOAA-20 & NOAA-21) [375m]"), Windy (source chips "ECMWF 9km / GFS 22km").
- **Screenshots:** [Watch Duty sensor cards](img/watch-duty/03-satellite-hotspots-layer-options.png) · [Worldview fire layers](img/nasa-worldview/02-task1-west-kalimantan-sep2026-fire-layers.png)
- **Verdict:** inherit
- **Serves:** all three users
- **Why:** One plain sentence per layer saying what a sensor can and cannot detect, plus its resolution and data age on the toggle itself, lets a non-scientist choose MODIS vs VIIRS vs the Harmonized Hotspot Count without knowing the instruments — the best sensor communication in the whole audit set.

### Per-sensor counts beside the Harmonized Hotspot Count
- **Sources:** SiPongi+ (per-satellite low/medium/high count strip, never merged), Global Nature Watch ex-GFW (high-confidence split beside every total), GWIS (MODIS and VIIRS chart pairs on a common 2012–2025 baseline), GitHub (one count in the cell, per-source breakdown one click down), Nusantara Atlas (published year comparisons "use the same satellites in both years, avoiding an artificial increase caused by adding sensors").
- **Screenshots:** [SiPongi per-satellite counts](img/sipongi/02-peta-province-picker-overlay.png) · [GWIS sensor-paired charts](img/gwis/07-seasonal-trend-indonesia.png)
- **Verdict:** adapt
- **Serves:** scientist
- **Why:** IGNIS's headline number is the Harmonized Hotspot Count, but scientists must see the raw MODIS and VIIRS counts beside it to know what harmonization did. **Where apps disagree:** SiPongi and Watch Duty never merge (honest but leaves no comparable series), FIRMS merges with no per-sensor toggles at all, and GitHub's shape is the one to take — one harmonized number in the cell, per-sensor breakdown one click down. Nusantara Atlas adds the rule the count implies: any trend spanning the Overlap Period must say which sensor set produced it (see *Same-satellite discipline and the why-our-count-differs bridge*). All of it assembles into one renderable unit: *The Harmonized Hotspot Count block*.

### Place-chain Hotspot popup
- **Sources:** SiPongi+ (village → district → regency → province chain, satellite, confidence, lat/lon, timestamp).
- **Screenshots:** [SiPongi Hotspot popup](img/sipongi/08-hotspot-popup-village-detail.png)
- **Verdict:** adapt — the mechanism is inherited; the chain must be **per-country**, because SiPongi's desa → kecamatan → kabupaten → provinsi hierarchy is Indonesia's and the Coverage Area also spans Malaysia and Brunei: Sarawak/Sabah need division → district → sub-district/kampung, Brunei needs district → mukim. That admin-boundary GIS for all three countries is a named data dependency (GNW ex-GFW's "Political boundaries" preset layer is the audited proof such data exists as a product). Store the chain as official codes, not bare names — BNPB's Kemendagri ids (`id_prov` 62 / `id_kab` 6207 on every incident record) are the audited proof that codes keep joins stable across splits and renames ([bnpb-disaster-geoportal.md](bnpb-disaster-geoportal.md) B1).
- **Serves:** first responder
- **Why:** A click on a Hotspot that names the full local place chain is what a responder in Borneo actually dispatches to — the per-point detail FIRMS's merged canvas notably failed to deliver in four verified click attempts.

### One tabbed context-overlay panel
- **Sources:** SiPongi+ (Hotspot/Overlays/FDRS tabs: cloud, wind, air quality, rain, fire-danger indices), ASMC (2500 ft winds, rainfall, satellite image toggles), IQAir ("Fires", "Wind", "Air quality stations" side by side), BMKG (each FDRS index browsable as an obs → H+0–H+7 forecast ladder per area), Nusantara Atlas (concession, peatland and land-use layers explaining where Hotspots recur), BNPB (layer tree grouped Peta Bahaya / Peta Kerentanan / Peta Risiko — hazard → vulnerability → risk).
- **Screenshots:** [ASMC Haze Portal overlays](img/asmc/10-haze-information-portal.png) · [SiPongi layer panel](img/sipongi/03-peta-layer-panel-province-filter.png) · [IQAir fires + wind controls](img/apims-iqair/09-iqair-map-legend-fires-wind-controls.png) · [BMKG forecast ladder](img/bmkg-fire-potential/05-ffmc-forecast-next-day.png)
- **Verdict:** adapt
- **Serves:** first responder, scientist
- **Why:** Optional meteorological context (wind, rain, haze) in one tabbed panel keeps the heatmap uncluttered while making Hotspots legible as smoke transport — but no layer may swallow clicks aimed at the panel beneath it, the bug that broke SiPongi's own map drill-down. Organize the tabs along BNPB's hazard → vulnerability → risk ladder (Hotspots = detection; peat and land use = why it recurs; population = who it reaches) and let the FDRS tab browse BMKG-style forecast days, so the panel answers "where might it catch next week" as well as "what is burning now". One honesty mark: the audited FDRS feeds stop at Indonesia (SiPongi+'s tabs, BMKG's provincial ladder) or ship as a static daily image with no archive (BMKG's ASEAN map — the only audited FDRS product spanning Sarawak/Sabah/Brunei); a machine-readable FDRS feed covering MY/BN is a registered open dependency (end of this file), until which the forecast tab is Indonesia-side plus the dated BMKG ASEAN image, labeled as such.

### Mobile-first shell with bottom-sheet drawers
- **Sources:** Watch Duty (at 390 px only map + floating buttons remain; search/list as modal sheets; one drawer component reused on desktop; **avoid** ASMC's squeezed desktop layout and Windy's clipped timeline at the same width).
- **Screenshots:** [Watch Duty phone layout](img/watch-duty/05-mobile-first-screen.png) · [Watch Duty modal search](img/watch-duty/06-mobile-search-list-modal.png) · [ASMC squeezed layout](img/asmc/09-mobile-390px-home.png)
- **Verdict:** adapt — the sheet-and-drawer mechanism is taken as Watch Duty ships it; the named change is IGNIS's own: the Burning Calendar becomes one more drawer in that system (see below), which no source ships.
- **Serves:** first responder
- **Why:** The strongest phone layout in the audit set — everything collapses into modal sheets and bottom drawers over the map — and the only one that was actually verified at 390 px rather than squeezed.
- **Where the Burning Calendar lives on a phone (specified, so this pattern and the map-first landing cannot conflict):** at 390 px the calendar is a bottom-sheet drawer opened from a persistent Calendar button in the floating stack, with the recent-days strip kept visible above the map's timeline so the responder's daily surface survives without opening the drawer.

### Full state in the shareable URL
- **Sources:** NASA FIRMS (`#d:2026-09-01..2026-09-30;@111.12,-0.09,10.00z`), NASA Worldview (extent, layers, date, compare flag), Windy (`?fwi,-0.704,109.345,8,p:firespots` — round-trip verified), Watch Duty (`/@lat,lng,z/pin?search=…`), Copernicus Browser (every control serialized), GitHub (year windows as `from=/to=`), BNPB (map filter state as GET params: `startDate`, `endDate`, `provinsi`).
- **Screenshots:** [FIRMS SHARE dialog](img/nasa-firms/04-share-url-state.png)
- **Verdict:** inherit
- **Serves:** all three users
- **Why:** Seven independent apps converged on the same mechanic — Area of Interest, Burning Calendar month/year selection and heatmap state in the address bar — because it makes every answer a responder builds linkable to their team with no server work.

### Export beside the data, filename encoding the state
- **Sources:** SiPongi+ (XLSX / TXT / KMZ one-click menu on the table), NASA FIRMS (screenshot export whose filename reconstructs the view), Climate Reanalyzer (one menu: PNG/JPEG/PDF/SVG/print + raw JSON), GitHub (**gap:** no export at all), BMKG (every product PNG embeds its own bilingual legend, validity timestamp, producer and data sources; the attribution rule "Wajib mencantumkan BMKG sebagai sumber" sits on the page beside the images it governs; a daily narrative factsheet ships as PDF).
- **Screenshots:** [SiPongi export menu](img/sipongi/06-sebaran-table-export-xlsx-txt-kmz.png) · [BMKG self-describing hotspot image](img/bmkg-fire-potential/07-hotspot-static-image-product.png)
- **Verdict:** adapt
- **Serves:** scientist, land manager
- **Why:** Export controls belong next to the data they export — a CSV of the visible Harmonized Hotspot Count series and an image whose filename carries the Area of Interest and date range, not a separate download portal like FIRMS's archived-data flow. Every exported image must also be self-describing BMKG-style — legend, Harmonized Hotspot Count definition and source baked into the PNG so the export survives being reshared into a chat group — with the citation line beside the export button, not in a footer.

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

### Quiet-state vs Peak-state home
- **Sources:** NEA haze portal (quiet state leads with bands and a guide; the episode state inverts the first screen to a "Haze Situation Update" — forecast band in words, three-audience advisory, embedded hotspot map), ASMC (Alert Level 0 banner that also states the data's update cadence), BMKG (early-warning banner carousel on the homepage).
- **Screenshots:** [NEA quiet-state landing](img/nea-haze-portal/01-landing-air-quality-5-region-map.png)
- **Verdict:** adapt
- **Serves:** first responder, haze-impact audience
- **Why:** The same app should compose itself by Burning Phase — quiet months lead with the Typical Year and Burning Calendar, and when the current month turns Peak burning in the selected Area of Interest the heatmap, recent-days strip and haze-impact health action promote to the top — one site that reorganizes itself, not a separate emergency portal. The escalation trigger is the Burning Phase encoding's Peak tier, so the *Burning Phase encoding* cutoff caveat governs this pattern too: before the harmonization refit, the MY/BN side may classify no month as Peak under the proposed global cutoff, and the escalation rule for that scope is part of the same architect decision.

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
- **Sources:** IQAir (one number + tier + dominant pollutant + "1.4× the WHO guideline" + tier-specific actions), ASMC (daily prose narrative translating Hotspots into haze and air quality under the map), APIMS (dated "Transboundary Haze" references and a Malay advisory), NEA haze portal (source→downwind causal narrative — "dense smoke haze from fires in Kalimantan … under prevailing southeasterly winds" — always ending in a health action split by audience: "Healthy persons – REDUCE…" / "Vulnerable persons – AVOID…"), BMKG (daily one-page factsheet PDF: yesterday's counts, trend words per priority province, per-island risk outlook).
- **Screenshots:** [IQAir Kuching dashboard](img/apims-iqair/07-iqair-kuching-dashboard-aqi39-good.png) · [ASMC narrative under map](img/asmc/01-home-regional-haze-situation-map.png) · [NEA four-band action guide](img/nea-haze-portal/03-health-advisory-4-band-guide.png)
- **Verdict:** adapt
- **Serves:** haze-impact audience, first responder
- **Why:** Pairing the current air-quality tier and a health action with the Harmonized Hotspot Count and a Typical Year anchor ("3× a Typical March") is what makes burning in the Coverage Area legible as haze — IGNIS's clearest differentiator for the audience no fire app in this audit serves directly. NEA supplies the sentence template IGNIS should generate per Area of Interest — source, transport wind, local tier, one action — and the healthy-vs-vulnerable audience split the Burning Phase tier cards should carry.
- **Data dependency, stated honestly:** no audited source exposes a free, downloadable Sarawak/Kuching air-quality feed — APIMS's pages are authoritative but static (no export, state not in the URL), IQAir shows the data but publishes no public CSV, and ASMC's WIS2 catalog link covers Hotspot coordinates, not AQ. Candidates for IGNIS: APIMS/MyEQMS as the authoritative Malaysian feed, IQAir as the design-and-possibly-API partner, ASMC's haze portal for regional context. Which feed ships — and on what terms — is an **open dependency for the architect**; until it is settled, the panel degrades to linking out (IQAir city page / APIMS tab) rather than fabricating a tier.

### Ranked Areas-of-Interest table
- **Sources:** GWIS (ranked table: area, historical average, current year, in absolute and %), Global Nature Watch ex-GFW ("regions with the most fire alerts"), IQAir (live city ranking), Nusantara Atlas (FireWatch "most affected provinces" rankings plus Alerts Tracker lists of concessions, protected areas and jurisdictions whose View button zooms the map and overlays its alerts for verification against imagery).
- **Screenshots:** [GWIS ranked comparison table](img/gwis/08-estimates-country-comparison.png)
- **Verdict:** adapt
- **Serves:** land manager
- **Why:** A ranked list of provinces or districts inside the Coverage Area — current Harmonized Hotspot Count against each one's Typical Year — makes cross-place comparison instant where map gazing is not, and each row should act like Nusantara's land-unit lists: one click zooms the heatmap to that Area of Interest and shows its Hotspots for the selected period.

### Tri-country coded Areas of Interest at mixed depths (B1)
- **Sources:** BNPB (every incident carries Kemendagri codes `id_prov`/`id_kab` beside names; **avoid** its casing-duplicate province dropdown listing every Kalimantan province twice), SiPongi+ (surfaced Desa → Kecamatan → Kabupaten → Provinsi chain), BMKG (searchable 42-preset ladder: 34 provinces including all five Kalimantan, plus Sumatera / Kalimantan / Indonesia / ASEAN rollups), ASMC (flattened tri-country chart presets: Kalimantan, Sabah & Sarawak, Brunei, …), Nusantara Atlas (one depth — "down to municipalities" — across Indonesia, Malaysian Borneo and Brunei alike), GWIS (province list predating the 2012 Kalimantan Utara split — the stale-boundary pitfall).
- **Screenshots:** [BMKG searchable area box](img/bmkg-fire-potential/03-ffmc-page-legend-and-warning.png)
- **Verdict:** adapt
- **Serves:** land manager, scientist
- **Why:** One picker must span Provinsi/Kabupaten (Indonesia), Sarawak divisions and Sabah districts (Malaysia) and Brunei daerah at their real, unequal depths — so select and store official codes (BNPB's model, which survives splits and renames like Kalimantan Utara in 2012), surface each country's own level names in its own locale (SiPongi+), and top the ladder with a whole-Coverage-Area rollup (BMKG's ASEAN map proves the data spans all three countries). The audited code evidence is Indonesia-only — Kemendagri ids are the sole official code system any audit touched, and no source names Malaysia's or Brunei's equivalents — so which code IGNIS stores for MY/BN areas is a registered open dependency (end of this file), with Kemendagri as the proof of concept, not the tri-country rule. **Where apps disagree:** SiPongi+ surfaces the full chain while ASMC and Nusantara Atlas flatten to one level — take the coded chain where deep boundary GIS exists (Indonesia), named single-depth presets where it does not yet (Sarawak/Sabah/Brunei), and never a bare-name dropdown (BNPB's "Kalimantan Barat"/"KALIMANTAN BARAT" duplicate is the trap in miniature).

### Cross-border comparison with equal country standing (B2)
- **Sources:** ASMC (Select Regions chart checkboxes — Sumatra, Kalimantan, Sabah & Sarawak, Brunei… as multiple series in one monthly chart; the only audited control that puts both sides of the border in a single view, though only from fixed presets and only in charts), GWIS (ranked region table on one common axis — area, historical average, current year, in absolute and % — plus per-province bars within a country), NEA haze portal (foreign-baseline framing — the daily narrative names "fires in Kalimantan" and the transport wind behind the local PSI band, but no foreign region is ever selectable and Sarawak appears only as words), BMKG (**avoid:** the ASEAN FFMC map colors Sarawak, Sabah and Brunei unlabeled under Indonesian national branding, and the Kalimantan island map draws the whole of Borneo but greys out the non-Indonesian side), Nusantara Atlas (**avoid:** whole-island map extent with every analytic tool stopping at Indonesia — depth asymmetry left implicit), BNPB (**avoid:** strictly 34 provinces, nothing outside Indonesia — the national-only shell).
- **Screenshots:** [ASMC multi-region chart](img/asmc/04-monthly-hotspot-count-2026.png) · [GWIS ranked comparison table](img/gwis/08-estimates-country-comparison.png) · [BMKG unlabeled ASEAN map](img/bmkg-fire-potential/09-asean-ffmc-obs-cross-border.png) · [NEA prose-only neighbours](img/nea-haze-portal/02-hotspot-section-canvas-legend.png)
- **Verdict:** adapt — the mechanism is inherited: ASMC's multi-select region series on one shared month axis, plus GWIS's ranked common-axis table, are the two audited components that already compare regions; IGNIS's changes are freeing them from fixed presets, baselining each series against its own Typical Year, and labeling every country.
- **Serves:** land manager, scientist, haze-impact audience
- **Why:** "West Kalimantan vs Sarawak, same season" is supported by no audited app, but the parts exist. **The buildable mechanism (specified once):** (1) the *Ranked Areas-of-Interest table* spans all three countries — a country column, sortable, each row stating its current Harmonized Hotspot Count against its own Typical Year (GWIS's table shape); (2) pinning any two Areas of Interest plots them as two series on the same monthly chart, each with its own Typical Year envelope band (ASMC's checkbox mechanism, freed from presets — a foreign baseline must be fair, not foreign); (3) the heatmap's existing *A\|B compare modes* extend to region-vs-region with a pinned Area of Interest per side at the same date — an IGNIS composition, specified here, of Worldview's per-side mechanic. Honesty rules that make the comparison equal: label every country (not BMKG's unlabeled neighbors), and state per-country data depth — until the harmonization refit, a pinned MY/BN preset compares as the one approximate Sarawak + Sabah + Brunei region, and the chart subtitle must say so (Nusantara's lesson: never let a Borneo-wide map imply Borneo-wide analytics).

### Scrollable, responsive dashboard
- **Sources:** APIMS (**avoid:** page height locked to the viewport, half its own content unreachable at 768p and 1080p, right side clipped at 1282 px, state filter invisible to the accessibility layer).
- **Screenshots:** [APIMS clipped laptop viewport](img/apims-iqair/05-apims-laptop-viewport-clipped.png)
- **Verdict:** avoid
- **Serves:** all three users
- **Why:** A dashboard that scrolls and reflows is not optional — APIMS's fixed-viewport layout physically hid its ranking, chart and references from real users, the single most consequential layout defect in the audit set.

---

## About / method

### Methodology one click from every number
- **Sources:** GitHub ("Learn how we count contributions" directly under the grid), Global Nature Watch ex-GFW (per-dataset metadata modal with citation + DOI + licence), NASA FIRMS (Layer Information modal: temporal coverage, latency, overpass times), GWIS (ⓘ per metric + envelope footnotes), Climate Reanalyzer (dataset + version + DOIs + license below the chart), Nusantara Atlas (citation-per-layer: a peer-reviewed source for every dataset — Schroeder et al. 2014 for VIIRS 375 m, Justice et al. 2002 for MODIS — on the About page).
- **Screenshots:** [GNW metadata modal](img/global-forest-watch/04-dataset-metadata-modal.png) · [GitHub grid with method link](img/github-contrib-graph/01-first-screen-calendar-heatmap.png)
- **Verdict:** inherit
- **Serves:** scientist
- **Why:** Every app trusted by scientists puts the method one click from the data — for IGNIS that means the Harmonized Hotspot Count definition and the Overlap Period calibration linked under the grid and beside every headline number, not parked on an unvisited page.
- **IGNIS already has the target pages — link them:** the formula, its per-month factors and its ±12% error live in [docs/research/harmonization-analysis.md](../harmonization-analysis.md) and the decision behind it in [ADR 0001](../../../docs/adr/0001-viirs-equivalent-scaling.md); every "how is this counted?" affordance in the app should land on those (or an app-rendered summary of them), not on text yet to be written.

### The Harmonized Hotspot Count block: number, split, method, caveat as one unit
- **Sources:** GitHub (count in the heading, per-source breakdown one click down, "Learn how we count contributions" one line under the grid), SiPongi+ (per-satellite count strip beside the map), Global Nature Watch ex-GFW (sampling caveat directly under the numbers), Watch Duty (provenance banner on every update), Nusantara Atlas (same-satellites footnote on every published comparison).
- **Screenshots:** [GitHub grid with method link](img/github-contrib-graph/01-first-screen-calendar-heatmap.png) · [SiPongi per-satellite counts](img/sipongi/02-peta-province-picker-overlay.png)
- **Verdict:** adapt — every ingredient is inherited; assembling them into one reusable block is IGNIS's own.
- **Serves:** all three users plus the haze-impact audience
- **Why:** Four patterns in this library each mandate a slice of the same affordance — *Per-sensor counts beside the Harmonized Hotspot Count*, *Methodology one click from every number*, *Inline caveat under every chart*, *Same-satellite discipline and the why-our-count-differs bridge* — and a builder needs the unit they compose. Wherever a headline count renders (calendar-cell tooltip, region panel, ranked-table row, haze-impact panel), render one block: **[1]** the Harmonized Hotspot Count, large; **[2]** the per-sensor MODIS and VIIRS counts one click down; **[3]** the method link landing on the harmonization analysis / ADR 0001 summary; **[4]** the caveat line — ±12% and an "estimate" flag for harmonized 2002–2011 months, the same-satellites note on any multi-year trend, and links to the nearest official numbers (KLHK per-satellite counts, ASMC high-confidence charts, BPBD incidents, FIRMS) rather than reproductions of them.

### Inline caveat under every chart
- **Sources:** ASMC (same five-bullet caveat block under every map and chart), Global Nature Watch ex-GFW (sampling note under the numbers; "be cautious comparing before/after 2015"), Watch Duty (provenance on every update; "reporters are not actively monitoring this incident"), APIMS (averaging rule stated under the data).
- **Screenshots:** [Watch Duty provenance banner](img/watch-duty/02-incident-detail-updates.png)
- **Verdict:** inherit
- **Serves:** scientist
- **Why:** Never show a Hotspot count without its caveats in the same breath — cloud-cover misses, reprocessing, and the harmonization approximation are part of the number, and repeating the block on every view (ASMC's discipline) beats a single FAQ entry.

### Sensor-era honesty: transition notices and record-aware periods
- **Sources:** SiPongi+ (dated banner: NOAA-21 replaces retired SNPP, "coverage unchanged"), NASA FIRMS (first-load data-cessation notice + greyed-out layer rows), ASMC ("2019 onwards NOAA-20; 2013–2018 Suomi-NPP"), GWIS (period slider auto-clamps to each sensor's record), BMKG (**avoid:** page copy still names S-NPP while the daily hotspot image itself lists Terra, Aqua, NOAA20 and NOAA21 — copy drifting from the product with no notice).
- **Screenshots:** [SiPongi transition notice](img/sipongi/01-homepage-information-section.png) · [FIRMS S-NPP cessation row](img/nasa-firms/01-first-screen-default-view.png)
- **Verdict:** inherit
- **Serves:** scientist, land manager
- **Why:** Three national-scale authorities independently prove users need the sensor record's breaks stated where the data lives — IGNIS states the Overlap Period (2012 onward) and what the Harmonized Hotspot Count did about it, as a dated banner plus an about/method explanation, not silence.

### Same-satellite discipline and the why-our-count-differs bridge (B4)
- **Sources:** Nusantara Atlas (year comparisons "use the same satellites in both years, avoiding an artificial increase caused by adding sensors", plus a second consistent-sensor-since-2015 check and the standing line that Hotspots and burned area "measure different aspects"; uncertainty published as a range across official map vintages — 17–23% inside peat boundaries depending on the 2011 vs 2019 MoA maps), BMKG (two same-day official counts diverging by scope with no reconciliation note: the factsheet's 26 high-confidence national Hotspots vs the intraday image's 784 all-confidence — same sensors, both "official"), BNPB vs SiPongi+ (Aug-2026 Kaltim: 30 BNPB-reported karhutla *incidents* against thousands of satellite *Hotspots* for the same island — two official Indonesian numbers, neither site references the other), NEA haze portal (publishes no counts at all and delegates verbatim to ASMC rather than half-reproducing them).
- **Screenshots:** [BMKG in-image count table](img/bmkg-fire-potential/07-hotspot-static-image-product.png)
- **Verdict:** adapt
- **Serves:** scientist, land manager
- **Why:** The Harmonized Hotspot Count must explain itself wherever it appears: Nusantara's same-satellites footnote is the direct precedent (and part of the reason the count exists), while BMKG's divergent same-day counts and the BNPB-incident-vs-SiPongi-Hotspot gap are the "why we differ" worlds users actually meet — so IGNIS's method note defines the count against KLHK per-satellite counts, ASMC high-confidence charts, BPBD incident reports and FIRMS merged dots, and links out to those official numbers (NEA's delegation) instead of half-reproducing them. Assembled with the per-sensor split, method link and caveat line into one renderable unit by *The Harmonized Hotspot Count block*.

### English + Bahasa Indonesia + Bahasa Malaysia from day one, Iban next
- **Sources:** SiPongi+ (full ID/EN toggle translating every string), Global Nature Watch ex-GFW (six languages including Bahasa Indonesia), APIMS (BM advisory PDFs); NASA FIRMS, ASMC and GWIS as the **avoid** cases (English-only despite Borneo audiences); Borneo supplement — BMKG and BNPB (national authorities shipping BI-only, even for BMKG's ASEAN-wide product), NEA (EN-only UI whose actionable guide ships as four downloadable PDFs — EN/MS/ZH/TA, no Bahasa Indonesia at all), Nusantara Atlas (EN-only for a tri-country audience).
- **Screenshots:** none (no screenshot of a language switcher was captured).
- **Verdict:** adapt — the one-click full-string-table toggle is inherited from SiPongi+ as-is; the named change is that no audited app ships this particular combination, so EN + ID + MS in one string table is IGNIS's own scope decision.
- **Serves:** all three users plus the haze-impact audience
- **Why:** The Coverage Area spans Bahasa Indonesia-speaking Kalimantan (including the source-side of the haze-impact audience this library defines) and Bahasa Malaysia-speaking Sarawak, Sabah and Brunei, SiPongi+ proves a complete bilingual toggle is cheap, and every English-only predecessor is a demonstrated gap. NEA's PDF-artifact approach — localize the *actions*, not the chrome — is the cheaper fallback for any locale that misses a release, but it missed the source-side (Bahasa Indonesia) audience entirely, which is why the full string-table toggle is the recommendation.
- **Iban (team decision, not audit evidence):** Iban is the language of Sarawak's largest ethnic group, and many longhouse and rural communities sit closest to recurring burning, so it reaches the land managers and residents the Malay locales miss. No audited app ships Iban, and terms like Hotspot, Harmonized Hotspot Count and Burning Phase have no settled Iban wording, so the strings need a native-speaker reviewer. Plan the string table for a fourth locale from the start; ship Iban at launch only if that reviewer signs off, otherwise as the first post-launch locale.

---

## Open dependencies register

Data and decisions this library names but cannot settle. Each gates the patterns above; none is owned by the UI — each is an architect / data-lead (or, for Iban, team) decision, recorded here so no pattern reads as more data-backed than the repo is.

1. **Tri-country boundary GIS** — gates depth-2 presets, per-country place chains and the harmonization refit (*Tri-country coded Areas of Interest at mixed depths*, *Named Areas of Interest*, *Place-chain Hotspot popup*). Audited proof such a product exists: GNW ex-GFW's "Political boundaries" preset layer.
2. **Malaysian and Bruneian admin-code gazetteers** — gates coded selection/storage outside Indonesia (*Tri-country coded Areas of Interest at mixed depths*). Audited codes are Kemendagri/Indonesia only; no audited source names the MY/BN equivalents.
3. **Harmonization refit on Malaysian/Bruneian boundaries** — gates per-AOI Harmonized Hotspot Counts, Typical Years and Burning Phases on the MY/BN side (*Pre-aggregated historical envelope band*, *Burning Phase encoding*, *Cross-border comparison*, *Quiet-state vs Peak-state home*). Until the refit the [harmonization analysis](../harmonization-analysis.md) itself calls for, Sarawak + Sabah + Brunei is one approximate region and its months may never classify Peak under the proposed global cutoff.
4. **Sarawak/Kuching air-quality feed** — gates the haze-impact panel's live tier (*Haze-impact panel*; declared in that pattern: APIMS static, IQAir no public CSV, ASMC WIS2 covers Hotspot coordinates only, NEA delegates to Data.gov.sg).
5. **Machine-readable FDRS feed covering MY/BN** — gates the context panel's forecast tab outside Indonesia (*One tabbed context-overlay panel*); audited FDRS is Indonesia-only (SiPongi+, BMKG provincial) or a static daily ASEAN image (BMKG).
6. **Endonym gazetteer per locale** — anchors Q3's place-name spellings (*English + Bahasa Indonesia + Bahasa Malaysia from day one, Iban next*): one coded gazetteer carrying Kalimantan Barat / West Kalimantan per locale.
7. **Iban native-speaker reviewer** — gates the fourth locale's launch (language pattern above; team decision, no audit evidence exists).
