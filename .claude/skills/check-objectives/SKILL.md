---
name: check-objectives
description: Audit IGNIS against the NASA Space Apps 2026 "MODIS and VIIRS Hot Spots" challenge objectives in docs/OBJECTIVES.md. Use when someone asks to check objectives, check the challenge requirements, ask "are we ready to submit", do a pre-submission check, or after a feature lands that could tick an objective.
---

# Check objectives

`docs/OBJECTIVES.md` is the single source of truth. `scripts/check-objectives.sh` only proves that evidence files exist. This skill judges whether the evidence actually meets each objective.

## Steps

1. Run `sh scripts/check-objectives.sh --strict` and keep its FAIL / TODO / READY lines.
2. Read `docs/OBJECTIVES.md`. For every item, ticked or not, open its evidence and decide:
   - **Met**: the evidence really does what the objective says. For app features, load the page (the `heatmap-prototype` preview in `.claude/launch.json`, or the live site via the `deploy-prototype` skill's URL) and try the feature, not just grep for it.
   - **Partly met**: name exactly what is missing.
   - **Not met** or **No evidence**.
   A ticked item that is only partly met is a finding. Say so; do not untick it yourself.
3. **S5-PLAIN-LANGUAGE**: read the visible app text and any submission drafts as a non-technical judge would. List every jargon term shown without a plain explanation on first use (MODIS, VIIRS, FRP, harmonization, anomaly, hotspot, AOI, k-factor, and similar) with a suggested plain rewrite.
4. **Prohibited**: confirm no NASA logo, flag or mission identifier appears in the UI, assets or video.
5. The hard submission deadline is Sun 15 Nov 2026, 9pm (Sarawak time). Compare with today's date and say how long is left.

## Report

One table: ID | status (Met / Partly / Not met / No evidence) | one-line reason. Then a short list of the next three items to do, Must first. Keep it plain; the team includes non-technical members.

Never tick or untick items or edit OBJECTIVES.md unless asked. Offer the edits instead.
