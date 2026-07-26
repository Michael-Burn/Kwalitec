# Conflict Resolution Framework

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS002 — Conflict Resolution Framework  
**Classification:** Constitutional specification — how simultaneously valid educational decisions yield one lawful outcome  
**Status:** APPROVED — governing for educational conflict resolution  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec resolves conflicts between simultaneously valid educational decisions** while preserving constitutional ownership.

It answers *when a conflict exists*, *which constitutional principles resolve it*, *which lawful outcomes may result*, and *how resolution is explained* — without transferring ownership, redefining educational meaning, or inventing a meta-coach.

It does **not** implement Runtime A, conflict-resolution algorithms, scheduling, execution engines, databases, services, UI, or analytics.

> **Conflict resolution preserves authority.  
> It never transfers ownership or changes educational meaning.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — mutation rights remain orthogonal
7. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map this Framework must preserve; resolution never amends ownership by fiat**
8. Programme VI constitutional corpora — **educational meaning authorities whose outputs may compete for action; this Framework never redefines them**
9. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration flow that may surface concurrent recommendations; this Framework governs lawful selection among them, not stage invention**

Related (non-authoritative for conflict-resolution law):

- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority; does not replace Programme VII conflict law
- Educational Validation Framework — quality release lens, not coordination outcomes

## Contents

| Document | Role |
|---|---|
| [`CONFLICT_RESOLUTION_FRAMEWORK.md`](CONFLICT_RESOLUTION_FRAMEWORK.md) | Constitutional overview: what conflict resolution is, responsibilities, integrity, stack position |
| [`CONFLICT_TYPES.md`](CONFLICT_TYPES.md) | Constitutional conflict kinds that may arise (coordination only) |
| [`RESOLUTION_PRINCIPLES.md`](RESOLUTION_PRINCIPLES.md) | Binding principles used to resolve conflicts without transferring ownership |
| [`RESOLUTION_OUTCOMES.md`](RESOLUTION_OUTCOMES.md) | Lawful outcomes of conflict resolution |
| [`RESOLUTION_EXPLAINABILITY.md`](RESOLUTION_EXPLAINABILITY.md) | How conflict resolution is explained to students and developers (MS002 disposition-layer contract) |

Related (downstream explanation law):

- [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003) — unified permission narrative spanning ordinary decisions, delegation, and conflict; must remain consistent with `RESOLUTION_EXPLAINABILITY.md` and must not invent CT/RP/RO law

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised recommendations |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — may surface concurrent valid artefacts |
| **Programme VII / WS2 / MS001 — Authority Model** | Catalogue *who owns* each educational decision class |
| **Programme VII / WS2 / MS002 — this corpus** | When multiple *constitutionally valid* recommendations coexist, determine *which lawful educational outcome is acted upon* |
| **Programme VII / WS2 / MS003 — Authority Decision Explainability** | Explain *why a component was permitted* (and why alternatives were not) across ownership and conflict paths |

```
Educational Constitution / EIP
        │
        ▼
Programme VI meaning authorities
        │  may each emit constitutionally valid recommendations
        ▼
Educational Authority Model (WS2 / MS001)
        │  ownership map — who may decide what (unchanged by resolution)
        ▼
Educational Workflow Engine (WS1)
        │  may surface concurrent valid recommendations for coordination
        ▼
Conflict Resolution Framework (this milestone)
        │  selects lawful outcome among valid recommendations
        │  preserves ownership · meaning · boundaries
        ▼
Authorised educational outcome acted upon
        │  explainable (WS2 / MS003): conflict → rules → outcome → ownership intact
        │  (+ ordinary / delegation permission speech when no concurrency)
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 / MS001 settles *decision ownership*.  
Programme VII Workstream 2 / MS002 settles *lawful outcome when valid recommendations compete for action*.  
Programme VII Workstream 2 / MS003 settles *how permission and conflict disposition are explained*.  
EIP-001 settles *state mutation rights*.

## Architectural requirement

Conflict resolution may determine **which constitutionally valid recommendation is acted upon**. It must **never**:

| Lawful | Unlawful |
|--------|----------|
| Defer, supersede, queue, merge (where permitted), or reject as unlawful per published rules | Transfer decision ownership from one constitutional owner to another |
| Apply higher constitutional obligations where explicitly defined | Redefine Programme VI educational meaning while “resolving” |
| Preserve each owner’s domain after the outcome | Modify Authority Model boundaries by runtime convenience |
| Explain why the conflict existed and why the outcome was lawful | Invent a meta-coach that absorbs sibling meanings |
| Coordinate action among already-valid artefacts | Resolve by ranking scores, optimiser discretion, or silent product preference |

If a proposed behaviour would require inventing ownership, rewriting meaning, or discretionary arbitration, **amend the owning constitutional corpora first** — or refuse. Conflict resolution never gains authority by shortcut.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **WS2 / MS001 Authority Model** | Who owns each decision class; how ownership is preserved | Which valid recommendation is acted on when several coexist (this Framework) |
| **WS1 Workflow Model / Transitions / Completion** | How flow is sequenced, moved, and concluded | Lawful selection among concurrent valid educational outcomes (this Framework) |
| **Programme VI coach / planner models** | What each recommendation means educationally | Cross-cutting conflict-resolution law (this Framework) |
| **This Conflict Resolution Framework** | How conflicts among valid recommendations yield one lawful acted-upon outcome | Algorithms, Runtime A, ownership maps, educational meaning |
| **WS2 / MS003 Authority Decision Explainability** | Why a component was permitted to decide / why alternatives were not (including conflict paths) | CT/RP/RO catalogue amendments; ownership map; UI rendering |

**Binding distinction:** MS001 prevents *competing ownership claims* by design (single owner). MS002 resolves *competing action among already-valid recommendations* without collapsing ownership. Ownership conflicts that violate AP-01 are **not** resolved here — they are refused and referred to the Authority Model. MS003 narrates permission and disposition faithfully — it does not invent unpublished precedence.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Conflict-resolution algorithms, scoring, ranking engines, or priority heaps
- Scheduling / calendar packing
- Workflow execution engines, sagas, job queues, or state machines in code
- Database models, schemas, or ORM entities
- UI components, navigation, or notifications
- Analytics pipelines or telemetry schemas
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)
- Amendments to Authority Model domains by resolution fiat

## How to use this corpus

1. Read `CONFLICT_RESOLUTION_FRAMEWORK.md` first.
2. Classify the situation under `CONFLICT_TYPES.md` — confirm it is coordination among valid artefacts, not an ownership dispute.
3. Apply binding principles in `RESOLUTION_PRINCIPLES.md` — never invent discretionary arbitration.
4. Select only outcomes listed in `RESOLUTION_OUTCOMES.md`.
5. Require explainability contracts from `RESOLUTION_EXPLAINABILITY.md` before student- or developer-facing conflict narration; for the unified authority-permission explanation contract, also consult [`../authority_explainability/`](../authority_explainability/) (MS003).
6. When ownership is unclear or contested, consult [`../authority/`](../authority/) — do not “resolve” ownership here.
7. When stage order is at stake, consult [`../workflows/`](../workflows/) and siblings — do not invent stages via conflict outcomes.
8. Do not implement behaviours that contradict this corpus without amending it first.
