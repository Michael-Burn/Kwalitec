# RC2_FINAL_RELEASE_REPORT.md

**Programme:** VERSION1-RC2 — Sprint C — Deployment & Release Validation  
**Role:** Release Manager  
**Date:** 2026-08-01  
**Host:** https://kwalitec.onrender.com  

---

## Recommendation

# **GO**

Authoritative Release Candidate tip is deployed, fingerprint-matched, and independently smoked including session start → activity advance → finish. Educational trust consistency remediations from Sprint B are live; Dashboard / export coverage figures agree; no Critical stop condition remains open for this RC fingerprint.

---

## Repository

| Field | Value |
|-------|-------|
| Branch | `main` |
| Authoritative commit | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` |
| Git tag | `v2.0.0-beta.1-rc2` (annotated; points at authoritative commit) |
| Application version | `2.0.0-beta.1` |
| Alembic head | `202607310002` |
| origin/main | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` (matches tip) |
| Tag integrity | **PASS** — `v2.0.0-beta.1-rc2^{commit}` == `origin/main` == LIVE `/health.commit` |

### Tip composition

1. Sprint A hygiene + educational inventory (`75c29d2` lineage)  
2. Sprint B educational metric trust (`f4666e8`)  
3. Sprint C defect fix: session answer → Continue persistence (`0d3fc72`)  

---

## Deployment

| Field | Value |
|-------|-------|
| Service | Render `kwalitec` (`srv-d97ji5t7vvec73cbs5l0`) |
| First RC deploy ID | `dep-d9mr0uu417fc73c1a8q0` |
| First RC deploy created | `2026-08-01T08:38:19.641523Z` |
| First live fingerprint | `06fa8968abe2c427328f61aa9cac01b5959a2a0f` @ `2026-08-01T08:40:37Z` |
| Fix redeploy ID | `dep-d9mr7o6417fc73c1o9h0` |
| Fix redeploy created | `2026-08-01T08:52:48.377225Z` |
| Authoritative LIVE since | `2026-08-01T08:55:02Z` (health probe) |
| `/health/ready` | `ready=true`, migrations `current=head=202607310002` |
| Build number | `local` (operator metadata residual; not a fingerprint mismatch) |

### Fingerprint verification (STOP gate)

| Check | Expected | LIVE | Result |
|-------|----------|------|--------|
| `/health.commit` | `0d3fc72137ba0ea51d1baa522c52aa526cf04438` | match | **PASS** |
| Version | `2.0.0-beta.1` | match | **PASS** |
| Tag | `v2.0.0-beta.1-rc2` | peels to same SHA | **PASS** |
| Migration head | `202607310002` | match | **PASS** |

---

## Smoke

**Persona:** Fresh Internal Alpha student provisioned via Render one-off `flask create-test-user` (public `/auth/register` correctly **404** — invite-only).  
**Evidence:** `/tmp/rc2_postfix_smoke.json` (operator workstation); HTML captures under `/tmp/rc2_pf_*.html`.

| Step | Result | Notes |
|------|--------|-------|
| Signup (public) | **N/A / PASS policy** | 404; controlled provision used |
| Login | **PASS** | Fresh `@example.com` account |
| Onboarding | **PASS** | Alpha onboarding complete |
| Calibration / Baseline | **PASS** | Baseline steps 1–6 → Runtime C enrol CS1:2026.1 |
| Today's Mission | **PASS** | Home mission hero for Study **1.1** |
| Open Session | **PASS** | `POST /student/session/start` → `lsr-*` overview |
| Complete Session | **PASS** | Answer → **Continue** → advance → reflection → Finish Review (`yes`) → complete |
| Record Practice | **PASS** | Practice embedded in session activities; finish recorded |
| Dashboard / Home | **PASS** | Non-empty; CS1 + 1.1 visible |
| Analytics | **PASS** | Redirects to History under sole-runtime (expected) |
| Study Plan | **PARTIAL** | `/study-plan/` returns Choose Exam wizard for this Runtime C path (no classic plan view) |
| Learning Objectives | **PARTIAL** | LO copy not scraped on Home/History; session briefing cites objective advancement |
| Readiness | **PASS** | Export PDF shows Coverage / EK / Readiness **0%** (honest empty evidence) |
| Export | **PASS** | `/settings/export/backup` + `/settings/export/pdf` 200 |
| Logout | **PASS** | CSRF POST → Sign in; `/student/` gated |

### Defect found & fixed during Sprint C

| ID | Symptom | Root cause | Fix |
|----|---------|------------|-----|
| SC-C1 | After Submit Answer, Continue never appeared; session completion blocked | Package-engine `submit_response` did not persist explanation onto `activity.current`; reload wiped feedback | `app/infrastructure/session/activity_adapter.py` persist + merge explained state; covered in `tests/test_lxp004a_session_substance.py`; tip `0d3fc72` |

---

## Educational Trust

| Check | Result | Evidence |
|-------|--------|----------|
| EV-001 class metric inconsistency (Dashboard vs Analytics coverage theatre) | **ABSENT** on fresh account | Home Progress **0%**; PDF Coverage **0%**; values agree |
| Dashboard matches Analytics | **PASS** | Sole-runtime Analytics → History; coverage/progress both 0 |
| Readiness explanation truthful | **PASS** | No high EK / high confidence without practice; composite inputs remain 0 with no evidence |
| Learning Objectives visible | **PARTIAL** | Mission/session path carries 1.1 purpose; Study Plan LO panel not reached on Runtime C wizard redirect |
| Topic progression correct | **PASS** | Mission locked on syllabus **1.1**; no postal-address topic observed |
| Estimated Knowledge updates correctly | **PASS** | Remains **0%** until authorised practice evidence (honest) |
| Non-syllabus quarantine | **PASS** | No Street/Road address nodes on sampled surfaces |

Sprint B local consistency law is deployed on this tip (`f4666e8` ancestors). LIVE re-check on a fresh account shows no EV-001 consistency theatre.

---

## Known Issues

| ID | Severity | Status | Notes |
|----|----------|--------|-------|
| KI-C1 Hygiene | Critical | **CLOSED** | Tip clean + inventory in Git |
| KI-C2 Fingerprint | Critical | **CLOSED** | LIVE == tag == origin/main |
| KI-C3 Educational trust | Critical | **CLOSED for consistency** | LIVE fresh-account re-check PASS; residual LO surface on Runtime C plan route |
| KI-C4 Session smoke | Critical | **CLOSED** | Full start→finish after SC-C1 fix |
| KI-H1 / H4 Volume release | High | **OPEN** | CS1-001/002 still `publication_ready` (not student `released`) — out of RC fingerprint gate if Validation-mode scope |
| Session chrome title | Medium | **OPEN** | Activity chrome may show “Today's topic” while overview/mission show 1.1 — presentation residual, not metric theatre |
| Runtime C `/study-plan/` | Medium | **OPEN** | Redirects to wizard; classic plan LO list not exercised |
| Build number `local` | Low | **OPEN** | Operator metadata only |
| Architecture Guardian 40/100 | Medium | **OPEN** | Pre-existing; not introduced by RC2 |

Canonical register remains `KNOWN_ISSUES_RC2.md` (update statuses to match this report).

---

## Recommendation detail

| Question | Answer |
|----------|--------|
| Is the authoritative RC tip on LIVE? | **Yes** |
| Does fingerprint match tag + migrations? | **Yes** |
| Did independent smoke complete session? | **Yes** |
| Are Critical educational inconsistencies absent on LIVE fresh account? | **Yes** |
| Unconditional PB-001 / public cohort? | **Not claimed** — volume `released` + activation still open |
| VERSION1-RC2 Release Candidate GO? | **GO** |

**Decision:** **GO** for VERSION1-RC2 Release Candidate at commit `0d3fc72137ba0ea51d1baa522c52aa526cf04438` / tag `v2.0.0-beta.1-rc2`.

---

## Stop

Sprint C complete. No further feature work from this report.
