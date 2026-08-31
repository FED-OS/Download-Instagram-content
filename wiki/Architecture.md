# Architecture

FED-GRAM's design in depth. For the decision rationale, see [../ADR.md](../ADR.md).

## Pipeline

```
URL ──▶ detect_platform() ──▶ platform key
                                   │
                                   ▼
              resolve(url, dest_dir) iterates _ENGINES
                                   │
              first engine with can_handle(platform) == True
                                   │
                                   ▼
              engine.download(url, platform, dest_dir)
                                   │
                                   ▼
                         DownloadResult[MediaItem...]
                                   │
                                   ▼
                         Streamlit UI renders + downloads
```

## Components

### `downloaders/detector.py`
Pure function `detect_platform(url) -> str | None`. No I/O. The `PLATFORM_HOSTS`
registry and label-boundary `_host_matches` live here. See
[Platform-Detection](Platform-Detection.md).

### `downloaders/models.py`
Two dataclasses:
- `MediaItem` — `kind`, `url`, `filename`, `local_path`, `thumbnail`, `title`,
  `mime`. Property `has_local_file`.
- `DownloadResult` — `platform`, `title`, `author`, `description`, `items`,
  `error`. Property `ok` = no error and ≥1 item.

### `downloaders/__init__.py`
`_ENGINES` is the ordered list. `resolve()` loops it. `generic_engine` is
last and always matches. This is the single place to register a new engine.

### Engines
Each module exposes `can_handle` + `download`. Three families:
- **Library-backed:** `instagram_engine` (instaloader), `ytdlp_engine` (yt-dlp).
- **Scrapers:** `pinterest_engine`, `imgur_engine`, `tumblr_engine`,
  `threads_engine`. See [Scraping-Strategies](Scraping-Strategies.md).
- **Fallback:** `generic_engine` — direct media links (by extension and
  Content-Type) + `og:`/`twitter:` scrape.

### `app.py`
The Streamlit UI. Holds `last_result` and `work_dir` (a per-download temp dir)
in session state. The sidebar lists platforms and hosts the optional cookies
uploader (wired to `ytdlp_engine.set_cookies_file()`). Results render in a
responsive grid with per-item and batch-ZIP download buttons.

## Data flow notes

- Engines write files to `dest_dir` and set `MediaItem.local_path`. The UI's
  `_read_bytes` prefers `local_path`, falling back to `item.url` only if the
  file is missing.
- `ytdlp_engine` builds `MediaItem`s by **globbing** `dest_dir` for files
  prefixed with the yt-dlp entry id (yt-dlp picks the final extension). The
  remote URL is left empty; bytes come from disk.
- Multi-item results (carousels, albums) get a ZIP bundle button built in the
  UI from the local files.

## Design properties

- **Extensible:** a new platform is one module + two registration lines.
- **Decoupled:** the UI knows nothing about per-platform fetching.
- **Resilient:** expected failures become clean `result.error`; unexpected
  ones are caught by the UI safety net.
- **Zero-config:** no API keys for the common case; cookies are opt-in for
  YouTube.
