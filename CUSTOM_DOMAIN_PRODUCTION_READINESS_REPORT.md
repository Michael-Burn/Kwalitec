# Custom Domain Production Readiness Report

**Date:** 2026-07-31  
**Scope:** Configuration and deployment readiness for a Render custom domain  
**Constraint:** No educational / product behaviour changes

---

## Summary

Kwalitec is ready for a custom-domain cutover on Render. The app already had production-safe cookies, CSRF, HSTS, ProxyFix, and static cache headers. This pass adds a configuration-driven `APP_URL`, optional `SERVER_NAME` / `SESSION_COOKIE_DOMAIN`, APP_URL-aware sitemap/robots/OG metadata, Render env wiring, and an operator cutover checklist.

---

## Audit findings (already healthy)

| Area | Status |
|---|---|
| `SESSION_COOKIE_SECURE` / HttpOnly / SameSite=Lax | Pass (`ProductionConfig`) |
| Remember-me cookie mirrors | Pass |
| CSRF enabled; rejected if disabled in production | Pass |
| HSTS (`max-age=31536000; includeSubDomains`) when `APP_ENV=production` | Pass |
| `ProxyFix` via `TRUSTED_PROXY_HOPS` (prod default `1`) | Pass |
| HTML `Cache-Control: no-store`; static `public, max-age, immutable` | Pass |
| Favicon / manifest relative paths | Pass (host follows request) |
| Hardcoded `*.onrender.com` in `app/` / `src/` | None found |

---

## Files changed and why

| File | Why |
|---|---|
| `app/config.py` | Add `APP_URL`, optional `SERVER_NAME` / `SESSION_COOKIE_DOMAIN`, scheme inference from `APP_URL`, remember-cookie domain mirror |
| `app/public_url.py` | **New** — normalize / resolve public origin for absolute links |
| `app/__init__.py` | Warn if `APP_URL` unset in production; log domain config; register `/robots.txt` + `/sitemap.xml`; inject `app_url` / `canonical_page_url` / `social_preview_url` into templates |
| `app/templates/partials/brand_meta.html` | Add `canonical` + `og:url`; drive OG/Twitter images from `APP_URL` when set |
| `.env.example` | Document `APP_URL`, `SERVER_NAME`, `SESSION_COOKIE_DOMAIN` |
| `render.yaml` | Declare `APP_URL` (sync), `PREFERRED_URL_SCHEME`, `TRUSTED_PROXY_HOPS` |
| `docs/production/ENVIRONMENT.md` | Document custom-domain env vars |
| `docs/production/DEPLOYMENT.md` | Point operators at `APP_URL` + cutover guide |
| `docs/production/CUSTOM_DOMAIN_CUTOVER.md` | **New** — checklist for Render URL → custom domain |
| `docs/production/README.md` | Index the cutover guide |
| `docs/ga/RELEASE_CHECKLIST.md` | Require `APP_URL` on GA deploys |
| `tests/test_custom_domain_readiness.py` | **New** — config, robots/sitemap, metadata, URL generation tests |
| `knowledge/evidence/releases/.../capture_rc08_evidence.py` | Remove hardcoded `onrender.com` default; require `KWALITEC_BASE_URL` or `APP_URL` |
| `knowledge/evidence/releases/.../capture_rc09_evidence.py` | Same as above |
| `CUSTOM_DOMAIN_PRODUCTION_READINESS_REPORT.md` | This report |

---

## Recommendations (ops, not code)

1. Set `APP_URL=https://<canonical-host>` on Render before declaring cutover complete.
2. Leave `SERVER_NAME` and `SESSION_COOKIE_DOMAIN` **unset** during dual-host cutover.
3. Expect users to re-login after hostname change (cookies are host-scoped).
4. Do not submit HSTS preload until the custom domain is permanent.
5. Follow `docs/production/CUSTOM_DOMAIN_CUTOVER.md` end-to-end.

---

## Tests executed

```bash
python3 -m pytest tests/test_custom_domain_readiness.py -q
```

Result: **10 passed**.

---

## Migration impact

None.

---

## Architecture compliance

Additive config + presentation/metadata only. Curriculum V1/V2 loaders untouched. Layering preserved (routes → helpers; no business-rule changes).

---

## Technical debt / limitations

- Historical evidence JSON under `knowledge/` still records the old Render URL as captured artefacts (intentional archives).
- CSP still allows `'unsafe-inline'` + jsDelivr (pre-existing residual).
- Sitemap lists only public entry URLs (`/`, `/auth/login`) — appropriate for invite-only beta.
