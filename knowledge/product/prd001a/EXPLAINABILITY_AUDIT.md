# PRD-001A — Explainability Audit

**Standard references:** P-001.2 Explainability; MES delivery (EP-006.x); Recommendation Trust (EP-008.x).  
**Student surface of record:** EOS Home (`student/home.html`) + Session overview + Revision.

---

## Recommendation explainability checklist (student-answerable?)

| Question | Visible on Home when MES complete? | Honest for Learning Mode mission? | Gap |
|---|---|---|---|
| Why this topic? | **Yes** — `why_recommended` | Often educational benefit language; **may not** say “next incomplete syllabus leaf” | B |
| Why today? | **Yes** — `timeliness_line` (“Why now”) | May cite plan/day framing; not EK urgency | B |
| Why now? | Same as above | Same | B |
| Why ~30 minutes? | **Partial** — duration label from plan minutes | Duration is preference/plan math, rarely explained as such | B |
| Why before another chapter? | **Rarely explicit** | True reason is canonical order — under-stated | A/B |
| What evidence produced this? | **Partial** — L2 supporting evidence / readiness drivers | Evidence may describe readiness/practice even when selection ignored mastery | B / integrity risk |

---

## Where explainability is implemented

| Surface | Mechanism | Student-visible |
|---|---|---|
| Home hero | L1 Why / Why now / Next / Benefit | Yes |
| Home disclosure | `explanation_card` (“Why this tip?”) + alternatives | Yes (opt-in details) |
| Readiness panel | “Why this estimate?” drivers/evidence | Yes |
| Coach | Structured why/why_now when not duplicating hero | Partial |
| Session overview | `why_studying` | Yes |
| Revision | `explanation_card` | Yes |
| Journey / History | Structural / narrative — not full decision chain | No for daily MES |
| Decision Journal | Backend `Decision` rows | **Not** primary student UI |

Schema keys (packaging): `why_recommended`, `supporting_evidence`, `suggested_next_action`, `confidence_level`, `expected_benefit`, `plan_coherence`, `explanation_schema_version` (`recommendation_quality.py`).

---

## Hidden-from-students gaps (must record)

| Hidden truth | Student impact | Category |
|---|---|---|
| Learning Mode ignores review/weak interruption by law | Students infer broken adaptivity | A (rule hidden) |
| Twin OFF in production | “Education OS intelligence” feels hollow vs Blueprint Twin language | A + D |
| EK does not pick today’s topic | “Understanding” promise unmet on primary CTA | A |
| Decision Journal exists internally | No self-audit of past accepts/dismisses | A |
| Legacy analytics charts redirected | Deeper evidence charts unavailable on sole runtime | C |

---

## Explainability integrity rule (audit finding)

**Explainability without selection transparency is a student experience gap even when MES fields are non-empty.**

If L1 text implies personalised understanding-driven choice while `_select_topic_for_today` uses only `completed`, classify as:

- **Category B** if copy is vague, or  
- **Category F** if Blueprint/Vision language was updated toward Twin-first decisions without updating Learning Mode law or student contract.

Version 1 Blueprint already admits Twin-first cutover is incomplete — student-facing honesty should match that admission.
