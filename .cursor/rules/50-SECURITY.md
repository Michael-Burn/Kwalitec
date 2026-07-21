# Security Requirements

**Status:** Permanent Cursor governance  
**Companion:** [`.cursor/rules/10-security.mdc`](10-security.mdc), [`src/infrastructure/security/`](../../src/infrastructure/security/)

Security by default. Every external input is untrusted until validated.

---

## Authentication and passwords

| Requirement | Implementation |
|---|---|
| **Argon2 hashing** | `infrastructure.security.Argon2PasswordHasher` (Argon2id). Application uses `PasswordHasher` port — never imports Argon2 directly. |
| **Password policy** | Enforce minimum length and complexity at validation boundary (domain/application). Reject weak passwords before hashing. |
| **Constant-time comparisons** | Use `hmac.compare_digest` or framework equivalents for tokens and secrets. Never compare secrets with `==`. |
| **Session timeout** | Configured session lifetime; idle timeout where applicable. |
| **Account lockout** | Rate-limit or lock after repeated failed login attempts. |

---

## Web security

| Requirement | Detail |
|---|---|
| **CSRF** | Flask-WTF CSRF enabled outside tests. Preserve CSRF tokens in all POST forms. |
| **Secure cookies** | `SESSION_COOKIE_SECURE` in production; `HttpOnly`; `SameSite` appropriate for deployment. |
| **Rate limiting** | Apply to auth endpoints and sensitive operations. |
| **Open redirects** | Reject non-local `next` URLs after login. |
| **Security headers** | Preserve CSP and security header behaviour in app factory. |

---

## Authorization

- `@login_required` on authenticated views.
- Scope queries to the current user for personal resources (plans, missions, progress, twin).
- Return 403/404 appropriately; do not leak existence of foreign resources.
- Registration is **not** publicly exposed. Admin via `flask create-admin` or `StartupService`.

---

## Input validation

- Prefer WTForms for POST data.
- Normalize emails (lower/strip) consistently.
- Validate wizard/step inputs server-side even when UI constrains them.
- **Validate all external input** — query params, JSON bodies, file uploads, headers used for logic.

---

## Secrets and environment

| Rule | Detail |
|---|---|
| **Secrets never committed** | `.env` is local only; use host env in production. |
| **No hard-coded credentials** | `SECRET_KEY`, `ADMIN_PASSWORD`, `DATABASE_URL` from environment. |
| **No credential logging** | Never log passwords, session cookies, or full DB URLs with credentials. |
| **Production `SECRET_KEY`** | Factory validates; default insecure key aborts production startup. |
| **Least privilege** | DB users, API keys, and service accounts scoped to minimum required access. |

---

## SQLAlchemy safety

- ORM queries or bound parameters only — never concatenate user input into SQL.
- Roll back on 500 paths.
- No raw DDL from request handlers.
- Schema changes through Alembic migrations only.

---

## Dependencies and network

- Treat new network calls and third-party script CDNs as security-sensitive (CSP impact).
- AI provider keys in environment variables only.
- AI failures must degrade enrichment only — never bypass auth or leak twin data.

---

## Layer placement

| Concern | Layer |
|---|---|
| Password hashing implementation | Infrastructure (`Argon2PasswordHasher`) |
| Auth use-cases and ports | Application (`application.auth`) |
| Auth domain rules | Domain (`domain.auth`) |
| Login/logout HTTP | Adapters (`adapters.flask.auth`) |
| Session middleware | Adapters / Infrastructure config |

Domain and Application must not import Argon2, Flask-Login, or SQLAlchemy directly.
