# ADR-027 Phase 3 — V1 Adaptive Policy Design (Final)

## Status
Design, verified against current code and data. Not yet authorized for implementation -- a separate scoped implementation brief is required before any code changes.

## Governing ADR
docs/adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md

## Revision history

This design went through two rounds of correction based on empirical verification before reaching this final form. An earlier version assumed a consolidation mechanism already existed on the runtime real students actually use and just needed to become evidence driven; verification found that runtime has no review concept at all today. A second version assumed review could be targeted at an individual weak topic; verification found the content that actually exists for review purposes is organized as topic blocks, each covering a cluster of related syllabus topics together, with no clean way to address an individual topic in isolation. This is the design that accounts for both corrections.

## Context

Phase 2 made the Learner Twin the genuine, unconditional, canonical source of Estimated Knowledge for this product. Policy V0, introduced in Phase 1, was a deliberate behavioral wrap of the existing linear selection logic, designed to prove the Decision Engine boundary was correct without yet introducing any adaptive intelligence. The runtime real students use today, once enrolled, progresses through new material indefinitely with no mechanism to revisit anything already covered.

This phase closes that gap directly, using a policy built from principles this project has already established as sound rather than invented from nothing: this product's own creator intends to use it himself as a genuine student before anyone else does, which is a real evidence loop, however small at first, and the standing development philosophy for this project is to build the best reasoned version of a given piece now, grounded in realistic assumptions and this product's own established pedagogy, refining it once real use exists rather than either guessing without grounding or deferring indefinitely for a population of users that does not yet exist.

## The V1 policy

Policy V1 replaces Policy V0's internal logic behind the exact same decision interface already established in Phase 1. It introduces no new decision type and requires no change to the three recorded outcomes already in place.

A review day is determined using the same cadence this product has already validated on its other runtime: reviewing becomes due roughly every four new topics when more than sixty days remain before the student's exam, every three topics between thirty and sixty days, and every two topics inside thirty days. This cadence is reused deliberately rather than reinvented, since it reflects judgment this project has already applied and validated elsewhere.

On a day when review is due, the policy considers every existing authored revision package for the student's subject. Each such package already covers a defined cluster of syllabus topics. For each package, the policy looks at every topic in its cluster that the student has covered and for which the Learner Twin has recorded at least three independent evidenced observations, the same reliability floor established earlier in this project's own reasoning: a topic with fewer than three observations is not yet a reliable enough signal to act on, whether considered alone or as part of a larger cluster. The policy averages the Estimated Knowledge across whichever of a package's topics meet that bar, producing a weakness score for that package. The package with the lowest such score, among all packages that have at least one topic meeting the bar, is selected as that day's review target.

Packages are allowed to share topics in their coverage, and this is not treated as a conflict to resolve: each package is scored independently, and a topic that is genuinely weak may quite reasonably pull down the score of more than one package that happens to include it. The policy does not need a single, exclusive mapping between a topic and a package to make a sound choice.

If no revision package yet has even one topic meeting the evidence bar, which is the expected and entirely normal state for a student, including this product's own creator, early in his own use of the platform, the policy defers to Policy V0's existing behavior exactly as it stands today and introduces the next new topic as normal. This is recorded honestly as a safe fallback outcome, not as an adaptive one, consistent with this project's standing principle that a fallback must never be presented as though it were a genuinely adaptive decision.

As a student's exam date approaches, the review cadence itself tightens continuously rather than switching abruptly at a single point, becoming meaningfully more frequent in the final weeks before the exam. This uses the student's own exam date, which already exists on this runtime's enrolment record but is not yet available at the point this decision is made, and will need to be added to the request this policy receives.

## Known content limitations, tracked deliberately rather than treated as a blocker

Two real gaps exist in the revision content available today. The syllabus's opening topics have no revision package dedicated specifically to them, only packages that touch them as part of a broader mixed cluster. And the depth of retrieval practice within existing revision packages is thin relative to the breadth of syllabus material each one claims to cover, often only two practice items for a cluster spanning five to ten topics. Neither of these is a limitation of this architecture; both are gaps in authored content that can be closed later using the same careful, individually reviewed batch process this project has already used successfully several times over for exactly this kind of content work. This is deliberately treated as a follow up to be prioritized once real use, starting with this product's own creator, reveals which gaps actually matter in practice, rather than something to guess at and fix pre-emptively now.

## Relationship to the existing architecture

This remains Policy V1 behind the Decision Engine boundary established in Phase 1. It changes nothing about that boundary, the thin coordination layer between it and session composition, or that composition layer's role as a pure executor of a decision already made. It reads Estimated Knowledge exclusively through the canonical Learner Twin query interface established in Phase 2 and never touches any retired legacy representation. Every decision it produces remains one of the same three recorded outcomes already established: a genuinely evidence driven review selection is recorded as adaptive, deferring to the existing new material progression because too little evidence yet exists is recorded honestly as a safe fallback, and any case where no valid decision can be made at all remains blocked, exactly as already handled.

## Consequences

This is expected to be the first decision this product makes about a real student that is genuinely adaptive in the sense the entire architecture leading up to this phase exists to make possible, introducing the concept of review to a runtime that has never had one, using content this project has already authored and a cadence this project has already validated, with an honest and expected fallback for exactly the situation its own creator will be in personally when he first begins using it as a real student himself.

---

## Verification findings

Empirical check against the current working tree and local data (2026-08-30), after the block-level correction. Findings only — this document still does **not** authorize implementation.

### 1. Block coverage via `return_targets` — present in content; not yet on the typed loader model

**Count:** There are **19** publication-approved CS1 revision packages under `app/curriculum/data/educational_packages/cs1/` (matches the inventory asserted in package MCQ tests). `EducationalPackageLoader.packages_for_subject("CS1")` filtered by `mode == "revision"` returns the same **19**.

**Field in JSON:** Every one of those 19 JSON files has a non-empty top-level `return_targets` list of syllabus LO / topic codes (examples: `2.6.1`…`2.6.6` on sampling-distributions; `4.1.1`…`4.1.5` on linear-models; 24 targets on midspine). Overlap across packages is real (e.g. linear-models and linear-regression-NU share `4.1.1`–`4.1.5`; midspine / regression-GLM / GLM-XI share large 4.x / 5.x clusters) — consistent with scoring each package independently.

**Queryable at decision time today?** Partially.

| Surface | Result |
|---------|--------|
| Raw package JSON on disk | Yes — `return_targets` present on all 19 |
| Runtime C inventory discovery | Yes — same loader already used by Runtime C (`find_package_by_id` / `packages_for_subject` / `EducationalPackageLoader`) discovers all 19 revision packages |
| Typed `CertifiedEducationalPackage` | **No** — `app/application/educational_packages/models.py` has no `return_targets` field; `_parse_package` in `loader.py` does not map it (metadata keeps only `cmp_edition` / `published_at`) |
| Practical bridge without inventing a new corpus | Yes — loaded packages retain `source_path`, so an implementation can re-read `return_targets` from the same JSON the loader already resolved, or (preferable at implement time) add an additive parse onto the model |

**Verdict for this design:** The block-scoring mechanism is computable from existing authored data. The cluster membership is genuine and discoverable through the package inventory Runtime C already uses. Surfacing `return_targets` as a first-class field (or reading it via `source_path`) is a small, additive implementation concern for the future brief — not a missing-content blocker and not something this design-only milestone changes.

Content-gap claims in the design prose also match disk: opening `1.1*` topics appear only inside mixed clusters (`PURPOSE-EDA`, `PUBLICATION-FRONT-RHO`), with no dedicated opening-only revision package; 17 of 19 packages have only two knowledge-check items (typically 1 active_recall + 1 checkpoint) against clusters of 2–24 targets.

### 2. Learner Twin query — EK + `evidence_count` for a block of topics

`LearnerTwinQueryPort` (`app/application/student_twin/query.py`) and `DailyLoopLearnerTwinQueryAdapter` already expose, per topic:

- `estimated_knowledge` / `has_estimated_knowledge`
- `evidence_count`
- `last_practised_at`
- plus `topic_covered(...)` for Study Progress coverage

**Batch vs N calls:**

| Method | Shape | Notes |
|--------|-------|-------|
| `topic_knowledge(...)` | One topic | Exists; adapter reloads the Twin document on **each** call |
| `knowledge_snapshot(...)` | All Twin topics for learner/subject | One load; filter in memory by the package’s `return_targets` |
| `topics_with_estimated_knowledge(...)` | All topics with admitted EK | Same snapshot path underneath |
| Dedicated `topics_knowledge(topic_ids: Sequence[str])` | **Does not exist** | Not required for correctness |

**Practical approach for block scoring:** one `knowledge_snapshot` (or `topics_with_estimated_knowledge`) plus coverage checks for the package’s target ids, then average EK over targets that are covered and have `evidence_count >= 3`. N separate `topic_knowledge` calls would work for CS1-scale clusters (≤24 targets) but are unnecessarily chatty because each call reloads the Twin. Either approach is practical; snapshot-then-filter is the natural fit.

### 3. Worked example (illustrative — local Twin stores empty)

Local `instance/kwalitec.sqlite3` has **zero** daily-loop Twin documents (`student_digital_twins`, `twin_snapshots`, and related stores empty / unused for Stack B daily-loop). Session-document Twin persistence was likewise empty for a live student. Therefore the numeric example below is **illustrative**, built with:

- **Real** package: `CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS` (`revision-sampling-distributions-cs1009.json`)
- **Real** `return_targets`: `2.6.1`, `2.6.2`, `2.6.3`, `2.6.4`, `2.6.5`, `2.6.6`
- **Synthetic** Twin evidence ingested through the real `StudentTwinEngine` + queried through the real `DailyLoopLearnerTwinQueryAdapter`

Assumed coverage: `2.6.1`–`2.6.5` covered; `2.6.6` not covered.

| Topic | Covered | `evidence_count` | EK (adapter) | Eligible (≥3 evidence + covered + EK)? |
|-------|---------|------------------|--------------|----------------------------------------|
| 2.6.1 | yes | 5 | 0.410 | yes |
| 2.6.2 | yes | 4 | 0.092 | yes |
| 2.6.3 | yes | 3 | 0.254 | yes |
| 2.6.4 | yes | 1 | 0.098 | no (below floor) |
| 2.6.5 | yes | 0 | none | no (no Twin EK) |
| 2.6.6 | no | 0 | none | no (uncovered) |

**Block weakness score** = mean EK of eligible topics = `(0.410 + 0.092 + 0.254) / 3` ≈ **0.252**.

Among packages that had at least one eligible topic, this package would compete on that score; packages with no eligible topics would be skipped. If *no* package had any eligible topic, Policy V1 would SAFE_FALLBACK to Policy V0 new-material progression.

### 4. Conflict check with Phase 2 / M0 — Policy V0 untouched; `exam_date` still missing on the request

| Check | Finding |
|-------|---------|
| This milestone | **Design-only.** No application code changes. Policy V0 (`app/application/adaptive_decision/policy_v0.py`), orchestrator, Runtime C selection, and Twin ports are unmodified by this document update. |
| Phase 2 Twin canonicality | Compatible. Policy V1 is specified to read EK only via `LearnerTwinQueryPort`; no legacy mastery path. |
| M0 Decision Engine boundary | Compatible. Same `decide_daily_sitting` / `SittingDecision` / three outcomes (`ADAPTIVE` / `SAFE_FALLBACK` / `BLOCKED`). Orchestrator today still forbids `ADAPTIVE` under Policy V0 only — that gate is policy-id behaviour for implementation, not a type-system conflict. |
| Runtime C review today | Confirmed absent: Policy V0 wraps linear `compute_daily_sitting_selection` only; no revision/review branch on the sole-runtime path. Introducing review is new policy behaviour, not a wrap of an existing Runtime C consolidation selector. |
| Cadence precedent | Runtime A `PlanningService._consolidation_cadence` still implements the 4 / 3 / 2 new-topic bands at >60 / 30–60 / <30 days — the bands this design reuses. (The design’s “tightens continuously” prose is aspirational relative to those discrete bands; the bands themselves are what exists and is validated on the other runtime.) |
| `DailySittingRequest.exam_date` | **Still holds.** `DailySittingRequest` (`types.py`) fields remain only `user_id`, `subject_code`, `mission_date`, optional `curriculum_identity`. Adaptive-decision package has **zero** `exam_date` references. `EnrolmentSnapshot.exam_date` exists on Runtime C enrolment DTOs; `SittingDecisionOrchestrator` loads enrolment for `curriculum_identity` only and does not pass exam date into the request. Exam-proximity cadence therefore still requires extending `DailySittingRequest` (and the orchestrator wiring) at implementation time. |

**No conflict** that would invalidate this block-level Policy V1 design relative to shipped Phase 2 or M0. Remaining implementation prerequisites (already known): surface or re-read `return_targets`; extend `DailySittingRequest` with `exam_date`; replace Policy V0 internals behind the same engine interface when a separate brief authorizes code.

---

## Document control

| Field | Value |
|-------|-------|
| Authoring mode | Final design + verification — **do not implement from this file alone** |
| Supersedes | Earlier per-topic Consolidation draft at this same path (commit `dcbf6b72`) |
| Next step | Scoped implementation brief only if authorized |
