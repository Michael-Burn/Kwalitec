# ILE-001 — Design Review

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Document:** `ILE001_DESIGN_REVIEW.md`  
**Status:** Design review (documentation milestone)  
**Date:** 2026-07-28  

---

## 1. Scope check

| Deliverable | Present |
|---|---|
| `ADAPTIVE_ASSESSMENT_VISION.md` | Yes |
| `STUDENT_JOURNEYS.md` | Yes |
| `EXPERIENCE_PRINCIPLES.md` | Yes |
| `ADAPTIVE_SELECTION_MODEL.md` | Yes |
| `SESSION_TYPES.md` | Yes |
| `QUESTION_SELECTION_POLICY.md` | Yes |
| `FEEDBACK_MODEL.md` | Yes |
| `CONFIDENCE_AND_UNCERTAINTY_UX.md` | Yes |
| `FAILURE_AND_RECOVERY.md` | Yes |
| `PERSONALISATION_BOUNDARIES.md` | Yes |
| `IMPLEMENTATION_ROADMAP.md` | Yes |
| `SUCCESS_MEASURES.md` | Yes |
| `ILE001_DESIGN_REVIEW.md` | Yes (this document) |

**Constraints:** Documentation only — no production code, architecture modifications, or educational reasoning modifications in this milestone.

---

## 2. Alignment with ILE-000

| Authority | Verdict | Notes |
|---|---|---|
| Product Strategy | **Pass** | Surfaces Educational Intelligence; value = trust + evidence quality |
| Product Principles | **Pass** | Evidence before inference; explain decisions; respect uncertainty; no engagement-over-learning |
| UX Philosophy | **Pass** | Calm, non-overwhelming, Mission-owned Next, uncertainty visible |
| Educational Philosophy | **Pass** | Assessment as evidence; confidence tracks evidence; Tutor explains |
| Roadmap ILE-001 intent | **Pass** | Learning instrument; Twin-visible effect; no mastery theatre |
| Success Metrics family | **Pass** | Learner outcomes & trust; anti-vanity metrics explicit |

---

## 3. Educational consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Learner experience, not algorithm fetish | **Pass** | Vision + journeys + principles lead |
| No marks / ranking culture | **Pass** | Throughout pack |
| Single check ≠ mastery | **Pass** | Vision, confidence UX, feedback |
| Anxiety-safe framing | **Pass** | Principles + session types + failure modes |
| Curriculum-first personalisation | **Pass** | Boundaries document |
| Mistakes as educational fuel | **Pass** | Feedback + recovery |

**Residual risk:** Implementation copy/visuals may reintroduce exam chrome — mitigate with perception validation (ILE-001.I) and EQ copy review.

---

## 4. Platform / authority consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Assessment produces observations | **Pass** | Vision; selection model; feedback |
| Reasoning interprets; Twin stores belief | **Pass** | No experience-layer mastery writes |
| Mission schedules / owns Next | **Pass** | Vision; journeys; feedback |
| Tutor explains, never grades | **Pass** | Vision; feedback model |
| No second educational brain | **Pass** | Selection model forbids LLM authority |
| Compatible with AP-002 design | **Pass** | Maps triggers to session types; does not replace AP-002 |
| Curriculum V1/V2 | **N/A / Pass** | Docs only; policy requires both remain supported at implementation |

**Residual risk:** Pressure to “update mastery in the UI for speed” during engineering — block via architecture tests and review checklists when code starts.

---

## 5. Completeness for small-milestone implementation

| Need | Covered by |
|---|---|
| Why build it | Vision |
| Who feels what when | Journeys + session types |
| UX decision filters | Experience principles |
| What adapts (product behaviour) | Selection model + question policy |
| Feedback lifecycle | Feedback model |
| Uncertainty speech | Confidence & uncertainty UX |
| Messy reality | Failure & recovery |
| Fairness limits | Personalisation boundaries |
| Slice plan | Implementation roadmap |
| How we’ll know it worked | Success measures |

**Verdict:** Implementation can proceed in ILE-001.A→I slices without inventing product intent ad hoc.

---

## 6. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Students still feel “tested” | High | Principles + perception validation; exam-skin ban |
| Over-assessment fatigue | High | Mission density gates; prefer study when gates fail |
| Adaptive opacity (“AI mystery”) | High | Mandatory why-framing; deterministic intent language |
| Conflict with AP-002 runtime timing | Medium | Roadmap dependency posture; thin Quick Check first |
| Confidence UX anxiety | Medium | Optional prompts; ILE-005 for broader surfaces |
| Readiness check overclaim | High | Non-guarantee language; success measure comprehension item |
| Scope creep into mock exams | Medium | Explicit non-goals |
| Personalisation unfairness | Medium | Boundaries + reproducibility rule |

---

## 7. Open questions

1. **Deferral UX on Home:** Exact control for declining a Mission-embedded check without breaking “one Next”?  
2. **Item authoring source:** Curriculum Studio vs Assessment Studio vs import packs (owned with AP-002)?  
3. **Overlap with LXP practice capture:** When does Adaptive Assessment become the preferred formative evidence path vs existing practice attempts?  
4. **Confidence scale standard:** Shared ordinal labels across ILE-001 and ILE-005?  
5. **Readiness Check weighting:** Product-visible “syllabus-weighted” explanation depth before ILE-003?  
6. **Mobile parity:** How much of ILE-001.B must wait for ILE-008 vs responsive web sufficiency?  
7. **Feature flag grain:** Per subject vs global for first Quick Check release?

---

## 8. Recommendations

1. Start engineering at **ILE-001.B (Quick Check in Mission)** after **ILE-001.A** copy/flag foundations — prove observation yield and anxiety safety before Deep/Readiness.  
2. Reuse AP-001 as sole Twin observation ingress; do not create a parallel write path.  
3. Run educational copy review before first student-visible release.  
4. Keep selection explanations at **intent level**; defer algorithmic disclosure that confuses students.  
5. Coordinate AP-002 implementation milestones under the experience roadmap rather than shipping a disconnected quiz module.  
6. Treat ILE-005 as the home for product-wide uncertainty patterns; keep ILE-001 assessment-time contracts stable.  
7. Do not claim KSI movement from this design-only pack.

---

## 9. Design milestone verdict

**APPROVED FOR IMPLEMENTATION PLANNING** — Adaptive Assessment has a complete learner experience design aligned with ILE-000 product principles and certified Educational Intelligence authorities.

No production code, architecture changes, or educational reasoning changes were made in this milestone.

Implementation must preserve: *assess to understand; never assess to judge* — and *never overstate confidence*.

---

**End of ILE001_DESIGN_REVIEW**
