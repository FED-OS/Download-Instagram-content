# Frequently Asked Questions

## General

### What is FED-GRAM?

FED-GRAM is a self-hosted Streamlit web app that lets you paste a link from a supported social media platform and download the underlying images, videos, GIFs, or audio — all from one place. It auto-detects the platform and routes the URL to the right backend engine.

### Is FED-GRAM free?

Yes. It is open source under the MIT license and free to run locally or deploy on Streamlit Community Cloud. If you'd like to support development, you can donate at [Ko-fi](https://ko-fi.com/YOUR_USERNAME).

### Does FED-GRAM store my data?

No. Downloaded media is written to a temporary directory and cleared on the next download or when you press "Clear". Nothing is retained after the app process exits. The only network traffic is between your machine and the source platform.

---

## Platforms & compatibility

### Which platforms are supported?

Eighteen, plus a generic fallback: Instagram, Threads, TikTok, YouTube, Reddit, Twitter / X, Facebook, Pinterest, Twitch, Vimeo, Dailymotion, SoundCloud, Imgur, Bluesky, Tumblr, Snapchat, LinkedIn, Streamable — and "generic" for any other URL with embeddable `og:image` / `og:video` tags or a direct media link.

### Can I download from private accounts?

No. FED-GRAM only works on **public** content by design. Private, friends-only, or login-walled media will fail with a clear error message.

### Can you add support for platform X?

Maybe! Open a [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) describing the platform and what kind of media you want to grab. New engine contributions are very welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Errors & troubleshooting

### YouTube says "Sign in to confirm you're not a bot"

YouTube increasingly blocks unauthenticated downloads. Use the **cookies.txt uploader** in the app sidebar. Export a Netscape-format `cookies.txt` from a logged-in browser session (browser extensions such as "Get cookies.txt LOCALLY" work well) and upload it. FED-GRAM passes it to `yt-dlp` automatically.

### I get "No media found" / "No embeddable media found"

The link may point to a text-only post, private content, or a page whose markup has changed. For scraping-based engines (Pinterest, Tumblr, Threads, Imgur, generic), platforms sometimes change their HTML structure. Try a different post, or open an issue with the URL so we can update the scraper.

### The download is slow or times out

Large videos can take a while, especially on slow connections. `yt-dlp` uses concurrent fragment downloads and retries, but very large files may still exceed default timeouts. Try a shorter video or a higher-quality-but-smaller source.

### Instagram returns a rate-limit / connection error

Instagram aggressively rate-limits scraping. Wait a few minutes and try again. FED-GRAM is designed for light, personal use — not bulk downloading.

### `ModuleNotFoundError: No module named 'yt_dlp'`

Your `requirements.txt` is outdated or dependencies weren't installed. Run `pip install -r requirements.txt` again. The current requirements include `yt-dlp` and `Pillow`.

### Video has no audio (or fails to merge)

`yt-dlp` needs **ffmpeg** to merge separate video and audio streams (common for YouTube). Install it: `sudo apt install ffmpeg` (Linux), `brew install ffmpeg` (macOS), or download from [ffmpeg.org](https://ffmpeg.org).

---

## Deployment

### Can I deploy FED-GRAM publicly?

Yes, but with care. The default config disables XSRF protection and CORS for a smooth single-user experience, which is **not safe on a public network**. See the hardening checklist in [SECURITY.md](SECURITY.md) — at minimum, put it behind an authenticated reverse proxy and re-enable XSRF protection.

### Does it work on Streamlit Community Cloud?

Yes. Push the repo to GitHub, create a new app at [share.streamlit.io](https://share.streamlit.io), set the main file to `app.py`, and deploy. Note that the free tier has resource and timeout limits, and some platforms may block cloud-IP downloads.

---

## Ethics & legality

### Is downloading social media content legal?

Downloading **public** content you have the right to access is generally fine for personal use, but you remain responsible for complying with each platform's Terms of Service and applicable copyright law. FED-GRAM is a convenience tool, not a license to redistribute.

### Will FED-GRAM get me banned?

Light personal use is very unlikely to trigger action. Aggressive, automated, bulk scraping can get your IP rate-limited or blocked by platforms, and may violate their ToS. Use responsibly.
