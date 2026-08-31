# Governance

This document describes how decisions are made in the FED-GRAM project and how
the project is structured for long-term health.

## Guiding principles

1. **Open and transparent.** All discussion happens in public GitHub issues,
   discussions, and pull requests. Private channels are reserved for security
   reports (see [SECURITY.md](SECURITY.md)).
2. **Merit-based.** Influence is earned through sustained, quality
   contribution — not claimed.
3. **Respectful.** Everyone participates under the [Code of Conduct](CODE_OF_CONDUCT.md).
4. **Pragmatic.** FED-GRAM is a small tool. We favor simple, working solutions
   over elaborate process. Governance scales to the project's needs.

## Roles

### Contributors

Anyone who opens a pull request, files a helpful issue, or improves docs.
Contributors are credited in [AUTHORS.md](AUTHORS.md) and on GitHub's
contributor graph. No special rights.

### Maintainers

Contributors with commit/review rights who have shown sustained judgment and
familiarity with the codebase. Maintainers review PRs, triage issues, and keep
engines healthy. See [MAINTAINERS.md](MAINTAINERS.md) for the current roster
and responsibilities.

### Lead maintainer

The maintainer with final say on releases, security responses, and
governance changes. The lead is currently the FED-GRAM Team
([@FED-OS](https://github.com/FED-OS)). The lead's role is to break ties and
keep the project moving, not to overrule consensus lightly.

## Decision-making

### Day-to-day changes (bug fixes, docs, engine updates)

**Lazy consensus.** A maintainer or contributor proposes a change via a PR.
If no maintainer objects within a reasonable review window (target 7 days),
the PR is merged. Maintainers may merge their own trivial PRs (typos, docs)
without external review.

### Significant changes (new dependencies, architecture shifts, new platform
strategies)

These should be proposed as a **GitHub Discussion** or issue tagged
`proposal` before implementation. The aim is to reach rough consensus among
maintainers and interested contributors. The lead maintainer calls the
decision when discussion has run its course.

### Governance changes and release policy

Decided by the lead maintainer in consultation with active maintainers.
Material governance changes are documented in [CHANGELOG.md](CHANGELOG.md) or
a dedicated governance changelog.

## Adding and removing maintainers

**Adding:** A contributor becomes a maintainer by invitation from the lead,
based on sustained quality contributions and community trust. Nominations can
be raised in private with the lead or openly in discussions.

**Removing:** Maintainers who become inactive (no review activity for ~6 months
without notice) or who violate the Code of Conduct may be removed. Removal for
inactivity is handled gracefully with thanks; removal for conduct follows the
[Code of Conduct](CODE_OF_CONDUCT.md) enforcement steps.

## Security

Security decisions are made privately by the lead maintainer (and a
designated security maintainer if one is assigned), following
[SECURITY.md](SECURITY.md). Disclosure timing is coordinated with the reporter.

## Succession

If the lead maintainer steps down or becomes unreachable, active maintainers
select a successor by rough consensus. If no maintainer is available, the
project may be marked as seeking new ownership. The community is encouraged to
fork and continue under the MIT license if needed — the license guarantees
this right.
