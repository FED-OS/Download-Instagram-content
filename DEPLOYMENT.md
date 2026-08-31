# Deployment

FED-GRAM is a Streamlit app. There are several ways to deploy it, from local
to cloud. Choose based on your needs.

---

## 1. Local (development / personal use)

```bash
cd FED-GRAM
pip install -r requirements.txt
streamlit run app.py
```

Opens at **http://localhost:8501**. This is the simplest and safest option for
personal use — nothing is exposed to the internet.

---

## 2. Streamlit Community Cloud (free, public)

Best for a shareable, no-ops instance with modest usage.

1. Push the repo to GitHub (e.g. `github.com/FED-OS/FED-GRAM`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with
   GitHub.
3. Click **New app** → select the repo and branch → set main file to `app.py`.
4. (Optional) Under **Advanced settings**, add any secrets if needed.
5. Click **Deploy**. The app goes live at `your-app-name.streamlit.app`.

**Notes:**
- The free tier has resource and timeout limits; very large video downloads
  may time out.
- Some platforms block cloud datacenter IPs; YouTube may require the cookies
  workaround.
- The `.streamlit/config.toml` is already set for headless, CORS-free
  operation.

---

## 3. Docker (self-hosted, reproducible)

FED-GRAM doesn't ship a Dockerfile yet (on the roadmap), but a minimal one
looks like:

```dockerfile
FROM python:3.11-slim

# ffmpeg needed for yt-dlp stream merging
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
docker build -t fedgram .
docker run -p 8501:8501 fedgram
```

---

## 4. Behind a reverse proxy (public, hardened)

If you expose FED-GRAM beyond localhost, **put it behind an authenticated
reverse proxy with TLS**. The default config disables XSRF protection and CORS
for smooth single-user UX, which is unsafe on a public network.

### With Caddy (automatic HTTPS)

```caddyfile
fedgram.example.com {
    basicauth {
        admin $2a$14$...hashed-password...
    }
    reverse_proxy 127.0.0.1:8501
}
```

### With nginx

```nginx
server {
    listen 443 ssl http2;
    server_name fedgram.example.com;
    ssl_certificate     /etc/ssl/fedgram.crt;
    ssl_certificate_key /etc/ssl/fedgram.key;

    auth_basic           "FED-GRAM";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_read_timeout 300s;   # allow long video downloads
    }
}
```

Then bind Streamlit to localhost only and re-enable XSRF in
`.streamlit/config.toml`:

```toml
[server]
address = "127.0.0.1"
enableXsrfProtection = true
enableCORS = true
```

Run `streamlit run app.py` and let the reverse proxy handle public access.

---

## Hardening checklist (public deployments)

See [SECURITY.md](SECURITY.md) for the full list. In short:

1. ✅ Reverse proxy with HTTPS + authentication.
2. ✅ Re-enable XSRF protection; bind to `127.0.0.1`.
3. ✅ Run as a non-root user; read-only root filesystem if possible.
4. ✅ Never store real platform cookies on a shared instance.
5. ✅ Keep `yt-dlp`, `instaloader`, `streamlit`, `requests` updated.
6. ✅ Set resource/timeouts appropriate to your users.

---

## Configuration reference

`.streamlit/config.toml` options that matter for FED-GRAM:

| Option | Default | Purpose |
|--------|---------|---------|
| `server.headless` | `true` | Don't auto-open a browser. |
| `server.port` | `8501` | Listen port. |
| `server.address` | `0.0.0.0` | Bind address (use `127.0.0.1` behind a proxy). |
| `server.maxUploadSize` | `2000` | Max cookies-file upload size (MB). |
| `server.enableCORS` | `false` | Set `true` behind a proxy. |
| `server.enableXsrfProtection` | `false` | Set `true` for public deployments. |
| `browser.gatherUsageStats` | `false` | No telemetry. |
