# 🎞️ FED-GRAM

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W3T61ZU5FS)

A universal social media downloader built with Python and Streamlit. Paste a link from **any** popular social media platform and FED-GRAM auto-detects the site, fetches the media (images, videos, carousels, albums, audio), previews it, and gives you one-click downloads — all from a single web interface.

v3: https://fed-gram-download-instagram-content-yfergqmofa9rckmn2uo7jw.streamlit.app/

> Originally a small Instagram-only image downloader, FED-GRAM has been upgraded into a multi-platform tool covering **18+ popular social media sites**.

## ✨ Features

- **Auto-detect** the platform from any pasted URL (no dropdowns needed)
- Download **images, videos, GIFs, carousels, albums and audio**
- In-browser **preview** before downloading
- **Per-file** download buttons + **Download all as ZIP** for multi-item posts
- Metadata display (title, author, description, file sizes)
- Clean, responsive Streamlit UI with a supported-platforms sidebar
- Modular engine architecture — easy to add new platforms

## ✅ Supported platforms

| Platform | What you can download |
| --- | --- |
| 📸 **Instagram** | Posts, Reels (video), multi-image carousels |
| 🧵 **Threads** | Post images & videos |
| 🎵 **TikTok** | Videos, slideshow images |
| ▶️ **YouTube** | Videos (best mp4), audio |
| 🐦 **Twitter / X** | Tweets — images, videos, GIFs |
| 👽 **Reddit** | Video posts & embedded media (text/image posts via fallback) |
| 👍 **Facebook** | Public videos & watch links |
| 📌 **Pinterest** | High-resolution pin images |
| 🎮 **Twitch** | Clips & VODs |
| 🎬 **Vimeo** | Videos |
| 📡 **Dailymotion** | Videos |
| ☁️ **SoundCloud** | Tracks (audio) |
| 🖼️ **Imgur** | Single images, GIFs, and full albums |
| 🔷 **Bluesky** | Post media |
| ✏️ **Tumblr** | Post images, GIFs, videos |
| 👻 **Snapchat** | Spotlight videos |
| 💼 **LinkedIn** | Public post media (via fallback) |
| ⏯️ **Streamable** | Videos |
| 🌐 **Generic / direct links** | Any page with `og:image` / `og:video`, or direct media URLs |

## 🏗️ How it works

FED-GRAM uses a small **engine router**:

```
downloaders/
├── detector.py          # URL → platform key (18 platforms, boundary-safe)
├── models.py            # MediaItem / DownloadResult data structures
├── __init__.py          # resolve(url) router
├── instagram_engine.py  # instaloader (posts / reels / carousels)
├── ytdlp_engine.py      # yt-dlp (YouTube, TikTok, Twitter, FB, Twitch, Vimeo, …)
├── pinterest_engine.py  # high-res pin scraping
├── imgur_engine.py      # single / gif / album
├── tumblr_engine.py     # post media
├── threads_engine.py    # Threads post media
└── generic_engine.py    # og:image / og:video fallback + direct media links
```

`yt-dlp` powers most video platforms, `instaloader` handles Instagram, and dedicated scrapers handle image-first sites. A generic fallback catches anything else with Open Graph metadata.

## 🚀 Run locally

```bash
git clone https://github.com/FED-OS/FED-GRAM.git
cd FED-GRAM
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

## ☁️ Deploy for free (Streamlit Community Cloud)

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repo and branch, set the main file to `app.py`.
4. Click **Deploy**. Your app goes live at `your-app-name.streamlit.app`.

## ⚠️ Limitations & notes

- **Public content only.** Private accounts and members-only videos will fail.
- Some platforms (Instagram especially) **rate-limit or block** scraping if used heavily — this tool is intended for light, personal use.
- A few sites require JavaScript rendering or login; those may not work without a session. yt-dlp covers an enormous range of sites, so most public video links just work.
- Video downloads may take a few seconds depending on length and quality.

## 🧩 Adding a new platform

1. Add the host(s) to `PLATFORM_HOSTS` in `downloaders/detector.py`.
2. Create `downloaders/<name>_engine.py` with `can_handle(platform)` and `download(url, platform, dest_dir) -> DownloadResult`.
3. Register it in `downloaders/__init__.py` (before `generic_engine`).

## 📄 License

MIT
