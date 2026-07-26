# Explainability Review Checklist

**Programme:** P-001.2 — Explainability Standard  
**Version:** 1.0  
**Status:** Mandatory gate for relevant EP / P programmes  
**Effective:** 2026-07-26  
**Canonical path:** `knowledge/product/p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md`  

---

## When this checklist is required

Complete this checklist for every future **EP** or **P** programme (and material milestone) that affects **student-facing intelligence**, including changes to:

- recommendations, Coach, or Insights copy/contracts;
- daily / study planning decisions shown to students;
- readiness assessments or composites;
- predictions or prioritisation surfaced as guidance;
- revision advice, study warnings, recovery, or reinforcement tied to educational decisions;
- presentation consolidation that narrates the above across Runtime A surfaces.

**Not required** (state N/A with one-line rationale in the completion report):

- Pure infrastructure, security hardening, or docs with no student-facing intelligence speech;
- Operator-only diagnostics with no student surface;
- Changes that cannot alter explanation content, confidence, or next actions.

**Authority:** `knowledge/GOVERNANCE.md` §4.2; companion law in [`EXPLAINABILITY_STANDARD.md`](EXPLAINABILITY_STANDARD.md).

---

## How to use

1. Copy the verification table into the programme completion report (or link here and attach a filled copy as `EXPLAINABILITY_REVIEW.md` in the programme folder).
2. Mark each item **Pass / Fail / N/A**.
3. Failures block “explainability complete” claims for that programme until remediated or explicitly waived by Product + Educational governance with written rationale.
4. Prefer under-claiming. Do not mark Pass without citing the surface or artefact reviewed.

---

## Document header (fill)

| Field | Value |
|---|---|
| **Programme / Milestone ID** | |
| **Title** | |
| **Date** | |
| **Reviewer** | |
| **Surfaces / contracts in scope** | |
| **Default explanation level(s)** | L1 / L2 / L3 |
| **Runtime A surfaces touched** | |

---

## Mandatory verification items

Every relevant programme must verify:

| # | Requirement | Pass / Fail / N/A | Evidence (path, surface, or note) |
|---|---|---|---|
| R1 | **Explanations are evidence-backed.** Why + Supporting evidence cite identifiable student/syllabus/practice inputs — not vague “learning evidence” authority theatre. | | |
| R2 | **Confidence is communicated appropriately.** Confidence / Suggested / Estimated / Cannot yet be estimated matches evidence strength; no false precision. | | |
| R3 | **Student action is clear.** Exactly one primary Suggested next action on the default path. | | |
| R4 | **Explanations avoid unnecessary technical detail.** No Twin / Adaptive / warrant / pipeline / entity-id leakage on student surfaces; Level 3 remains opt-in or operator-scoped. | | |
| R5 | **Explanations remain consistent across Runtime A.** Same decision class does not produce conflicting Why/Evidence/today stories across Dashboard, Coach, Insights, Plan, Readiness, Journey. | | |

---

## Schema & level checks (required when R1–R5 apply)

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Mandatory Explanation Schema fields present at the declared level (Recommendation, Why, Evidence, Confidence, Expected benefit, Next action, Review point when applicable). | | |
| S2 | Default level matches surface job (daily action → L1; judgement surfaces → L2; diagnostics → L3 opt-in). | | |
| S3 | Reading-time / length targets respected (L1 ≤ ~10s / ≤40 words primary; L2 ≤ ~45s). | | |
| S4 | EIP-003 four questions answered (Know / Estimate / Why / Next). | | |
| S5 | Facts, estimates, and advice remain distinguishable. | | |
| S6 | Advice does not silently replace Learning Mode / Today’s Mission authority. | | |
| S7 | Pattern used (or justified deviation) from [`EXPLANATION_PATTERNS.md`](EXPLANATION_PATTERNS.md) when a catalogue type applies. | | |
| S8 | Accessibility: meaning not colour-only; warnings include text reason + next action. | | |

---

## Outcome

| Result | Rule |
|---|---|
| **Pass** | All applicable R1–R5 are Pass; applicable S-items Pass or justified N/A |
| **Fail** | Any applicable R1–R5 is Fail — remediate before claiming student-trust improvement on K8 |
| **Waived** | Written Product + Educational governance waiver attached (rare; must state student risk) |

**Outcome for this review:** Pass / Fail / Waived  

**Notes:**

>

---

## Relationship to other gates

| Gate | Relationship |
|---|---|
| Student Impact Assessment | Still required for EP/P completion; this checklist does not replace it |
| Estimated KSI contribution | K8 claims require this checklist Pass (or honest ΔKSI = 0 if docs-only) |
| EVF / Educational Release Gate | May consume this checklist as trust evidence; EVF still owns release |
| EIP-003 / Architecture Art. IV | Higher educational/structural law — checklist verifies product conformance |

---

## Completion-report checklist

Programme completion reports for in-scope work must include or link:

- [ ] Filled verification tables (R1–R5 and applicable S-items)
- [ ] Outcome (Pass / Fail / Waived)
- [ ] Link to [`EXPLAINABILITY_STANDARD.md`](EXPLAINABILITY_STANDARD.md)

---

**End of EXPLAINABILITY_REVIEW_CHECKLIST**
