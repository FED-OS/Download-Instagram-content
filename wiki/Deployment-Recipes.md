# Deployment Recipes

Extended setup recipes. The canonical guide is [../DEPLOYMENT.md](../DEPLOYMENT.md);
this page adds edge cases.

## Run on a custom port

```bash
streamlit run app.py --server.port 8765 --server.address 127.0.0.1
```

## Run over SSH tunnel

If the app runs on a remote machine but you want to use it from your laptop
without exposing a port:

```bash
# on your laptop
ssh -L 8501:localhost:8501 user@remote-host
# then keep that session open and visit http://localhost:8501 locally
```

## Systemd service (Linux)

`/etc/systemd/system/fedgram.service`:

```ini
[Unit]
Description=FED-GRAM
After=network.target

[Service]
Type=simple
User=fedgram
WorkingDirectory=/opt/FED-GRAM
ExecStart=/opt/FED-GRAM/venv/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fedgram
```

Put nginx/Caddy in front for TLS + auth (see [../DEPLOYMENT.md](../DEPLOYMENT.md)).

## Docker with a named volume for cookies

If you persist cookies across restarts (single-user, trusted), mount a volume:

```bash
docker run -p 8501:8501 -v fedgram_cookies:/tmp/cookies fedgram
```

and point `ytdlp_engine.set_cookies_file()` at `/tmp/cookies/cookies.txt`.
**Do not do this on a multi-user/public instance** — cookies are sensitive.

## Resource limits

Large video downloads can run long. Behind a reverse proxy, raise timeouts:

```nginx
proxy_read_timeout 600s;
proxy_send_timeout 600s;
```

On Streamlit Cloud, be aware of the platform's per-request and memory limits.

## Updating in place

```bash
cd /opt/FED-GRAM
git pull
./venv/bin/pip install -r requirements.txt --upgrade
./venv/bin/pip install -U yt-dlp
sudo systemctl restart fedgram
```
