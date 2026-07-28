# EI-007 — Educational Reasoning Engine Architecture

**Programme:** EI-007 — Educational Reasoning Engine  
**Date:** 2026-07-28  
**Status:** Complete  
**Code:** `app/domain/educational_reasoning_engine/` · `app/application/educational_reasoning_engine/` · `app/models/educational_reasoning_engine.py`  
**Depends on:** [EI-006 Twin Inference](../ei006_twin_inference_engine/ARCHITECTURE.md) · [EI-005 Learning Evidence](../ei005_learning_evidence_engine/ARCHITECTURE.md) · [EI-004 Student Curriculum Binding](../ei004_student_curriculum_binding/ARCHITECTURE.md) · [EI-001 / EI-003 Published CKG](../ei001_curriculum_knowledge_graph/ARCHITECTURE.md)

---

## 1. Capability statement

> Kwalitec can determine what a student should learn next, and explain why.

Given a Published Curriculum Edition, Student Curriculum Instance, Learning Evidence references, and Twin Beliefs, Kwalitec deterministically produces ordered, explainable educational decisions. No mission text, Coach responses, or student UI are generated in EI-007.

---

## 2. Reasoning philosophy

| Principle | Meaning |
|-----------|---------|
| 1. Decisions ≠ interface | The engine produces educational actions only — never UI copy or mission wording. |
| 2. Explainability | Every decision cites beliefs, curriculum dependencies, rules, evidence ids, priority arithmetic, and rationale. |
| 3. Determinism | Same curriculum, SCI state, beliefs, evidence refs, and rule pack → identical decisions. |
| 4. Rule modularity | Reasoning rules are independently testable units composing a versioned pack (`ere.v1`). |
| 5. Trusted inputs only | Consumes published CKG + SCI + Twin beliefs + evidence references; mutates none of them. |
| 6. No generative AI | Deterministic educational reasoning only — no probabilistic LLM ranking. |

```
Published Curriculum (CKG edition)
        ↓
Student Curriculum Instance (EI-004)
        ↓
Twin Beliefs (EI-006) + Evidence refs (EI-005)
        ↓
Educational rules (modular, versioned)
        ↓
Ordered Educational Decisions (derived, rebuildable)
```

Package naming note: EI-007 lives under `educational_reasoning_engine` / `ere_*` to remain distinct from the legacy Version-2 `app.domain.educational_reasoning` module.

---

## 3. Decision lifecycle

1. **Observe** — SCI node educational slots and Twin beliefs exist for the instance.  
2. **Evaluate** — `DecisionReasoningService.evaluate_instance` builds a `ReasoningContext`, runs `EducationalReasoningEngine`, and optionally persists `ere_educational_decisions`.  
3. **Explain** — Every persisted decision stores an `explanation_json` with rules, priority calculation, and rationale.  
4. **Rebuild** — `rebuild_decisions` deletes prior decision rows for the SCI and recalculates from current trusted assets. Beliefs/evidence/curriculum are not mutated by rebuild.  
5. **Query** — `DecisionQueryService` retrieves ordered decisions and explainable summaries without re-reasoning.

Decisions **reference** belief ids, curriculum stable ids, and evidence ids; they never duplicate observation payloads.

---

## 4. Rule evaluation

Modular rules under `app/domain/educational_reasoning_engine/rules/`:

| Rule id | Concern |
|---------|---------|
| `prerequisite_satisfaction` | Propose `satisfy_prerequisite` when incomplete LOs are blocked by weak hard prerequisites |
| `low_confidence_topics` | Propose `strengthen_confidence` when mastery exists but confidence is low |
| `incomplete_curriculum_paths` | Propose `study_new` for incomplete, unblocked learning objectives |
| `revision_due_nodes` | Propose `revise` for due / overdue revision slots |
| `syllabus_priority` | Priority boost for earlier syllabus-index targets |
| `topic_dependency_ordering` | Prefer shallower prerequisite-DAG nodes; soft-penalise unsatisfied deps |
| `effort_estimation` | Attach deterministic effort (minutes) from difficulty; small inverse-effort boost |
| `study_continuity` | Propose `continue_path` from the most recent study interaction |

**Evaluation flow**

```
ReasoningContext (SCI nodes + beliefs + prereqs + syllabus order)
        ↓
Each rule emits RuleProposal(s)
        ↓
Merge by (decision_type, curriculum_target); typeless boosts attach by target
        ↓
clamp(sum(priority_deltas), 0, 1)
        ↓
Rank by (-priority, decision_type, curriculum_target)
        ↓
Emit EducationalDecision + DecisionExplanation (reasoning_version=ere.v1)
```

---

## 5. Prioritisation strategy

- Typed proposer rules seed candidate decisions with base priority deltas.  
- Modifier rules (`syllabus_priority`, `topic_dependency_ordering`, `effort_estimation`) contribute typeless deltas to matching curriculum targets.  
- Priority is the clamped sum of all contributing deltas — fully exposed in `PriorityCalculation`.  
- Final order is deterministic: higher priority first; ties broken by `decision_type` then `curriculum_target`.  
- Educational intent: overdue revision outranks ordinary new study; blocked dependents yield prerequisite satisfaction before advancement.

Decision types (`DecisionType`):

- `study_new` · `revise` · `strengthen_confidence` · `satisfy_prerequisite` · `continue_path`

Expected outcomes are structured codes (`ExpectedOutcome`), not student-facing sentences.

---

## 6. Educational Decision domain model

| Field | Role |
|-------|------|
| `decision_type` | Educational action category |
| `curriculum_target` | CKG node stable id |
| `priority` / `rank_position` | Explainable score and ordered rank |
| `rationale_summary` | Required human-readable why (internal, not UI copy) |
| `prerequisite_chain` | Hard prerequisite ids considered |
| `estimated_effort_minutes` | Deterministic effort estimate |
| `expected_educational_outcome` | Structured outcome code |
| `supporting_belief_ids` | EI-006 belief references |
| `supporting_curriculum_refs` | CKG stable ids |
| `supporting_evidence_ids` | EI-005 evidence references |
| `applied_rule_ids` | Rules that contributed |
| `reasoning_version` | Rule-pack id (`ere.v1`) |

No decision may be constructed without a non-empty rationale and at least one applied rule in its explanation.

---

## 7. Explainability model

`DecisionExplanation` always exposes:

- contributing beliefs  
- curriculum dependencies  
- educational rules applied  
- evidence references  
- priority calculation (raw sum, clamp, formula, components)  
- rule proposal records  
- rationale summary  
- reasoning version  

`DecisionQueryService.get_explainable_summary` returns a compact consumer view of the same facts.

---

## 8. Persistence (EI-007 additive)

Migration `202607280070`:

- `ere_educational_decisions`

Does not alter `tie_node_beliefs`, `lee_evidence_events`, CKG node content, V1/V2 curriculum engine, missions, or recommendation schema. Reversible via `downgrade()`.

---

## 9. Explicit non-goals

- Daily Mission generation  
- Coach / Tutor response generation  
- Student UI surfaces  
- Mutating Learning Evidence, Twin beliefs, or published curriculum  
- Probabilistic AI / LLM reasoning  
- Forgetting-curve engines (revision status is read from SCI slots)

---

## 10. Future extensibility

| Concern | Strategy |
|---------|----------|
| New rules | Add modular rule class; bump `REASONING_VERSION` |
| Alternate packs | Inject custom `rules=` into `EducationalReasoningEngine` |
| Mission generation | Downstream consumer of decisions (never inside EI-007) |
| Coach speech | Downstream narrative layer over explainable decisions |

```
Published CKG Edition (immutable)
        ↑
Student Curriculum Instance (EI-004)
        ↑
Learning Evidence (EI-005) → Twin Beliefs (EI-006)
        ↓
Educational Reasoning Engine (EI-007)  ← decisions + explanations
        ↓
(Future) Missions / Coach / Session surfaces
```
