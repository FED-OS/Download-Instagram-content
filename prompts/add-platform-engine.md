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
