"""
FED-GRAM platform detector.

Given a URL, returns the canonical platform name (matched against the
PLATFORMS registry) so the UI can route the download to the right backend.
"""
from __future__ import annotations

from urllib.parse import urlparse


# Ordered list of (platform_key, display_name, list of host substrings).
# The first host that matches wins. Matching is done against the full netloc
# AND the registered root domain, so e.g. "t.co" does not accidentally match
# inside "reddit.com".
PLATFORM_HOSTS = [
    ("instagram", "Instagram", ["instagram.com", "instagr.am"]),
    ("threads",   "Threads",   ["threads.net", "threads.com"]),
    ("tiktok",    "TikTok",    ["tiktok.com"]),
    ("youtube",   "YouTube",   ["youtube.com", "youtu.be", "youtube-nocookie.com"]),
    ("reddit",    "Reddit",    ["reddit.com", "redd.it"]),
    ("twitter",   "Twitter / X", ["twitter.com", "x.com", "t.co"]),
    ("facebook",  "Facebook",  ["facebook.com", "fb.watch", "fb.com"]),
    ("pinterest", "Pinterest", ["pinterest.com", "pin.it"]),
    ("twitch",    "Twitch",    ["twitch.tv"]),
    ("vimeo",     "Vimeo",     ["vimeo.com"]),
    ("dailymotion","Dailymotion", ["dailymotion.com", "dai.ly"]),
    ("soundcloud","SoundCloud",["soundcloud.com"]),
    ("imgur",     "Imgur",     ["imgur.com"]),
    ("bluesky",   "Bluesky",   ["bsky.app", "bsky.social"]),
    ("tumblr",    "Tumblr",    ["tumblr.com"]),
    ("snapchat",  "Snapchat",  ["snapchat.com", "snap.com"]),
    ("linkedin",  "LinkedIn",  ["linkedin.com"]),
    ("streamable","Streamable",["streamable.com"]),
]

# Pretty registry used by the UI sidebar / supported list.
PLATFORMS = {key: name for key, name, _ in PLATFORM_HOSTS}


def _host_matches(host: str, candidate: str) -> bool:
    """True if `host` ends with the registered domain `candidate`.

    We compare on domain-label boundaries so 't.co' doesn't match 'reddit.com'.
    """
    host = host.lower()
    cand = candidate.lower()
    if host == cand:
        return True
    return host.endswith("." + cand) or host.endswith("/" + cand)


def detect_platform(url: str) -> str | None:
    """Return the platform key for a URL, or None if unknown."""
    if not url:
        return None
    cleaned = url.strip()
    # Make sure it has a scheme so urlparse behaves.
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    parsed = urlparse(cleaned)
    host = (parsed.netloc or "").lower()
    # Strip port and userinfo.
    host = host.split("@")[-1].split(":")[0]
    if not host:
        return None
    for key, _name, hosts in PLATFORM_HOSTS:
        for cand in hosts:
            if _host_matches(host, cand):
                return key
    return None
