# Todo

Track of outstanding work for the FED-GRAM project. Items move from here into
[CHANGELOG.md](CHANGELOG.md) when shipped. Checkboxes show current status.

## Documentation & project files
- [x] Write advanced multi-platform `app.py` (replaces stale Instagram-only version).
- [x] Update `requirements.txt` to include `yt-dlp` and `Pillow`.
- [x] Rewrite `README.md` for the 18-platform reality + Ko-fi button.
- [x] Add `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `SUPPORT.md`.
- [x] Add `CHANGELOG.md`, `FAQ.md`, `usage.md`, `NOTICE.md`.
- [x] Add `CLAUDE.md`, `AGENTS.md` for AI-assisted development.
- [x] Add `AUTHORS.md`, `MAINTAINERS.md`, `GOVERNANCE.md`.
- [x] Add `ROADMAP.md`, `ADR.md`, `DEPLOYMENT.md`, `BUILD.md`, `INSTALL.md`.
- [x] Add `SUMMARY.md`, `COPYING.md`, `CITATIONS.md`.
- [x] Add `.github/` issue templates, PR template, discussion welcome readme.
- [x] Add `social-image.png` and `prompts/`, `wiki/`, `discussion/` dirs.
- [x] Update `.gitignore` (cookies, downloaded media, caches).

## Code & stability (v1.2)
- [ ] Add a formal `pytest` test suite for `detect_platform` and each engine's
      `can_handle`.
- [ ] Improve error-message taxonomy (private vs deleted vs rate-limited vs
      markup-changed).
- [ ] Add a download quality/format selector for `yt-dlp`.
- [ ] Add progress feedback for large video downloads.
- [ ] Verify TikTok slideshow image extraction path.

## Features (v1.3+)
- [ ] Optional API-key engines for Imgur (Client-ID) and Reddit (OAuth).
- [ ] Per-platform rate-limit awareness with simple backoff.
- [ ] Session-scoped download history.
- [ ] Docker image + `docker-compose.yml`.
- [ ] Headless CLI mode (`python -m fedgram <url>`).
- [ ] Pluggable third-party engine registry.
- [ ] i18n of the Streamlit UI.

## Maintenance
- [ ] Replace placeholder maintainer/contact details (Ko-fi username, security
      email) with real values before public release.
- [ ] Set up CI to run import + launch checks on push.
- [ ] Schedule periodic yt-dlp / instaloader dependency updates.
