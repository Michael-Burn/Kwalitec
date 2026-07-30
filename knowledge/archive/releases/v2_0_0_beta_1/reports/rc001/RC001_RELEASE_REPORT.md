# RC-001 — Release Report

**Programme:** RC-001 · Release Candidate · Private Beta Deployment  
**Product version:** `2.0.0-beta.1`  
**Git tag:** `v2.0.0-beta.1`  
**Date:** 2026-07-30  
**Host:** `https://kwalitec.onrender.com`  
**Constraint:** Feature freeze — no new educational architecture, AI systems, curriculum reasoning, UI redesign, or commercial expansion

---

## Summary

RC-001 packaged the Private Beta baseline (EI-001/002, EQ-001, RR-001, UX-001, PB-001, founder dogfood closures) into a versioned production release. Application identity is `2.0.0-beta.1`. Repository audit found no deployment-blocking hygiene issues. Local regression suites passed. Render deploy of commit `7302bb7` succeeded with migrations at head `202607300005`. Authenticated production smoke of Founder Console, Private Beta Dashboard, Curriculum Health, Curriculum Studio subjects, Student Home/Tutor/Knowledge Map/Journey, Help, and Feedback returned HTTP 200 without server errors.

---

## FINAL DECISION

# DEPLOYED FOR PRIVATE BETA

**Justification:** Production serves `2.0.0-beta.1` at commit `7302bb7…` with healthy database, migrations current=head=`202607300005`, and verified Founder + Student surfaces. No critical post-deploy defects observed. Educational optimisation remains intentionally deferred.

---

## Repository status

| Item | Result |
|---|---|
| Audit | PASS — `REPOSITORY_AUDIT.md` |
| Experimental / temp junk | None under `app/` |
| Debug leftovers | None |
| Blocking TODOs | None |
| Alembic head | `202607300005` |
| Destructive upgrades in RC migrations | None (additive) |
| Release commit | `7302bb7f955e4f2e8512d5af28ee258f34abbc00` |

---

## Versioning

| Source | Value |
|---|---|
| `VERSION` | `2.0.0-beta.1` |
| `pyproject.toml` | `2.0.0-beta.1` |
| Runtime `/health` | `2.0.0-beta.1` |
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

## Production validation

### Local (pre-deploy)

| Gate | Result |
|---|---|
| Focused pytest (EI/PB/UX/identity/operational smoke) | **180 passed** |
| Identity / release artefact tests | **50 passed** |
| Route registration (auth, founder beta, student tutor/KG, feedback) | PASS |

### Production (post-deploy)

| Surface | Result |
|---|---|
| `/health`, `/health/live`, `/health/ready` | **200 / ok** |
| `/auth/login` identity (`Kwalitec v2.0.0-beta.1`, build `beta.1`) | PASS |
| Static CSS (`tokens`, `student`) with RC fingerprint | **200** |
| Founder Console `/console/` | **200** |
| Private Beta Dashboard `/console/beta` | **200** |
| Curriculum Health `/console/curriculum-health` | **200** |
| Curriculum Studio subjects `/console/studio/subjects` | **200** |
| Student Home / Tutor / Knowledge Map / Journey | **200** |
| Help / Private Beta feedback | **200** |
| Settings | **302** (no login bounce; no 5xx) |

Evidence: `evidence/post_deploy_*.json`.

Full create-subject → upload → certify → publish → Begin Learning → session completion was previously proven on this baseline by RR-001 / FV-002 dogfood; RC-001 confirms the deployed build boots those surfaces without 5xx. Operator should still run one live publish+session loop when onboarding the first beta cohort (see `PRIVATE_BETA_GUIDE.md`).

---

## Environment validation

| Check | Result |
|---|---|
| `environment` | `production` |
| Database | `connected` (latency ~3ms) |
| CSRF / secure cookies / DEBUG=false | Verified in config review |
| `render.yaml` releaseCommand | Applied — migrations advanced to head |
| Instance storage | Present under `/opt/render/project/src/instance` (DP-003 durability residual unchanged) |

---

## Database review

| Item | Result |
|---|---|
| Pre-deploy stamp | `202607290001` |
| Post-deploy stamp | **`202607300005` = head** |
| RC revisions | `202607300001`…`202607300005` additive |
| Destructive upgrades | None |
| Rollback | Prefer backup restore (`FOUNDER_DEPLOYMENT_GUIDE.md`) |

---

## Performance review

| Item | Result |
|---|---|
| Versioned static assets load | PASS |
| Production static max-age | 1 year (fingerprinted URLs) |
| Large static (>500KB) | 3 branding PNGs; non-blocking |
| Deploy cutover | Brief connection reset during swap; recovered |

---

## Security review

| Item | Result |
|---|---|
| CSRF | Enabled; login CSRF token observed |
| Auth | Founder session established; student surfaces reachable under Founder dual capability |
| Session cookies | Present post-login |
| Password hashing | User model hashing path present |
| Founder-only Console | Operational under admin session |
| Debug | Disabled in production config |
| Secret leakage in RC docs | None found |

---

## Deployment evidence

| Item | Value |
|---|---|
| Render service | `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| Deploy id | `dep-d9lg6su7bikc7390572g` |
| Trigger | API manual deploy |
| URL | `https://kwalitec.onrender.com` |
| Pre-deploy commit | `6abacdd7d14176a0ada980bf08ea8595295c7b2f` |
| Release / post-deploy commit | **`7302bb7f955e4f2e8512d5af28ee258f34abbc00`** |
| Post-deploy version | **`2.0.0-beta.1`** |
| Post-deploy migrations | **`202607300005`** |

---

## Known issues / residuals

1. Full-tree Ruff remains dirty with large pre-existing debt; RC-touched version modules clean; mass auto-fix deferred under feature freeze.
2. Instance storage durability residual (DP-003) — no persistent disk proven; accepted for Private Beta.
3. Educational quality / mission / tutor intelligence improvements explicitly out of scope.
4. Login POST briefly reported `405` on `/auth/experience` during redirect chain; session still established and all smoke URLs succeeded — monitor, not a deploy blocker.

---

## Git

| Item | Value |
|---|---|
| Release commit | `7302bb7f955e4f2e8512d5af28ee258f34abbc00` |
| Annotated tag | `v2.0.0-beta.1` |
| Branches | `main` and `feature/ap-002-assessment-engine` at release tip |

---

## Quality gates

| Gate | Result |
|---|---|
| Tests (RC scope) | PASS |
| Ruff (RC-touched modules) | PASS; full-tree pre-existing debt residual |
| Production deploy | PASS |
| Database healthy at head | PASS |
| Critical bugs post-deploy | None observed |
| Student journey surfaces | PASS (HTTP smoke) |
| Founder journey surfaces | PASS (HTTP smoke) |
| Beta dashboard | PASS |
| Feedback surface | PASS |
| Security review | PASS |

---

## Final recommendation

**Begin Private Beta** with 10–20 invite-only users under `PRIVATE_BETA_GUIDE.md`. No further platform development is required before cohort start unless a deployment-blocking defect is discovered in live use.
