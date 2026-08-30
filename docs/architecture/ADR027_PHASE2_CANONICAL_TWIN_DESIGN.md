# ADR-027 Phase 2 — Canonical Learner Twin / Estimated Knowledge Design

**Status:** Accepted design for Phase 2 implementation — authorizes the **design only**; does **not** authorize code changes, flag flips, schema drops, or commits (implementation requires a separate scoped brief)  
**Governing ADR:** [`docs/adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md`](../adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md)  
**Nature:** Implementation design under ADR-027 (not a new ADR)  
**Date:** 2026-08-30  
**Verified against:** current working tree (Stage A `TopicProgress` / `AdaptiveLearningService`, `StudentTwinEngine` daily-loop, SDT-001 `SdtMasteryRecord` / `StudentReasoningService`, Runtime C `get_estimated_knowledge_inputs`, M0 `adaptive_decision/`, founder Twin diagnostics)  
**Predecessor:** Phase 2 scoping investigation (Approach 1 — adopt Twin B as canonical; retire A and C write paths; disposable production data authorized)  
**Sibling design:** [`docs/architecture/ADR027_M0_DECISION_BOUNDARY_DESIGN.md`](ADR027_M0_DECISION_BOUNDARY_DESIGN.md) (accepted M0 / Policy V0 boundary)

---

## Document purpose

Phase 2 establishes a **single authoritative Learner Twin** that owns Estimated Knowledge (EK) as core state, so architectural trustworthiness (single writer, no unexplained divergence, working drift detector) becomes achievable **before** real external students exist.

Phase 2 does **not**:

- Introduce a genuinely adaptive (knowledge-driven) Decision Engine policy (that remains V1+)  
- Change Policy V0 / M0 behavioural wrap of linear Runtime C selection  
- Author, edit, or restructure educational content  
- Preserve or migrate existing production Twin / mastery / progress estimate rows (explicitly disposable per founder authorization)

**Success criterion (binding):**  
*Is there one Learner Twin that owns Estimated Knowledge, with Study Progress kept separate, every former A/C reader either repointed or retired by plan, and a concrete drift detector that can fail closed on architectural inconsistency?*

---

## Placement rationale

Same convention as M0: implementation designs under accepted ADRs live in `docs/architecture/`; the ADR itself remains in `docs/adr/`.

Suggested filename if accepted without rename:  
`docs/architecture/ADR027_PHASE2_CANONICAL_TWIN_DESIGN.md`.

---

## Hard guardrail — student runtime data only (content boundary)

### Rule (binding)

This design, and any future implementation brief derived from it, may touch **only student-specific runtime data**:

| Allowed (student runtime) | Forbidden (educational content) |
|---------------------------|----------------------------------|
| Per-student mastery / EK scores | Anything under `app/curriculum/data/educational_packages/` |
| Twin documents (`sdt.daily_loop_twin`, Twin domain state) | Anything under `app/curriculum/data/educational_campaigns/` |
| Progress / coverage records (`TopicProgress`, Runtime C progress events) | Syllabus authoring JSON under `app/curriculum/data/` used as **content source of truth** (e.g. `ifoa/cs1/2026.json` package trees) |
| Founder diagnostics that read/write **student Twin state** | Package loaders, campaign editors, CIP **authoring**, curriculum import **content** mutations |

Stacks in scope are **A / B / C / D** only (defined below). Content authoring and storage paths are out of scope forever for this programme.

### How verified (2026-08-30 re-check)

1. **Stack A writers/readers** (`AdaptiveLearningService`, `LearningService`, `StudySessionService`, `ReadinessService`, `RecommendationService`, `mission_optimizer`, `analytics_service`, `planning_service`, `learning_lifecycle_service`, `EducationalContinuityService` estimate copy) — no imports of `educational_packages`, `educational_campaigns`, or filesystem reads of `curriculum/data/` authoring trees. They use ORM `Topic` / `CurriculumService` (imported DB projection) only.  
2. **Stack B** (`StudentTwinEngine`, `session_evidence_consumer`, `daily_loop_codec`, `DailyLoopTwinPersistence`) — consumes session evidence package metadata (`topic_id`, scores); does not load package JSON or campaign trees. Persistence namespace is `sdt.daily_loop_twin` via `SessionDocumentStore`.  
3. **Stack C** (`StudentReasoningService`, `DecisionGenerator`, `TwinUpdater`, `TwinPersistenceService`, `SdtMasteryRecord`) — persists to SDT SQL; CIP retrieval (when used for gaps) reads **imported CIP corpus tables**, not package/campaign authoring paths. No student hot-path dependency on content trees.  
4. **Stack D** (`StudyPlanService` wizard sync, baseline coordinator, mission completion `completed=True`) — writes `TopicProgress.completed` only; no content-tree I/O.  
5. **Where content *does* live** (orthogonal): `app/application/educational_packages/loader.py` → `curriculum/data/educational_packages` — used by Runtime C composition / Home chrome, **not** by A/B/C/D mastery writers.

**Edge case (allowed):** reading **imported** curriculum projection (`topics` ORM rows, Runtime C artefacts already loaded for enrolment, CIP entity ids already in DB) to *key* student state is not content authoring. Phase 2 must not add writers into package/campaign/syllabus JSON.

Any implementation PR that edits files under `educational_packages/`, `educational_campaigns/`, or curriculum authoring JSON for Phase 2 is **out of scope and must be rejected**.

---

## Four stacks (re-verified baseline)

| Stack | Store | Scale | Identity today | Live student hot path? |
|-------|-------|-------|----------------|------------------------|
| **A** | SQL `topic_progress.mastery_score` (+ `average_accuracy` gates `has_estimated_knowledge`) | 0–100 | `int` `topics.id` | **Yes — current EK authority for Stage A surfaces** |
| **B** | Opaque doc `sdt.daily_loop_twin` via `StudentTwinEngine` | 0–1 | `str` session / package `topic_id` | **No — `SR_TWIN_DAILY_LOOP=0` in `render.yaml`** |
| **C** | SQL `mastery_records` (`SdtMasteryRecord`) | 0–1 | `str` `concept_id` | **No — founder / diagnostics / certification only** |
| **D** | SQL `topic_progress.completed` (+ Runtime C event-sourced `completed_topic_ids`) | bool / coverage | A: `int` FK; Runtime C: `str` | **Yes — Study Progress only; not EK** |

Authoritative write for A: `AdaptiveLearningService.update_mastery_after_attempt` (from `LearningService` / `StudySessionService` after Educational Evidence Authority acceptance). Continuity remap may copy estimate fields (`EducationalContinuityService`) — also in retirement scope for EK fields.

---

## 1. Target state

### 1.1 Canonical Learner Twin = Stack B (`StudentTwinEngine`)

**Confirm:** `StudentTwinEngine` + daily-loop persistence (`DailyLoopTwinPersistence` / `sdt.daily_loop_twin`) becomes the **canonical Learner Twin** under ADR-027.

- The Knowledge Engine for Phase 2 **is** the Twin’s evidence ingest + deterministic recalculation path (`SessionTwinEvidenceConsumer` → `StudentTwinEngine.ingest_*` / `recalculate`), writing **directly into Twin-owned state**.  
- There is **no** independent EK store that the Twin must sync from.  
- Scale for EK / Estimated Mastery inside the Twin remains **0–1** (domain already enforces unit interval). Presentation layers may format as percent for students; storage and Twin APIs stay 0–1.  
- Existing production documents and Stage A / SDT estimate rows are **disposable** — no migration of historical scores into the new canonical Twin.

### 1.2 What “retire” means for A and C

Given clean-slate cutover (no real external students; founder dogfood disposable), prefer **delete write authority immediately** and **remove schema soon after reader cutover**, not a long dual-store deprecation theatre.

| Artefact | Recommendation | Rationale |
|----------|-----------------|-----------|
| **A — `TopicProgress.mastery_score` writes** | **Retire immediately** in the implementation PR: stop calling `update_mastery_after_attempt` for EK; remove / no-op estimate mutations; continuity copy of estimate fields stops | Single-writer rule; disposable data |
| **A — `average_accuracy` / `has_estimated_knowledge` on TopicProgress** | **Retire as EK gate** with mastery_score; do not keep a second evidence-backed EK channel on this table | Same |
| **A — columns `mastery_score`, `average_accuracy` (and EK-derived use of `current_stage` for mastery thresholds)** | **Deprecate in code in the same cutover**; **drop columns in a follow-up Alembic** once readers are Twin-backed and tests updated | Cleanest long-term; avoid zombie columns that invite accidental writes. Keep table itself for Study Progress (see §2) |
| **A — AdaptiveLearningService EK helpers** (`get_weak_topics`, `get_mastered_topics`, snapshot mastery ordering) | **Repoint or delete** once Twin Query API exists; do not leave “temporary” SQL mastery queries | Prevent silent reintroduction of Stack A authority |
| **C — `DecisionGenerator` / `TwinUpdater` / `reason()` → `SdtMasteryRecord` writes** | **Retire as EK authority**; stop treating SDT SQL mastery as belief about the student | Not on student hot path today, but still a second writer if left alive |
| **C — SQL tables `mastery_records` (+ related SDT inference tables written only for parallel belief)** | **Keep schema short-term** (founder tooling may still open rows); **drop or empty after founder surfaces repoint (§6)** | Clean-slate allows drop; soft-delete-first avoids breaking founder routes mid-cutover |
| **C — Learning Graph projections refreshed only by the full `reason()` cycle** | **Out of Phase 2 EK authority**; do not silently promote graph projections as EK. Founder graph diagnostics stay diagnostic until a separate programme owns them | Avoid inventing a fourth EK store |

**“Retire” does not mean:** delete `TopicProgress` as a table, delete Study Progress writers, or delete `StudentTwinEngine`.

**“Retire” does mean:** zero production writers to A’s EK fields and C’s mastery belief tables as sources of truth; readers cut over to Twin; schema cleanup follows.

### 1.3 Disposable-data posture (authorized)

Founder has authorized treating current production data in A/B/C estimate stores as disposable. Therefore:

- No dual-run reconciliation of old A vs B vs C scores.  
- No backfill from `TopicProgress.mastery_score` into Twin documents.  
- Optional one-shot wipe of existing `sdt.daily_loop_twin` docs and/or `mastery_records` at cutover is acceptable (operator step, not required for design acceptance).  
- Fresh Twin state begins from the next authorised Educational+ evidence after `SR_TWIN_DAILY_LOOP` resumes (§8).

---

## 2. Study Progress (D) stays separate

### 2.1 Principle (ADR-027, binding)

Study Progress (whether a student has **covered** a topic) and Estimated Knowledge (what the system **believes they understand**) remain **two genuinely separate concepts**, each with its own writer and meaning. Neither may proxy for the other.

Wizard / baseline declaration already encodes this (`StudyPlanService` initializes completed topics with `mastery_score=0.0` and never mints EK from declaration). Mission completion can set `completed=True` without writing mastery. Runtime C coverage uses event-sourced `TOPIC_COMPLETED` / `derive_progress`, independent of Stage A EK.

### 2.2 Recommendation

**Keep Study Progress on its existing durable writers; do not move it into the Twin’s EK maps; expose it as a Twin-*answered* facet via the Query API.**

| Concern | Decision |
|---------|----------|
| **Where Study Progress lives** | **Keep** `TopicProgress.completed` (and related non-EK progress fields: e.g. `last_reviewed`, `revision_count` as activity metadata) for Stage A / wizard / continuity. **Keep** Runtime C event-sourced `completed_topic_ids` as Study Progress for published-curriculum students. |
| **Does Twin “own” Study Progress inside the daily-loop document?** | **Not as EK.** Phase 2 does **not** require stuffing `completed` into `estimated_knowledge`. Optionally, a later additive Twin document facet `study_progress` may **cache** coverage for answer convenience — but its **writer** must remain Progress writers, never the Knowledge Engine. |
| **TopicProgress table** | **Keep alive** for Study Progress (and non-EK scheduling fields still used by Stage A). **Remove EK authority** from it (§1). |
| **Readiness “coverage” vs “avg mastery”** | Coverage continues to use Study Progress (`completed` / Runtime C coverage). Average EK uses Twin Query API only. |

### 2.3 Why not fold Study Progress fully into the Twin document in Phase 2?

1. Runtime C already has a working, event-sourced Study Progress spine for the live CS1 Home path — collapsing it into Twin persistence in the same programme as EK cutover mixes two risk surfaces.  
2. Wizard declaration and Stage A `get_next_incomplete_topic` already speak `TopicProgress.completed`.  
3. ADR requires separation of **writers**; a Twin Query facade that answers “is this covered?” by reading Progress stores satisfies “Twin answers questions” without collapsing writers into the Knowledge Engine.

**Rejected alternative:** using Twin EK (or lack of EK) as a substitute for coverage — forbidden by ADR and by existing EIP-001 / IA-004 honesty.

---

## 3. Topic identity mapping

### 3.1 Mismatch (re-verified)

| Stack | Key type | Example |
|-------|----------|---------|
| A | `int` FK `topics.id` | `42` |
| B / Runtime C | `str` published topic id | `CS1-A-T01` (from curriculum JSON `sections[].topics[].id` / progress model) |
| C | `str` `concept_id` / `curriculum_entity_id` | CIP / observation concept reference (not guaranteed equal to published topic id) |

No production helper today maps A ↔ B ↔ C in one place. Package JSON also carries human `topic_code` (e.g. `1.1`) and sometimes `topic_id` — student chrome must not treat internal `node-…` ids as syllabus identity (MISSION-002).

### 3.2 Canonical identity going forward

**Canonical Learner Twin topic key = published curriculum string topic id**  
(e.g. `CS1-A-T01`), i.e. the same string space Runtime C `progress_model.topic_ids` and session evidence already use.

| Non-canonical | Treatment |
|---------------|-----------|
| ORM `topics.id` (int) | **Surrogate only.** Resolve to canonical string at the Twin Query / ingest boundary. Never store int FKs inside Twin EK maps. |
| Human syllabus `code` (`1.1`) | Display / chrome only — **not** the Twin key (codes can collide across papers / remaps). |
| Stack C `concept_id` | **Not** the Phase 2 Twin key. Founder/CIP concepts may later map *onto* canonical topic ids via an explicit adapter; they must not silently redefine Twin keys. |
| Internal `node-…` ids | Forbidden as Twin keys and as student-facing identity. |

### 3.3 Establishing the standard (clean-slate, not id migration)

1. **Ingest:** `SessionTwinEvidenceConsumer` already prefers observation / package `topic_id` strings — keep and harden: reject / ignore blank or `node-` keys; require canonical published ids on Educational+ observations that update the Twin.  
2. **Mapping helper (new, student-runtime only):** e.g. `CanonicalTopicId.resolve_from_orm_topic(topic: Topic) -> str` and `resolve_from_runtime_topic_id(topic_id: str) -> str`, implemented against **imported** curriculum projection / Runtime C artefacts — **not** by editing syllabus JSON. If ORM `Topic` lacks a durable official string id column today, Phase 2 implementation must use the existing import/artefact join the product already relies on for Runtime C (or add a **projection** column populated by curriculum import — that is schema on `topics`, still not content authoring). Exact join is an implementation detail for the brief; the **standard** is string published id.  
3. **Stage A readers:** when calling Twin Query with historically int-keyed loops, convert at the edge once, then query by canonical id.  
4. **No migration** of old Twin documents keyed by inconsistent strings — wipe or ignore (disposable).  
5. **Do not** invent a fourth parallel key space.

---

## 4. Reader cutover

### 4.1 Live / production-relevant readers of Stack A EK (re-verified)

| Consumer | What it reads today | Cutover proposal |
|----------|---------------------|------------------|
| **`ReadinessService`** | `TopicProgress.mastery_score` where `has_estimated_knowledge`; weak/strong topic lists; composite score’s 30% EK component | Read EK via Twin Query API (`estimated_knowledge_for_user`, weak topics by Twin EK). Keep coverage from Study Progress (`completed` / Runtime C). |
| **`RecommendationService`** | Indirect via Readiness weak topics / coverage / overall readiness | No direct Twin coupling required if Readiness is cut over; verify no residual `mastery_score` assumptions in tip copy thresholds. |
| **`mission_optimizer`** | `AdaptiveLearningService.get_weak_topics` / due-review → `mastery_score` | Repoint weak-topic selection to Twin Query; or mark optimizer deprecated-unused if already off sole-runtime Home (still remove A dependency so it cannot resurrect Stack A). |
| **`analytics_service`** | Sums / averages `p.mastery_score` | Repoint averages to Twin overall / per-topic EK; empty Twin ⇒ honest “no estimate” not `0` pretending to be evidence. |
| **`planning_service`** | `determine_stage(progress.mastery_score)` for consolidation weak-topic pick | Use Twin EK (0–1) with explicit stage policy adapter; do not keep Stage A score as authority. |
| **`learning_lifecycle_service`** | Orders by `TopicProgress.mastery_score` | Twin weak-ordering API. |
| **`AdaptiveLearningService` query helpers** | Direct SQL on `mastery_score` | Delete or thin-wrap Twin Query after write retirement. |
| **Templates** (`study_plan/view.html`; legacy `dashboard/index.html`, `analytics/index.html`) | `has_estimated_knowledge` + displayed `%` | Gate on Twin “has evidence-backed EK for topic”; format Twin 0–1 as percent. Prefer sole-runtime student templates; legacy Contained shells only if still reachable. |
| **`EducationalContinuityService` estimate field copy** | Copies `mastery_score` across remaps | Stop copying EK fields; Twin rebuilds from evidence after remap (or subject-scoped Twin key includes curriculum identity — open if multi-version remap must preserve Twin docs). |
| **`settings` export / readiness print** | `avg_mastery` from Readiness | Follows Readiness cutover. |
| **Runtime C `get_estimated_knowledge_inputs`** | Stub always `has_estimated_knowledge: False` | Become real Twin-backed API (§5). |
| **Intelligence / session presentation** | Readiness / Recommendation surfaces | Inherit cutover; no new A reads. |

**Not Stack A EK (leave alone as Study Progress):** `TopicProgress.completed` readers (`get_next_incomplete_topic`, readiness coverage, wizard sync, journey mappers that use completion status).

**Not student hot-path Stack A:** Stack C founder routes, certification harnesses — handled in §6.

### 4.2 Twin Query interface (“Twin answers questions”)

ADR-027: the Twin answers questions about a learner; it does **not** rank, weigh, prioritise, or recommend.

Propose a narrow **Learner Twin Query Port** (name illustrative) living beside Twin persistence — e.g. `app/application/student_twin/query.py` — with **read-only**, deterministic methods:

```python
@dataclass(frozen=True)
class TopicKnowledgeFact:
    topic_id: str                    # canonical published id
    has_estimated_knowledge: bool    # evidence admitted for this topic
    estimated_knowledge: float | None  # 0–1 when has_… else None
    estimated_mastery: float | None    # 0–1; Twin-internal; not a decision score
    evidence_count: int
    last_practised_at: datetime | None  # fact, if Twin retains it

@dataclass(frozen=True)
class LearnerKnowledgeSnapshot:
    user_id: int
    subject_code: str
    curriculum_identity: str | None
    overall_estimated_knowledge: float | None
    topics: tuple[TopicKnowledgeFact, ...]

class LearnerTwinQueryPort(Protocol):
    def knowledge_snapshot(
        self, *, user_id: int, subject_code: str
    ) -> LearnerKnowledgeSnapshot: ...

    def topic_knowledge(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> TopicKnowledgeFact: ...

    def topics_with_estimated_knowledge(
        self, *, user_id: int, subject_code: str
    ) -> tuple[TopicKnowledgeFact, ...]: ...

    # Study Progress answered without collapsing into EK:
    def topic_covered(
        self, *, user_id: int, subject_code: str, topic_id: str
    ) -> bool: ...
```

**Rules for this port:**

- Load Twin via `DailyLoopTwinPersistence` + `decode_daily_loop_twin` (or engine reload from retained evidence events if that becomes the source of truth).  
- `has_estimated_knowledge` is true only when Twin has admitted authorised evidence for that topic — **not** when Study Progress is complete.  
- **Forbidden on this port:** urgency scores, recommendation ranks, “study next”, priority weights, readiness composite scores. Those stay in Decision Engine / Readiness policy consumers.  
- Weak-topic **lists for UI** may sort by EK ascending as a **presentation of facts** (ordering by a fact is still answering “what is low?”); they must not encode mission selection policy. Mission selection remains M0/V1 Decision Engine territory.

Existing Twin-internal helpers (`WeaknessAnalyser`, Twin `RecommendationService`) are **not** automatically promoted to student hot-path authority; Phase 2 prefers the narrow Query Port above to avoid sneaking policy into the Twin.

---

## 5. Runtime C EK API fix

### 5.1 Current stub (verified)

`EducationalRuntimeEngineService.get_estimated_knowledge_inputs` always sets `has_estimated_knowledge: False`, `mastery_score: None`, `average_accuracy: None` for every topic. Attached to `RuntimeJourneySnapshot` but **not consumed** by `EducationalExperienceService._project()` today — so Home/Journey do not yet show Runtime C EK.

### 5.2 Proposed behaviour

Make the method a **real adapter** over `LearnerTwinQueryPort`:

- For each Runtime C `topic_id` (already canonical strings), query Twin.  
- Map Twin 0–1 → DTO fields honestly:  
  - `has_estimated_knowledge` ← Twin fact  
  - `mastery_score` ← **presentation scalar**: either keep `None` + add `estimated_knowledge_0_1`, or document that Runtime C DTO’s `mastery_score` means **0–100 display** derived as `round(ek * 100, 1)` when present — pick one in implementation and update certification tests that currently assert the stub. Prefer renaming in DTO comments to “Estimated Knowledge display” to avoid Stack A connotations.  
- `completed` continues to come from Runtime C `derive_progress` (Study Progress), **not** from Twin EK.

### 5.3 Callers / tests

- Update `tests/application/educational_runtime_engine/test_integration.py` and `tests/certification/test_cs10_cs11_inputs.py` that pin the stub.  
- Journey projection may begin surfacing EK only when product copy is ready; wiring the API real does **not** by itself require new student chrome — but lying stubs must end.

---

## 6. Stack C founder / diagnostic surfaces

Do **not** silently break founder tooling.

### 6.1 Surfaces (verified)

| Surface | Role today | Phase 2 plan |
|---------|------------|--------------|
| `/founder/twin` | CRUD Twin, observations, reason(), mastery display against **SDT SQL** | **Repoint reads** of “what does this student know?” to **canonical Twin Query (B)**. Manual observation → reason() write path either **retired** or rewritten to ingest into `StudentTwinEngine` (preferred long-term). Short-term: label SDT SQL mastery as **legacy diagnostic sandbox**, not student authority. |
| `/founder/reasoning` | Runs `StudentReasoningService.reason` | Same — either repoint to B Knowledge Engine or mark sandbox-only with banner. |
| `/founder/assessment` pipeline | Ingest can refresh SDT inferences | Stop writing student-authoritative EK to `SdtMasteryRecord`; optional sandbox mode. |
| `/founder/tutor`, `/founder/missions`, `/founder/learning-graph` | Twin-first / graph diagnostics | Read Twin B where they need EK; graph remains non-authoritative for EK. |
| `EducationalPipelineOrchestrator` + DecisionGenerator chain | **Not wired** to student Home | Keep as **test/cert harness** until rewritten against Twin B, or quarantine behind explicit “legacy SDT sandbox” naming. |
| `tests/certification/educational_intelligence/*` | CI purity / pipeline cert | Update expectations when SDT mastery authority is retired; do not drop educational-intelligence CI without a replacement assertion that Twin B is sole EK writer. |
| Student tutor soft-fail paths | Optional Twin presence | Point at Twin B documents when present. |

### 6.2 Recommendation

1. **Primary:** Founder “student knowledge” views **repoint to Twin B**.  
2. **Secondary:** Retain SDT SQL + DecisionGenerator as an **explicitly labelled sandbox** for Epic-2 reasoning experiments until a separate programme deletes them — **zero** claim that sandbox mastery is production EK.  
3. **Do not** leave two founder buttons that write different EK stores without labelling.  
4. Schema drop of `mastery_records` only after founder repoint + cert suite update (§1).

---

## 7. Drift detector (concrete)

ADR-027 requires a working drift detector for **architectural** trustworthiness (single writer, no unexplained divergence). With one canonical store, the detector is **not** “diff A vs B vs C forever.”

### 7.1 What to check (Phase 2)

| Check | Mechanism | Failure meaning |
|-------|-----------|-----------------|
| **D1 — Replay determinism** | Reload Twin from ordered admissible evidence events; re-run `StudentTwinEngine.recalculate`; compare `estimated_knowledge` / `estimated_mastery` maps and overall scores to persisted daily-loop document (tolerance = exact float round-trip used by codec, e.g. 6 d.p.) | Twin document diverged from Knowledge Engine — corruption or non-engine write |
| **D2 — Single-writer sentry** | CI / runtime assert: no writes to `TopicProgress.mastery_score` / `average_accuracy` from application services except an explicit deny-list of zero; no production path calls `TwinPersistenceService.replace_inferences` for student-authoritative EK | Stack A/C writer regression |
| **D3 — Identity hygiene** | Twin topic keys ⊆ canonical published ids for the student’s curriculum identity; reject `node-` / blank / pure-int keys in Twin maps | Identity drift |
| **D4 — Study Progress ≠ EK** | Invariant test: topics with `completed=True` (or Runtime C completed) and **no** Twin evidence must have `has_estimated_knowledge=False` | Honesty collapse |
| **D5 — Scale** | All Twin EK/mastery values ∈ [0, 1] | Codec / adapter bug |

### 7.2 What not to build as “the” ADR-027 detector

- Shadow soak monitors (`TwinDriftDetectionMonitor`, adaptive/strategy shadow drift) — observational Epic-2 telemetry; **not** EK authority reconciliation.  
- Diffing disposable legacy A/C rows against Twin after cutover — waste; optional one-time wipe instead.  
- Pedagogical calibration (“does EK predict exam pass?”) — explicitly **later**, needs real learners.

### 7.3 Where it runs

- **CI:** deterministic replay fixtures + single-writer grep/architecture guardian rules.  
- **Ops (optional):** founder diagnostic “replay Twin and show drift” button using D1.  
- Failures must be **visible** (test fail / founder alert), not silent self-heal that hides a second writer.

---

## 8. Resuming `SR_TWIN_DAILY_LOOP`

### 8.1 Current hold (verified)

`render.yaml` sets `SR_TWIN_DAILY_LOOP=0` (ADR-027 hold, 2026-08-30). `SessionTwinEvidenceConsumer` returns `ignored("twin_daily_loop_flag_off")` when OFF. Session evidence packages still persist and remain replayable. Resume instructions already exist in `docs/production/VERSION_1_FLAG_MATRIX.md` §2.1.

### 8.2 Conditions to turn the flag back ON

All of the following — **deliberate later operator step**, **not** part of accepting this design document:

1. Canonical **write path** is Twin B only (A EK writes retired; C not student-authoritative).  
2. **Reader cutover** complete for §4 consumers that ship in the same release train (at minimum Readiness EK component + Runtime C `get_estimated_knowledge_inputs` + no live template still claiming Stage A EK as authority).  
3. **Drift detector** D1–D5 exist at least in CI.  
4. **Founder plan** from §6 is either repointed or explicitly sandboxed with labels.  
5. Optional: wipe stale Twin docs so resume starts clean.  
6. Update `VERSION_1_FLAG_MATRIX.md` resume record; remove or set `SR_TWIN_DAILY_LOOP=1` in `render.yaml`; **redeploy** when deploys resume.

### 8.3 Explicit non-action of this proposal

This design document **does not** flip `SR_TWIN_DAILY_LOOP`. Implementation may land code paths behind the existing flag; production remains OFF until the checklist above is signed off.

---

## 9. Flag / rollout strategy

### Context

- Production deploy is manual and was paused when the Twin hold was recorded.  
- Production estimate data is disposable — dual-run of A and B writers adds cost without preserving value.  
- M0 already established the pattern of default-OFF flags for behaviour boundaries.

### Recommendation (reasoned, not “always flag”)

**Do not dual-run EK writers.** On implementation merge: Stage A EK writes stop; Twin is the only Knowledge Engine target (still gated by `SR_TWIN_DAILY_LOOP` for *consumption*).

**Do use a short-lived reader cutover flag** for Stage A surfaces that today read `TopicProgress.mastery_score`, e.g. `KWALITEC_ADR027_PHASE2_TWIN_EK_READS` (name illustrative):

| Mode | Writers | Readers |
|------|---------|---------|
| Flag OFF (default at merge) | Twin-only path prepared; A EK writes already removed or no-op | Keep temporary “no EK / empty” honest behaviour **or** keep reading A only if A writes not yet removed — prefer **not** to leave A writes alive |
| Preferred merge sequence | (1) land Query Port + tests, (2) stop A/C authoritative writes, (3) flip reader flag ON in non-prod, (4) resume `SR_TWIN_DAILY_LOOP`, (5) production reader flag ON | Instant kill-switch on reader flag if Twin reads misbehave |

**Why not a pure unflagged cutover?** Reader bugs (wrong identity mapping, percent scale mistakes) can still ship even with disposable data; a reader flag is cheap reversibility without resurrecting multi-writer drift.

**Why not dual-write A+B?** Re-creates the ADR’s synchronisation problem and wastes the clean-slate authorization.

**Direct cutover without any new flag** is acceptable only if implementation ships in one tightly tested PR **and** `SR_TWIN_DAILY_LOOP` remains OFF until soak — i.e. students see “no EK” briefly rather than wrong EK. Still update the flag matrix. Prefer the reader flag if the PR touches Readiness/templates.

---

## 10. Relationship to M0

### Confirmed: no conflict; Policy V0 stays Twin-free

M0 (`ADR027_M0_DECISION_BOUNDARY_DESIGN.md` + `app/application/adaptive_decision/`) wraps Runtime C daily sitting selection behind `AdaptiveDecisionEngine` / `SittingDecisionOrchestrator` with **Policy V0** = existing linear / campaign progression. Acceptance requires **no Twin/EK-driven branches**.

Re-verified: `adaptive_decision/` has **zero** imports of Twin, `TopicProgress`, mastery, or SDT packages. Policy V0 calls `compute_daily_sitting_selection` (enrolment, `derive_progress`, PB-002, certified overlay) only.

| Question | Answer |
|----------|--------|
| Does Phase 2 require M0 redesign? | **No.** |
| Does Phase 2 change Policy V0 inputs? | **No.** Policy V0 remains without Twin/EK dependency. |
| When may Decision Engine consume Twin? | **V1+ adaptive policy**, explicitly after M0 instrumentation and Phase 2 Twin trustworthiness. |
| Can Phase 2 and M0 flag land independently? | **Yes.** Orthogonal flags: `KWALITEC_ADR027_M0_DECISION_BOUNDARY` vs Twin daily-loop / Phase 2 reader flag. |

Phase 2 enables the **data plane** ADR-027 needs before adaptive policy; M0 remains the **decision boundary** with honest `SAFE_FALLBACK` until then.

---

## 11. Open questions

Requiring product / architectural judgment (not further code archaeology):

1. **Study Progress facet storage:** Confirm §2 recommendation (Progress writers stay; Twin Query answers coverage) vs accelerating an in-document Twin `study_progress` cache in the same implementation train.  
2. **ORM official string id:** Prefer artefact/import join only vs adding a durable `topics.official_id` (or equivalent) projection column for int→canonical resolution — still student-runtime schema, but touches curriculum **import** codepaths; confirm appetite.  
3. **Stack C sandbox lifetime:** How long may labelled SDT SQL sandbox remain before mandatory drop? (Affects founder UX and cert suite.)  
4. **Reader flag vs single-PR cutover:** Confirm §9 preference for `KWALITEC_ADR027_PHASE2_TWIN_EK_READS` vs accepting a brief global “no EK displayed” window with no new flag.  
5. **Runtime C DTO shape:** Keep `mastery_score` as 0–100 display field vs introduce explicit `estimated_knowledge` 0–1 on `EstimatedKnowledgeRuntimeInputs` (breaking cert tests either way — choose the clearer student-meaning name).  
6. **Continuity / curriculum version remap:** When syllabus remap occurs, is Twin document keyed by `(user, subject, curriculum_identity)` and discarded on remap, or replayed from evidence against new topic ids? (Disposable data makes discard acceptable initially.)  
7. **Scope of template cutover:** Sole-runtime student templates only vs also legacy Contained `dashboard/` / `analytics/` shells still reachable under redirects.

### Resolution (chief architect review — accepted)

Reviewed and accepted. The seven open points are resolved as follows:

1. **Study Progress facet storage:** Keep narrowly scoped to EK for this phase; do not accelerate an in-document Twin `study_progress` cache in the same implementation train. That remains a legitimate future enhancement, not required now.
2. **ORM official string id:** Prefer the artefact/import join only, not a new durable `topics.official_id` column, for now. Revisit only if the join proves fragile in practice.
3. **Stack C sandbox lifetime:** Give it a concrete end date rather than leaving it open-ended — retained through Phase 2 implementation plus one subsequent review cycle, then removed unless a separate initiative explicitly claims it.
4. **Reader flag vs single-PR cutover:** Use the reader flag (`KWALITEC_ADR027_PHASE2_TWIN_EK_READS` or equivalent). Cheap reversibility is worth the small overhead, consistent with M0's ship-dark philosophy.
5. **Runtime C DTO shape:** Introduce an explicit new `estimated_knowledge` 0–1 field rather than overloading the legacy `mastery_score` name. Clearer student-meaning naming; avoids resurrecting Stage-A-flavored baggage on a field meant to represent the new canonical source.
6. **Continuity / curriculum remap:** Discard Twin documents on remap, given the disposable-data authorization already in force. Replay-from-evidence-after-remap is a legitimate future refinement, not needed now.
7. **Template cutover scope:** Sole-runtime student templates only. Legacy `dashboard/` / `analytics/` shells are out of scope unless someone confirms they are still actually reachable.

---

## Suggested implementation touch list (future Agent brief — not authorized)

When (and only when) this proposal is accepted, a subsequent brief should limit edits approximately to:

| Create / extend | Modify | Must not touch |
|-----------------|--------|----------------|
| `LearnerTwinQueryPort` + Twin query adapter | `AdaptiveLearningService` (retire EK writes) | `educational_packages/`, `educational_campaigns/`, syllabus authoring JSON |
| Drift detector tests (D1–D5) | `ReadinessService`, analytics, planning, lifecycle, mission_optimizer readers | M0 Policy V0 logic (unless wiring flags only) |
| Canonical topic id helper (runtime projection) | Runtime C `get_estimated_knowledge_inputs` | New Educational Framework law |
| Flag matrix + optional reader flag | Founder Twin routes (repoint / sandbox labels) | Cap 2.8 live Home promotion |
| Alembic follow-up to drop A EK columns / later C tables | `session_evidence_consumer` identity hardening | Content loaders |

**Commit:** only when a later implementation brief / human explicitly asks.

---

## Acceptance criteria (for a future implementation — not this proposal)

Phase 2 implementation is done when:

1. Twin B is the only student-authoritative EK writer (when `SR_TWIN_DAILY_LOOP` ON).  
2. Stack A EK fields are unwitten; readers use Twin Query or show honest absence.  
3. Stack C is non-authoritative (sandbox or removed) with founder plan executed.  
4. Study Progress still uses Progress writers; invariants prove no EK minting from completion alone.  
5. Canonical string topic ids used in Twin maps; drift detector D1–D5 green in CI.  
6. Runtime C EK API is non-stub.  
7. Content boundary respected (no package/campaign/syllabus authoring edits).  
8. M0 / Policy V0 still Twin-independent.  
9. `SR_TWIN_DAILY_LOOP` resume is a separate, checklist-gated operator step.

---

## Document control

| Field | Value |
|-------|-------|
| Authoring mode | Proposal only — **do not implement from this file alone** |
| Commit | Committed as accepted Phase 2 design under ADR-027 (design authorization only; implementation not yet authorized — requires a separate scoped brief) |
| Supersedes | Nothing; implements the Learner Twin / EK slice of ADR-027 (Approach 1 clean-slate) |
| Does not supersede | M0 decision boundary design |
| Next step after acceptance | Scoped implementation brief with Goal + Touch List + mandated tests + explicit non-touch of content paths |
