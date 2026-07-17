# V1SP-001B — High Priority Operational Fixes

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001B  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Nature:** Hardening only — no new product capabilities  
**Closes:** RC2 Operational Readiness High findings H-1 through H-9  
**Commit:** `77edeb8` — `fix: resolve RC2 High operational readiness findings (V1SP-001B)`  

---

## Summary

V1SP-001B resolves every High-severity issue from the RC2 Operational Readiness Review. Open-redirect and production cookie/SECRET_KEY gates are hardened; Founder sidebar active-state and Feedback inbox honesty are fixed; static asset caching and brand raster weight are improved; top-level Version 1 documentation is refreshed to the RC2 fingerprint (`1.0.0` / Build RC2).

No educational cores, Twin behaviour, or new Founder product features were introduced.

---

## Security

### H-1 — Open redirect protection

`_safe_next_url` in `app/auth/routes.py` now:

- requires a path-absolute destination (single leading `/`);
- rejects `//`, `///`, backslashes, and control characters;
- fully percent-decodes before validation (blocks `/%2f%2f…` bypasses);
- returns a normalised local path (never the raw attacker string).

### H-2 — Production cookie security

`ProductionConfig` sets:

| Setting | Value |
|---|---|
| `SESSION_COOKIE_SECURE` | `True` |
| `SESSION_COOKIE_HTTPONLY` | `True` |
| `SESSION_COOKIE_SAMESITE` | `Lax` |
| `REMEMBER_COOKIE_SECURE` | `True` |
| `REMEMBER_COOKIE_HTTPONLY` | `True` |
| `REMEMBER_COOKIE_SAMESITE` | `Lax` |
| `SEND_FILE_MAX_AGE_DEFAULT` | `31536000` (1 year) |

Requires HTTPS termination (Render). Development / testing configs unchanged.

### H-3 — SECRET_KEY gate aligned to selected config

`_validate_env_vars(config_object)` rejects insecure placeholder secrets whenever `ProductionConfig` is active (whether selected via `APP_ENV` or `FLASK_ENV`), not only when `APP_ENV=production`.

---

## Founder Experience

### H-4 — Sidebar active state

Student Dashboard highlighting uses `request.endpoint.startswith('dashboard.')`, so Founder Command Centre routes no longer falsely activate Dashboard.

Command Centre secondary nav continues to highlight Overview, Operational Health, Feedback, Vision Journal, Releases, and Settings via `active_section_id`.

### H-5 — Feedback inbox declutter

Feedback is triage-first per POP-002:

- removed Internal Alpha summary, “since yesterday”, Product Health, and Research Insights blocks from the Feedback page;
- retained filters, inbox list, detail pane, and workflow actions;
- analysis/create-finding paths point to Research / Findings sections;
- Findings page hosts the create-finding form.

### H-6 — Inbox capacity

Silent 50-item truncation replaced with pagination:

- `count_inbox` + `list_inbox(..., offset=)`;
- `DashboardContext` exposes `inbox_page`, `inbox_per_page`, `inbox_total`, and page helpers;
- UI shows “Showing X–Y of N” and Previous/Next controls when more than one page exists.

---

## Performance

### H-8 — Static asset caching

- HTML responses keep `Cache-Control: no-store`.
- Static endpoints (`static` / `*.static` / `/static/…`) receive `public, max-age=…, immutable`.
- `url_defaults` appends `v={APP_VERSION}-{INTERNAL_ALPHA_BUILD_LABEL}` to static `url_for` calls so deployments bust caches without renaming files.

### H-9 — Brand asset optimisation

Raster pack under `app/static/branding/` reduced from ~5.3 MB to ~2.1 MB:

| Asset | Change |
|---|---|
| `logo-primary.png` / `logo-white.png` | max dimension 800 |
| `logo-icon.png` | max dimension 256 |
| `social-preview.png` | cropped to **1200×630** OG size |

SVG remains the runtime canonical logo format.

---

## Documentation

Updated for Version1-RC2 / V1SP-001B:

- `README.md` — version fingerprint table; release references
- `PROJECT_CONTEXT.md` — live blueprints, folder map, status
- `ARCHITECTURE.md` — blueprint map; security summary (cookies, redirects, static cache)
- `app/static/branding/README.md` — optimisation note + OG dimensions
- `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md` — this report

---

## Tests

### Automated

```bash
python -m pytest tests/test_v1sp001b_operational_fixes.py -q
```

Coverage includes redirect bypasses, production cookie flags, SECRET_KEY gate, sidebar prefix match, Feedback declutter + pagination totals, static cache headers / fingerprint, and brand size / OG dimensions.

Related suites re-run: `test_auth`, `test_config`, `test_iahf003_founder_command_centre`, `test_iahf004a_brand_infrastructure`, `test_rip003_founder_command_centre`.

### Manual verification checklist

| Check | Expected |
|---|---|
| Login `?next=///evil.com` | Falls back to dashboard (no external redirect) |
| Production cookies over HTTPS | `Secure; HttpOnly; SameSite=Lax` |
| Founder Overview | Dashboard sidebar inactive; Overview CC nav active |
| Feedback with >50 submissions | “Showing … of N” + pagination |
| `/static/css/app.css` | `Cache-Control` public/immutable; URL has `v=` |
| Brand SVGs in chrome | Unchanged visual quality |

### Security verification

- Parametrised open-redirect rejections in `tests/test_v1sp001b_operational_fixes.py`
- Production config assertions for session + remember cookies
- ProductionConfig + default SECRET_KEY raises `RuntimeError`

---

## Remaining Risks

Intentional deferrals (Medium/Low from RC2 — out of V1SP-001B scope):

- Login rate limiting / lockout (M-1)
- Founder post-login landing on Command Centre (M-7)
- CSP nonce / remove `'unsafe-inline'` follow-up (post C-1)
- Archive recovery UI, settings honesty, a11y skip link (M/L items)
- Further PNG palette quantisation (optional; current budgets met via resize)

---

## Files Created

- `tests/test_v1sp001b_operational_fixes.py`
- `knowledge/releases/V1SP-001B_OPERATIONAL_FIXES.md`

## Files Modified

- `app/auth/routes.py`
- `app/config.py`
- `app/__init__.py`
- `app/templates/partials/sidebar.html`
- `app/services/founder_research_service.py`
- `app/founder/dashboard/feedback_handlers.py`
- `app/founder/dashboard/routes.py`
- `app/founder/dashboard/templates/founder_dashboard/feedback.html`
- `app/founder/dashboard/templates/founder_dashboard/findings.html`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/static/branding/*.png` (optimised rasters)
- `app/static/branding/README.md`
- `README.md`
- `PROJECT_CONTEXT.md`
- `ARCHITECTURE.md`

## Migration Impact

None.

## Architecture Compliance

Layering preserved (routes → services → models). Curriculum V1/V2 untouched. Founder Feedback changes align with POP-002 triage-before-analysis and DP-001/DP-006/DP-008.

## Technical Debt

- Feedback create-finding POST still lands on the Feedback route handler (form lives on Findings) — acceptable for Alpha; optional later: dedicated Findings POST.
- Static fingerprint is version query string, not content hash — sufficient for RC2 deploy cadence.

## Known Limitations

- Does not close Medium/Low RC2 items.
- Does not implement Founder post-login default home.
- Physical-device visual QA of brand rasters after resize remains a release recommendation.

---

*End of V1SP-001B Operational Fixes report.*
