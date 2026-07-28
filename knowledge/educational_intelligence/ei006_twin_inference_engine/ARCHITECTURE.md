# EI-006 — Twin Inference Engine Architecture

**Programme:** EI-006 — Twin Inference Engine  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/twin_inference/` · `app/application/twin_inference/` · `app/models/twin_inference.py`  
**Depends on:** [EI-005 Learning Evidence Engine](../ei005_learning_evidence_engine/ARCHITECTURE.md) · [EI-004 Student Curriculum Binding](../ei004_student_curriculum_binding/ARCHITECTURE.md) · [EI-001 Curriculum Knowledge Graph](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can explain what it believes a student currently knows, and why.

Given a Published Curriculum Edition, Student Curriculum Instance, and Learning Evidence history, Kwalitec infers a complete, explainable, and reproducible set of learner beliefs for every curriculum node. No recommendations or study missions are generated in EI-006.

---

## 2. Inference philosophy

| Principle | Meaning |
|-----------|---------|
| 1. Evidence immutability | Evidence rows are never updated or deleted. Beliefs are derived and may be recalculated at any time. |
| 2. Explainability | Every belief cites supporting evidence, contributing rules, confidence arithmetic, rationale, and inference version. |
| 3. Determinism | Same curriculum, student state, evidence, and rule pack → identical beliefs. |
| 4. Rule modularity | Inference rules are independently testable units composing a versioned pack (`tie.v1`). |
| 5. No generative AI | Deterministic educational inference only — no probabilistic LLM reasoning. |

```
Learning Evidence (EI-005, immutable)
        ↓
Inference rules (weighted, modular)
        ↓
Twin Beliefs (derived, rebuildable)
        ↓
Knowledge State (subject roll-up)
```

---

## 3. Belief lifecycle

1. **Observe** — EI-005 appends evidence against an SCI node.  
2. **Infer** — `BeliefInferenceService.infer_node_belief` loads usable evidence, applies `TwinInferenceEngine`, persists `tie_node_beliefs`, and optionally projects mastery/confidence onto `SciCurriculumNodeState`.  
3. **Explain** — Every persisted belief stores an `explanation_json` with rules, calculations, and rationale.  
4. **Rebuild** — `rebuild_beliefs` deletes prior belief rows for the SCI and recalculates all nodes from evidence (two-pass for prerequisites). Evidence is untouched.  
5. **Query** — `BeliefQueryService` retrieves explainable summaries and subject knowledge state without re-inference.

Beliefs **reference** evidence ids; they never duplicate observation payloads.

---

## 4. Evidence-to-belief pipeline

```
Active SCI + node_stable_id
        ↓
Load lee_evidence_events (chronological)
        ↓
Exclude corrected events (corrects_evidence_id targets)
        ↓
Apply rule pack (early rules → provisional scores)
        ↓
Prerequisite awareness (late rule; caps weak-prereq mastery)
        ↓
Clamp mastery/confidence · derive learning_state
        ↓
Emit TwinBelief + BeliefExplanation (inference_version=tie.v1)
        ↓
Upsert tie_node_beliefs · project SCI mastery/confidence slots
```

Corrected evidence remains in the immutable store for audit; scoring uses the surviving (correction-aware) set only.

---

## 5. Twin belief domain model

Each curriculum node belief contains:

| Field | Role |
|-------|------|
| `mastery_level` | Deterministic [0, 1] educational mastery estimate |
| `confidence_score` | Deterministic [0, 1] belief confidence |
| `learning_state` | Discrete disposition (`unknown` … `mastered` / `revising` / `struggling`) |
| `supporting_evidence_ids` | Ordered references into EI-005 |
| `inference_timestamp` | Clock used for the inference pass (`as_of`) |
| `inference_version` | Rule-pack id (`tie.v1`) |
| `rationale_summary` | Required human-readable why |

No belief may be constructed without a non-empty rationale.

---

## 6. Inference rules framework

Modular rules under `app/domain/twin_inference/rules/`:

| Rule id | Concern |
|---------|---------|
| `evidence_weighting` | Base mastery/confidence deltas by evidence type |
| `recency_handling` | Age-banded multiplicative weight |
| `repeated_attempts` | Practice success/failure + diminishing returns |
| `assessment_outcomes` | Score/passed mapping; founder absolute overrides |
| `revision_events` | Revision confidence/mastery refresh |
| `prerequisite_awareness` | Cap mastery when hard `requires` prerequisites are weak |

Aggregation: `clamp(sum(delta × weight), 0, 1)`. Founder overrides tagged `absolute:` replace the summed mastery/confidence while remaining fully explained.

---

## 7. Explainability model

`BeliefExplanation` always exposes:

- supporting evidence ids  
- contributing rule records (deltas, weights, detail)  
- confidence calculation (raw sum, clamp, formula, components)  
- mastery calculation (same shape)  
- inference rationale  
- inference version  
- learning-state reason  

`BeliefQueryService.get_explainable_summary` returns a compact consumer view of the same facts.

---

## 8. Subject knowledge state

`aggregate_knowledge_state` / `infer_subject_knowledge_state` roll up node beliefs into:

- mean mastery / mean confidence  
- learning-state counts  
- node id list  
- subject-level rationale  

This is a derived educational knowledge state for the SCI — not a recommendation or mission plan.

---

## 9. Persistence (EI-006 additive)

Migration `202607280060`:

- `tie_node_beliefs`

Does not alter `lee_evidence_events`, CKG node content, V1/V2 curriculum engine, missions, or recommendation schema. SCI `mastery` / `confidence` columns may be projected from beliefs (slots reserved since EI-004).

---

## 10. Explicit non-goals

- Recommendations or study mission generation  
- Mutating Learning Evidence history  
- Modifying published curriculum content  
- Probabilistic AI / LLM inference  
- Forgetting-curve engines (revision status scheduling remains out of scope)  
- Student HTTP / Coach surface wiring  

---

## 11. Future extensibility

| Concern | Strategy |
|---------|----------|
| New rules | Add modular rule class; bump `INFERENCE_VERSION` |
| New evidence types | Extend weighting catalogue; no belief schema change |
| Alternate packs | Inject custom `rules=` into `TwinInferenceEngine` |
| Retention / forgetting | New rule consuming revision + recency (separate programme) |
| Recommendations | Downstream consumer of beliefs (never inside EI-006) |

```
Published CKG Edition (immutable)
        ↑
Student Curriculum Instance (EI-004)
        ↑ instance_id / node_stable_id
Learning Evidence Events (EI-005)  ← observations only
        ↓
Twin Inference Engine (EI-006)     ← beliefs + explanations
        ↓
(Future) Reasoning / Recommendations / Missions
```
