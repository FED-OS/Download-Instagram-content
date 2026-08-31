# Pull Request Template

> This is the root-level copy. GitHub uses `.github/PULL_REQUEST_TEMPLATE.md`
> automatically; this file is kept in sync for visibility and for non-GitHub
> workflows. The canonical version is at
> [`.github/PULL_REQUEST_TEMPLATE.md`](.github/PULL_REQUEST_TEMPLATE.md).

## Summary

Briefly describe what this PR changes and why.

## Related issue

Closes #<issue number> (if applicable). Or: "N/A".

## What kind of change is this?

- [ ] Bug fix (non-breaking)
- [ ] New feature / new platform engine
- [ ] Refactor (no behavior change)
- [ ] Documentation
- [ ] Breaking change
- [ ] Other: ____

## What was tested

Describe how you verified the change. For engine changes, include an example
**public** URL you tested and the result.

- Tested URL: `https://...` (public only)
- Result: (e.g. "downloaded 1 image, 245 KB" or "clean error for invalid URL")

## Checklist

- [ ] I read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md).
- [ ] My code follows the project conventions (engines return `DownloadResult`, network calls wrapped in try/except, no API keys).
- [ ] I added/updated a platform only if it works on **public** content without login (or via the existing cookies mechanism).
- [ ] I did **not** commit secrets, cookies, downloaded media, or `__pycache__`.
- [ ] I updated `requirements.txt` if I added a dependency, and explained why.
- [ ] I updated [CHANGELOG.md](CHANGELOG.md) under `[Unreleased]`.
- [ ] I updated [README.md](README.md) / docs if the change is user-facing.
- [ ] `streamlit run app.py` launches with no import errors.
- [ ] An unsupported URL still falls through to `generic_engine`.
- [ ] A private/invalid URL returns a clean error, not a traceback.

## Notes for reviewers

Anything maintainers should pay attention to, known limitations, or follow-up
work.
