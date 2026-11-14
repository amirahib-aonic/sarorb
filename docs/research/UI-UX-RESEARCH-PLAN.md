# UI/UX Research Plan

Goal: study existing fire, haze and earth-observation apps and note which UI/UX patterns IGNIS can reuse or adapt for its burning calendar (when) and heatmap (where). Nothing here is copied wholesale; we record patterns, not branding.

## 0. Brief for the research agent

**Your job:** run the audits in this plan and write the results into `docs/research/ui-ux/`. Only research and write notes.

**Allowed**
- Browse the reference apps and their public docs.
- Create and edit files inside `docs/research/ui-ux/` only.

**Not allowed**
- Editing any file outside `docs/research/ui-ux/` (this plan included).
- Writing app code, choosing a stack, or making wireframes and ADRs (that is a later step).
- Committing or pushing.
- Signing up for accounts or entering credentials. If an app needs a login, write down that it does and skip it.

**Folder layout**
```
docs/research/ui-ux/
├── README.md            index: each app, status (done/skipped), one-line takeaway
├── <app-slug>.md        one per app, e.g. nasa-firms.md, global-forest-watch.md
├── PATTERNS.md          pattern library built from all audits
└── img/<app-slug>/      screenshots, named NN-what-it-shows.png
```

**Per-app file template** (`<app-slug>.md`)
```markdown
# <App name>
URL: <link> · Audited: <YYYY-MM-DD> · Tier: <1|2|3>

## Summary
2–3 sentences: what it is, what it does best for IGNIS.

## Task walkthrough
| Task | Steps / clicks | Result | Notes |
|---|---|---|---|
| Hotspots in West Kalimantan last September | | | |
| Which months burn most, year over year | | | |
| 2023 vs 2019 | | | |

## Checklist
| # | Item | Observation | Responder 0-2 | Scientist 0-2 | Land mgr 0-2 | Verdict |
|---|---|---|---|---|---|---|
(one row per item 1–13 in section 3; Verdict = inherit / adapt / avoid)

## Screenshots
- ![](img/<app-slug>/01-....png) caption

## Patterns worth taking
- **<Pattern name>**: what it is, why it fits IGNIS, which user it serves.
```

**PATTERNS.md format**: one entry per pattern: name, source app(s), screenshot link, inherit/adapt/avoid, which user it serves, and which IGNIS view it belongs to (calendar, heatmap, region panel, about/method).

**Definition of done**
- Every Tier 1 and Tier 3 app has a file. Tier 2 apps are optional if time is short, but they must be listed in README.md as skipped.
- PATTERNS.md has at least 15 patterns, split by IGNIS view.
- README.md has a short "answers to open questions" section that gives a recommendation for each item in section 7, with evidence.
- Use the terms from `GLOSSARY.md` (Hotspot, Fire Area, Impact Area, Harmonized Hotspot Count).

## 1. Who we design for

Each audit is scored against our three users:

| User | Core question | What the UI must make fast |
|---|---|---|
| First responders | Is it burning now, and where? | Latest hotspots, map-first, mobile-friendly, low clutter |
| Scientists | Is the MODIS/VIIRS record consistent over years? | Date ranges, sensor toggle, export, clear methodology |
| Land managers | When is burning season, and where does it repeat? | Calendar/seasonality view, region selection, year-to-year comparison |

Plus the Impact Area angle: people in Sarawak/Kuching linking Fire Area burning to haze.

## 2. Reference apps to audit

### Tier 1: same problem (fire hotspots)
| App | Why study it |
|---|---|
| NASA FIRMS Fire Map | The canonical MODIS/VIIRS viewer: sensor layers, time slider, point vs. density display |
| Global Forest Watch (fire alerts and dashboards) | Region dashboards, area-of-interest drawing, weekly fire charts vs. historical average |
| SiPongi+ (Indonesia KLHK karhutla) | Local fire-area audience, Bahasa Indonesia, province-level hotspot stats |
| ASMC (ASEAN Specialised Meteorological Centre) haze/hotspot maps | Regional haze framing, hotspot + wind/smoke overlays |
| GWIS / EFFIS (Copernicus) | Fire danger, seasonal statistics charts, country/region comparison |

### Tier 2: same data style (time + geography)
| App | Why study it |
|---|---|
| NASA Worldview | Date picker, layer comparison (swipe/side-by-side), animation |
| Sentinel Hub EO Browser | Date timeline with data-availability marks, area selection |
| Windy | Smooth timeline playback, legend design, mobile map UX |
| Malaysia APIMS / IQAir | How haze impact is communicated to the public (color scales, AQI tiers) |
| Watch Duty | Responder-oriented alerts, mobile-first fire info |

### Tier 3: calendar/heatmap patterns
| Pattern source | Why study it |
|---|---|
| GitHub contribution graph | Day/week calendar heatmap that is easy to read |
| Climate Reanalyzer / "climate stripes" charts | Year-over-year seasonality comparison |
| Observable/D3 calendar heatmap examples | Interaction (hover, brush, click-to-filter) |

## 3. What to look at in each app (audit checklist)

1. **First screen**: what loads first (map, chart, summary)? Time to first useful answer.
2. **Time controls**: date picker, slider, playback, presets (24h / 7d / season / year), and how gaps in data are shown.
3. **Space controls**: region picker, draw-a-box, admin boundaries, search.
4. **Hotspot display**: points vs. clusters vs. density grid; behavior at each zoom level.
5. **Sensor handling**: how MODIS vs. VIIRS is labeled, toggled or merged; confidence levels.
6. **Color and legend**: sequential scale choice, colorblind safety, legend placement, dark/light basemap.
7. **Linked views**: does picking a date on the chart update the map, and the other way round?
8. **Comparison**: year vs. year, region vs. region, anomaly vs. baseline.
9. **Explaining the data**: methodology, uncertainty, caveats; how much and where.
10. **Mobile**: layout at phone width, touch on the map, bottom sheets.
11. **Export/share**: CSV, PNG, shareable URL with state.
12. **Language and locale**: English/Malay/Indonesian, date formats.
13. **Performance**: load weight, responsiveness on slow connections.

## 4. Method

1. **Walkthrough per app** (~30 min each): run the same 3 tasks:
   - "Where were hotspots in West Kalimantan last September?"
   - "Which months burn most, year after year?"
   - "Is 2023 worse than 2019?"
2. **Capture**: screenshots of each key screen, saved to `docs/research/ui-ux/<app>/`.
3. **Score** each checklist item 0–2 per user type and write one line: *inherit / adapt / avoid*.
4. **Synthesize** into a pattern library: one card per pattern (name, source app, screenshot, why it fits IGNIS, which user it serves).
5. **Decide**: map the chosen patterns onto IGNIS screens (calendar, heatmap, region panel, about/method) as low-fi wireframes.

## 5. Deliverables

| File | Content |
|---|---|
| `docs/research/ui-ux/<app>.md` | Per-app audit notes + scores |
| `docs/research/ui-ux/PATTERNS.md` | Pattern library: inherit / adapt / avoid |
| `docs/research/ui-ux/WIREFRAMES.md` (or images) | IGNIS layouts built from the chosen patterns |
| `docs/adr/` entry | Key UX decisions (e.g. map-first vs. calendar-first, linked views) |

## 6. Order of work

1. Tier 1 apps (FIRMS, GFW, SiPongi+, ASMC, GWIS): highest relevance.
2. Calendar/heatmap pattern sources (Tier 3): our two signature features.
3. Tier 2 apps for time-control and mobile polish.
4. Synthesis → pattern library → wireframes → ADRs.

## 7. Open questions to settle during the research

- Map-first or calendar-first landing view?
- Show raw MODIS and VIIRS layers, or only the Harmonized Hotspot Count?
- Calendar granularity: daily, weekly or monthly cells?
- Do we need a Sarawak haze/impact view, or only Fire Area burning?
- Which languages ship first?
