# Platform Detection

How FED-GRAM maps a URL to a platform key.

## The registry

`downloaders/detector.py` defines `PLATFORM_HOSTS`, an ordered list of tuples:

```python
("platform_key", "Display Name", ["domain1.com", "domain2.co"])
```

The first host that matches wins, so order matters (put more specific
platforms before generic ones).

## Matching algorithm

`detect_platform(url)`:

1. Strips and ensures the URL has a scheme (`https://` is prepended if missing)
   so `urlparse` behaves.
2. Extracts the `netloc`, lowercases it, and strips port and userinfo.
3. For each registered candidate domain, checks `_host_matches(host, candidate)`.

`_host_matches` compares on **domain-label boundaries**:

```python
def _host_matches(host, candidate):
    host = host.lower(); cand = candidate.lower()
    if host == cand: return True
    return host.endswith("." + cand) or host.endswith("/" + cand)
```

This is important: a naive `endswith` would let `"t.co"` match inside
`"reddit.com"`. The label-boundary check (`"." + cand`) prevents that.

## Adding a new domain

1. Pick a `platform_key` (lowercase, no spaces).
2. Add a tuple to `PLATFORM_HOSTS` with all the domains that host that platform
   (including shorteners like `youtu.be`, `pin.it`, `redd.it`).
3. Place it in a sensible position (specific before generic).
4. `PLATFORMS` (the pretty `{key: name}` dict used by the UI) is derived
   automatically — no separate update needed.

## Testing detection

```python
from downloaders import detect_platform
assert detect_platform("https://youtu.be/abc") == "youtube"
assert detect_platform("https://www.tiktok.com/@u/video/1") == "tiktok"
assert detect_platform("https://reddit.com/r/x") == "reddit"
assert detect_platform("https://t.co/abc") == "twitter"   # not reddit!
assert detect_platform("") is None
assert detect_platform("https://example.com") is None
```

## Why a key, not the URL?

Engines are matched by a canonical **platform key**, not by re-parsing the URL.
This decouples detection from download logic and lets one engine (e.g.
`ytdlp_engine`) handle many platforms via a set membership check.
