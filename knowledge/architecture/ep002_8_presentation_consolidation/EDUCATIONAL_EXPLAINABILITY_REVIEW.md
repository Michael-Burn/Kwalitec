# EP-002.8 — EducationalExplainability Review

**Milestone:** EP-002.8  
**Date:** 2026-07-26  
**Decision:** **Outcome B — Become a presentation adapter (legacy)**

---

## Options evaluated

| Option | Meaning | Verdict |
|---|---|---|
| **A** Remain as a separate presentation component | Peer SoT beside Insight on Twin surfaces | Rejected — violates Programme O5 / TD-ARCH-02 retirement |
| **B** Become a presentation adapter | Legacy/fail-open narration under unified facade | **Accepted** |
| **C** Be deprecated | Remove EIP-003 service | Rejected — fail-open + coverage + session still require it |

---

## Evidence

1. **EIP-003 scope** — “binds presentation and coaching copy only”; does not own evaluation (`EDUCATIONAL_EXPLAINABILITY_STANDARD.md`).
2. **EP-001.4 ownership** — Communication / student guidance canonical owner is RecommendationService + Insight when Twin ON (`AUTHORITY_MATRIX.md` AD-03).
3. **Programme O5** — Collapse dual presentation without inventing a third narrator.
4. **Fail-open law** — Production and ineligible cohorts must keep truthful legacy narration.
5. **Partial skips already treat EIP-003 as skippable** when Twin owns communication (EP-002.5–7).

---

## Binding rules after EP-002.8

1. For Runtime A dashboard / analytics / mission **index** surfaces, narration selection goes through `RuntimeAPresentationAdapter`.
2. When `source_authority` is Twin-owned, do **not** call EIP-003 re-narration for that concern.
3. When `source_authority` is `legacy`, EIP-003 remains the speech adapter.
4. Coverage readiness and session feedback remain EIP-003 (ORM-backed, no Twin cutover).
5. EIP-003 speech rules (Observed / Estimates / Advice / Next step) remain the standard for legacy cohorts and the explainability macro.
6. Templates must not gain evaluation or planning logic.

---

## Non-decisions

- Does not merge EI Stage A `RecommendationCardBuilder` into EIP-003 or Insight.
- Does not delete `educational_explainability.html`.
- Does not claim Twin Ready or deprecate EIP-003 globally.
