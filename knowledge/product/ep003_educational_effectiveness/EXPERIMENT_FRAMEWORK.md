# Experiment Framework

**Programme:** EP-003 — Workstream 3  
**Version:** 1.0  
**Status:** Active governance  
**Updated:** 2026-07-24  
**Authority:** Product + Educational governance + Architecture (for behaviour changes)  
**Does not:** Authorise silent A/B changes to Twin, Educational State, Mission selection, or recommendations

---

## 1. Purpose

Provide a **standard experiment template** and hard rule:

> **No experiment may influence educational behaviour without an approved PRD.**

Observation-only analysis (reading existing events, interviews, scorecard trends) does **not** require an experiment PRD. Any change to what the student is shown, assigned, scored, or recommended **does**.

---

## 2. Hard gates

| Gate | Rule |
|---|---|
| PRD required | Behaviour-influencing experiment → PRD from `knowledge/prd/PRD_TEMPLATE.md`, status **Approved** before start |
| Educational honesty | Must not fake mastery, readiness, or next action for metric gaming |
| One Educational Truth | Analytics / experiment code must not invent Twin or ESS beliefs |
| Recommendations | Recommendation behaviour experiments require a dedicated future PRD (explicitly out of EP-003 scope) |
| Rollback | Every experiment defines rollback before start; default = restore prior behaviour via flag / config / revert |
| Privacy | New data collection paths require Privacy Review update |
| Sample floors | Claims follow [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md) §4 / EP-001 §5 |

---

## 3. Experiment template (required fields)

Copy this block into the experiment PRD (or PRD appendix). All fields mandatory.

```markdown
## Experiment card

| Field | Content |
|---|---|
| **Experiment ID** | EXP-NNN |
| **Title** | |
| **Owner** | |
| **PRD ID** | PRD-NNN (must be Approved before start) |
| **Status** | Draft \| Approved \| Running \| Stopped \| Completed \| Rolled back |

### Hypothesis

State a falsifiable claim about learning (not vanity activity).

Example: “If we clarify Session reflection prompts, Reflection Completion Rate (M3) rises by ≥10 pp without reducing Session Completion Rate (M4).”

### Population

| Field | Spec |
|---|---|
| Inclusion | |
| Exclusion | |
| N target | |
| Assignment | All-on / staged cohort / time-split (describe). Randomised assignment only with ethics + privacy note. |

### Success Metric

| Field | Spec |
|---|---|
| Primary metric | Must be an ID from EDUCATIONAL_METRICS (M1–M9) or EP-001 (O1–O9) |
| Guardrail metrics | Metrics that must not regress beyond threshold |
| Decision rule | Pre-registered: ship / iterate / rollback |

### Duration

| Field | Spec |
|---|---|
| Start | |
| End (planned) | |
| Minimum exposure | |
| Early-stop rules | P0 harm, support overload, educational honesty breach |

### Risk

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Educational harm (wrong next action, false readiness) | | | |
| Privacy | | | |
| Support load | | | |
| Dual-truth / architecture drift | | | |

### Rollback

| Field | Spec |
|---|---|
| Trigger | |
| Mechanism | Feature flag OFF / config revert / release revert |
| Verification | How we confirm prior behaviour restored |
| Owner on-call | |
```

---

## 4. Allowed without experiment PRD

| Activity | Notes |
|---|---|
| Scorecard / dashboard analysis of existing events | Read-only |
| Private-beta interviews | Per protocol |
| Bug fixes restoring intended documented behaviour | Normal PR; not an “experiment” |
| Copy clarifications that do not change selection / scoring | Prefer lightweight PR; if disputed as behavioural, escalate to PRD |

---

## 5. Forbidden without Approved PRD

- Changing Mission / Session selection or completion rules
- Changing Twin update rules, readiness bands, or mastery interpretation
- Changing Educational State assembly contracts
- Changing recommendation ranking, content, or pressure-to-accept
- New analytics payloads that include educational content or PII beyond approved catalogue
- Holding out educational help from a control group in a way that harms learning without ethics review

---

## 6. Lifecycle

```text
Idea → Hypothesis + metric ID
    → Draft PRD (template + experiment card)
    → Review (Product, Educational, Architecture as needed)
    → Approved
    → Run (duration + monitoring)
    → Analyse vs pre-registered rule
    → Ship / iterate / rollback
    → Write short completion note linked from PRD
```

---

## 7. Reporting

| Audience | When | Content |
|---|---|---|
| Founder / Product | Weekly while Running | Primary + guardrails vs decision rule |
| Educational governance | On stop / complete | Honesty + outcome impact |
| V1 Go / No-Go | If experiment affects educational readiness claim | Link evidence |

---

## 8. Exit criteria (WS3)

| Criterion | Status |
|---|---|
| Template defined | COMPLETE |
| PRD-required rule documented | COMPLETE |
| Rollback mandatory | COMPLETE |
| Recommendation exclusion explicit | COMPLETE |

---

## References

- [`../../prd/PRD_TEMPLATE.md`](../../prd/PRD_TEMPLATE.md)
- [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md)
- [`../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md`](../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md)
- [`../../educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md`](../../educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md)
