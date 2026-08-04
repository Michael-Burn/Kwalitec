# P-002.1 — Performance Report

**Programme:** P-002.1  
**Date:** 2026-08-04  
**Gate:** G7  
**Verdict:** **HOLD**

---

## 1. Scope

Validate student-critical performance under P-002.1 rules:

- LIVE Core Web Vitals  
- Loading behaviour  
- Responsiveness / perceived performance  
- CI soft budgets  

**Non-claims:** No WCAG timing claims; no high-traffic marketing; no load-test PASS.

---

## 2. CI soft budgets (G7.1) — PASS

| Suite | Result | Evidence |
|-------|--------|----------|
| `tests/ga/test_performance_benchmarks.py` | **13 passed** | `knowledge/evidence/releases/P002_1/regression/pytest_quality_curriculum_ga.txt` |
| Baseline | Soft budgets per `docs/ga/PERFORMANCE_BASELINE.md` | Dashboard/Journey 2500ms · health live 500ms · ready 1500ms |

---

## 3. Loading behaviour / perceived performance — PASS (craft)

| Signal | Result | Evidence |
|--------|--------|----------|
| Home / Mission / Plan skeletons | Present | PX-006 contracts; re-verified in PX premium suite (**72 passed**) |
| Optimistic nav / reduced motion | Present | PX-004 / PX-006 |
| Asset bytes vs PX-007 | Unchanged | See §5 |

---

## 4. LIVE Core Web Vitals — NOT MEASURED → HOLD residual

| Item | Status |
|------|--------|
| LCP / INP / CLS field measure on `https://kwalitec.onrender.com` | **Not collected this programme** |
| Residual ID | **P0021-R5** (carry **PX7-R5 / PX6-R2**) |
| Formal HOLD | `docs/production/G7_PERFORMANCE_HOLD.md` remains in force |

Operator concurrency sample and production load test remain **NOT STARTED** for high-traffic claim class.

---

## 5. Local asset baseline

| Asset | Bytes |
|-------|------:|
| `app/static/css/tokens.css` | 12,016 |
| `app/static/css/student/student.css` | 46,466 |
| `app/static/js/student.js` | 5,814 |

Source: `knowledge/evidence/releases/P002_1/performance/asset_bytes.txt` — matches PX-007 baseline (no bloat).

---

## 6. LIVE health timing sample (not CWV)

Host: `https://kwalitec.onrender.com` · tip expected `272a095…`  
File: `knowledge/evidence/releases/P002_1/performance/live_health_timings.txt`

| Probe | HTTP | time_total (s) |
|-------|------|----------------|
| live_1 | 200 | 0.467 |
| ready_1 | 200 | 0.482 |
| live_2 | 200 | 0.462 |
| ready_2 | 200 | 0.447 |
| live_3 | 200 | 1.131 |
| ready_3 | 200 | 0.460 |

**Interpretation:** Ready consistently within soft ready budget. Live sample shows cold-start variance (live_3 &gt; 0.5s soft live budget) — **insufficient** to lift G7 HOLD; reinforces need for proper operator sample + CWV field measure.

---

## 7. Gate disposition

| Criterion | Disposition |
|-----------|-------------|
| G7.1 | **PASS** |
| G7.2 | **HOLD** |
| G7.3 | No unexplained P1 latency regression vs certified craft baseline |

**Overall G7:** **HOLD** — invite-only / low-concurrency claims only; no high-traffic marketing.

Signed: P-002.1 Performance Validation · 2026-08-04
