"""
yt-dlp powered engine.

yt-dlp supports a huge range of sites out of the box, so this single engine
covers YouTube, TikTok, Twitter/X, Facebook, Twitch, Vimeo, Dailymotion,
SoundCloud, Reddit (video posts), Streamable, Bluesky and many others.

We ask yt-dlp to download into a temp directory (no playlist explosion) and
report back MediaItems that the Streamlit UI can preview + offer for download.
"""
from __future__ import annotations

import os
import glob
from typing import Optional

try:
    import yt_dlp
except ImportError:  # pragma: no cover - handled at runtime
    yt_dlp = None  # type: ignore[assignment]

from .models import DownloadResult, MediaItem


# Optional cookies file path. Set via set_cookies_file() from the UI when the
# user uploads a Netscape-format cookies.txt (needed for YouTube age-restricted
# or bot-detected content). None means no cookies are used.
_cookies_file: Optional[str] = None


def set_cookies_file(path: Optional[str]) -> None:
    """Set (or clear) the cookies file used for yt-dlp downloads."""
    global _cookies_file
    _cookies_file = path if (path and os.path.exists(path)) else None


def get_cookies_file() -> Optional[str]:
    return _cookies_file


# Friendly names for the platforms we route through yt-dlp.
_YTDLP_PLATFORMS = {
    "youtube", "tiktok", "twitter", "facebook", "twitch", "vimeo",
    "dailymotion", "soundcloud", "reddit", "streamable", "bluesky",
    "snapchat", "linkedin",
}


_MIME_BY_EXT = {
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mkv": "video/x-matroska",
    ".m4a": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".opus": "audio/ogg",
    ".ogg": "audio/ogg",
    ".wav": "audio/wav",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def _kind_for_ext(ext: str) -> str:
    ext = ext.lower()
    if ext in (".mp4", ".webm", ".mkv", ".mov", ".avi"):
        return "video"
    if ext in (".mp3", ".m4a", ".opus", ".ogg", ".wav", ".aac", ".flac"):
        return "audio"
    if ext == ".gif":
        return "gif"
    if ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
        return "image"
    return "file"


def can_handle(platform: str) -> bool:
    return platform in _YTDLP_PLATFORMS


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    if yt_dlp is None:
        return DownloadResult(
            platform=platform, title="",
            error="yt-dlp is not installed. Add 'yt-dlp' to requirements.txt and redeploy.",
        )
    os.makedirs(dest_dir, exist_ok=True)
    outtmpl = os.path.join(dest_dir, "%(id)s.%(ext)s")

    ydl_opts = {
        "outtmpl": outtmpl,
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "skip_download": False,
        # Prefer a single progressive mp4 when available for easy in-browser
        # playback, otherwise let yt-dlp merge best video+audio.
        "format": "best*[ext=mp4]/best/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noprogress": True,
        "concurrent_fragment_downloads": 4,
        "retries": 3,
        "fragment_retries": 3,
        "geo_bypass": True,
        # For audio-only platforms (soundcloud) prefer extracting to mp3.
        "postprocessors": [],
    }

    # Attach cookies if the user provided a cookies.txt (e.g. for YouTube).
    if _cookies_file:
        ydl_opts["cookiefile"] = _cookies_file

    info: dict = {}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except yt_dlp.utils.DownloadError as exc:
        msg = str(exc)
        # Trim noisy yt-dlp prefixes for a cleaner UI message.
        for prefix in ("ERROR: ", "WARNING: "):
            if msg.startswith(prefix):
                msg = msg[len(prefix):]
        # Give a helpful hint for YouTube's bot-detection / sign-in wall.
        if "Sign in to confirm" in msg or "cookies" in msg.lower():
            msg = (msg + "  —  Tip: upload a cookies.txt file (sidebar) "
                    "exported from your browser to download from YouTube.")
        return DownloadResult(platform=platform, title="", error=msg or "Download failed.")
    except Exception as exc:
        return DownloadResult(platform=platform, title="", error=f"yt-dlp error: {exc}")

    if not info:
        return DownloadResult(platform=platform, title="", error="No media info returned.")

    title = info.get("title") or info.get("id") or "media"
    author = info.get("uploader") or info.get("channel") or info.get("creator")
    description = (info.get("description") or "")[:500] or None
    thumbnail = info.get("thumbnail")

    items: list[MediaItem] = []

    # --- Carousel / multi-item posts (e.g. some TikTok slideshows, galleries) ---
    if info.get("_type") == "playlist" and info.get("entries"):
        for entry in info["entries"]:
            if not entry:
                continue
            _collect_entry_files(entry, dest_dir, items)
    else:
        _collect_entry_files(info, dest_dir, items)

    if not items:
        return DownloadResult(
            platform=platform, title=title,
            error="yt-dlp resolved the page but no media files were produced.",
        )

    # Attach a representative thumbnail + title to the first item for previews.
    if items and thumbnail:
        items[0].thumbnail = thumbnail
    for it in items:
        if not it.title:
            it.title = title

    return DownloadResult(
        platform=platform, title=title, author=author,
        description=description, items=items,
    )


def _collect_entry_files(entry: dict, dest_dir: str, items: list[MediaItem]) -> None:
    """Find the file(s) yt-dlp wrote for one entry and build MediaItems."""
    entry_id = entry.get("id") or "media"
    # Search for any file whose basename starts with the entry id.
    candidates = []
    for pat in (f"{entry_id}.*", f"{entry_id}*"):
        candidates.extend(glob.glob(os.path.join(dest_dir, pat)))
    # Deduplicate while preserving order.
    seen = set()
    candidates = [c for c in candidates if not (c in seen or seen.add(c))]

    # Prefer the "final" media file (skip .part / .temp / .ytdl sidecars).
    final_files = [
        f for f in candidates
        if not f.endswith((".part", ".temp", ".ytdl", ".jpg", ".webp", ".png"))
    ]
    media_files = final_files or candidates

    thumbnail = entry.get("thumbnail")

    for path in media_files:
        ext = os.path.splitext(path)[1].lower()
        items.append(MediaItem(
            kind=_kind_for_ext(ext),
            url="",  # local file; we read bytes in the UI
            local_path=path,
            filename=os.path.basename(path),
            mime=_MIME_BY_EXT.get(ext, "application/octet-stream"),
            thumbnail=thumbnail,
        ))

    # If there's a thumbnail and no image item yet, also surface it.
    if thumbnail and not any(i.kind == "image" for i in items):
        items.append(MediaItem(
            kind="image", url=thumbnail,
            filename=f"{entry_id}_thumb.jpg",
            thumbnail=thumbnail, mime="image/jpeg",
        ))
