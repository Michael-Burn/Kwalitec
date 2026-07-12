# Capability 3.7.1 — Twin Persistence Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.7.1 Twin Persistence (Application Layer durable Twin snapshot storage preceding repository implementation)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Upstream Calibration architecture:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Upstream Calibration mapping:** [`CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md`](CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Persistence debt:** Technical Debt Register **E2-PE-01** (Twin persistence) — owned architecturally by this capability  
**Scope:** Structural architecture for Twin Persistence — durable storage of immutable Digital Twin snapshots without creating, interpreting, mutating, or educationally reasoning about them — **no code, Flask, ORM, SQL, schemas, migrations, repository implementations, or persistence technology choices**

---

## Document purpose

Student Calibration (Capability 3.6) is complete. The platform can create a truthful Birth Digital Twin — priors and Identity / Goals anchors from self-declared educational history, never educational judgements.

That birth Twin cannot yet survive sessions. TwinProvider can retrieve only what exists. Without durable persistence, calibrated birth state and every later Twin evolution remain ephemeral — debt **E2-PE-01**, not a license to fabricate Twins on the read path.

This capability defines **Twin Persistence**: the architectural contract for storing and loading Digital Twin snapshots so Educational Intelligence can consume truthful learner state across sessions — without Persistence becoming Educational Intelligence.

**Governing principle (binding):**

> **Persistence stores the Digital Twin. It never creates it. It never interprets it. It never mutates it. It never reasons educationally.**

**Architectural restatement:**

> **Twin Persistence is an Application Layer durable snapshot store. StudentCalibrationBuilder creates birth Twins. Twin Update Strategies produce successor Twins. TwinRepository persists and loads immutable snapshots. TwinProvider retrieves what Persistence holds (or signals honest absence). Educational Intelligence remains the sole owner of educational judgement. Learning Evidence remains the sole owner of evidence-backed belief evolution.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Twin Persistence** | Architectural capability: durable storage of immutable Twin snapshots (this document) |
| **TwinRepository** | Application persistence adapter that owns persist / load / absence signalling for Twin snapshots |
| **Storage** | Infrastructure underneath TwinRepository — holds bytes / durable records; never defines educational honesty policy |
| **Birth Twin** | First lawful Digital Twin snapshot (typically from Student Calibration) |
| **Successor Twin** | New immutable snapshot produced by Twin Update Strategies (or other lawful authors); never an in-place edit of a prior snapshot |
| **Current Twin** | The latest lawful snapshot for a student / sitting scope that TwinProvider retrieves for product read paths |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Flask routes, forms, templates, or UI copy  
- Database schemas, Alembic migrations, ORM models, SQL, or repository implementations  
- Persistence technology choices (database engines, file formats, caches, queues)  
- Redesign of Evidence, Twin domains, Twin Update Pipeline, Readiness, Decision, Recommendation, or Mission  
- Redesign of Student Calibration or TwinProvider honesty contracts  
- Educational algorithms, mastery inference, readiness scoring, or recommendations  

---

# 1. Purpose

## 1.1 Why Twin Persistence exists

Without Twin Persistence:

- Birth Twins from Calibration cannot survive the session that created them.  
- Evidence-driven Twin updates cannot accumulate as durable learner history.  
- TwinProvider has nothing durable to retrieve; Internal Alpha cold-start honesty remains permanent theatre debt.  
- Pressure rises to invent Mid preparedness, starter Twins, or legacy mastery rows as substitute Twin authority — exactly what TwinProvider and ADR-002 forbid.  
- Educational Intelligence remains correct in theory and unavailable in product practice.

**Twin Persistence** exists to:

1. **Durably store** immutable Digital Twin snapshots authored elsewhere.  
2. **Make TwinProvider real** — retrieve what exists across sessions, or signal honest absence.  
3. **Preserve truthful evolution** — each stored Twin is a complete snapshot with provenance intact (including Calibration `self_declared` markers).  
4. **Keep Domains framework-free** — Persistence absorbs durable storage concerns; domains receive Twin snapshots as arguments.  
5. **Refuse educational ownership** — Persistence never creates, interprets, mutates, or reasons about Twin content.

It is the lawful answer to:

> “Where does an already-authored Digital Twin live so the product can retrieve it later?”

It is **not** the answer to:

> “What should the Twin contain?”  
> “What does the student know?”  
> “What should they study next?”

```
Student Calibration / Twin Update Strategies
              ↓
        Digital Twin (immutable snapshot)
              ↓
   Twin Persistence / TwinRepository     ← stores and loads (this document)
              ↓
        TwinProvider
              ↓
   Educational Orchestrator
              ↓
   Readiness → Decision → Recommendation → Mission
```

Governing restatement:

> **Twin Persistence changes *where* the Twin lives. It does not change *what* the Twin means, *who* may author it, or *how* Educational Intelligence judges the student.**

## 1.2 Relationship with Student Calibration

| Concern | Owner |
|---|---|
| Capture self-declared history; map priors; emit Birth Twin | **Student Calibration** (Capability 3.6) |
| Store the Birth Twin snapshot; load it later | **Twin Persistence** (this document) |
| Retrieve Twin or TwinAbsent for orchestration | **TwinProvider** |

**Rules:**

1. **Calibration creates; Persistence stores.** TwinRepository never authors priors, Identity, Goals, or empty-domain fills “for schema completeness.”  
2. **Provenance must survive storage.** Persisting a calibrated Twin must not strip `self_declared` markers or rebrand priors as Evidence-backed mastery.  
3. **Absence of Persistence is not absence of Calibration law.** Until Persistence ships, Calibration may still emit lawful Twins that cannot yet survive sessions — that is E2-PE-01 debt, not permission for TwinProvider fabrication.  
4. **Re-calibration is not silent rewrite.** History correction remains an explicit Calibration (or Evidence) event that produces a new Twin; Persistence stores the replacement snapshot, never patches fields in place.

### Calibration invariant

> **Twin Persistence stores what Calibration produced. It does not become a second Calibration Builder.**

## 1.3 Relationship with Educational Intelligence

| Concern | Owner |
|---|---|
| Learner-state authority and belief evolution | **Educational Intelligence** (Twin domains + Twin Update Pipeline + Strategies) |
| Durable snapshot storage and load | **Twin Persistence / TwinRepository** |
| Educational judgement (readiness, decision, packaging, mission) | **Educational Intelligence Domains** |

**Rules:**

1. **Educational Intelligence never depends on Persistence frameworks.** Domains receive Twin snapshots; they do not import TwinRepository, ORM, or storage.  
2. **Persistence never performs educational judgement.** No readiness bands, mastery inference, Decision selection, Recommendation packaging, or Mission composition inside TwinRepository.  
3. **Write/read firewall preserved.** Belief evolution remains Evidence → Twin Update Pipeline → new Twin snapshot → Persist. Dashboard composition remains TwinProvider load-only.  
4. **Persistence is not a parallel learner-state store.** Legacy mastery / readiness % tables must not compete with stored Digital Twin snapshots as Twin-first authority.

### Educational Intelligence invariant

> **Educational Intelligence owns Twin meaning. Twin Persistence owns Twin durability. Neither may absorb the other.**

---

# 2. Ownership

## 2.1 TwinRepository owns persistence only

| Responsibility | Meaning |
|---|---|
| **Persist** | Accept an already-authored immutable Digital Twin snapshot and store it durably for the authorised student / sitting scope. |
| **Load** | Return the current (or explicitly requested historical) Twin snapshot when storage can supply a lawful one. |
| **Absence signalling** | Signal that no Twin exists for the requested scope — without inventing one. |
| **Integrity signalling** | Signal corrupt / unreadable / contract-violating payloads without “repairing” beliefs. |
| **Provenance preservation** | Persist Twin content — including Calibration prior markers and lineage — without reinterpretation. |
| **Version identity** | Retain snapshot identity / version markers required for history and future compatibility (architectural identity, not a technology choice). |
| **Framework isolation** | Keep Domains free of durable storage concerns by owning the Application ↔ Storage boundary. |

TwinRepository is a **persistence adapter**. It is not Educational Intelligence. It is not Twin birth. It is not Twin retrieval honesty policy for Orchestrator (that remains TwinProvider). It is not Infrastructure policy beyond mapping Twin snapshots to durable form.

## 2.2 What TwinRepository never owns

| Forbidden ownership | Why |
|---|---|
| **Twin creation** | Birth Twins belong to StudentCalibrationBuilder (and lawful Calibration mapping). |
| **Twin interpretation** | Meaning of Knowledge, Memory, Behaviour, Performance, priors, and warrant belongs to Educational Intelligence. |
| **In-place mutation** | Belief evolution produces new Twin snapshots via Twin Update Strategies / Pipeline — never field patches inside storage. |
| **Educational reasoning** | Readiness, Decision, Recommendation, and Mission remain domain-owned. |
| **Learning Evidence authorship** | Evidence remains append-only study truth via EvidenceRecorder / Evidence model. |
| **Twin retrieval honesty policy for Orchestrator** | TwinProvider owns DigitalTwin \| TwinAbsent (and classified retrieval failure) for the product read path. |
| **Curriculum ownership** | Syllabus structure belongs to Curriculum Engine / `CurriculumService`. |
| **Presentation concerns** | HTTP, forms, templates, and UX copy are not Persistence. |

## 2.3 Owner map (no duplication)

| Concept | Layer | Owns | Relation to Twin Persistence |
|---|---|---|---|
| **StudentCalibrationBuilder** | Application | Creates Birth Twins from Calibration Contract | Emits Twin; Persistence stores it |
| **TwinRepository** | Application | Persist / load / absence / integrity signalling | Owns persistence only (this document) |
| **TwinProvider** | Application | Retrieve Twin or TwinAbsent for Orchestrator | Delegates durable load to TwinRepository when present |
| **Twin Update Strategies / Pipeline** | Domain | Produce new Twin snapshots from Evidence | Persistence stores each successor; never mutates prior |
| **Educational Intelligence Domains** | Domain | Consume Twins; judge preparedness / next action | Receive snapshots; never persist |
| **EvidenceRecorder** | Application | Record Learning Evidence | Separate write path; may precede Pipeline → new Twin → Persist |
| **EducationalOrchestrator** | Application | Compose day from Twin + CurriculumContext | Calls TwinProvider; never writes Twin via Persistence on dashboard path |
| **Storage** | Infrastructure | Durable records / bytes | Holds what TwinRepository maps; no educational policy |
| **Presentation** | Presentation | Auth, surfaces, collection of declarations | Never bypasses Application to edit Twin storage |

### Ownership invariants

1. **TwinRepository does not create Twins.**  
2. **TwinRepository does not interpret Twins.**  
3. **TwinRepository does not mutate Twins in place.**  
4. **TwinRepository does not reason educationally.**  
5. **StudentCalibrationBuilder creates; Twin Update Strategies evolve; TwinRepository stores; TwinProvider retrieves; Educational Intelligence consumes.**  
6. **Domains never import TwinRepository.** They receive Twin snapshots as arguments.  
7. **Presentation never bypasses TwinRepository** (via Application write paths) to patch learner-state rows as “quick fixes.”

Governing restatement:

> **TwinRepository answers only: “Can I durably store or load this immutable Twin snapshot?” It never answers educational questions about the student.**

---

# 3. Lifecycle

Twin Persistence participates in a **replace-by-snapshot** lifecycle. There is no lawful in-place edit of a stored Twin.

```
Birth Twin
     ↓
 Persist
     ↓
 Retrieve
     ↓
 Update Strategy produces new Twin
     ↓
 Persist replacement
     ↓
 Retrieve
```

## 3.1 Birth Twin

1. Student Calibration (Contract → Mapping → Builder) emits an immutable Birth Twin.  
2. TwinRepository **persists** that Birth Twin as the first durable snapshot for the student / sitting scope.  
3. Persistence does not validate educational meaning; it stores the lawful snapshot as authored.

## 3.2 Persist

- Persist means: accept a complete immutable Twin snapshot and write it durably.  
- Persist does **not** mean: merge fields, fill empty domains, strip provenance, or invent missing beliefs.  
- A successful persist makes the snapshot available for later retrieval as current (or as a versioned history entry — see §4 and §7).

## 3.3 Retrieve

- TwinProvider requests load via TwinRepository (once Persistence exists).  
- TwinRepository returns the current immutable Twin snapshot, or signals absence / failure.  
- TwinProvider maps that outcome to **DigitalTwin** or **TwinAbsent** (or equivalent classified retrieval failure) for Orchestrator.  
- Retrieve never fabricates educational state.

## 3.4 Update Strategy produces new Twin

1. Learning Evidence arrives through lawful write paths.  
2. Twin Update Pipeline invokes domain Update Strategies.  
3. Strategies return a **new** Digital Twin snapshot (UpdateResult / successor Twin).  
4. The prior Twin remains historically true; it is not overwritten in meaning by silent field edits.

## 3.5 Persist replacement

1. TwinRepository persists the **successor** Twin as the new current snapshot.  
2. Prior snapshots remain available as versioned history where the architecture requires truthful evolution (see §4).  
3. “Replacement” means **new current pointer / new snapshot identity** — not mutating the previous snapshot’s content.

## 3.6 Retrieve again

- Subsequent product read paths retrieve the latest lawful Twin.  
- Educational Intelligence consumes that Twin as current learner-state authority.  
- The cycle repeats: Evidence → new Twin → Persist → Retrieve.

### Lifecycle invariant

> **Never mutate in place. Every Twin that crosses Persistence is a complete immutable snapshot — birth or successor.**

### Forbidden lifecycle patterns

| Pattern | Why forbidden |
|---|---|
| Patch Knowledge / Memory fields in storage | Silent belief mutation; bypasses Update Strategies |
| “Upsert” partial Twin fragments | Partial mutation; loses snapshot integrity |
| Delete-and-recreate without history when evolution occurred | Erases truthful evolution |
| Persist a Twin invented by TwinProvider to avoid TwinAbsent | Fabrication; Persistence becomes birth author |
| Persist readiness / Decision / Mission as Twin | Wrong artefact; domains do not own Twin storage that way |

---

# 4. Persistence philosophy

## 4.1 Immutable snapshots

Every Twin that Persistence stores is an **immutable snapshot**.

- Authors produce complete Twin aggregates.  
- Persistence stores them whole.  
- Consumers receive them whole.  
- No component may treat storage as a mutable bag of Twin fields.

Immutability here is architectural: snapshots do not change after persist. Evolution is expressed only by **new** snapshots.

## 4.2 Versioned history

Twin Persistence prefers **versioned history** over destructive overwrite of meaning.

| Requirement | Meaning |
|---|---|
| **Snapshot identity** | Each persisted Twin has a durable identity distinct from “the student.” |
| **Ordering** | Snapshots form a truthful sequence (birth → successors). |
| **Current designation** | Exactly one snapshot is current for a given student / sitting scope on the product read path (unless an explicit historical read is requested). |
| **Prior retention** | Previous snapshots remain available for audit, explainability, and migration — they are not silently erased by evolution. |

Versioned history is how the product remains explainable: recommendations and decisions can cite Twin lineage without inventing a rewritten past.

## 4.3 Truthful evolution

Evolution of learner state is **truthful** only when:

1. Evidence (or lawful Calibration events) author change.  
2. Update Strategies (or Calibration Builder at birth / re-calibration) produce a new Twin.  
3. Persistence stores that new Twin without reinterpretation.  
4. Prior Twins remain historically accurate records of what the product believed at that time.

Truthful evolution forbids:

- Quietly “fixing” old snapshots after the fact.  
- Rebranding Calibration priors as Evidence-backed beliefs during storage.  
- Collapsing history into a single mutable row that forgets how the Twin got there.

## 4.4 No partial mutation

Persistence must not accept or perform **partial mutation** of Twin content.

Forbidden examples (architectural, not implementation):

- Updating only Knowledge while leaving Memory stale in the same snapshot identity.  
- Writing a single domain slice without a complete Twin aggregate.  
- Nulling warrant / provenance fields to “simplify” storage.  
- Filling empty Memory / Behaviour / Predictions because a schema disliked emptiness.

Empty domains that Calibration and Twin law leave empty must remain empty through Persistence. Silence is honesty.

## 4.5 No hidden writes

Every durable Twin write must be an **explicit Application persistence action** on a lawful write path.

| Lawful write path | Author of Twin content | Persistence role |
|---|---|---|
| Calibration birth / re-calibration | StudentCalibrationBuilder | Persist Birth / corrected Twin |
| Evidence → Twin Update Pipeline | Twin Update Strategies | Persist successor Twin |

Forbidden hidden writes:

- Dashboard composition side-effecting Twin storage.  
- TwinProvider persisting a fabricated Twin to avoid absence.  
- Presentation routes editing Twin storage directly.  
- Background jobs inventing Twin fields for completeness or engagement.  
- “Just this once” readiness or Decision caches written back as Twin state.

### Philosophy invariant

> **Immutable snapshots. Versioned history. Truthful evolution. No partial mutation. No hidden writes.**

---

# 5. Contracts

## 5.1 Boundary stack

```
Application
     ↓
TwinRepository
     ↓
Storage
```

| Boundary | What crosses | What must not cross |
|---|---|---|
| **Application → TwinRepository** | Immutable Digital Twin snapshots; authorised identity / sitting scope; persist or load intent | Educational goals as scoring inputs; partial field patches; invented Mid Twins |
| **TwinRepository → Storage** | Durable representation of those immutable snapshots (technology-neutral) | Educational interpretation; belief repair; hidden product writes |
| **TwinRepository → Application (load)** | Immutable Twin snapshot, or honest absence / integrity failure | Fabricated Twin; legacy % dressed as Twin; silently repaired corrupt payloads |

## 5.2 Only immutable Twins cross the boundary

**Binding contract rule:**

> **Only immutable Digital Twin snapshots cross the TwinRepository boundary.**

Implications:

1. **Persist input** is a complete Twin snapshot already authored by Calibration Builder or Update Strategies — not a declaration form, not Evidence raw events, not a readiness score, not a Decision.  
2. **Load output** is that same class of artefact — a Digital Twin snapshot — or an explicit non-Twin signal (absent / corrupt / unavailable).  
3. **Storage** may use any durable form later milestones choose; that choice is out of scope here. Architecturally, Storage is opaque underneath TwinRepository and must not invent Twin meaning.  
4. **Domains** never see Storage. They see Twin snapshots passed as arguments from Application.  
5. **TwinProvider** remains the Orchestrator-facing retrieval contract. TwinRepository is the durable adapter behind it (and behind lawful write-path persist calls). Collapsing Provider and Repository into one god adapter is forbidden.

## 5.3 Closed persist / load intents

| Intent | Meaning | Success cargo | Failure / honesty cargo |
|---|---|---|---|
| **Persist** | Store an authored immutable Twin as current (and retain history per philosophy) | Acknowledgement that the snapshot is durably current | Storage unavailable; reject unlawful / incomplete persist attempts without inventing content |
| **Load current** | Retrieve the current Twin for authorised scope | Immutable Digital Twin | Missing Twin; Corrupt Twin; Storage unavailable |
| **Load historical** (when product requires) | Retrieve a specific prior snapshot by identity / version | Immutable Digital Twin at that version | Missing version; Corrupt Twin; Storage unavailable |

### Contract invariant

> **Application asks TwinRepository to store or return immutable Twins. Storage holds them. Nothing in between may author educational belief.**

---

# 6. Failure behaviour

**Product rule (binding):**

> **The student should always receive the best truthful experience available. Never fabricate educational certainty.**

Twin Persistence prefers honest failure signals over a complete false Twin. Product behaviour below is architectural — not implementation.

## 6.1 Storage unavailable

| Condition | Persistence / product behaviour |
|---|---|
| Durable storage cannot accept or return Twin snapshots (outage, timeout, infrastructure failure) | Do **not** invent an in-memory Twin, Mid defaults, or starter Twin to keep surfaces full. |
| Persist path | Fail the persist attempt explicitly. Do not pretend durability. Do not silently drop the Twin while claiming success. |
| Retrieve path | TwinRepository signals unavailability; TwinProvider emits TwinAbsent-equivalent / retrieval failure; Orchestrator degrades composition. |
| Student experience | Reduced truthful surface; reload / retry may re-run identical contracts after recovery. |
| Forbidden | Fake Twin for availability theatre; inventing Decision “just this once”; treating outage as Mid preparedness. |

## 6.2 Missing Twin

| Condition | Persistence / product behaviour |
|---|---|
| No Twin snapshot exists for the authorised student / sitting scope | TwinRepository signals absence. TwinProvider returns **TwinAbsent**. |
| Truthful downstream effect | Orchestrator surfaces Missing Twin / cold-start posture; product may route the student to Calibration; no Mid/High readiness theatre. |
| Forbidden | TwinRepository inventing Birth Twin; TwinProvider fabricating priors; Persistence “helpfully” writing empty Knowledge as Mid. |

Absence is a **first-class honest outcome**, not an error to paper over with educational fiction.

## 6.3 Corrupt Twin

| Condition | Persistence / product behaviour |
|---|---|
| Stored payload cannot be mapped to a lawful Digital Twin (corrupt, contract-violating, unreadable, provenance stripped beyond recovery) | Do **not** repair by inventing beliefs or backfilling domains. |
| Retrieve path | Signal corrupt-load failure; TwinProvider treats as TwinAbsent-equivalent / explicit corrupt failure for Orchestrator. |
| Persist path | Reject attempts to persist known-unlawful Twin cargo if Application can detect contract violation before store — without “fixing” content. |
| Student experience | Degraded composition; Warnings may name degraded state; honesty over a patched Twin. |
| Forbidden | Best-effort “fix enough to score”; dropping warrant while retaining bold readiness; substituting legacy mastery rows as Twin. |

## 6.4 Concurrent updates

| Condition | Persistence / product behaviour |
|---|---|
| Two lawful write paths attempt to persist different successor Twins for the same scope (e.g. overlapping Evidence processing, Calibration correction racing an Evidence update) | Persistence must not silently merge Twin fields or invent a hybrid Twin. |
| Architectural requirement | Preserve snapshot integrity: one complete Twin wins as current under an explicit concurrency rule (e.g. reject stale write, or accept last complete snapshot with history retained) — **without** educational reinterpretation of either Twin. |
| Product behaviour | Prefer explicit conflict / retry / re-derive from Evidence + Pipeline over opaque field merges. The student must never receive a Twin that no Strategy authored. |
| Forbidden | Partial merge of Knowledge from A and Memory from B; hidden “average” of beliefs; discarding provenance to force a single row. |

### Failure propagation principle

```
Storage unavailable / Missing Twin / Corrupt Twin / Concurrent conflict
        ↓
TwinRepository signals honesty (unavailable | absent | corrupt | conflict)
        ↓
TwinProvider → TwinAbsent or classified retrieval failure (read path)
   or Application write path reports persist failure (write path)
        ↓
Educational Orchestrator / product workflow degrades claims
        ↓
Student sees best truthful experience available
```

### Failure invariant

> **Persistence failures are product honesty events. They are never permission to fabricate Educational Intelligence.**

---

# 7. Versioning

## 7.1 Future compatibility

Twin Persistence must assume Twin snapshot **shape and Twin domain contracts evolve**.

| Requirement | Meaning |
|---|---|
| **Snapshot format version** | Every persisted Twin carries an explicit structural version identity so future loaders know which Twin contract they are reading. |
| **Forward honesty** | Newer Persistence must load older snapshots without inventing educational meaning the old snapshot did not contain. |
| **Unknown fields** | Future fields absent from old snapshots remain empty / unknown — not Mid-filled for compatibility theatre. |
| **Provider contract stability** | TwinProvider outputs remain DigitalTwin or TwinAbsent regardless of snapshot format generation. |

Future compatibility is architectural discipline, not a license to rewrite history into the newest educational story.

## 7.2 Snapshot evolution

Snapshot evolution has two distinct meanings — both lawful, neither is in-place mutation:

| Kind | Meaning | Persistence role |
|---|---|---|
| **Educational evolution** | New Twin from Calibration correction or Evidence → Update Strategies | Persist successor; retain prior as history |
| **Structural evolution** | Twin contract / format version advances over product life | Store format version with each snapshot; migrate on load or via explicit migration — without changing educational authorship |

Educational evolution and structural evolution must not be conflated. A format migration must not quietly upgrade Calibration priors into Evidence-backed mastery.

## 7.3 Migration philosophy

When Twin snapshot contracts change:

1. **Prefer additive, immutable migration** — transform old snapshots into new snapshot versions as explicit artefacts, retaining lineage.  
2. **Do not destroy history** — migration must not erase prior snapshot meaning required for audit / explainability.  
3. **Do not invent beliefs during migration** — empty remains empty; unknown remains unknown; self-declared remains self-declared.  
4. **Fail honestly when migration cannot preserve law** — corrupt or unmigratable snapshots surface as corrupt / absent, not as Mid theatre.  
5. **Keep Domains free of migration machinery** — Application / Persistence own structural migration; domains continue to consume lawful Twin snapshots.  
6. **Technology choice remains deferred** — how bytes move is a later milestone; that migration must still obey this philosophy.

### Versioning invariant

> **Snapshots evolve by new versions and new Twin identities. Migration preserves truth. Compatibility never fabricates educational certainty.**

---

# 8. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Persistence becomes Twin author** | TwinRepository fills empty domains, invents Birth Twin on missing, or “completes” Calibration | Persist/load only; Calibration Builder and Strategies remain sole authors |
| **In-place mutation** | Storage patches fields; Update Pipeline bypassed | Immutable snapshots only; replace-by-snapshot lifecycle |
| **Hidden writes** | Dashboard / TwinProvider / jobs write Twin as side effects | Closed lawful write paths only; no composition side effects |
| **Provenance stripping** | Priors rebranded as Evidence-backed during store/load | Provenance preservation is a Persistence acceptance condition |
| **Parallel Twin stores** | Legacy mastery / readiness % compete as learner truth | TwinRepository load is Twin-first durable authority; legacy peers never substitute as DigitalTwin |
| **Failure fabrication** | Unavailable / missing / corrupt cases emit Mid Twins | TwinAbsent / classified failure only; Orchestrator degrades honestly |
| **Concurrency merge** | Racing writes produce hybrid Twins no Strategy authored | Complete snapshot wins under explicit conflict rule; no field merges |
| **Migration theatre** | Format upgrades invent Mid mastery for “compatibility” | Additive migration; empty/unknown/self-declared preserved |

### Risk restatement

The primary danger is not missing storage technology. It is a **persistence adapter that starts creating, interpreting, mutating, or reasoning** — recreating parallel learner truth and reintroducing the study-planner pathology Epic 2 ended.

---

# 9. Recommendations

## Architecture sequence

How Twin Persistence work should proceed after this architecture:

1. **Treat this document as architecture law for Capability 3.7.1** — Persistence stores; it never creates, interprets, mutates, or reasons. Do not reopen ADR-002’s educational chain.  
2. **Proceed Architecture → Implementation → Review** (Engineering Charter). This note authorises none of the code.  
3. **Keep TwinRepository thin** — persist / load / honesty signals only; TwinProvider remains Orchestrator retrieval contract.  
4. **Prove honesty first** — Missing Twin, Corrupt Twin, Storage unavailable, and Concurrent conflict must yield truthful product degradation before happy-path polish.  
5. **Preserve Calibration provenance** as an acceptance condition of any later Persistence implementation (E2-PE-01).  
6. **Enforce replace-by-snapshot lifecycle** — never mutate in place; never partial mutation; never hidden writes.  
7. **Wire TwinProvider → TwinRepository.load** when Persistence lands — without changing DigitalTwin \| TwinAbsent law.  
8. **Keep Domains framework-free** — TwinRepository absorbs durable storage concerns; domains receive Twin snapshots as arguments only.  
9. **Defer technology choices** — schemas, ORM, SQL, and engines belong to later implementation milestones, still bound by this architecture.  
10. **Guard against Persistence-as-author and parallel Twin stores** in Integration reviews.  
11. **Keep application code untouched until an explicit implementation milestone** authorises TwinRepository types, storage mapping, and tests.  
12. **STOP.** This milestone is architecture only. No services. No code. No ORM. No SQL. No tests. No implementation until an explicit implementation milestone authorises them.

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing Educational Intelligence ADR |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain and immutable snapshot law |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | TwinRepository named as Application persistence adapter |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Retrieval honesty; TwinRepository as future load delegate |
| [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md) | Birth Twin author; Persistence stores, never calibrates |
| [`CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md`](CAPABILITY_3_6_5_CALIBRATION_TWIN_MAPPING.md) | Mapping law Persistence must not reinterpret |
| [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md) | Orchestrator composition; Twin load on read path |
| [`docs/TECHNICAL_DEBT_REGISTER.md`](../TECHNICAL_DEBT_REGISTER.md) | E2-PE-01 Twin persistence debt |
| [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md) | Epic 3 product integration law |
