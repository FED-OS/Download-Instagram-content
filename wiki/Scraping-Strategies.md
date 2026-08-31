# Scraping Strategies

The HTML-scraping engines (Pinterest, Imgur, Tumblr, Threads, generic) share a
common approach. This page documents the patterns and the rationale.

## Why scrape instead of using APIs?

FED-GRAM aims for **zero-config** usage — no API keys, no sign-ups. Public
pages embed media URLs in standard OpenGraph (`og:image`, `og:video`) and
Twitter (`twitter:image`) meta tags, plus platform-specific embedded JSON.
Scraping these is enough for the common case and keeps the tool simple.

The trade-off is **fragility**: platforms change markup. We mitigate this with
multiple fallback patterns per engine and the `generic_engine` catch-all.

## Standard header

Every scraper sends a desktop User-Agent to avoid being served a stripped-down
mobile page:

```python
_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
}
```

## Extraction patterns (in priority order)

1. **`og:video`** before `og:image` — videos are higher value and less commonly
   duplicated.
2. **`og:image`** — the canonical preview image.
3. **`twitter:image`** — fallback when `og:image` is missing.
4. **Platform-specific JSON** — e.g. Imgur's embedded `image:[...]` array,
   Pinterest's `"image_url":"..."`, Tumblr's `64.media.tumblr.com` `src`/`data-src`.

## JSON-escape unescaping

Meta/Imgur/Pinterest embed URLs in JSON with `\u002F` for `/` and `\/`.
Always unescape:

```python
url = m.group(1).replace("\\u002F", "/").replace("\\/", "/")
```

## Resolution preference (Pinterest example)

Pinterest serves multiple resolutions of the same pin. Prefer the best:

```python
def score(u):
    s = 0
    if "originals" in u: s += 100
    if "/736x/" in u:    s += 50
    if "/600x/" in u:    s += 30
    return s
img_urls.sort(key=score, reverse=True)
```

## gifv → mp4 (Imgur)

Imgur's `.gifv` is really an MP4 wrapper. Normalize before downloading:

```python
link = link.replace(".gifv", ".mp4")
```

## Deduplication

Always dedupe media URLs before fetching (a `seen` set) — pages often repeat
the same image in `og:image`, `twitter:image`, and inline `src`.

## Caps

Limit to a reasonable number of items (engines use `[:20]`) to avoid runaway
downloads on huge albums.

## When scraping breaks

A platform change typically produces a clean `"No media found"` error rather
than a crash (because engines return `DownloadResult` with `error`). The fix
flow is in [`prompts/fix-broken-scraper.md`](../prompts/fix-broken-scraper.md).
The roadmap includes optional API-key engines for Imgur and Reddit (v1.3) to
improve reliability where users opt in.
