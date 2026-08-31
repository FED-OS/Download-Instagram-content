# Engine Development Guide

A complete walkthrough for adding a new platform engine to FED-GRAM.

## The contract

Every engine is a Python module under `downloaders/` exposing two functions:

```python
def can_handle(platform: str) -> bool: ...
def download(url: str, platform: str, dest_dir: str) -> DownloadResult: ...
```

- `can_handle` returns `True` only for this engine's platform key.
- `download` **never raises** for expected failures — it returns a
  `DownloadResult` with `error` set. Unexpected exceptions are caught by the
  UI's safety net, but engines should be self-contained.

## Step 1 — Register the platform

Edit `downloaders/detector.py` and add an entry to `PLATFORM_HOSTS`:

```python
("yourplatform", "Your Platform", ["yourplatform.com", "yp.co"]),
```

The list is ordered; the first host match wins. Domain matching uses
label boundaries (see [Platform-Detection](Platform-Detection.md)) so choose
distinctive root domains.

## Step 2 — Create the engine module

`downloaders/yourplatform_engine.py`:

```python
"""Your Platform downloader — scrape og:image / embedded JSON for media URLs."""
from __future__ import annotations

import os, re
import requests
from .models import DownloadResult, MediaItem

_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
}

def can_handle(platform: str) -> bool:
    return platform == "yourplatform"

def download(url, platform, dest_dir) -> DownloadResult:
    os.makedirs(dest_dir, exist_ok=True)
    try:
        resp = requests.get(url, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return DownloadResult(platform=platform, title="", error=f"Couldn't fetch: {exc}")

    html = resp.text
    media_urls: list[str] = []
    for pattern in (r'property="og:image"\s+content="([^"]+)"',
                    r'property="og:video"\s+content="([^"]+)"'):
        for m in re.finditer(pattern, html):
            if m.group(1) not in media_urls:
                media_urls.append(m.group(1))

    if not media_urls:
        return DownloadResult(platform=platform, title="Your Platform",
                              error="No media found on this page.")

    items: list[MediaItem] = []
    seen = set()
    for i, murl in enumerate(media_urls[:20], start=1):
        if murl in seen:
            continue
        seen.add(murl)
        try:
            data = requests.get(murl, headers=_HEADERS, timeout=30).content
        except Exception:
            continue
        low = murl.lower().split("?")[0]
        ext = "mp4" if ".mp4" in low else "jpg"
        fname = f"fedgram_yourplatform_{i}.{ext}"
        path = os.path.join(dest_dir, fname)
        with open(path, "wb") as fh:
            fh.write(data)
        kind = "video" if ext == "mp4" else "image"
        items.append(MediaItem(kind=kind, url=murl, local_path=path,
                               filename=fname, mime=f"{'video' if ext=='mp4' else 'image'}/{ext}",
                               thumbnail=murl if ext != "mp4" else None))

    if not items:
        return DownloadResult(platform=platform, title="Your Platform",
                              error="Found media but failed to download.")
    return DownloadResult(platform=platform, title="Your Platform", items=items)
```

## Step 3 — Register the engine

In `downloaders/__init__.py`:

```python
from . import (..., yourplatform_engine, ...)
_ENGINES = [..., yourplatform_engine, generic_engine]  # before generic!
```

## Step 4 — Add a UI icon

In `app.py`, add to `_PLATFORM_ICON`:

```python
"yourplatform": "🟢",
```

## Step 5 — Test

1. `streamlit run app.py` launches with no import error.
2. A real public URL from the platform downloads successfully.
3. An invalid/private URL returns a clean error, not a traceback.

## Step 6 — Document

- Add the platform to `README.md`'s supported list.
- Add a `CHANGELOG.md` entry under `[Unreleased] > Added`.

That's it. See [Scraping-Strategies](Scraping-Strategies.md) for robust
extraction patterns and [Architecture](Architecture.md) for the big picture.
