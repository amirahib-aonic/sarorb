# IGNIS

Burning activity calendar for the Sarawak Space Challenge. The baseline verifies the handoff from the offline Python pipeline to a static Vite and TypeScript page.

## Run locally

Open this repo folder in VS Code. Use Python 3.13 and Node.js 22.12+ (or Node.js 24).

From the repo root:

```powershell
python scripts/build_preview_data.py
npm --prefix web install
npm --prefix web run dev
```

The script with no arguments writes the empty preview. To see ingestion counts in the browser, pass one or more FIRMS CSV paths, then refresh:

```powershell
python scripts/build_preview_data.py data/firms_raw/modis.csv data/firms_raw/viirs.csv
```

Raw inputs can stay in the git-ignored `data/firms_raw/` directory or anywhere locally. Commit only the small generated files intended for the preview. The baseline preview lists input row counts and filenames. It does not publish raw rows. Future processing stages belong under `scripts/`, with browser-ready outputs under `web/public/data/`.

Run `npm --prefix web run build` to type-check and build the production bundle into `web/dist/`.

## Burning Calendar data

In Git Bash, extract the local `firmsdata` branch and generate the JSON:

```bash
mkdir -p data/firms_raw
git archive --format=tar firmsdata | tar -xf - -C data/firms_raw
python -m pip install pandas
python scripts/build_burning_calendar.py --download-area
```

The download-area run uses the FIRMS rectangle. For island-only results, install
Shapely 2 and pass `--boundary data/firms_raw/borneo.geojson` in place of
`--download-area`. Use a WGS84 GeoJSON Feature containing the island polygon.

The script filters archive detections, counts UTC months, fits 12 pooled
S-NPP/MODIS ratios on paired months in 2012–2025, and estimates the NOAA-20/S-NPP
ratio in their overlap. It selects S-NPP first, adjusted NOAA-20 second, then
scaled MODIS for pre-2012 months. Interior archive months are treated as covered,
and partial edge months are excluded. Commit the regenerated JSON under
`web/public/data/` to publish the new numbers.

## Vercel previews

Import this GitHub repo in Vercel and use these settings:

| Setting | Value |
| --- | --- |
| Root Directory | `web` |
| Framework Preset | Vite |
| Install Command | `npm install` |
| Build Command | `npm run build` |
| Output Directory | `dist` |

Keep `main` as the production branch if `ignis` should stay in Preview. Once the Git integration is connected, pushes to non-production branches create previews. Use `ignis` as the integration branch and open feature PRs against it. Vercel serves the committed JSON as a static asset.

```powershell
git switch ignis
git pull --ff-only origin ignis
git switch -c feature/firms-ingest
# Work, commit, then push the feature branch.
git push -u origin feature/firms-ingest
```

Adam can start with `feature/firms-ingest`. Amirah can use `feature/data-integration`, and Nazmi can use `feature/frontend`. Review each branch's Vercel preview before merging into `ignis`.
