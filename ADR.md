# Architecture Decision Records (ADR)

This file records significant architectural decisions made in FED-GRAM, along
with their context and consequences. The format follows the ADR pattern
popularized by Michael Nygard. New ADRs are appended; existing ones are never
deleted — superseded ones are marked as such.

## ADR-0001 — Engine-plugin architecture with a router chain

**Status:** Accepted
**Date:** 2026-08-30

### Context

The original FED-GRAM (v1.0) was a single 70-line `app.py` that only handled
Instagram images via `instaloader`. As we expanded to video platforms and more
social sites, a single monolithic handler would become unmaintainable and
would mix very different fetching strategies (library-based for Instagram,
HTML-scraping for Pinterest/Tumblr, yt-dlp for video sites).

### Decision

Adopt a **detector → router → engine** architecture:

- `detector.py` maps a URL to a canonical platform key.
- `__init__.py`'s `resolve()` iterates an ordered list of engine modules; the
  first whose `can_handle(platform)` is `True` wins.
- Each engine is a self-contained module implementing
  `can_handle(platform) -> bool` and
  `download(url, platform, dest_dir) -> DownloadResult`.
- A `generic_engine` with `can_handle() -> True` is always last, acting as a
  universal fallback.
- All engines return the shared `DownloadResult` / `MediaItem` dataclasses, so
  the UI renders results uniformly.

### Consequences

**Positive:** Adding a platform is a localized change (new module + two-line
registration). Engines are independently testable. The UI is decoupled from
fetching strategy. Failure of one engine's strategy doesn't affect others.

**Negative:** Engines must discipline themselves to return `DownloadResult`
rather than raising. The scraping engines share boilerplate (headers,
dedup, save-to-disk) — some future refactor could extract a shared helper,
but for now duplication is preferred over premature abstraction.

---

## ADR-0002 — Use yt-dlp for all video platforms

**Status:** Accepted
**Date:** 2026-08-30

### Context

Supporting YouTube, TikTok, Twitch, Vimeo, Dailymotion, SoundCloud, Reddit
video, Streamable, Bluesky, etc. individually would require a large amount of
bespoke, fragile code. These sites use signed URLs, DASH/HLS, and change
frequently.

### Decision

Route all video-capable platforms through **`yt-dlp`** via a single
`ytdlp_engine`. yt-dlp already supports these sites, handles format
selection, merging, and updates independently of FED-GRAM.

### Consequences

**Positive:** One engine covers 13+ platforms. Format/merging handled for us.
Community-maintained extractors keep up with platform changes.

**Negative:** Adds a heavy dependency and a system dependency on `ffmpeg` for
stream merging. YouTube's bot-detection requires the optional cookies
mechanism (ADR-0003). yt-dlp error messages needed trimming for a clean UI.

---

## ADR-0003 — Optional cookies.txt upload for YouTube

**Status:** Accepted
**Date:** 2026-08-30

### Context

YouTube increasingly blocks unauthenticated yt-dlp downloads with a "Sign in
to confirm you're not a bot" wall. There is no reliable server-side workaround
that doesn't involve user credentials.

### Decision

Add a sidebar **cookies.txt uploader** (Netscape format) that writes to the
system temp directory and is passed to yt-dlp via `ytdlp_engine.set_cookies_file()`.
Cookies are git-ignored and never committed.

### Consequences

**Positive:** Users can self-serve a fix for YouTube without us handling
credentials. Keeps FED-GRAM dependency-free of auth infrastructure.

**Negative:** Users must export cookies themselves (minor friction). A
cookies.txt is sensitive — the security policy (SECURITY.md) documents the
git-ignore and temp-only storage, and warns against using it on shared/public
instances.

---

## ADR-0004 — Scraping engines rely on regex over page HTML/JSON, no API keys

**Status:** Accepted
**Date:** 2026-08-30

### Context

Pinterest, Tumblr, Threads, Imgur, and the generic fallback need media URLs
that are embedded in the page. We want FED-GRAM to work with zero
configuration and no API-key signup for the common case.

### Decision

Scraping engines fetch the public page HTML and extract media via regex
against `og:image`, `og:video`, `twitter:image`, and platform-specific
embedded JSON patterns. No API keys are required.

### Consequences

**Positive:** Zero-config, instant usability. No secret management.

**Negative:** Fragile — platforms can change markup and break an engine
silently (it returns "No media found" rather than crashing). Mitigations:
multiple fallback regex patterns per engine, and the `generic_engine`
catch-all. The roadmap includes optional API-key engines (v1.3) for Imgur and
Reddit to improve reliability where users opt in.
