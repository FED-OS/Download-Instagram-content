# Install

Step-by-step instructions to get FED-GRAM running on your machine. For
deployment to the cloud or a server, see [DEPLOYMENT.md](DEPLOYMENT.md). For
how to use the app once it's running, see [usage.md](usage.md).

---

## Requirements

- **Python 3.11 or newer**
- **pip**
- **ffmpeg** (only needed for video downloads via yt-dlp — YouTube, TikTok,
  Twitch, Vimeo, etc.)

---

## 1. Get the code

```bash
git clone https://github.com/FED-OS/FED-GRAM.git
cd FED-GRAM
```

Or download and extract the ZIP from the GitHub releases page.

---

## 2. (Recommended) Create a virtual environment

Isolating dependencies avoids conflicts with other Python projects.

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
# Windows PowerShell:  venv\Scripts\Activate.ps1
# Windows cmd:         venv\Scripts\activate.bat
```

---

## 3. Install Python dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This installs: `streamlit`, `instaloader`, `requests`, `yt-dlp`, `Pillow`.

---

## 4. Install ffmpeg (for video support)

`yt-dlp` needs ffmpeg to merge separate video and audio streams (common for
YouTube and other platforms). Without it, some downloads will fail or produce
video without audio.

| OS | Command |
|----|---------|
| Debian / Ubuntu | `sudo apt install ffmpeg` |
| Fedora | `sudo dnf install ffmpeg` |
| macOS (Homebrew) | `brew install ffmpeg` |
| Windows (winget) | `winget install Gyan.FFmpeg` |
| Windows (manual) | Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH |

Verify:

```bash
ffmpeg -version
```

If you only ever download images (Instagram, Pinterest, Imgur, Tumblr,
Threads), ffmpeg is not strictly required — but it's recommended.

---

## 5. Run FED-GRAM

```bash
streamlit run app.py
```

Your browser should open automatically at **http://localhost:8501**. If it
doesn't, open that URL manually.

You should see the FED-GRAM title, a link input, and the sidebar listing
supported platforms. You're ready — head to [usage.md](usage.md).

---

## Troubleshooting the install

### `ModuleNotFoundError: No module named 'streamlit'` (or another dep)

You forgot step 3, or you're not in the virtual environment. Re-run
`pip install -r requirements.txt` with the venv activated.

### `ModuleNotFoundError: No module named 'yt_dlp'`

Your `requirements.txt` is outdated. Pull the latest and reinstall, or run
`pip install yt-dlp` directly.

### Port 8501 is already in use

Another process is using the port. Either stop it, or run on a different port:

```bash
streamlit run app.py --server.port 8502
```

### YouTube downloads fail with "Sign in to confirm you're not a bot"

This is a YouTube bot-detection wall, not an install problem. Use the
**cookies.txt uploader** in the app sidebar — see [usage.md](usage.md) →
"YouTube cookies" and [FAQ.md](FAQ.md).

### The app runs but video downloads produce no audio

ffmpeg isn't installed or isn't on your PATH. Revisit step 4 and run
`ffmpeg -version` to confirm.

---

## Upgrading

To update FED-GRAM and its dependencies:

```bash
cd FED-GRAM
git pull
pip install -r requirements.txt --upgrade
pip install -U yt-dlp     # keep yt-dlp current; it updates often
```

See [CHANGELOG.md](CHANGELOG.md) for what's new.
