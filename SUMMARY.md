# Summary

> A one-page overview of FED-GRAM for quick orientation.

## What it is

FED-GRAM is a free, open-source **Streamlit** web app that downloads media
(images, videos, GIFs, audio) from **18+ social platforms** by pasting a
single link. It auto-detects the platform and routes the URL to the right
backend engine. Self-hosted, no telemetry, MIT licensed.

## Supported platforms

Instagram, Threads, TikTok, YouTube, Reddit, Twitter/X, Facebook, Pinterest,
Twitch, Vimeo, Dailymotion, SoundCloud, Imgur, Bluesky, Tumblr, Snapchat,
LinkedIn, Streamable — plus a generic fallback for any URL with embeddable
media or a direct media link.

## Architecture

A **detector → router → engine** pipeline:

- `downloaders/detector.py` — URL → platform key.
- `downloaders/__init__.py` — `resolve()` runs the first matching engine.
- `downloaders/<platform>_engine.py` — each engine returns a uniform
  `DownloadResult` of `MediaItem`s.
- `generic_engine` — always-last catch-all.

Engines: `instaloader` (Instagram), `yt-dlp` (video platforms), and HTML/og:
scrapers (Pinterest, Imgur, Tumblr, Threads, generic).

## Quick start

```bash
git clone https://github.com/FED-OS/FED-GRAM.git
cd FED-GRAM
pip install -r requirements.txt
streamlit run app.py      # → http://localhost:8501
```

Video downloads need `ffmpeg` installed system-wide.

## Key facts

| | |
|---|---|
| **License** | MIT ([LICENSE](LICENSE)) |
| **Language** | Python 3.11+ |
| **UI** | Streamlit |
| **Video backend** | yt-dlp |
| **Instagram backend** | instaloader |
| **Current version** | 1.1.0 (see [CHANGELOG.md](CHANGELOG.md)) |
| **Repo** | https://github.com/FED-OS/FED-GRAM |

## Important docs

| Doc | For |
|-----|-----|
| [README.md](README.md) | Project overview & quick start |
| [INSTALL.md](INSTALL.md) | Step-by-step install |
| [usage.md](usage.md) | How to use the app |
| [BUILD.md](BUILD.md) | Build/verify/package |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Cloud, Docker, reverse proxy |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [SECURITY.md](SECURITY.md) | Reporting vulnerabilities, hardening |
| [FAQ.md](FAQ.md) | Common questions |
| [ROADMAP.md](ROADMAP.md) | Future plans |
| [ADR.md](ADR.md) | Architecture decisions |
| [CLAUDE.md](CLAUDE.md) / [AGENTS.md](AGENTS.md) | AI assistant guidance |

## Ethics

Public content only. Personal use. Respect each platform's Terms of Service
and copyright. No bulk scraping. See [NOTICE.md](NOTICE.md) and
[SECURITY.md](SECURITY.md).

## Support

Issues, feature requests, and discussions happen on GitHub. See
[SUPPORT.md](SUPPORT.md). Donations welcome at
[Ko-fi](https://ko-fi.com/YOUR_USERNAME). 💛
