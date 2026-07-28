# CQ-005 Completion Report — Guidance Trust

**Programme:** CQ-005 — Commercial Quality Programme  
**Date:** 2026-07-28  
**Status:** Complete  
**Commits:** `6bf1378` (`feat(cq-005)`) · `docs(cq-005)`  

---

### Summary

CQ-005 audited every founder-facing guidance surface for **CR3 Guidance Trust** and implemented Version 1 refinements that make existing recommendations clearer, more consistent, and easier to act on: Home why continuity into Session Overview and Activity, canonical “Why” labelling, resume reconnection line, Guidance panel trust extras (alternatives / basis), and student-centred wording that drops “evidence” jargon from UI labels and cold-start / Quick Check / MI synthesis. No recommendation algorithms, Twin ranking, readiness math, AI, or new educational capability. Provisional CRI moves from **49% → 51%**; no `cri-*` tag (validation required).

---

### Files Created

- `knowledge/product/cq005_guidance_trust/README.md`
- `knowledge/product/cq005_guidance_trust/CRI_INTAKE.md`
- `knowledge/product/cq005_guidance_trust/GUIDANCE_JOURNEY_AUDIT.md`
- `knowledge/product/cq005_guidance_trust/IMPROVEMENT_PLAN.md`
- `knowledge/product/cq005_guidance_trust/CQ005_COMPLETION_REPORT.md`
- `tests/presentation/student/test_cq005_guidance_trust.py`

---

### Files Modified

- `app/infrastructure/session/defaults.py` — humble default `why_studying`; activity context accepts mission why
- `app/infrastructure/session/composition.py` — seed Overview why from Adaptive recommendation
- `app/infrastructure/session/activity_adapter.py` — thread overview why into activity context
- `app/templates/session/overview.html` — labelled “Why this Session”
- `app/templates/student/home.html` — canonical Why label; resume reconnection; Guidance trust extras; readiness basis label
- `app/templates/student/components/explanation_card.html` — “What this is based on” aria-label
- `app/domain/student_experience/recommendation_explanation.py` — soften cold-start why copy
- `app/domain/daily_mission_intelligence/compose.py` — soften MI synthesis (no “evidence” jargon)
- `app/application/adaptive_assessment/copy_registry.py` — Quick Check why copy without “evidence”
- `app/application/daily_mission_intelligence/dto.py` — evidence heading label
- `tests/application/session_experience/helpers.py` — aligned default why helper
- `knowledge/product/cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md`
- `knowledge/operations/oa001/PROGRAMME_DASHBOARD.md`
- `.cursor/rules/99-CURRENT_MILESTONE.md`

---

### Tests Executed

```bash
python3 -m pytest tests/presentation/student/test_cq005_guidance_trust.py \
  tests/presentation/student/test_cq003_daily_habit_fit.py \
  tests/presentation/student/test_cq004_session_substance.py \
  tests/presentation/student/test_recommendation_trust_contract.py \
  tests/presentation/student/test_rr001_3d_educational_consistency.py \
  tests/presentation/student/test_rr001_3a_educational_identity.py \
  tests/presentation/student/test_readiness_experience_delivery.py \
  tests/presentation/student/test_daily_mission_intelligence.py \
  tests/domain/daily_mission_intelligence/test_compose.py \
  tests/infrastructure/session/test_adapters.py \
  tests/application/session_experience/test_services.py \
  tests/presentation/session/test_product_language.py -q
```

**Outcome:** CQ-005 contracts **11 passed**; focused related suite **254 passed**.

```bash
python3 -m ruff check app/infrastructure/session/defaults.py \
  app/infrastructure/session/composition.py \
  app/infrastructure/session/activity_adapter.py \
  app/domain/student_experience/recommendation_explanation.py \
  app/domain/daily_mission_intelligence/compose.py \
  app/application/adaptive_assessment/copy_registry.py \
  app/application/daily_mission_intelligence/dto.py \
  tests/presentation/student/test_cq005_guidance_trust.py
```

**Outcome:** All checks passed.

---

### Migration Impact

None.

---

### Architecture Compliance

Layering preserved (templates / presentation / adapters / domain copy). No Twin ranking, recommendation selection, readiness calculation, or curriculum engine changes. Curriculum V1/V2 load/traversal untouched. Guidance still originates from existing MES / Adaptive opaque fields — CQ-005 only surfaces and echoes them.

---

### Technical Debt

- History still defers full “why it mattered” to Journal/Timeline (G08 deferred).
- Brand Home exit mid-session still unconfirmed (CQ-003 H07).
- Resume Continue still hops via Overview redirect.
- Strong-band CR3 still needs founder-validated observational follow-through (K2).

---

### Known Limitations

- CRI increase is **provisional** (tests + audit; not founder dogfood-validated).
- CR3 moves Emerging → stronger Emerging, not yet Strong (needs validated trust / follow-through).
- No `cri-50` / `cri-45` tag — thresholds not founder-validated.
- No new educational capabilities or ranking intelligence by design.

---

### CRI domains improved

| Domain | Before | After | Notes |
|---|---:|---:|---|
| **CR3 Guidance Trust** | 50 | **62** | Why continuity; resume reconnection; trust extras; student wording |
| **CR1 Core Study Loop** | 60 | **62** | Natural — clearer why → next action continuity |
| **CR5 Experience Cohesion** | 51 | **54** | Natural — Home ↔ Overview ↔ Activity why echo |
| **CR2 Daily Habit Fit** | 55 | **56** | Natural — resume why reconnection without re-commitment theatre |

---

### Estimated CRI delta

**+2 provisional points** (49% → **51%**).

Weighted contribution (approx.): CR3 +12 × 0.12 ≈ +1.44; CR1 +2 × 0.18 ≈ +0.36; CR5 +3 × 0.10 ≈ +0.30; CR2 +1 × 0.14 ≈ +0.14 → ≈ +2.24 on composite.

---

### Evidence supporting the increase

- `tests/presentation/student/test_cq005_guidance_trust.py` — overview why threading, resume reconnection, Guidance alternatives, readiness label, cold-start wording
- Existing trust / MES / CQ-003 / CQ-004 / session adapter suites remain green
- [`GUIDANCE_JOURNEY_AUDIT.md`](GUIDANCE_JOURNEY_AUDIT.md) · [`IMPROVEMENT_PLAN.md`](IMPROVEMENT_PLAN.md)

---

### Remaining blockers

| ID | Blocker | Caps |
|---|---|---|
| B-CR3-02 | Strong-band CR3 needs founder-validated trust / observational follow-through | CR3 Strong |
| B-CR1-01 | Residual Emerging CR1 (density / scarce-time continuity) | CR1 Strong |
| B-CR2-02 | Fresh-start hero density; preferred-minutes echo | CR2 Strong |
| B-CR4-02 | Strong-band CR4 needs dogfood / authored banks V2 | CR4 Strong |
| B-CR8-01 / B-CR8-02 | Validated KSI / external N | CR8 |
| B-CR9-01 | Commercial freezes | CR9 |

---

### Provisional or validated

**Provisional.** Do not create `cri-50` or `cri-45` until founder usage validates the guidance-trust claim.

---

### Student Impact Assessment

| Lens | Assessment |
|---|---|
| Student problem | Guidance felt fragmented — clear on Home, weak in Session, erased on resume, jargon in secondary panels |
| Student benefit | Same recommendation is understandable across Home → Overview → Activity; resume recalls why; Guidance adds useful trust extras |
| Learning benefit | Higher confidence to start and continue today’s work without second-guessing the product |
| Success metrics | Founder can state why today’s work was recommended and act without searching for buried rationale |
| Risks | Softened cold-start copy must not be mistaken for richer authored MES; continuity depends on Adaptive fields being present |
| Assumptions | Sole-runtime path; Adaptive recommendation / MES fields available when session seeds |

---

### Estimated KSI contribution

ΔKSI ≈ **0** (presentation/continuity polish of existing V1 guidance; no new educational capability or validated effectiveness claim). Secondary K2/K8 support only — not scored.

---

### Evidence collected

- CQ-005 presentation/adapter tests; existing recommendation trust, MES, readiness, MI, and session suites; programme audit/plan artefacts.

---

### Lessons learned for student value

Surfacing and echoing already-computed why fields across surfaces is higher leverage than adding more explanation chrome: when Overview and Activity repeat the Home rationale, trust survives the transition into work. Resume needs one reconnection sentence, not the full commitment stack.

---

### Explainability Review

N/A for algorithm changes — presentation continuity of existing MES fields only. No new opaque scores.

---

### Recommendation Quality Review

N/A — no ranking or selection changes.

---

### Version 1 readiness residual

No change to P-002.1 gates. CRI provisional movement does not clear G1 or educational evidence holds.

---

### CRI domains improved (Version 1 programme section)

See domain table above (CR3 primary; CR1/CR5/CR2 natural).

### Estimated CRI delta (Version 1)

**+2 provisional** (49% → 51%).

### Evidence supporting the increase (Version 1)

See Evidence sections above.

### Remaining blockers (Version 1)

See Remaining blockers table; next Board priority: residual Strong-band polish on CR1–CR5 after dogfood, or CR6 craft if justified.

### Provisional or validated (Version 1)

**Provisional.**

---

**End of CQ-005 Completion Report**
