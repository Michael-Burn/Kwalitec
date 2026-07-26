# Version 1 Educational Review

**Programme:** EP-003 — Workstream 4  
**Version:** 1.0  
**Status:** Qualitative baseline review — quantitative validation pending private beta  
**Updated:** 2026-07-24  
**Subject:** Version 1 Platform Baseline  
**Does not:** Change product behaviour, Twin algorithms, or recommendation engines

---

## 1. Purpose

Evaluate whether core Version 1 educational surfaces are **useful for learning** — not merely present.

Surfaces in scope:

| Surface | Learner question |
|---|---|
| Mission / Session | What should I study now, and did I complete it? |
| Reflection | What did I learn / struggle with, and what changes next? |
| Coach | What guidance helps me decide without replacing judgement? |
| Journey | How am I progressing through the syllabus? |
| Digital Twin | Does the system’s model of me feel evidence-based and trustworthy? |

**Explicitly excluded until future PRDs:** Recommendation effectiveness / acceptance / benefit (EP-001 O8 / WS4). This review may note Coach *narrative* usefulness but must not claim recommendation engine validation.

---

## 2. Evaluation method

| Layer | Method | When |
|---|---|---|
| A — Design intent | Map surface to Vision + Educational Constitution | This document |
| B — Baseline readiness | Architecture / GA / LXP presence without redesign | This document |
| C — Learner evidence | Private-beta interviews + KPIs (M1–M9) | After cohort |
| D — Go / No-Go | Aggregate into educational release gates | [`GO_NO_GO_REPORT.md`](GO_NO_GO_REPORT.md) |

Ratings used here:

| Rating | Meaning |
|---|---|
| **Fit for beta** | Clear educational purpose; safe to evaluate with students |
| **Conditional** | Useful intent; known integrity / language / emit gaps |
| **Not ready to claim** | Must not be marketed as proven educational value yet |

---

## 3. Mission / Session usefulness

### Intent

Primary learning commitment. Linear flow: Overview → Activity → Reflection → Summary → Complete (`LEARNING_SESSION_EXPERIENCE`). Answers “what now?” with one objective.

### Evidence of usefulness (design)

- Aligns with Vision: structure, consistency, objective feedback.
- Completion is an educational KPI (M2, M4) with PRD-001 events (`session.started` / `session.completed`).
- Abandon is observable (`abandoned_after_start`) — enables honest completion rates.

### Known risks

- Historical Mission / Session / “Study Coach” naming friction (PTP-005) can confuse “one daily object.”
- Usefulness fails if students abandon because the Session feels like busywork — interview theme required.

### Baseline rating

**Fit for beta** — primary validation surface. Success depends on M4 + interview themes, not feature count.

### Review questions (beta)

1. Did Today's Session feel like the highest-value next study act?
2. Was completion meaningful (not click-through)?
3. When abandoned, why? (maps to M4)

---

## 4. Reflection usefulness

### Intent

Structured pause after study so learning consolidates and next study choices improve (Educational Constitution — reflection / feedback).

### Evidence of usefulness (design)

- Built into Session linear flow (not optional garnish in the canonical path).
- Instrumented: `reflection.submitted` / `reflection.completed`; body text excluded from analytics (privacy-correct).
- KPI M3 / EP-001 O7 define completion + quality flags.

### Known risks

- Skip-through / empty structured fields inflate completion without learning.
- Quality rubric (Phase 2) not yet the V1 marketing claim — completion ≠ quality.

### Baseline rating

**Fit for beta** for completion usefulness; **Not ready to claim** for “reflection improves outcomes” until M3 + interview + (later) quality rubric evidence.

### Review questions (beta)

1. Did reflection change what you did next?
2. Were prompts understandable?
3. Did you feel pressure to invent text vs honest struggle?

---

## 5. Coach usefulness

### Intent

Coaching narrative / Study Coach framing should help judgement: clarity, encouragement, explainability — without becoming a second educational brain or opaque AI tutor.

### Evidence of usefulness (design)

- Product philosophy: AI improves judgement; recommendations (when present) must be explainable — but recommendation *engine* validation is out of scope here.
- Coach copy appears in Mission / Session chrome; Daily Briefing / tips historically competed with Mission (PTP-004) — cohesion work reduces dual messaging.

### Known risks

- Multiple names (Mission / Session / Study Coach) dilute trust.
- Coaching that contradicts Today's Session topic destroys usefulness (IA-001 integrity lessons).
- Must not equate “Coach present” with “Coach improves pass probability.”

### Baseline rating

**Conditional** — narrative Coach may aid orientation; educational effectiveness claims require interview evidence that Coach clarifies *why* without conflicting with Session. Recommendation ranking excluded.

### Review questions (beta)

1. Did Coach language help you know what to do?
2. Did any Coach message conflict with Today's Session?
3. Did you trust the tone (honest vs hype)?

---

## 6. Journey usefulness

### Intent

Show syllabus progress so students know where they are and what remains (Vision: “How am I progressing?”).

### Evidence of usefulness (design)

- Learning Journey domain exists; student Journey surfaces in orientation checklist.
- Progress velocity KPI (M5) defined; preferred event `journey.progressed` registered; **production emit deferred** (ADR-026) — measurement may be provisional.

### Known risks

- Progress UI without durable progression events under-measures velocity.
- Journey that feels like a second curriculum browser (activity without learning) fails Vision philosophy.

### Baseline rating

**Conditional** — fit for qualitative beta review; quantitative M5 claims labelled provisional until Journey emit / durable repository path is live.

### Review questions (beta)

1. Can you explain your progress in one sentence after using Journey?
2. Does Journey reduce anxiety or increase overwhelm?
3. Does progress match what Sessions felt like?

---

## 7. Digital Twin usefulness

### Intent

Evidence-based model of the learner that supports readiness / mastery interpretation without teaching, storing PDFs, or letting AI invent state (`STUDENT_DIGITAL_TWIN`).

### Evidence of usefulness (design)

- Twin is constitutional educational authority for belief; analytics only observes (`twin.evolved` hash + metadata).
- Time to Readiness (M8) and readiness accuracy (EP-001 O6) depend on Twin honesty.
- Twin V2 metric expansion designed under EP-001 but **implementation gated** — V1 baseline Twin must not be oversold.

### Known risks

- Self-report inflation / mastery theatre (philosophy audit EP findings) — Twin usefulness collapses if students see unearned “ready.”
- Learner-facing Twin explainability must stay traceable to evidence.
- Persistence / UI cutover notes: live surfaces still primarily consume Stage A readiness paths in places — do not claim full Twin-first UI.

### Baseline rating

**Conditional** — architectural Twin is fit as authority for measurement design; **Not ready to claim** student-perceived Twin usefulness until interviews + readiness calibration evidence exist. No Twin algorithm changes under EP-003.

### Review questions (beta)

1. Do readiness / progress signals match how prepared you feel?
2. When the system changes its view of you, is the reason understandable?
3. Any moment you felt the system was “making it up”?

---

## 8. Cross-cutting findings (baseline)

| Finding | Severity | Follow-up |
|---|---|---|
| Session is the right primary learning object for V1 validation | — | Measure M2/M4 |
| Reflection is instrumented and privacy-safe for completion metrics | — | Measure M3; defer quality claims |
| Coach / Mission naming cohesion still a trust risk | Medium | Interview + copy governance (no EP-003 code change) |
| Journey quantitative claims provisional until emit path | Medium | ADR-026 follow-through (separate programme) |
| Twin usefulness ≠ Twin existence | High for marketing | Go / No-Go forbids overclaim |
| Recommendations excluded | Gate | Future PRD |

---

## 9. Version 1 educational readiness (summary)

| Surface | Baseline rating | Ready to measure in beta? | Ready to claim effectiveness? |
|---|---|---|---|
| Mission / Session | Fit for beta | Yes | No — pending cohort evidence |
| Reflection | Fit for beta (completion) | Yes | No — pending M3 + interviews |
| Coach | Conditional | Yes (qualitative) | No |
| Journey | Conditional | Yes (qualitative / provisional M5) | No |
| Digital Twin | Conditional | Yes (careful; authority-respecting) | No |
| Recommendations | Excluded | No (effectiveness) | No |

**Programme conclusion:** Version 1 Platform Baseline is **ready for educational effectiveness measurement** under the Private Beta Protocol. It is **not** yet evidenced as measurably improving outcomes — that is the point of EP-003 execution after this documentation freeze.

---

## 10. Exit criteria (WS4)

| Criterion | Status |
|---|---|
| All five surfaces reviewed | COMPLETE |
| Recommendations exclusion explicit | COMPLETE |
| Beta questions defined | COMPLETE |
| Claim vs measure distinction clear | COMPLETE |

---

## References

- Vision 2030 · Educational Constitution  
- `knowledge/version2/LEARNING_SESSION_EXPERIENCE.md`  
- `knowledge/version2/STUDENT_DIGITAL_TWIN.md`  
- `knowledge/product/PTP-005_VERSION1_COHESION.md`  
- [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md)  
- [`GO_NO_GO_REPORT.md`](GO_NO_GO_REPORT.md)
