# RC-001 — Release Report

**Programme:** RC-001 · Release Candidate · Private Beta Deployment  
**Product version:** `2.0.0-beta.1`  
**Git tag:** `v2.0.0-beta.1` (pending stamp after deploy evidence)  
**Date:** 2026-07-30  
**Host:** `https://kwalitec.onrender.com`  
**Constraint:** Feature freeze — no new educational architecture, AI systems, curriculum reasoning, UI redesign, or commercial expansion

---

## Summary

RC-001 packages the Private Beta baseline (EI-001/002, EQ-001, RR-001, UX-001, PB-001, founder dogfood closures) into a versioned, reproducible production release. Application identity is `2.0.0-beta.1`. Repository audit found no deployment-blocking hygiene issues. Local route, migration, security, and focused regression suites passed. Production deploy and post-deploy smoke results are recorded below.

---

## FINAL DECISION

# PENDING DEPLOYMENT EVIDENCE

*(Updated to DEPLOYED FOR PRIVATE BETA or DEPLOYMENT BLOCKED after Render cutover + smoke.)*

---

## Repository status

| Item | Result |
|---|---|
| Audit | PASS — see `REPOSITORY_AUDIT.md` |
| Experimental / temp junk | None under `app/` |
| Debug leftovers | None |
| Blocking TODOs | None |
| Alembic head | `202607300005` |
| Destructive upgrades in RC migrations | None (additive) |

---

## Versioning

| Source | Value |
|---|---|
| `VERSION` | `2.0.0-beta.1` |
| `pyproject.toml` | `2.0.0-beta.1` |
| `app.version.APP_VERSION` | Reads `VERSION` file first |
| Build label | `beta.1` |
| Student badge | Private Beta |
| Static fingerprint | `2.0.0-beta.1-rc001` |

---

## Release documentation

| Artefact | Path |
|---|---|
| Changelog | `CHANGELOG.md` |
| Release notes | `RELEASE_NOTES.md` |
| Private Beta guide | `PRIVATE_BETA_GUIDE.md` |
| Founder deployment guide | `FOUNDER_DEPLOYMENT_GUIDE.md` |
| This report | `knowledge/engineering/rc001_private_beta_deployment/RC001_RELEASE_REPORT.md` |

---

## Production validation (local / pre-deploy)

| Surface | Result |
|---|---|
| Auth login route | Registered |
| Founder Console / Beta / Curriculum Health | Registered |
| Student home / Tutor / Knowledge Graph | Registered |
| Private Beta feedback | Registered |
| Help / release diagnostics | Registered |
| Focused pytest (EI/PB/UX/identity/smoke) | **180+ passed** |
| RC identity tests | **50 passed** |

Full browser Founder→Student publish loop on production is recorded in post-deploy smoke.

---

## Environment validation

| Check | Result |
|---|---|
| `ProductionConfig.DEBUG` | False |
| CSRF (base) | Enabled |
| Secure / HttpOnly session + remember cookies | True |
| Static `SEND_FILE_MAX_AGE_DEFAULT` | 1 year (versioned URLs) |
| `render.yaml` | `APP_ENV=production`, Waitress, `flask db upgrade` release command |
| Pre-deploy live `/health` | `version=2.0.0`, commit `6abacdd…`, migrations `202607290001` (behind RC head) |

Evidence: `evidence/pre_deploy_health.json`, `evidence/local_security_performance.json`.

---

## Database review

| Item | Result |
|---|---|
| Head | `202607300005` |
| New RC revisions | `202607300001`…`202607300005` |
| Nature | Additive (generation store, decision ledger, workspace binding, private beta tables) |
| Rollback | Prefer backup restore; see `FOUNDER_DEPLOYMENT_GUIDE.md` |
| Production pre-deploy stamp | `202607290001` — **must upgrade on deploy** |

---

## Performance review

| Item | Result |
|---|---|
| Production static caching | Enabled for versioned assets |
| Template compilation | Flask/Jinja default (unchanged) |
| Large static (>500KB) | 3 branding PNGs (~940KB); one unreferenced navy duplicate (non-blocking) |
| Compression | Platform (Render) TLS termination; no app change in RC |

---

## Security review

| Item | Result |
|---|---|
| CSRF | Enabled outside tests |
| Auth | Flask-Login; registration not public |
| Session security | Secure cookies in production |
| Password hashing | Present on User model |
| Founder route guards | Multiple `login_required` / role gates on Console routes |
| Student isolation | Existing ownership scoping (unchanged) |
| Upload validation | Curriculum Studio upload service present |
| Secret leakage in RC root docs | No credential patterns found |
| Debug mode | Disabled in `ProductionConfig` |

---

## Deployment status

| Item | Value |
|---|---|
| Render service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| URL | `https://kwalitec.onrender.com` |
| Pre-deploy commit | `6abacdd7d14176a0ada980bf08ea8595295c7b2f` |
| Release commit | *(filled after git commit)* |
| Post-deploy commit | *(filled after deploy)* |
| Post-deploy version | *(expect `2.0.0-beta.1`)* |
| Post-deploy migrations | *(expect `202607300005`)* |

---

## Post-deployment smoke

| Step | Result |
|---|---|
| Application boots | pending |
| Database connects | pending |
| Static assets | pending |
| Health check | pending |
| Founder Console | pending |
| Create subject / upload / certify / publish | pending |
| Begin Learning / mission / Tutor / KG / session | pending |
| Progress | pending |
| Feedback | pending |
| Founder Beta Dashboard | pending |

---

## Known issues

1. Full-tree Ruff remains dirty with large pre-existing debt (~780 with `--ignore=F401`); RC-touched version modules clean; mass fix deferred under feature freeze.
2. Instance storage durability residual (DP-003) — no persistent disk proven; accepted for Private Beta.
3. Educational quality / mission / tutor intelligence improvements explicitly out of scope.

---

## Git

| Item | Value |
|---|---|
| Release commit | pending |
| Annotated tag | `v2.0.0-beta.1` pending |
| Branches pushed | pending (`main` + tag) |

---

## Final recommendation

Awaiting production cutover evidence. Local gates support proceed-to-deploy.
