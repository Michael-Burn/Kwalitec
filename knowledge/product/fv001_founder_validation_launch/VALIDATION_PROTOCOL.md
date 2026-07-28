# FV-001 — Validation Protocol

**Programme:** FV-001 — Founder Validation & Dogfooding  
**Date:** 2026-07-28  
**Status:** Normative for the open validation window

---

## 1. Purpose

Validate the completed Educational Intelligence Platform through sustained real-world founder usage. Convert provisional Engineering CRI (53%) into **Founder Validated CRI** evidence. Identify product defects, usability issues, educational inconsistencies, and operational risks before external pilot users.

---

## 2. Operating rules

| Rule | Requirement |
|---|---|
| Primary OS | Mission selection, session structure, guidance, reflection, and continuity run through Kwalitec |
| EI path | Significant interactions prefer Educational Intelligence via Runtime Integration |
| Content depth | Exam-grade practice may use authorised materials — do not pretend scaffolded activities are item banks |
| Runtime | Student sole-runtime path only; not Founder Console as study surface |
| Production | Maintain `KWALITEC_V2_SOLE_RUNTIME=1` |
| Evidence | Record only what happened in a real study session |
| Speculation | Forbidden — no hypothetical bugs, imagined improvements, or staged scenarios |
| Architecture | No new EI layers; no duplicated reasoning; no Runtime Integration bypass. Architectural change only when a validated defect demonstrates need |

---

## 3. Artefact cadence

| Artefact | When |
|---|---|
| [`DAILY_VALIDATION_JOURNAL.md`](DAILY_VALIDATION_JOURNAL.md) | Every study session |
| [`FOUNDER_VALIDATION_LOG.md`](FOUNDER_VALIDATION_LOG.md) | Every issue encountered |
| [`EXPLAINABILITY_AUDIT.md`](EXPLAINABILITY_AUDIT.md) | When a recommendation fails any of the five questions |
| [`UX_DEFECT_REGISTER.md`](UX_DEFECT_REGISTER.md) | When an issue is categorised for prioritisation |
| [`PRODUCT_METRICS.md`](PRODUCT_METRICS.md) | After meaningful study days (`flask fv-metrics`) |
| [`WEEKLY_VALIDATION_SUMMARY.md`](WEEKLY_VALIDATION_SUMMARY.md) | Weekly |
| [`FOUNDER_ACCEPTANCE_REVIEW.md`](FOUNDER_ACCEPTANCE_REVIEW.md) | End of validation period only |

---

## 4. Severity (daily-use test)

> Would this realistically stop the founder from using Kwalitec every day?

| Class | Meaning | Engineering |
|---|---|---|
| **Critical** | Breaks the daily loop or destroys trust | **Authorised** — fix before continuing exclusive OS claims |
| **Major** | Repeatedly derails daily use under scarce time | **Authorised** — fix or explicit Board accept |
| **Minor** | Friction / polish | Log only; no engineering by default |
| **None** | No issue | — |
| **Constraint** | Known accepted V1 limitation (C-01…C-04) | Do not reclassify as bugs |

---

## 5. Founder Validated CRI update rule

1. Append journal entry after each session.  
2. File issues with full fields; promote Critical/Major to blocker + engineering docs.  
3. Weekly: complete weekly summary; refresh metrics snapshot.  
4. Update [`VALIDATED_CRI_BOARD.md`](VALIDATED_CRI_BOARD.md) only when session evidence supports a domain re-score.  
5. Sync snapshot fields on [`COMMERCIAL_READINESS_BOARD.md`](../cq001_commercial_readiness/COMMERCIAL_READINESS_BOARD.md).  
6. Do **not** create `cri-*` tags until validated thresholds are met and Board accepts.

---

## 6. Engineering gate

Engineering work is **only** authorised when the blocker register shows **Critical** or **Major** items that affect daily adoption, with cited journal and issue IDs — **except** FV-001 instrumentation itself (observational metrics / workflows), which is programme scope.

Minor residuals from CQ-007 (B-01…B-07) stay deferred unless real sessions promote them.

---

**End of Validation Protocol**
