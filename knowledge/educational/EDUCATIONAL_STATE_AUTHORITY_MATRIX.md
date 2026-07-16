# Educational State Authority Matrix

**Capability ID:** EIP-001  
**Programme:** Educational Integrity Programme  
**Title:** Educational State Ownership & Authority  
**Classification:** Operational Educational Reference  
**Status:** APPROVED — governing for implementation  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This Matrix is the operational ownership reference for educational state mutation in Kwalitec.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001)
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002)
3. `EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` (EGI-003)
4. `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` (EIP-000)

**Rule:** Every educational state has exactly one Owner and exactly one Authority.  
**Rule:** No component may modify an educational state unless listed as a Permitted Writer under that state’s Authority.  
**Rule:** Correctness prefers leaving a Twin-owned estimate unchanged over inventing an unauthorised write.

---

## Concepts

| Term | Meaning |
|------|---------|
| **Owner** | Who is educationally responsible for the meaning of the state |
| **Authority** | Who is permitted to mutate the state |
| **Permitted Writers** | Concrete writers that may change persistence under Authority |
| **Forbidden Writers** | Writers that must never mutate the state |
| **Primary Readers** | Components that may consume the state without mutating it |

Owner and Authority are different. Ownership answers meaning; Authority answers mutation rights.

---

## Matrix

### 1. Study Progress

| Aspect | Value |
|--------|-------|
| **Educational State** | Study Progress (`TopicProgress.completed` / coverage lifecycle) |
| **Owner** | Learner (User) — educational history asset; Study Plan is context for declarations only |
| **Authority** | Mission Completion; Manual Topic Completion |
| **Permitted Writers** | Mission completion coverage path; Study Plan Wizard / edit manual topic completion; CurriculumService progress APIs used for those purposes |
| **Forbidden Writers** | Estimated Mastery; Educational Evidence; Confidence; Recommendation Engine; Digital Twin; Adaptive mastery formulae; Study Plan delete / archive lifecycle |
| **Primary Readers** | Learning Mode; Planning Service; Dashboard; Analytics (coverage); Readiness (as coverage input only) |
| **Related Constitution Articles** | II §1.8; III §5; IV.1; IV.2; IV.14; VIII.15–16; IX §4 |
| **Related Logic IDs** | EL-001; EL-004 (coverage side only); EL-011 |
| **Governance Categories** | A, B, E (supports D, G) |
| **Required invariants** | Completing studying never mints Estimated Mastery. Mastery ≥ threshold never sets `completed=True`. Confidence never sets coverage. Study Plan deletion must not erase Study Progress (EIP-005). |

---

### 2. Educational Evidence

| Aspect | Value |
|--------|-------|
| **Educational State** | Educational Evidence (observational history) |
| **Owner** | Educational Evidence Pipeline |
| **Authority** | Assessment Results; Mission Assessment Results; Quiz Results; Mock Examination Results |
| **Permitted Writers** | Lawful assessment / quiz / mock / scored mission-assessment recorders (when implemented under EIP-002+) |
| **Forbidden Writers** | Study Progress; Mission Completion alone; Time Spent; Confidence; Recommendation Engine; Planning Service |
| **Primary Readers** | Digital Twin; Estimated Knowledge / Mastery estimation; Readiness; Recommendations (consume, do not author) |
| **Related Constitution Articles** | III; IV.5; V |
| **Related Logic IDs** | EL-004; EL-005; EL-006; EL-007 |
| **Governance Categories** | A, B, D |
| **Required invariants** | Coverage, confidence, and elapsed time alone never create Educational Evidence of understanding. EIP-001 does not implement the Evidence pipeline — only forbids unauthorised writers. |

---

### 3. Estimated Knowledge

| Aspect | Value |
|--------|-------|
| **Educational State** | Estimated Knowledge |
| **Owner** | Digital Twin |
| **Authority** | Educational Evidence |
| **Permitted Writers** | Twin / authorised estimation paths that consume Educational Evidence only |
| **Forbidden Writers** | Completion; Study Progress; Mission Completion; Confidence; Recommendation Engine; Learning Mode mission closure |
| **Primary Readers** | Dashboard; Analytics; Recommendations; Readiness |
| **Related Constitution Articles** | III; IV.6; IV.7; V |
| **Related Logic IDs** | EL-006; EL-007 |
| **Governance Categories** | A, B, D, E |
| **Required invariants** | Absence of Educational Evidence ⇒ estimate left unchanged (no artificial write). Product `mastery_score` must not be treated as Twin Knowledge unless Evidence Authority has lawfully updated it. |

---

### 4. Estimated Mastery

| Aspect | Value |
|--------|-------|
| **Educational State** | Estimated Mastery (`TopicProgress.mastery_score` / mastery stage when evidence-backed) |
| **Owner** | Digital Twin |
| **Authority** | Educational Evidence |
| **Permitted Writers** | Twin / authorised estimation paths that consume Educational Evidence only |
| **Forbidden Writers** | Mission Completion; Completion; Confidence; Study Progress; Current Learning; Recommendation Engine |
| **Primary Readers** | Analytics; Advisory recommendations; Review scheduling consumers |
| **Related Constitution Articles** | II §1.3, §1.6; III; IV.8; V §4–5; VIII |
| **Related Logic IDs** | EL-007; EL-005 |
| **Governance Categories** | A, B, D, E |
| **Required invariants** | Mission completion must not recalculate `mastery_score`. Student confidence must not alter `mastery_score`. Mastery formulae must never write Study Progress (`completed`). |

---

### 5. Current Learning Topic

| Aspect | Value |
|--------|-------|
| **Educational State** | Current Learning Topic (plan `curriculum_topic_code` + first incomplete syllabus unit) |
| **Owner** | Study Plan |
| **Authority** | Learning Mode |
| **Permitted Writers** | Learning Mode / Planning reconciliation driven by Study Progress and syllabus order |
| **Forbidden Writers** | Recommendations; Mission Completion (except via Study Progress → Learning Mode reconciliation after lawful coverage); Educational Evidence; Confidence; Digital Twin |
| **Primary Readers** | Planning Service (Today’s Mission); Dashboard; Mission surface |
| **Related Constitution Articles** | IV.3; VI (Learning Mode); VIII |
| **Related Logic IDs** | EL-002; EL-003; EL-009; EL-011 |
| **Governance Categories** | A, B, E, G |
| **Required invariants** | Recommendations may advise a different focus but must not mutate the Current Learning Topic. |

---

### 6. Today's Mission

| Aspect | Value |
|--------|-------|
| **Educational State** | Today’s Mission (persisted Learning Mode mission for the study day) |
| **Owner** | Planning Service |
| **Authority** | Learning Mode |
| **Permitted Writers** | `PlanningService.generate_today_mission` and Mission Service task/status updates for that mission’s lifecycle |
| **Forbidden Writers** | Recommendation Engine; Digital Twin; Confidence; Educational Evidence |
| **Primary Readers** | Mission UI; Dashboard; Analytics (activity) |
| **Related Constitution Articles** | IV.4; VI; VIII |
| **Related Logic IDs** | EL-003; EL-009 |
| **Governance Categories** | A, B, E, G |
| **Required invariants** | Recommendation generation is advisory-only and must not create, replace, or retarget Today’s Mission under Learning Mode. |

---

## Write-Path Summary (Version 1.0 product)

| From ↓ / To → | Study Progress | Educational Evidence | Estimated Knowledge | Estimated Mastery | Current Learning | Today's Mission |
|---------------|----------------|----------------------|---------------------|-------------------|------------------|-----------------|
| Mission Completion | **Permitted** (coverage) | Forbidden | Forbidden | Forbidden | Indirect via Learning Mode reconcile after coverage | Lifecycle status only |
| Manual Topic Completion | **Permitted** | Forbidden | Forbidden | Forbidden | Indirect via Learning Mode | Forbidden |
| Confidence (self-report) | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Mastery formula | Forbidden | Forbidden | Only via Evidence Authority | Only via Evidence Authority | Forbidden | Forbidden |
| Recommendation Engine | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden | Forbidden |
| Digital Twin | Forbidden | Consume only | **Permitted** (Evidence-driven) | **Permitted** (Evidence-driven) | Forbidden | Forbidden |
| Learning Mode / Planning | Advances after Study Progress | Forbidden | Forbidden | Forbidden | **Permitted** | **Permitted** |

---

## EPA-002 Violations Closed by This Matrix

| Finding | Ownership fix |
|---------|---------------|
| FINDING-001 Mastery auto-writes Study Progress | Forbidden: Estimated Mastery → Study Progress |
| FINDING-002 Confidence authors Mastery | Forbidden: Confidence → Estimated Mastery |
| FINDING-003 Mission completion recalculates Mastery | Forbidden: Mission Completion → Estimated Mastery / Knowledge |
| FINDING-004 Study Progress co-writes confidence | Study Progress writes coverage only; confidence not a coverage side-effect |

Residual Evidence Integrity (density, Dual Twin stores, Rank-D soft signals) remains for **EIP-002**.

---

## Cross References

- Constitution Article IV Educational State Model
- Registry Educational State Ownership Matrix + EL-001–EL-011
- Blueprint Capability EIP-001
- Regression: `tests/test_eip001_educational_state_ownership.py`

---

## Closing

This Matrix is the implementation gate for educational mutation.

If code would write a state and the writer is Forbidden here, the code is constitutionally unlawful — even if the write appears educationally convenient.
