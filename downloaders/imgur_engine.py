"""
Imgur downloader.

Handles single images, gifs, and albums (imgur.com/a/... and imgur.com/gallery/...).
Uses the Imgur public page scraping approach (og:image / json embed) so no
API key is required.
"""
from __future__ import annotations

import os
import re
import json

import requests

from .models import DownloadResult, MediaItem


_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0 Safari/537.36"),
}


def can_handle(platform: str) -> bool:
    return platform == "imgur"


def _save(url: str, dest_dir: str, idx: int) -> MediaItem | None:
    try:
        data = requests.get(url, headers=_HEADERS, timeout=30).content
    except Exception:
        return None
    ext = "jpg"
    low = url.lower().split("?")[0]
    if low.endswith(".png"):
        ext = "png"
    elif low.endswith(".gif"):
        ext = "gif"
    elif low.endswith(".webp"):
        ext = "webp"
    elif low.endswith(".mp4"):
        ext = "mp4"
    fname = f"fedgram_imgur_{idx}.{ext}"
    path = os.path.join(dest_dir, fname)
    with open(path, "wb") as fh:
        fh.write(data)
    kind = "video" if ext == "mp4" else ("gif" if ext == "gif" else "image")
    return MediaItem(
        kind=kind, url=url, local_path=path, filename=fname,
        mime=f"{'video' if ext=='mp4' else 'image'}/{ext}",
        thumbnail=url if ext != "mp4" else None,
    )


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    os.makedirs(dest_dir, exist_ok=True)

    # Normalise: strip query, get the id portion.
    clean = url.split("?")[0].rstrip("/")

    try:
        resp = requests.get(clean, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return DownloadResult(platform="imgur", title="", error=f"Couldn't fetch Imgur page: {exc}")

    html = resp.text
    title_match = re.search(r'<title>([^<]+)</title>', html)
    title = title_match.group(1).strip() if title_match else "Imgur post"

    media_urls: list[str] = []

    # Album: look for the "image" array embedded in the page JSON.
    album_match = re.search(r'image\s*:\s*(\[.*?\])\s*,\s*group', html, re.DOTALL)
    if album_match:
        try:
            arr = json.loads(album_match.group(1))
            for obj in arr:
                link = obj.get("link") or obj.get("gifv") or obj.get("mp4")
                if link:
                    # gifv -> mp4
                    link = link.replace(".gifv", ".mp4")
                    media_urls.append(link)
        except Exception:
            pass

    # Fallback: og:image / og:video.
    if not media_urls:
        for pattern in (
            r'property="og:image"\s+content="([^"]+)"',
            r'property="og:video"\s+content="([^"]+)"',
            r'<meta[^>]+name="twitter:image"[^>]+content="([^"]+)"',
        ):
            for m in re.finditer(pattern, html):
                media_urls.append(m.group(1))

    # Direct i.imgur.com links passed straight in.
    if not media_urls and "i.imgur.com" in url:
        media_urls.append(url)

    if not media_urls:
        return DownloadResult(platform="imgur", title=title, error="No media found on this Imgur page.")

    items: list[MediaItem] = []
    for i, murl in enumerate(media_urls[:20], start=1):
        item = _save(murl, dest_dir, i)
        if item:
            item.title = title
            items.append(item)

    if not items:
        return DownloadResult(platform="imgur", title=title, error="Found media URLs but failed to download.")

    return DownloadResult(platform="imgur", title=title, items=items)
