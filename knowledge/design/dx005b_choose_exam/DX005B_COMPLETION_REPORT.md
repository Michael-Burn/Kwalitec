# DX-005B Completion Report

**Programme:** DX-005B — Choose Exam Redesign (Discovery First)  
**Status:** Complete  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None (documentation-only; no CSS, layouts, components, or routes)

---

## Summary

DX-005B designs Choose Exam from first principles as the **student discovery surface** under **Discovery First**. The page answers one question — **Which exam do I want to begin?** — with exactly one Primary (**Begin Learning**) and an L0–L3 hierarchy (Ready curricula → Search/Filters → Supporting metadata → shell navigation). Coming Soon is secondary with **Notify when available** only. After commitment, Home owns continuation. Premium scorecard target **≥9/10** is met for the architecture. No UI was implemented.

---

## Elements removed

(From legacy Choose Exam / Study Plan wizard — Zero Legacy; register for implementation removal)

- Marketing / tutorial helper paragraphs on discovery  
- Feature lists and promotional catalogue chrome  
- Readiness percentages and progress rings  
- Recommendation essays / coach stacks on Choose Exam  
- Multiple Primaries (Next as peer product Primary; twin Yes/No filled CTAs)  
- Decorative badge clusters  
- Coming Soon as peer radio cards with repeated essay walls  
- Review sections presenting unchosen defaults (position / style / target) as if decided  
- “Today’s mission” / Home theatre on discovery  
- Operator pipeline language (Publish, Validation, Knowledge Graph) on student UI  
- Study Plan / Planning as the discovery nav purpose label (retire in favour of Choose Exam)

---

## Elements retained

| Element | Reason |
|---|---|
| **Page title — Choose Exam** | Recognition; DX-001 page heading |
| **L0 Ready list** | Decision object; select one published curriculum |
| **Primary — Begin Learning** | Sole commitment action |
| **Search + Family / Status / Sort** | Simple L1 find path |
| **L2 description / scope / updated** | Commitment confidence — not promotion |
| **Coming Soon band** | Honesty without false Begin |
| **Notify when available** | Secondary Soon affordance |
| **Confirm (quiet)** | Commitment check before Mission create |
| **Empty: Reason → Return later** | DX-003 / DX-005B empty law |
| **L3 shell navigation** | Escape without duplicate local nav |
| **Fail-closed Ready gate** | Preserve support / enrolment honesty |

Every retained element is justified by discovery or commitment — not decoration.

---

## Ready / Coming Soon honesty

| State | Affordance |
|---|---|
| Ready + enrolable | Select → Confirm → **Begin Learning** |
| Ready package, enrolment gated | Visible, non-selectable; no Begin |
| Coming Soon | **Notify when available** only |
| Not supported | Omitted |

Documented in `READY_STATE_SPEC.md` and `COMING_SOON_SPEC.md`.

---

## Selection flow

```
Student → Chooses curriculum → Confirms → Mission created → Redirect Home
```

Home receives the learner; Choose Exam does not become a second continuation surface.

---

## Estimated reduction in discovery friction

| Metric | Legacy | Target | Δ |
|---|---|---|---|
| Independent decisions on entry | 2–4 | **1** | ~60–75% |
| Primary-weight CTAs on path | Next + Begin + dual confirm | **1** (Begin Learning) | ~70% |
| Soon essay density | Repeated per-row walls | Band-secondary / one line | Major |
| Review surprise sections | 3+ unchosen blocks | ≤1 defaults line or omit | ~35%+ |
| Post-commit OS entry | Split Calibration/Home clarity | **Home** owns continuation | Continuity restored |

*(Estimates are architectural; not instrumented UX timings.)*

---

## Implementation notes

1. Do not CSS-hide legacy wizard chrome — replace discovery body and quiet the commitment path (`IMPLEMENTATION_PLAN.md`).  
2. Discovery DTO: Ready / Soon fields only — no KPI aggregates.  
3. Begin Learning → Home with Mission; coordinate Calibration as brief gate if still required.  
4. Rename nav Study Plan → Choose Exam; align Home empty CTA.  
5. Re-score live UI with `PREMIUM_SCORECARD.md`; any dimension ≤8 → redesign before ship.  
6. Update UI Guardian for discovery L0–L3 + Ready/Soon rules.  
7. No curriculum engine / V1–V2 changes.

---

## Known limitations

- Architecture only — live product still shows Study Plan wizard / legacy Choose Exam until implementation.  
- Notify-when-available may lack backend at Alpha — honesty over fake success.  
- Exam family filter depends on metadata maturity.  
- Runtime A Calibration may still sit between Begin and Home until a later simplification.  
- No Figma file; ASCII wireframe is the layout authority.  
- Premium scores are **design-target** scores, not validated on rendered UI.  
- Study Session still legacy until DX-005C.

---

## Recommendations for DX-005C

**DX-005C — Study Session Redesign** should:

1. Own **execution only** — practice steps now; not a second Home or Choose Exam.  
2. Receive learners from Home Primary (Continue Session) — not from discovery as daily entry.  
3. Preserve explainability / reflection at Session density — do not push essays back onto Choose Exam or Home.  
4. Honour Mission identity from DX-005A after Begin Learning handoff.  
5. Apply DX-001–003: one Primary per practice decision; no KPI theatre.  
6. Keep Return Home as the default post-session OS entry.  
7. Update Guardian rules for Session L0–L3 once defined.  
8. Sequence UI: stable Home + Choose Exam handoff before or tightly coupled with Session chrome.

---

## Premium review

See `PREMIUM_SCORECARD.md`.

| Dimension | Score |
|---|---:|
| Discovery Clarity | 10 |
| Decision Clarity | 10 |
| Commitment Honesty | 10 |
| Information Density | 9 |
| Professional Tone | 10 |
| Minimalism | 10 |
| Navigation Clarity | 10 |
| Handoff Continuity | 10 |
| Overall Premium Feel | 10 |

**Mandatory checks: PASS. Verdict: SHIP (design).**

---

## Files Created

- `knowledge/design/dx005b_choose_exam/DX005B_EXECUTIVE_SUMMARY.md`  
- `knowledge/design/dx005b_choose_exam/DISCOVERY_ARCHITECTURE.md`  
- `knowledge/design/dx005b_choose_exam/DISCOVERY_WIREFRAME.md`  
- `knowledge/design/dx005b_choose_exam/READY_STATE_SPEC.md`  
- `knowledge/design/dx005b_choose_exam/COMING_SOON_SPEC.md`  
- `knowledge/design/dx005b_choose_exam/SEARCH_FILTER_SPEC.md`  
- `knowledge/design/dx005b_choose_exam/PREMIUM_SCORECARD.md`  
- `knowledge/design/dx005b_choose_exam/IMPLEMENTATION_PLAN.md`  
- `knowledge/design/dx005b_choose_exam/DX005B_COMPLETION_REPORT.md`  

## Files Modified

- `.cursor/rules/99-CURRENT_MILESTONE.md` (milestone pointer → DX-005B complete)

## Tests Executed

None (documentation-only).

## Migration Impact

None.

## Architecture Compliance

N/A for curriculum V1/V2 traversal. No application layering or engine changes. Design architecture is additive under `knowledge/design/`. Student shell remains the learner shell (DX-002); Choose Exam is the discovery surface; Home remains continuation (DX-005A). Founder Subjects catalogue (DX-004B) unchanged and separate.

## Technical Debt

- Live Choose Exam / Study Plan wizard still violates DX-001–005B until implementation.  
- Nav still labels Study Plan / Planning.  
- Home empty CTA still “Open Study Plan” until DX-005A UI.  
- DX-005C required before Session feels premium end-to-end with Home/discovery handoff.

## CRI / KSI / Student Impact

N/A for validated KSI movement — design documentation only; no Runtime A ranking changes shipped. ΔKSI = 0 (provisional). ΔCRI = 0 (provisional; no board update). Student benefit is architectural (clearer discovery → commitment → Home) pending UI.

## Explainability Review

N/A for this documentation programme — Choose Exam forbids recommendation essays by design; no student-facing intelligence code changed. Re-run explainability checklist if Recommended markers are later driven by recommendation services.

## Recommendation Quality Review

N/A — no recommendation ranking changes in DX-005B. Recommended sort/marker is optional and essay-free when implemented.

## Version 1 readiness residual

N/A — does not claim V1 production-ready progress; clears a design gate for Student OS discovery UX.

---

## Exit criteria

| Criterion | Status |
|---|---|
| One Primary (Begin Learning) | ✓ Architecture |
| Discovery only | ✓ Architecture + boundaries |
| Honest Ready / Coming Soon separation | ✓ READY + COMING_SOON specs |
| Home receives learner after commitment | ✓ Selection flow + handoff |
| Premium score ≥9/10 | ✓ Scorecard (all ≥9) |

**DX-005B is complete.** The project may proceed to **DX-005C — Study Session Redesign** (design) and/or Choose Exam UI implementation per `IMPLEMENTATION_PLAN.md`.
