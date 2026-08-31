"""
FED-GRAM downloaders package.

Routes a URL to the appropriate platform engine and returns a unified
DownloadResult. Engine resolution order matters: specific engines first,
generic fallback last.
"""
from __future__ import annotations

from .models import DownloadResult, MediaItem
from .detector import detect_platform, PLATFORMS


def _safe_import(module_name: str):
    """Import a downloader engine module, returning None on ImportError.

    This lets the Streamlit app start even if an optional dependency
    (e.g. yt-dlp, instaloader) is not yet installed; the affected engine
    simply reports a clean error at download time instead of crashing the
    whole app on import.
    """
    import importlib
    try:
        return importlib.import_module(f".{module_name}", __package__)
    except ImportError:
        return None


from . import (
    pinterest_engine,
    imgur_engine,
    tumblr_engine,
    threads_engine,
    generic_engine,
)
instagram_engine = _safe_import("instagram_engine")
ytdlp_engine = _safe_import("ytdlp_engine")


# Engines tried in order for a given platform. The first one whose
# can_handle() returns True wins. Some may be None if their optional
# dependency (instaloader / yt-dlp) is not installed.
_ENGINES = [
    instagram_engine,
    pinterest_engine,
    imgur_engine,
    tumblr_engine,
    threads_engine,
    ytdlp_engine,
    generic_engine,  # always last; can_handle() is always True
]

# Filter out engines that failed to import (None).
_ENGINES = [e for e in _ENGINES if e is not None]


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
