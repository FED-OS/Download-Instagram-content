"""
Common data structures shared across all FED-GRAM downloaders.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MediaItem:
    """A single downloadable piece of media."""
    kind: str  # "image" | "video" | "audio" | "gif"
    url: str          # direct media URL (remote) used for preview/stream
    filename: str     # suggested filename for the download button
    local_path: Optional[str] = None  # path on disk if already downloaded
    thumbnail: Optional[str] = None   # optional preview thumbnail URL
    title: Optional[str] = None       # optional caption / title
    mime: str = "application/octet-stream"

    @property
    def has_local_file(self) -> bool:
        return bool(self.local_path)


@dataclass
class DownloadResult:
    """The result of resolving a single post / video URL."""
    platform: str
    title: str
    author: Optional[str] = None
    description: Optional[str] = None
    items: list[MediaItem] = field(default_factory=list)
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return not self.error and len(self.items) > 0
