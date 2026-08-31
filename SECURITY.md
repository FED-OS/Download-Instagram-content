# Security Policy

## Supported versions

FED-GRAM is a small, actively-developed project. Security fixes are applied to
the latest `main` branch only. We do not maintain separate backport lines.

| Version | Supported          |
|---------|--------------------|
| latest `main` | ✅ Yes       |
| older releases | ⚠️ Best effort |

## Reporting a vulnerability

We take security reports seriously. **Please do not open a public GitHub issue
for security vulnerabilities.**

Instead, report them privately by emailing **security@FED-OS.local** (replace
with a real contact address before publishing). Include:

- A clear description of the issue and its potential impact.
- Steps to reproduce (commands, URLs, configuration).
- The version / commit you tested against.
- Any suggested fix, if you have one.

We will acknowledge receipt within **72 hours** and aim to provide an initial
assessment within **7 days**. Coordinated disclosure is preferred; we are happy
to credit reporters in release notes unless you prefer to remain anonymous.

## Security considerations for FED-GRAM

FED-GRAM is a **self-hosted, single-user** Streamlit application. The following
points describe its threat model and built-in mitigations:

- **No authentication by default.** The app binds to `0.0.0.0:8501` per
  `.streamlit/config.toml`. If you expose it beyond your local machine
  (e.g. on a public server), **put it behind a reverse proxy with
  authentication** (Caddy, nginx, Streamlit Cloud auth, etc.). We disable XSRF
  protection and CORS in the config to keep the single-user UX smooth, which is
  **not** safe on a public network without an auth layer in front.
- **No persistent storage of user data.** Downloaded media is written to an
  ephemeral temp directory and cleared on the next download or when the "Clear"
  button is pressed. Nothing is retained after the process exits.
- **Cookies handling.** The optional `cookies.txt` upload for YouTube is written
  to the system temp directory (`fedgram_cookies.txt`) and is **git-ignored**
  (see `.gitignore`). Never commit a cookies file. If you deploy publicly,
  disable the cookies uploader or ensure only trusted users can access it.
- **Third-party fetching.** Engines issue HTTP requests to the source platform
  using a desktop `User-Agent`. We do not execute JavaScript from fetched pages
  — scraping is regex/HTML based, which limits XSS surface, but the fetched
  HTML is never rendered. Streamlit's `st.markdown(..., unsafe_allow_html=True)`
  is used only for hardcoded platform badges, not for user or remote content.
- **`yt-dlp` and `instaloader`.** These are trusted, widely-audited libraries,
  but keep them updated (`pip install -U yt-dlp instaloader`) to pick up
  upstream security fixes.

## Hardening checklist for public deployments

1. Put the app behind a reverse proxy with HTTPS and authentication.
2. Re-enable XSRF protection in `.streamlit/config.toml` (`enableXsrfProtection = true`).
3. Bind to `127.0.0.1` instead of `0.0.0.0` if only local access is needed.
4. Run the process as a non-root user in a container with a read-only root
   filesystem where possible.
5. Never upload or store real platform cookies on a shared instance.
6. Keep `yt-dlp`, `instaloader`, `streamlit`, and `requests` updated.
