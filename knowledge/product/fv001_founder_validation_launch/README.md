# FV-001 — Founder Validation & Dogfooding

**Programme:** FV-001 — Founder Validation  
**Date opened:** 2026-07-28  
**Status:** **Active** — validation window open (instrumentation authorised)  
**Type:** Exclusive daily OS dogfood under CQ-007 **🟡 GO WITH CONSTRAINTS**  
**Engineering CRI:** **53%** provisional (unchanged unless Critical/Major fix)  
**Founder Validated CRI:** **0%** — **Open** (accumulating from genuine sessions only)

---

## Mission

Operate Kwalitec as the **primary study platform** for real examination preparation. Every significant interaction should pass through the Educational Intelligence Platform. Record defects, usability issues, educational inconsistencies, and operational risks **before** external pilot users.

This programme does **not** build new Educational Intelligence architecture.

---

## Scope — Version 1 student journey

Registration · Study Plan · SCI creation · Curriculum binding · Dashboard · Daily Mission · Study Session · Learning Evidence · Twin refresh · Educational Decisions · Experience Models · Revision Planner · Coach · Progress tracking

Catalogue (code): `app/application/founder_validation/workflows.py`  
Operator dump: `flask fv-metrics`

---

## Documents

| Document | Role |
|---|---|
| [`CRI_INTAKE.md`](CRI_INTAKE.md) | Pre-task CRI intake |
| [`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md) | Rules, severity, engineering gate |
| [`FOUNDER_VALIDATION_LOG.md`](FOUNDER_VALIDATION_LOG.md) | **Issue log** (every defect encountered) |
| [`DAILY_VALIDATION_JOURNAL.md`](DAILY_VALIDATION_JOURNAL.md) | **Per-session journal** |
| [`PRODUCT_METRICS.md`](PRODUCT_METRICS.md) | Baseline product metrics board |
| [`EXPLAINABILITY_AUDIT.md`](EXPLAINABILITY_AUDIT.md) | Recommendation explainability gaps |
| [`UX_DEFECT_REGISTER.md`](UX_DEFECT_REGISTER.md) | Functional / Educational / UX / Performance / Reliability |
| [`REAL_WORLD_BLOCKER_REGISTER.md`](REAL_WORLD_BLOCKER_REGISTER.md) | Critical/Major promotion for engineering |
| [`VALIDATED_CRI_BOARD.md`](VALIDATED_CRI_BOARD.md) | Founder Validated CRI scores |
| [`WEEKLY_VALIDATION_SUMMARY.md`](WEEKLY_VALIDATION_SUMMARY.md) | Weekly roll-up |
| [`ENGINEERING_RECOMMENDATIONS.md`](ENGINEERING_RECOMMENDATIONS.md) | Fix authorisation (Critical/Major only) |
| [`FOUNDER_ACCEPTANCE_REVIEW.md`](FOUNDER_ACCEPTANCE_REVIEW.md) | End-of-period acceptance |
| [`FV001_LAUNCH_REPORT.md`](FV001_LAUNCH_REPORT.md) | Window-open report |
| [`FV001_COMPLETION_REPORT.md`](FV001_COMPLETION_REPORT.md) | Instrumentation + workflows report |

---

## Instrumentation

| Mechanism | Purpose |
|---|---|
| `FounderValidationMetricsService` | Assembles onboarding, SCI, Experience Model, fallback, session, evidence, latency, failure metrics |
| `FounderValidationTelemetry` | Process-scoped hook outcomes + decision refresh latency |
| Enrolment / evidence hooks | Emit FV telemetry without changing EI reasoning |
| `flask fv-metrics` | Operator JSON snapshot + workflow catalogue |
| RI-002 adoption metrics | Reused for Experience Model rate and Runtime A fallback |

---

## CQ-007 constraints (must remain accepted)

1. Kwalitec = daily **OS** (mission, session, guidance, reflection, continuity). Authorised materials remain exam-grade practice depth.  
2. Dogfood on the **student sole-runtime path**, not Founder Console as the study surface.  
3. Keep **`KWALITEC_V2_SOLE_RUNTIME=1`** in production.  
4. Engineering CRI **53%** stays provisional until Founder Validated CRI earns evidence.  
5. No `cri-*` / `ecri-*` tags, public launch, or effectiveness claims from adoption alone.

Upstream: [`../cq007_founder_adoption_readiness/FOUNDER_ADOPTION_DECISION.md`](../cq007_founder_adoption_readiness/FOUNDER_ADOPTION_DECISION.md)

---

## Success criteria

- Founder completes repeated real study cycles on Kwalitec as primary OS.  
- Significant defects documented with evidence.  
- Educational Intelligence Platform demonstrates stable operation during genuine study.  
- Capability statement (at completion): *Kwalitec has been validated through sustained founder use, producing evidence-based priorities for pilot testing and commercial readiness.*

---

## Explicit non-claims

- No new EI layers / duplicated educational reasoning / Runtime Integration bypass  
- No speculative bugs or hypothetical improvements  
- No Engineering CRI inflation from instrumentation alone  
- No Version 1 production-ready / effectiveness / Stage 1 clearance  

---

**End of README**
