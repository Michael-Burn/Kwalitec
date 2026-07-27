# Educational Clarity Review — PR-001B

**Programme:** PR-001B — Student Pilot Journey  
**Date:** 2026-07-27  
**Surfaces reviewed:** Student Home, Journey, Educational context panel (Runtime C)

---

## Review questions

Every Runtime C educational explanation must answer:

1. **Why this mission?**  
2. **Why now?**  
3. **What should I accomplish?**  
4. **What comes next?**

---

## Field mapping

| Question | Product fields | Where shown |
|---|---|---|
| Why this mission? | `why_this_mission` / `educational_rationale` / hero **Why** | Home hero; Educational context `mission_rationale` |
| Why now? | `why_today` / timeliness | Home **Why now**; Educational context `why_today` |
| What should I accomplish? | Learning objectives + **Done when** (`completion_definition`) | Educational context |
| What comes next? | `suggested_next_action` / `unlocks_next` | Educational context `what_comes_next`; Journey unlocks next; hero Next |

Supporting: curriculum position, estimated duration, prerequisites, progress, exam pacing, explainability disclosure.

---

## Verdict

| Criterion | Result | Evidence |
|---|---|---|
| Why this mission present | **Pass** | EQ-001 rationale + PX-001 panel; acceptance `test_four_clarity_questions` |
| Why now present | **Pass** | Journey explanation `why_today` |
| Accomplish criteria present | **Pass** | Objectives + completion definition |
| What comes next present | **Pass** | Panel `what_comes_next` (PR-001B); unlocks_next |
| HTTP visibility | **Pass** | `data-edu-field` assertions in PR-001B suite |

**Overall: Pass** for Runtime C Home/Journey pilot clarity.

---

## Residual clarity risks

- Explainability disclosure is nested under a `<details>` block — primary answers are above the fold; disclosure is optional depth.  
- Revision/History are not Runtime C projected — students directed to Home/Journey in docs.  
- Mission study happens off-platform; clarity of CTA copy (“Mark mission complete”) is documented in the Pilot Guide to avoid Guided Session expectations.

---

## Changes in PR-001B

- Surfaced **What comes next** as a first-class Educational context field.  
- Home CTA enabled for Runtime C completion with honest helper copy (study materials, then confirm).  
- Day-complete copy includes next-up guidance from `unlocks_next` when available.
