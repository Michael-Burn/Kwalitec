# Capability 3.7.3 — Twin Repository Contract

**Status:** Contract only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.7.3 Twin Repository Contract (immutable Application ↔ Persistence boundary for Twin snapshots)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Persistence architecture:** [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md)  
**Upstream Persistence analysis:** [`CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md`](CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Upstream Calibration:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Persistence debt:** Technical Debt Register **E2-PE-01** (Twin persistence)  
**Scope:** Closed, immutable Application contract for TwinRepository educational persistence operations — **no code, APIs, ORM, SQL, schemas, repository classes, or persistence technology**

---

## Document purpose

Capabilities 3.7.1–3.7.2 established:

- **Architecture** — Twin Persistence stores immutable Digital Twin snapshots; it never creates, interprets, mutates, or reasons.  
- **Analysis** — what educational state belongs inside a persisted snapshot, and what must remain derived.

This milestone defines the **immutable TwinRepository Contract**.

It answers:

> What exact persistence operations may Application ask of TwinRepository so authored Twin snapshots survive sessions — without TwinRepository becoming Educational Intelligence?

It is the sole Application persistence boundary for durable Twin snapshots.

**Governing principle (binding):**

> **The contract exposes educational persistence operations. It never exposes storage operations as educational meaning.**

**Architectural restatement:**

> **Authors produce Twins. TwinRepository persists and retrieves immutable snapshots. TwinProvider maps retrieval honesty for Orchestrator. Domains consume Twins. Storage holds bytes. Nothing in the repository contract may create, update, or interpret learner belief.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **TwinRepository Contract** | Immutable closed set of educational persistence operations (this document) — Version 1.0 |
| **TwinRepository** | Application persistence adapter that will honour this contract (named conceptually; not implemented here) |
| **Birth Twin** | First lawful Digital Twin snapshot for a student / sitting scope (typically from Student Calibration) |
| **Successor Twin** | New immutable snapshot produced by Twin Update Strategies (or other lawful authors) |
| **Current Twin** | The single snapshot designated current for a student / sitting scope on the product read path |
| **Snapshot history** | Ordered prior Twin snapshots retained as truthful evolution, not mutated past |

**Non-goals of this document**

- Implementation types, dataclasses, interfaces, repository classes, or package layouts  
- HTTP APIs, route handlers, ORM models, SQL, schemas, or migrations  
- Persistence technology choices (engines, formats, caches, queues)  
- Redesign of Twin domains, Calibration, TwinProvider, Update Strategies, Readiness, Decision, Recommendation, or Mission  
- Educational algorithms, mastery inference, readiness scoring, or recommendation selection  

---

# 1. Purpose

## 1.1 Why TwinRepository exists

Without a closed TwinRepository contract:

- Calibration birth Twins and Evidence-driven successors have no lawful durable home;  
- TwinProvider has nothing durable to retrieve across sessions;  
- pressure rises to invent Mid Twins, patch fields in place, or treat legacy mastery rows as Twin authority;  
- Domains are tempted to import storage concerns;  
- Persistence technology details leak upward as educational “operations.”

**TwinRepository** exists so that:

1. **Application has one closed persistence boundary** for Digital Twin snapshots.  
2. **Authors remain authors** — Calibration Builder and Update Strategies produce Twins; the repository only stores and returns them.  
3. **TwinProvider remains honest** — load outcomes map to Twin presence, absence, or classified failure without fabrication.  
4. **Domains stay framework-free** — they receive Twin snapshots as arguments; they never own durability.  
5. **Educational language stays educational** — operations name Twin lifecycle events, not tables, rows, or queries.

It is the lawful answer to:

> “How does Application durably keep and later obtain an already-authored Digital Twin snapshot?”

It is **not** the answer to:

> “What should the Twin contain?”  
> “What does the student know?”  
> “What should they study next?”  
> “Which database stores the bytes?”

Governing restatement:

> **TwinRepository changes *where* an authored Twin lives. It does not change *what* the Twin means or *who* may author it.**

## 1.2 Relationship with StudentCalibrationBuilder

| Concern | Owner |
|---|---|
| Capture declarations; map priors; emit Birth Twin | **StudentCalibrationBuilder** |
| Persist the Birth Twin; retrieve it later | **TwinRepository** (this contract) |

**Rules:**

1. **Builder creates; Repository stores.** TwinRepository never authors priors, Identity, Goals, or empty-domain fills.  
2. **Provenance must survive persist / retrieve.** Self-declared markers and Calibration lineage must not be stripped or rebranded as Evidence-backed mastery.  
3. **Re-calibration produces a new Twin.** The repository persists a successor (or corrected) snapshot; it never patches the original birth snapshot in place.  
4. **No Birth Twin without an author.** Missing Twin is absence, not permission for the repository to invent Calibration.

### Calibration invariant

> **TwinRepository stores what StudentCalibrationBuilder produced. It does not become a second Calibration Builder.**

## 1.3 Relationship with TwinProvider

| Concern | Owner |
|---|---|
| Orchestrator-facing retrieval honesty: DigitalTwin or TwinAbsent (or classified failure) | **TwinProvider** |
| Durable persist / retrieve / current designation / history for Twin snapshots | **TwinRepository** |

**Rules:**

1. **Provider retrieves; Repository supplies durability.** TwinProvider may delegate load to TwinRepository; it does not become Persistence.  
2. **Provider remains load-only on the dashboard path.** TwinRepository write operations belong only to lawful write paths (Calibration birth / correction; Evidence → Update Strategies → persist successor).  
3. **Absence remains first-class.** Repository signals missing Twin; Provider maps that to TwinAbsent — never to a fabricated Mid Twin.  
4. **Collapsing Provider and Repository is forbidden.** One answers Orchestrator honesty; the other answers durable snapshot persistence.

### Provider invariant

> **TwinRepository changes *where* TwinProvider loads from. It does not change *that* TwinProvider may only return DigitalTwin or TwinAbsent (or classified retrieval failure).**

## 1.4 Relationship with Twin Update Strategies

| Concern | Owner |
|---|---|
| Produce successor Twin snapshots from Evidence (via Twin Update Pipeline) | **Twin Update Strategies** |
| Persist each successor; retain prior snapshots as history; designate current | **TwinRepository** |

**Rules:**

1. **Strategies evolve; Repository stores succession.** Evolution is replace-by-snapshot, never in-place field mutation.  
2. **Every successor is a complete Twin.** The repository accepts wholes only — not domain slices.  
3. **Prior snapshots remain historically true.** Designating a new current does not rewrite prior snapshot content.  
4. **The repository never invokes Strategies.** It does not re-derive beliefs, merge racing successors educationally, or “fix” incomplete evolution.

### Update Strategies invariant

> **Twin Update Strategies author change. TwinRepository records the succession of immutable wholes.**

## 1.5 Relationship with Educational Orchestrator

| Concern | Owner |
|---|---|
| Compose the Twin-first product day from Twin + CurriculumContext | **Educational Orchestrator** |
| Durable Twin snapshot persist / retrieve | **TwinRepository** |
| Orchestrator-facing Twin presence or absence | **TwinProvider** (delegating durable load when Persistence exists) |

**Rules:**

1. **Orchestrator never writes Twin via Persistence on the dashboard read path.** Composition is read-only for Twin state.  
2. **Orchestrator never imports TwinRepository for educational judgement.** It consumes Twin (or TwinAbsent) and CurriculumContext; readiness / decision / packaging remain domains.  
3. **Honest degradation on persistence failure.** Missing, corrupt, or unavailable Twin yields reduced truthful composition — never Mid theatre.  
4. **Write/read firewall preserved.** Evidence recording and Twin succession persist remain separate from Orchestrator composition.

### Orchestrator invariant

> **Educational Orchestrator consumes what TwinProvider retrieves. TwinRepository never participates as an educational domain.**

```
StudentCalibrationBuilder / Twin Update Strategies
              ↓
        Digital Twin (immutable snapshot)
              ↓
   TwinRepository  ← this contract (persist / retrieve)
              ↓
        TwinProvider
              ↓
   Educational Orchestrator
              ↓
   Readiness → Decision → Recommendation → Mission
```

---

# 2. Ownership

Ownership is absolute. TwinRepository is a persistence adapter, not a shared editable Twin worksheet.

| Actor | Owns | Must never |
|---|---|---|
| **StudentCalibrationBuilder** | Create Birth Twins from Calibration Contract | Persist storage policy; invent durability from silence |
| **Twin Update Strategies / Pipeline** | Produce successor Twins from Evidence | Mutate stored snapshots in place; call storage as belief editor |
| **TwinRepository** | **Store** and **retrieve** immutable Twin snapshots; designate current; retain history; signal absence / integrity / conflict | Create Twins; update Twin beliefs; perform educational reasoning; repair corrupt cargo by inventing beliefs |
| **TwinProvider** | Map durable load outcomes to DigitalTwin \| TwinAbsent (or classified failure) for Orchestrator | Persist fabricated Twins; become Persistence author |
| **Educational Orchestrator** | Compose product day from Twin + CurriculumContext | Write Twin on dashboard path; score readiness inside Persistence |
| **Educational Intelligence Domains** | Consume Twins; judge preparedness / next action | Import TwinRepository; persist derived artefacts as Twin truth |
| **Storage (Infrastructure)** | Hold durable records / bytes underneath the adapter | Define educational honesty policy; invent Twin meaning |

## 2.1 Repository stores snapshots

TwinRepository **stores**:

- Birth Twin snapshots authored by StudentCalibrationBuilder.  
- Successor Twin snapshots authored by Twin Update Strategies (or other lawful authors).  
- Snapshot identity, ordering, current designation, and provenance required for truthful evolution.  
- Structural format version identity required for forward compatibility.

Store means: accept a complete immutable Twin and make it durable for the authorised student / sitting scope.

## 2.2 Repository retrieves snapshots

TwinRepository **retrieves**:

- The current Twin for an authorised student / sitting scope.  
- Explicitly requested historical snapshots by snapshot identity / version.  
- Ordered snapshot history when product integrity requires lineage.  
- Honest signals when no lawful Twin can be returned.

Retrieve means: return an immutable Twin snapshot whole, or signal why none can be returned.

## 2.3 Repository never creates Twins

Forbidden:

- Inventing a Birth Twin when none exists.  
- Filling empty domains “for schema completeness.”  
- Seeding Mid Knowledge / Memory / Behaviour from silence.  
- Treating TwinAbsent as permission to author priors.

Absence is an outcome, not a construction prompt.

## 2.4 Repository never updates Twins

Forbidden:

- In-place field patches to Knowledge, Memory, Behaviour, Performance, Identity, or Goals.  
- Partial “upsert” of domain slices into an existing snapshot identity.  
- Quiet rewrite of provenance (e.g. self-declared → Evidence-backed).  
- Destructive overwrite of prior snapshot meaning when a successor arrives.

Evolution is expressed only by **persisting a new complete snapshot** and designating it current.

## 2.5 Repository never performs educational reasoning

Forbidden inside TwinRepository:

- Readiness aggregation or preparedness bands.  
- Mastery inference or belief reinterpretation.  
- Decision selection, Recommendation packaging, Mission composition.  
- Educational conflict resolution that invents a hybrid Twin no Strategy authored.  
- Migration that upgrades empty / unknown / self-declared into Mid certainty.

### Ownership invariants

1. **Repository stores snapshots.**  
2. **Repository retrieves snapshots.**  
3. **Repository never creates Twins.**  
4. **Repository never updates Twins.**  
5. **Repository never performs educational reasoning.**  
6. **StudentCalibrationBuilder creates; Twin Update Strategies evolve; TwinRepository stores; TwinProvider retrieves; Educational Intelligence consumes.**

Governing restatement:

> **TwinRepository answers only: “Can I durably store or retrieve this immutable Twin snapshot?” It never answers educational questions about the student.**

---

# 3. Contract

Version **1.0** of the TwinRepository Contract is a **closed** set of educational persistence operations.

Operations are named for Twin lifecycle meaning — not for storage mechanics.

## 3.1 Closed operations

| Operation | Meaning | Success cargo | Honesty cargo |
|---|---|---|---|
| **Persist Birth Twin** | Accept the first lawful Twin for a student / sitting scope and store it as the initial durable snapshot (and current) | Acknowledgement that the Birth Twin is durably current | Scope already has a Twin; storage unavailable; unlawful / incomplete Twin cargo rejected without repair |
| **Retrieve Current Twin** | Return the Twin currently designated for the authorised student / sitting scope | Immutable Digital Twin (current) | Missing Twin; Corrupt Twin; Storage unavailable |
| **Persist Successor Twin** | Accept a new complete Twin authored by Update Strategies (or lawful re-calibration) and store it as the new current, retaining prior snapshots as history | Acknowledgement that the successor is durably current | Concurrent successor conflict; duplicate snapshot identity; storage unavailable; unlawful / incomplete cargo rejected without repair |
| **Retrieve Snapshot History** | Return the ordered lineage of Twin snapshots for the authorised scope (birth → successors) | Ordered immutable Twin snapshots (or identities + current designation sufficient for lineage) | Missing history / empty scope; Corrupt Twin in lineage; Storage unavailable |
| **Determine Current Snapshot** | Resolve which snapshot is current for the authorised student / sitting scope without inventing one | Current snapshot identity (and optionally the Twin itself) | No current designation (Missing Twin); Corrupt current; Storage unavailable |

### Operation language rules

1. **Educational persistence, not storage.** Prefer “Persist Birth Twin” over “insert row”; prefer “Retrieve Current Twin” over “query latest.”  
2. **Wholes only.** Every persist accepts a complete Twin aggregate; every retrieve returns a complete Twin or an honest non-Twin signal.  
3. **No mutate operation.** There is no Version 1.0 operation to patch, merge, or edit an existing snapshot’s educational content.  
4. **No invent operation.** There is no Version 1.0 operation to create Twin beliefs from absence.  
5. **Current is designation, not mutation.** Persist Successor changes which snapshot is current; it does not rewrite prior snapshot content.

## 3.2 Persist Birth Twin

**Intent:** Make the first authored Twin durable for a scope that has none.

**Requires:**

- Authorised student / sitting scope.  
- A complete immutable Birth Twin already authored (typically StudentCalibrationBuilder).  
- No existing Twin for that scope (or an explicit product rule that birth is first-only).

**Must not:**

- Author missing domains.  
- Silently replace an existing current Twin without succession semantics.  
- Strip Calibration provenance.

## 3.3 Retrieve Current Twin

**Intent:** Obtain the Twin Educational Intelligence should reason from now.

**Requires:**

- Authorised student / sitting scope.

**Returns:**

- The immutable Twin currently designated for that scope, **or**  
- Missing Twin / Corrupt Twin / Storage unavailable honesty signals.

**Must not:**

- Fabricate a Twin to avoid absence.  
- Substitute legacy mastery / readiness percentages as DigitalTwin.  
- Repair corrupt cargo by inventing beliefs.

## 3.4 Persist Successor Twin

**Intent:** Record truthful evolution as a new immutable snapshot and designate it current.

**Requires:**

- Authorised student / sitting scope.  
- A complete immutable successor Twin already authored.  
- Lawful succession posture (Evidence → Strategies, or explicit re-calibration / correction event).

**Effects (conceptual):**

- Prior current becomes historical.  
- Successor becomes current.  
- Prior snapshot content remains unchanged.

**Must not:**

- Merge fields from concurrent candidates.  
- Accept partial domain fragments.  
- Mutate the previous snapshot identity’s content.

## 3.5 Retrieve Snapshot History

**Intent:** Expose truthful Twin lineage for audit, explainability, and reconstruction.

**Requires:**

- Authorised student / sitting scope.

**Returns:**

- Ordered snapshots (or equivalent lineage cargo) from birth through successors, **or** honest emptiness / failure signals.

**Must not:**

- Rewrite historical snapshots to match current educational fashion.  
- Drop provenance to “simplify” history.  
- Invent intermediate Twins to fill gaps.

## 3.6 Determine Current Snapshot

**Intent:** Resolve current designation without fabricating educational state.

**Requires:**

- Authorised student / sitting scope.

**Returns:**

- Identity of the current snapshot (and optionally the Twin), **or** Missing Twin / failure honesty.

**Must not:**

- Elect a “best guess” Twin from corrupt or partial candidates.  
- Create a current designation without a persisted Twin.  
- Average or blend snapshot identities.

### Contract invariant

> **Application asks TwinRepository to persist or retrieve immutable Twins — birth, current, successor, history, current designation. Nothing in between may author educational belief.**

### Boundary rule (binding)

> **Only immutable Digital Twin snapshots cross the TwinRepository boundary.** Persist inputs and retrieve outputs are Twin wholes (or explicit non-Twin honesty signals). Declarations, Evidence events, readiness scores, Decisions, Recommendations, and Missions are not TwinRepository cargo.

---

# 4. Immutability

## 4.1 Why repositories never mutate existing snapshots

TwinRepository must treat every stored Twin as an **immutable snapshot**.

Educational integrity depends on it:

1. **Explainability** — recommendations and Decisions cite Twin factors that must remain reconstructible as they were.  
2. **Auditability** — the product must answer what it believed about the learner, when, and under which authorship path.  
3. **Determinism** — Educational Intelligence requires a pin-able Twin identity; live field edits make “the Twin” timing-dependent.  
4. **Historical reconstruction** — prior snapshots must regenerate prior derived artefacts without archaeology of overwritten fields.  
5. **Authorship clarity** — mutation hides whether Calibration, Strategies, or Persistence wrote the change.

In-place mutation would make Persistence a silent co-author of learner belief — exactly what Capability 3.7.1 forbids.

## 4.2 How evolution remains lawful without mutation

| Event | Lawful repository behaviour |
|---|---|
| Birth | Persist Birth Twin as first immutable snapshot and current |
| Evidence-driven change | Persist Successor Twin; retain prior as history; designate successor current |
| Re-calibration / history correction | Persist a new complete Twin; do not patch the original birth snapshot |
| Format / structural migration | Produce explicit migrated snapshot artefacts with lineage; do not silently rewrite educational meaning inside an old identity |

### Immutability invariant

> **Never mutate in place. Every Twin that crosses TwinRepository is a complete immutable snapshot — birth or successor. Evolution is succession of wholes.**

### Forbidden mutation postures

| Posture | Why forbidden |
|---|---|
| Patch Knowledge / Memory fields in an existing snapshot | Silent belief mutation; bypasses Update Strategies |
| Upsert partial Twin fragments | Loses snapshot integrity |
| Rebrand self-declared priors as Evidence-backed during store/load | Provenance stripping |
| Delete prior history when a successor arrives | Erases truthful evolution |
| “Fix” old snapshots after the fact for compatibility theatre | Rewrites the past |

---

# 5. Failure behaviour

**Product rule (binding):**

> **The student should always receive the best truthful experience available. Never fabricate educational certainty.**

Contract behaviour only — no storage mechanics, retries as infrastructure detail, or UI copy.

## 5.1 Missing Twin

| Condition | Contract behaviour |
|---|---|
| No Twin snapshot exists for the authorised student / sitting scope | **Retrieve Current Twin** / **Determine Current Snapshot** signal **Missing Twin** |
| Truthful downstream effect | TwinProvider returns TwinAbsent; Orchestrator degrades to cold-start / Missing Twin posture; product may route to Calibration |
| Persist Birth Twin when scope is empty | Lawful — this is how absence ends |
| Forbidden | Invent Birth Twin; fill Mid defaults; treat missing as Mid preparedness |

Absence is a **first-class honest outcome**, not an error to paper over with educational fiction.

## 5.2 Storage unavailable

| Condition | Contract behaviour |
|---|---|
| Durable persistence cannot accept or return Twin snapshots | Signal **Storage unavailable** on the affected operation |
| Persist path | Fail explicitly — do not claim durability; do not silently drop the Twin while reporting success |
| Retrieve path | TwinProvider maps to TwinAbsent-equivalent / classified retrieval failure; Orchestrator degrades composition |
| Forbidden | Invent in-memory Twin, starter Twin, or Mid defaults for availability theatre |

## 5.3 Duplicate snapshot

| Condition | Contract behaviour |
|---|---|
| Persist attempts to store a Twin under a snapshot identity that already exists, or Persist Birth Twin when a Twin already exists for the scope | Signal **Duplicate snapshot** (or equivalent birth-already-exists honesty) |
| Truthful effect | Reject the persist; retain the existing lawful snapshot(s) unchanged |
| Forbidden | Silently overwrite existing snapshot content; merge duplicate cargo into a hybrid Twin; invent a third “reconciled” Twin |

Duplicate detection protects immutability. Correction requires Persist Successor Twin (or an explicit new birth/correction event with clear succession semantics) — never silent replace of the same identity’s meaning.

## 5.4 Concurrent successor

| Condition | Contract behaviour |
|---|---|
| Two lawful write paths attempt to Persist Successor Twin for the same scope (e.g. overlapping Evidence processing racing Calibration correction) | Signal **Concurrent successor** / conflict — do not invent a hybrid |
| Architectural requirement | Preserve snapshot integrity: one complete Twin may become current under an explicit concurrency rule (reject stale succession, or accept last complete snapshot with history retained) — **without** educational reinterpretation of either Twin |
| Product behaviour | Prefer explicit conflict / retry / re-derive from Evidence + Pipeline over opaque field merges |
| Forbidden | Partial merge of Knowledge from A and Memory from B; hidden “average” of beliefs; discarding provenance to force a single current |

The student must never receive a Twin that no Strategy (or Calibration Builder) authored.

## 5.5 Corrupt snapshot

| Condition | Contract behaviour |
|---|---|
| Stored cargo cannot be mapped to a lawful Digital Twin (corrupt, contract-violating, unreadable, provenance stripped beyond recovery) | Signal **Corrupt Twin** — do not repair by inventing beliefs |
| Retrieve path | TwinProvider treats as TwinAbsent-equivalent / explicit corrupt failure for Orchestrator |
| Persist path | Reject known-unlawful Twin cargo if Application can detect contract violation before store — without “fixing” content |
| Forbidden | Best-effort “fix enough to score”; dropping warrant while retaining bold readiness; substituting legacy mastery rows as Twin |

### Failure summary

| Failure | Contract posture |
|---|---|
| Missing Twin | Absent signal — no fabrication |
| Storage unavailable | Unavailable signal — no durability theatre |
| Duplicate snapshot | Reject — no silent overwrite |
| Concurrent successor | Conflict signal — no hybrid merge |
| Corrupt snapshot | Corrupt signal — no belief repair |

### Failure propagation principle

```
Missing Twin / Storage unavailable / Duplicate snapshot / Concurrent successor / Corrupt snapshot
        ↓
TwinRepository signals honesty
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

# 6. Versioning

## 6.1 Forward compatibility

The TwinRepository Contract must remain stable for Application consumers while Twin snapshot shape evolves.

| Requirement | Meaning |
|---|---|
| **Contract operation stability** | Version 1.0 operations (Persist Birth Twin, Retrieve Current Twin, Persist Successor Twin, Retrieve Snapshot History, Determine Current Snapshot) remain the closed educational persistence vocabulary |
| **Snapshot format version** | Every persisted Twin carries structural version identity so future retrieval knows which Twin contract it is reading |
| **Forward honesty** | Newer Persistence must retrieve older snapshots without inventing educational meaning the old snapshot did not contain |
| **Unknown fields** | Future Twin fields absent from old snapshots remain empty / unknown — not Mid-filled for compatibility theatre |
| **Provider contract stability** | TwinProvider outputs remain DigitalTwin or TwinAbsent (or classified failure) regardless of snapshot format generation |

Forward compatibility is architectural discipline, not a license to rewrite history into the newest educational story.

## 6.2 Snapshot evolution

Snapshot evolution has two distinct meanings — both lawful, neither is in-place mutation:

| Kind | Meaning | Repository role |
|---|---|---|
| **Educational evolution** | New Twin from Calibration correction or Evidence → Update Strategies | Persist Successor Twin; retain prior as history |
| **Structural evolution** | Twin contract / format version advances over product life | Store format version with each snapshot; migrate via explicit artefacts — without changing educational authorship |

Educational evolution and structural evolution must not be conflated. A format migration must not quietly upgrade Calibration priors into Evidence-backed mastery.

## 6.3 Repository stability

| Change type | Breaking for Contract Version 1.0? | Rule |
|---|---|---|
| Add optional honesty signal detail (e.g. finer corrupt classification) | No if existing Missing / Unavailable / Duplicate / Concurrent / Corrupt meanings remain | Additive honesty |
| Add optional retrieve-by-identity operation | No if Version 1.0 operations unchanged | Additive operation under new contract minor version |
| Remove Persist Successor Twin | Yes | Breaks truthful evolution |
| Add “Patch Twin Field” operation | Yes — forbidden | Violates immutability law |
| Redefine Missing Twin as invent-Mid | Yes — forbidden | Violates honesty law |
| Change Persist Birth Twin to author empty domains | Yes — forbidden | Repository becomes Calibration |

### Versioning rules

1. **Additive by default** for optional honesty detail and non-breaking retrieval convenience.  
2. **Never silently redefine Version 1.0 operation meaning.**  
3. **No mutation operation may be introduced** without an architecture revision that overturns Persistence law (not expected).  
4. **Snapshot format versions evolve independently** of this repository operation contract — format migration must still obey immutability and provenance preservation.  
5. **Domains remain free of repository versioning machinery** — Application / Persistence own structural migration; domains consume lawful Twin snapshots.

### Versioning invariant

> **Repository operations stay educational and stable. Snapshots evolve by new versions and new Twin identities. Compatibility never fabricates educational certainty.**

---

# 7. Contract Compliance Summary

| Invariant | Status under this contract |
|---|---|
| Educational persistence operations (not storage verbs) | Defined — Version 1.0 closed set |
| Persist Birth Twin / Retrieve Current Twin / Persist Successor Twin / Retrieve Snapshot History / Determine Current Snapshot | Affirmed |
| Stores and retrieves snapshots only | Affirmed |
| Never creates Twins | Affirmed |
| Never updates Twins in place | Affirmed |
| Never performs educational reasoning | Affirmed |
| Relationship with Calibration Builder, TwinProvider, Update Strategies, Orchestrator | Affirmed |
| Immutability of stored snapshots | Affirmed |
| Honest failure: missing / unavailable / duplicate / concurrent / corrupt | Affirmed |
| Forward-compatible versioning without Mid theatre | Affirmed |
| No code / APIs / SQL / ORM / repository class | Honoured — contract only |

---

# 8. STOP

This document defines the **TwinRepository Contract** only.

It does **not** authorise:

- Implementation  
- Repository classes or interfaces  
- APIs or route handlers  
- ORM models, SQL, schemas, or migrations  
- Persistence technology choices  
- Twin redesign  
- Educational algorithms or Intelligence changes  
- TwinProvider or Orchestrator code changes  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing Educational Intelligence ADR |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain and immutable snapshot law |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | TwinRepository named as Application persistence adapter |
| [`CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md`](CAPABILITY_3_7_1_TWIN_PERSISTENCE_ARCHITECTURE.md) | Twin Persistence architecture law |
| [`CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md`](CAPABILITY_3_7_2_TWIN_PERSISTENCE_ANALYSIS.md) | What educational state belongs in snapshots |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Retrieval honesty; TwinRepository as durable load delegate |
| [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md) | Birth Twin author |
| [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md) | Orchestrator composition; Twin load on read path |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law |
| [`docs/TECHNICAL_DEBT_REGISTER.md`](../TECHNICAL_DEBT_REGISTER.md) | E2-PE-01 Twin persistence debt |
