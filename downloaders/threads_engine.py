"""
Threads (Meta) downloader.

Threads post pages embed og:image / og:video tags. We scrape those.
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
    return platform == "threads"


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    os.makedirs(dest_dir, exist_ok=True)

    try:
        resp = requests.get(url, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return DownloadResult(platform="threads", title="", error=f"Couldn't fetch Threads post: {exc}")

    html = resp.text

    media_urls: list[str] = []
    for pattern in (
        r'property="og:image"\s+content="([^"]+)"',
        r'property="og:video"\s+content="([^"]+)"',
        r'"image":"(https://scontent[^"]+)"',
        r'"video_url":"(https://[^"]+)"',
    ):
        for m in re.finditer(pattern, html):
            u = m.group(1).replace("\\u002F", "/").replace("\\/", "/")
            if u not in media_urls:
                media_urls.append(u)

    title_match = re.search(r'property="og:title"\s+content="([^"]+)"', html)
    desc_match = re.search(r'property="og:description"\s+content="([^"]+)"', html)
    title = title_match.group(1) if title_match else "Threads post"

    if not media_urls:
        return DownloadResult(platform="threads", title=title, error="No media found (post may be text-only or private).")

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
        ext = "jpg"
        if ".mp4" in low:
            ext = "mp4"
        elif ".png" in low:
            ext = "png"
        elif ".webp" in low:
            ext = "webp"
        fname = f"fedgram_threads_{i}.{ext}"
        path = os.path.join(dest_dir, fname)
        with open(path, "wb") as fh:
            fh.write(data)
        kind = "video" if ext == "mp4" else "image"
        items.append(MediaItem(
            kind=kind, url=murl, local_path=path, filename=fname,
            mime=f"{'video' if ext=='mp4' else 'image'}/{ext}",
            thumbnail=murl if ext != "mp4" else None, title=title,
        ))

    if not items:
        return DownloadResult(platform="threads", title=title, error="Found media but failed to download.")
    return DownloadResult(
        platform="threads", title=title,
        description=desc_match.group(1) if desc_match else None, items=items,
    )
