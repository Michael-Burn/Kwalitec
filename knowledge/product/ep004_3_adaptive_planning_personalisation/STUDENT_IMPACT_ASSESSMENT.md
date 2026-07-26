# EP-004.3 — Student Impact Assessment

**Template:** [`../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-004.3 |
| **Title** | Adaptive Planning Personalisation |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | Gated — only when Personal Learning Profile flag ON and attributes available |
| **Production activation?** | Gated (default OFF) |
| **Related KSI categories** | K1, K4, K7, K8 |

---

## 1. Student problem

**Student problem:**

> Today's plan can feel one-size-fits-all — it ignores how I actually complete plans, recover after misses, revise, and how long I prefer to study, even after the product has observed those behaviours.

**Evidence:**

> K4 personalisation remained thin for planning after EP-004.1 (substrate only) and EP-004.2 (recommendations closed). EP-003.3 improved explainability and recovery structure but not habit-aware pacing.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | Next action / review-first framing can reflect revision habits |
| How am I progressing? | N/A | No new progress surface |
| What is stopping me? | Partial | Low completion / declining consistency lightens pace |
| What happens next? | Yes | Session duration alignment from declared preference when available |

**Student benefit summary:**

> When the profile flag is ON and evidence is strong enough, the day plan can feel more completable and personal without becoming opaque — students see when habits influenced pacing or repair emphasis.

**Final Test:** Does this help students become better professionals? **Yes** — sustainable, explainable daily plans that respect observed study behaviour support disciplined preparation.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Improves learning (not activity theatre)? | Yes — protects review timing; emphasises repair when follow-through supports it; lightens overload |
| Avoids false mastery claims? | Yes — habit rates never invent mastery or readiness scores |
| Preserves Mission / plan authority? | Yes — educational slot order unchanged; PlanningService remains owner |

---

## 4. Success metrics

| Metric | Target (estimated) | Notes |
|---|---|---|
| Personalisation explainability compliance | 100% of personalised plans carry factors + evidence | Test-backed |
| Educational order integrity | 100% of personalised plans keep review→repair→progression | Abort on violation |
| Flag-OFF behavioural parity | Identical to EP-003.3 baseline | Fail-open |
| K1 / K4 estimated movement | See KSI Impact | Under-claim; live re-score pending |

---

## 5. Risks to students

| Risk | Mitigation |
|---|---|
| Opaque “personalised for you” plans | Require factor + evidence disclosure |
| Over-fitting thin history | Confidence + sample gates; unsupported ignored |
| Undermining syllabus priorities | Educational order hard-preserved |
| Swapping to weaker topics inappropriately | Equivalent selection only among revision-pool alternatives when follow-through is low |

---

## 6. Assumptions

- Profile flag remains independently gated.
- Declared session minutes may be supplied later via settings; until then duration stays unsupported unless declared.
- Live Scorecard lifts are not claimed in this programme.
- Recommendation accept/dismiss must not drive plan construction.
