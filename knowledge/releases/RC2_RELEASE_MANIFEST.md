# RC2 Release Manifest

**Product:** Kwalitec  
**Version:** 1.0.0  
**Build:** RC2 (`INTERNAL_ALPHA_BUILD_LABEL`)  
**Release type:** Invite-only Internal Alpha  
**Manifest date:** 2026-07-18  
**Nature:** Operational release record — no application behaviour change under this artefact.

---

## Identity

| Field | Value |
|---|---|
| Product name | Kwalitec |
| Application version | `1.0.0` (`pyproject.toml` / `APP_VERSION`) |
| Internal Alpha build label | RC2 |
| Release candidate name | Version 1.0.0 RC2 |
| Deployment target | Production (Render) — `render.yaml` |

---

## Current repository state

| Field | Value |
|---|---|
| Branch | `main` |
| Application baseline commit (full) | `c6864dcca45b41184cb9435c7a1623c38bf08fd4` |
| Application baseline commit (short) | `c6864dc` |
| Application baseline subject | `docs: record V1SP-005 commit fingerprint in audit report` |
| Release documentation commit | Recorded at tip of `main` after `docs(release): finalize RC2 release documentation` |
| Working tree (RC2 scope) | Clean for release documentation; Version 2 planning intentionally untracked outside RC2 commit |
| Merge conflicts | None |
| Relationship to `origin/main` | Local `main` ahead until operator push |
| Annotated release tag | Pending at Release |
| Production deploy fingerprint | Pending at Release |

### Repository State Notes (2026-07-18)

| Artefact | Disposition |
|---|---|
| `knowledge/releases/IPV-RC2_REPORT.md` | In RC2 release documentation commit |
| `knowledge/releases/RC2_LAUNCH_CHECKLIST.md` | In RC2 release documentation commit |
| `knowledge/releases/RC2_RELEASE_MANIFEST.md` | In RC2 release documentation commit |
| `knowledge/releases/RC2_FINAL_READINESS_REPORT.md` | In RC2 release documentation commit |
| `instance/ipv_rc2_harness_out.txt` | Ignored (`instance/*_harness_out.txt`) |
| `knowledge/product/roadmap/VERSION2_PRODUCT_STRATEGY.md` | Excluded from RC2 (Version 2 planning) |

Roadmap canonical path: `knowledge/product/roadmap/` (not `knowledge/roadmap/`).

---

## Current migration version

| Field | Value |
|---|---|
| Alembic head (repository) | `202607170003` |
| Head file | `migrations/versions/202607170003_add_v1sp003_performance_indexes.py` |
| Chain integrity | Single linear head; 22 revisions from `202607080001` → `202607170003`; no divergent heads |
| Pending migrations in repo | None (scripts are at head) |
| Production `alembic_version` | Pending at Release |

---

## Current release status

| Field | Value |
|---|---|
| Product / engineering gate | Prior gates approve invite-only Internal Alpha (RC2 Operational Readiness **APPROVED WITH MINOR ISSUES**; IPV-RC2 **APPROVE**; V1SP-004 **PASS WITH LOW-RISK OBSERVATIONS**; V1SP-005 **PASS WITH MINOR**) |
| Launch / deploy gate | **APPROVED WITH OBSERVATIONS** — see `RC2_LAUNCH_CHECKLIST.md` and `RC2_FINAL_READINESS_REPORT.md` |
| Authorised for public launch | No — invite-only Internal Alpha only |
| Founder day-of sign-off | Pending at Release |
| Live production smoke | Pending at Release |
| Production backup confirmed | Pending at Release |

---

## Build fitness evidence (already recorded)

| Gate | Artefact | Verdict |
|---|---|---|
| Operational readiness | `RC2_OPERATIONAL_READINESS_REPORT.md` | APPROVED WITH MINOR ISSUES |
| High findings closure | `V1SP-001B_OPERATIONAL_FIXES.md` | High items closed |
| Security re-verification | `V1SP-004_SECURITY_VERIFICATION.md` | PASS WITH LOW-RISK OBSERVATIONS |
| Documentation baseline | `V1SP-005_DOCUMENTATION_COMPLETION.md` | PASS WITH MINOR |
| Independent product validation | `IPV-RC2_REPORT.md` | APPROVE |

---

## Operator checklist (at Release)

| Item | Value |
|---|---|
| Push intended commit to `origin/main` | Pending at Release |
| Tag (if used) | Pending at Release |
| Render deploy of published commit | Pending at Release |
| `/health` OK with `version=1.0.0` | Pending at Release |
| Chrome shows Build RC2 | Pending at Release |
| Live student smoke | Pending at Release |
| Live Founder smoke | Pending at Release |
| `ADMIN_EMAIL` matches Founder allowlist account | Pending at Release |
| Alpha participant list | Pending at Release |

---

## References

- `docs/process/RELEASE_PROTOCOL.md`
- `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`
- `knowledge/releases/RC2_LAUNCH_CHECKLIST.md`
- `knowledge/releases/RC2_FINAL_READINESS_REPORT.md`
- `render.yaml`
- `CHANGELOG.md`
