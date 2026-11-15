# UI/UX Borneo Supplement — Research Brief

This is the brief for the **Borneo supplement** audits: four more apps studied on top of the 13 core reference apps audited on 2026-11-14, because IGNIS's Coverage Area is the *whole island* of Borneo and the core audits underweight the Indonesian side and tri-country UX problems.

**This brief is self-contained.** A supplement auditor never needs to read `docs/research/UI-UX-RESEARCH-PLAN.md` (the main plan): everything allowed, required and expected is in this file. Scoping of the four apps below was browser-verified on 2026-11-14; where a claim about a live site could not be confirmed, this brief says so and tells you what to do.

`GLOSSARY.md` is the canonical vocabulary and is still required reading; it supersedes any older term list anywhere, including one inside the main plan.

> Note: this brief and the audit tree under `docs/research/ui-ux/` are tracked in git, as is the main research plan.

## 0. Brief for the supplement auditor

**Your job:** audit ONE assigned app and write `docs/research/ui-ux/<slug>.md`. Only research and write notes.

**Allowed**
- Browse the app and its public documentation.
- Create and edit files inside `docs/research/ui-ux/` only.

**Not allowed**
- Editing any file outside `docs/research/ui-ux/` — this brief and the main plan included.
- Writing app code, choosing a stack, or making wireframes and ADRs (that is a later step).
- Committing or pushing.
- Signing up for accounts or entering credentials. If an app needs a login, note it and write the skipped stub (section 5).

**Folder layout**
```
docs/research/ui-ux/
├── <slug>.md            one per supplement app (your audit file)
└── img/<slug>/          screenshots, named NN-what-it-shows.png
```
This folder already holds the 13 core audits plus `PATTERNS.md` and `README.md` — add your files alongside them; do not touch the existing ones.

## 1. Who we design for

Each audit is scored against the same three users as the core audits:

| Audience | Core question | What the UI must make fast |
|---|---|---|
| First responders | Is it burning now, and where? | Latest Hotspots, map-first, mobile-friendly, low clutter |
| Scientists | Is the MODIS/VIIRS record consistent over years? | Date ranges, sensor toggle, export, clear methodology |
| Land managers | When is burning season, and where does it repeat? | Burning Calendar / seasonality view, region selection, year-to-year comparison |

Plus the **haze-impact audience**: everyone in the Coverage Area exposed to haze — downwind (Sarawak, Sabah, Brunei, Singapore-side) and source-side (Kalimantan). This supplement exists largely for them: haze does not stop at borders, and neither should the UI.

**Vocabulary** — read `GLOSSARY.md` and use its exact terms:
- **Coverage Area**: the island of Borneo (Kalimantan, Sarawak, Sabah and Brunei); every Area of Interest lies inside it.
- **Area of Interest**: any region a person selects to examine, drawn on the map or picked from a preset.
- **Hotspot**: a single satellite detection of active fire at a location and time, from either MODIS or VIIRS.
- **Harmonized Hotspot Count**: the monthly Hotspot count in an Area of Interest expressed as the count VIIRS would have recorded.
- **Burning Calendar**: the view of when burning happens — a Typical Year on top, a year-by-month grid below.
- **Typical Year**: the average Harmonized Hotspot Count per calendar month, each month given a Burning Phase.
- **Burning Phase**: how much of a Typical Year's burning falls in one month (Peak, Active, Moderate, Low).
- **Overlap Period**: the years when MODIS and VIIRS both observed the Coverage Area (2012 onward).

## 2. The four supplement apps

### bmkg-fire-potential — BMKG fire potential
- **URL**: https://www.bmkg.go.id/ · **Tier**: 1
- **Focus**: FFMC fire-potential map images and how a national met service communicates fire danger in Bahasa Indonesia only.
- **Why picked**: official Indonesian ignition-risk forecast for the Kalimantan side, complementing IGNIS's detection record, and a static-image baseline the interactive views must beat.
- **Scoping notes (2026-11-14)**: homepage product card "Potensi Kebakaran Hutan" links to FFMC map images under dataweb.bmkg.go.id/cuaca/spartan/; peta.bmkg.go.id was DNS-dead and /kualitas-udara/kebakaran-hutan 404'd at scoping — lean on the image products.

### nusantara-atlas — Nusantara Atlas
- **URLs**: https://nusantara-atlas.org/ and https://map.nusantara-atlas.org/ · **Tier**: 2
- **Focus**: land-use, peatland and concession context layers that explain where Hotspots recur.
- **Why picked**: Borneo-wide land-use and peat context — the where complement to the Burning Calendar's when.
- **Scoping notes (2026-11-14)**: successor of the CIFOR Borneo Atlas; LAYERS/CONCESSIONS/search-by-coordinate verified live. The audit must confirm whether the map extent covers Sarawak/Sabah or is Indonesia-only, and record the answer.

### nea-haze-portal — NEA haze portal
- **URL**: https://www.haze.gov.sg/ · **Tier**: 2
- **Focus**: cross-border haze communication: PSI toggle, hotspots section, health advisories, per-region breakdown.
- **Why picked**: the region's most mature public cross-border haze site — the model for linking Coverage Area burning to health outcomes.
- **Scoping notes (2026-11-14)**: 24-hr PSI toggle, HOTSPOTS section with legend, HEALTH ADVISORY, downloadable PDF guides and region breakdown all verified live.

### bnpb-disaster-geoportal — BNPB disaster geoportal
- **URL**: https://gis.bnpb.go.id/ · **Tier**: 2
- **Focus**: how Indonesia structures disaster incident data by admin hierarchy across hazards (karhutla as an official disaster class).
- **Why picked**: national-authority data architecture the region panel and about/method views can learn from.
- **Scoping notes (2026-11-14)**: ArcGIS hub, login-free: Data Bencana / Pantauan Bencana / Peta Krisis / InaRISK / InAWARE / Dashboard Pencegahan.
- **CONDITIONAL APP**: fire/karhutla content was NOT confirmed at scoping (2026-11-14). Spend a bounded look (about ten minutes) across the sections named in the scoping notes for fire or karhutla layers, dashboards or incident classes. If none is found, write the skipped stub (header line plus "Status: skipped" plus a Summary of what the portal does cover) and stop — that stub counts as complete. If fire content is found, audit it normally.

## 3. Walkthrough tasks

Run the same three tasks in every app that supports them:

1. **"Where were hotspots in Central Kalimantan last August?"**
2. **"Compare the burning season across borders: West Kalimantan vs Sarawak"**
3. **"Is 2023 worse than 2019?"**

Rules:
- Count the actual clicks for the Steps/clicks column.
- Where a task exceeds the app, write **"not supported"** in the Result column and move on.
- **Apps without Hotspot data** (Nusantara Atlas; BNPB unless fire content is confirmed) replace the three tasks with the fallback: **"How does the app present its data at a glance for someone in the Coverage Area?"**
- **Risk-forecast apps without detections** (BMKG) adapt each task to the app's own product (where is potential highest / when does it peak / compare two periods) — say so in the Notes column.
- A walkthrough you could not execute is recorded as **documented-not-executed**, never silently claimed.

## 4. Audit checklist

Score the core 13 items (condensed from the core audit checklist):

1. **First screen** — what loads first; time to first useful answer.
2. **Time controls** — date picker, slider, playback, presets; how gaps in data are shown.
3. **Space controls** — region picker, draw-a-box, admin boundaries, search.
4. **Hotspot display** — points vs clusters vs density grid; behavior at each zoom.
5. **Sensor handling** — how MODIS vs VIIRS is labeled, toggled or merged; confidence levels.
6. **Color and legend** — scale choice, colorblind safety, legend placement, basemap.
7. **Linked views** — picking a date updates the map, and the other way round?
8. **Comparison** — year vs year, region vs region, anomaly vs baseline.
9. **Explaining the data** — methodology, uncertainty, caveats; how much and where.
10. **Mobile** — phone-width layout, touch on the map, bottom sheets.
11. **Export/share** — CSV, PNG, shareable URL with state.
12. **Language and locale** — English/Malay/Indonesian, date formats.
13. **Performance** — load weight, responsiveness on slow connections.

Then the four Borneo items, new in this supplement:

- **B1 Tri-country admin-boundary hierarchies**: how one region picker handles mixed depths — Provinsi/Kabupaten (ID) vs Sarawak divisions & Sabah residency/districts (MY) vs Brunei daerah — surfaced (SiPongi chain) or flattened (ASMC presets); stale-boundary pitfalls (pre-2012 Kalimantan Utara).
- **B2 Cross-border region comparison**: compare Areas of Interest across national borders (e.g. West Kalimantan vs Sarawak same season); country labeling/tiers; foreign-baseline framing.
- **B3 Tri-lingual language handling**: EN/BM/BI default + toggle; localized place names (Kalimantan Barat vs West Kalimantan); date/number locale; divergent fire vocabulary (BM "api" vs BI "karhutla" vs EN "hotspot").
- **B4 Cross-source count attribution**: how an app explains its counts vs KLHK/ASMC/FIRMS official numbers (methodology note, "why we differ" affordance) — the Harmonized Hotspot Count precedent.

**Scoring**: 0–2 per audience (Responder / Scientist / Land mgr) and one verdict per row: **inherit / adapt / avoid**. Mark **N/A** where an item cannot apply to the app (e.g. B4 for an app with no counts).

## 5. Per-app file template

Write `docs/research/ui-ux/<slug>.md` with EXACTLY these sections:

```markdown
# <App name>
URL: <link> · Audited: <YYYY-MM-DD> · Tier: <1|2|3> · Supplement: Borneo

## Summary
2–3 sentences: what it is, what it does best for IGNIS's tri-country Coverage Area.

## Task walkthrough
| Task | Steps / clicks | Result | Notes |
|---|---|---|---|
(one row per section-3 task, or the fallback task)

## Checklist
| # | Item | Observation | Responder 0-2 | Scientist 0-2 | Land mgr 0-2 | Verdict |
|---|---|---|---|---|---|---|
(one row per checklist item 1–13 and B1–B4 = 17 rows; Verdict = inherit / adapt / avoid, or N/A)

## Screenshots
- ![](img/<slug>/01-....png) caption saying what it shows

## Patterns worth taking
- **<Pattern name>**: what it is, why it fits IGNIS, which audience it serves.
```

The section headers `## Summary`, `## Task walkthrough`, `## Checklist`, `## Screenshots` and `## Patterns worth taking`, the `Audited:` header line, and the bolded pattern bullets are checked mechanically — keep them exact.

**Skipped stub**: if the app demands an account/payment, or (for a conditional app) the content is absent after the bounded check, write `docs/research/ui-ux/<slug>.md` with the header line plus `Status: skipped` on it and a Summary explaining the wall or what you found instead, then stop. **That stub counts as complete.**

## 6. Open questions this audit feeds

Gather **evidence** for these three questions (takeaways, patterns, checklist rows) wherever your app shows the relevant behavior. The librarian answers them in README.md — you do not answer them yourself.

- **Q1 Default landing view for a tri-country audience**: whole Coverage Area vs the visitor's geo-located country vs last-visited Area of Interest; which country's framing leads About/method copy.
- **Q2 Region presets across three countries**: which preset set ships first (5 Kalimantan provinces + Sarawak + Sabah + Labuan + Brunei districts?) and at what boundary depth.
- **Q3 Language rollout**: EN-only v1 vs EN+BI (largest audience) vs EN+BM+BI; whose place-name spellings anchor map labels; separate BM/BI glossaries (the committed recommendation already adds Iban as a fourth locale — build on it, don't drop it).

## 7. Already covered by the core audits — do not re-audit

These angles already have evidence in existing audit files. If your app shows one of these angles, cite the existing file and differ — record only what YOUR app adds.

- `asmc.md` — tri-country chart presets, regional haze narrative — strongest tri-country source
- `sipongi.md` — Desa→Kecamatan→Kabupaten→Provinsi chain, BI-first + EN toggle
- `gwis.md` — province comparisons, pre-2012 Kalimantan Utara caveat
- `global-forest-watch.md` — West Kalimantan Area of Interest workflow, 6 UI languages incl. BI
- `apims-iqair.md` — MY-side haze impact communication
- `nasa-worldview.md` — place-search-to-polygon anti-pattern for a tri-country gazetteer
- `sentinel-hub.md` — state-in-URL sharing

## 8. Definition of done

- A file exists at `docs/research/ui-ux/<slug>.md` per the template — or a skipped stub; **a skipped stub counts as complete**.
- All 17 checklist rows are present (N/A allowed).
- Screenshots for the key screens, where the app allows.
- Limitations recorded: documented-not-executed walkthroughs labeled as such.
