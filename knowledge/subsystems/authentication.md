# Authentication

## Purpose

Authentication establishes who the user is and gates personal learning data (plans, missions, progress). Kwalitec uses **Flask-Login** with session cookies. Public self-registration is **intentionally disabled**; admin accounts are created via `flask create-admin` or production `StartupService` from `ADMIN_EMAIL` / `ADMIN_PASSWORD`.

Blueprint: `auth` (`/auth`) — login and logout. Login view name: `auth.login`.

## Responsibilities

| Concern | Owner |
|---|---|
| Login form, credential check, session | `auth` blueprint + Flask-Login |
| Logout | `auth` blueprint |
| Admin user bootstrap | CLI `create-admin` / `StartupService` (production) |
| Protect feature routes | `@login_required` on blueprints |
| CSRF on state-changing forms | Flask-WTF (enabled outside tests) |
| Open redirect protection | Post-login `next` URL allowlist (local only) |
| Security headers / CSP | `app/__init__.py` after-request hook |

Authorization for personal resources is **not** a separate IdP layer: services and routes must scope queries to `current_user` (or explicit `user_id`) and avoid leaking other users’ ids.

## Dependencies

```
Browser
  → auth.login (WTForms + CSRF)
  → User model (password hash verify)
  → flask_login.login_user
  → redirect to dashboard / safe next

Protected blueprints
  → @login_required
  → services with user_id / ownership checks
```

- **Depends on:** `User` model, `SECRET_KEY`, env-configured admin bootstrap in production.
- **Related:** `StartupService` (migrate + admin, production-gated, non-destructive).
- **Does not include:** OAuth/social login (not part of current architecture).

## Data Flow

```
GET/POST /auth/login
    → if authenticated, redirect away
    → validate LoginForm
    → lookup user by normalised email
    → verify password
    → login_user (optional remember)
    → redirect to safe next or dashboard

POST /auth/logout (login_required)
    → logout_user → redirect login
```

Production startup (orthogonal but related):

```
create_app() → StartupService.run(app)
    → alembic upgrade (safe)
    → ensure admin from ADMIN_EMAIL / ADMIN_PASSWORD (idempotent)
```

## Extension Points

- Additional authn factors or SSO would be a dedicated milestone; do not bolt tokens into random services.
- Role checks (if expanded beyond admin flag) should stay at blueprint edges and explicit service guards.
- Keep email normalisation (lower/strip) consistent with existing auth routes.

## Common Pitfalls

| Pitfall | Why it hurts |
|---|---|
| Exposing public registration | Violates product security posture |
| Open redirects via unchecked `next` | Account phishing / token theft patterns |
| Logging passwords or full DB URLs | Secret leakage |
| Skipping ownership checks because “obscure ids” | IDOR risk |
| Disabling CSRF outside tests | Cross-site write risk |
| Committing `.env` | Credential leak |

## Future Improvements

- Explicit role/permission model if multi-admin or coach roles appear.
- Audit logging for admin bootstrap and failed logins (without logging secrets).
- Session hardening reviews aligned with deployment (HTTPS, cookie flags) on Render.

**See also:** `.cursor/rules/10-security.mdc`, [ADR-002](../architecture/ADR-002-blueprint-architecture.md), [`CONTRIBUTING.md`](../../CONTRIBUTING.md).
