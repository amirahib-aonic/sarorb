# Tech Stack

Challenge: NASA Space Apps 2026, *Harmonization of MODIS and VIIRS Hot Spots*, entered through Sarawak Space Challenge. The goal is a burning activity calendar web app built on one harmonized MODIS + VIIRS hotspot record. West Kalimantan is the priority region.

## Guiding constraints

- **Instant output.** The demo must answer in under 3 seconds. Heavy processing happens offline, and the app only reads small precomputed files.
- **Live demo + public repo.** Both are Gate 0 requirements. A dead link or a private repo means disqualification.
- **Cite the data by name.** NASA FIRMS MODIS Collection 6.1 (1 km) and VIIRS 375 m (S-NPP, NOAA-20).
- **Free to host, no keys in the browser.**

## Architecture

```
FIRMS CSVs (raw, ~620 MB, git-ignored)
        │  Python pipeline (offline)
        ▼
harmonize ─► grid ─► aggregate
        │
        ▼
web/data/*.json  (small, versioned)
        │  static site
        ▼
Browser: map + calendar + anomaly + CSV export
```

The app never touches raw hotspots. The pipeline bins the harmonized detections into a grid (for example 0.1° cells × month) and writes compact JSON. When a user selects a region or draws a box, the browser sums the cells inside it. That keeps "any region, any date range" instant without a backend.

## Layers

### 1. Data pipeline (Python, offline)

| Concern | Choice | Why |
|---|---|---|
| Language | Python 3.13 | Already used in `scripts/` |
| Tables | pandas (DuckDB if grids get large) | DuckDB can query the raw CSVs directly, with no loading step |
| Geometry | shapely 2 | Vectorized point-in-polygon, already in use |
| Boundaries | geoBoundaries IDN ADM1 (ODbL) | Province outlines; Sarawak/Malaysia ADM1 can be added the same way |
| Fire-event clustering | scikit-learn DBSCAN | "Fires, not pixels" grouping in space and time |
| Harmonization | Aqua × S-NPP same-overpass pairs → detection-probability model (scikit-learn logistic / isotonic) | Measured transfer function instead of a single ratio |
| Validation | Holdout on years the model never saw | Reported error for the Data award pitch |
| Output | JSON (gzip-friendly), plus CSV for downloads | Readable directly by the browser |

Entry points live in `scripts/`. Raw data stays in `data/firms_raw/` and is not committed.

### 2. Web app (static)

| Concern | Choice | Why |
|---|---|---|
| Build | Vite + vanilla TypeScript (or React if the UI grows) | Fast dev server, static output |
| Map | MapLibre GL JS + free OSM/Carto tiles | Draw-a-region, no API key |
| Region drawing | maplibre-gl-draw or a simple bbox tool | Brief asks for drawn area or lat/lon entry |
| Charts | Observable Plot (or D3) | Calendar heatmap, anomaly bars, time series |
| Color | Color-blind-safe sequential ramp (viridis/inferno family) | Brief asks for accessible color ramps |
| Export | Client-side CSV build + download button | Brief asks for downloadable analytics |
| i18n | English + Bahasa Malaysia strings | Local Impact framing for Sarawak |

### 3. Repo and CI

- GitHub public repo; `main` is what gets deployed.
- GitHub Actions: lint, run the pipeline on a small fixture, build the site.
- `README.md` with a setup that works in one command, the data citation, and the AI-use statement.

## Hosting options

All options below serve the same static `dist/` folder, so we can switch later without code changes.

| Option | Cost | Setup | Pros | Cons |
|---|---|---|---|---|
| **GitHub Pages** | Free | Actions workflow builds and publishes `dist/` | Repo and demo in one place; previous winners used it (PureFlow 2025) | Public repos only on free plan; 1 GB site limit; no preview deploys per branch |
| **Vercel** | Free (Hobby) | Import repo, framework preset Vite | Preview URL per branch/PR, fast CDN; most common among 2025 winners (QUEÑARIS, Resonant, Astro Sweepers) | Hobby plan is for non-commercial use; team members need accounts to manage it |
| **Netlify** | Free | Import repo or drag-and-drop `dist/` | Preview deploys, drag-and-drop fallback if CI breaks during the hackathon | Monthly build-minute cap on free tier |
| **Cloudflare Pages** | Free | Import repo | Unlimited bandwidth, fast in Southeast Asia | Slightly more setup; less familiar to the team |
| **Hugging Face Spaces / Streamlit Cloud** | Free | Push a Python app | Lets us skip the JS front end entirely | Cold starts (often >3 s), weaker map UX; risky for the 3-second rule |

### Recommendation

1. **Hackathon weekend: Vercel.** Each push gets a preview URL the team can check, and it matches what recent winners shipped.
2. **Backup: GitHub Pages** from the same repo, set up at the same time. If Vercel has an issue near the deadline, the Pages link is already live.
3. **After the hackathon:** if the app grows to cover all of Southeast Asia or gets daily FIRMS updates, add a scheduled GitHub Action that downloads the newest near-real-time FIRMS data, reruns the pipeline and redeploys. That still needs no server. A FIRMS MAP_KEY stays in GitHub Actions secrets, never in the site.

### Size budget

| Item | Target |
|---|---|
| Monthly grid, Indonesia + Borneo, 0.1°, 2002–2026 | < 5 MB compressed |
| Daily series for the priority region | < 1 MB |
| First page load | < 2 MB before data |

If the grid gets bigger than this, split it into one file per year or per tile and load only what the selected region needs.

## Not in scope for the hackathon

- A database or API server
- User accounts
- Wind, CO₂ or emissions layers beyond one smoke-direction arrow for the Sarawak story
- ML fire forecasting
