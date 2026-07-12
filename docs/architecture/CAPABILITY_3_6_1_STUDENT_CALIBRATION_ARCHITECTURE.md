# Capability 3.6.1 — Initial Student Calibration Architecture

**Status:** Architecture only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.6.1 Initial Student Calibration (Application Layer Twin-birth prior construction preceding Twin Persistence and Evidence loops)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Upstream Twin retrieval:** [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md)  
**Upstream orchestration:** [`CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md`](CAPABILITY_3_2_EDUCATIONAL_ORCHESTRATION_ARCHITECTURE.md)  
**Product law:** [`docs/product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md`](../product/EPIC_3_PRODUCT_INTEGRATION_BLUEPRINT.md)  
**Persistence debt:** Technical Debt Register **E2-PE-01** (Twin persistence) — related, not owned here  
**Scope:** Structural architecture for Initial Student Calibration — capturing self-declared educational history into truthful Twin *priors* before persistence and Evidence loops exist — **no code, Flask, routes, database, UI, schemas, migrations, or tests**

---

## Document purpose

Internal Alpha preparation exposed an educational gap:

> The product currently treats every new Study Plan as if the student is a beginner.

That assumption is false for returning students — candidates who have completed Core Reading, previously attempted an IFoA paper, or already covered sections of the syllabus.

Educational Intelligence must begin from a **truthful initial Digital Twin**, not from an implicit zero-knowledge birth.

This capability defines **Initial Student Calibration**: the architectural contract for capturing self-declared educational history at Twin birth / Study Plan creation, and mapping that history into Digital Twin structure as **priors only**.

**Governing principle (binding):**

> **Calibration captures history. It never reasons. Priors are not truth.**

**Architectural restatement:**

> **Initial Student Calibration is an Application Layer Twin-birth constructor. It records what the student declares about their educational past and objective. It never infers mastery, confidence, readiness, predicted marks, or recommendations. Educational Intelligence remains the sole owner of educational judgement. Learning Evidence remains the sole owner of evidence-backed belief evolution. Twin Persistence remains the sole owner of durable snapshot storage.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Initial Student Calibration** | Self-declared educational history → Twin priors at birth (this capability) |
| **Confidence calibration** (Epic 2 deferred) | Separable Confidence domain / measured-vs-felt calibration — **not** this capability |
| **Prediction / model calibration** | Forecast accuracy against outcomes — **not** this capability |

**Non-goals of this document**

- Code, pseudocode, dataclasses, service class designs, or package layouts  
- Flask routes, forms, templates, wizard steps, or premium UX copy  
- Database schemas, Alembic migrations, or ORM adapters  
- Redesign of Evidence, Twin Update Pipeline, Readiness, Decision, Recommendation, or Mission  
- Implementation of TwinRepository / Twin Persistence (E2-PE-01)  
- Diagnostic assessments, mocks, or any assessed baseline that would produce Learning Evidence  
- Inferring or inventing educational beliefs from declared history  

---

# 1. Purpose

## 1.1 Why Initial Student Calibration exists

Without Calibration:

- Every new Study Plan births an empty Twin and product behaviour treats the student as a beginner.  
- Returning students receive foundations-first guidance that contradicts their real history.  
- TwinProvider / Internal Alpha cold-start sources can only supply Identity + empty domains — honest about *absence of evidence*, but dishonest about *known educational history*.  
- Study Plan wizard facts (exam, sitting, hours) become planning inputs without becoming Twin priors.  
- Pressure rises later to “fix cold start” by inventing Mid mastery or readiness theatre — exactly what TwinProvider architecture forbids on the read path.

**Initial Student Calibration** exists to:

1. **Capture** self-declared educational history at Twin birth (or Study Plan creation that births a Twin).  
2. **Establish priors** on the Digital Twin so Educational Intelligence starts from a non-zero, non-beginner-assuming structural position when the student says they are not a beginner.  
3. **Preserve honesty** — every calibrated field remains tagged as self-declared prior, never as assessed belief.  
4. **Bridge the gap** between “no Evidence yet” and “student already has educational history outside the product.”  
5. **Refuse educational reasoning** — Calibration never answers *what to study next*, *how ready*, or *how mastered*.

It is the lawful answer to:

> “What does the student *say* about their educational past and objective before Learning Evidence exists?”

It is **not** the answer to:

> “What does Educational Intelligence *believe* about the student?”

```
Self-declared educational history
              ↓
   Initial Student Calibration     ← Application Twin-birth prior constructor (this document)
              ↓
   Digital Twin (priors + Identity / Goals)
              ↓
   Twin Persistence (future)       ← stores the birth snapshot
              ↓
   TwinProvider → Orchestrator     ← retrieves what exists
              ↓
   Readiness → Decision → Recommendation → Mission
```

Governing restatement:

> **Begin from what the student declares. Never pretend declaration is mastery. Never invent Mid readiness to fill the gap.**

---

# 2. Educational philosophy

These principles bind Calibration. They extend ADR-002, STUDENT_DIGITAL_TWIN, and Epic 3 product honesty into Twin birth.

### Educational history is self-reported

Calibration records what the student *claims*: previously studied material, Core Reading completion, prior exam attempts, declared completed sections, current objective, intended sitting. The product did not observe these events. They are not Learning Evidence.

### Self-report establishes priors, not educational truth

A prior shapes the Twin’s starting structure. It does not certify mastery, retention, exam readiness, or pass probability. Educational Intelligence may later *consume* priors under thin warrant; it must never treat them as assessed Performance or dense Knowledge belief.

### Calibration is not educational reasoning

Calibration does not score, select, rank, forecast, or recommend. If a step requires educational judgement, it belongs to Readiness, Decision, Recommendation, Mission, or Twin Update Strategies — not here.

### Declared coverage ≠ mastery

“I completed Core Reading for Section X” means **declared exposure / coverage prior**. It must never write `mastery_belief`, Confidence, or readiness bands.

### Declared attempts ≠ measured performance

“I sat CS1 previously” means **declared attempt history**. It must never invent mock scores, pass/fail beliefs, or predicted marks.

### Evidence remains sovereign for belief evolution

After birth, Learning Evidence → Twin Update Pipeline is the only lawful path that evolves Knowledge, Memory, Behaviour, and Performance beliefs. Calibration does not reopen a second write authority that bypasses Evidence.

### Cold-start honesty survives Calibration

A calibrated Twin may be non-empty in structure and still **thin in warrant**. Product language must remain cold-start / thin-warrant honest until Evidence densifies. Calibration reduces beginner-assumption falsehood; it does not authorise Mid/High preparedness theatre.

### Curriculum remains syllabus truth

Declared completed sections must reference canonical curriculum identities (V1 topics or V2 sections/topics via Curriculum authority). Calibration never invents syllabus structure or free-text topics as Twin identities.

### One Twin birth story

Calibration is the Twin-birth prior path for students who declare history. Students who declare true beginner status still birth a Twin — with empty educational-history priors and explicit beginner declaration — not a silent zero fabricated as Mid.

Governing restatement:

> **Priors are honest starting structure. Truth is earned by Evidence. Judgement belongs to Educational Intelligence.**

---

# 3. Ownership

## 3.1 Initial Student Calibration owns

| Responsibility | Meaning |
|---|---|
| **History capture contract** | Define which self-declared educational-history fields may be collected at Twin birth / Study Plan creation. |
| **Prior construction** | Map validated declarations into Digital Twin structural priors (Identity / Goals anchors + history prior markers) without computing educational beliefs. |
| **Provenance tagging** | Ensure every calibrated field carries explicit self-declared / calibration-prior provenance so downstream domains cannot mistake priors for assessed Evidence. |
| **Beginner vs returning posture** | Record whether the student declares beginner or non-beginner history — as a declared posture, not as a readiness band. |
| **Structural validation** | Ensure declared curriculum references are syllabus-legal (canonical ids via Curriculum helpers) and sitting / objective fields are structurally coherent. Fail or degrade honestly when validation cannot pass. |
| **Immutable emission** | Emit a birth Twin snapshot (or CalibrationResult containing that snapshot) that downstream Persistence / TwinProvider can store and retrieve — without mutating it educationally. |

Calibration is a **Twin-birth Application constructor**. Educational Orchestrator remains the composition conductor for daily guidance. Domains remain educational judgement owners. Twin Persistence remains durable storage. Evidence remains append-only study truth.

## 3.2 Initial Student Calibration never owns

| Forbidden ownership | Why |
|---|---|
| **Mastery inference** | Knowledge beliefs evolve from Learning Evidence via Twin Update Strategies. Declared Core Reading / sections must not become mastery scores. |
| **Confidence inference** | Self-report Confidence (and Confidence calibration domain) is separable and deferred. Calibration history must not invent Confidence. |
| **Readiness judgement** | Preparedness belongs to Readiness Aggregation. Calibration never emits readiness bands or overall %. |
| **Predicted marks / pass probability** | Predictions belong to Predictions domain / later calibrated forecasting. Calibration never forecasts. |
| **Educational recommendations** | Next-action selection belongs solely to Decision Engine; packaging to Recommendation; execution to Mission. |
| **Learning Evidence authorship** | Declared history is not study Evidence. Fabricating Evidence rows from Calibration would poison the audit spine. |
| **Twin Persistence schema** | Durable storage belongs to future TwinRepository (E2-PE-01). Calibration produces the birth snapshot; Persistence stores it. |
| **Twin retrieval honesty policy** | TwinProvider owns DigitalTwin \| TwinAbsent on the read path. Calibration must not become a read-path “fabricate Twin if missing” escape hatch. |
| **Curriculum ownership** | Syllabus structure and traversal belong to Curriculum Engine / `CurriculumService`. |
| **Constraint / session feasibility** | Session bounds belong to ConstraintBuilder. Calibration is educational-history priors, not study-minute construction. |

### Owner map (no duplication)

| Concept | Layer | Relation to Calibration |
|---|---|---|
| **Initial Student Calibration** | Application | Twin-birth prior constructor; history capture → structural priors |
| **TwinProvider** | Application | Read-path retrieval only; never invents birth Twin; loads what Calibration + Persistence left behind |
| **TwinRepository** (future) | Application | Durable persist/load of Twin snapshots including calibrated birth state |
| **EvidenceRecorder** | Application | Write-path Learning Evidence bridge — separate from Calibration |
| **CurriculumContextBuilder** | Application | Syllabus context for orchestration — not history capture |
| **ConstraintBuilder** | Application | Feasibility bounds — not educational history |
| **Student Digital Twin** | Domain | Authoritative learner-state aggregate; Calibration may *initialise* structure, never *reason* about it |
| **Twin Update Pipeline** | Domain | Sole lawful Evidence-driven mutation path after birth |
| **Readiness / Decision / Recommendation / Mission** | Domains | Downstream consumers; never implemented inside Calibration |
| **Study Plan Wizard / product surfaces** | Presentation | May collect declarations; must not perform educational math locally |

### Ownership invariants

1. **Calibration does not reason about the student educationally.** Capture, validate structure, map priors, emit.  
2. **Calibration does not invent Evidence.** Self-report history ≠ Learning Evidence.  
3. **Calibration does not invent Mid readiness or mastery.** Thin warrant is mandatory.  
4. **Calibration is write-at-birth, not read-path fabrication.** TwinProvider remains retrieve-or-absent.  
5. **Domains never import Calibration.** They receive Twin snapshots as arguments.  
6. **Presentation never bypasses Calibration** to write mastery / readiness into Twin or legacy stores as “quick setup.”

Governing restatement:

> **Calibration answers only: “What educational history and objective did this student declare at Twin birth?” It never answers educational questions about preparedness or next action.**

---

# 4. Inputs

Calibration accepts only what Twin-birth prior construction requires. It does not accept product pressure to invent mastery, and it does not accept Evidence streams (those do not exist yet at lawful Calibration time).

## 4.1 Required identity and syllabus scope

| Input | Meaning |
|---|---|
| **Authorised student identity** | The student whose Twin is being born. Ownership must already be validated by Presentation / Application before Calibration runs. |
| **Curriculum / exam scope** | Canonical curriculum identity (and exam / paper label when known) the Twin is scoped to. Calibration never invents a syllabus. |

## 4.2 Allowed educational-history declarations

These are the **only** educational-history fields Calibration may capture in this capability. All are self-declared.

| Input | Meaning | Educational meaning (limited) |
|---|---|---|
| **Previously studied** | Student declares they have studied this paper / syllabus before (boolean or coarse posture). | Exposure prior — not mastery. |
| **Completed Core Reading** | Student declares Core Reading completion (whole paper and/or section-scoped where syllabus supports it). | Declared coverage prior — not mastery or retention. |
| **Previous exam attempts** | Student declares prior sitting attempts (count and/or sitting labels when known; pass/fail only if explicitly declared as history fact, never as predicted mark). | Attempt-history prior — not Performance belief from mocks. |
| **Declared completed sections** | Student declares sections (V2) or equivalent topic groupings (V1-safe mapping via Curriculum helpers) already completed in their own study. | Declared syllabus-position prior — not weighted coverage score or mastery map. |
| **Current objective** | What the student is trying to achieve now (e.g. first sit, re-sit, revise after Core Reading, finish remaining sections). | Goals posture — not readiness. |
| **Intended sitting** | Target exam sitting / date the student is aiming for. | Identity / Goals anchor — not completion forecast. |

## 4.3 Optional product sitting facts (non-educational)

| Input | Meaning |
|---|---|
| **Declared study capacity** (if already collected by Study Plan) | Hours / availability the student commits — may inform Goals capacity fields structurally; must not become Behaviour adherence or burnout judgement. |
| **Beginner declaration** | Explicit “I am starting from scratch” — lawful empty-history prior posture. |

## 4.4 Forbidden inputs (must be rejected if offered as Calibration authority)

| Forbidden input | Why |
|---|---|
| Mastery percentages, readiness %, predicted marks | Educational judgement — not history capture |
| Legacy `TopicProgress` / heuristic readiness composites as birth truth | Parallel learner stores — Stage A dual truth, not Calibration authority |
| Fabricated Learning Evidence “seed” rows | Poisons Evidence sovereignty |
| LLM-inferred history from free text without explicit student confirmation of the closed field set | Opaque inference — violates explainability and self-report discipline |
| Confidence ratings treated as readiness or mastery | Separability law |

### Input invariant

> **If the student did not declare it in the closed Calibration field set, Calibration must not invent it.**

---

# 5. Outputs

## 5.1 Primary output

| Output | Meaning |
|---|---|
| **Calibrated birth Twin** | A Digital Twin snapshot whose Identity / Goals are anchored, and whose educational-history priors are structurally present with self-declared provenance — Belief domains that Calibration does not lawfully initialise remain empty. |

## 5.2 Accompanying calibration metadata (conceptual)

| Output | Meaning |
|---|---|
| **Calibration provenance** | Explicit marker that Twin birth included Initial Student Calibration (timestamp conceptual; source = self_declared). |
| **Declared posture** | Beginner \| Returning / history-declared (coarse), derived only from closed declarations — not a readiness band. |
| **Warrant posture** | Mandatory thin / self-declared warrant for all history priors until Evidence supersedes. |
| **Validation outcome** | Accepted \| Partially accepted (unknowns preserved) \| Rejected (structural failure) — never silently coerced into Mid beliefs. |

## 5.3 Closed output law

Calibration may emit:

1. **Calibrated birth Twin** (+ metadata), or  
2. **Calibration failure / honest degradation** when required identity/syllabus scope is missing or declarations are structurally unlawful.

Calibration must **never** emit:

- Readiness summary or preparedness band  
- Decision / Recommendation / Mission  
- Mastery beliefs, Confidence beliefs, or predicted marks  
- Learning Evidence records  
- A Twin that TwinProvider could mistake for Evidence-dense Mid preparedness  

### Output invariant

> **Calibration output is a Twin *prior snapshot*, not an Educational Experience and not an Evidence batch.**

---

# 6. Mapping into Digital Twin

Mapping is **structural placement of priors**. It is not belief computation.

## 6.1 Domain mapping table

| Calibration input | Twin domain | Lawful mapping | Forbidden mapping |
|---|---|---|---|
| Authorised student identity | **Identity** | `student_id` | Auth secrets, other users’ ids |
| Curriculum / exam scope | **Identity** | `curriculum_id`, `current_exam` | Invented syllabus nodes |
| Intended sitting | **Identity** and/or **Goals** | `target_sitting` / target completion date as declared | Completion forecast, risk-of-missing-date |
| Current objective | **Goals** | Structural goal posture / objective label as declared | Readiness target as preparedness truth; Decision selection |
| Declared study capacity (optional) | **Goals** | `planned_study_hours_per_week` when declared | Behaviour adherence, burnout flags |
| Previously studied | **Knowledge** (prior marker) | Coarse self-declared exposure prior at paper/syllabus scope, provenance = self_declared | `mastery_belief` fill; Memory strength; Readiness upgrade |
| Completed Core Reading | **Knowledge** (prior marker) | Declared Core Reading completion prior (paper and/or section-scoped ids), provenance = self_declared | Equating Core Reading with mastery or exam readiness |
| Declared completed sections | **Knowledge** (prior marker) | Structural “declared complete” markers keyed by canonical section/topic ids via Curriculum helpers | Weighted coverage %, mastery map, skipping foundations by policy inside Calibration |
| Previous exam attempts | **Performance** (prior marker) *or* Calibration metadata bag consumed later by Performance strategies | Declared attempt history (count / sitting labels / declared outcome only if student stated it as history) | Mock score invention; pass probability; Assessment Performance warrant upgrade |
| Beginner declaration | Calibration metadata + empty history priors | Explicit empty-history posture | Fabricating Mid empty Twin theatre |
| Memory / Behaviour / Predictions | — | Remain **empty** at Calibration | Decay curves, streak theatre, pass forecasts |

## 6.2 Knowledge mapping rule (binding)

Declared Core Reading and declared completed sections create **coverage / exposure priors**, not TopicMastery beliefs.

Architectural rule:

> **Calibration may mark that the student *declared* prior engagement with a curriculum node. It must not write assessed mastery, retention, or confidence into Knowledge.**

Downstream Educational Intelligence may interpret declared coverage under thin warrant (e.g. avoid absolute beginner assumptions). It must still prefer Evidence when Evidence exists, and must not treat declaration as permission to skip foundations without Decision authority.

## 6.3 Performance mapping rule (binding)

Previous exam attempts create **attempt-history priors**, not Performance summaries.

Architectural rule:

> **Calibration may record that attempts occurred. It must not invent marks, grade beliefs, or exam-condition Performance warrant.**

## 6.4 Empty domains are intentional

Empty Memory, Behaviour, and Predictions at birth after Calibration is **correct**. Declaring history does not imply retention schedules, study habits, or forecasts.

## 6.5 Provenance is part of the Twin story

Every calibrated prior must remain distinguishable from Evidence-backed state for the life of the Twin until superseded — conceptually tagged `self_declared` / `calibration_prior`. Analytics, Coach, and Decision risk-framing must be able to see that distinction.

Governing restatement:

> **Map declarations into structure. Leave belief evolution to Evidence. Leave judgement to Educational Intelligence.**

---

# 7. Boundaries

## 7.1 Hard boundary — what Calibration may do

- Collect the closed self-declared field set  
- Validate curriculum identities through Curriculum authority (V1/V2 safe)  
- Construct Identity / Goals anchors  
- Attach structural history priors with thin warrant  
- Emit calibrated birth Twin (+ metadata)  
- Record beginner vs returning declared posture  

## 7.2 Hard boundary — what Calibration must never do

| Forbidden act | Rationale |
|---|---|
| Infer mastery from Core Reading or completed sections | Mastery is Evidence-driven |
| Infer Confidence | Separable / deferred; self-report Confidence ≠ Calibration history |
| Infer readiness or overall preparedness | Readiness Aggregation only |
| Infer predicted marks or pass probability | Predictions / later calibration only |
| Produce educational recommendations or next actions | Decision / Recommendation only |
| Compose missions or filler tasks | Mission Intelligence only |
| Author Learning Evidence from declarations | Evidence sovereignty |
| Fabricate Twins on the TwinProvider read path | Retrieve-or-absent law |
| Average legacy % progress into birth Twin | Dual-truth prohibition |
| Treat Study Plan rows as Twin authority | Plans are consequences, not learner truth |
| Perform diagnostic scoring inside Calibration | Diagnostics produce Evidence; different path |

## 7.3 Boundary with Study Plan Wizard

The Study Plan Wizard may **collect** Calibration inputs as part of plan creation UX. It must not:

- Become a parallel mastery store  
- Feed planning heuristics that silently assume beginner when Calibration declared otherwise  
- Bypass Twin birth and write only ORM plan progress as “the learner”  

Wizard collects; Calibration maps to Twin priors; Planning remains a consequence of intelligence + constraints — not the Twin.

## 7.4 Boundary with Internal Alpha cold-start

`InternalAlphaTwinSource` (Identity + empty domains) remains an **interim honesty device** when no Twin exists. Calibration, once implemented, is the lawful way to birth a non-beginner-assuming Twin. Alpha empty Twin must not be “upgraded” into Mid beliefs to simulate Calibration.

## 7.5 Boundary with diagnostic assessment

STUDENT_DIGITAL_TWIN names diagnostic assessment as a high-warrant cold-start path. Diagnostics are **not** Calibration:

| | Initial Student Calibration | Diagnostic assessment |
|---|---|---|
| Source | Self-declaration | Assessed performance / structured probe |
| Output | Priors | Learning Evidence → Pipeline beliefs |
| Warrant | Thin / self_declared | Higher at birth when assessed |
| This capability | Yes | Out of scope (future Evidence path) |

Governing restatement:

> **Calibration ends where educational judgement, Evidence authorship, or persistence schema begin.**

---

# 8. Relationship with Twin Persistence

## 8.1 Sequencing

```
Calibration (birth priors)
        ↓
Twin Persistence / TwinRepository (store birth snapshot)     ← E2-PE-01 future
        ↓
TwinProvider (retrieve DigitalTwin | TwinAbsent)
        ↓
Educational Orchestrator (compose day)
```

## 8.2 Ownership split

| Concern | Owner |
|---|---|
| What priors mean and how declarations map | **Initial Student Calibration** (this document) |
| How snapshots are stored, versioned, loaded | **TwinRepository / Twin Persistence** (future) |
| Whether a Twin exists for orchestration today | **TwinProvider** |

## 8.3 Rules

1. **Calibration does not replace Twin Persistence.** Without Persistence, calibrated birth state cannot survive sessions; that is debt (E2-PE-01), not a license for TwinProvider fabrication.  
2. **Persistence must preserve provenance.** Storing a calibrated Twin must not strip `self_declared` markers or rebrand priors as Evidence-backed mastery.  
3. **Re-calibration is not casual rewrite.** Later product flows that allow history correction must be explicit Calibration (or Evidence) events — not silent ORM edits of Twin beliefs.  
4. **TwinProvider never calibrates.** If Twin is absent, Provider signals `TwinAbsent`; product may route the student to Calibration — Provider must not invent priors to avoid absence.  
5. **Write/read firewall preserved.** Calibration is a birth/write-at-birth Application path. Dashboard composition remains load-only via TwinProvider.

### Persistence invariant

> **Twin Persistence changes *where* the calibrated birth Twin lives. It does not change *that* Calibration only writes priors, never educational judgements.**

---

# 9. Relationship with Evidence

## 9.1 Separation of authorities

| Authority | Question answered | Timing |
|---|---|---|
| **Initial Student Calibration** | What did the student *declare* about history and objective at birth? | Twin birth / plan creation |
| **Learning Evidence** | What study / assessment events does the product *observe*? | Ongoing after product use |
| **Twin Update Pipeline** | How do Evidence + prior Twin evolve beliefs? | After Evidence exists |

## 9.2 Calibration is not Evidence

Creating Evidence rows from “completed Core Reading” declarations would:

- Falsify the append-only audit spine  
- Inflate Knowledge warrant  
- Teach Decision that sparse self-report is assessed Performance  

Therefore Calibration **must not** call EvidenceRecorder to seed fake study events.

## 9.3 How Evidence supersedes priors

Architectural expectation (not implementation):

1. Birth Twin contains self-declared priors.  
2. Real study produces Learning Evidence.  
3. Twin Update Strategies evolve Knowledge / Memory / Behaviour / Performance.  
4. Evidence-backed state **dominates** conflicting self-declared priors for educational judgement.  
5. Priors may remain visible as lineage / audit (“student declared Core Reading complete at birth”) without continuing to act as mastery.

## 9.4 Manual confidence and Calibration

STUDENT_DIGITAL_TWIN allows manual confidence adjustment as a tagged self-report channel. That channel is **not** Initial Student Calibration. Confidence remains separable. Calibration history fields must not be smuggled in as Confidence ratings or readiness upgrades.

### Evidence invariant

> **Evidence is observed. Calibration is declared. Only Evidence may densify educational belief warrant.**

---

# 10. Product flow

Conceptual product flow only — no routes, wizard wireframes, or UI.

```
Student creates / starts Study Plan for a syllabus + sitting
        ↓
Product asks closed Calibration questions (self-declared history + objective)
        ↓
Initial Student Calibration validates + maps → birth Twin priors
        ↓
(Future) Twin Persistence stores birth Twin
        ↓
TwinProvider can retrieve Twin (no longer forced empty-beginner assumption)
        ↓
Educational Orchestrator composes Experience under thin warrant
        ↓
Student studies → EvidenceRecorder → Twin Update Pipeline
        ↓
Evidence-backed Twin evolves; priors lose authority where Evidence conflicts
```

### Flow rules

1. **Calibration precedes Educational Intelligence claims about the returning student.**  
2. **Calibration may be skipped only with explicit beginner declaration** — skipping must not silently mean “assume Mid.”  
3. **Absence of Calibration + absence of Twin ⇒ TwinAbsent / empty cold-start honesty** — not fabricated returning-student theatre.  
4. **Study Plan generation remains downstream** of Twin + Curriculum + constraints — Calibration does not become a second planner.  
5. **Daily Mission / Recommendation paths never re-run Calibration as selection.** Birth happens once per Twin scope (with explicit re-calibration events only when product allows history correction).

### Minimum educational honesty in product language (conceptual)

After Calibration, product may truthfully say the Twin *includes self-declared history*. It must not say the student is Mid/High ready, has mastery of declared sections, or is predicted to pass.

---

# 11. Risks

| Risk | Failure mode | Mitigation principle |
|---|---|---|
| **Prior → mastery collapse** | Declared Core Reading / completed sections written as `mastery_belief` or coverage %. | Mapping law: priors only; no mastery writes; review gate rejects belief fill. |
| **Prior → readiness theatre** | Returning posture coerced into Mid/High readiness for “better UX.” | Readiness remains Aggregation-only; thin warrant mandatory; Experience Contract honesty preserved. |
| **Fake Evidence seeding** | Calibration inserts Evidence rows so Pipeline “has something to chew.” | Hard ban: Calibration never authors Learning Evidence. |
| **TwinProvider fabrication** | Missing Twin path “calibrates empty defaults” on dashboard load. | Provider retrieve-or-absent; Calibration is explicit birth flow, not read-path escape. |
| **Beginner assumption remains** | Architecture exists but wizard still assumes zero knowledge for planning / missions. | Product cutover must consume calibrated Twin; legacy beginner defaults freeze as dual-truth debt until Stage C. |
| **Curriculum-unsafe declarations** | Free-text sections or invalid ids enter Twin. | Curriculum helper validation; V1/V2 safe identity mapping only. |
| **Re-calibration drift** | Students edit history casually; Twin oscillates without lineage. | Explicit re-calibration events; provenance retained; no silent belief rewrites. |
| **Confidence conflation** | Calibration confused with Confidence calibration domain. | Naming disambiguation binding; Confidence remains out of scope. |
| **Persistence without provenance** | TwinRepository stores priors as if Evidence-backed. | Persistence must preserve self_declared markers (E2-PE-01 acceptance condition). |
| **Over-trust of self-report** | Decision skips foundations because student declared completion. | Decision / Readiness consume priors under thin warrant only; self-report never upgrades selection into exam-rehearsal-only without Evidence. |

### Risk restatement

The primary danger is not missing Calibration. It is **Calibration that starts reasoning** — turning self-report into mastery, readiness, or recommendations and recreating the beginner-assumption problem as an *overconfidence* problem.

---

# 12. Recommendations

## 12.1 Architectural recommendations (binding for later implementation)

1. **Implement Calibration as an Application Twin-birth constructor**, parallel in discipline to ConstraintBuilder / CurriculumContextBuilder — capture, validate, map, emit; no educational math.  
2. **Keep the closed input set** from §4.2; expand only via a new architecture revision, not ad-hoc wizard fields that imply mastery.  
3. **Mandate provenance** (`self_declared` / `calibration_prior`) on every history prior before any Persistence milestone accepts calibrated snapshots.  
4. **Sequence after TwinProvider contract, with Twin Persistence** — Calibration without Persistence cannot survive sessions; Persistence without Calibration re-ships beginner falsehood for returning students.  
5. **Do not seed Evidence from Calibration.** Prefer empty Evidence + explicit priors over fake Evidence density.  
6. **Preserve TwinProvider honesty.** Calibration is a product birth flow; absence on read path remains `TwinAbsent`.  
7. **Teach Decision / Readiness (later) to consume priors under thin warrant** — never as mastery or Assessment Performance.  
8. **Keep V1/V2 safe** — declared completed sections resolve through Curriculum helpers only.  
9. **Separate diagnostics** — assessed baselines remain a future Evidence path; do not overload Calibration.  
10. **Name carefully in code and docs** — avoid `calibrate()` methods on Readiness or Predictions that collide with this capability’s meaning.

## 12.2 Implementation sequence (when authorised — not authorised by this document)

1. Architecture acceptance of this document  
2. Twin prior representation design (structural markers + provenance) without mastery fields  
3. Application Calibration constructor + validation via Curriculum helpers  
4. Twin Persistence storing calibrated birth Twin with provenance  
5. Study Plan creation flow collects closed declarations (UI later)  
6. Orchestration / Decision thin-warrant consumption of priors  
7. Explicit rejection tests: no mastery inference, no readiness emission, no Evidence seeding  

## 12.3 Explicit non-recommendations

- Do not “fix” Internal Alpha by inventing Mid Twin beliefs.  
- Do not treat legacy TopicProgress as Calibration.  
- Do not let LLM paraphrase become undeclared syllabus completion.  
- Do not ship Calibration UI before the prior-mapping contract is stable.  

---

# 13. Architecture Compliance Summary

| Invariant | Status under this architecture |
|---|---|
| Application does not perform educational reasoning | Preserved — Calibration is capture/map/emit only |
| Twin beliefs evolve from Evidence → Pipeline | Preserved — Calibration writes priors, not Evidence-backed beliefs |
| TwinProvider never fabricates | Preserved — birth flow ≠ read-path fabrication |
| Decision sole next-action authority | Preserved — Calibration emits no recommendations |
| Readiness owns preparedness | Preserved — Calibration emits no readiness |
| Curriculum V1/V2 safety | Required — declared sections via Curriculum helpers only |
| Educational honesty / thin warrant | Required — self_declared provenance mandatory |
| No Flask / DB / UI in this milestone | Honoured — architecture only |

---

# 14. STOP

This document defines **Initial Student Calibration architecture only**.

It does **not** authorise:

- Implementation  
- Flask routes or forms  
- Database tables or migrations  
- UI / wizard steps  
- Twin Persistence implementation  
- Evidence seeding  
- Educational Intelligence changes  

**STOP.**
