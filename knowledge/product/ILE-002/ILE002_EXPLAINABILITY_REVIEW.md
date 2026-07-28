# ILE-002 Explainability Review

**Programme / Milestone ID:** ILE-002  
**Title:** Decision Journal  
**Date:** 2026-07-28  
**Reviewer:** Implementation agent (Composer)  
**Surfaces / contracts in scope:** `/student/decision-journal` timeline; `DecisionJournalService.to_student_dict`  
**Default explanation level(s):** L2 (judgement / continuity surface)  
**Runtime A surfaces touched:** History sibling (Decision Journal); Home commitment mirror write path only  

Template: `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | Pass | `supporting_evidence_summary` + append-only evidence events; seeded from tip reason / review point |
| R2 | Confidence communicated appropriately | Pass | Qualitative ILE-011 bands only; `CONFIDENCE_LABELS` student text |
| R3 | Student action is clear | Pass | `student_action_label` / “What did I choose?” |
| R4 | Avoid unnecessary technical detail | Pass | `assert_student_safe_text`; presentation tests forbid Twin/engine terms |
| R5 | Consistent across Runtime A | Pass | Journal narrates the same tip family already shown on Home; does not invent rival ranking |

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Mandatory schema fields | Pass | observation, meaning, recommendation, evidence, confidence, benefit, uncertainty, outcome |
| S2 | Default level matches surface | Pass | Continuity / reflection surface → L2 |
| S3 | Reading-time targets | Pass | Arc fields are short prose; details collapsed |
| S4 | EIP-003 four questions | Pass | What / Why / Chose / Afterwards (+ learn) |
| S5 | Facts vs estimates vs advice | Pass | Observation vs meaning vs recommendation separated |
| S6 | Advice does not replace Mission authority | Pass | Journal is retrospective; no competing “start now” authority |
| S7 | Pattern from EXPLANATION_PATTERNS | Pass | Default arc |
| S8 | Accessibility | Pass | Text labels; details/summary keyboard; landmarks |

## Verdict

**Pass** — journal freezes explainability for significant guidance without exposing internals.
