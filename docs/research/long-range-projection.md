# Long-range Hotspot projection (5, 10, 20 years)

How IGNIS could extrapolate the Harmonized Hotspot Count 5, 10 and 20 years ahead for an Area of Interest. Terms follow [GLOSSARY.md](../../GLOSSARY.md). Status: research notes, not a decision. Sources were read at abstract or snippet level only; check figures against full texts before quoting them in the app.

## The core problem

IGNIS holds about 24 years of monthly counts (MODIS from 2002, VIIRS from 2012). Borneo burning is driven mainly by **El Niño and positive Indian Ocean Dipole (IOD) drought years**, and those cannot be predicted more than a season or two ahead. A statistical model trained on 24 years cannot know whether 2031 is an El Niño year. So a 5–20 year "forecast" of monthly counts is not defensible. A **scenario projection** of the expected level and its range is.

## Options, ranked

1. **Climate-scenario scaling (recommended)**
   - Fit a simple model of yearly (or dry-season) count against a drought index: KBDI, consecutive dry days or the Niño3.4 and IOD indices, from ERA5 or CHIRPS.
   - Feed it CMIP6 projections of that index under SSP2-4.5 and SSP5-8.5 for the 2030s and 2040s.
   - Show a median plus a band, per scenario.
   - Literature supports the drought–fire link and a rising risk: CMIP6 projects more consecutive dry days in Indonesian Borneo in June–August under SSP5-8.5 (Lam et al. 2024), KBDI high-risk area grows under RCP4.5 and RCP8.5 (Yamamoto), and burned area rises by up to about 25% in a CMIP6 + FLAM storyline (Corning 2024). Deforestation alone can quadruple fire-weather frequency by 2050 (Trancoso 2022), so a land-cover toggle is worth considering.
2. **Monte Carlo of El Niño frequency (simplest honest option)**
   - Treat each future year as a draw: El Niño, neutral or La Niña, with the Typical Year scaled by that year type's historical ratio.
   - Simulate thousands of 5/10/20-year paths and show percentiles.
   - Needs no climate model data. Can optionally shift El Niño odds per scenario.
3. **SARIMA / Prophet trend extrapolation**
   - Common in the Indonesian literature (ARIMA/SARIMA for West Kalimantan, SARIMA vs intervention models nationally).
   - Fine for a 1–12 month horizon only. At 5–20 years it collapses to the Typical Year plus a linear trend, with error bands that explode. Use only as a short-range baseline, if at all.
4. **ML (random forest, LSTM)**
   - Not worth it: 24 years equals about 24 independent fire seasons. It would overfit, and it still needs future climate drivers, which brings you back to option 1.

## Suggested shape for the Insights tab

- **Outlook** card: 2030 / 2035 / 2045 expected yearly count for the Area of Interest, as a range under two scenarios. Label it plainly as a scenario projection, not a forecast.
- Method: start with option 2 (hackathon-feasible), then upgrade to option 1 once ENSO/IOD and drought index data are wired in.
- Validate by backtesting: fit on 2002–2014, project 2015–2025, and report coverage of the bands.

## Open questions for grilling

- Yearly totals only, or monthly shape too? Monthly shape can reuse the Typical Year.
- Whole Coverage Area only, or every Area of Interest? Small areas get very noisy.
- Do we model land-cover change, such as peat drainage and deforestation, or climate only?

## Sources

- Lam et al. 2024, causal teleconnections to drought and fire in Indonesian Borneo: https://nora.nerc.ac.uk/537661/
- Future fire risk under climate change and deforestation, Borneo: https://ore.exeter.ac.uk/articles/journal_contribution/Future_fire_risk_under_climate_change_and_deforestation_scenarios_in_tropical_Borneo/29793704
- Corning 2024, ERL 19 114039: https://pure.iiasa.ac.at/20017/1/Corning_2024_Environ._Res._Lett._19_114039.pdf
- Yamamoto, KBDI peat fire risk projection: https://www.dpri.kyoto-u.ac.jp/hapyo/23/pdf/C307.pdf
- Indonesian fires 1997–2015, ENSO and IOD: https://ui.adsabs.harvard.edu/abs/2016AGUFMGC44B..03P
- ARIMA/SARIMA hotspot prediction: https://www.researchgate.net/publication/378250669
- SARIMA vs intervention model, Indonesia: https://ejurnal.ung.ac.id/index.php/jps/article/view/38133
- Kalimantan hotspot distribution and ENSO: https://reference-global.com/download/article/10.14746/quageo-2023-0006.pdf
