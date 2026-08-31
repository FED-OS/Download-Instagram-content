# Troubleshooting

Extended troubleshooting. For the most common items, see [../FAQ.md](../FAQ.md).

## App won't start

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ModuleNotFoundError: No module named 'streamlit'` | deps not installed / wrong venv | `pip install -r requirements.txt` with venv active |
| `ModuleNotFoundError: No module named 'yt_dlp'` | stale requirements | `pip install yt-dlp` and update requirements |
| `ModuleNotFoundError: No module named 'downloaders'` | running from wrong directory | `cd FED-GRAM` then `streamlit run app.py` |
| Port 8501 in use | another process | `--server.port 8502` or stop the other process |
| `SyntaxError` on `str \| None` | Python < 3.11 | upgrade to Python 3.11+ |

## Downloads fail

### "No media found" / "No embeddable media found"
- The post may be text-only, private, or deleted.
- For scrapers, the platform may have changed markup → open an issue with the URL.
- Try the same content's direct media URL if you can find it (generic engine handles direct links).

### "Sign in to confirm you're not a bot" (YouTube)
- Upload a `cookies.txt` via the sidebar (Netscape format, from a logged-in browser).
- Keep yt-dlp updated: `pip install -U yt-dlp`.

### Video downloads but has no audio
- ffmpeg is missing or not on PATH. Install it and verify `ffmpeg -version`.

### Instagram rate-limit / connection error
- Wait a few minutes. Instagram throttles scraping. Use lightly.

### Slow / timeout on large videos
- Raise proxy timeouts if behind one (see [Deployment-Recipes](Deployment-Recipes.md)).
- Try a shorter or lower-resolution source.

### `AttributeError` in yt-dlp engine
- You may be on an old code version with the line-169 bug (fixed in 1.1.0).
  Update to the latest `main`.

## Detection problems

### Wrong platform detected
- Check `PLATFORM_HOSTS` ordering in `detector.py` — specific platforms must
  come before generic ones.
- Verify label-boundary matching isn't being fooled by a short domain.

### Platform not detected at all → shows "Generic"
- The domain isn't registered. Add it to `PLATFORM_HOSTS` (see
  [Platform-Detection](Platform-Detection.md)) or rely on the generic fallback.

## Deployment problems

### Behind reverse proxy: blank page / WebSocket errors
- Ensure the proxy upgrades WebSocket (`Connection: upgrade`) — see the nginx
  example in [../DEPLOYMENT.md](../DEPLOYMENT.md).
- If you re-enabled XSRF/CORS, make sure headers are passed through.

### Streamlit Cloud: some downloads fail
- Cloud datacenter IPs are often blocked by platforms (especially YouTube).
- Use the cookies workaround where applicable.

## Still stuck?

Gather: OS, Python version, FED-GRAM commit, the exact error text, and a
public example URL. Then open a [Bug Report](../.github/ISSUE_TEMPLATE/bug_report.md).
