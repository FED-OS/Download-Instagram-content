# CLAUDE.md

> Guidance for Claude (and other AI coding assistants) when working in this
> repository.

## Project summary

FED-GRAM is a Streamlit web app for downloading media (images, videos, GIFs,
audio) from 18+ social platforms. It uses a **detector → router → engine**
architecture: `detect_platform(url)` maps a URL to a platform key, and
`resolve(url, dest_dir)` runs the first matching engine. Every engine returns
a uniform `DownloadResult` of `MediaItem` objects.

## Tech stack

- **Language:** Python 3.11+ (uses `from __future__ import annotations` and
  `str | None` union syntax).
- **UI:** Streamlit (`app.py`).
- **Instagram backend:** `instaloader`.
- **Video backend:** `yt-dlp` (needs `ffmpeg` on the system for stream merging).
- **HTTP:** `requests`.
- **Image handling:** `Pillow` (via Streamlit).

## Key files

- `app.py` — the entire Streamlit UI. Session state holds `last_result` and
  `work_dir` (a temp dir per download).
- `downloaders/__init__.py` — `resolve()` and the ordered `_ENGINES` chain.
  `generic_engine` must always be last.
- `downloaders/detector.py` — `PLATFORM_HOSTS` registry and `detect_platform()`.
  Domain matching uses label boundaries (see `_host_matches`).
- `downloaders/models.py` — `DownloadResult` and `MediaItem` dataclasses.
  `result.ok` is `True` when there's no error and at least one item.
- `downloaders/<platform>_engine.py` — each engine exposes
  `can_handle(platform: str) -> bool` and
  `download(url, platform, dest_dir) -> DownloadResult`.

## Conventions to follow

- **Never raise out of an engine's `download()` for expected failures.** Put
  the human-readable message in `result.error` instead. The UI's safety net
  catches unexpected exceptions, but engines should be self-contained.
- **Wrap every network call in `try/except`.** A single broken source must not
  crash the app.
- **Create the dest dir** with `os.makedirs(dest_dir, exist_ok=True)` at the
  start of each engine.
- **Deduplicate media URLs** before downloading (use a `seen` set).
- **No API keys or secrets** in any engine. We rely on public page data and
  `yt-dlp`.
- **No new dependencies** without updating `requirements.txt` and explaining
  why in the PR.
- Keep docstrings; each engine's module docstring should explain its scraping
  strategy so future maintainers (human or AI) understand the approach.

## When adding a new platform engine

1. Add the platform's hosts to `PLATFORM_HOSTS` in `downloaders/detector.py`.
2. Create `downloaders/<name>_engine.py` with `can_handle()` and `download()`.
3. Import it and add it to `_ENGINES` in `downloaders/__init__.py` **before**
   `generic_engine`.
4. Add an icon entry in `_PLATFORM_ICON` in `app.py`.
5. Test with a real public URL; confirm a private/deleted URL returns a clean
  `result.error`.

## Known gotchas

- `ytdlp_engine._collect_entry_files` builds `MediaItem`s by globbing the dest
  dir for files prefixed with the entry id — don't assume the remote URL is
  populated; read bytes from `local_path` (the UI's `_read_bytes` prefers it).
- YouTube often requires a `cookies.txt` for bot-detection bypass; the UI
  sidebar uploader wires into `ytdlp_engine.set_cookies_file()`.
- `imgur_engine` converts `.gifv` → `.mp4`.
- HTML-scraping engines are fragile; if a platform changes its markup, the
  engine silently returns "No media found" rather than crashing.

## Testing

There is no automated test suite. Before declaring a change done:
1. `streamlit run app.py` launches with no import errors.
2. At least one real public URL works for the affected engine.
3. An unsupported URL falls through to `generic_engine`.
4. A private/invalid URL yields a clean error, not a traceback.

## Commit style

Prefer Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`,
`test:`. Keep commits focused and update `CHANGELOG.md` under `[Unreleased]`.
