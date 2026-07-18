# RC2-LAUNCH-001 — Release Readiness & Deployment Checklist

**Programme:** Release Operations  
**Product:** Kwalitec  
**Version:** 1.0.0  
**Build:** RC2  
**Release type:** Invite-only Internal Alpha  
**Deployment environment:** Production (Render)  
**Milestone status:** DEPLOYMENT  
**Verification date:** 2026-07-18  
**Intended release commit (local `main` HEAD):** `c6864dc` (`c6864dcca45b41184cb9435c7a1623c38bf08fd4`)  
**Nature:** Operational verification only — no application development in this milestone.

---

## Objective

Final operational verification immediately before releasing Version 1.0.0 RC2 to the Internal Alpha programme. This checklist exists to prevent operational mistakes.

---

## Release Metadata

| Field | Value |
|---|---|
| Product | Kwalitec |
| Version | 1.0.0 (`pyproject.toml` / `APP_VERSION`) |
| Build | RC2 (`INTERNAL_ALPHA_BUILD_LABEL`) |
| Release type | Invite-only Internal Alpha |
| Deployment environment | Production |
| Render Blueprint | `render.yaml` (`APP_ENV=production`, Waitress, PostgreSQL) |

---

## Verification method

| Layer | Method |
|---|---|
| Repository / config | Inspected in-tree on 2026-07-18 |
| Prior product gates | `RC2_OPERATIONAL_READINESS_REPORT.md`, `V1SP-001B`, `V1SP-004`, `V1SP-005`, `IPV-RC2_REPORT.md` |
| Live production | Not confirmed for the intended RC2 commit (see Infrastructure / Release Decision) |

**Status legend**

| Mark | Meaning |
|---|---|
| ✓ Completed | Verified for this launch gate |
| ⚠ Pending | Not yet verified, blocked on operator/live action, or incomplete |
| ✗ Failed | Verified as failing or blocking |

---

## Infrastructure

### Environment

| Check | Status | Evidence / reason |
|---|---|---|
| Production environment available | ⚠ Pending | `render.yaml` defines the production web service + DB. Live host availability for the **intended** RC2 commit (`c6864dc`) is not confirmed; prior probe to `https://kwalitec.onrender.com/health` timed out. |
| DEBUG disabled | ✓ Completed | `ProductionConfig.DEBUG = False` (`app/config.py`). |
| ProductionConfig selected | ✓ Completed | `render.yaml` sets `APP_ENV=production`; factory selects `ProductionConfig`. |
| SECRET_KEY verified | ⚠ Pending | Code gate rejects insecure defaults under `ProductionConfig`. Render uses `generateValue: true`. **Operator must confirm** the live Render dashboard value is non-placeholder (V1SP-004 M-4: `.env.example` placeholder `change-this-secret-key` is not in deny-list). |
| ADMIN_EMAIL configured | ⚠ Pending | Declared in `render.yaml` (`sync: false`). Startup **warns** and skips admin creation if missing — not a hard startup failure. **Operator must confirm** live value matches the Founder allowlist account (IPV-RC2 H-1). |
| Environment variables documented | ✓ Completed | `.env.example`, README Getting Started / Deploy, `render.yaml`, `docs/process/RELEASE_PROTOCOL.md`. |

### Database

| Check | Status | Evidence / reason |
|---|---|---|
| Backup completed | ⚠ Pending | Not confirmed in this session. Operator must take / confirm a production PostgreSQL backup before deploy or schema apply. |
| Restore procedure verified | ⚠ Pending | No restore drill evidence recorded for this launch gate. |
| Latest migration applied | ⚠ Pending | Repo head revision is `202607170003`. **Not confirmed** on live production `alembic_version` for commit `c6864dc`. |
| Migration version confirmed | ✓ Completed | Alembic single head: `202607170003` (linear chain, 22 revisions). |
| No pending migrations | ✓ Completed | Single head; no divergent heads in `migrations/versions/`. Live pending state unchecked (covered under Latest migration applied). |

### Static Assets

| Check | Status | Evidence / reason |
|---|---|---|
| Branding assets deployed | ⚠ Pending | Canonical pack under `app/static/branding/` present in repo. Live deploy of this pack unchecked until push + Render build. |
| Manifest present in repo | ✓ Completed | `app/static/branding/manifest.webmanifest` present. |
| Favicons present in repo | ✓ Completed | `favicon.ico`, apple-touch, android-chrome assets present. |
| OpenGraph image present in repo | ✓ Completed | `app/static/branding/social-preview.png` present. |
| Cache invalidation confirmed | ⚠ Pending | `ProductionConfig.SEND_FILE_MAX_AGE_DEFAULT` + versioned static fingerprinting / immutable cache headers in `app/__init__.py`. Live CDN/browser invalidation after deploy not confirmed. |

### HTTPS

| Check | Status | Evidence / reason |
|---|---|---|
| HTTPS active | ⚠ Pending | Live TLS not confirmed this session. Render normally terminates TLS. |
| HSTS configured in code | ✓ Completed | Production path sets `Strict-Transport-Security: max-age=31536000; includeSubDomains` when `APP_ENV=production` (V1SP-004 PASS). |
| HSTS verified live | ⚠ Pending | Live header not re-probed. |
| Redirect HTTP → HTTPS | ⚠ Pending | Platform-level (Render); not re-verified live. |
| Certificate valid | ⚠ Pending | Not re-verified live. |

---

## Product Smoke Test

Evidence basis for student/Founder journeys: **IPV-RC2** (local black-box, 2026-07-17) + V1SP/RC2 readiness reports. These prove the **build** is fit; they do **not** replace production smoke on the deployed commit.

### Student

| Check | Status | Evidence / reason |
|---|---|---|
| Register | ✓ Completed | Public registration intentionally disabled. Invite path: coordinator provisions via `flask create-admin` / `flask create-test-user` (IPV-RC2). |
| Login (build / IPV) | ✓ Completed | IPV-RC2 PASS. |
| Login (production) | ⚠ Pending | Production smoke not run for `c6864dc`. |
| Create Study Plan (IPV) | ✓ Completed | Supported CS1 plan created in IPV. |
| Create Study Plan (production) | ⚠ Pending | Production smoke pending. |
| Begin Study Session (IPV) | ✓ Completed | Learning loop PASS in IPV. |
| Begin Study Session (production) | ⚠ Pending | Production smoke pending. |
| Complete Practice (IPV) | ✓ Completed | Practice outcome capture PASS in IPV. |
| Complete Practice (production) | ⚠ Pending | Production smoke pending. |
| Analytics updates (IPV) | ✓ Completed | Analytics with topic/readiness language observed in IPV. |
| Analytics updates (production) | ⚠ Pending | Production smoke pending. |
| Revision Workspace (IPV) | ✓ Completed | Full syllabus → Revision Workspace + revision session PASS in IPV. |
| Revision Workspace (production) | ⚠ Pending | Production smoke pending. |
| Logout (IPV) | ✓ Completed | POST + CSRF logout; GET returns 405 (IPV / V1SP-004). |
| Logout (production) | ⚠ Pending | Production smoke pending. |

### Founder

| Check | Status | Evidence / reason |
|---|---|---|
| Founder login (IPV) | ✓ Completed | Requires `ADMIN_EMAIL` ∪ `FOUNDER_EMAILS` match (IPV H-1). |
| Founder login (production) | ⚠ Pending | Production smoke pending; allowlist must match live env. |
| Overview (IPV) | ✓ Completed | `/founder` HTTP 200 in IPV. |
| Overview (production) | ⚠ Pending | Production smoke pending. |
| Operational Health (IPV) | ✓ Completed | Signals present in IPV. |
| Operational Health (production) | ⚠ Pending | Production smoke pending. |
| Feedback (IPV) | ✓ Completed | Inbox reflected Product Check-in in IPV. |
| Feedback (production) | ⚠ Pending | Production smoke pending. |
| Vision Journal (IPV) | ✓ Completed | Entry create PASS in IPV. |
| Vision Journal (production) | ⚠ Pending | Production smoke pending. |
| Internal Alpha (IPV) | ✓ Completed | Surface reflects 1.0.0 / Build RC2 in IPV. |
| Internal Alpha (production) | ⚠ Pending | Production smoke pending. |
| Releases (IPV) | ✓ Completed | Release identity PASS in IPV. |
| Releases (production) | ⚠ Pending | Production smoke pending. |
| Logout (IPV) | ✓ Completed | Same auth logout path. |
| Logout (production) | ⚠ Pending | Production smoke pending. |

---

## Educational Workflow

| Check | Status | Evidence / reason |
|---|---|---|
| Learning progression | ✓ Completed | IPV: Plan → session → practice → dashboard recommendations. |
| Revision progression | ✓ Completed | IPV: Revision Mode + revision session after syllabus completion. |
| Progress preserved | ✓ Completed | IPV: Syllabus topic counts intact after revision session (14/14). |
| Recommendations displayed | ✓ Completed | IPV: Explainable why/language on Dashboard. |
| Analytics consistent | ✓ Completed | IPV: Topic/readiness language after practice. |

---

## Security

| Check | Status | Evidence / reason |
|---|---|---|
| CSRF functioning | ✓ Completed | V1SP-004 + IPV: missing token → 400; forms + `X-CSRFToken`. `WTF_CSRF_ENABLED = True` on BaseConfig. |
| Session cookies secure | ✓ Completed | `ProductionConfig`: Secure / HttpOnly / SameSite=Lax (+ remember-me mirrors). V1SP-001B / V1SP-004. |
| Redirect protection | ✓ Completed | V1SP-001B hardening; IPV external `next=` rejected. |
| Founder permissions | ✓ Completed | Students → 403 on `/founder/`; allowlist-gated (IPV). |
| Student permissions | ✓ Completed | Ownership checks; cross-user session access denied (IPV). |
| Error pages | ✓ Completed | V1SP-004 error-handling verification PASS for Alpha. |
| HSTS configured | ✓ Completed | See HTTPS section. |

---

## Performance

| Check | Status | Evidence / reason |
|---|---|---|
| Dashboard responsive | ✓ Completed | IPV / V1SP-003: primary pages typically tens of ms locally; indexes on hot paths. |
| Founder responsive | ✓ Completed | Founder GETs returned promptly in IPV. |
| Analytics responsive | ✓ Completed | Measured + indexed paths (V1SP-003). |
| Assets cached (code) | ✓ Completed | Long-lived cache for static; HTML `no-store`. |
| Assets cached (live) | ⚠ Pending | Live confirmation pending deploy. |

---

## Documentation

| Check | Status | Evidence / reason |
|---|---|---|
| README | ✓ Completed | Getting Started + Deploy (RC2); fingerprint aligned (V1SP-005). |
| Release Notes | ✓ Completed | `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`. |
| Release Manifest | ✓ Completed | `knowledge/releases/RC2_RELEASE_MANIFEST.md` created and populated for known fields (2026-07-18). |
| Changelog | ✓ Completed | `CHANGELOG.md` entry `[1.0.0]` — Version1-RC2. |
| Deployment Guide | ✓ Completed | README Deploy (RC2) + `docs/process/RELEASE_PROTOCOL.md`. Historical `docs/release/*_v0.4.0.md` must **not** be used as RC2 runbook. |
| `knowledge/` tree | ✓ Completed | Present with architecture, educational, releases, product, etc. |
| `knowledge/releases/` | ✓ Completed | Present. |
| `knowledge/product/roadmap/` (canonical) | ✓ Completed | Intentional path is `knowledge/product/roadmap/` (tracked stub `README.md`). Do **not** create `knowledge/roadmap/`. Documented in `knowledge/README.md` and `KWALITEC_VERSION1_RELEASE_CERTIFICATION.md`. |

**Note:** RC2 release artefacts under `knowledge/releases/` are included in the RC2 release documentation commit. Version 2 planning remains outside that commit at `knowledge/product/roadmap/VERSION2_PRODUCT_STRATEGY.md`.

---

## Internal Alpha

| Check | Status | Evidence / reason |
|---|---|---|
| Alpha participant list confirmed | ⚠ Pending | No participant roster confirmation recorded in this session. |
| Feedback process confirmed | ✓ Completed | Product Check-in → Founder Feedback (IPV); offline week pipeline docs in FSI-003. Operator must still brief participants. |
| Founder monitoring ready (product) | ✓ Completed | Command Centre surfaces ready in IPV when allowlisted. |
| Founder monitoring ready (live ops) | ⚠ Pending | Live monitoring after deploy pending. |
| Backup schedule active | ⚠ Pending | Not confirmed for production PostgreSQL. |

---

## Git / deploy readiness (launch-critical)

| Check | Status | Evidence / reason |
|---|---|---|
| Intended commit on `origin/main` | ⚠ Pending | Local `main` remains ahead of `origin/main` until push. Repository is prepared for push; publish is an operator step (not performed in this milestone). |
| Working tree clean for release | ✓ Completed | RC2 release docs staged/committed; harness output ignored via `.gitignore` (`instance/*_harness_out.txt`); Version 2 strategy relocated out of release commit scope to `knowledge/product/roadmap/VERSION2_PRODUCT_STRATEGY.md`. No application WIP. |
| Tag `v1.0.0` / RC2 tag | ⚠ Pending | Not created as part of this checklist. |
| Production fingerprint matches intended commit | ⚠ Pending | Not verified on live production. |

---

## Release Approval

| Role | Status | Basis |
|---|---|---|
| Engineering | ✓ Completed | RC2 operational readiness **APPROVED WITH MINOR ISSUES**; V1SP-001B High closure; V1SP-004 **PASS WITH LOW-RISK OBSERVATIONS**; V1SP-005 documentation **PASS WITH MINOR**. |
| Product | ✓ Completed | IPV-RC2 release decision **APPROVE** (invite-only Internal Alpha baseline). |
| Founder | ⚠ Pending | Explicit Founder day-of launch sign-off **not recorded**. Product/engineering gates are clear; Founder should confirm backup, participant list, and go-live window. |

---

## Release Decision

**Exactly one selected:**

- [x] **RELEASE RC2** (Internal Alpha baseline — repository ready; day-of deploy steps remain operator observations)
- [ ] HOLD RELEASE

### Why RELEASE (with observations)

Product quality for invite-only Internal Alpha is **approved** by prior gates. Repository operational blockers for the release documentation tree are **cleared**:

1. ~~Clean or intentionally archive untracked release artefacts~~ — **Done:** IPV/checklist/manifest/readiness docs in release commit; harness ignored; Version 2 strategy excluded from RC2 commit.
2. ~~Roadmap path ambiguity~~ — **Done:** canonical path confirmed as `knowledge/product/roadmap/`.

**Remaining operator observations (do not block repository APPROVED WITH OBSERVATIONS):**

1. **Publish** — push local `main` (including this release documentation commit) to `origin/main`.
2. **Confirm production backup** (and restore awareness) before migration/deploy.
3. **Deploy + fingerprint** — Render build for the published commit; `/health` OK with `version=1.0.0`; chrome Build RC2.
4. **Live production smoke** — student learning loop + Founder Overview / Operational Health / Feedback / Vision / Internal Alpha / Releases.
5. **Founder ops confirmation** — participant list, feedback briefing, backup schedule, Founder allowlist (`ADMIN_EMAIL`).

### Clear-to-go-live criteria

When observations 1–5 above are checked ✓ (and Founder approval is ✓), proceed with production cutover per `docs/process/RELEASE_PROTOCOL.md` §7–10.

---

## Prior gate summary (build fitness)

| Gate | Verdict |
|---|---|
| RC2 Operational Readiness | APPROVED WITH MINOR ISSUES |
| V1SP-001B Operational Fixes | High findings closed |
| V1SP-004 Security Verification | PASS WITH LOW-RISK OBSERVATIONS |
| V1SP-005 Documentation Completion | PASS WITH MINOR OBSERVATIONS |
| IPV-RC2 Independent Product Validation | APPROVE |

---

## Files created / modified this milestone

| Path | Action |
|---|---|
| `knowledge/releases/RC2_LAUNCH_CHECKLIST.md` | Updated (✓ / ⚠ / ✗ audit) |
| `knowledge/releases/RC2_RELEASE_MANIFEST.md` | Created |
| `knowledge/releases/RC2_FINAL_READINESS_REPORT.md` | Created |

Application code: **unchanged**.

---

## References

- `docs/process/RELEASE_PROTOCOL.md`
- `docs/release/RELEASE_NOTES_v1.0.0-RC2.md`
- `CHANGELOG.md`
- `README.md` (Deploy RC2)
- `render.yaml`
- `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md`
- `knowledge/releases/RC2_RELEASE_MANIFEST.md`
- `knowledge/releases/RC2_FINAL_READINESS_REPORT.md`
- `knowledge/releases/V1SP-004_SECURITY_VERIFICATION.md`
- `knowledge/releases/V1SP-005_DOCUMENTATION_COMPLETION.md`
- `knowledge/releases/IPV-RC2_REPORT.md`
