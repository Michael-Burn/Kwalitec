# Recommendation Assembly Framework

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS002 — Recommendation Assembly Framework  
**Classification:** Constitutional specification — how lawful educational recommendations are assembled into coherent recommendation sets  
**Status:** APPROVED — governing for recommendation assembly  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how constitutionally valid educational recommendations are organised into a single coherent recommendation set**.

It answers *what assembly must optimise*, *which components an assembled set must carry*, *what assembly may and must not do*, and *how recommendation sets are explained* — without inventing educational meaning, altering ownership, resolving conflicts, or executing workflows.

It does **not** implement Runtime A, ranking algorithms, recommendation scoring, rendering, UI, databases, services, or analytics.

> **Assembly organises recommendations.  
> It does not create educational meaning, alter ownership, resolve conflicts, or execute workflows.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-008 (Recommendations)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — mutation rights remain orthogonal
8. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities; assembly never redefines them**
9. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration context a set may reference; assembly never invents stages or executes flows**
10. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map assembly must preserve**
11. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **lawful disposition among competing valid recommendations; assembly references disposition, never re-resolves**
12. [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003) — **permission / refusal / conflict narration; assembly explainability specialises set-level organisation speech**
13. [`../recommendations/`](../recommendations/) — Educational Recommendation Model (WS3 / MS001) — **defines what each constituent recommendation is; this Framework organises already-valid artefacts into sets**

Related (non-authoritative for assembly law):

- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority; does not replace Programme VII assembly law
- Educational Validation Framework — quality release lens, not assembly constitutional structure
- Product recommendation / ranking engines — operational proxies must consume this Framework; they never redefine it

## Contents

| Document | Role |
|---|---|
| [`RECOMMENDATION_ASSEMBLY_FRAMEWORK.md`](RECOMMENDATION_ASSEMBLY_FRAMEWORK.md) | Constitutional overview: what assembly is, responsibilities, integrity, stack position |
| [`ASSEMBLY_OBJECTIVES.md`](ASSEMBLY_OBJECTIVES.md) | Constitutional objectives recommendation assembly must serve |
| [`ASSEMBLY_COMPONENTS.md`](ASSEMBLY_COMPONENTS.md) | Constitutional components every assembled recommendation set must carry |
| [`ASSEMBLY_BOUNDARIES.md`](ASSEMBLY_BOUNDARIES.md) | What assembly may organise and must never invent or resolve |
| [`ASSEMBLY_EXPLAINABILITY.md`](ASSEMBLY_EXPLAINABILITY.md) | How assembled recommendation sets are explained to students and developers |

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised educational guidance |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — supplies orchestration context |
| **Programme VII / WS2 / MS001 — Authority Model** | Catalogue *who owns* each educational decision class — supplies constitutional owner |
| **Programme VII / WS2 / MS002 — Conflict Resolution** | When valid recommendations compete, determine *which lawful outcome is acted upon* |
| **Programme VII / WS2 / MS003 — Authority Decision Explainability** | Explain *why a component was permitted to decide* |
| **Programme VII / WS3 / MS001 — Educational Recommendation Model** | Define *what a constitutional educational recommendation is* |
| **Programme VII / WS3 / MS002 — this corpus** | Define *how lawful recommendations are assembled into a coherent recommendation set* |
| **Programme VII / WS3 / MS003 — Recommendation Set Explainability** | Explain *why the set exists, how it was assembled, and how it should be interpreted* |

```
Educational Constitution / EIP
        │
        ▼
Programme VI meaning authorities
        │  emit educational guidance under coach / planner models
        ▼
Educational Authority Model (WS2 / MS001)
        │  names the constitutional owner of each decision
        ▼
Educational Workflow Engine (WS1)
        │  supplies orchestration context (event, stages, participation)
        ▼
Conflict Resolution Framework (WS2 / MS002)
        │  when concurrency arises: lawful acted-upon disposition
        ▼
Educational Recommendation Model (WS3 / MS001)
        │  closes the single recommendation artefact
        ▼
Recommendation Assembly Framework (this milestone)
        │  organises lawful artefacts into one coherent recommendation set
        │  preserves ownership · provenance · consistency — never invents or resolves
        ▼
Recommendation Set Explainability (WS3 / MS003)
        │  narrates why the set exists · how assembled · how to interpret
        ▼
Authorised educational recommendation set
        │  explainable: why together · how related · sources · provenance preserved
        │  (+ per-artefact explainability via WS3 / MS001; permission via WS2 / MS003)
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 settles *decision ownership, conflict disposition, and permission speech*.  
Programme VII Workstream 3 / MS001 settles *what a constitutional educational recommendation is*.  
Programme VII Workstream 3 / MS002 settles *how lawful recommendations form a coherent set*.  
Programme VII Workstream 3 / MS003 settles *how assembled recommendation sets are explained*.  
EIP-001 settles *state mutation rights*.

## Architectural requirement

Recommendation assembly may **organise** already-lawful recommendations and **preserve** constitutional context. It must **never**:

| Lawful | Unlawful |
|--------|----------|
| Organise constitutionally valid recommendations into a set | Invent recommendations or average coaches into a new tip |
| Reference workflow, authority, and conflict context | Alter recommendation ownership or absorb sibling domains |
| Preserve provenance of each constituent | Redefine educational meaning while “assembling” |
| Maintain internal consistency of the set | Resolve conflicts already governed by WS2 / MS002 |
| Support explainable recommendation sets | Bypass constitutional workflows or Authority Model checks |
| Surface disposition already decided by Conflict Resolution | Rank, score, or personally optimise winners as assembly law |

If a proposed set would require inventing tips, silent ownership, undocumented provenance, or re-resolving conflicts, **amend the owning constitutional corpora first** — or refuse. Assembly never gains educational authority by product convenience.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **Programme VI coach / planner models** | What each piece of guidance *means* educationally | Cross-cutting set organisation law (this Framework) |
| **WS1 Workflow Model / Transitions / Completion** | How flow is sequenced, moved, and concluded | How multiple recommendations form one set (this Framework) |
| **WS2 / MS001 Authority Model** | Who owns each decision class | Set composition and provenance packaging (this Framework) |
| **WS2 / MS002 Conflict Resolution** | Which valid recommendation is *acted upon* when several compete | How dispositioned artefacts are *organised together* in a set (this Framework) |
| **WS2 / MS003 Authority Decision Explainability** | Why a component was *permitted* to decide | Why recommendations *appear together* as a set (this Framework) |
| **WS3 / MS001 Educational Recommendation Model** | What a single constitutional recommendation *is* | How multiple lawful recommendations form a coherent *set* (this Framework) |
| **WS3 / MS003 Recommendation Set Explainability** | Why the set exists / how assembled / how interpreted | Set organisation law itself (this Framework); tip invention; ownership maps |
| **This Recommendation Assembly Framework** | How lawful recommendations are assembled into coherent sets | Algorithms, Runtime A, UI rendering, ranking, conflict resolution, state mutation |

**Binding distinction:** Programme VI creates educational meaning. Workstream 1 coordinates flow. Workstream 2 owns ownership and conflict disposition. Workstream 3 / MS001 defines the **recommendation artefact**. Workstream 3 / MS002 defines **set organisation** of already-valid artefacts — never a second tutor, never a conflict engine, never a ranking layer. Workstream 3 / MS003 defines **how organised sets are explained**.

## Out of scope (MS002)

- Runtime A integration, feature flags, or services
- Ranking algorithms, recommendation scoring, or personalisation mathematics
- Rendering, UI components, navigation, or notifications
- Database models, schemas, or ORM entities
- Analytics pipelines or telemetry schemas
- Workflow execution engines, sagas, job queues, or state machines in code
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)
- Amendments to Authority Model domains or Conflict Resolution CT/RP/RO catalogues by assembly fiat
- Amendments to the Educational Recommendation Model artefact law by assembly packaging convenience

## How to use this corpus

1. Read `RECOMMENDATION_ASSEMBLY_FRAMEWORK.md` first.
2. Treat objectives in `ASSEMBLY_OBJECTIVES.md` as binding targets for every recommendation-set surface.
3. Require set components in `ASSEMBLY_COMPONENTS.md` before any multi-recommendation packaging is treated as constitutional.
4. Enforce limits in `ASSEMBLY_BOUNDARIES.md` before any proposed assembly behaviour.
5. Require explainability contracts from `ASSEMBLY_EXPLAINABILITY.md` before student- or developer-facing set narration; for the full set-explanation model (principles, components, boundaries, patterns), consult [`../recommendation_explainability/`](../recommendation_explainability/); for each constituent tip, also consult [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md); for ownership-permission speech, consult [`../authority_explainability/`](../authority_explainability/).
6. Admit only constituents that satisfy [`../recommendations/`](../recommendations/) — incomplete artefacts are not assembly inputs.
7. When ownership is unclear, consult [`../authority/`](../authority/). When concurrency arises, consult [`../conflict_resolution/`](../conflict_resolution/) — do not re-resolve here. When stage order is at stake, consult [`../workflows/`](../workflows/).
8. Do not implement behaviours that contradict this corpus without amending it first.
