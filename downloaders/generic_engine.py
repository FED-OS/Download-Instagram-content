"""
Generic fallback downloader.

If the URL doesn't match any dedicated engine, we try to scrape the page for
embedded media (og:image / og:video / direct image link). This catches
lesser-known sites, direct media links, and LinkedIn posts.
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
    # Always available as a last resort.
    return True


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    os.makedirs(dest_dir, exist_ok=True)
    clean = url.strip()
    if not clean.startswith(("http://", "https://")):
        clean = "https://" + clean
    # Strip query string for extension detection.
    low = clean.lower().split("?")[0]
    low = low.split("#")[0]

    # Direct media link?
    if low.endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".mp4", ".webm")):
        try:
            data = requests.get(clean, headers=_HEADERS, timeout=30).content
        except Exception as exc:
            return DownloadResult(platform=platform, title="", error=f"Couldn't download direct media: {exc}")
        ext = low.rsplit(".", 1)[-1]
        kind = "video" if ext in ("mp4", "webm") else ("gif" if ext == "gif" else "image")
        fname = f"fedgram_direct.{ext}"
        path = os.path.join(dest_dir, fname)
        with open(path, "wb") as fh:
            fh.write(data)
        return DownloadResult(
            platform=platform, title="Direct media",
            items=[MediaItem(kind=kind, url=clean, local_path=path, filename=fname,
                             mime=f"{'video' if kind=='video' else 'image'}/{ext}",
                             thumbnail=clean if kind != "video" else None)],
        )

    try:
        resp = requests.get(clean, headers=_HEADERS, timeout=30)
        resp.raise_for_status()
    except Exception as exc:
        return DownloadResult(platform=platform, title="", error=f"Couldn't fetch page: {exc}")

    ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip().lower()

    # If the URL itself returns a media file (e.g. an image CDN without an
    # extension), save it directly instead of trying to parse HTML.
    if ctype.startswith(("image/", "video/", "audio/")):
        ext = "bin"
        if "jpeg" in ctype or "jpg" in ctype:
            ext = "jpg"
        elif "png" in ctype:
            ext = "png"
        elif "gif" in ctype:
            ext = "gif"
        elif "webp" in ctype:
            ext = "webp"
        elif "mp4" in ctype:
            ext = "mp4"
        elif "webm" in ctype:
            ext = "webm"
        elif "mpeg" in ctype or "mp3" in ctype:
            ext = "mp3"
        elif "ogg" in ctype:
            ext = "ogg"
        elif "wav" in ctype:
            ext = "wav"
        kind = "video" if ctype.startswith("video") else ("audio" if ctype.startswith("audio") else ("gif" if ext == "gif" else "image"))
        fname = f"fedgram_direct.{ext}"
        path = os.path.join(dest_dir, fname)
        with open(path, "wb") as fh:
            fh.write(resp.content)
        return DownloadResult(
            platform=platform, title="Direct media",
            items=[MediaItem(kind=kind, url=clean, local_path=path, filename=fname,
                             mime=ctype or f"{'video' if kind=='video' else 'image'}/{ext}",
                             thumbnail=clean if kind in ("image", "gif") else None)],
        )

    html = resp.text
    media_urls: list[str] = []
    for pattern in (
        r'property="og:video"\s+content="([^"]+)"',
        r'property="og:image"\s+content="([^"]+)"',
        r'name="twitter:image"\s+content="([^"]+)"',
    ):
        for m in re.finditer(pattern, html):
            u = m.group(1)
            if u not in media_urls:
                media_urls.append(u)

    title_match = re.search(r'<title>([^<]+)</title>', html)
    title = title_match.group(1).strip() if title_match else "Media"

    if not media_urls:
        return DownloadResult(platform=platform, title=title,
                              error="No embeddable media found on this page.")

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
        ml = murl.lower().split("?")[0]
        ext = "jpg"
        if ".mp4" in ml:
            ext = "mp4"
        elif ".png" in ml:
            ext = "png"
        elif ".gif" in ml:
            ext = "gif"
        elif ".webp" in ml:
            ext = "webp"
        fname = f"fedgram_generic_{i}.{ext}"
        path = os.path.join(dest_dir, fname)
        with open(path, "wb") as fh:
            fh.write(data)
        kind = "video" if ext == "mp4" else ("gif" if ext == "gif" else "image")
        items.append(MediaItem(
            kind=kind, url=murl, local_path=path, filename=fname,
            mime=f"{'video' if ext=='mp4' else 'image'}/{ext}",
            thumbnail=murl if ext != "mp4" else None, title=title,
        ))

    if not items:
        return DownloadResult(platform=platform, title=title, error="Found media but failed to download.")
    return DownloadResult(platform=platform, title=title, items=items)
