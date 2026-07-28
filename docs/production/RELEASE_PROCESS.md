# Release Process

**Programme:** PR-001  
**Canonical protocol:** [`docs/process/RELEASE_PROTOCOL.md`](../process/RELEASE_PROTOCOL.md)  
**RC fingerprint (G11):** [`RELEASE_CANDIDATE_FINGERPRINT.md`](RELEASE_CANDIDATE_FINGERPRINT.md) (EI-001.1)

## Production quality gates (must all pass)

1. Architecture tests green (`pytest tests/architecture/`)
2. Full test suite green
3. Ruff clean (`ruff check app/ src/ tests/`)
4. Migrations validate (Alembic head present; upgrade path tested on staging)
5. Security dependency scan green (`./scripts/dependency_audit.sh`; unaccepted advisories fail CI — see `docs/security/DEPENDENCY_ASSURANCE_POLICY.md`)
6. Accessibility review for UI-impacting changes
7. Health endpoints green on staging (`/health/live`, `/health/ready`)
8. Version tag matches `VERSION` / `APP_VERSION`

**Sole CI authority:** `.github/workflows/ci.yml` (`Kwalitec CI`). Do not cite retired or parallel workflows. CI enforces architecture, unit, integration, educational-intelligence certification, lint, production-gates, and release-build. The **production-gates** job fails the pipeline when critical gates fail.

## Tagging

```bash
# After gates pass on main (canonical ci.yml green on the intended SHA)
git tag -a "v$(tr -d '[:space:]' < VERSION)" -m "Release $(tr -d '[:space:]' < VERSION)"
git push origin "v$(tr -d '[:space:]' < VERSION)"
```

After tagging, file an **RC fingerprint** per [`RELEASE_CANDIDATE_FINGERPRINT.md`](RELEASE_CANDIDATE_FINGERPRINT.md) (commit SHA, tag, Actions run URL, required jobs).

See [Versioning Policy](VERSIONING_POLICY.md).

## Artefacts

- `VERSION`
- Release notes under `docs/release/` or root `RELEASE_NOTES_*.md`
- RC / engineering fingerprint record (commit + tag + CI run)
- Deploy fingerprint via `KWALITEC_GIT_COMMIT` / platform commit env
