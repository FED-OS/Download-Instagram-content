# Changelog

All notable changes to FED-GRAM are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Pending
- Formal test suite.
- Per-platform rate-limit backoff.
- Optional API-key engines for Imgur/Reddit.

---

## [1.1.0] — 2026-08-30

### Added
- **Universal multi-platform architecture**: new `downloaders/` package with a detector → router → engine pipeline.
- **18 supported platforms**: Instagram, Threads, TikTok, YouTube, Reddit, Twitter/X, Facebook, Pinterest, Twitch, Vimeo, Dailymotion, SoundCloud, Imgur, Bluesky, Tumblr, Snapchat, LinkedIn, Streamable.
- **Video & audio support** via `yt-dlp` (YouTube, TikTok, Twitch, Vimeo, SoundCloud, Reddit, Streamable, Bluesky, and more).
- **Instagram Reels** download (in addition to image posts and carousels).
- **Optional `cookies.txt` upload** in the sidebar for YouTube age-restricted / bot-detected content.
- **Batch ZIP download** for multi-item results (carousels and albums).
- Live platform detection badge next to the URL input.
- Responsive wide-layout UI with media preview grid (up to 3 columns).
- `.streamlit/config.toml` for headless, CORS-free, 0.0.0.0 deployment.
- New dependencies: `yt-dlp`, `Pillow`.

### Fixed
- `AttributeError: 'str' object has no attribute 'kind'` in `ytdlp_engine._collect_entry_files` — the image-existence check now iterates `items` (`MediaItem` objects) instead of `media_files` (path strings).
- `generic_engine` now handles **direct media URLs** (by extension *and* by `Content-Type` sniffing) instead of only `og:` meta tags, fixing the "No embeddable media found" failure on direct image/video links.
- `imgur_engine` normalises `.gifv` → `.mp4` for proper video playback.
- Cleaner, trimmed error messages for `yt-dlp` `DownloadError` (stripped `ERROR:` / `WARNING:` prefixes) with a helpful cookies hint for YouTube sign-in walls.

### Changed
- `app.py` rewritten from a 70-line Instagram-only script to a full multi-platform UI (~210 lines).
- Page layout changed from `centered` to `wide`.
- `requirements.txt` updated to include `yt-dlp` and `Pillow` with lower-bound pins.

### Removed
- None.

---

## [1.0.0] — 2026-08-26

### Added
- Initial release: a lightweight Streamlit app to download **images** from **public Instagram posts**.
- Supports single-image posts and multi-image **carousels**.
- One-click download buttons with `instaloader` + `requests`.
- Friendly error handling for rate-limiting and private/deleted posts.
- MIT license, README, `.gitignore`, and Streamlit Community Cloud deployment instructions.
- Dependencies: `streamlit`, `instaloader`, `requests`.

### Limitations (documented)
- Public posts only.
- Images only (no Reels/video).
- Subject to Instagram rate-limiting under heavy use.
