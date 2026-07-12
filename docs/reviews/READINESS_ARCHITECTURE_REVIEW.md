# Capability 2.7.5 — Readiness Architecture Review

**Status:** APPROVED WITH CONDITIONS  
**Date:** 11 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Capability:** 2.7 Readiness Aggregation  
**Milestone:** 2.7.5 Architecture Review  
**Review type:** Architecture / fidelity review only — no implementation in this milestone  
**Governing architecture:** [`docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](../architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Approved predecessors:**

- [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](../architecture/CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md) (2.7.1)
- [`CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md`](../architecture/CAPABILITY_2_7_READINESS_AGGREGATION_ARCHITECTURE.md) (2.7.2)
- [`CAPABILITY_2_7_READINESS_IMPLEMENTATION_PLAN.md`](../architecture/CAPABILITY_2_7_READINESS_IMPLEMENTATION_PLAN.md) (2.7.3)

**Gate:** Epic 2 Midpoint Architecture Review — APPROVED WITH CONDITIONS ([`EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md`](EPIC_2_MIDPOINT_ARCHITECTURE_REVIEW.md))  
**Implementation under review:** `app/domain/readiness/` + `tests/test_readiness_aggregation.py`  
**Companions:** Twin README (`app/domain/twin/README.md`), legacy `app/services/readiness_service.py`, [`knowledge/subsystems/readiness.md`](../../knowledge/subsystems/readiness.md)

---

## 1. Executive Summary

Capability 2.7 delivers a coherent **read-side** readiness layer: a framework-free `ReadinessAggregation.derive(...)` that produces an immutable, factorable, warrant-aware `ReadinessState` from Twin + `CurriculumContext` + Goals, without mutating Knowledge, Memory, Behaviour, Performance, or the Twin aggregate.

The shipped design matches the approved educational charter and aggregation architecture on the binding invariants: write/read firewall, full factor catalogue, Evidence Warrant propagation, cold-start honesty, Confidence omission, V1/V2-safe curriculum context, explainability attributions, and Stage A legacy coexistence without a third live formula.

Residual risk is **operational dual truth**: product surfaces still consume legacy `ReadinessService` TopicProgress composites while Educational Intelligence truth lives in `ReadinessState`. Structural postures (presence / absence / conflict visibility, no numeric composites) are intentionally limited — sufficient as Decision Engine **context**, not as a finished preparedness score.

**Acceptance decision: APPROVED WITH CONDITIONS.** Capability 2.7 structural aggregation is architecturally sound. Capability 2.8 may proceed only under the conditions in §11.

**Application / production code was not modified by this review.**

---

## 2. Strengths

| Strength | Evidence |
|---|---|
| **Clear read-side placement** | Sibling package `app/domain/readiness/`; no required `readiness` field on `DigitalTwin`; Twin README and `BaseUpdateStrategy` docs state Readiness is not an Update Strategy |
| **Write/read firewall** | Aggregation reads Twin domains only; returns frozen `ReadinessState`; tests assert Twin equality before/after derive |
| **Factorable judgement** | Full seven-factor catalogue always present; `ReadinessState.create` rejects incomplete catalogues |
| **Educational separations preserved** | Assessment Performance ≠ Behaviour Reliability; Memory Stability ≠ Knowledge Strength; Evidence Warrant ≠ Confidence; Time/Goal Pressure is supporting only |
| **Warrant-first honesty** | Per-factor + overall warrant; sparse/unknown Performance floors exam-preparedness warrant; low-weight-only density cannot inflate sitting warrant |
| **Cold-start contract** | Goals-only / empty Twin → `not_yet_knowable` + low warrant; Behaviour-only Twin does not yield exam-ready overall |
| **No Mid/High fabrication** | `OverallPosture` vocabulary excludes Mid/High; structural ship ceilings at fragile / mixed / unknown |
| **Confidence omitted (v1)** | No Confidence input path; fidelity tests block Confidence-shaped Knowledge lineage from upgrading Assessment Performance |
| **Explainability spine** | Every factor carries `FactorAttribution` (twin domains, curriculum entity ids, evidence hooks, structural notes) |
| **Layering purity** | No Flask / SQLAlchemy / ORM / persistence / services in aggregation; AST import bans in tests |
| **V1/V2 compatibility** | `CurriculumContext` supports flat and sectioned fixtures; aggregator never requires Sections globally |
| **Deterministic core** | Same Twin + CurriculumContext → equal structural fields (when `as_of` omitted) |
| **Stage A discipline** | Legacy `ReadinessService` left intact; no hybrid average of legacy % + Twin factors shipped |

---

## 3. Weaknesses

| Weakness | Severity | Note |
|---|---|---|
| **Dual readiness authority still live** | High (program) | Dashboard, analytics, settings, missions, recommendations, burnout, and exam timeline still call legacy `ReadinessService`. Twin-first aggregation is not yet product-facing |
| **Structural belief proxy** | Medium | Knowledge Strength becomes `supportive` when any `mastery_belief` bag is present — without reading belief content. Honest for structural phase; easy to over-narrate as “knows it” |
| **Overall posture ceiling** | Medium | Structural v1 never emits an overall supportive/ready posture. Correct for honesty; Decision Engine must reason from factors + warrant, not wait for a green overall |
| **Performance risk via summary tags** | Low–Medium | Assessment risk elevation depends on string tags in Performance summary dicts (`weak`, `fail`, …). Fragile coupling to summary vocabulary until a defined fact schema exists |
| **CurriculumContext not yet orchestrated** | Medium | Domain expects a pre-built context; no production builder via `CurriculumService` helpers yet. Required before any live consumer |
| **Subsystem doc drift** | Low–Medium | `knowledge/subsystems/readiness.md` still names legacy `ReadinessService` as primary owner and does not point to `app/domain/readiness/` |
| **Coverage attribution fallback** | Low | Empty presence path may cite `curriculum.topic_ids[:3]` as attribution placeholders — explainable but slightly noisy |
| **Prediction float bag untouched** | Low | `PredictionState.readiness_snapshot: float \| None` remains a legacy-shaped slot; unused by aggregation (correct), but still a temptation for snapshot-as-truth later |

None of these weaknesses break the approved 2.7 structural contracts. They constrain how 2.8 and presentation cutover must proceed.

---

## 4. Technical Debt

| Item | Classification | Owner / next step |
|---|---|---|
| Legacy `ReadinessService` composites (TopicProgress / weighted % / streak-adjacent analytics) coexist with Twin-first `ReadinessState` | **High** | Stage B: Decision / new intelligence consume Twin-first only; freeze legacy formula deepening |
| Product UI still presents legacy readiness as authority | **High** | Stage C presentation cutover; adapters must not invent Mid defaults |
| No `CurriculumContext` builder from `CurriculumService` | **Medium** | Thin orchestration helper outside domain before any service wiring |
| Structural postures without belief-content interpretation | **Medium** | Deferred numeric / belief enrichment stays in domain Update Strategies — not inside aggregation |
| Performance summary string-tag risk heuristic | **Medium** | Define Performance summary fact vocabulary before richer assessment factor logic |
| `knowledge/subsystems/readiness.md` lag behind Twin-first ownership | **Medium** | Documentation hygiene when Stage B starts |
| `PredictionState.readiness_snapshot` float without warrant | **Low** | Snapshot path must store factorable / warrant-preserving copies when shipped |
| Overall posture never “supportive” in structural v1 | **Low** | Intentional; unlock only with explicit scoring milestone + warrant discipline |

No new High debt was introduced *inside* the domain package relative to the approved plan. The High items are the documented Stage A coexistence costs.

---

## 5. Risks

| Risk | Status after 2.7 | Mitigation / condition |
|---|---|---|
| **Factor coupling** | Controlled | Factors judged independently; warrant alignment is explicit meta-step, not silent average |
| **Duplicated reasoning** | Active (Stage A) | Twin aggregation + legacy service both answer “readiness”; Educational Intelligence paths must prefer Twin-first; do not deepen legacy |
| **Hidden scoring** | Controlled in domain; active in legacy | Domain has no % / pass probability; legacy composites remain opaque relative to Twin factors |
| **Context leakage** | Controlled | Aggregation is pure; CurriculumContext is a value object; Goals notes are structural tags only |
| **Curriculum coupling** | Controlled | Weights/order via `CurriculumContext` only; no parallel syllabus tree; V1 does not require Sections |
| **Future Confidence integration** | Controlled | v1 omits Confidence; architecture defines additive provisional factor with lower warrant than Performance — do not smuggle via Knowledge |
| **Belief engines inside aggregation** | Controlled | Structural presence/absence only; empty bags stay empty |
| **Readiness → Decision conflation** | Watch for 2.8 | Firewall holds today; 2.8 must consume context, never ask readiness to select actions |
| **Activity-as-readiness** | Controlled | Behaviour-only / mission-lineage paths do not grant exam-ready overall |
| **Snapshot-as-truth** | Deferred risk | Prediction snapshot strategy not shipped; float bag must not become live authority |
| **Warrant stripped at presentation** | Future UI risk | Any adapter or dashboard cutover must carry overall + per-factor warrant |

---

## 6. Checklist Findings (review axes)

### 6.1 Read-side integrity

| Domain | Mutated by Readiness? | Finding |
|---|---|---|
| Knowledge | No | Observational read of slots / beliefs / evidence ids |
| Memory | No | Observational read of retention / reinforcement / revision ids |
| Behaviour | No | Observational read of lineage; never grants exam readiness alone |
| Performance | No | Observational read of assessments / summaries |
| Digital Twin | No | No `DigitalTwin.create` write-back; no Update Strategy registration |

**Verdict:** PASS.

### 6.2 Factor integrity

| Factor | Educational meaning | Ownership | Independence | Explainability |
|---|---|---|---|---|
| Curriculum Coverage | Weighted Twin presence vs syllabus denominator | Aggregation synthesises; Curriculum owns weights | Separate from Knowledge Strength | Cites Knowledge + Curriculum |
| Knowledge Strength | Current mastery / structural proxy | Consumes Knowledge; does not own mastery | Separate from Memory | Cites Knowledge + evidence hooks |
| Memory Stability | Retention availability at sitting | Consumes Memory + Goals sitting context | Separate from Knowledge Strength | Cites Memory + Goals |
| Behaviour Reliability | Pace / adherence feasibility | Consumes Behaviour + Goals capacity | Separate from Assessment Performance | Notes `not_exam_readiness` |
| Assessment Performance | Assessed-condition strength/weakness | Consumes Performance + weight emphasis | Separate from Behaviour | Cites Performance + Curriculum |
| Time / Goal Pressure | Calendar / capacity reframe | Consumes Goals / Identity | Supporting only | Cites Goals + Identity |
| Evidence Warrant | Meta honesty about support | Aggregation; not a content belief | Meta vs content separation held | Aligned to overall warrant |

**Verdict:** PASS (structural meanings). Belief-content depth deferred by design.

### 6.3 Evidence Warrant

| Rule | Finding |
|---|---|
| No fabricated certainty | Overall never Mid/High; cold start → not_yet_knowable |
| Cold-start honesty | Goals-only and empty domains keep low warrant |
| Uncertainty preserved | Sparse Performance constrains overall warrant; warrant factor re-aligned after propagation |
| Absence ≠ Mid | Empty domains → unknown / low-warrant postures |

**Verdict:** PASS.

### 6.4 Educational fidelity

| Claim | Finding |
|---|---|
| Owns no evidence | PASS — cites lineage only |
| Owns no mastery | PASS — Knowledge remains belief authority |
| Owns no recommendations | PASS — no recommendation APIs |
| Owns no decisions | PASS — no action selection |
| Owns no missions | PASS — no mission generation |

**Verdict:** PASS.

### 6.5 Explainability chain

```
Curriculum (CurriculumContext weights / format)
    ↓
Evidence (ids when Twin lineage exposes them)
    ↓
Twin Domain (attribution tags)
    ↓
Readiness Factor (FactorJudgement)
    ↓
ReadinessState (overall posture + overall warrant)
```

**Verdict:** PASS for structural chain. Completeness of Evidence ids depends on upstream Twin lineage density (correct — aggregation must not invent evidence).

### 6.6 Legacy coexistence (Stage A)

| Check | Finding |
|---|---|
| No third readiness implementation | PASS — domain aggregation + legacy service only; no hybrid average adapter |
| No deeper legacy forks in this capability | PASS — `ReadinessService` not expanded for Twin-first |
| Migration path clear | PASS — Stages A→D documented in 2.7.2 §13; this ship remains Stage A |
| Dual product authority | OPEN debt — UI still legacy-first |

**Verdict:** PASS for Stage A scope; dual truth remains program debt.

### 6.7 Layering

| Constraint | Finding |
|---|---|
| Framework free | PASS |
| Pure domain | PASS |
| No Flask | PASS (tested) |
| No ORM | PASS (tested) |
| No persistence | PASS |

**Verdict:** PASS.

### 6.8 Decision Engine readiness (Capability 2.8)

| Question | Assessment |
|---|---|
| Can 2.8 consume readiness as preparedness context? | **Yes** — factor postures, warrant, cold_start, attributions, and disagreement are sufficient structural inputs |
| Is readiness a finished preparedness score? | **No** — intentionally structural; no %, no pass probability, no overall “ready” |
| Must 2.8 invent Mid readiness when Twin is thin? | **No** — must prefer diagnostics / evidence-creating actions under `not_yet_knowable` + low warrant |
| Blocker to starting 2.8 design? | **No**, if conditions in §11 are accepted |

**Verdict:** Sufficient to **start** Capability 2.8. Not sufficient to claim Twin-first product readiness cutover.

---

## 7. Acceptance Decision

### APPROVED WITH CONDITIONS

Capability 2.7 Readiness Aggregation (structural ship) is architecturally compliant with the approved educational analysis, aggregation architecture, and implementation plan.

Proceed to Capability 2.8 Decision Engine **only** under the conditions below.

---

## 8. Conditions (binding)

1. **Decision Engine consumes `ReadinessState` as context only** — never treats readiness as an action selector, never asks readiness to generate missions, and never coerces unknown / low-warrant / `not_yet_knowable` into Mid or High preparedness.
2. **Preserve Evidence Warrant end-to-end** — any 2.8 reason codes that cite readiness must inherit warrant honesty (e.g. prefer diagnostics when warrant is low).
3. **Do not deepen legacy TopicProgress readiness formulas** while Twin-first intelligence lands; no hybrid average of legacy % + Twin factors as temporary truth.
4. **Build `CurriculumContext` via canonical Curriculum helpers** before any production consumer of domain readiness; do not invent parallel weights/order inside Decision Engine.
5. **Do not product-narrate structural `supportive` Knowledge Strength as exam readiness** — overall exam preparedness remains constrained by Assessment Performance warrant and cold-start rules.
6. **Confidence remains omitted** from readiness until an explicit Confidence-domain / provisional-factor milestone; Knowledge-held confidence lineage must not upgrade Assessment Performance.
7. **Prediction snapshots (when added) derive first, store second**, and must not drop warrant while retaining a bold overall claim; do not treat `PredictionState.readiness_snapshot` float as live Twin-first authority.
8. **Update subsystem documentation** (`knowledge/subsystems/readiness.md` and related) to reflect Twin-first derivation ownership before or with Stage B wiring.

---

## 9. Recommendations

1. **Start Capability 2.8** with explicit input contracts: Twin snapshot + `ReadinessState` factors/warrant + Goals + Curriculum — firewall against readiness→action shortcuts.
2. **Ship a thin `CurriculumContext` builder** (orchestration/service layer) using `CurriculumService.get_all_topics_ordered` and V1/V2 weight helpers before Decision Engine production wiring.
3. **Plan Stage B cutover** so new Educational Intelligence paths never call `ReadinessService.get_overall_readiness` as authority.
4. **Keep numeric composites deferred** until structural consumption by Decision Engine proves factor disagreement and warrant handling in reason codes.
5. **Define Performance summary fact vocabulary** before enriching Assessment Performance beyond tag heuristics.
6. **Refresh `knowledge/subsystems/readiness.md`** to distinguish legacy analytics owner vs Twin-first `ReadinessAggregation` derivation owner.
7. **Do not start Prediction snapshot strategy, Recommendation packaging, or Mission Generation** under the Capability 2.7 label; those remain adjacent / later capabilities.

---

## 10. Architecture Compliance Summary

| Invariant | Status |
|---|---|
| Twin sole educational-state authority | Preserved — readiness consumes, does not fork beliefs |
| Evidence append-only | Preserved — readiness never authors evidence |
| Write/read firewall | Preserved |
| Activity ≠ readiness; Confidence ≠ mastery; Behaviour ≠ learning | Preserved in domain aggregation |
| Readiness ≠ Decision; Readiness ≠ Missions | Preserved |
| Curriculum V1/V2 loadable / traversable | Preserved via CurriculumContext; no traversal redesign |
| No third live readiness formula introduced | Preserved (Stage A coexistence only) |
| Migration impact | None for Capability 2.7 structural ship |
| Application code intentionally untouched by this review | Yes |

---

## 11. Document Control

| Field | Value |
|---|---|
| Milestone | Capability 2.7.5 — Readiness Architecture Review |
| Nature | Review only |
| Code impact | None |
| Migration impact | None |
| Curriculum V1/V2 | Compatibility confirmed for domain aggregation |
| Acceptance | **APPROVED WITH CONDITIONS** |
| Next | Capability 2.8 Decision Engine (separate milestone), under §8 conditions |

---

*End of Capability 2.7.5 Readiness Architecture Review. STOP.*
