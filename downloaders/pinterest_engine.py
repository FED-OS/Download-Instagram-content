"""
Pinterest downloader.

Pinterest pin pages embed the high-resolution image URL inside the HTML.
We fetch the page, look for known og:image / pin image patterns, and grab
the best-resolution version we can find.
"""
from __future__ import annotations

import os
import re

import requests

from .models import DownloadResult, MediaItem


_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
}


def can_handle(platform: str) -> bool:
    return platform == "pinterest"


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    os.makedirs(dest_dir, exist_ok=True)

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return DownloadResult(platform="pinterest", title="", error=f"Couldn't fetch pin: {exc}")

    html = resp.text

    # Try og:image first (usually a good-sized pin image).
    img_urls: list[str] = []
    for pattern in (
        r'property="og:image"\s+content="([^"]+)"',
        r'content="([^"]+)"\s+property="og:image"',
        r'"image_url":"([^"]+)"',
        r'"url":"(https://i\.pinimg\.com/[^"]+)"',
    ):
        for m in re.finditer(pattern, html):
            candidate = m.group(1).replace("\\u002F", "/").replace("\\/", "/")
            if candidate not in img_urls:
                img_urls.append(candidate)

    # Prefer originals.
    def score(u: str) -> int:
        s = 0
        if "originals" in u:
            s += 100
        if "/736x/" in u:
            s += 50
        if "/600x/" in u:
            s += 30
        return s

    img_urls.sort(key=score, reverse=True)

    title_match = re.search(r'property="og:title"\s+content="([^"]+)"', html)
    title = title_match.group(1) if title_match else "Pinterest pin"

    if not img_urls:
        return DownloadResult(platform="pinterest", title=title, error="No image found on this pin page.")

    items: list[MediaItem] = []
    for i, img_url in enumerate(img_urls[:8]):
        try:
            data = requests.get(img_url, headers=_HEADERS, timeout=30).content
            ext = "jpg"
            if ".png" in img_url:
                ext = "png"
            elif ".gif" in img_url:
                ext = "gif"
            elif ".webp" in img_url:
                ext = "webp"
            fname = f"fedgram_pinterest_{i+1}.{ext}"
            path = os.path.join(dest_dir, fname)
            with open(path, "wb") as fh:
                fh.write(data)
            items.append(MediaItem(
                kind="gif" if ext == "gif" else "image",
                url=img_url, local_path=path, filename=fname,
                mime=f"image/{ext}", thumbnail=img_url, title=title,
            ))
        except Exception:
            continue

    if not items:
        return DownloadResult(platform="pinterest", title=title, error="Found image URL but failed to download it.")

    return DownloadResult(platform="pinterest", title=title, items=items)
