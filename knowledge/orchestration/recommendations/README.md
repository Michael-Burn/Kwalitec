# Educational Recommendation Model

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS001 — Educational Recommendation Model  
**Classification:** Constitutional specification — structure and constitutional meaning of educational recommendations  
**Status:** APPROVED — governing for educational recommendation meaning  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **what a constitutional educational recommendation is**.

It answers *what objectives recommendations must serve*, *from which lawful sources they may be derived*, *which structural components they must carry*, *what recommendations may and must not do*, and *how recommendations are explained* — without inventing educational meaning, altering constitutional ownership, or executing workflows.

It does **not** implement Runtime A, rendering, UI, algorithms, databases, services, or analytics.

> **Recommendations communicate lawful educational guidance.  
> They do not create educational meaning, alter constitutional authority, or execute workflows.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-008 (Recommendations)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — mutation rights remain orthogonal
8. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities whose outputs may become recommendations; this Model never redefines them**
9. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration context recommendations may reference; this Model never invents stages or executes flows**
10. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map recommendations must preserve**
11. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **lawful disposition among competing valid recommendations; this Model defines the recommendation artefact, not conflict selection**
12. [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003) — **permission / refusal / conflict narration; recommendation explainability here specialises guidance communication, not ownership permission**

Related (non-authoritative for educational recommendation meaning):

- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority; does not replace Programme VII recommendation law
- Educational Validation Framework — quality release lens, not recommendation constitutional structure
- Product recommendation / ranking engines — operational proxies must consume this Model; they never redefine it

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_RECOMMENDATION_MODEL.md`](EDUCATIONAL_RECOMMENDATION_MODEL.md) | Constitutional overview: what a recommendation is, responsibilities, integrity, stack position |
| [`RECOMMENDATION_OBJECTIVES.md`](RECOMMENDATION_OBJECTIVES.md) | Constitutional objectives educational recommendations must serve |
| [`RECOMMENDATION_SOURCES.md`](RECOMMENDATION_SOURCES.md) | Lawful sources from which recommendations may be derived |
| [`RECOMMENDATION_STRUCTURE.md`](RECOMMENDATION_STRUCTURE.md) | Constitutional components every recommendation must carry |
| [`RECOMMENDATION_BOUNDARIES.md`](RECOMMENDATION_BOUNDARIES.md) | What recommendations may communicate and must never invent or alter |
| [`RECOMMENDATION_EXPLAINABILITY.md`](RECOMMENDATION_EXPLAINABILITY.md) | How recommendations are explained to students and developers |

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised educational guidance |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — supplies orchestration context |
| **Programme VII / WS2 / MS001 — Authority Model** | Catalogue *who owns* each educational decision class — supplies constitutional owner |
| **Programme VII / WS2 / MS002 — Conflict Resolution** | When valid recommendations compete, determine *which lawful outcome is acted upon* |
| **Programme VII / WS2 / MS003 — Authority Decision Explainability** | Explain *why a component was permitted to decide* |
| **Programme VII / WS3 / MS001 — this corpus** | Define *what a constitutional educational recommendation is* — structure, sources, objectives, boundaries, and guidance explainability |
| **Programme VII / WS3 / MS002 — Recommendation Assembly** | Define *how lawful recommendations are organised into a coherent recommendation set* — see [`../recommendation_assembly/`](../recommendation_assembly/) |

```
Educational Constitution / EIP
        │
        ▼
Programme VI meaning authorities
        │  emit educational guidance under coach / planner models
        ▼
Educational Authority Model (WS2 / MS001)
        │  names the constitutional owner of the decision
        ▼
Educational Workflow Engine (WS1)
        │  supplies orchestration context (event, stages, participation)
        ▼
Conflict Resolution Framework (WS2 / MS002)
        │  when concurrency arises: lawful acted-upon disposition
        ▼
Educational Recommendation Model (this milestone)
        │  unifies lawful outputs into the constitutional recommendation artefact
        │  communicates guidance — does not invent meaning or execute workflows
        ▼
Authorised educational recommendation
        │  explainable: why · contributors · owner · evidence · constitutional validity
        │  (+ authority-permission speech via WS2 / MS003 when ownership is narrated)
        ▼
Recommendation Assembly Framework (WS3 / MS002)
        │  organises lawful artefacts into a coherent recommendation set
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 settles *decision ownership, conflict disposition, and permission speech*.  
Programme VII Workstream 3 / MS001 settles *what a constitutional educational recommendation is*.  
Programme VII Workstream 3 / MS002 settles *how lawful recommendations form a coherent set*.  
EIP-001 settles *state mutation rights*.

## Architectural requirement

Educational recommendations may **communicate** constitutional outcomes and aggregate lawful educational outputs. They must **never**:

| Lawful | Unlawful |
|--------|----------|
| Surface guidance already authorised by a Programme VI owner | Invent educational meaning or tips without a documented source |
| Aggregate lawful outputs under published structure | Alter constitutional ownership or absorb a sibling domain |
| Reference authority, workflow, and conflict context | Reinterpret Educational Evidence or Twin estimates |
| Remain fully explainable end-to-end | Bypass constitutional workflows or Authority Model checks |
| Refuse / defer speech when no lawful warrant exists | Execute workflows, mutate states, or rank by undocumented scores |

If a proposed tip would require inventing meaning, silent ownership, or undocumented provenance, **amend the owning constitutional corpora first** — or refuse. Recommendations never gain educational authority by product convenience.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **Programme VI coach / planner models** | What each piece of guidance *means* educationally | Cross-cutting recommendation artefact law (this Model) |
| **WS1 Workflow Model / Transitions / Completion** | How flow is sequenced, moved, and concluded | What a recommendation *is* as a constitutional artefact (this Model) |
| **WS2 / MS001 Authority Model** | Who owns each decision class | Recommendation structure and source catalogue (this Model) |
| **WS2 / MS002 Conflict Resolution** | Which valid recommendation is *acted upon* when several compete | What each recommendation must contain as an artefact (this Model) |
| **WS2 / MS003 Authority Decision Explainability** | Why a component was *permitted* to decide | Why *this guidance* exists and what evidence supports it (this Model) |
| **This Educational Recommendation Model** | What a constitutional recommendation is — objectives, sources, structure, boundaries, explainability | How multiple lawful recommendations form a coherent *set* ([`../recommendation_assembly/`](../recommendation_assembly/)); algorithms, Runtime A, UI rendering, ranking, state mutation |
| **WS3 / MS002 Recommendation Assembly** | How lawful recommendations are organised into a coherent set | What a single recommendation artefact is (this Model); conflict disposition (WS2 / MS002) |

**Binding distinction:** Programme VI creates educational meaning. Workstream 1 coordinates flow. Workstream 2 owns ownership and conflict disposition. Workstream 3 / MS001 defines the **recommendation artefact** that communicates lawful guidance without becoming a second tutor. Workstream 3 / MS002 defines **set organisation** of already-valid artefacts.

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Rendering, UI components, navigation, or notifications
- Algorithms, scoring, ranking engines, or personalisation mathematics
- Database models, schemas, or ORM entities
- Analytics pipelines or telemetry schemas
- Workflow execution engines, sagas, job queues, or state machines in code
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)
- Amendments to Authority Model domains or Conflict Resolution CT/RP/RO catalogues by recommendation fiat

## How to use this corpus

1. Read `EDUCATIONAL_RECOMMENDATION_MODEL.md` first.
2. Treat objectives in `RECOMMENDATION_OBJECTIVES.md` as binding targets for every recommendation surface.
3. Derive recommendations only from sources listed in `RECOMMENDATION_SOURCES.md` — undocumented provenance is unlawful.
4. Require structural components in `RECOMMENDATION_STRUCTURE.md` before any student- or developer-facing tip is treated as constitutional.
5. Enforce limits in `RECOMMENDATION_BOUNDARIES.md` before any proposed recommendation behaviour.
6. Require explainability contracts from `RECOMMENDATION_EXPLAINABILITY.md` before student- or developer-facing recommendation narration; for ownership-permission speech, also consult [`../authority_explainability/`](../authority_explainability/).
7. When ownership is unclear, consult [`../authority/`](../authority/). When concurrency arises, consult [`../conflict_resolution/`](../conflict_resolution/). When stage order is at stake, consult [`../workflows/`](../workflows/).
8. Do not implement behaviours that contradict this corpus without amending it first.
