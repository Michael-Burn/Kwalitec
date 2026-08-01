# RR-001 — Live Smoke Report

**Programme:** RR-001 — Release Readiness Gate for PB-001  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Deploy tip smoked:** `613722cffa16e6badbdb3a1161e4feaa35fd02db`  
**Actor:** Founder dual-access account from operator `.env` (`ADMIN_EMAIL`)  
**Overall smoke verdict:** **FAIL** for PB-001 gate (core auth/nav partial pass; release criteria not met)

---

## Method

- Unauthenticated HTTP probes to public/auth surfaces.  
- Authenticated browserless smoke via Python `urllib` + cookie jar + CSRF.  
- Session **completion** deliberately not executed on LIVE (avoids mutating production study state during a NO-GO gate).  
- Public **registration** not available (product policy) — student persona exercised via Founder dual-access → Student Experience.

---

## Founder checklist

| Step | Result | Evidence |
|------|--------|----------|
| Login | **PASS** | POST `/auth/login` → `/auth/experience`; flash “Welcome back to Kwalitec.” |
| Baseline (if applicable) | **N/A** | Not required for this dual-access account in this sitting |
| Home (Console) | **PASS** | `/console/` → `Home · Kwalitec Console` (200) |
| Home (Student) | **PASS** | `/student/` → `Home · Kwalitec` (200) |
| Today's Mission | **PASS** | Home CTA → `/session/lsr-f40a7a183c80/overview` |
| Session Overview | **PASS** | Overview resolves; redirects into in-progress activity |
| Session start | **PARTIAL** | Sitting already open on topic **4.2**; cold start not re-proven |
| Session completion | **NOT RUN** | Intentionally skipped |

Additional Founder surfaces:

| Surface | Result |
|---------|--------|
| Experience selection | **PASS** — `Choose experience · Kwalitec` |
| Curriculum Health | **PASS** — `/console/curriculum-health` (200) |
| Settings / profile | **PASS** — `/settings/` → `/student/profile` (200) |
| Logout (CSRF POST) | **PASS** — `/auth/logout` → Sign in; subsequent `/student/` requires auth |

---

## Student checklist

| Step | Result | Evidence |
|------|--------|----------|
| Registration | **N/A** | Public registration disabled |
| Login | **PASS** | Same dual-access login; Student Experience selected via `/student/` |
| Study flow | **PARTIAL** | Home → open session activity for 4.2; full answer→complete loop not run |
| Mission rendering | **PARTIAL** | Mission/session chrome loads; educational substance quality not re-certified here (see EV-001) |
| Navigation | **PASS** | Home, Learning Journey, Study Plan wizard, Settings reachable |
| Logout | **PASS** | CSRF POST logout returns Sign in |

Harvested student-home links (authenticated):

- `/session/lsr-f40a7a183c80/overview`  
- `/student/learning-journey`  
- `/study-plan/`

---

## Failures / gaps counted against gate

1. Smoke was run against **`613722c`**, not an intended post-inventory release tip.  
2. Session start (cold) and session completion not proven.  
3. Student registration path not available to exercise.  
4. Probe paths `/student/begin` and `/mission/` return **404** (routing differs; not used as primary CTAs).  
5. Educational quality on this tip remains under prior **EV-001 FAIL** (not cleared by RR-001).

---

## Unauthenticated sanity

| Check | Result |
|-------|--------|
| Login page loads | PASS |
| Health live/ready | PASS |
| No 500 on sampled public routes | PASS |

---

## Smoke conclusion for RR-001

Operational reachability of Founder login, Console, Student Home, and an open session is **demonstrated** on the current LIVE tip. That is **insufficient** for PB-001 commencement: the tip is not the intended release, inventory does not match, and end-to-end session completion was not verified on a canonical deploy.

**Gate smoke status:** **FAIL**
