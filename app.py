import os
import shutil
import tempfile
import time

import streamlit as st

from downloaders import detect_platform, PLATFORMS, resolve, DownloadResult, MediaItem
from downloaders import ytdlp_engine as _ytdlp_engine


# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="FED-GRAM — Universal Social Media Downloader",
    page_icon="🎞️",
    layout="wide",
)

# Brand emoji per platform for nice badges.
_PLATFORM_ICON = {
    "instagram": "📸", "threads": "🧵", "tiktok": "🎵", "youtube": "▶️",
    "twitter": "🐦", "reddit": "👽", "facebook": "👍", "pinterest": "📌",
    "twitch": "🎮", "vimeo": "🎬", "dailymotion": "📡", "soundcloud": "☁️",
    "imgur": "🖼️", "bluesky": "🔷", "tumblr": "✏️", "snapchat": "👻",
    "linkedin": "💼", "streamable": "⏯️", "generic": "🌐",
}


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "last_result" not in st.session_state:
    st.session_state.last_result = None  # type: ignore[assignment]
if "work_dir" not in st.session_state:
    st.session_state.work_dir = None  # type: ignore[assignment]


def _new_work_dir() -> str:
    """Create a fresh temp dir for this download session."""
    if st.session_state.work_dir and os.path.isdir(st.session_state.work_dir):
        shutil.rmtree(st.session_state.work_dir, ignore_errors=True)
    d = tempfile.mkdtemp(prefix="fedgram_")
    st.session_state.work_dir = d
    return d


def _read_bytes(item: MediaItem) -> bytes:
    """Read media bytes from the local file (preferred) or remote URL."""
    if item.local_path and os.path.exists(item.local_path):
        with open(item.local_path, "rb") as fh:
            return fh.read()
    import requests
    return requests.get(item.url, timeout=60).content


# ---------------------------------------------------------------------------
# Sidebar — supported platforms
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎞️ FED-GRAM")
    st.caption("Universal social media downloader")
    st.divider()
    st.markdown("### ✅ Supported platforms")
    cols = st.columns(2)
    for i, (key, name) in enumerate(PLATFORMS.items()):
        icon = _PLATFORM_ICON.get(key, "🔗")
        cols[i % 2].markdown(f"{icon} **{name}**")
    st.divider()
    st.markdown("#### 🛠️ How it works")
    st.write(
        "Paste **any** link from a supported platform. FED-GRAM auto-detects "
        "the site, fetches the media (images, videos, carousels & albums), "
        "and gives you one-click downloads."
    )
    st.divider()
    st.markdown("#### 🍪 YouTube cookies (optional)")
    st.write(
        "YouTube sometimes blocks downloads with a &ldquo;sign in to confirm "
        "you&rsquo;re not a bot&rdquo; message. Upload a **cookies.txt** file "
        "(Netscape format, exported with a browser extension) to bypass this."
    )
    if _ytdlp_engine is None:
        st.warning("yt-dlp is not installed — video downloads are unavailable until you add `yt-dlp` to requirements.txt and redeploy.")
    else:
        cookies_file = st.file_uploader(
            "cookies.txt",
            type=["txt"],
            label_visibility="collapsed",
            key="cookies_uploader",
        )
        if cookies_file is not None:
            cookies_path = os.path.join(tempfile.gettempdir(), "fedgram_cookies.txt")
            try:
                with open(cookies_path, "wb") as fh:
                    fh.write(cookies_file.getvalue())
                _ytdlp_engine.set_cookies_file(cookies_path)
                st.success("✅ Cookies loaded — YouTube downloads enabled.")
            except Exception as exc:
                st.error(f"Couldn't save cookies file: {exc}")
                _ytdlp_engine.set_cookies_file(None)
        else:
            _ytdlp_engine.set_cookies_file(None)
    st.divider()
    st.caption("⚠️ For personal use with public content only. Respect each platform's Terms of Service and copyright.")


# ---------------------------------------------------------------------------
# Main header
# ---------------------------------------------------------------------------
st.title("🎞️ FED-GRAM")
st.caption("Download images & videos from every popular social media site — all in one place.")
st.write("---")

# ---------------------------------------------------------------------------
# Input
# ---------------------------------------------------------------------------
col_input, col_detect = st.columns([4, 1])
with col_input:
    url = st.text_input(
        "Paste a social media link:",
        placeholder="https://www.instagram.com/p/…  •  https://youtu.be/…  •  https://www.tiktok.com/…",
        label_visibility="collapsed",
    )
with col_detect:
    platform = detect_platform(url) if url else None
    if platform:
        st.markdown(
            f"<div style='text-align:center;padding-top:6px;'>"
            f"<span style='font-size:1.6rem'>{_PLATFORM_ICON.get(platform,'🔗')}</span><br>"
            f"<b>{PLATFORMS.get(platform, 'Link')}</b></div>",
            unsafe_allow_html=True,
        )
    elif url:
        st.markdown(
            "<div style='text-align:center;padding-top:10px;color:#888'>🌐 Generic</div>",
            unsafe_allow_html=True,
        )

col_btn1, col_btn2, _ = st.columns([1, 1, 4])
do_download = col_btn1.button("⬇️ Download", type="primary", disabled=not bool(url))
do_clear = col_btn2.button("🧹 Clear")


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------
if do_clear:
    if st.session_state.work_dir and os.path.isdir(st.session_state.work_dir):
        shutil.rmtree(st.session_state.work_dir, ignore_errors=True)
    st.session_state.work_dir = None
    st.session_state.last_result = None
    st.rerun()


# ---------------------------------------------------------------------------
# Download action
# ---------------------------------------------------------------------------
if do_download and url:
    work_dir = _new_work_dir()
    platform = detect_platform(url) or "generic"
    with st.spinner(f"Fetching from {PLATFORMS.get(platform, 'the web')}…"):
        try:
            result = resolve(url, work_dir)
        except Exception as exc:  # safety net
            result = DownloadResult(platform=platform, title="", error=f"Unexpected error: {exc}")
    st.session_state.last_result = result


# ---------------------------------------------------------------------------
# Render result
# ---------------------------------------------------------------------------
result: DownloadResult | None = st.session_state.last_result
if result:
    if result.error:
        st.error(f"❌ {result.error}")
        st.caption("The content may be private, deleted, region-locked, or the link is invalid. Some platforms rate-limit heavy use — try again shortly.")
    elif result.ok:
        # ---- Header / metadata ----
        icon = _PLATFORM_ICON.get(result.platform, "🔗")
        pname = PLATFORMS.get(result.platform, "Link")
        st.success(f"✅ Found {len(result.items)} item(s) from {pname}")
        st.markdown(f"### {icon} {result.title or 'Untitled'}")
        meta_bits = []
        if result.author:
            meta_bits.append(f"👤 **{result.author}**")
        meta_bits.append(f"🔗 `{result.platform}`")
        if len(result.items) > 1:
            meta_bits.append(f"📦 {len(result.items)} files")
        st.markdown("  ".join(meta_bits))
        if result.description:
            with st.expander("📝 Description"):
                st.write(result.description)

        st.write("---")

        # ---- Media grid ----
        is_multi = len(result.items) > 1
        n_cols = min(len(result.items), 3)
        cols = st.columns(n_cols) if is_multi else [st]

        for i, item in enumerate(result.items):
            target = cols[i % n_cols] if is_multi else cols[0]
            with target:
                with st.container(border=True):
                    badge = "🎬 Video" if item.kind == "video" else (
                            "🎧 Audio" if item.kind == "audio" else (
                            "🎞️ GIF" if item.kind == "gif" else "🖼️ Image"))
                    st.markdown(f"**{badge}**{' · #' + str(i+1) if is_multi else ''}")

                    # Preview
                    try:
                        if item.kind == "video" and item.local_path and os.path.exists(item.local_path):
                            st.video(item.local_path)
                        elif item.kind == "audio" and item.local_path and os.path.exists(item.local_path):
                            st.audio(item.local_path)
                        elif item.kind in ("image", "gif"):
                            if item.local_path and os.path.exists(item.local_path):
                                st.image(item.local_path, use_container_width=True)
                            elif item.url:
                                st.image(item.url, use_container_width=True)
                        else:
                            if item.thumbnail:
                                st.image(item.thumbnail, use_container_width=True)
                    except Exception:
                        if item.thumbnail:
                            try:
                                st.image(item.thumbnail, use_container_width=True)
                            except Exception:
                                pass

                    # Download button
                    try:
                        data = _read_bytes(item)
                        st.download_button(
                            label=f"💾 Download {item.filename}",
                            data=data,
                            file_name=item.filename,
                            mime=item.mime,
                            key=f"dl_{id(item)}_{i}_{int(time.time()*1000)}",
                            use_container_width=True,
                        )
                        size_kb = len(data) / 1024
                        size_str = f"{size_kb:.1f} KB" if size_kb < 1024 else f"{size_kb/1024:.2f} MB"
                        st.caption(f"{size_str} · {item.kind}")
                    except Exception as exc:
                        st.error(f"Couldn't prepare download: {exc}")

        # ---- Download all (zip) ----
        if is_multi and all(it.local_path and os.path.exists(it.local_path) for it in result.items):
            st.write("---")
            work_dir = st.session_state.work_dir or tempfile.gettempdir()
            zip_path = os.path.join(work_dir, "fedgram_bundle.zip")
            try:
                import zipfile
                files_to_zip = [it.local_path for it in result.items if it.local_path]
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for fp in files_to_zip:
                        zf.write(fp, arcname=os.path.basename(fp))
                with open(zip_path, "rb") as fh:
                    st.download_button(
                        label="📦 Download all as ZIP",
                        data=fh.read(),
                        file_name="fedgram_bundle.zip",
                        mime="application/zip",
                        use_container_width=True,
                        type="secondary",
                    )
            except Exception as exc:
                st.warning(f"Couldn't build ZIP bundle: {exc}")
    else:
        st.warning("No media found for this link.")

    st.write("---")
    st.caption("⚠️ Only works on public content. For personal use only — respect copyright and each platform's Terms of Service.")
elif not url:
    st.info("👆 Paste a link from any supported platform to get started.")
