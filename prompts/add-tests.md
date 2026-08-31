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
