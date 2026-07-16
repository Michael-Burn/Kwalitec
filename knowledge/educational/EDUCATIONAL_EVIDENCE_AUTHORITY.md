# Educational Evidence Authority

**Capability ID:** EIP-002  
**Programme:** Educational Integrity Programme  
**Title:** Educational Evidence Authority  
**Classification:** Operational Educational Reference  
**Status:** IMPLEMENTED — pending Architecture Review  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This document defines **what** may lawfully enter Educational Evidence and therefore
what may update Twin-owned educational estimates in the live product.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001)
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002)
3. `EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` (EGI-003)
4. `EDUCATIONAL_EVIDENCE_MODEL.md` (EIP-002-DESIGN)
5. `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` (EIP-001)

**Rule:** Observing student behaviour does not automatically produce Educational Evidence.  
**Rule:** Only V1.0 authorised observations may enter the Educational Evidence layer for Twin updates.  
**Rule:** Correct silence is preferred to artificial educational certainty.

---

## 1. The Educational Chain

```
Educational Activity
         ↓
Educational Observation
         ↓
Authorised Educational Evidence   ← EIP-002 gate
         ↓
Educational Inference
         ↓
Educational Guidance
```

No educational inference about understanding may bypass this chain.
No Twin-owned estimate may be written from Activity or Observation alone.

| Concept | Meaning | May write Estimated Knowledge / Mastery? |
|---------|---------|------------------------------------------|
| **Educational Activity** | Something the student or system did (start mission, mark coverage, accept advice, spend time). | No |
| **Educational Observation** | Durable historical record of activity or soft signal (attempt row, confidence report, duration, reflection). | No by itself |
| **Educational Evidence** | Observation authorised by V1.0 catalogue for understanding claims. | Necessary input only |
| **Educational Inference** | Interpretation of authorised Evidence into provisional beliefs. | Writes estimates under Twin / estimate Authority |
| **Educational Guidance** | Advice built from estimates and coverage — never itself evidence. | No |

---

## 2. Authorised Educational Evidence (Version 1.0)

Only the following observations may enter the Educational Evidence layer for Twin updates:

| Source | Current product pathway | Status |
|--------|-------------------------|--------|
| **Structured Question Results** | `StudyAttempt` with measurable `questions_attempted` / `questions_correct` | Live interim pathway |
| **Quiz Results** | Reserved | Not implemented — silence |
| **Mission Assessment Results** | Reserved | Not implemented — silence |
| **Mock Examination Results** | Reserved | Not implemented — silence |
| **Official Examination Results** | Reserved | Not implemented — silence |

Where authorised pathways other than Structured Question Results do not yet exist,
the application **leaves Twin-owned educational states unchanged**.

Code gate: `app/services/educational_evidence_authority.py`  
Estimate writer: `AdaptiveLearningService.update_mastery_after_attempt` (invoked only when authorised accuracies exist).

---

## 3. Unauthorised Observations (must not update the Twin)

These may be retained as history. They are **not** Educational Evidence of understanding.

| Observation | Lawful uses | Forbidden effect |
|-------------|-------------|------------------|
| Topic marked completed | Study Progress | Estimated Knowledge / Mastery |
| Mission completed | Study Progress; opportunity to gather evidence | Estimated Knowledge / Mastery from completion alone |
| Reading completed | Study Progress when reading is the study obligation | Estimated Mastery |
| Time spent studying | Workload / analytics observation | Estimated Knowledge |
| Current Learning changes | Learning Mode pointer | Twin estimates |
| Study Plan completion | Study Progress declarations | Educational Evidence of understanding |
| Student confidence | Soft Educational Observation | Educational Evidence; Twin estimates |
| Reflection | Soft Educational Observation | Educational Evidence of understanding |
| Recommendation acceptance | Decision Journal preference | Educational Evidence |
| Recommendation dismissal | Decision Journal preference | Educational Evidence |

---

## 4. Examples

### Lawful silence (preferred)

Student completes today’s mission without recording question outcomes.

- Study Progress may advance for the covered topic.
- StudyAttempt may record that the session happened.
- Estimated Knowledge unchanged.
- Estimated Mastery unchanged.

### Lawful estimate update

Student records structured question results (e.g. 8 of 10 correct) on a study attempt.

- Observation is retained.
- Accuracy enters Educational Evidence as Structured Question Results.
- Twin estimate path may update Estimated Knowledge / Mastery scalars.
- Study Progress is not auto-written from the score.

### Unlawful (removed)

Completion alone or revision count alone used to mint a mastery baseline score.
Confidence rated “Mastered” advancing Estimated Mastery or Mastered stages.
Recommendation acceptance writing understanding Evidence.

---

## 5. Educational Rationale

Kwalitec coaches students for demanding professional examinations. Trust collapses
when coverage theatre, elapsed time, or self-report are narrated as validated
understanding.

Educational Evidence Authority exists so that:

- Activity remains activity;
- Observations remain honest history;
- Only constitutionally ranked performance outcomes may evolve Estimated Knowledge
  and Estimated Mastery;
- Thin history produces understatement, not invented certainty.

High Mastered-stage language additionally requires accumulation of authorised
observations (EL-007; Constitution Article V §5) — a single favourable score
may raise an estimate but must not alone certify Mastered-stage speech.

---

## 6. Governance Categories

| Category | How EIP-002 contributes |
|----------|-------------------------|
| **A — Constitution** | Hardens Articles III, V, VIII claim lawfulness |
| **B — Logic Registry** | Strengthens EL-004–EL-007 operational behaviour |
| **D — Evidence Integrity** | Closes activity→estimate succession without Evidence |
| **E — State Ownership** | Reinforces Twin Authority over estimate writes |

---

## 7. Cross References

| Document | Relationship |
|----------|----------------|
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Articles III, IV.5–14, V, VIII |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-004, EL-005, EL-006, EL-007 |
| `EDUCATIONAL_EVIDENCE_MODEL.md` | Full source catalogue and Quality Levels (design law) |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Owner / Authority / Permitted Writers |
| `EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | Categories A, B, D, E |
| `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | EIP-002 Capability |

---

## Document Control

| Field | Value |
|-------|-------|
| Capability | EIP-002 |
| Implementation | `educational_evidence_authority.py` + gated mastery update path |
| Next step | Architecture Review |
| Forbidden next step | EIP-003 without Architecture Review approval of EIP-002 |

**Stop.** Do not begin EIP-003 from this document alone.
