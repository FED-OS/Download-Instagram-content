# Roadmap

This is a living document describing the direction of FED-GRAM. It is not a
commitment — items may be reprioritized or dropped — but it communicates what
the maintainers currently intend to work on.

Status legend: ✅ done · 🚧 in progress · 📋 planned · 💡 idea

---

## v1.1 ✅ (released 2026-08-30)

- ✅ Universal `downloaders/` engine architecture.
- ✅ 18 supported platforms.
- ✅ Video & audio via `yt-dlp`.
- ✅ Instagram Reels.
- ✅ Optional cookies upload for YouTube.
- ✅ Batch ZIP download.

## v1.2 🚧 (near-term)

- 🚧 Formal test suite (pytest) covering `detect_platform`, each engine's
  `can_handle`, and `DownloadResult` correctness against fixture HTML.
- 🚧 Better error messaging taxonomy — distinguish "private", "deleted",
  "rate-limited", and "markup changed" where possible.
- 📋 Configurable download quality/format selector for `yt-dlp` (e.g. best mp4
  vs. audio-only).
- 📋 Progress feedback for large video downloads.
- 📋 Update README/FAQ to reflect the 18-platform reality (done in this pass).

## v1.3 📋 (mid-term)

- 📋 Optional API-key engines for **Imgur** (Client-ID) and **Reddit** (OAuth)
  for more reliable, less fragile fetching than HTML scraping.
- 📋 **TikTok slideshow** image extraction (currently goes through yt-dlp as a
  playlist — verify and polish).
- 📋 Per-platform rate-limit awareness with simple backoff for
  `instaloader`/scraping engines.
- 📋 Download history (session-scoped) so users can re-download without
  re-pasting.
- 📋 Docker image and `docker-compose` for one-command self-hosting.

## v2.0 💡 (longer-term ideas)

- 💡 Pluggable engine registry so third parties can add engines without forking.
- 💡 Async/concurrent multi-URL batch input (paste several links at once).
- 💡 Optional browser extension that sends the current tab's URL to a running
  FED-GRAM instance.
- 💡 Headless CLI mode (`python -m fedgram <url>`) reusing the same engines.
- 💡 Internationalization (i18n) of the Streamlit UI.

---

## Non-goals

To keep scope manageable, FED-GRAM will **not** aim to:

- Download **private** or login-walled content (beyond the optional cookies
  mechanism for personal YouTube access).
- Support **bulk / automated mass scraping**. This is a personal-use tool and
  bulk features would violate platform ToS and risk legal exposure.
- Store or re-host downloaded media. Everything is ephemeral and local.
- Become a general-purpose archival system. Use dedicated tools for that.

---

## How to influence the roadmap

Open a [Discussion](https://github.com/FED-OS/FED-GRAM/discussions) or a
[Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) describing your
use case. Well-argued proposals with real demand tend to move up the list.
Maintainers prioritize based on demand, maintenance burden, and ethical
considerations.
