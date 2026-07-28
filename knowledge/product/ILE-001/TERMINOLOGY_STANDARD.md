# ILE-001A — Terminology Standard

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Active for Adaptive Assessment product resources  
**Effective:** 2026-07-28  
**Enforcement:** `app/application/adaptive_assessment/terminology.py`

---

## Purpose

Prevent exam / judgement language from entering Adaptive Assessment student-facing product resources. Learners should feel guided, never tested or ranked.

---

## Forbidden student-facing terms

| Forbidden | Why |
|---|---|
| Exam | Invokes high-stakes chrome; use learning/readiness check framing |
| Test | Same anxiety register as exam |
| Pass | Binary identity outcome |
| Fail | Shame / identity language |
| Weak | Deficit identity; prefer thin evidence / needs reinforcement |
| Strong student | Identity comparison |
| Poor performance | Judgemental performance framing |
| Low intelligence | Never — no identity language |

Enforcement is case-insensitive with word-boundary matching on Adaptive Assessment copy and session metadata.

---

## Approved replacements (ILE-001)

| Instead of | Prefer |
|---|---|
| Exam / test | Quick Check, Deep Check, learning check, today’s check |
| Pass / fail | Complete, continue, incomplete evidence, needs reinforcement |
| Weak topic / weak student | Needs reinforcement, thin evidence, uncertain understanding |
| Strong student | Solid evidence, well-supported understanding |
| Poor performance | Thin evidence, needs more practice |
| Mock exam / pop quiz | (Do not use on this surface) |

Session type names from `SESSION_TYPES.md` are canonical: Quick Check, Deep Check, Recovery Check, Confidence Check, Revision Check, Readiness Check.

---

## Scope of enforcement

| In scope | Out of scope |
|---|---|
| Adaptive Assessment copy registry defaults | Founder / engineering docs |
| Session registry student-facing fields | Syllabus calendar “exam date” product language outside AA |
| Presentation contracts built from those registries | Pre-existing platform “Exam Readiness” nav label (PX-002A) |

Validation fails CI when forbidden terms appear in registered Adaptive Assessment product resources (`validate_registered_adaptive_assessment_resources`).

---

## Relationship to other standards

- UX tone: `USER_EXPERIENCE_PHILOSOPHY.md`  
- Platform nouns: `knowledge/product/px002a/TERMINOLOGY_STANDARD.md`  
- Internal jargon ban (Twin, Mission Engine, …): `app/domain/student_experience/recommendation_explanation.py`  

This standard is **additional** and specific to Adaptive Assessment anxiety-safe framing.

---

**End of TERMINOLOGY_STANDARD**
