# DEP-002 — Deployment Audit

**Programme:** DEP-002  
**Evidence date:** 2026-07-27  
**Host probed:** `https://kwalitec.onrender.com`

---

## 1. Deployed commit chain

| Layer | Value | Source |
|---|---|---|
| Local `HEAD` / `origin/main` | `353f4b294a2a970208c433ed8c81619a91c66a1d` | `git rev-parse` |
| Tag `v1.0.0-rc1` | `550d0696a6e81331bbc0d0b8893da97a0ca09761` | `git rev-parse v1.0.0-rc1` |
| Commits after RC1 tag on `main` | `2f17883` merge educational-architecture-consolidation; `353f4b2` `chore(deploy): run database migrations during Render release` | `git log v1.0.0-rc1..HEAD` |
| **Render production `/health` commit** | **`353f4b294a2a970208c433ed8c81619a91c66a1d`** | Live JSON |

**Conclusion:** Render is serving the current GitHub `main` tip, not a stale RC1-only tree. Deployment is **newer** than the `v1.0.0-rc1` tag by two commits (expected if release continued after tagging).

---

## 2. Runtime identity from `/health` and `/health/details`

Observed fields (production):

| Field | Value |
|---|---|
| `status` | `ok` |
| `environment` | `production` |
| `version` | `2.0.0` |
| `commit` | `353f4b294a2a970208c433ed8c81619a91c66a1d` |
| `build_date` | `2026-07-27` |
| `build_number` | `local` |
| `database` | `connected` |
| migrations `current` / `head` | `202607260001` / `202607260001` (up to date) |
| `ready` (`/health/details`) | `true` |
| Origin server | `waitress` (`x-render-origin-server`) |

WSGI entry: `render.yaml` → `waitress-serve --port=$PORT wsgi:app` → `wsgi.py` imports `app.create_app` (Kwalitec Flask factory). The separate Education OS factory in `src/web/app.py` is **not** the production process.

---

## 3. `render.yaml` configuration (repo)

Confirmed keys on the `kwalitec` web service:

| Key | Declared value |
|---|---|
| `APP_ENV` | `production` |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `1` |
| `KWALITEC_V2_DURABLE_STORE` | `1` |
| `KWALITEC_V2_INJECT_ENGINES` | `1` |
| `KWALITEC_V2_SEED_DEMO` | `0` |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | `1` |
| `KWALITEC_V2_SOLE_RUNTIME` | `1` |
| `buildCommand` | `pip install -r requirements.txt` |
| `releaseCommand` | `flask db upgrade` |
| `startCommand` | `waitress-serve --port=$PORT wsgi:app` |

`ADMIN_EMAIL` / `ADMIN_PASSWORD` / `SECRET_KEY` / `DATABASE_URL` are host-managed (sync false / generate / fromDatabase). Dashboard-only env overrides were **not** readable from this investigation (no Render API token in the agent environment). Behavioural probes substitute for dashboard inspection.

---

## 4. Runtime proof that `KWALITEC_V2_SOLE_RUNTIME` is active

| Probe | Result | Interpretation |
|---|---|---|
| `GET /` (unauthenticated) | `302` `Location: /student/` | Sole-runtime root path (`app/__init__.py` `_register_routes`) |
| Login page meta / footer | Descriptor **Education Operating System**, `Kwalitec v2.0.0`, Internal Alpha / RC2 badge | Product identity from live templates |
| Local flag resolution with `render.yaml` matrix | `SOLE_RUNTIME=True`, dual-run label `sole-runtime-v2` | Matches intended Stage 1 posture |

If the flag were unset, `/` would redirect to `/dashboard/` (legacy). Observed production behaviour matches sole runtime **on**.

---

## 5. Stale / cached / partial deploy checks

| Risk | Finding |
|---|---|
| Stale commit | **No** — health commit equals `origin/main` |
| Cached wrong build | **Unlikely** — commit fingerprint embedded in health payload; static assets use `v=2.0.0-px001` |
| Failed release / migrations behind | **No** — `current == head == 202607260001` |
| Partial deploy (two apps) | **No** — single waitress process, one `create_app` |
| Local uncommitted drift vs prod | **Yes (docs only)** — working tree has uncommitted edits to `app/templates/auth/login.html` (removes `landing-brand-name`); production still serves committed login with brand name line. Does **not** explain dual runtime |

---

## 6. Consistency matrix

| Concern | GitHub `main` | Render production | Local clean tree (`353f4b2`) |
|---|---|---|---|
| Commit | `353f4b2` | `353f4b2` | `353f4b2` |
| Sole runtime env (declared) | `render.yaml` = `1` | Behaviourally on | Must set env locally |
| Blueprint registration | Always both stacks | Same code | Same |
| Migrations head | `202607260001` | Applied | Applied (local test DB) |

---

## 7. Gaps / operator follow-ups (non-blocking for root cause)

1. Render Dashboard env UI not inspected — confirm no manual override sets `KWALITEC_V2_SOLE_RUNTIME=0` (behaviour says no).  
2. `build_number: "local"` is cosmetic / release-info, not evidence of wrong tree.  
3. Authenticated founder walkthrough on the live host requires credentials (invite-only; no public registration) — see founder section in `ROOT_CAUSE_ANALYSIS.md`.
