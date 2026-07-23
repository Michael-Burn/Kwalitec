# GA-001 Security Review

**Programme:** GA-001 — Workstream 4  
**Evidence:** `tests/ga/test_security_review.py`, `tests/test_pr001_production_readiness.py`  
**Scope:** RBAC, portal separation, session/CSRF/cookies/headers, input validation, secrets, CSP residual risk.

## Findings summary

| Area | Status | Notes |
|---|---|---|
| RBAC roles & permissions | **Pass** | Founder/Admin/Support/Student matrix enforced; least-privilege student portal |
| Portal separation | **Pass** | Console requires capability; students receive 403 |
| Session security | **Pass** | `HttpOnly`, `SameSite=Lax`; production `Secure` cookies |
| CSRF | **Pass** | Enabled outside tests (`WTF_CSRF_ENABLED`) |
| Cookie flags | **Pass** | Production mirrors session + remember-me Secure/HttpOnly/SameSite |
| Security headers | **Pass** | nosniff, DENY frame, Referrer-Policy, Permissions-Policy, CSP, HSTS in production |
| Input validation | **Pass** | WTForms on auth/feedback/telemetry; open-redirect `next` restricted to local paths |
| Secrets | **Pass** | Production rejects insecure/short `SECRET_KEY`; requires `DATABASE_URL` |
| CSP residual | **Accepted risk** | `'unsafe-inline'` + `cdn.jsdelivr.net` still required for legacy templates/Chart.js |

## RBAC

- Roles: founder, administrator, content_manager, support, research, student
- Console access: capability `console` + permission `console.access`
- Identity tables: `user_roles`, `user_capabilities` (PR-001 migration)
- Legacy allowlist (`ADMIN_EMAIL` / `FOUNDER_EMAILS`) still bridges to durable Founder roles

## Portal separation

- Student portal surfaces: `/student/*`, missions, study plan, settings, alpha help
- Console: `/console/*` (founder dashboard blueprint)
- One identity may hold both portals via capabilities; students without Console are denied

## Session / CSRF / cookies

| Setting | Non-production | Production |
|---|---|---|
| CSRF | On (tests off) | On (validated at startup) |
| Session HttpOnly | Yes | Yes |
| Session Secure | Off | On |
| SameSite | Lax | Lax |

## Headers

Present on responses (including health):

- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy` (sensors/camera/mic denied)
- `Content-Security-Policy` (self + jsDelivr + unsafe-inline)
- `Strict-Transport-Security` when `APP_ENV=production`

## CSP residual issues (not GA blockers)

1. `'unsafe-inline'` for scripts/styles — required by Analytics Chart.js bootstrap, Product Check-in, Study Plan wizard confirms, and similar template patterns.
2. `https://cdn.jsdelivr.net` allowlist — Chart.js / related assets.
3. Prefer nonces/hashes + self-hosted assets in a post-GA hardening milestone.

## Secrets hygiene

- Never commit `.env`
- Production startup validation rejects default/short secrets
- Health and logs must not emit credentials or full DB URLs with passwords (operator discipline)

## Recommendation

Security posture is **sufficient for GA** with documented CSP tech debt. No open P0 authz bypass found in automated review. Schedule CSP nonce migration as a dedicated security hardening programme after GA.
