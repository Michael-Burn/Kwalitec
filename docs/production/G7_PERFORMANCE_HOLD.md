# G7 Performance — Evidence & HOLD (EI-001.3)

**Programme:** EI-001.3 — Release Operations & Deployment Evidence  
**Authority:** P-002.1 Gate G7 · ER-RB-02 · `docs/ga/PERFORMANCE_BASELINE.md`  
**Date:** 2026-07-28  
**Disposition:** **HOLD** for G7.2 / production load (high-traffic claims restricted)  
**G7.1 status:** Soft CI budgets green (re-verified in EI-001.3 test report)

---

## 1. Clearance path used

ER-RB-02 clearance: *G7.2 sample filed **or** approved HOLD with high-traffic claim restriction.*

This artefact records:

1. **G7.1** — CI soft-budget verification procedure and result pointer.  
2. **G7.2** — Formal **HOLD** (no staging/production operator concurrency sample filed in this WP; load test remains NOT STARTED).  
3. **G7.3** — No unexplained P1 latency regression debt entry required for this claim window (invite-only; no high-traffic baseline yet).

---

## 2. G7.1 — CI soft budgets

**Command:**

```bash
.venv/bin/python -m pytest tests/ga/test_performance_benchmarks.py -v --tb=line -q
```

**Baseline:** `docs/ga/PERFORMANCE_BASELINE.md`  
**Result:** Recorded in `knowledge/release/EI-001/EI001_3_TEST_REPORT.md` (must be green for this HOLD to remain valid alongside CI).

---

## 3. G7.2 — Operator sample procedure (for when HOLD is lifted)

Use staging or production only with operator approval:

```bash
export BASE_URL="https://<staging-or-prod-host>"

# Health (always)
curl -fsS -o /dev/null -w 'live %{http_code} %{time_total}\n' "$BASE_URL/health/live"
curl -fsS -o /dev/null -w 'ready %{http_code} %{time_total}\n' "$BASE_URL/health/ready"

# Authenticated surfaces (session cookie / operator harness as applicable)
# Dashboard / Journey — record time_total and compare to PERFORMANCE_BASELINE soft budgets
curl -fsS -o /dev/null -w 'dashboard %{http_code} %{time_total}\n' "$BASE_URL/student/"
curl -fsS -o /dev/null -w 'journey %{http_code} %{time_total}\n' "$BASE_URL/student/journey"
```

Optional SQL calibration: `PROFILE_SQL=1`, `SLOW_REQUEST_THRESHOLD_MS=300` per Performance Baseline.

File results under a dated evidence folder or attach to the Version 1 Evidence Package (`G7_performance/`).

**Production load test** under cohort concurrency remains a separate Release operator activity before high-traffic marketing.

---

## 4. HOLD terms (P-002.1 §4 G7–G9)

| Term | Statement |
|------|-----------|
| Residual | No staging/production operator sample under concurrency; production load test NOT STARTED |
| Debt entry | `ER-TD-H05` (retained under HOLD until sample + load evidence filed) |
| Claim restriction | **No high-traffic marketing**, **no public launch concurrency claims**, **no Stage 1 cohort expansion justified by performance evidence** |
| Allowed claim class | Invite-only Internal Alpha / private dogfood under existing low concurrency |
| Sign-off capacities | Engineering Owner + Release / Operations Owner (Product acknowledges claim restriction) |

**HOLD is not a waiver of educational honesty or security Criticals.**

---

## 5. Gate score (engineering)

| Criterion | Status |
|-----------|--------|
| G7.1 CI soft budgets | **PASS** when pytest green on candidate |
| G7.2 Operator sample | **HOLD** — this document |
| G7.3 No unexplained P1 regression | **PASS** for invite-only claim class (no prior certified production SLO to regress against) |

**Overall G7:** **HOLD** (claim-restricted).

---

**End of G7_PERFORMANCE_HOLD**
