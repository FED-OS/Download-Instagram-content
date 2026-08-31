# AGENTS.md

> Operating instructions for AI agents (Claude, Codex, Cursor, etc.) working in
> this repository. This complements [CLAUDE.md](CLAUDE.md), which has the
> technical detail.

## Mission

FED-GRAM is a community-friendly, MIT-licensed Streamlit app for downloading
public media from social platforms. AI agents contributing here should produce
clean, defensive, well-documented code that a human maintainer can review
quickly.

## Operating principles

1. **Read before you write.** Always read the relevant engine and `app.py`
   before editing. The architecture is small but consistent — match it.
2. **Never raise from engine `download()` for expected failures.** Return a
   `DownloadResult` with `error` set. See `CLAUDE.md` → Conventions.
3. **No secrets, no keys.** Engines must work without API keys. If a platform
   truly requires auth (e.g. YouTube bot-walls), wire it through the existing
   cookies mechanism — never hard-code credentials.
4. **Defensive network code.** Every `requests.get` / `yt-dlp` call wrapped in
   `try/except`. Timeouts on all fetches (30s is the project norm).
5. **Update everything that's affected.** Adding a platform means touching
   `detector.py`, the engine module, `__init__.py`'s `_ENGINES`, and
   `app.py`'s `_PLATFORM_ICON`. Update `requirements.txt` if a new dependency
   is introduced, and `CHANGELOG.md` under `[Unreleased]`.
6. **Don't commit runtime artifacts.** Downloaded media, `cookies.txt`,
   `__pycache__`, and `.env` are git-ignored. Never stage them.

## What an agent should do for common tasks

### Add a new platform engine
- Follow the 5-step checklist in [CLAUDE.md](CLAUDE.md) → "When adding a new
  platform engine".
- Add a module docstring describing the scraping strategy.
- Test with a real public URL and a deliberately invalid one.

### Fix a bug
- Reproduce it first (read the error, find the engine, test the URL).
- Make the minimal change. Prefer fixing the root cause over catching the
  symptom.
- Add a `CHANGELOG.md` entry under `### Fixed` in `[Unreleased]`.

### Update a broken scraper
- Fetch the target page, inspect current markup, update the regex patterns.
- Keep multiple fallback patterns (the project style) so minor markup shifts
  don't break everything.
- Note the change in `CHANGELOG.md`.

### Improve docs
- Keep the tone friendly and practical. Cross-link related docs
  (`INSTALL.md`, `usage.md`, `FAQ.md`, `SECURITY.md`).
- Don't duplicate content — reference instead.

## What an agent must NOT do

- ❌ Introduce a dependency without updating `requirements.txt` and justifying it.
- ❌ Use `unsafe_allow_html=True` with remote or user-supplied content.
- ❌ Disable error handling to "make it work" — surfacing clean errors is a
  feature.
- ❌ Bulk-download or stress-test platforms (violates ToS and the project ethos).
- ❌ Edit `LICENSE`, `CHANGELOG.md` released sections, or semver tags without
  maintainer sign-off.
- ❌ Open PRs that mix unrelated changes. One concern per PR.

## Verification before declaring done

1. `python -c "import downloaders"` succeeds (no import errors).
2. `streamlit run app.py` launches and serves HTTP 200.
3. The affected engine handles a real public URL.
4. A bad URL returns a clean `DownloadResult.error`, not a traceback.
5. `CHANGELOG.md` updated if user-facing.

## Communication

When summarizing work for a maintainer, report: what changed, why, which files,
how it was verified, and any follow-up risks (e.g. "this scraper may break if
Pinterest changes their pin JSON structure").
