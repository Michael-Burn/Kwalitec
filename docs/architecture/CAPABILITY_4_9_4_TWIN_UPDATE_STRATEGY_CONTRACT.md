# Capability 4.9.4 — Twin Update Strategy Contract

**Status:** Contract only — no implementation  
**Epic:** Epic 4 — Educational Intelligence Evolution (Internal Alpha active)  
**Capability:** 4.9.4 Twin Update Strategy Contract (immutable Application Layer write-side boundary for Twin evolution)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Application Layer law:** [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md)  
**Upstream Strategy architecture:** [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md)  
**Upstream educational analysis:** [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md)  
**Upstream product flow:** [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md)  
**Contract companions:** [`CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md`](CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md), [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md), [`CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md`](CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Evidence companion (Epic 0 catalogue):** [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md)  
**Scope:** Closed, immutable Application Contract for Version 1.0 Twin Update Strategies — **no Flask, ORM, persistence schemas, update mathematics, algorithms, Pipeline implementation, or Educational Intelligence reasoning**

---

## Document purpose

Capabilities 4.9.1–4.9.3 established:

- **Architecture** — Twin Update Strategies are the sole authority permitted to evolve a Digital Twin from Educational Evidence; they interpret; they never mutate; they never recommend.  
- **Educational analysis** — observations are not educational state; Educational Sufficiency may warrant preservation rather than densification.  
- **Product flow** — Twin evolution is invisible continuity after valid Evidence; students experience better guidance, not Twin machinery.

This milestone defines the **immutable Twin Update Strategy Contract**.

It answers:

> What exact Application boundary may invoke one Twin Update Strategy so Current Twin + Educational Evidence become one complete immutable Successor Twin — and nothing else?

It is the sole Version 1.0 Application write-side boundary for Evidence-driven Twin evolution under a named Strategy.

**Governing principle (binding):**

> **Twin Update Strategies consume a Current Twin and Educational Evidence. They author one complete immutable Successor Twin. Nothing else crosses this boundary.**

**Architectural restatement:**

> **Application owns Twin evolution. Strategies receive educational inputs. Strategies return a Successor Twin. Educational Intelligence never invokes educational reasoning through this contract. The contract is the stable write-side boundary — and it stops there.**

**Naming disambiguation (binding):**

| Term | Meaning in this document |
|---|---|
| **Twin Update Strategy Contract** | Immutable closed Application write-side boundary for one Strategy invocation (this document) — Version 1.0 |
| **Twin Update Strategy** | Named educational interpreter that authors a complete immutable Successor Twin from Current Twin + Educational Evidence |
| **Current Twin** | Latest lawful immutable Digital Twin snapshot for the authorised student / sitting scope |
| **Educational Evidence Package** | Immutable educational observation memory (Capability 4.8) — already created; not Presentation session cargo |
| **Successor Twin** | New complete immutable Twin snapshot authored by the Strategy — never an in-place edit or patch |
| **Preserved successor Twin** | Lawful Version 1.0 outcome when Educational Sufficiency does not warrant belief change — succession discipline maintained without inventing densification |
| **Educational Sufficiency** | Educational concept (Capability 4.9.2): whether Evidence warrants any successor state change — named here; not computed as an algorithm in this document |
| **Strategy Composition** | Future coordination of multiple Strategies into one successor (Capability 4.9.5) — sits above this contract |

**Non-goals of this document**

- Implementation types, dataclasses, JSON schemas, ORM, or API payloads  
- Flask routes, forms, templates, or background workers  
- Belief-update algorithms, sufficiency formulas, BKT, forgetting curves, or numeric engines  
- Twin Repository / TwinProvider / Evidence Repository schemas or adapters  
- Twin Update Pipeline orchestration code or Strategy registration machinery  
- Multi-Strategy composition (deferred to Capability 4.9.5)  
- Educational Intelligence reasoning, readiness, Decision, Recommendation, or Mission  

---

# 1. Purpose

## 1.1 Why the contract exists

Without a closed Application write-side contract for Twin Update Strategies:

- Current Twin, Evidence packages, and Strategy outputs invent incompatible shapes;  
- Presentation objects, dashboard scrap, or mission ticks leak into Twin authorship;  
- Educational Intelligence is tempted to rewrite Twin state while judging preparedness;  
- Persistence adapters are tempted to accept partial patches as “updates”;  
- Twin evolution becomes untraceable — successors without named Strategy, Evidence, or lineage.

The **Twin Update Strategy Contract** exists so that:

1. **Application owns Twin evolution** — the write path for Evidence-driven succession has one closed Application boundary.  
2. **Twin Update Strategies receive educational inputs** — Current Twin + Educational Evidence Package only, with Strategy identity and version anchors.  
3. **Strategies return a Successor Twin** — one complete immutable Twin; never patches, domain slices, or recommendations.  
4. **Educational Intelligence never invokes educational reasoning through this contract** — Intelligence consumes Twins on the read path; it must not call Strategies as a side effect of readiness or recommendation.  
5. **The contract becomes the stable write-side boundary** — everything educational about “author a successor from this Evidence under this Strategy” crosses here or does not cross at all.

It is the lawful answer to:

> “What may Application hand one Twin Update Strategy, and what must that Strategy return?”

It is **not** the answer to:

> “What was observed?” / “How ready is the student?” / “What should they study next?” / “How should multiple Strategies be composed?” / “Which table stores the Twin?”

## 1.2 Relationship to Product Flow

Capability 4.9.3 defines the invisible product journey:

```
Study ends → Educational Evidence created / accepted / persisted
        ↓
Twin Update may begin (student already gone)
        ↓
Twin Update Strategy Contract   ← this document (Application write-side handoff)
        ↓
Strategy interprets → Successor Twin (or preserved successor)
        ↓
Twin Repository persists (when available)
        ↓
Next dashboard → Twin Provider → Educational Intelligence
```

Product Flow owns *when* Twin Update may begin and that students never operate Strategies.  
This Contract owns *what* crosses the Strategy invocation boundary once Twin Update begins.

| Product Flow concern | Contract concern |
|---|---|
| Entry only after valid Evidence | Contract requires an immutable Educational Evidence Package |
| Invisible continuity; no student Twin UI | Contract is Application-facing — never Presentation ceremony |
| Educational Sufficiency may preserve state | Contract permits preserved successor Twin as lawful output |
| Repository unavailability leaves Intelligence on current Twin | Contract failure posture: successor not persisted; no fabricated Twin |
| Composition of guidance on next visit | Out of contract — Educational Intelligence consumes Twin |

Governing restatement:

> **Product Flow times and hides Twin evolution. The Contract freezes what one Strategy may consume and must emit.**

## 1.3 Relationship to write / read separation (ADR-002)

```
WRITE path:
  Educational Evidence → Twin Update Strategy Contract → Successor Twin → Twin Repository

READ path:
  Twin Repository → Twin Provider → Educational Intelligence
  (Readiness → Decision → Recommendation → Mission)
```

Rules:

1. **This contract is the Version 1.0 Application write-side Strategy boundary** for one named Strategy.  
2. **Educational Intelligence never calls this contract.** Judgement consumes Twins via Provider.  
3. **Twin Repository never interprets through this contract.** Repository stores what Strategies author.  
4. **Educational Evidence Contract remains a different artefact** — observation handoff ends when Evidence is created; this contract begins when Evidence already exists.

Governing restatement:

> **No valid Strategy Contract inputs ⇒ no Successor Twin authorship. Never invent educational state to keep the Twin moving.**

---

# 2. Ownership

Ownership is absolute. The contract is an Application write-side boundary artefact, not a shared editable Twin worksheet.

| Actor | Owns | Must never |
|---|---|---|
| **Presentation** | **Nothing here** | Gather Twin beliefs; invoke Strategies; send session UI as Strategy authority; display Twin-update ceremony |
| **Educational Evidence** | **Immutable observations** already created under Capability 4.8 | Author Twin beliefs; interpret meaning into mastery / readiness; mutate Twin snapshots |
| **Twin Update Strategy** | **Educational interpretation** of Current Twin + Evidence into one complete immutable Successor Twin | Mutate Current Twin in place; recommend; ready / score / missionise; invent missing Evidence; persist storage policy |
| **Application (validation)** | **Structural validation** of contract inputs — integrity, identity, version, Strategy compatibility | Score educational correctness of Strategy conclusions; invent Mid beliefs on failure |
| **Twin Repository** | **Persistence** of authored Twin wholes (Persist Successor Twin) | Author successors; merge hybrid Twins; patch domains |
| **Twin Provider** | **Retrieval** of current Twin or honest absence for read paths | Fabricate successors; invoke Strategies on dashboard load |
| **Educational Intelligence** | **Future reasoning** from successor Twins (Readiness → Decision → Recommendation → Mission) | Invoke this contract; write Twin beliefs from Evidence; treat Strategies as recommendation helpers |

## 2.1 Presentation owns

**Nothing.** Twin Update Strategies are not a student-facing feature (Capability 4.9.3). Presentation does not emit this contract and does not own Strategy inputs or outputs.

## 2.2 Educational Evidence owns

| Responsibility | Meaning |
|---|---|
| **Immutable observations** | Lawful Educational Evidence Package cargo that Strategies may interpret |
| **Provenance of observation** | Observed vs declared tags remain Evidence-owned history |

Evidence never becomes Twin belief by crossing this boundary alone — Strategies interpret.

## 2.3 Twin Update Strategy owns

| Responsibility | Meaning |
|---|---|
| **Educational interpretation** | Decide what Current Twin + Evidence warrant as successor educational state |
| **Whole Twin authorship** | Emit one complete immutable Successor Twin |
| **Conservative honesty** | Preserve state when Educational Sufficiency does not warrant densification |
| **Traceability posture** | Successor Twin lineage remains attributable to Evidence + Strategy |

## 2.4 Twin Repository owns

| Responsibility | Meaning |
|---|---|
| **Persistence** | Store the complete Successor Twin when durable write succeeds |
| **Succession designation** | Designate successor current; retain prior Twin as history |

Repository stores. It does not interpret.

## 2.5 Twin Provider owns

| Responsibility | Meaning |
|---|---|
| **Retrieval** | Return Digital Twin or TwinAbsent (or classified failure) on the product read path |

Provider retrieves. It does not author successors from Evidence.

## 2.6 Educational Intelligence owns

| Responsibility | Meaning |
|---|---|
| **Future reasoning from successor Twins** | Judgement after Twin Provider supplies Twin state |

Intelligence never owns Twin authorship and never crosses this write-side contract.

### Ownership invariants

1. **Presentation owns nothing here.**  
2. **Educational Evidence owns immutable observations.**  
3. **Twin Update Strategy owns educational interpretation.**  
4. **Twin Repository owns persistence.**  
5. **Twin Provider owns retrieval.**  
6. **Educational Intelligence owns future reasoning from successor Twins.**  
7. **Application validates structure at the boundary — it does not second-guess Strategy educational conclusions.**

Governing restatement:

> **Observe → interpret → store → retrieve → judge. No owner at this boundary may invent learning or reopen the write path from Intelligence.**

---

# 3. Required Inputs

Version **1.0** of the Twin Update Strategy Contract is a **closed** minimum input set.

Only **immutable** Current Twins and **immutable** Educational Evidence Packages are accepted.

| Input | Meaning | Class |
|---|---|---|
| **Current Digital Twin** | Complete immutable Twin snapshot for the authorised student / sitting scope — the educational state Strategies interpret from | Required |
| **Educational Evidence Package** | Complete immutable Educational Evidence already created / accepted — observational memory only | Required |
| **Strategy identity** | Named Twin Update Strategy authorised to interpret (e.g. Knowledge / Performance / Behaviour / Memory / Goal Strategy identity under Version 1.0 catalogue) | Required |
| **Contract version** | Contract version identity — `1.0` for this milestone | Required |
| **Processing timestamp** | When Application invoked the Strategy boundary (product clock of the write attempt) | Required |
| **Evidence provenance** | Provenance identifiers / tags carried with the Evidence Package (observed vs declared lineage; Evidence identity anchors) so interpretation remains attributable | Required |

## 3.1 Input honesty rules

| Rule | Meaning |
|---|---|
| **Only immutable Twins** | Mutable working copies, domain fragments, and in-progress drafts are rejected |
| **Only immutable Educational Evidence** | Presentation session cargo, activity scrap, mission ticks that never became Evidence, and draft contracts are rejected |
| **Complete wholes** | Current Twin must be a whole Twin aggregate; Evidence Package must be a whole observational package — not sparse UI leftovers promoted as truth |
| **Strategy identity required** | Anonymous “update the Twin” invocations are forbidden — authorship must name which Strategy interprets |
| **Evidence provenance required** | Strategies must not interpret provenance-stripped Evidence as if warrant density were unknown history |

## 3.2 Forbidden as Required (or any) Strategy authority

| Forbidden input | Why |
|---|---|
| Presentation / session objects | Not educational-state authorship authority |
| Dashboard analytics aggregates | Product mirrors |
| Readiness / Decision / Recommendation / Mission payloads | Read path must not reopen write path |
| Raw activity streams | Evidence boundary only |
| Calibration declarations as Evidence substitutes | Calibration remains birth priors |
| Partial Twin patches offered as “current” | Violates immutability |

### Closed Required invariant

> **Version 1.0 Strategy invocation accepts only this Required spine. Strategies consume Current Twin + Educational Evidence — nothing else.**

---

# 4. Optional Inputs

Optional inputs enrich operational explainability. Their omission remains **educationally acceptable**.

| Input | Meaning | Class |
|---|---|---|
| **Execution metadata** | Non-educational run labels (batch id, worker id, environment tag) | Optional |
| **Diagnostic trace identifiers** | Correlation ids for engineering audit of the write attempt | Optional |
| **Replay identifier** | Identity that this invocation is a lawful replay / reconstruction of a prior interpretation posture | Optional |
| **Operator context** | Non-student operator metadata when Internal Alpha tooling invokes under explicit product rules | Optional |

## 4.1 Why omission remains educationally acceptable

| Optional input | Why absence is honest |
|---|---|
| **Execution metadata** | Twin meaning does not depend on which worker ran; educational succession depends on Twin + Evidence + Strategy |
| **Diagnostic trace identifiers** | Useful for engineering reconstruction; not educational warrant |
| **Replay identifier** | Most Version 1.0 invocations are first-time succession, not replay |
| **Operator context** | Student Evidence paths need no operator theatre; silence is normal |

## 4.2 Optional field rules

1. **No educational meaning belongs here.** Optional inputs must not densify mastery, readiness, confidence, or Goals.  
2. **Omitted Optional inputs must not be invented** as educational fillers.  
3. **Optional presence must not redefine Required meaning** — e.g. a diagnostic id must not substitute for Evidence identity.  
4. **Operator context never becomes Evidence.** Internal tooling cannot smuggle undeclared observations through Optional cargo.

### Optional invariant

> **Optional operational metadata may be present. Educational meaning may not hide in Optional fields.**

---

# 5. Required Output

## 5.1 Primary output (binding)

| Output | Meaning |
|---|---|
| **One complete immutable Successor Twin** | Whole Twin aggregate representing post-interpretation educational state for the scope |

## 5.2 Required accompanying cargo

| Cargo | Meaning |
|---|---|
| **Successor provenance** | Lineage anchors tying the Successor Twin to Current Twin + Evidence + Strategy (Section 8) |
| **Strategy identity** | Same Strategy that authored (must match input Strategy identity) |
| **Update timestamp** | When the Successor Twin was authored under this contract invocation |
| **Version** | Twin / contract structural version identity required for forward honesty |

## 5.3 Output law (binding)

1. **Partial Twin updates are not permitted.**  
2. **Patch objects are not permitted.**  
3. **Strategies always author whole Twins.**  
4. **Domain slices without a whole Twin are not permitted.**  
5. **Recommendations, readiness bands, missions, and pass probabilities are not permitted Strategy outputs.**

## 5.4 Preserved successor Twin

When Educational Sufficiency does not warrant belief change, Version 1.0 still requires succession honesty:

| Lawful outcome | Meaning |
|---|---|
| **Preserved successor Twin** | A complete immutable Twin whose educational meaning remains unchanged relative to Current Twin (or changes only in domains that Strategy explicitly leaves as preservation) — still a whole Twin with succession / provenance posture, not a silent in-place mute of the prior snapshot |
| **Not an error** | Preservation is educational honesty (Capability 4.9.2 / 4.9.3) — not contract failure |

Application must not invent densified domains to avoid preservation outcomes.

### Output invariant

> **One complete immutable Successor Twin. Not patches. Not partial updates. Strategies always author wholes.**

---

# 6. Validation

Application validates **structural legality** of the write-side invocation.

It answers:

> “Are Current Twin, Evidence, version, identity, and Strategy posture lawful for invocation?”

It never answers:

> “Did the Strategy interpret correctly / is mastery warranted / are they ready / should confidence rise?”

## 6.1 Application validates

| Check | Pass condition |
|---|---|
| **Current Twin integrity** | Current Twin is present, complete as a Twin whole, immutable, and structurally lawful for the authorised scope |
| **Evidence integrity** | Educational Evidence Package is present, immutable, observational-only, and attributable (with Required provenance) |
| **Version compatibility** | `contract_version` is a known accepted version; Twin / Evidence structural versions are compatible with Version 1.0 Strategy invocation |
| **Identity consistency** | Student / sitting / Study Plan / curriculum identities align across Current Twin and Evidence Package; Mission / topic identities consistent when applicable |
| **Strategy compatibility** | Strategy identity is recognised for Version 1.0; Strategy is authorised for this invocation posture |

## 6.2 Application deliberately does NOT validate

| Non-validation | Why |
|---|---|
| **Educational correctness** | Interpretation belongs to the Strategy |
| **Strategy conclusions** | Application must not re-score or reject a whole Twin because Application “disagrees” educationally |
| **Mastery** | Mastery belief is Strategy educational ownership — not boundary validation |
| **Readiness** | Readiness Aggregation is Educational Intelligence |
| **Confidence** | Confidence domain truth is not a structural Validation check |

### Validation outcome (conceptual)

| Outcome | Meaning |
|---|---|
| **Accepted for Strategy invocation** | Structurally valid; Strategy may interpret and author Successor Twin |
| **Rejected** | Structurally unlawful; Strategy must not invent a Successor Twin |
| **Invoked with preservation permitted** | Structural acceptance does not force densification — Educational Sufficiency may still yield preserved successor |

Governing restatement:

> **Validate integrity of inputs — never the educational truth of Strategy conclusions.**

---

# 7. Failure Behaviour

Product-level contract behaviour only — no routes, queues, or persistence mechanics.

**Binding rule:**

> **No fabricated successors. No partial Twins.**

## 7.1 Missing Current Twin

```
Missing Current Twin
        ↓
Reject
```

| Condition | Contract behaviour |
|---|---|
| No lawful Current Twin for the authorised scope | **Rejected** — do not invent a Birth Twin; do not Mid-fill domains; Calibration remains the birth author |

## 7.2 Invalid Educational Evidence

```
Invalid Educational Evidence
        ↓
Reject
```

| Condition | Contract behaviour |
|---|---|
| Evidence Package missing, mutable, non-observational, provenance-stripped beyond recovery, or identity-incoherent | **Rejected** — do not invent Evidence; do not “update from activity” |
| Judgement fields smuggled as Evidence authority | **Rejected** |

## 7.3 Educational Sufficiency not achieved

```
Educational Sufficiency not achieved
        ↓
Return preserved successor Twin
```

| Condition | Contract behaviour |
|---|---|
| Evidence is structurally valid but does not warrant belief densification for the Strategy’s educational responsibility | **Return preserved successor Twin** — complete immutable Twin; educational meaning preserved where honesty requires |
| Truthful product effect | Continuity without theatre; Educational Intelligence may keep consuming effectively unchanged Twin meaning |

Preservation is **success**, not failure (Capability 4.9.2 / 4.9.3).

## 7.4 Repository unavailable

```
Repository unavailable
        ↓
Successor Twin not persisted
```

| Condition | Contract behaviour |
|---|---|
| Strategy authored a Successor Twin but Twin Repository cannot durably accept it | **Successor Twin not persisted** — signal honesty; do not claim durability; do not invent a different Twin; Educational Intelligence continues on last durable Current Twin when retrieve succeeds |
| Forbidden | Claiming persist success without store; Mid substitute Twin for availability theatre |

Persistence failure is Repository honesty (Capability 3.7.3) — it is not permission to fabricate educational state.

## 7.5 Other failures

| Condition | Contract behaviour |
|---|---|
| Version incompatible | **Reject** |
| Strategy identity unrecognised / incompatible | **Reject** |
| Identity inconsistency across Twin and Evidence | **Reject** |
| Strategy returns patch / partial Twin | **Reject** — do not forward to Repository |
| Educational Intelligence attempts invocation | **Reject / forbidden path** — wrong owner |

## 7.6 Failure summary

| Failure | Contract posture |
|---|---|
| Missing Current Twin | Reject |
| Invalid Educational Evidence | Reject |
| Educational Sufficiency not achieved | Return preserved successor Twin |
| Repository unavailable | Successor Twin not persisted |
| Partial / fabricated outputs | Reject — never invent |

Governing restatement:

> **Structural failure rejects. Educational thinness preserves. Persistence failure refuses durability theatre. Never fabricate successors.**

---

# 8. Provenance

Successor Twins **must** preserve provenance sufficient for educational traceability.

## 8.1 Required provenance cargo

| Provenance element | Meaning |
|---|---|
| **Current Twin identifier** | Snapshot identity of the Twin Strategies interpreted from |
| **Evidence identifiers** | Identity of the Educational Evidence Package(s) interpreted |
| **Strategy identifier** | Named Strategy that authored the Successor Twin |
| **Update timestamp** | When succession was authored under this contract |
| **Reasoning trace reference** | Reference to an explainability / audit trace for how interpretation was attributed (architectural identity — not an algorithm dump mandated here) |
| **Version** | Contract / Twin structural version identity |

## 8.2 Why educational traceability is mandatory

Without successor provenance:

- recommendations cannot cite what changed under which Evidence;  
- Internal Alpha cannot distinguish preservation from densification honestly;  
- Repository history loses authorship clarity (Calibration vs Strategies);  
- Educational Intelligence cannot pin the Twin it judged.

### Provenance invariants

1. **Educational traceability is mandatory.**  
2. **Provenance must not be stripped at Repository persist.**  
3. **Strategies must not rewrite Evidence provenance** (observed stays observed; declared stays declared).  
4. **Preserved successors still carry provenance** — preservation is attributable honesty, not silent absence of lineage.

Governing restatement:

> **Every Successor Twin must answer: from which Twin, under which Evidence, by which Strategy, when, and under which version.**

---

# 9. Versioning

## 9.1 Freeze Version 1.0

This document freezes **Twin Update Strategy Contract Version 1.0**.

Version 1.0 is intentionally small:

- one Current Twin;  
- one Educational Evidence Package;  
- one Strategy identity;  
- one complete immutable Successor Twin;  
- structural validation only;  
- preserved successor as lawful thin-Evidence outcome.

## 9.2 Additive future versions

Future versions may introduce **without breaking Version 1.0**:

| Future addition | How it evolves |
|---|---|
| **Multiple Evidence packages** | Additive under a new contract version; Version 1.0 remains single-package |
| **Strategy orchestration metadata** | Additive execution / composition cargo — not educational belief algebra inside Optional |
| **Parallel strategies** | Coordinated via Capability 4.9.5 composition above this contract; Version 1.0 one-Strategy invocation stays lawful |
| **Additional metadata** | Optional operational / explainability fields under newer versions; ignored by Version 1.0 consumers when unknown |

## 9.3 Evolution rules

1. **Additive by default.** Newer optional inputs must not redefine Version 1.0 Required meaning.  
2. **Never silently redefine Version 1.0 outputs.** Successor Twin wholes remain mandatory; patches remain forbidden.  
3. **Required inputs cannot be removed** from Version 1.0 without a breaking major version.  
4. **New Required inputs** belong only in a new major version; Version 1.0 invocations remain valid without them.  
5. **Educational Intelligence and Presentation remain outside this contract.** Growing the write-side boundary must not move judgement or UI into Strategy cargo.  
6. **Educational Sufficiency remains a concept**, not a Version 1.0 algorithm field that Intelligence may override.

### Compatibility posture

| Change type | Breaking for Version 1.0? | Example |
|---|---|---|
| Add optional replay identifier in `1.1` | No if ignored by V1.0 | Additive Optional |
| Allow multiple Evidence packages in `2.0` | Yes for emitters required to send multi-package | Major version |
| Permit patch outputs | Yes — forbidden | Violates immutability law |
| Make Educational Intelligence a Strategy invoker | Yes — forbidden | Breaks ADR-002 firewall |

Governing restatement:

> **Contract evolves additively. Version 1.0 remains lawful forever as history. Never version toward partial Twins or Intelligence write-path ownership.**

---

# 10. Relationship with Strategy Composition

## 10.1 This contract defines one Strategy

Version 1.0 of this contract freezes the boundary for **one Strategy**:

```
Current Twin + Educational Evidence Package
        ↓
One Twin Update Strategy (named)
        ↓
One complete immutable Successor Twin
```

It answers Strategy authorship for a single interpretive responsibility.

## 10.2 Future Capability 4.9.5 defines multiple Strategy composition

Multiple Strategies may exist educationally (Capability 4.9.1 catalogue). Coordinating them into one durable current Twin — order, merge-without-hybrid-authorship, domain independence — belongs to **Strategy Composition** (future Capability 4.9.5).

| Concern | Owner |
|---|---|
| One Strategy consume / produce law | **This contract (4.9.4)** |
| Multiple Strategy composition | **Future Capability 4.9.5** |
| Persist composed successor | **Twin Repository Contract (3.7.3)** |

## 10.3 Composition sits above the contract

```
Strategy Composition (future 4.9.5)
        ↓
invokes this contract per Strategy (or composes Strategy results under composition law)
        ↓
one durable complete Successor Twin → Twin Repository
```

Rules:

1. **Composition sits above the contract.** It must not bypass whole-Twin law by merging domain patches Repository-style.  
2. **This contract remains valid** for single-Strategy invocation even after composition exists.  
3. **Composition must not collapse Strategies into Educational Intelligence** or into Presentation.

Governing restatement:

> **This contract freezes one Strategy. Composition of many Strategies is a future capability above it — never a licence for partial Twins.**

---

# 11. Contract Compliance Summary

| Invariant | Status under this contract |
|---|---|
| Application owns Twin evolution write-side boundary | Affirmed |
| Required inputs: Current Twin + Educational Evidence Package + Strategy identity + version + timestamp + Evidence provenance | Affirmed |
| Only immutable Twin and Evidence accepted | Affirmed |
| Required output: one complete immutable Successor Twin + provenance | Affirmed |
| No patches / partial Twins | Affirmed |
| Structural validation only; no educational correctness scoring | Affirmed |
| Missing Twin / invalid Evidence → Reject | Affirmed |
| Educational Sufficiency not achieved → preserved successor Twin | Affirmed |
| Repository unavailable → successor not persisted | Affirmed |
| Provenance mandatory | Affirmed |
| Version 1.0 frozen; additive future versions | Affirmed |
| One Strategy; composition deferred to 4.9.5 | Affirmed |
| Consistent with Calibration / TwinRepository / Evidence / ADR-002 / Application Layer | Affirmed |
| No Flask / ORM / algorithms / persistence / Intelligence reasoning | Honoured — contract only |

---

# 12. STOP

This document defines the **Twin Update Strategy Contract** only.

It does **not** authorise:

- Implementation  
- Update mathematics or Educational Sufficiency algorithms  
- Flask routes, workers, or services  
- ORM models, schemas, or migrations  
- Twin Repository / TwinProvider code  
- Twin Update Pipeline or Strategy registration code  
- Strategy Composition (Capability 4.9.5)  
- Educational Intelligence reasoning or redesign  
- Persistence technology choices  
- Product UI for Twin updates  

**STOP.**

---

# References

| Artefact | Role |
|---|---|
| [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Governing ADR; write/read separation; Evidence → Twin → Intelligence |
| [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Platform educational chain; Update Strategy ownership |
| [`APPLICATION_LAYER_ARCHITECTURE.md`](APPLICATION_LAYER_ARCHITECTURE.md) | Application Layer boundary law |
| [`CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md`](CAPABILITY_4_9_1_TWIN_UPDATE_STRATEGY_ARCHITECTURE.md) | Strategy architecture law |
| [`CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md`](CAPABILITY_4_9_2_TWIN_UPDATE_STRATEGY_ANALYSIS.md) | Educational Sufficiency; preservation vs evolution |
| [`CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md`](../product/CAPABILITY_4_9_3_TWIN_UPDATE_STRATEGY_PRODUCT_FLOW.md) | Invisible Twin evolution journey |
| [`CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md`](CAPABILITY_4_8_4_EDUCATIONAL_EVIDENCE_CONTRACT.md) | Companion observation handoff — Evidence creation precedes this contract |
| [`CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md`](CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md) | Companion Presentation → Application birth handoff |
| [`CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md`](CAPABILITY_3_7_3_TWIN_REPOSITORY_CONTRACT.md) | Companion Application ↔ Persistence for Twin wholes |
| [`CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md`](CAPABILITY_3_3_TWIN_PROVIDER_ARCHITECTURE.md) | Retrieval honesty after succession |
| [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md) | Canonical Twin domain law; immutable snapshots |
| [`LEARNING_EVIDENCE_MODEL.md`](../../LEARNING_EVIDENCE_MODEL.md) | Epic 0 Evidence catalogue companion |
| [`UBIQUITOUS_LANGUAGE.md`](../../UBIQUITOUS_LANGUAGE.md) | Shared educational vocabulary |
