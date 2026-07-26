# Educational Authority Model

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS001 — Educational Authority Model  
**Classification:** Constitutional authority specification — ownership of educational decisions across Programme VI and Programme VII components  
**Status:** APPROVED — governing for educational authority ownership  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **which constitutional component has authority to make which educational decisions**.

It answers *who owns each class of educational decision*, *how authority may be delegated without being absorbed*, *where authority is bounded*, *how authority is preserved and restored*, and *how Kwalitec explains why one component decided and another could not*.

It does **not** redefine educational meaning, orchestrate workflows, implement Runtime A, resolve conflicts algorithmically, or mutate educational states.

Lawful disposition when multiple *constitutionally valid* recommendations compete for action is owned by [`../conflict_resolution/`](../conflict_resolution/) (WS2 / MS002) — that Framework preserves this Model’s ownership map; it does not amend it.

> **Authority governs ownership of educational decisions.  
> It does not redefine educational meaning or orchestrate workflows.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`](../../educational/KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md) (EIP-006)
6. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
7. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — **mutation rights for educational states**; this Model owns **decision ownership**, not write paths
8. Programme VI constitutional corpora (Master Planner, Daily Coach, Learning Coach, Recovery Coach, Revision Coach, Exam Coach) — **educational meaning authorities whose decision ownership this Model catalogues, never redefines**
9. [`../workflows/`](../workflows/) — Educational Workflow Model (Programme VII / Workstream 1) — **orchestration of flow**; this Model owns **who may decide**, not stage sequencing

Related (non-authoritative for educational authority ownership):

- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority (infrastructure / engines); does not replace Programme VI / VII educational decision ownership
- [`../../version2/ARCHITECTURE_DECISIONS/ADR-006-Authority-Boundaries.md`](../../version2/ARCHITECTURE_DECISIONS/ADR-006-Authority-Boundaries.md) — production integration boundaries
- Educational Validation Framework — quality release lens, not educational meaning or decision-authority ownership

## Contents

| Document | Role |
|---|---|
| [`EDUCATIONAL_AUTHORITY_MODEL.md`](EDUCATIONAL_AUTHORITY_MODEL.md) | Constitutional overview: what educational authority is, responsibilities, integrity, stack position |
| [`AUTHORITY_PRINCIPLES.md`](AUTHORITY_PRINCIPLES.md) | Binding principles: single owner, delegation, bounds, preservation, restoration, explicitness |
| [`AUTHORITY_DOMAINS.md`](AUTHORITY_DOMAINS.md) | Domains owned by each constitutional component — owned / consumed / prohibited decisions |
| [`AUTHORITY_BOUNDARIES.md`](AUTHORITY_BOUNDARIES.md) | Constitutional limits no component may cross |
| [`AUTHORITY_EXPLAINABILITY.md`](AUTHORITY_EXPLAINABILITY.md) | How authority decisions, refusals, and preservation are explained (MS001 ownership-layer contract) |

Related (downstream explanation law):

- [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003) — unified constitutional contract for permission, refusal, delegation, and conflict narration; faithfully describes this Model without amending it

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* for planning, today, learning, recovery, revision, and examination |
| **Programme VII / WS1 — Educational Workflow Model** | Decide *how those reasonings are sequenced, handed off, and concluded* |
| **Programme VII / WS2 / MS001 — this corpus** | Decide *which component owns which educational decision* — the constitutional ownership map |
| **Programme VII / WS2 / MS002 — Conflict Resolution** | When multiple valid recommendations coexist, decide *which lawful outcome is acted upon* — without transferring ownership |
| **Programme VII / WS2 / MS003 — Authority Decision Explainability** | Decide *how permission, refusal, delegation, and conflict disposition are explained* — without inventing ownership |
| **EIP-001 State Authority Matrix** | Decide *who may mutate which educational state* (distinct from decision ownership) |

```
Educational Constitution / EIP
        │  educational truth, evidence, continuity, mutation rights
        ▼
Programme VI meaning authorities
        │  Master Planner · Daily · Learning · Recovery · Revision · Exam
        │  each owns educational questions and meaning
        ▼
Educational Authority Model (this milestone)
        │  catalogues decision ownership — who may decide what
        │  does not invent meaning or stage order
        ▼
Educational Workflow Engine (WS1)
        │  sequences / hands off / concludes among owners
        │  may surface concurrent valid recommendations
        ▼
Conflict Resolution Framework (WS2 / MS002)
        │  lawful acted-upon outcome among valid peers
        │  preserves this ownership map
        ▼
Authorised educational outcome
        │  explainable (WS2 / MS003): why permitted → why alternatives not → rules → ownership intact
        │  (+ conflict disposition when concurrency arose)
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 / MS001 settles *decision ownership*.  
Programme VII Workstream 2 / MS002 settles *lawful action when valid recommendations compete*.  
Programme VII Workstream 2 / MS003 settles *how ownership permission and conflict disposition are explained*.  
EIP-001 settles *state mutation rights*.

## Architectural requirement

Educational authority must be **explicit**. No component may:

| Lawful | Unlawful |
|--------|----------|
| Own the decisions listed in its domain | Infer ownership from convenience, UI proximity, or performance |
| Consume another component’s authorised outputs as inputs | Reinterpret another component’s educational meaning |
| Delegate narrowly while remaining accountable | Modify the Canonical Study Plan outside Master Planner / Scheduling authority |
| Refuse a decision outside its domain and name the owner | Redefine Educational Evidence or Twin estimates under a coach label |
| Restore authority after temporary delegation or handoff | Claim educational ownership beyond its constitutional domain |

If a proposed behaviour would require inventing ownership, **amend this Model first** — or refuse. Authority is never gained by silent absorption.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **Programme VI coach / planner models** | What educational question means and how it is reasoned | Cross-cutting ownership catalogue (this Model) |
| **Programme VII Workflow Model** | How decisions flow between components | Who owns each decision class (this Model) |
| **EIP-001 State Authority Matrix** | Who may write Study Progress, Evidence, Mastery, … | Who owns “what to study today” vs “how to recover” (this Model) |
| **This Educational Authority Model** | Which component may make which educational decision | Algorithms, Runtime A, workflow stages, state writers |
| **WS2 / MS002 Conflict Resolution** | Which valid recommendation is acted upon when several coexist | Ownership map amendments; meaning rewrites; ranking algorithms |
| **WS2 / MS003 Authority Decision Explainability** | Why a component was permitted to decide and why alternatives were not | Ownership map; conflict outcome catalogue; Runtime A / UI rendering |

## Out of scope (MS001)

- Runtime A integration, feature flags, or services
- Conflict-resolution algorithms or ranking engines (constitutional conflict law lives in [`../conflict_resolution/`](../conflict_resolution/) — MS002; algorithms remain out of scope there too)
- Workflow execution engines, sagas, job queues, or state machines in code
- Scheduling / calendar packing
- Database models, schemas, or ORM entities
- UI components, navigation, or notifications
- Analytics pipelines or telemetry schemas
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning (owned by those corpora)

## How to use this corpus

1. Read `EDUCATIONAL_AUTHORITY_MODEL.md` first.
2. Treat principles in `AUTHORITY_PRINCIPLES.md` as binding for every educational decision path.
3. Classify proposed decisions under `AUTHORITY_DOMAINS.md` — owned, consumed, or prohibited for each domain.
4. Enforce limits in `AUTHORITY_BOUNDARIES.md` before any proposed cross-component behaviour.
5. Require explainability contracts from `AUTHORITY_EXPLAINABILITY.md` before student- or developer-facing authority narration; for the unified permission / delegation / conflict explanation contract, consult [`../authority_explainability/`](../authority_explainability/) (MS003).
6. When orchestration needs an owner, consult this Model; when orchestration needs stage order, consult [`../workflows/`](../workflows/).
7. When mutation rights are at stake, consult EIP-001 — do not conflate decision ownership with write authority.
8. Do not implement behaviours that contradict this corpus without amending it first.
