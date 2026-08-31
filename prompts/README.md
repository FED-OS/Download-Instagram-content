# Prompts

Reusable AI prompts for working on FED-GRAM. These are starting points — adjust
to your needs. See [CLAUDE.md](../CLAUDE.md) and [AGENTS.md](../AGENTS.md) for
the conventions an AI assistant should follow when using them.

---

## add-platform-engine.md

```
Add a new download engine to FED-GRAM for the platform "<PLATFORM NAME>".

Context: FED-GRAM uses a detector → router → engine architecture. See
CLAUDE.md. Engines live in downloaders/<name>_engine.py and each exposes
can_handle(platform) -> bool and download(url, platform, dest_dir) -> DownloadResult.

Do the following:
1. Read downloaders/detector.py and add the platform's domains to PLATFORM_HOSTS.
2. Read downloaders/models.py to understand DownloadResult and MediaItem.
3. Create downloaders/<name>_engine.py with can_handle() and download().
   - Fetch the public page with requests and a desktop User-Agent.
   - Extract media URLs via og:image / og:video / platform-specific patterns.
   - Deduplicate URLs, download each to dest_dir, and build MediaItem objects.
   - Return a DownloadResult; put failures in result.error, never raise.
4. Import the engine in downloaders/__init__.py and add it to _ENGINES before generic_engine.
5. Add an icon to _PLATFORM_ICON in app.py.
6. Update README.md's platform list and CHANGELOG.md under [Unreleased] > Added.

Example public URL to test: <PASTE A REAL PUBLIC URL>
Verify: streamlit run app.py launches, the URL downloads, and an invalid URL returns a clean error.
```

---

## fix-broken-scraper.md

```
The <PLATFORM> engine in FED-GRAM is returning "No media found" for public URLs
that used to work. The platform likely changed its page markup.

Steps:
1. Read downloaders/<platform>_engine.py to see the current regex patterns.
2. Fetch the example URL with curl and inspect the HTML for where media URLs now live.
3. Update the regex patterns (keep multiple fallbacks — the project style).
4. Ensure dedup and error handling stay intact.
5. Test with the example URL and with an invalid URL.
6. Add a CHANGELOG.md entry under [Unreleased] > Fixed.

Example URL: <PASTE URL>
```

---

## add-tests.md

```
Add pytest tests for FED-GRAM's downloaders package.

Cover:
- detect_platform() for each entry in PLATFORM_HOSTS (positive cases) and a few
  negative cases (unknown domains, empty string, scheme-less URLs).
- The label-boundary matching so "t.co" does NOT match "reddit.com".
- Each engine's can_handle() returns True only for its platform.
- DownloadResult.ok is True only when there are items and no error.

Use fixture HTML files under tests/fixtures/ for the scraping engines rather
than hitting live sites. Do not introduce network calls in unit tests.
Place tests in tests/. Add pytest to requirements if a dev-requirements.txt is
preferred instead — ask if unsure.
```

---

## write-docs.md

```
Improve FED-GRAM's documentation. Read the current README.md, usage.md, and
FAQ.md first. Then:

- Make sure the supported-platforms list is accurate against downloaders/detector.py.
- Cross-link related docs where helpful (INSTALL ↔ usage ↔ FAQ ↔ SECURITY).
- Keep the tone friendly and practical; avoid duplicating content between files.
- Update CHANGELOG.md under [Unreleased] > Docs if anything user-facing changed.

Do not invent features that aren't in the code.
```
