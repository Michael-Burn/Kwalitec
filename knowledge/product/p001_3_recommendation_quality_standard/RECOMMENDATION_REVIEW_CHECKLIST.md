# Recommendation Review Checklist

**Programme:** P-001.3 — Recommendation Quality Standard  
**Version:** 1.0  
**Status:** Mandatory gate for relevant EP / P programmes  
**Effective:** 2026-07-26  
**Canonical path:** `knowledge/product/p001_3_recommendation_quality_standard/RECOMMENDATION_REVIEW_CHECKLIST.md`  

---

## When this checklist is required

Complete this checklist for every future **EP** or **P** programme (and material milestone) that affects **student-facing recommendations**, including changes to:

- recommendation ranking, selection, or RecommendationService prioritisation;
- Coach / Insights / Dashboard / Mission tips framed as “what to do next”;
- revision, recovery, weak-topic, exam-prep, or workload recommendations;
- presentation consolidation that changes which recommendation wins as primary across Runtime A;
- copy or contracts that alter recommended actions (even if algorithms are unchanged).

**Not required** (state N/A with one-line rationale in the completion report):

- Pure infrastructure, security hardening, or docs with no recommendation behaviour or speech;
- Operator-only diagnostics with no student recommendation surface;
- Explainability-only wording changes that do not alter *what* is recommended (still require Explainability Review per §4.2 when in scope);
- Non-recommendation intelligence (e.g. readiness composite packaging) unless it emits a recommended next action.

**Authority:** `knowledge/GOVERNANCE.md` §4.3; companion law in [`RECOMMENDATION_QUALITY_STANDARD.md`](RECOMMENDATION_QUALITY_STANDARD.md).

---

## How to use

1. Copy the verification table into the programme completion report (or link here and attach a filled copy as `RECOMMENDATION_REVIEW.md` in the programme folder).
2. Mark each item **Pass / Fail / N/A**.
3. Failures block “recommendation quality complete” and K2 improvement claims for that programme until remediated or explicitly waived by Product + Educational governance with written rationale.
4. Prefer under-claiming. Do not mark Pass without citing the surface, decision case, or artefact reviewed.
5. When recommendations are in scope, also complete the [Explainability Review Checklist](../p001_2_explainability_standard/EXPLAINABILITY_REVIEW_CHECKLIST.md) unless speech is unchanged and already compliant (state rationale).

---

## Document header (fill)

| Field | Value |
|---|---|
| **Programme / Milestone ID** | |
| **Title** | |
| **Date** | |
| **Reviewer** | |
| **Recommendation surfaces / contracts in scope** | |
| **Decision cases reviewed** | (e.g. weak topic vs missed session) |
| **Runtime A surfaces touched** | |

---

## Mandatory verification items

Every relevant programme must verify:

| # | Requirement | Pass / Fail / N/A | Evidence (path, surface, or note) |
|---|---|---|---|
| Q-R1 | **Recommendation solves a real student problem.** Addresses a concrete study need (what to do now, recovery, weak-topic repair, revision timing, workload honesty) — not tip inventory or engagement filler. | | |
| Q-R2 | **Recommendation is evidence-backed.** Supporting inputs are identifiable (syllabus position, practice results, missed sessions, plan state, time-to-exam). Vague authority language fails. | | |
| Q-R3 | **Recommendation is proportionate.** Implied effort matches available time and evidence strength; no overwhelm dumps or trivial busywork as primary. | | |
| Q-R4 | **Recommendation has clear expected benefit.** Educational impact is nameable (coverage, repair, readiness honesty, revision, recovery) — not streak / vanity metrics. | | |
| Q-R5 | **Recommendation aligns with Product Constitution.** Passes Vision Final Test; does not fight Learning Mode / Today’s Mission without advice labelling; serves professional exam preparation. | | |
| Q-R6 | **Recommendation complies with Explainability Standard.** P-001.2 schema satisfiable at default level; Explainability Review Pass or justified N/A. | | |

---

## Decision & dimension checks (required when Q-R1–Q-R6 apply)

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| Q-D1 | Hard gates applied (lawful warrant, correctness, plan coherence, explainability readiness, proportionality, honest refusal). | | |
| Q-D2 | Competing candidates ranked per [`RECOMMENDATION_DECISION_FRAMEWORK.md`](RECOMMENDATION_DECISION_FRAMEWORK.md) (or justified documented exception). | | |
| Q-D3 | Quality dimensions addressed: Correctness, Priority, Personal relevance, Expected educational impact, Student effort, Confidence, Review trigger. | | |
| Q-D4 | Exactly one primary recommendation on single-CTA surfaces; secondaries do not override authorised today. | | |
| Q-D5 | Runtime A consistency: same decision class does not produce conflicting primary recommendations across Dashboard, Coach, Insights, Plan, Journey that day (unless plan state changed). | | |
| Q-D6 | Scorecard impact noted: which of Precision / Acceptance / Completion / Effectiveness / Satisfaction / Explainability compliance are expected to move (or explicitly “none yet — enabling only”). | | |
| Q-D7 | No effectiveness marketing claims beyond approved evidence freeze rules. | | |

---

## Outcome

| Result | Rule |
|---|---|
| **Pass** | All applicable Q-R1–Q-R6 are Pass; applicable Q-D items Pass or justified N/A |
| **Fail** | Any applicable Q-R1–Q-R6 is Fail — remediate before claiming K2 improvement |
| **Waived** | Written Product + Educational governance waiver attached (rare; must state student risk) |

**Outcome for this review:** Pass / Fail / Waived  

**Notes:**

>

---

## Relationship to other gates

| Gate | Relationship |
|---|---|
| Student Impact Assessment | Still required for EP/P completion; this checklist does not replace it |
| Estimated KSI contribution | K2 claims require this checklist Pass (or honest ΔKSI = 0 if docs-only) |
| Explainability Review (§4.2) | Complementary — speech vs selection/priority; both when recommendations change |
| EVF / Educational Release Gate | May consume this checklist as usefulness evidence; EVF still owns release |
| Educational Recommendation Model | Higher educational meaning law — checklist verifies product conformance |

---

## Completion-report checklist

Programme completion reports for in-scope work must include or link:

- [ ] Filled verification tables (Q-R1–Q-R6 and applicable Q-D items)
- [ ] Outcome (Pass / Fail / Waived)
- [ ] Link to [`RECOMMENDATION_QUALITY_STANDARD.md`](RECOMMENDATION_QUALITY_STANDARD.md)
- [ ] Explainability Review outcome or N/A rationale

---

**End of RECOMMENDATION_REVIEW_CHECKLIST**
