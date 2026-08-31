# Build

FED-GRAM is a Python application — there is no separate compile/build step.
"Building" means installing dependencies and verifying the app runs. This
document covers the setup-from-scratch workflow and how to package a
distributable archive.

---

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.11+ | Uses `str \| None` unions and `from __future__ import annotations`. |
| pip | latest | |
| ffmpeg | 5.x+ | **System tool**, required by `yt-dlp` for merging video+audio. |
| Git | any | For cloning and contributing. |

### Install ffmpeg

```bash
sudo apt install ffmpeg          # Debian / Ubuntu
sudo dnf install ffmpeg          # Fedora
brew install ffmpeg              # macOS
winget install Gyan.FFmpeg       # Windows (via winget)
```

Verify: `ffmpeg -version`.

---

## Install dependencies

```bash
cd FED-GRAM
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

`requirements.txt` pins lower bounds for: `streamlit`, `instaloader`,
`requests`, `yt-dlp`, `Pillow`.

---

## Verify the build

Run these checks after installing:

```bash
# 1. Imports resolve
python -c "import streamlit, instaloader, requests, yt_dlp, PIL; print('deps OK')"

# 2. The downloaders package loads and detection works
python -c "from downloaders import detect_platform, PLATFORMS, resolve; \
print('platforms:', len(PLATFORMS)); \
print('youtu.be ->', detect_platform('https://youtu.be/abc')); \
print('tiktok ->', detect_platform('https://tiktok.com/@u/video/1'))"

# 3. App launches
streamlit run app.py
# then open http://localhost:8501 and confirm HTTP 200
```

Expected output (platforms count may grow over time):

```
deps OK
platforms: 18
youtu.be -> youtube
tiktok -> tiktok
```

---

## Optional: keep yt-dlp current

`yt-dlp` releases frequently to keep up with platform changes. Update it
regularly, even outside FED-GRAM releases:

```bash
pip install -U yt-dlp
```

---

## Packaging a distributable archive

To share a snapshot of the project (excluding runtime artifacts):

```bash
cd ..
zip -r FED-GRAM.zip FED-GRAM \
    -x "FED-GRAM/venv/*" \
       "FED-GRAM/__pycache__/*" \
       "FED-GRAM/downloaders/__pycache__/*" \
       "FED-GRAM/*.pyc" \
       "FED-GRAM/cookies.txt" \
       "FED-GRAM/fedgram_cookies.txt" \
       "FED-GRAM/downloads/*"
```

Recipients then follow [INSTALL.md](INSTALL.md).

---

## CI considerations (when added)

When a CI pipeline is introduced (on the roadmap), it should at minimum:

1. Install `requirements.txt` on Python 3.11.
2. Install `ffmpeg`.
3. Run the three verify checks above.
4. (Future) run `pytest` once a test suite exists.

No build artifacts are published currently; deployment is via Streamlit Cloud
or direct `streamlit run` (see [DEPLOYMENT.md](DEPLOYMENT.md)).
