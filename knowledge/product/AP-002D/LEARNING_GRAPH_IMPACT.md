# AP-002D — Learning Graph Impact

**Programme:** AP-002 — Educational Assessment Engine  
**Milestone:** AP-002D — Educational Intelligence Integration  
**Status:** Design (authoritative)  
**Related:** [`ARCHITECTURE_INVARIANTS.md`](../../engineering/ARCHITECTURE_INVARIANTS.md) §5, [`INTEGRATION_SPECIFICATION.md`](INTEGRATION_SPECIFICATION.md)

---

## 1. Principle

The Learning Graph stores **relationships only**.

It never duplicates mastery as a learner-state system of record. Assessment evidence does not write Graph edges as “proof of mastery”.

---

## 2. What changes when assessment evidence arrives

```
Twin inferences updated by StudentReasoningService
        ↓
LearningGraphService.refresh_projections(twin, …)
        ↓
Graph projections reflect current Twin belief for traversal
```

| Graph artefact | Effect of AP-002D |
|---|---|
| Prerequisite / recovery / related-concept **structure** | Unchanged by Assessment (curriculum / graph authoring owns structure) |
| **Projections** conditioned on Twin mastery / gaps | Refresh after Reasoning so Mission/Reasoning see current belief |
| Edge creation from a single correct answer | **Forbidden** — evidence does not invent relationships |

---

## 3. Relationship update rules

1. Assessment may reference concept / LO ids on evidence metadata (opaque).
2. Reasoning may use Graph structure when forming recovery / prerequisite decisions.
3. After Twin mastery/gap changes, projections refresh (existing StudentReasoningService behaviour).
4. Graph adapters must not persist a parallel mastery table treated as SoT.
5. If projections lag, consumers trust Twin for belief and Graph for structure — never the reverse for mastery.

---

## 4. Explicit non-duplication

| Concept | Owner |
|---|---|
| Mastery / Estimated Knowledge | Twin (via Reasoning) |
| Gap records | Twin (via Reasoning) |
| Prerequisite edge “A before B” | Learning Graph structure |
| “Student currently weak on A” | Twin belief — Graph may **project** for UX/traversal, not own |

---

## 5. Out of scope

- Redesigning Graph schema
- Assessment-authored curriculum graphs
- Using Graph as recommendation engine
- Storing Evidence Bundles inside Graph

AP-002D Graph work, if any in implementation, is limited to ensuring projection refresh remains wired after assessment-triggered Reasoning — not new educational authority.
