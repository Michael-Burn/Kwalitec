# V1SP-004 — Security & Configuration Verification

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-004  
**Status:** VERIFICATION complete  
**Nature:** Independent audit (no feature development). No Critical or High blockers requiring immediate code change.  
**Date:** 2026-07-17  
**Build identity:** Product `1.0.0` (`pyproject.toml` / `APP_VERSION`) · Internal Alpha chrome **Build RC2**  
**Prior hardening:** V1SP-001B (cookies, redirects, SECRET_KEY gate) · V1SP-003 (performance; no security surface expansion)  
**Commit:** N/A — verification report only (no application code change)

---

## Executive Summary

Kwalitec RC2 was independently re-verified against authentication, authorisation, session, CSRF, redirect, header, configuration, error-handling, dependency, logging, and deployment standards required for continued Internal Alpha deployment.

**Verdict:** Security and configuration posture is **fit for continued RC2 Internal Alpha operation**. V1SP-001B hardening (open-redirect, production cookies, ProductionConfig SECRET_KEY gate) remains effective. Protected student and Founder surfaces correctly deny anonymous and non-Founder access. Production responses emit expected security headers, including HSTS when `APP_ENV=production`. CSRF rejects missing tokens on state-changing POSTs; AJAX `X-CSRFToken` is honoured.

No **Critical** or **High** defects were found that block Alpha deployment. Remaining items are **Medium / Low / Informational** (known Alpha deferrals, dependency pin hygiene, backup restore limits, auth audit-logging gaps). **No application code changes were made in this milestone.**

---

## Verification Matrix

| # | Area | Result | Notes |
|---|---|---|---|
| 1 | Authentication | **PASS** | Login, logout, remember-me, invalid credentials verified; password reset N/A |
| 2 | Authorisation | **PASS** | `@login_required` / `@founder_required`; ownership scoping; 403 for non-Founders |
| 3 | Session security | **PASS** | Production `Secure` / `HttpOnly` / `SameSite=Lax`; logout clears remember + session auth |
| 4 | CSRF protection | **PASS** | Forms + AJAX header; missing token → 400; no bypass found |
| 5 | Redirect safety | **PASS** | Absolute, protocol-relative, encoded, backslash, and malformed `next` rejected |
| 6 | HTTP security headers | **PASS** | CSP, XFO, Referrer-Policy, nosniff, Permissions-Policy, HSTS (prod) |
| 7 | Configuration | **PASS** | `DEBUG=False` in ProductionConfig; SECRET_KEY gate; Render env separation |
| 8 | Error handling | **PASS** | Friendly 403/404/500; no stack traces in production-mode handler |
| 9 | Dependencies | **PASS*** | Medium findings documented; no Critical runtime exploit path for current deploy |
| 10 | File handling | **PASS*** | Backup restore only; limits/mass-assignment are Medium observations |
| 11 | Logging | **PASS*** | Errors logged; credentials not logged; auth event audit is thin (Low) |
| 12 | Deployment configuration | **PASS** | `render.yaml` production env; migrate-on-start; static fingerprint |

\* = PASS with documented Medium/Low observations (see Findings).

---

## Findings

### Critical

None.

### High

None.

### Medium

#### M-1 — No login rate limiting / lockout

| Field | Detail |
|---|---|
| **Description** | Failed logins are not throttled at the application or documented edge layer. |
| **Evidence** | `app/auth/routes.py` accepts unlimited POSTs; RC2 finding M-1 still open; V1SP-001B explicitly deferred. |
| **Impact** | Credential stuffing risk against invite-only Alpha accounts. |
| **Recommendation** | Add IP+email rate limiting or edge WAF rules before public/wider cohorts. |
| **Status** | Open — accepted for invite-only Alpha |

#### M-2 — CSP still requires `'unsafe-inline'` (+ CDN scripts)

| Field | Detail |
|---|---|
| **Description** | Production CSP allows `'unsafe-inline'` for scripts/styles and `https://cdn.jsdelivr.net` (required after RC2 C-1 fix for Charts / Check-in / wizard / confirms). |
| **Evidence** | `app/__init__.py` `_add_security_headers`; RC2 C-1 / M-13 follow-up. |
| **Impact** | XSS impact window is larger than a nonce/hash CSP. |
| **Recommendation** | Move inline scripts to static files; introduce nonces; prefer vendored assets. |
| **Status** | Open — accepted for Alpha; do not reintroduce C-1 breakage |

#### M-3 — Backup restore lacks size cap and field allowlist

| Field | Detail |
|---|---|
| **Description** | `POST /settings/import/restore` accepts multipart JSON without `MAX_CONTENT_LENGTH` and reconstructs ORM rows via `model_class(**record_data)` (ownership forced to `current_user.id`). |
| **Evidence** | `app/settings/routes.py` `import_restore`; `app.config` has no `MAX_CONTENT_LENGTH`; RC2 M-13. |
| **Impact** | Authenticated DoS via large upload; residual mass-assignment surface within own user data. Filename is not written to disk (path traversal N/A). |
| **Recommendation** | Set `MAX_CONTENT_LENGTH`; allowlist restore columns per model. |
| **Status** | Open — Alpha-only authenticated feature |

#### M-4 — Example `SECRET_KEY` not in insecure deny-list

| Field | Detail |
|---|---|
| **Description** | `_INSECURE_SECRET_KEYS` rejects `dev-change-this-secret-key` but not `.env.example`’s `change-this-secret-key`. A misconfigured host selecting `ProductionConfig` with the example value would start. |
| **Evidence** | Ad-hoc probe: `_validate_env_vars(ProductionConfig)` with `SECRET_KEY=change-this-secret-key` succeeds. Render uses `generateValue: true` for `SECRET_KEY`. |
| **Impact** | Misconfiguration risk outside the standard Render path. |
| **Recommendation** | Add `change-this-secret-key` (and similar placeholders) to `_INSECURE_SECRET_KEYS`. |
| **Status** | Open — Render path safe; fix in next hardening pass |

#### M-5 — Flask pin below current security releases

| Field | Detail |
|---|---|
| **Description** | `requirements.txt` pins `Flask==3.1.0`. `pip-audit` reports PYSEC-2026-1377 (fix ≥3.1.1; SECRET_KEY_FALLBACKS ordering) and PYSEC-2026-2151 / CVE-2026-27205 (fix ≥3.1.3; `Vary: Cookie` on some session key accesses). |
| **Evidence** | `pip-audit -r requirements.txt`; installed `Flask=3.1.0`; codebase does **not** set `SECRET_KEY_FALLBACKS`; HTML responses set `Cache-Control: no-store`. |
| **Impact** | Low practical exploitability on current RC2 deploy; still overdue pin hygiene. |
| **Recommendation** | Upgrade to `Flask>=3.1.3` in a dedicated dependency bump with regression suite. |
| **Status** | Open — Medium for inventory; mitigated in practice |

#### M-6 — Remember-me cookie clear may omit Secure attributes

| Field | Detail |
|---|---|
| **Description** | Flask-Login 0.6.3 `delete_cookie` on logout passes name/path/domain only. Production remember cookies are set with `Secure; HttpOnly; SameSite=Lax`; the clearing `Set-Cookie` observed in probes lacked those flags. |
| **Evidence** | Probe logout `Set-Cookie: remember_token=; Expires=…; Max-Age=0; Path=/`; Flask-Login `login_manager.py` `_update_remember_cookie` delete path. Session auth is cleared; dashboard redirects to login in the test client. |
| **Impact** | Strict browsers may retain a Secure remember cookie after logout, allowing silent re-auth until expiry. |
| **Recommendation** | Explicitly `response.delete_cookie(..., secure=True, httponly=True, samesite="Lax")` after `logout_user()`, or upgrade Flask-Login when a fix is available; manually verify on HTTPS Chrome. |
| **Status** | Open — Medium; session cookie path verified cleared |

### Low

#### L-1 — Authentication events not structured in logs

| Field | Detail |
|---|---|
| **Description** | Successful/failed logins are not explicitly logged (only flash + CSRF missing-token logs from Flask-WTF). |
| **Evidence** | `app/auth/routes.py`; `knowledge/subsystems/authentication.md` lists audit logging as a future improvement. |
| **Impact** | Weaker forensic trail for abuse detection. |
| **Recommendation** | Log login success/failure with email hash or normalised email; never log passwords. |
| **Status** | Open |

#### L-2 — python-dotenv advisory (set_key symlink)

| Field | Detail |
|---|---|
| **Description** | `python-dotenv==1.0.1` flagged PYSEC-2026-2270 (symlink follow in `set_key` / `unset_key`). App uses `load_dotenv()` only. |
| **Evidence** | `pip-audit`; `app/config.py` `load_dotenv()`. |
| **Impact** | Runtime Alpha path unaffected; local/CI scripts that rewrite `.env` could be. |
| **Recommendation** | Bump to `python-dotenv>=1.2.2` with Flask bump. |
| **Status** | Open |

#### L-3 — Long remember-me duration (library default)

| Field | Detail |
|---|---|
| **Description** | `REMEMBER_COOKIE_DURATION` not overridden (Flask-Login default ~365 days). |
| **Evidence** | `ProductionConfig` sets Secure/HttpOnly/SameSite only. |
| **Impact** | Long-lived remember tokens on shared devices. |
| **Recommendation** | Set an Alpha-appropriate duration (e.g. 14–30 days) when tightening sessions. |
| **Status** | Open |

### Informational

| ID | Description | Status |
|---|---|---|
| I-1 | Password reset not implemented; login directs users to coordinator — intentional for Alpha | N/A / accepted |
| I-2 | Public registration closed (`/auth/register` → 404) | Confirmed |
| I-3 | `pytest` advisory (PYSEC-2026-1845) — test dependency only | Non-prod |
| I-4 | Werkzeug installed as 3.1.8 (transitive) — Windows device-name CVEs not applicable to Render Linux | OK |
| I-5 | HSTS gated on `APP_ENV==production` string (cookies gated on `ProductionConfig` class) — aligned on Render | OK |
| I-6 | Auth subsystem doc still says logout is `@login_required`; code correctly omits it for idempotency | Doc drift |
| I-7 | `/health` exposes version + DB connectivity (no secrets) — appropriate | OK |

---

## Security Findings Register

| ID | Severity | Area | Title | Status |
|---|---|---|---|---|
| M-1 | Medium | Auth | No login rate limiting | Open (Alpha deferral) |
| M-2 | Medium | Headers | CSP `'unsafe-inline'` + CDN | Open (Alpha deferral) |
| M-3 | Medium | Files | Backup restore size / allowlist | Open (RC2 M-13) |
| M-4 | Medium | Config | Example SECRET_KEY not denied | Open |
| M-5 | Medium | Dependencies | Flask &lt; 3.1.3 advisories | Open (mitigated) |
| M-6 | Medium | Session | Remember-me Secure delete flags | Open |
| L-1 | Low | Logging | No auth success/failure audit logs | Open |
| L-2 | Low | Dependencies | python-dotenv set_key advisory | Open |
| L-3 | Low | Session | 365-day remember default | Open |
| I-1…I-7 | Info | Various | See Informational | Recorded |

---

## Regression Results

### Security regression

| Suite / probe | Outcome |
|---|---|
| `tests/test_v1sp001b_operational_fixes.py` (redirects, cookies, SECRET_KEY, static cache) | **PASS** |
| `tests/test_auth.py` (login/logout/invalid/safe next/protected redirects) | **PASS** |
| `tests/test_config.py` | **PASS** |
| Ad-hoc ProductionConfig + CSRF-on probe (headers, CSRF 400, remember Secure flags, logout, Founder 403) | **PASS** |
| `pip-audit -r requirements.txt` | 4 advisories in 3 packages (documented) |

### Authentication regression

| Check | Result |
|---|---|
| Login valid credentials | PASS |
| Invalid / nonexistent user | PASS (generic message) |
| Remember me sets `remember_token` with Secure/HttpOnly/SameSite | PASS |
| Logout → login; subsequent dashboard → login redirect | PASS |
| Session invalidation (session auth cleared) | PASS |
| Password reset | **NOT APPLICABLE** |
| Public registration closed | PASS (`test_rr001b`) |

### Authorisation / Founder regression

| Check | Result |
|---|---|
| Founder Overview / Operational Health / Vision / Feedback / Internal Alpha as student | **403** |
| `tests/test_founder_dashboard.py`, `test_iahf003`, `test_v1sp001c`, `test_v1sp001d`, `test_rip003` | **PASS** |
| Anonymous access to student surfaces | Redirect to login |

### Student regression

| Check | Result |
|---|---|
| Dashboard / Analytics / Study Session ownership suites (`test_lxp002`, auth protected routes) | **PASS** |
| Study plan / mission ownership patterns (`current_user.id`, `get_owned_mission`) | Confirmed in code + tests |

### Operational regression

| Check | Result |
|---|---|
| Security headers on HTML | PASS (`no-store`, CSP, XFO, …) |
| Static assets cacheable + `v=` fingerprint | PASS (V1SP-001B) |
| `tests/test_routes.py` full module | **1 unrelated FAIL**: `test_dashboard_no_curriculum_summary_when_no_study_plan` (copy assertion drift; not a security defect) |

Focused security/authz run: **115 passed** (`test_auth`, `test_v1sp001b`, `test_config`, founder/OH/vision, registration closed, LXP-002 session).

---

## Area Detail (evidence)

### 1. Authentication

- Login: WTForms + email normalise + `User.check_password` (`app/auth/routes.py`, `LoginForm`).
- Logout: POST, CSRF-protected, **not** `@login_required` (idempotent; intentional).
- Remember me: `login_user(..., remember=form.remember_me.data)`.
- Invalid credentials: generic `"Invalid email or password."`
- Password reset: not implemented — **N/A** (coordinator path for Alpha).

### 2. Authorisation

- Student blueprints: `@login_required` (dashboard, mission, study_plan, analytics, settings, calibration, research check-in).
- Founder Command Centre + legacy `/research/founder*`: `@founder_required` (login + email allowlist from `ADMIN_EMAIL` / `FOUNDER_EMAILS`).
- Ownership: missions via `StudySessionService.get_owned_mission`; study plans compare `study_plan.user_id != current_user.id`.

### 3. Session security

| Flag | ProductionConfig |
|---|---|
| `SESSION_COOKIE_SECURE` | `True` |
| `SESSION_COOKIE_HTTPONLY` | `True` |
| `SESSION_COOKIE_SAMESITE` | `Lax` |
| `REMEMBER_COOKIE_*` | Mirror session |

Logout clears remember cookie (Max-Age=0) and replaces session with anonymous CSRF session. See M-6 for Secure delete nuance.

### 4. CSRF

- `WTF_CSRF_ENABLED = True` outside tests; `CSRFProtect` in factory.
- Meta `csrf-token` in base layouts; `mission.js` sends `X-CSRFToken`.
- Probe: bare POST `/auth/login` → **400**; logout without token → **400**; header token accepted.

### 5. Redirect safety

`_safe_next_url` rejects scheme/netloc, `//` / `///`, backslashes, control chars, and multi-decode `%2f%2f` bypasses; returns normalised path only. Covered by `test_v1sp001b` parametrised cases.

### 6. HTTP security headers

Observed under `APP_ENV=production` / `ProductionConfig`:

| Header | Value (summary) |
|---|---|
| Content-Security-Policy | `default-src 'self'` … `'unsafe-inline'` + jsDelivr |
| X-Frame-Options | `DENY` |
| Referrer-Policy | `strict-origin-when-cross-origin` |
| X-Content-Type-Options | `nosniff` |
| Permissions-Policy | sensors/camera/mic/… disabled |
| Strict-Transport-Security | `max-age=31536000; includeSubDomains` |
| Cache-Control | `no-store` (HTML); `public, immutable` (static) |

### 7. Configuration

- `ProductionConfig.DEBUG = False`.
- Config selection: `APP_ENV` (fallback `FLASK_ENV`).
- Insecure SECRET_KEY rejected when `ProductionConfig` active (V1SP-001B H-3); gap for example key → M-4.
- DB: `DATABASE_URL` → psycopg v3 normalisation; else SQLite instance path.
- Logs driver **prefix only** (no credentials).

### 8. Error handling

- Custom 403/404 always; 500 when `PROPAGATE_EXCEPTIONS` is false.
- Template copy is user-friendly; probe confirmed no traceback leak for intentional 500.
- `logger.exception` retains server-side diagnostics.

### 9. Dependencies

```
pip-audit -r requirements.txt
Flask 3.1.0          PYSEC-2026-1377 → 3.1.1 ; PYSEC-2026-2151 → 3.1.3
python-dotenv 1.0.1  PYSEC-2026-2270 → 1.2.2
pytest 8.3.4         PYSEC-2026-1845 → 9.0.3   (dev only)
```

Transitive `Werkzeug==3.1.8` is current enough for Linux deploy.

### 10. File handling

Only upload path: authenticated JSON backup restore. No general media upload. Validation: UTF-8 JSON + `metadata.version == "1.0"` + force `user_id`. Gaps → M-3. Directory traversal via filename: **N/A** (content parsed in memory).

### 11. Logging

- App errors / 500 / Founder provider failures logged.
- Startup logs env names and DB driver prefix — not secrets.
- Auth success/failure not explicitly logged → L-1.

### 12. Deployment configuration

| Item | Evidence |
|---|---|
| Environment separation | `render.yaml` `APP_ENV=production`; local `.env.example` development |
| SECRET_KEY | Render `generateValue: true` |
| Database | Render Postgres `DATABASE_URL` |
| Migrations | `StartupService` production-only alembic upgrade (idempotent) |
| Static fingerprint | `STATIC_ASSET_VERSION` = `{APP_VERSION}-{INTERNAL_ALPHA_BUILD_LABEL}` |
| Process | `waitress-serve --port=$PORT wsgi:app` |

---

## Production Readiness

| Question | Answer |
|---|---|
| Continue Internal Alpha on RC2? | **Yes** |
| Security blockers for Alpha? | **None Critical / High** |
| Ship as public / open registration? | **No** — invite-only; close M-1/M-2/M-5 first for wider exposure |
| V1SP-001B controls still effective? | **Yes** |
| V1SP-003 introduced new security regressions? | **No** (perf-only; one unrelated dashboard copy test drift) |

---

## Recommendation

**PASS WITH LOW-RISK OBSERVATIONS**

RC2 may proceed as the operational Internal Alpha baseline. Track Medium items M-1–M-6 on the stabilisation backlog; prioritise Flask ≥3.1.3, SECRET_KEY deny-list completion, and remember-cookie Secure deletion before expanding beyond invite-only Alpha.

---

## Acceptance Criteria Checklist

| Criterion | Met |
|---|---|
| Authentication verified | ✓ |
| Authorisation verified | ✓ |
| Session security verified | ✓ |
| CSRF verified | ✓ |
| Redirect protection verified | ✓ |
| Security headers reviewed | ✓ |
| Production configuration verified | ✓ |
| Error handling verified | ✓ |
| Dependencies reviewed | ✓ |
| Deployment configuration verified | ✓ |
| Findings documented | ✓ |
| Overall recommendation issued | ✓ |

---

## Implementation

**None.** Verification did not uncover Critical/High defects requiring an immediate code commit. Medium/Low observations are recorded for follow-up hardening milestones.

---

## References

- `knowledge/releases/RC2_OPERATIONAL_READINESS_REPORT.md`
- `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md`
- `knowledge/releases/V1SP-003_PERFORMANCE_OPTIMISATION.md`
- `ARCHITECTURE.md` (Security Architecture summary)
- `PRODUCT_BLUEPRINT.md`
- `knowledge/subsystems/authentication.md`
- `.cursor/rules/10-security.mdc`
