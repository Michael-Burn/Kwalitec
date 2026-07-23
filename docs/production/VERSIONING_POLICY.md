# Versioning Policy

**Programme:** PR-001

## Source of truth

- Repository file `VERSION` (semver)
- Python `app.version.APP_VERSION` must match for the legacy app
- Education OS may expose `APP_VERSION` via settings; keep aligned for dual-run releases

## When to bump

| Change | Bump |
|---|---|
| Breaking API / schema requiring coordinated cutover | MAJOR |
| Backward-compatible feature / ops capability | MINOR |
| Bugfix, docs, hardening without behaviour change for learners | PATCH |
| Internal Alpha / RC | Use pre-release tags (`1.0.0-rc.2`) when publishing candidates |

## Rules

- Every production deploy is tagged.
- Tags are immutable; fix-forward with a new tag.
- Health JSON `version` must match the tagged release.
- Do not retag `main` history; create a new patch release instead.
