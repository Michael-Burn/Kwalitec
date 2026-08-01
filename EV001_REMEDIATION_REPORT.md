# EV001_REMEDIATION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint B (Educational Trust Restoration)  
**Date:** 2026-08-01  
**Scope:** KI-C3 / EV-001 educational trust blockers — metric & status consistency  
**Constraint:** No deploy · No push · No new features · EF-001 freeze respected  

---

## Summary

Sprint B remediates the **educational consistency** failures that make Dashboard, Analytics, Readiness, Topic Status, Estimated Knowledge, and Learning Objectives disagree. Remediation is code-level on the local RC tip; LIVE re-validation remains Sprint C after deploy.

---

## EV-001 trust breaks — remediation status

| ID | Observation | Classification | Sprint B action | Status |
|----|-------------|----------------|-----------------|--------|
| TB-005 | Progress / History / Revision disagree; coverage theatre | Consistency | Unified Study Progress coverage authority (`completed`, plan-scoped) across Readiness + Analytics | **Remediated (code)** |
| TB-006 | Completed topic + LOs all “Not started”; chapters Future | Consistency | Curriculum Map LO inheritance + section roll-up; LO syllabus sort | **Remediated (code)** |
| TB-003 | Postal address as syllabus topic | Curriculum fidelity | Quarantine non-syllabus titles on Curriculum Map / pathway / Baseline helper (`is_non_syllabus_title`) | **Remediated (surfaces)** |
| TB-011 | LO order machine-shuffled | Curriculum fidelity | Syllabus-code sort on map children; Study Plan LOs by `order` | **Remediated (display)** |
| TB-012 | High confidence without practice | Honesty | Coverage no longer inflated by `revision_count`; EK only from evidence-backed rows | **Partially remediates** |
| TB-001 / TB-007 / TB-008 | Placeholder pedagogy / empty reading / stuck advance | Content / session | Out of Sprint B metric scope; inventory packages on tip still require LIVE smoke | **Open for Sprint C** |
| TB-002 / TB-004 / TB-013 | Syllabus-paste missions / boilerplate explainability | Content / voice | Not redesigned (no feature work) | **Open / operational** |
| TB-009 | Timing mismatch | Ops | Not in Sprint B metric scope | **Open** |
| TB-010 | Tomorrow preview vs address node | Continuity | Address filtered from map pathway | **Partially remediates** |
| TB-014 | Empty revision at high coverage | Revision ops | Not activated in Sprint B | **Open** |

---

## Authoritative calculation (post-remediation)

| Surface | Coverage source | Knowledge source |
|---------|-----------------|------------------|
| Dashboard Study Progress | `TopicProgress.completed` / weighted plan curriculum | Separate EK card when evidence exists |
| Analytics “Syllabus coverage” | `ReadinessService.get_curriculum_coverage` → same `completed` metrics | Composite uses evidence-backed mean |
| Readiness composite (50/30/20) | Study Progress completed % (plan-scoped when active plan exists) | Mean `mastery_score` where `has_estimated_knowledge` |
| Topic roadmap badge | Completed / Learning / Next / **Practised** / stage — not plan pointer alone | EK shown with explicit practice basis |

---

## Evidence

- `tests/test_rc2_educational_trust_consistency.py`
- `EDUCATIONAL_CONSISTENCY_REPORT.md`
- `READINESS_VALIDATION_REPORT.md`
- `RC2_SPRINT_B_COMPLETION_REPORT.md`

---

## Residual for Sprint C

1. Deploy RC tip; re-run EV-001 class smoke on LIVE.  
2. Confirm educational package overlays clear TB-001 / TB-007 on LIVE.  
3. Complete session smoke (KI-C4).  
4. Re-issue RR-001 only after fingerprint match + smoke + trust re-check.

**KI-C3 local remediation:** **CLOSED for consistency objectives** · **OPEN for LIVE educational re-validation**
