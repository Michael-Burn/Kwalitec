# RR-001 — Deployment Verification

**Programme:** RR-001 — Release Readiness Gate for PB-001  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  
**Service:** Render web service `kwalitec` (`render.yaml`)  
**Verdict:** **FAIL** — current LIVE is healthy but is **not** the intended PB-001 release tip

---

## 1. Fingerprints

| Surface | Value |
|---------|-------|
| LIVE `/health.commit` | `613722cffa16e6badbdb3a1161e4feaa35fd02db` |
| `origin/main` | `613722cffa16e6badbdb3a1161e4feaa35fd02db` |
| Local `HEAD` | `f066bcf989d51e658b92d22d172d955d1e1d3ece` |
| LIVE matches `origin/main` | **Yes** |
| LIVE matches local `HEAD` | **No** |
| LIVE matches intended educational release | **No** (inventory not in Git; HEAD not deployed) |

### Local HEAD subject

`EF-001: Freeze Educational Framework Version 1 under operational stewardship`

### LIVE tip subject (via `git log`)

`fix(scripts): make g1 student walkthrough importable on Render jobs`

---

## 2. Health probes (executed 2026-08-01)

### `/health`

| Field | Value |
|-------|-------|
| HTTP | 200 |
| `status` | `ok` |
| `environment` | `production` |
| `version` | `2.0.0-beta.1` |
| `database` | `connected` |
| `build_number` | `local` (fingerprint weak — commit still present) |

### `/health/live`

| Field | Value |
|-------|-------|
| HTTP | 200 |
| `status` | `ok` |
| `commit` | `613722c…` |

### `/health/ready`

| Field | Value |
|-------|-------|
| HTTP | 200 |
| `ready` | `true` |
| `status` | `ok` |
| Migrations | `current` = `head` = `202607310002`, component `status` = `ok` |
| Database latency | ~2 ms (sample) |
| Instance storage | `ok` (`/opt/render/project/src/instance`) |

**Startup health (current deploy):** PASS  
**Migrations (current deploy):** PASS  

---

## 3. Deploy action this gate

| Step | Result |
|------|--------|
| Precondition: clean tree + intended tip committed | **FAIL** |
| Push intended tip to `origin/main` | **NOT DONE** |
| Render deploy of intended tip | **NOT DONE** |
| Reason | Working tree dirty (125 paths); educational campaigns untracked; no `RENDER_API_KEY` / deploy hook in operator `.env`; Founder Deployment Guide requires manual dashboard deploy |

**Deploy performed in RR-001:** No  

Per `knowledge/archive/releases/v2_0_0_beta_1/release/FOUNDER_DEPLOYMENT_GUIDE.md`, production deploys are **manual** on Render after push. This gate could not lawfully start that sequence.

---

## 4. Unauthenticated route matrix (LIVE)

| Path | HTTP | Observation |
|------|------|-------------|
| `/` | 200 | Public landing reachable |
| `/auth/login` | 200 | Login form present (`password` field) |
| `/auth/experience` | 200* | Unauthenticated → login surface (client follows redirect) |
| `/student/` | 200* | Unauthenticated → login surface |
| `/founder/` | 308 | Redirects to `/console/` |
| `/admin/` | 404 | No public admin root at this path |

\* Protected routes resolve to Sign-in when unauthenticated.

---

## 5. Educational inventory verification

### 5.1 Ops registers (intended publication posture)

| Volume | Status | Student-reachable? | Source |
|--------|--------|--------------------|--------|
| **CS1-001** (Campaign Alpha) | `publication_ready` | **No** | `PR001_VOLUME_REGISTER.md` |
| **CS1-002** (Campaign Beta) | `publication_ready` | **No** | `CS1002_EDUCATIONAL_VOLUME.md` |

DSH on ordinary released path: **0** (`FV002_FINAL_RECOMMENDATION.md`, `DSH001_*`).

### 5.2 Local disk inventory (not in Git)

| Campaign | Version | Status field | Packages |
|----------|---------|--------------|----------|
| `CS1-EP001-CAMPAIGN-ALPHA` | `ep001-1.0.0` | `gate_cg_pass` | 4 (1.1, 1.2 summaries, 1.2 association, revision) |
| `CS1-CS1002-CAMPAIGN-BETA` | `cs1002-1.0.0` | `gate_cg_pass` | 4 (PCA, discrete, continuous, revision) |

Also on disk: `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` (EA-006 grandfather).

| Git tracking | Count |
|--------------|-------|
| `git ls-files app/curriculum/data/educational_campaigns` | **0** |
| `git ls-files app/application/educational_packages` | **0** |

**Therefore LIVE tip `613722c` cannot contain Campaign Alpha/Beta JSON or the educational_packages module.**

### 5.3 EF version

| Locus | EF posture |
|-------|------------|
| Local docs / HEAD commit `f066bcf` | EF-001 **FROZEN** Version 1 Educational Law |
| LIVE `613722c` | Pre-dates pushed EF-001 freeze commit |

### 5.4 Active mission observed on LIVE (smoke)

Authenticated student home linked an open sitting:

- `/session/lsr-f40a7a183c80/overview` → activity  
- Title: **Today: 4.2 Understand and use generalised linear models**

This is consistent with the pre-Alpha LIVE pathway / EA-006 4.2 locus audited under EV-001 — **not** with student-released CS1-001/CS1-002 Pilot Arc volumes.

---

## 6. Migration impact

None introduced by RR-001. LIVE Alembic head remains `202607310002`.

---

## 7. Deployment verification conclusion

| Question | Answer |
|----------|--------|
| Is LIVE up? | **Yes** |
| Is LIVE fingerprintable? | **Yes** (`613722c`) |
| Is LIVE the intended PB-001 release? | **No** |
| May PB-001 treat LIVE as canonical? | **No** until intended tip is committed, pushed, deployed, and re-verified |

See `RR001_RELEASE_DECISION.md`.
