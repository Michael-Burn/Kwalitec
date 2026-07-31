# Custom Domain Cutover Checklist (Render)

**Audience:** operators switching production traffic from `https://*.onrender.com` to a custom HTTPS domain  
**Scope:** configuration and verification only — no educational behaviour change  
**Companions:** [ENVIRONMENT.md](ENVIRONMENT.md), [DEPLOYMENT.md](DEPLOYMENT.md), [../ga/RELEASE_CHECKLIST.md](../ga/RELEASE_CHECKLIST.md)

---

## Pre-cutover

- [ ] Custom hostname provisioned at the DNS provider (apex and/or `www` / `app` as intended)
- [ ] Custom domain added on the Render web service; TLS certificate status **Issued**
- [ ] Decide the **canonical** origin (one preferred host; redirect others if needed at DNS/CDN)
- [ ] Database backup completed ([BACKUP_AND_RECOVERY.md](BACKUP_AND_RECOVERY.md))
- [ ] Confirm current deploy is healthy on the Render URL:
  - [ ] `curl -fsS https://<service>.onrender.com/health/live`
  - [ ] `curl -fsS https://<service>.onrender.com/health/ready`

## Render environment variables

Set (or update) on the web service:

| Variable | Value | Notes |
|---|---|---|
| `APP_ENV` | `production` | Already required |
| `APP_URL` | `https://<canonical-host>` | **No** trailing slash; drives sitemap / robots / OG |
| `PREFERRED_URL_SCHEME` | `https` | Default under `ProductionConfig`; keep explicit |
| `TRUSTED_PROXY_HOPS` | `1` | Enables `ProxyFix` for `X-Forwarded-*` |
| `SERVER_NAME` | *(unset)* | Leave unset while both hosts serve traffic |
| `SESSION_COOKIE_DOMAIN` | *(unset)* | Host-only cookies; set only for subdomain sharing |

- [ ] `APP_URL` updated to the custom domain **before** declaring cutover complete
- [ ] Redeploy / restart so workers load the new env (Render “Manual Deploy” or env-change restart)
- [ ] Confirm startup logs mention `Canonical APP_URL=https://…` and `Trusted proxy support enabled`

## DNS / TLS

- [ ] DNS records match Render’s instructions (CNAME or ALIAS/ANAME as documented by Render)
- [ ] Propagation checked (`dig` / DNS checker)
- [ ] `https://<canonical-host>` presents a valid certificate (no interstitial warning)
- [ ] Optional: configure Render or DNS to redirect non-canonical hosts → `APP_URL`

## Session / security verification

Expect **new** sessions on the custom host (cookies do not move from `*.onrender.com`):

- [ ] Login on the custom domain sets `Set-Cookie` with `Secure`, `HttpOnly`, `SameSite=Lax`
- [ ] CSRF form posts succeed after login (no 400 CSRF failures)
- [ ] Response includes `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- [ ] Other security headers present: `X-Content-Type-Options`, `X-Frame-Options`, CSP
- [ ] Authenticated HTML still `Cache-Control: no-store`
- [ ] `/static/…` responses remain `Cache-Control: public, max-age=…, immutable`

## Flask URL generation

- [ ] Relative redirects (login `next`, post-login home) stay on-site paths
- [ ] Absolute metadata uses the custom domain:
  - [ ] View source on `/auth/login` → `og:url` / `canonical` / `og:image` host = `APP_URL` host
- [ ] Hit the service via the **old** Render URL once during dual-host: app still serves; OG/canonical still prefer `APP_URL`

## SEO / discovery surfaces

```bash
export BASE_URL=https://<canonical-host>
curl -fsS "$BASE_URL/robots.txt"
curl -fsS "$BASE_URL/sitemap.xml"
curl -fsSI "$BASE_URL/static/branding/favicon.ico"
curl -fsSI "$BASE_URL/static/branding/manifest.webmanifest"
```

- [ ] `robots.txt` `Sitemap:` line uses `APP_URL`
- [ ] `sitemap.xml` `<loc>` entries use `APP_URL`
- [ ] Favicon / manifest return 200 (relative paths — host follows the request)
- [ ] Social preview asset reachable: `$BASE_URL/static/branding/social-preview.png`

## Functional smoke (same as GA, on the custom domain)

- [ ] Founder login → `/console/`
- [ ] Student login → `/student/`
- [ ] `/health/live`, `/health/ready`, `/health` green on **custom** domain
- [ ] Study-plan / session happy path once (no 5xx)

## Post-cutover

- [ ] Update operator bookmarks, invite emails, and Founder runbooks to `APP_URL`
- [ ] Evidence / smoke scripts: set `KWALITEC_BASE_URL` or `APP_URL` (no hardcoded `*.onrender.com`)
- [ ] Optionally disable or redirect the Render subdomain once DNS is exclusive
- [ ] Only after single-host traffic: consider setting `SERVER_NAME=<canonical-host>` if offline absolute URL generation is required
- [ ] Do **not** enable HSTS preload submission until the custom domain is permanent and all subdomains are HTTPS-ready

## Rollback

1. Point DNS / Render primary back to the previous hostname **or** set `APP_URL` back to `https://<service>.onrender.com` and redeploy.
2. Leave `SERVER_NAME` / `SESSION_COOKIE_DOMAIN` unset.
3. Users may need to log in again (cookie host changed).
4. Verify `/health/ready` on the restored origin.

---

## Stop conditions

Do **not** declare cutover complete if:

- TLS is not Issued for the custom hostname
- `APP_URL` still points at `*.onrender.com` while marketing/invites use the custom host
- `/health/ready` fails on the custom domain
- Secure cookie / HSTS / CSRF checks fail on the custom domain
