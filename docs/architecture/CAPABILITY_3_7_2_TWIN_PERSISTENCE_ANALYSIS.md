# Capability 3.7.2 — Twin Persistence Analysis

**Status:** Analysis only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.7.2 Twin Persistence Analysis (educational-state contents of immutable Twin snapshots preceding repository design)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream Persistence architecture:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Upstream Calibration mapping:** [`CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md`](CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Scope:** Determine what educational state belongs inside a persisted Twin snapshot and what must remain derived — **no code, ORM, SQL, schemas, repository APIs, or storage technology**

---

## Document purpose

Capability 3.7.1 defined Twin Persistence architecture: durable storage of immutable Digital Twin snapshots. Persistence never creates Twins, never mutates Twins, and never performs educational reasoning.

This milestone analyses the **persistence model itself** — not how to store bytes, but **what educational state must be durable** so that Educational Intelligence remains truthful across sessions.

It answers:

> Exactly what educational state should be persisted as a Twin snapshot, and what should remain derived from that state?

It protects the binding principle:

> **The Digital Twin is the single source of educational truth. Everything else is reproducible.**

**Architectural restatement:**

> **Persist the Twin aggregate that authors produced. Regenerate every product judgement and presentation artefact from that Twin. Never promote derived outputs into competing learner truth.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Persisted Twin snapshot** | Complete immutable Digital Twin aggregate stored as durable educational state |
| **Educational state** | Twin-owned learner beliefs, anchors, lineage, and snapshot identity — not product cards or dashboard caches |
| **Derived artefact** | Any output reproducible from Twin + Curriculum + constraints via Educational Intelligence or presentation |
| **Current snapshot** | The single Twin designated current for a student / sitting scope on the product read path |
| **Historical snapshot** | A prior Twin that remains valid as what the product believed at that time |
| **Learning Evidence** | Append-only study history (separate from Twin Persistence; not analysed as storage technology here) |

**Non-goals of this document**

- Implementation, pseudocode, services, dataclasses, or package layouts  
- Flask routes, forms, templates, or UI copy  
- Database schemas, Alembic migrations, ORM models, SQL, or repository APIs  
- Persistence technology choices (engines, formats, caches, queues)  
- Redesign of Evidence, Twin domains, Update Strategies, Readiness, Decision, Recommendation, or Mission  
- Educational algorithms, scoring formulas, or recommendation selection  

---

# 1. Persistence philosophy

## 1.1 Why immutable snapshots over in-place mutation

Capability 3.7.1 established replace-by-snapshot as Persistence law. This analysis explains **why that law is educationally necessary**, not merely operationally convenient.

In-place mutation treats learner state as a mutable bag of fields. That model fails educational integrity for four structural reasons:

1. **Past beliefs become unrecoverable.** Once Knowledge is overwritten, the product cannot say what it believed when a prior recommendation was issued.  
2. **Authorship becomes invisible.** Field patches hide whether Calibration, Evidence → Strategies, or a “helpful” repository wrote the change.  
3. **Determinism collapses.** Consumers cannot pin a reproducible Twin identity; “the Twin” becomes whichever row last won a race.  
4. **Audit trails become theatre.** Decision Journal and explainability cite Twin factors that no longer exist in their cited form.

Immutable snapshots invert that model:

- Authors emit a **complete** Twin.  
- Persistence stores that Twin **whole**.  
- Evolution is expressed only by a **new** snapshot.  
- Prior snapshots remain historically true.

### Philosophy restatement

> **Learner state evolves by succession of wholes, not by silent edits of parts.**

## 1.2 Explainability

Explainable recommendations require citable Twin factors: coverage gaps, retention pressure, behavioural reliability, assessment lineage, goal constraints, warrant density.

Those citations are meaningful only if the Twin they refer to is **stable and reconstructible**.

| Mutation model | Explainability outcome |
|---|---|
| In-place edit | “Why this recommendation?” cites fields that may already have changed; warrants become retrospective fiction |
| Immutable snapshot | Recommendation / Decision can cite a specific Twin snapshot identity; factors remain inspectable as they were |

Persistence of the Twin snapshot — not of the recommendation card — is what keeps explainability honest. Cards are ephemeral; Twin state is the warrant spine.

## 1.3 Auditability

Auditability answers: *What did the product believe about this learner, when, and on what authorship path?*

Immutable snapshots provide:

- **Point-in-time belief** — each snapshot is a complete educational posture.  
- **Lineage** — birth → successors ordered by evolution events.  
- **Provenance survival** — Calibration `self_declared` markers and Evidence lineage ids remain attached to the snapshot that carried them.  
- **Non-repudiation of past honesty** — a prior sparse / empty Twin remains sparse; later Evidence does not rewrite yesterday’s silence into Mid theatre.

Without snapshot history, audits can only inspect the latest row — which is operational convenience, not educational accountability.

## 1.4 Deterministic Educational Intelligence

Core Educational Intelligence is deterministic: same Twin inputs + same Curriculum context → same readiness / decision / recommendation outputs on core paths.

That contract requires a **pin-able Twin**.

| Requirement | Snapshot implication |
|---|---|
| Reproducible judgement | Consumers reason from an immutable Twin identity, not a live mutable row |
| Replay | Historical Twin + Curriculum version → regenerate the same derived artefacts |
| Testability | Fixtures are whole snapshots; no hidden mid-test field drift |
| Honesty under failure | Absent / corrupt Twin fails closed; no half-mutated “almost Twin” |

If Persistence mutated in place, determinism would depend on timing: two readers of “the Twin” during an update could see different educational worlds. Snapshots eliminate that ambiguity.

## 1.5 Historical reconstruction

Historical reconstruction answers product and integrity questions that current-state alone cannot:

- What was the Twin when this Decision was selected?  
- Did Calibration priors still dominate when this Mission was composed?  
- How did Knowledge evolve after this Evidence batch?  
- Can we re-derive yesterday’s Educational Experience from yesterday’s Twin?

Immutable Twin history makes reconstruction a **regeneration** problem (load snapshot → run Intelligence), not an archaeology problem (guess which fields were overwritten).

Old snapshots remain valid history precisely because they were never mutated. Retirement of “current” designation does not erase meaning.

### Section invariant

> **Immutable snapshots serve explainability, auditability, determinism, and reconstruction. In-place mutation serves none of them.**

---

# 2. Snapshot contents

## 2.1 What belongs inside a persisted Twin

A persisted Twin snapshot must contain the **authoritative educational state** for one student / sitting scope at one point in evolution — complete enough that Educational Intelligence can reason without consulting product caches.

Version 1.0 snapshot contents fall into seven families:

```
Persisted Twin snapshot
├── Identity
├── Goals
├── Knowledge
├── Memory
├── Behaviour
├── Performance
├── Metadata · Provenance · Snapshot version
└── (optional thin lineage hooks: Evidence ids / Decision Journal refs — not derived judgements)
```

Confidence remains separable / deferred per Twin and Calibration law: Persistence must not invent Confidence to “complete” a snapshot. Empty or deferred Confidence stays empty.

Readiness, Decision, Recommendation, Mission, Planning artefacts, and presentation models are **not** snapshot contents as learner truth (see §3). Optional Prediction *history* is a separate concern from Twin educational-state persistence and must not become a second mastery store (§7).

## 2.2 Identity

**What it is:** Anchors that bind the Twin to the authenticated learner and scope preferences that intelligence may lawfully read (without owning auth secrets).

**Why it belongs:**

- Every Twin operation is scoped to Identity.  
- Without durable Identity anchors, Persistence cannot return “this student’s Twin” honestly.  
- Identity is educational *scope*, not educational *judgement* — but without it, judgements cannot attach to a person.

**Must not absorb:** passwords, sessions, CSRF, institutional auth policy, or fabricated Mid readiness from account age.

## 2.3 Goals

**What it is:** Active sitting / paper / curriculum targets, ambition posture, capacity constraints, and goal status that frame intelligence.

**Why it belongs:**

- Readiness time pressure, Decision constraints, and Mission feasibility are meaningless without Goals.  
- Calibration and wizard flows author Goals into the Twin; Persistence must preserve those anchors.  
- Goals are learner-state, not regenerated dashboard copy.

**Must not absorb:** WeekPlan rows, Mission task lists, or “progress %” summaries dressed as goals.

## 2.4 Knowledge

**What it is:** Current mastery structure and beliefs (including Calibration priors marked as self-declared, and later Evidence-backed beliefs).

**Why it belongs:**

- Knowledge answers “what do they know *now*?” — primary educational truth for coverage and strength.  
- Priors and Evidence-backed beliefs must survive sessions with provenance intact.  
- Empty Knowledge slots must remain empty through Persistence; silence is honesty.

**Must not absorb:** readiness bands, pass probability, recommendation rankings, or Mid defaults for schema completeness.

## 2.5 Memory

**What it is:** Retention structure and beliefs — whether demonstrated knowledge remains available toward the sitting.

**Why it belongs:**

- Memory is a first-class Twin write domain; loss of Memory across sessions collapses revision pressure into Knowledge-only fiction.  
- Calibration may leave Memory empty at birth; Persistence must preserve emptiness, not invent decay curves.

**Must not absorb:** due-card UI lists, spaced-repetition presentation queues, or Mission “review today” cards.

## 2.6 Behaviour

**What it is:** How the student actually studies — consistency, adherence patterns, and behavioural structure evolved from Evidence.

**Why it belongs:**

- Behaviour is educational state about practice reliability, distinct from Knowledge and Performance.  
- Decision and Readiness consume Behaviour as Twin input; caching Behaviour only inside Mission completion rows creates parallel truth.  
- Birth Twins may leave Behaviour empty; Persistence preserves that honesty.

**Must not absorb:** streak theatre counters as competing Twin truth, gamification caches, or dashboard habit widgets as authority.

## 2.7 Performance

**What it is:** Assessment-condition lineage and scoped performance structure (mocks, exams, assessed attempts) as Twin belief structure.

**Why it belongs:**

- Performance answers how the student fares under assessment conditions — irreducible to untimed Knowledge.  
- Calibration may place Performance priors; Evidence later earns truth. Both must persist as Twin state.  
- Readiness Assessment Performance factor and Decision selection depend on this domain.

**Must not absorb:** analytics chart caches, gradebook presentation models, or pass/fail marketing claims without Twin warrant.

## 2.8 Metadata

**What it is:** Non-belief administrative facts required to treat the snapshot as a durable artefact: student / sitting scope keys, authorship class (Calibration birth vs Evidence successor), timestamps of Twin authorship (when the snapshot was produced), and any Application-required integrity markers.

**Why it belongs:**

- Metadata makes snapshots addressable, orderable, and distinguishable without interpreting educational meaning.  
- It supports current designation, concurrency honesty, and retrieval without inventing beliefs.  
- Metadata is about the snapshot as a record, not about syllabus mastery.

**Must not absorb:** readiness scores, recommendation payloads, or “engagement” metrics as educational authority.

## 2.9 Provenance

**What it is:** Lineage that explains *how this Twin came to be*: Calibration contract / mapping lineage where applicable; Evidence ids that drove Update Strategies; warrant markers (`self_declared` vs Evidence-backed); strategy / pipeline identity at a structural level.

**Why it belongs:**

- Without provenance, Persistence can store a Twin that looks complete but cannot be trusted educationally.  
- Calibration law forbids rebranding priors as Evidence-backed during storage; provenance is the acceptance condition of that law.  
- Explainability and audit cite provenance hooks, not reconstructed guesses.

**Must not absorb:** narrative coach copy, UI warnings text, or Decision packaging strings as substitute warrant.

## 2.10 Snapshot version

**What it is:** Dual version identity:

1. **Educational snapshot identity / sequence** — which Twin this is in the birth → successor chain (distinct from “the student”).  
2. **Structural format version** — which Twin contract shape the payload obeys (for future-compatible load).

**Why it belongs:**

- Current designation needs an identity to point at.  
- Historical reconstruction needs ordered identities.  
- Format evolution must not invent Mid mastery when old snapshots lack new fields (Capability 3.7.1 §7).  
- Deterministic Intelligence needs a pin-able version to replay.

**Must not absorb:** product release marketing versions, A/B experiment flags that rewrite beliefs, or “compatibility Mid-fill” as version migration.

### Contents invariant

> **Persist complete Twin educational state: Identity, Goals, belief domains, metadata, provenance, and snapshot version. Persist emptiness where authors left emptiness. Never persist derived judgements as if they were Twin domains.**

### Contents that are adjacent but not Twin Persistence cargo

| Artefact | Relation to Twin Persistence |
|---|---|
| **Learning Evidence** | Append-only study history; separate durability concern; Twin may hold Evidence *ids* as lineage hooks |
| **Decision Journal outcomes** | Accept/dismiss audit spine; may be referenced, not embedded as Recommendation cards inside the Twin |
| **Curriculum** | Syllabus truth outside the Twin; Twin references curriculum identities, never embeds a second syllabus |

---

# 3. Derived artefacts

## 3.1 What must NEVER be persisted as Twin educational truth

Derived artefacts are reproducible from persisted Twin + Curriculum + lawful constraints. Persisting them *as* Twin state creates competing learner truth and invites stale intelligence.

| Derived artefact | Why it must not be Twin Persistence cargo |
|---|---|
| **Educational Experience** | Orchestrator composition for the day — regenerable from TwinProvider load + Intelligence read path |
| **Dashboard ViewModels** | Presentation projections; may cache for performance only if invalidated from Twin identity, never as authority |
| **Recommendation cards** | Packaging of Decision outcomes for UX — not learner beliefs |
| **Mission cards / Mission lists** | Daily work projections — Planning/Mission consequence of intelligence |
| **Readiness outputs / ReadinessState** | Read-path aggregation from Twin + Curriculum + Goals — regenerate on consume |
| **Decision outputs / Decision State packages** | Selected next-action judgement — regenerate from current Twin |
| **Recommendation outputs** | Ranked / packaged actions — regenerate from Decision |
| **Progress summaries** | Narrative or %-style rollups for surfaces — regenerate; never a parallel mastery store |
| **WeekPlan / schedule grids** | Planning consequences — rebuild when Twin, calendar, or constraints change |
| **Coach narratives / insight blurbs** | Explanatory projections around Twin factors — must not silently own Twin state |

## 3.2 Why they are regenerated

Regeneration is not waste — it is **integrity**.

1. **Single source of truth.** If Readiness is stored beside Knowledge and later Knowledge evolves, stored Readiness lies unless every write path remembers to refresh it. Regeneration makes freshness structural.  
2. **Determinism.** Same Twin → same derived outputs. Stored cards freeze a judgement that may no longer follow from the Twin.  
3. **Explainability.** Fresh derivation can cite the *current* Twin factors; stale cards cite ghosts.  
4. **Failure honesty.** TwinAbsent must not be papered over by last week’s Mission cards pretending authority.  
5. **Layering.** Domains judge; Persistence stores Twin; Presentation displays. Persisting ViewModels into Twin Persistence collapses layers.  
6. **Calibration honesty.** A birth Twin with empty Memory must not inherit a cached “High readiness” card from a previous sitting’s theatre.

### Regeneration rule

```
Persisted Twin snapshot (+ Curriculum + constraints)
        ↓
Readiness Aggregation → Decision Engine → Recommendation → Mission
        ↓
Educational Experience / Dashboard ViewModels / cards
```

Nothing in the lower row may write back into Twin Persistence as educational state.

## 3.3 Allowed caches vs forbidden authority

| Pattern | Lawful? | Condition |
|---|---|---|
| Ephemeral cache of a ViewModel keyed by Twin snapshot identity | Yes (performance) | Must not outrank TwinProvider; invalidate when current Twin changes |
| Persisting last Recommendation as “what the student needs” without Twin | No | Competing educational truth |
| Persisting Readiness % table as Twin substitute | No | Parallel learner-state store (Epic 2 pathology) |
| Optional Prediction *history* explicitly labelled as derived judgement archive | Deferred / careful | Must never substitute for Knowledge/Memory/Behaviour/Performance; V1.0 recommendation is to avoid (§7) |

### Derived invariant

> **If Educational Intelligence can regenerate it from the Twin, Persistence must not elevate it to Twin truth.**

---

# 4. Snapshot lifecycle

## 4.1 Lifecycle chain

Twin Persistence participates only in durable store / load of immutable wholes. Educational authorship remains elsewhere.

```
Birth
  ↓
Persist
  ↓
Retrieve
  ↓
Update Strategy (produces successor Twin)
  ↓
New Snapshot
  ↓
Persist
  ↓
Retire previous current snapshot
```

“Retire” means: **withdraw current designation**. It does **not** mean delete, mutate, or reinterpret the prior snapshot.

## 4.2 Birth

1. Student Calibration (or another lawful birth author) produces an immutable Birth Twin.  
2. Contents are priors + Identity / Goals anchors; empty domains remain empty.  
3. Persistence has not yet run — the Twin exists as authored state, not yet durable.

Birth is authorship, not Persistence.

## 4.3 Persist (birth)

1. Twin Persistence accepts the complete Birth Twin.  
2. Snapshot identity / format version / provenance are retained as authored.  
3. The snapshot becomes **current** for the student / sitting scope.  
4. No fields are filled, stripped, or Mid-defaulted for storage convenience.

## 4.4 Retrieve

1. TwinProvider requests load of the current Twin.  
2. Persistence returns the immutable snapshot or signals absence / integrity failure.  
3. Educational Orchestrator and Domains consume that Twin.  
4. Derived artefacts are regenerated — not loaded as Twin cargo.

## 4.5 Update Strategy → New Snapshot

1. Learning Evidence arrives on the lawful write path.  
2. Twin Update Pipeline invokes Update Strategies.  
3. Strategies return a **new** complete Twin (successor), not a patch list.  
4. The prior Twin remains historically accurate as what the product believed before this Evidence batch.

## 4.6 Persist (successor)

1. Persistence stores the successor Twin as a new snapshot identity.  
2. Provenance includes Evidence lineage that authored the change.  
3. The successor becomes **current**.

## 4.7 Retire previous current snapshot

1. Previous snapshot loses **current** designation only.  
2. Content remains intact and loadable as history.  
3. No educational reinterpretation accompanies retirement.  
4. Product read paths default to the new current Twin; explicit historical reads may pin prior identities for audit / reconstruction.

## 4.8 Why old snapshots remain valid history

Old snapshots remain valid because:

| Reason | Meaning |
|---|---|
| **They were true then** | Educational honesty is time-indexed; later Evidence does not falsify prior sparse honesty |
| **Explainability needs them** | Past Decisions and Missions cite past Twin factors |
| **Audit needs them** | Authorship disputes resolve against immutable records |
| **Reconstruction needs them** | Replay Intelligence from a pinned Twin identity |
| **Migration needs them** | Structural format upgrades start from truthful priors, not invented Mid rows |

Destructive overwrite of prior snapshots would convert Persistence into a forgetting machine — convenient for storage volume, fatal for educational integrity.

### Lifecycle invariant

> **Birth and Strategies author. Persistence stores wholes. Current moves forward. History stays true.**

---

# 5. Educational integrity

## 5.1 Why Intelligence must reason from the persisted Twin

Educational Integrity requires that every preparedness claim and next-action selection be warranted by learner-state authority.

That authority is the **Digital Twin**.

| Input to Intelligence | Integrity outcome |
|---|---|
| Persisted current Twin | Judgements track true learner state; same Twin → same outputs |
| Cached Recommendation / Mission / Readiness | Judgements track last product packaging; may diverge from Twin after Evidence |
| Legacy mastery / readiness % peers | Parallel truth; Stage A dual-authority pathology returns |
| Fabricated Mid Twin on absence | Certainty theatre; TwinAbsent law violated |

Therefore:

1. **Read path:** TwinProvider loads persisted Twin (or TwinAbsent) → Orchestrator → Domains.  
2. **Write path:** Evidence → Strategies → new Twin → Persist → later Retrieve.  
3. **Never:** Dashboard reads last Mission card and treats it as Knowledge.  
4. **Never:** Persistence “helps” by writing derived Readiness back into the Twin aggregate as if it were a belief domain.

## 5.2 Cached recommendations are not educational state

A Recommendation card answers: *What did we show the student?*  
A Twin answers: *What do we believe about the student?*

Those are different questions.

| If Intelligence reasons from… | Failure |
|---|---|
| Cached cards | Accept/dismiss loops amplify stale packaging; Evidence updates ignored until cache expires |
| Twin | Cards regenerate; accept/dismiss become Evidence / Journal events that evolve the Twin lawfully |

Cached recommendations may exist briefly for UX performance. They must never become the input to Readiness, Decision, or Mission composition. The moment a cache becomes an input to educational judgement, the Twin is no longer the single source of truth.

## 5.3 Integrity chain (binding)

```
Learning Evidence / Calibration authorship
        ↓
Digital Twin snapshot (persisted)
        ↓
Educational Intelligence (Readiness → Decision → Recommendation → Mission)
        ↓
Educational Experience / presentation
```

Any arrow that skips the Twin — or writes derived outputs back as Twin beliefs — breaks integrity.

### Integrity invariant

> **Educational Intelligence always reasons from the persisted Twin (or honest absence). Cached recommendations are consequences, never premises.**

---

# 6. Risks

## 6.1 Stale derived state

**Failure mode:** Product surfaces or secondary stores retain Readiness / Recommendation / Mission artefacts after the current Twin has advanced.

**Educational harm:** Student acts on judgements that no longer follow from learner state; trust erodes when “study next” contradicts fresh Evidence.

**Mitigation principle:** Treat derived artefacts as regenerable and Twin-identity-keyed. Prefer recompute-on-read for Version 1.0 core paths. Never persist derived artefacts as Twin Persistence cargo.

## 6.2 Hidden mutations

**Failure mode:** Dashboard composition, TwinProvider, background jobs, or “quick fix” routes patch Twin fields in storage without Calibration or Update Strategies.

**Educational harm:** Beliefs appear without Evidence or declaration; provenance becomes fiction; determinism dies.

**Mitigation principle:** Closed lawful write paths only (Calibration birth / re-calibration; Evidence → Pipeline → successor). Persistence accepts complete snapshots only — never field patches.

## 6.3 Partial writes

**Failure mode:** Persistence accepts a Knowledge-only fragment, a domain slice upsert, or a half-written successor while leaving Memory / Behaviour from an older snapshot under the same identity.

**Educational harm:** Hybrid Twins no Strategy authored; domains disagree across invisible version seams; concurrency races invent educational chimeras.

**Mitigation principle:** Only complete immutable Twin aggregates cross Persistence. Successor replaces current as a whole. Conflict rules choose among complete snapshots — never merge fields.

## 6.4 Snapshot drift

**Failure mode:** Structural format migration, “compatibility fills,” or provenance stripping cause loaded Twins to differ educationally from what authors produced — empty → Mid, `self_declared` → Evidence-backed, unknown → invented.

**Educational harm:** Persistence silently becomes Calibration and Intelligence; historical reconstruction lies; cold-start honesty collapses.

**Mitigation principle:** Additive migration; preserve empty / unknown / self-declared; format version on every snapshot; fail corrupt loads honestly rather than repair by invention.

## 6.5 Repository becoming educational

**Failure mode:** TwinRepository (or underlying storage adapter) starts creating Birth Twins on absence, interpreting mastery, scoring readiness, composing Missions, or “completing” empty domains for schema satisfaction.

**Educational harm:** Persistence absorbs Educational Intelligence — recreating the study-planner pathology Epic 2 ended, with durable false certainty.

**Mitigation principle:** TwinRepository answers only durable store / load / absence / integrity signalling. Authors remain Calibration Builder and Update Strategies. Domains never import Persistence. TwinProvider remains retrieval honesty for Orchestrator.

### Risk restatement

| Risk | Core danger |
|---|---|
| Stale derived state | Judgement without current Twin |
| Hidden mutations | Belief without lawful authorship |
| Partial writes | Twin no Strategy produced |
| Snapshot drift | History rewritten by storage |
| Repository becoming educational | Persistence owns meaning |

> **The primary educational risk is not missing storage. It is Persistence that creates, mutates, merges, or judges.**

---

# 7. Version 1.0 recommendations

## 7.1 Simplest persistence strategy that preserves educational integrity

Version 1.0 should prefer the **smallest durable model** that keeps the Twin as single educational truth:

### Recommendation A — Persist whole Twin snapshots only

- Store complete immutable Twin aggregates authored by Calibration or Update Strategies.  
- Include Identity, Goals, Knowledge, Memory, Behaviour, Performance as authored (including lawful emptiness).  
- Include metadata, provenance, and snapshot version identity.  
- Do **not** persist Educational Experience, ViewModels, cards, Readiness outputs, Decision outputs, Recommendation outputs, Mission lists, or progress summaries as Twin Persistence cargo.

### Recommendation B — Replace-by-snapshot with retained history

- One **current** snapshot per student / sitting scope for product read paths.  
- Prior snapshots retained as valid history (audit / explainability / reconstruction).  
- No in-place field mutation; no partial upsert; no educational merge on conflict.

### Recommendation C — Regenerate all intelligence on read

- TwinProvider loads current Twin (or TwinAbsent).  
- Readiness → Decision → Recommendation → Mission run from that Twin.  
- Optional ephemeral caches keyed by Twin snapshot identity are allowed for performance; they must never become educational premises.  
- Version 1.0 should **not** require a durable Prediction / Readiness judgement archive to ship Twin Persistence.

### Recommendation D — Keep adjacent durability separate

- Learning Evidence remains append-only and separate.  
- Decision Journal remains separate accept/dismiss audit.  
- Twin snapshots may hold lineage *references* (Evidence ids, journal hooks) without embedding derived product cards.

### Recommendation E — Honesty over completeness

- Missing Twin → TwinAbsent, not invented Birth Twin.  
- Corrupt Twin → integrity failure, not Mid repair.  
- Empty domains stay empty through store and load.  
- Calibration provenance survives Persistence as an acceptance condition.

## 7.2 Explicit Version 1.0 non-goals (persistence model)

| Non-goal | Why deferred |
|---|---|
| Durable store of ReadinessState / Decision packages as Twin truth | Derived; regenerate |
| Embedding Mission / Recommendation cards in Twin snapshots | Presentation / packaging |
| Technology choice (SQL/ORM/engine) | Later implementation milestone |
| Aggressive history compaction that destroys prior snapshots | Threatens audit / explainability |
| Dual-write to legacy mastery % as Twin peer authority | Parallel truth |

## 7.3 Success criteria for Version 1.0 Persistence model

Version 1.0 Twin Persistence analysis is satisfied when later implementation can claim:

1. A calibrated Birth Twin survives sessions with priors and emptiness intact.  
2. An Evidence-evolved successor Twin becomes current without mutating the prior.  
3. TwinProvider retrieves durable Twin or honest absence — never fabrication.  
4. Educational Intelligence judgements after retrieve match judgements from the same Twin in memory.  
5. No derived artefact is required to reconstruct educational state.  
6. Persistence still never creates, interprets, mutates, or reasons.

### Version 1.0 restatement

> **Persist the Twin whole. Retain history. Regenerate everything else. Prefer honesty to completeness.**

---

# 8. Closing

Capability 3.7.1 defined *how* Persistence must behave. Capability 3.7.2 defines *what* educational state that behaviour protects.

**Persisted:** Identity, Goals, Knowledge, Memory, Behaviour, Performance, metadata, provenance, snapshot version — the Digital Twin aggregate as authored.

**Not persisted as Twin truth:** Educational Experience, dashboard ViewModels, recommendation and mission cards, readiness / decision / recommendation outputs, progress summaries — all reproducible.

**Lifecycle:** Birth → Persist → Retrieve → Update Strategy → New Snapshot → Persist → Retire previous current — with old snapshots remaining valid history.

**Integrity:** Educational Intelligence reasons from the persisted Twin, never from cached recommendations.

**Version 1.0:** Whole-snapshot replace-with-history; regenerate intelligence on read; keep Persistence non-educational.

Governing principle remains binding:

> **The Digital Twin is the single source of educational truth. Everything else is reproducible.**

**STOP.** This milestone is analysis only. No ORM. No SQL. No repository code. No implementation.

---

# References

| Artefact | Role |
|---|---|
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Upstream Persistence architecture law |
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing Educational Intelligence ADR |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Immutable Twin snapshots; write/read separation |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law |
| [`CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md`](CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md) | Birth Twin contents Persistence must not reinterpret |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Retrieval honesty; load of durable Twin |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | TwinRepository as Application persistence adapter |
| [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md) | Readiness as derived; optional Prediction path |
| [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md) | Epic 3 product integration law |
