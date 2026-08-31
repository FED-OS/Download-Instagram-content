# Contributing to FED-GRAM

First off — thank you for taking the time to contribute! 🎉 FED-GRAM is a community-friendly project and every contribution, from typo fixes to new platform engines, is welcome.

This document explains how to set up the project, the conventions we follow, and the process for getting your changes merged.

---

## 📜 Code of Conduct

By participating in this project you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please be respectful and constructive in all interactions.

---

## 🛠️ Development setup

```bash
# 1. Fork & clone
git clone https://github.com/YOUR_USERNAME/FED-GRAM.git
cd FED-GRAM

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional but recommended for video engines) install ffmpeg
sudo apt install ffmpeg         # Debian/Ubuntu
brew install ffmpeg             # macOS

# 5. Run the app
streamlit run app.py
```

The app launches at **http://localhost:8501**.

---

## 🧱 Architecture overview

FED-GRAM uses a **detector → router → engine** pipeline. Understanding this is essential before adding features:

- **`downloaders/detector.py`** — maps a URL to a platform key (`"instagram"`, `"youtube"`, etc.) via domain matching.
- **`downloaders/__init__.py`** — `resolve(url, dest_dir)` iterates an ordered list of engines; the first whose `can_handle(platform)` is `True` wins. `generic_engine` is always last as a catch-all.
- **`downloaders/models.py`** — the shared `DownloadResult` and `MediaItem` dataclasses that every engine must return.
- **`downloaders/<platform>_engine.py`** — each engine exposes two functions: `can_handle(platform: str) -> bool` and `download(url, platform, dest_dir) -> DownloadResult`.

If you add a new platform you only need to: (1) register its hosts in `detector.py`, (2) write an engine module with `can_handle`/`download`, and (3) import + order it in `__init__.py`.

---

## ✅ Coding conventions

- **Python 3.11+** (uses `from __future__ import annotations` and `str | None` syntax).
- Every engine **must** return a `DownloadResult` — never raise out of `download()` for expected failures; put the message in `result.error` instead.
- Wrap all network calls in `try/except` so a single broken source doesn't crash the app.
- Deduplicate media URLs before downloading to avoid redundant fetches.
- Use `os.makedirs(dest_dir, exist_ok=True)` at the top of each engine's `download()`.
- Keep functions small and documented with a module-level docstring explaining the scraping strategy.
- No external API keys or secrets should be required for any engine — we rely on public page data and `yt-dlp`.

---

## 🧪 Testing your changes

There is no formal test suite yet. Before opening a PR, manually verify:

1. The app launches without import errors: `streamlit run app.py`.
2. Your new/changed engine handles at least one real public URL from its platform.
3. An unsupported URL still falls through to `generic_engine` gracefully.
4. A private / deleted / invalid URL returns a clean `result.error` rather than a stack trace.

If you add a new engine, include a short comment with an example URL that was tested.

---

## 🔀 Pull request process

1. **Fork** the repo and create a branch from `main`:
   ```bash
   git checkout -b feat/add-pixiv-engine
   ```
2. Make your changes, keeping commits focused. Follow Conventional Commits style if you can:
   - `feat: add Pixiv engine`
   - `fix: handle imgur gifv → mp4 conversion`
   - `docs: update supported platforms list`
3. Update **`requirements.txt`** if you introduce a new dependency, and explain *why* in your PR description.
4. Update **`CHANGELOG.md`** under the `## [Unreleased]` section.
5. Run the app and the manual checks above.
6. Open a pull request using the [PR template](.github/PULL_REQUEST_TEMPLATE.md) and fill it out completely.
7. Be responsive to review feedback. We aim to review within a few days.

A maintainer will merge once CI (if configured) is green and the review is approved.

---

## 🐛 Reporting bugs

Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md). The more detail (URL, platform, error text, screenshots), the faster we can reproduce and fix it.

---

## 💡 Suggesting features

Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md). New platform engines are always welcome — let us know which site and what kind of media it should grab.

---

## 📂 Good first issues

Look for issues labelled `good first issue` or `help wanted`. These are scoped to be approachable for newcomers to the codebase. Adding a new scraping engine for a single platform is a great first contribution.

Thank you again — happy hacking! 🚀
