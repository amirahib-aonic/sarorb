# AGENTS.md

## Project

This repo (sarorb) holds **IGNIS** (Integrated Geospatial Network for Ignition Surveillance), built by team Sarawak Orbiters for the NASA Space Apps Challenge 2026 through the Sarawak Space Challenge. Challenge: *Harmonization of MODIS and VIIRS Hot Spots*.

IGNIS is a web app that brings MODIS and VIIRS fire hotspots into one consistent view: an interactive burning calendar shows when hotspots were detected, and a heatmap shows where they cluster. It serves first responders, scientists and land managers.

## Status

The repository is at its initial commit and contains no application code yet. There is no chosen stack, build, test or lint tooling. Update this file as those are added.

## Working conventions

- Keep changes small and focused; one concern per commit.
- Match the style of surrounding code once it exists.
- Do not commit secrets, API keys or `.env` files.
- Document any new setup, build or test commands in this file.

## Git hooks

Hooks in `.githooks/` block secrets, personal data (emails, MyKad, NIK, phone numbers), private Google Drive/Docs links, office documents and files over 5 MB. Enable them once per clone:

```bash
git config core.hooksPath .githooks
```

They need [gitleaks](https://github.com/gitleaks/gitleaks) on your PATH (`winget install Gitleaks.Gitleaks` or `brew install gitleaks`). Rules live in `.gitleaks.toml`.
