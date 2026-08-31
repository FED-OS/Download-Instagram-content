# Usage Guide

A practical walkthrough of using FED-GRAM once it's running. For installation
steps, see [INSTALL.md](INSTALL.md).

## Launching the app

From the project directory:

```bash
streamlit run app.py
```

Your browser opens at **http://localhost:8501**. If it doesn't, open that URL
manually.

---

## Downloading media

1. **Paste a link** into the "Paste a social media link" field at the top.
   The link can be from any supported platform — for example:
   - `https://www.instagram.com/p/Cxxxxxxx/`
   - `https://youtu.be/dQw4w9WgXcQ`
   - `https://www.tiktok.com/@user/video/123456`
   - `https://imgur.com/a/abc123`
   - A direct image URL like `https://example.com/photo.jpg`

2. **Check the detection badge.** To the right of the input, FED-GRAM shows the
   detected platform icon and name (e.g. ▶️ YouTube, 📸 Instagram). If it shows
   🌐 Generic, the URL didn't match a specific engine and the fallback scraper
   will be used.

3. **Click ⬇️ Download.** A spinner appears while the matching engine fetches
   the media.

4. **Preview the result.** Once finished you'll see:
   - A success banner with the number of items found.
   - The post/video title and author (when available).
   - An expandable **Description** section for posts that include captions.
   - A media grid showing each item — images, GIFs, and video previews render
     inline; audio items get a player.

5. **Download.** Each item has its own **💾 Download** button with the filename
   and file size. For multi-item results (carousels, albums), a **📦 Download
   all as ZIP** button appears at the bottom.

6. **Clear.** Press 🧹 Clear to discard the current result and free the temp
   directory before starting a new download.

---

## YouTube cookies (optional)

YouTube increasingly requires sign-in to download some videos. If you see a
"Sign in to confirm you're not a bot" error:

1. In your browser, install a cookies-export extension (e.g. "Get cookies.txt
   LOCALLY") and export a **Netscape-format `cookies.txt`** while logged into
   YouTube.
2. In the FED-GRAM **sidebar**, under **🍪 YouTube cookies (optional)**, upload
   that file.
3. You'll see a "Cookies loaded ✔" confirmation. Retry the download.

The cookies file is stored only in your system temp directory and is never
committed to git (it's in `.gitignore`). To stop using cookies, clear the
uploader.

---

## Supported media types

| Type | What it covers | Preview |
|------|----------------|---------|
| 🖼️ Image | JPEG, PNG, WebP | Inline image |
| 🎞️ GIF | Animated images | Inline image |
| 🎬 Video | MP4, WebM, MKV | Inline video player |
| 🎧 Audio | MP3, M4A, Opus, OGG, WAV | Inline audio player |

---

## Tips

- **Carousels & albums** (Instagram multi-image posts, Imgur albums) produce
  multiple items — use the ZIP button to grab them all at once.
- **Direct media links** (a URL ending in `.jpg`, `.mp4`, etc.) are handled by
  the generic engine instantly, no platform detection needed.
- **Unknown sites** still work if their pages expose `og:image` or `og:video`
  meta tags — the generic fallback scrapes those.
- **Re-running a download** creates a fresh temp directory and cleans up the
  previous one, so you won't accumulate stale files.

---

## What won't work

- **Private / login-walled content** — by design, only public media.
- **Text-only posts** — there's nothing to download; you'll get "No media
  found".
- **Heavy bulk scraping** — platforms will rate-limit or block you. FED-GRAM is
  for light, personal use.

For more on limitations, see the [FAQ](FAQ.md).
