# Release Process

**Programme:** PR-001  
**Canonical protocol:** [`docs/process/RELEASE_PROTOCOL.md`](../process/RELEASE_PROTOCOL.md)

## Production quality gates (must all pass)

1. Architecture tests green (`pytest tests/architecture/`)
2. Full test suite green
3. Ruff clean (`ruff check app/ src/ tests/`)
4. Migrations validate (Alembic head present; upgrade path tested on staging)
5. Security scan reviewed (`pip-audit`; no unresolved criticals without waiver)
6. Accessibility review for UI-impacting changes
7. Health endpoints green on staging (`/health/live`, `/health/ready`)
8. Version tag matches `VERSION` / `APP_VERSION`

CI enforces architecture, unit, integration, lint, and release-build jobs. The **production-gates** job fails the pipeline when critical gates fail.

## Tagging

```bash
# After gates pass on main
git tag -a "v$(tr -d '[:space:]' < VERSION)" -m "Release $(tr -d '[:space:]' < VERSION)"
git push origin "v$(tr -d '[:space:]' < VERSION)"
```

See [Versioning Policy](VERSIONING_POLICY.md).

## Artefacts

- `VERSION`
- Release notes under `docs/release/` or root `RELEASE_NOTES_*.md`
- Deploy fingerprint via `KWALITEC_GIT_COMMIT` / platform commit env
