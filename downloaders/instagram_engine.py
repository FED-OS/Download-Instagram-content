"""
Instagram downloader — keeps the original instaloader spirit of FED-GRAM
but adds Reel/video support and carousel handling.
"""
from __future__ import annotations

import os

try:
    import instaloader
except ImportError:  # pragma: no cover - handled at runtime
    instaloader = None  # type: ignore[assignment]

import requests

from .models import DownloadResult, MediaItem


def can_handle(platform: str) -> bool:
    return platform == "instagram"


def download(url: str, platform: str, dest_dir: str) -> DownloadResult:
    if instaloader is None:
        return DownloadResult(
            platform="instagram", title="",
            error="instaloader is not installed. Add 'instaloader' to requirements.txt and redeploy.",
        )
    os.makedirs(dest_dir, exist_ok=True)

    # Accept /p/ (posts), /reel/ (reels), and /reels/ URLs.
    shortcode = None
    for sep in ("/p/", "/reel/", "/reels/"):
        if sep in url:
            shortcode = url.split(sep)[1].split("/")[0]
            break
    if not shortcode:
        return DownloadResult(platform="instagram", title="", error="Not a valid Instagram post/reel URL.")

    L = instaloader.Instaloader(
        download_videos=True,
        download_video_thumbnails=False,
        download_comments=False,
        download_geotags=False,
        save_metadata=False,
        quiet=True,
    )

    try:
        post = instaloader.Post.from_shortcode(L.context, shortcode)
    except instaloader.exceptions.ConnectionException as exc:
        return DownloadResult(platform="instagram", title="", error=f"Couldn't reach Instagram: {exc}")
    except Exception as exc:
        return DownloadResult(platform="instagram", title="", error=f"Invalid or private post: {exc}")

    title = post.caption[:300] if post.caption else f"Instagram post {shortcode}"
    author = post.owner_username

    items: list[MediaItem] = []

    try:
        if post.typename == "GraphSidecar":
            for i, node in enumerate(post.get_sidecar_nodes()):
                if node.is_video and node.video_url:
                    ext = "mp4"
                    mime = "video/mp4"
                    media_url = node.video_url
                    kind = "video"
                else:
                    ext = "jpg"
                    mime = "image/jpeg"
                    media_url = node.display_url
                    kind = "image"

                data = requests.get(media_url, timeout=30).content
                fname = f"fedgram_{shortcode}_{i+1}.{ext}"
                path = os.path.join(dest_dir, fname)
                with open(path, "wb") as fh:
                    fh.write(data)
                items.append(MediaItem(
                    kind=kind, url=media_url, local_path=path,
                    filename=fname, mime=mime, thumbnail=node.display_url,
                    title=title,
                ))
        else:
            if post.is_video and post.video_url:
                media_url = post.video_url
                ext = "mp4"
                mime = "video/mp4"
                kind = "video"
            else:
                media_url = post.url
                ext = "jpg"
                mime = "image/jpeg"
                kind = "image"

            data = requests.get(media_url, timeout=30).content
            fname = f"fedgram_{shortcode}.{ext}"
            path = os.path.join(dest_dir, fname)
            with open(path, "wb") as fh:
                fh.write(data)
            items.append(MediaItem(
                kind=kind, url=media_url, local_path=path,
                filename=fname, mime=mime, thumbnail=post.url,
                title=title,
            ))
    except Exception as exc:
        return DownloadResult(platform="instagram", title=title, error=f"Download failed: {exc}")

    return DownloadResult(
        platform="instagram", title=title, author=author,
        description=post.caption if post.caption else None, items=items,
    )
