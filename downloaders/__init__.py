"""
FED-GRAM downloaders package.

Routes a URL to the appropriate platform engine and returns a unified
DownloadResult. Engine resolution order matters: specific engines first,
generic fallback last.
"""
from __future__ import annotations

from .models import DownloadResult, MediaItem
from .detector import detect_platform, PLATFORMS
from . import (
    instagram_engine,
    pinterest_engine,
    imgur_engine,
    tumblr_engine,
    threads_engine,
    ytdlp_engine,
    generic_engine,
)


# Engines tried in order for a given platform. The first one whose
# can_handle() returns True wins.
_ENGINES = [
    instagram_engine,
    pinterest_engine,
    imgur_engine,
    tumblr_engine,
    threads_engine,
    ytdlp_engine,
    generic_engine,  # always last; can_handle() is always True
]


def resolve(url: str, dest_dir: str) -> DownloadResult:
    """Detect the platform and run the matching engine."""
    platform = detect_platform(url) or "generic"
    for engine in _ENGINES:
        if engine.can_handle(platform):
            return engine.download(url, platform, dest_dir)
    # Should never happen because generic_engine.can_handle is always True.
    return DownloadResult(platform=platform, title="", error="No engine available.")


__all__ = [
    "DownloadResult", "MediaItem", "detect_platform", "PLATFORMS", "resolve",
]
