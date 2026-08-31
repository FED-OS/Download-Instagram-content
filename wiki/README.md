# FED-GRAM Wiki

This directory holds extended documentation in a wiki style. The primary docs
live in the repository root (see [SUMMARY.md](../SUMMARY.md) for an index);
this wiki goes deeper on specific topics.

## Pages

- [Home](Home.md) — wiki landing page.
- [Engine-Development-Guide](Engine-Development-Guide.md) — how to write and
  register a new platform engine, end to end.
- [Platform-Detection](Platform-Detection.md) — how `detect_platform` works and
  how to add a new domain.
- [Scraping-Strategies](Scraping-Strategies.md) — patterns used by the
  HTML-scraping engines and why.
- [Deployment-Recipes](Deployment-Recipes.md) — local, Streamlit Cloud, Docker,
  reverse-proxy setups (mirrors [../DEPLOYMENT.md](../DEPLOYMENT.md) with
  extras).
- [Troubleshooting](Troubleshooting.md) — common errors and fixes (mirrors
  [../FAQ.md](../FAQ.md) with edge cases).
- [Architecture](Architecture.md) — the detector→router→engine pipeline in
  depth (mirrors [../ADR.md](../ADR.md)).

> Note: if you enable GitHub's built-in Wiki, prefer keeping these files in the
> repo under `wiki/` (side-bar wiki) so they are versioned with the code. If
> you migrate to GitHub's native wiki, copy these files across.
