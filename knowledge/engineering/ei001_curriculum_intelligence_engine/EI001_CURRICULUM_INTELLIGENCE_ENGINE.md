# EI-001 — Curriculum Intelligence Engine

**Programme:** Educational Intelligence · EI-001  
**Status:** Canonical architecture specification  
**Date:** 2026-07-30  
**Authority:** Future CIP / educational-quality work must follow this document  
**Predecessor:** EQ-001 Educational Quality (proved semantic classification, syllabus-first hierarchy, front-matter gating, measurable coverage — certified **BLOCKED** pending CMP coherence + live republish)  
**Related:** CIP-001/002/003 · FV-001A workflow · `ARCHITECTURE.md` CIP section · `knowledge/engineering/ARCHITECTURE_INVARIANTS.md`

---

## 1. Mission

EQ-001 proved that curriculum quality can be significantly improved through
semantic classification, syllabus-first hierarchy, front-matter filtering, and
educational validation — still inside a **one-pass document parser**.

EI-001 replaces that operating model.

Kwalitec shall no longer operate as a document parser.  
It shall become a **Curriculum Intelligence Engine**.

Instead of producing a curriculum in one pass, the system shall progressively
**construct, optimise, validate, and certify** the curriculum through multiple
educational generations.

| Law | Meaning |
|---|---|
| One purpose per generation | Each generation has a single educational job |
| Monotonic improvement | Each generation improves the previous one or is rejected |
| Measured impact | Every generation emits comparable quality metrics |
| Safe rollback | If quality deteriorates, reject the optimisation and restore the prior generation |
| Explainable lineage | Founder can always inspect *why* a node exists |

---

## 2. Architectural principle

### Replace

```
PDF → Extraction → Curriculum
```

### With

```
PDF
  → Generation 1  (Raw Educational Graph)
  → Generation 2  (Noise Elimination)
  → Generation 3  (Hierarchy Construction)
  → Generation 4  (Topic Consolidation)
  → Generation 5  (Objective Intelligence)
  → Generation 6  (Educational Reconciliation)
  → Generation 7  (Educational Certification)
  → Founder Calibration
  → Publication
```

**Ingress remains CIP document storage** (CS-DOC-001 / Curriculum Studio upload).  
**Egress remains Studio structure preparation → preview → approve → publish** (FV-001A).  
EI-001 owns the **intelligence core between extract and Founder-facing structure**.

---

## 3. Architecture

### 3.1 Bounded contexts

| Context | Role under EI-001 |
|---|---|
| `curriculum_documents` | Document kinds + storage ingress (unchanged) |
| `curriculum_studio` | Founder workflow, calibration UI projection, publish gates |
| `curriculum_intelligence` | **Curriculum Intelligence Engine** — generations, lineage, regression, certification |
| `curriculum` (engine JSON) | V1/V2 official syllabus traversal for Student Runtime — **not replaced**; publication may later project certified graphs into engine packages |
| Student Twin / Mission / Tutor | Consume published curriculum only; never call generation services |

### 3.2 Layering

```
Templates / Founder Console
        ↓
Curriculum Studio blueprints (thin)
        ↓
Curriculum Studio application services
  (upload, structure prep, preview, calibration projection, publish)
        ↓
Curriculum Intelligence Engine (application)
  GenerationOrchestrator · RegressionGuard · CertificationEngine · CalibrationRouter
        ↓
Domain contracts
  Generation · LineageNode · QualitySnapshot · CertificationDecision · CalibrationProfile
        ↓
Ports
  PdfExtractionPort · GenerationStorePort · ReviewPackPort · SyllabusAuthorityPort
        ↓
Infrastructure adapters + CIP persistence (extended)
```

Laws preserved from `ARCHITECTURE_INVARIANTS.md`:

- Application never imports Infrastructure.
- No LLM inside educational decisions (generations remain deterministic rule/evidence systems).
- Deterministic educational decisions: same sources + calibration → same certified graph.
- Evidence precedes inference; provenance is mandatory.
- Curriculum V1 and V2 remain loadable and traversable.

### 3.3 Relationship to CIP pipeline stages

CIP-001 stages remain the **document processing spine** (verify → extract → …).  
EI-001 generations are a **second state machine** that consumes normalised extraction
and emits certified curriculum graphs.

| CIP stage (existing) | EI-001 role |
|---|---|
| `VERIFIED` … `NORMALIZED` | Unchanged — PDF → durable extracted/normalised document |
| `PARSED` / `MAPPED` / `GRAPH_BUILT` | **Migrate** into Generations 1–5 (see §9 Migration) |
| CIP-002 provenance / confidence / audit | **Extend** into Curriculum Memory (§5) |
| CIP-003 embeddings | Run only on **certified** (or calibrated) graph nodes |
| Studio structure preparation | Consumes **certified generation snapshot**, not raw mapper output |

```
┌─────────────────────────────────────────────────────────────┐
│ Document spine (CIP)                                        │
│  Upload → Store → Verify → Extract → Normalize              │
└────────────────────────────┬────────────────────────────────┘
                             │ normalised ExtractedDocument(s)
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Curriculum Intelligence Engine (EI-001)                     │
│  G1 → G2 → G3 → G4 → G5 → G6 → G7                           │
│  + RegressionGuard on every G≥2                             │
│  + Curriculum Memory (lineage)                              │
└────────────────────────────┬────────────────────────────────┘
                             │ CertifiedCurriculumSnapshot
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Founder surface                                             │
│  Calibration (partial regen) → Preview → Approve → Publish  │
└─────────────────────────────────────────────────────────────┘
```

### 3.4 Core components

| Component | Responsibility |
|---|---|
| **GenerationOrchestrator** | Runs generations in order; checkpoints snapshots; never skips regression gates |
| **GenerationRunner[N]** | One educational purpose; pure transform over prior snapshot(s) + sources |
| **CurriculumMemory** | Append-only lineage for every educational node and rejection |
| **RegressionGuard** | Compares quality vectors; accepts or rolls back |
| **CertificationEngine** | Generation 7 scoring + pass/fail decision |
| **CalibrationRouter** | Maps Founder style settings → affected generation subset only |
| **ReviewPackEmitter** | Educational Review Pack artefacts (comparison, lineage, coverage, …) |
| **SyllabusAuthorityPort** | Official syllabus as WHAT-authority (EQ-001 reconciliation) |
| **CmpInstructionPort** | CMP as HOW-support (teaching assets, not hierarchy authority when syllabus present) |

### 3.5 Snapshot contract

Every generation produces an immutable **CurriculumGenerationSnapshot**:

```
CurriculumGenerationSnapshot
  generation_id: str
  generation_index: 1..7
  purpose: str
  parent_generation_ids: list[str]   # multi-parent for G≥3 validation views
  source_document_ids: list[int]
  nodes: list[EducationalNode]
  rejected_nodes: list[RejectedNode]  # soft-deleted; never destroyed
  metrics: QualitySnapshot
  provenance_bundle_id: str
  created_at
  status: accepted | rejected_by_regression | superseded
```

Publication and Founder Preview bind to the latest **accepted** snapshot at or
beyond Generation 7 (or a calibrated child of Generation 7).

---

## 4. Generation model

### Shared rules for all generations

1. **Deterministic** — no hidden randomness; LLM prose (if any) is presentation-only.
2. **Evidence-bearing** — every accept/reject/merge carries reason, confidence, source evidence.
3. **Non-destructive** — rejected or superseded nodes remain in Curriculum Memory.
4. **Multi-generation validation (G≥3)** — optimisation generations compare against:
   - original source evidence (normalised extract / Gen 1),
   - previous generation,
   - generation before previous  
   (never optimise against a single prior output alone).
5. **One educational purpose** — no generation may absorb another generation’s job.

---

### Generation 1 — Raw Educational Graph

**Purpose:** Produce the richest possible educational graph. Do **not** optimise.

| Rule | Detail |
|---|---|
| Capture | Everything that could plausibly be educational |
| Confidence | Required on every node |
| Provenance | Page/block/document/job required |
| Deletion | **Forbidden** — Gen 1 never deletes |

**Inputs:** Normalised `ExtractedDocument` (syllabus and/or CMP).  
**Outputs:** Maximal node set with provisional roles (reuses EQ-001 `ContentRole` taxonomy as *labels*, not yet as filters that drop content).  
**EQ-001 mapping:** Expand current extract → parse path to retain chrome/TOC/etc. as first-class nodes with roles, rather than silently dropping them before memory exists.

---

### Generation 2 — Noise Elimination

**Purpose:** Remove non-curriculum material from the *active* hierarchy while preserving rejected nodes for comparison.

Remove (active set):

Front matter · Copyright · Publisher metadata · Navigation · Headers/Footers · TOC · Qualification pages · Marketing · Appendices · Indexes · References · Blank artefacts · Assessment logistics (when not educational)

Every removal must include:

| Field | Requirement |
|---|---|
| `reason` | Stable code + human label |
| `confidence` | 0–1 with factors |
| `source_evidence` | Page/block excerpt |

**No destructive deletion.** Rejected nodes remain queryable in Curriculum Memory and Review Pack (`nodes_rejected`).

**Inputs:** Gen 1 snapshot.  
**Validation parents:** Original extract + Gen 1.  
**EQ-001 mapping:** `ContentClassificationService` + `NON_CURRICULUM_ROLES` + front-matter gate — moved from inline parse-time drop to an explicit generation with regression metrics (noise rate, contamination).

---

### Generation 3 — Hierarchy Construction

**Purpose:** Construct the educational role chain:

```
Subject → Chapter → Section → Topic → Learning Objective
```

| Rule | Detail |
|---|---|
| Parent justification | Every node must justify its parent (evidence + rule code) |
| Arbitrary nesting | Rejected |
| Authority | Syllabus numbering / weighted topics are authoritative when present; CMP chapter codes are instructional support |

**Inputs:** Gen 2 active set + syllabus authority.  
**Validation parents:** Original + Gen 1 + Gen 2.  
**EQ-001 mapping:** Depth-aware structural parse + syllabus-first mapping + nest-stack sync — become the Gen 3 runner, not a side effect of parsing.

---

### Generation 4 — Topic Consolidation

**Purpose:** Merge fragmented topics into coherent learning units.

| Optimise for | Do **not** optimise for |
|---|---|
| Educational coherence | Topic count targets as primary objective |

Decision questions (encoded as deterministic heuristics + evidence scores):

1. Would an IFoA student naturally study these together?
2. Would a lecturer teach these together?
3. Would separating them improve understanding?

Merges record lineage: `merged_into` / `merged_from` with evidence spans.

**Inputs:** Gen 3 hierarchy.  
**Validation parents:** Original + Gen 2 + Gen 3.  
**EQ-001 debt closed here:** CMP ~936 → coherent instructional units (EQ-001B coalescing becomes Gen 4).

---

### Generation 5 — Objective Intelligence

**Purpose:** Associate every topic with:

- learning objectives  
- competencies  
- exam expectations  
- knowledge statements  

Each objective receives confidence, source evidence, and syllabus reference.

**Inputs:** Gen 4 topics + syllabus LO grammar + CMP objective hints (as support).  
**Validation parents:** Original + Gen 3 + Gen 4.  
**EQ-001 mapping:** Depth-aware LO extraction + false-positive hint control.

---

### Generation 6 — Educational Reconciliation

**Purpose:** Compare the working curriculum against:

- Official Syllabus (WHAT)  
- CMP (HOW)  
- Previous generations  

Determine: coverage · missing concepts · unexpected concepts · hierarchy consistency · educational completeness.

**Inputs:** Gen 5 + SyllabusAuthority + CmpInstruction.  
**Validation parents:** Original + Gen 4 + Gen 5 (+ Gen 1 coverage ceiling).  
**EQ-001 mapping:** `SyllabusReconciliationService` elevated to a first-class generation with regression on completeness.

---

### Generation 7 — Educational Certification

**Purpose:** Produce certification artefacts and a decision.

| Output | Meaning |
|---|---|
| Quality Score | Aggregate educational quality 0–100 |
| Confidence | Mean / distribution of node confidence |
| Coverage | Syllabus completeness |
| Hierarchy Score | Role-chain and parent-justification integrity |
| Granularity Score | Topic coherence / density appropriateness |
| Certification decision | `CERTIFIED` · `CERTIFIED_WITH_WARNINGS` · `NOT_CERTIFIED` |

**Inputs:** Gen 6 + full metric history.  
**EQ-001 mapping:** `EducationalQualityAuditService` + product EQ-001 certifier patterns — curriculum-structure certification (distinct from Runtime C mission-quality EQ-001 envelopes; see §11 naming note).

Only **CERTIFIED** or **CERTIFIED_WITH_WARNINGS** snapshots may enter Founder Preview for publication (warnings require explicit Founder acknowledgement — calibration or accept-as-is).

---

## 5. Lineage model (Curriculum Memory)

### 5.1 Principle

Every educational node preserves lineage so the Founder can always inspect why
the node exists.

### 5.2 Example

```
Conditional Probability
  Created:     Generation 1
  Modified:    Generation 4
  Merged with: Discrete Probability
  Evidence:    CMP pages 143–151
  Syllabus:    1.3.2
  Confidence:  94%
```

### 5.3 Domain shape

```
EducationalNode
  node_id                 # stable across generations (UUID)
  generation_local_id     # id within a snapshot
  title / kind / role
  parent_node_id
  confidence: ConfidenceRecord
  provenance: ProvenanceRecord
  lineage:
    created_generation
    last_modified_generation
    operations: [created | role_changed | reparented | merged | split | rejected | restored]
    related_node_ids      # merge/split partners
    syllabus_refs[]
    cmp_evidence[]
  active: bool            # false when rejected from active hierarchy
```

### 5.4 Memory laws

1. **Append-only operations log** — never rewrite history.
2. **Stable `node_id`** across generations when the educational identity continues.
3. **New `node_id`** only for genuine splits/creations; merges keep survivor id and record absorbed ids.
4. **Rejected ≠ deleted** — `active=false` + rejection reason; available for Gen N vs Gen N−k comparison.
5. CIP-002 `ProvenanceRecord` / `ConfidenceRecord` remain the evidence/score atoms; lineage wraps them with generation operations.

---

## 6. Regression engine

### 6.1 Quality vector

Every generation (and the original extract baseline) computes:

| Metric | Intent |
|---|---|
| Coverage | Syllabus objective completeness |
| Hierarchy | Parent justification + role-chain integrity |
| Duplicates | Duplicate-title / near-duplicate rate |
| Noise | Front-matter / non-curriculum contamination in active set |
| Granularity | Topic coherence / over-segmentation proxy |
| Confidence | Mean confidence + low-confidence share |

### 6.2 Acceptance rule

For optimisation generations (G2–G6):

```
IF quality_vector(candidate) is educationally worse than
     max(previous, previous-of-previous, original_ceiling_where_applicable)
   THEN reject optimisation
        rollback to last accepted snapshot
        record RegressionReport
        DO NOT allow silent degradation
```

“Worse” is defined by **weighted lexicographic gates**, not a single opaque score:

1. Coverage must not decrease beyond ε (default ε = 0).  
2. Noise must not increase beyond ε.  
3. Hierarchy score must not decrease beyond ε.  
4. Among remaining, prefer better granularity + confidence.

Exact weights live in domain policy (`RegressionPolicy`); Founder calibration may retune granularity bias **without** disabling coverage/noise hard gates.

### 6.3 Multi-generation validation

Example — Generation 5 analyses:

- Original source evidence / Gen 1 ceiling  
- Generation 3  
- Generation 4  

Never optimise using only one previous output. This prevents educational regression disguised as local improvement.

### 6.4 Rollback semantics

- Snapshot status → `rejected_by_regression`.  
- Active pointer remains on last `accepted` snapshot.  
- Orchestrator may retry with stricter parameters or surface Founder calibration.  
- No automatic “best effort publish” of a rejected generation.

---

## 7. Certification engine

### 7.1 Inputs

- Gen 6 reconciliation report  
- Quality vectors for G1…G6  
- Regression history  
- Lineage completeness checks (every active node has provenance + confidence)

### 7.2 Scores (normative outputs)

| Score | Derivation (high level) |
|---|---|
| Quality Score | Weighted blend of coverage, hierarchy, granularity, noise⁻¹, confidence |
| Confidence | Distribution summary over active nodes |
| Coverage | From Gen 6 matrix |
| Hierarchy Score | Parent justification rate × role-chain compliance |
| Granularity Score | Inverse over-segmentation + merge coherence signals |

### 7.3 Decisions

| Decision | Condition |
|---|---|
| `CERTIFIED` | All hard gates pass; warnings = 0 |
| `CERTIFIED_WITH_WARNINGS` | Hard gates pass; soft issues remain (e.g. cross-diet partial matches) |
| `NOT_CERTIFIED` | Hard gate fail — Preview publish path blocked |

Hard gates (initial, CS1-informed from EQ-001):

- Front-matter contamination = 0 in active hierarchy  
- Coverage completeness ≥ configured floor (EQ-001 observed ~0.93; floor programme-set)  
- No regression-rejected generation left as active head  
- Syllabus-first hierarchy when syllabus document present  
- Every active LO has syllabus ref **or** explicit “CMP-only support” flag

---

## 8. Founder calibration architecture

### 8.1 Role shift

Founder does **not** verify correctness of extraction.  
Founder **calibrates educational style**.

### 8.2 Calibration dimensions

| Dimension | Options |
|---|---|
| Granularity | Very Detailed · Balanced · Concept Focused |
| Hierarchy | Strict Syllabus · Balanced · Teaching Optimised |
| Topic Density | Fine · Balanced · Consolidated |
| Difficulty Bias | Exam Focused · Conceptual · Balanced |

### 8.3 Partial regeneration

Calibration settings rerun **only the affected optimisation generation(s)**:

| Setting change | Primary regen | May cascade |
|---|---|---|
| Granularity / Topic Density | Gen 4 | Gen 5–7 |
| Hierarchy style | Gen 3 | Gen 4–7 |
| Difficulty Bias | Gen 5 | Gen 6–7 |

**Never** rerun the full pipeline (extract → G1…) unless sources change or Gen 1/2 are invalidated.

```
CalibrationRouter
  → select generation subset
  → GenerationOrchestrator.run_from(N, profile=CalibrationProfile)
  → RegressionGuard
  → CertificationEngine
  → new Certified snapshot (lineage links to pre-calibration parent)
```

### 8.4 Workflow binding (FV-001A)

Calibration sits **after** Generation 7 certification and **before/within** Preview:

```
… → G7 Certified → [Optional Calibration] → Preview → Approve → Publish
```

Facts (additive to FV-001A):

| Fact | Meaning |
|---|---|
| `intelligence_certified` | Gen 7 decision is CERTIFIED or CERTIFIED_WITH_WARNINGS |
| `calibration_applied` | Founder saved a CalibrationProfile for this workspace version |
| `preview_built` | Hierarchy projected from certified (± calibrated) snapshot |

Founder still approves structure for release; calibration does not replace Approve.

---

## 9. Educational Review Pack

Generated for every engine run (and on calibration):

| Artefact | Purpose |
|---|---|
| Generation comparison report | Diff metrics and node deltas G(n) vs G(n−1)/G(n−2)/original |
| Curriculum lineage | Node-level created/modified/merged/rejected history |
| Coverage report | Syllabus ↔ curriculum matrix |
| Hierarchy report | Role-chain tree + parent justification failures |
| Optimisation metrics | Per-generation quality vector |
| Confidence report | Bands, low-confidence review queue |
| Regression report | Accepted vs rolled-back attempts |
| Educational certification report | Scores + decision |

Location convention:

`knowledge/evidence/releases/<run-id>/educational_review_pack/`  
(plus workspace-scoped runtime storage for Founder UI).

EQ-001 pack under `knowledge/engineering/eq001_educational_quality/educational_review_pack/` remains the **baseline evidence**; EI-001 supersedes the *format* with generation-aware artefacts.

---

## 10. Migration strategy from EQ-001

### 10.1 What EQ-001 delivered (keep)

| Asset | Migration |
|---|---|
| `ContentRole` + `NON_CURRICULUM_ROLES` | Domain vocabulary for Gen 1 labels / Gen 2 removals |
| `content_classification_service` | Gen 2 runner core |
| Front-matter / chrome / TOC gates | Gen 2 policy |
| Depth-aware hierarchy + nest sync | Gen 3 runner core |
| Syllabus-first structure prep | Gen 3 authority + Studio projection input = certified snapshot |
| `syllabus_reconciliation_service` | Gen 6 runner core |
| `educational_quality_audit_service` | RegressionGuard + Gen 7 inputs |
| Review pack concept | Expand to generation-aware pack |

### 10.2 What must change

| Today (one-pass) | Target (EI-001) |
|---|---|
| Parse-time drops discard noise early | Gen 1 retains all; Gen 2 soft-rejects |
| Map + graph = final curriculum | Intermediate snapshots; only certified head publishes |
| Structure prep reads CIP map entities | Structure prep reads certified generation snapshot |
| No rollback of educational optimisations | RegressionGuard mandatory |
| Founder “fixes” via re-upload / hope | Founder calibrates style dimensions |
| CMP coalescing deferred (EQ-001B) | Becomes Generation 4 |

### 10.3 Compatibility shims

1. **Adapter period:** `PipelineCoordinator` after `NORMALIZED` invokes `GenerationOrchestrator`; CIP stages `PARSED`/`MAPPED`/`GRAPH_BUILT` map to “engine progress” milestones for UI continuity.  
2. **Dual-read:** Structure prep accepts legacy CIP maps **or** certified snapshots; prefer snapshot when present.  
3. **No Student Runtime change** until republish.  
4. **Idempotent reprocess:** Re-running engine on same documents creates a new generation chain; prior chains remain auditable.

### 10.4 Ordering of delivery (see §12)

EQ-001 residual (CMP coalescing + live republish) is **absorbed** into EI-001 Gen 4 + certification dogfood — not a separate permanent one-pass patch track.

---

## 11. Naming and scope boundaries

| Name | Scope |
|---|---|
| **EI-001** | This Curriculum Intelligence Engine architecture |
| **EQ-001 (engineering CIP quality)** | 2026-07-30 extraction quality programme — predecessor evidence |
| **EQ-001 (product Runtime C)** | Mission/plan/journey educational quality certification — **orthogonal**; remains Runtime C authority |

Do not conflate curriculum-structure certification (Gen 7) with student-facing mission quality envelopes. Both must remain explainable and deterministic; they certify different artefacts.

---

## 12. Implementation roadmap

### Phase A — Domain & persistence (foundation)

- Domain: `Generation`, `EducationalNode` lineage, `QualitySnapshot`, `RegressionPolicy`, `CertificationDecision`, `CalibrationProfile`
- Generation store (immutable snapshots + active pointer)
- Extend CIP-002 provenance/confidence linkage to lineage operations
- **Exit:** Contracts + empty orchestrator + persistence tests

### Phase B — Generations 1–3 (construct)

- Gen 1 raw graph (retain-all)
- Gen 2 noise elimination (EQ-001 classifier lifted)
- Gen 3 hierarchy (syllabus-first)
- RegressionGuard online for G2–G3
- **Exit:** CS1 syllabus path reproduces EQ-001 5/15/73 shape with lineage

### Phase C — Generations 4–6 (optimise & reconcile)

- Gen 4 topic consolidation (close CMP ~936 debt)
- Gen 5 objective intelligence
- Gen 6 reconciliation (coverage matrix)
- Multi-parent validation enforced
- **Exit:** CMP instructional map coherent; coverage ≥ EQ-001 floor; regression reports green on CS1 fixtures

### Phase D — Generation 7 + Review Pack

- CertificationEngine + hard gates
- Full Educational Review Pack emitter
- Studio structure prep reads certified snapshot
- **Exit:** `CERTIFIED` decision on CS1 dogfood artefacts

### Phase E — Founder calibration

- CalibrationProfile + CalibrationRouter partial regen
- Founder Console controls (style, not node editing)
- FV-001A facts: `intelligence_certified`, `calibration_applied`
- **Exit:** Changing Topic Density regenerates G4+ only; lineage inspectable

### Phase F — Live validation

- Reprocess live CS1 workspace; republish
- Student missions sourced from certified hierarchy
- Evidence pack under `knowledge/evidence/releases/`
- **Exit:** Monotonic quality vs EQ-001 baseline; Founder dogfood pass

---

## 13. Technical debt

| Debt | Origin | EI-001 treatment |
|---|---|---|
| CMP topic over-segmentation (~936) | EQ-001 | Gen 4 |
| Live CS1 still on pre-EQ-001 package | EQ-001 | Phase F republish |
| 2019 CMP vs 2026 syllabus diet mismatch | EQ-001 | Gen 6 partial coverage + CERTIFIED_WITH_WARNINGS |
| PDF line wrapping / OCR debris | CIP extract | Gen 1 retain + Gen 2/5 stitching rules |
| Objective-hint false positives | EQ-001 | Gen 5 stricter grammar |
| CMP teaching assets not bound under syllabus LOs | EQ-001 | Gen 5/6 attach as support entities, not hierarchy topics |
| One-pass CIP stages UI labels | CIP-001 | Shim milestones until Founder strip shows generations |
| Structure prep dual-read shim | Migration | Remove after all workspaces certified |
| Product EQ-001 name collision | Historical | Document boundary (§11); rename only in a dedicated docs programme |

---

## 14. Success metrics

| Metric | Target |
|---|---|
| Educational quality measurable | Quality vector on every generation |
| Every optimisation explainable | reason + confidence + evidence required |
| No silent concept removal | Rejected nodes retained; coverage hard gate |
| Founder calibrates, not edits | Calibration dimensions drive partial regen |
| Curriculum lineage preserved | Curriculum Memory for every node |
| Optimisations reversible | Regression rollback to last accepted snapshot |
| Quality increases monotonically | RegressionGuard rejects regressions |
| Educational confidence measurable | ConfidenceRecord on every active node |
| Certification decision explicit | Gen 7 CERTIFIED / WARNINGS / NOT_CERTIFIED |

---

## 15. Architecture compliance checklist

| Invariant | Status in this design |
|---|---|
| Layered Presentation → Application → Domain → Infra | Preserved |
| No LLM in educational decisions | Preserved |
| Deterministic cores | Preserved |
| CIP ingress / Studio publish egress | Preserved |
| V1/V2 curriculum engine loadable | Untouched until optional projection |
| Student Twin / Mission / Tutor isolation | Preserved |
| Alembic for durable schema | Required in Phase A (generation store) |
| Explainability | Lineage + Review Pack + calibration diffs |

---

## 16. Known limitations (architecture-level)

1. **Heuristic coherence (Gen 4/5)** remains rule-based; actuarial expert review of Review Packs still informs denylists and merge dictionaries.  
2. **Cross-diet semantic matching** cannot invent missing 2026 content from a 2019 CMP — certification may warn, not fabricate.  
3. **Calibration is style, not correctness** — Founder cannot “approve away” a NOT_CERTIFIED hard-gate failure without changing sources or policy floors.  
4. **UI generation strip** is not specified as a full redesign here; FV-001A remains the Founder publication strip with additive certification/calibration facts.  
5. **Implementation is not delivered by this document** — readiness below is architectural readiness only.

---

## 17. FINAL DECISION

# CURRICULUM INTELLIGENCE ARCHITECTURE READY

### Why READY

1. The multi-generation model cleanly supersedes the one-pass parser without abandoning CIP ingress, CIP-002 evidence atoms, or FV-001A publication workflow.  
2. EQ-001 assets map 1:1 onto Generations 2, 3, 5, 6 and certification inputs; EQ-001 residual CMP debt has a named home (Gen 4).  
3. Curriculum Memory, RegressionGuard, CertificationEngine, and CalibrationRouter form a complete educational control plane: measurable, explainable, reversible, monotonic.  
4. Migration shims (dual-read structure prep, CIP stage labels) keep Student Runtime and live workspaces safe during rollout.  
5. No architectural contradiction with Educational Intelligence authorities (Twin, Reasoning, Mission, Tutor, Retrieval) — EI-001 certifies curriculum structure **before** those consumers.

### What READY does **not** mean

- Engine code is not yet shipped.  
- EQ-001 educational-quality **product** decision remains BLOCKED until Phase C–F close CMP coherence and live republish evidence.  
- Architecture READY authorises implementation programmes (Phases A–F); it does not declare Version 1 curriculum-intelligence complete.

### Immediate next programme

**EI-001A — Domain contracts + Generation store + Orchestrator skeleton (Phase A)**, then **EI-001B — Generations 1–3 with RegressionGuard (Phase B)** reproducing the EQ-001 syllabus-first 5/15/73 baseline with lineage.
