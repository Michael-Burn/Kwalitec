# Authority Decision Explainability

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS003 — Authority Decision Explainability  
**Classification:** Constitutional specification — how authority decisions, delegations, and conflict resolutions are explained  
**Status:** APPROVED — governing for authority decision explainability  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec explains educational authority decisions** — why a constitutional component was permitted to decide, why alternatives were not, how delegation and conflict disposition are narrated, and what explanations must never invent.

It answers:

> **“Why was this constitutional component permitted to make this decision, and why were alternative components not permitted to do so?”**

It does **not** redefine educational meaning, alter decision ownership, perform orchestration, implement Runtime A, or invent unpublished precedence rules.

> **Authority explanations communicate constitutional reasoning only.  
> They do not introduce educational meaning, alter ownership, or perform orchestration.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — mutation rights remain orthogonal
7. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map that explanations must faithfully describe**
8. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **lawful disposition law that conflict explanations must faithfully describe**
9. Programme VI constitutional corpora — **educational meaning authorities whose decisions may be framed by ownership speech; this corpus never redefines them**
10. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration participation may be referenced; this corpus never invents stage order or recommendations**

Related (non-authoritative for authority decision explainability law):

- [`../authority/AUTHORITY_EXPLAINABILITY.md`](../authority/AUTHORITY_EXPLAINABILITY.md) — MS001 ownership-layer speech contract; this corpus generalises and binds the *decision permission* narrative across ownership, delegation, and conflict
- [`../conflict_resolution/RESOLUTION_EXPLAINABILITY.md`](../conflict_resolution/RESOLUTION_EXPLAINABILITY.md) — MS002 conflict-disposition speech contract; this corpus requires consistency with it and does not replace CT/RP/RO law
- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority; does not replace Programme VII explainability
- Educational Validation Framework — quality release lens, not authority narration law

## Contents

| Document | Role |
|---|---|
| [`AUTHORITY_DECISION_EXPLAINABILITY.md`](AUTHORITY_DECISION_EXPLAINABILITY.md) | Constitutional overview: what authority decision explainability is, stack position, integrity |
| [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md) | Binding principles governing authority explanations |
| [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md) | Information every authority explanation should contain |
| [`EXPLANATION_BOUNDARIES.md`](EXPLANATION_BOUNDARIES.md) | What explanations may say and must never invent |
| [`EXPLANATION_EXAMPLES.md`](EXPLANATION_EXAMPLES.md) | Illustrative constitutional explanation patterns |

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised recommendations |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners |
| **Programme VII / WS2 / MS001 — Authority Model** | Catalogue *who owns* each educational decision class |
| **Programme VII / WS2 / MS002 — Conflict Resolution** | When valid recommendations compete, determine *which lawful outcome is acted upon* |
| **Programme VII / WS2 / MS003 — this corpus** | Describe *why a component was permitted to decide* (and why others were not) — consistently across ordinary decisions, delegation, and conflict disposition |

```
Educational Constitution / EIP
        │
        ▼
Programme VI meaning authorities
        │  educational reasoning + coach/planner explainability
        ▼
Educational Authority Model (WS2 / MS001)
        │  ownership map — who may decide what
        ▼
Conflict Resolution Framework (WS2 / MS002)
        │  lawful acted-upon outcome among valid peers (when concurrency arises)
        ▼
Authority Decision Explainability (this milestone)
        │  constitutional narration of permission, refusal, delegation, conflict
        │  faithfully describes MS001 / MS002 — never invents ownership or precedence
        ▼
Speakable authorised outcome
        │  owner permitted · alternatives refused · rules applied · ownership intact
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 / MS001 settles *decision ownership*.  
Programme VII Workstream 2 / MS002 settles *lawful action when valid recommendations compete*.  
Programme VII Workstream 2 / MS003 settles *how ownership, permission, and conflict disposition are explained*.  
EIP-001 settles *state mutation rights*.  
EIP-003 settles *student-facing educational speech honesty* — this corpus specialises *authority-permission* speech.

## Architectural requirement

Authority explanations must **faithfully describe** constitutional ownership and lawful resolution.

They must **never**:

| Lawful | Unlawful |
|--------|----------|
| Name the decision owner and why that owner was permitted | Imply ownership transferred to a sibling, workflow, or “the app” |
| Cite constitutional authority invoked (AP / AD / AB; RP / CT / RO when conflict) | Invent unpublished precedence, scoring, or discretionary winners |
| Identify consumed recommendations and refused alternatives | Redefine educational meaning while “explaining” |
| Describe delegation without alienating ownership | Present AP-04 exercise as a new standing owner |
| Describe conflict disposition without rewriting owners | Narrate RO outcomes as ownership or meaning amendments |
| Reference workflow participation as orchestration context | Claim the Workflow Engine decided educational content |

If a proposed narration would require inventing ownership, altering meaning, or publishing undeclared rules, **amend the owning constitutional corpora first** — or refuse the narration. Explainability never gains authority by storytelling.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **WS2 / MS001 Authority Model** | Who owns each decision class | How permission/refusal/delegation/conflict are narrated consistently (this corpus) |
| **WS2 / MS001 `AUTHORITY_EXPLAINABILITY.md`** | Ownership-layer speech themes for MS001 | Full decision-explainability model spanning delegation and conflict (this corpus specialises and binds) |
| **WS2 / MS002 Conflict Resolution** | Which valid recommendation is acted upon; CT/RP/RO law | Unified permission narrative across non-conflict and conflict paths (this corpus) |
| **WS2 / MS002 `RESOLUTION_EXPLAINABILITY.md`** | Conflict-disposition speech (RQ1–RQ4) | Ordinary authority permission and delegation patterns outside concurrency (this corpus) |
| **WS1 Workflow / Transition / Completion explainability** | Why flow started, moved, or completed | Why a *decision owner* was constitutionally permitted (this corpus) |
| **Programme VI `*_EXPLAINABILITY.md`** | Why *this educational answer* emerged | Why *this owner* could speak and others could not (this corpus) |
| **This Authority Decision Explainability** | Why permitted / why not / what constitutional facts an explanation must carry | Algorithms, Runtime A, UI rendering, ownership maps, meaning rewrites |

**Binding distinction:** MS001 owns the ownership map. MS002 owns conflict disposition law. MS003 owns the **constitutional explanation contract** for authority decisions — including ordinary decisions, delegations, and conflict resolutions — without amending either map or disposition catalogue.

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Rendering engines, UI components, navigation, templates, or notifications
- Explanation algorithms, ranking, scoring, or natural-language generation systems
- Database models, schemas, or ORM entities
- Analytics pipelines or telemetry schemas
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning
- Amendments to Authority Model domains or Conflict Resolution outcomes by explanation fiat
- Workflow execution engines, sagas, job queues, or state machines in code

## How to use this corpus

1. Read `AUTHORITY_DECISION_EXPLAINABILITY.md` first.
2. Treat principles in `EXPLANATION_PRINCIPLES.md` as binding for every authority narration path.
3. Require the information set in `EXPLANATION_COMPONENTS.md` before student- or developer-facing authority speech.
4. Enforce limits in `EXPLANATION_BOUNDARIES.md` — refuse narration that invents ownership, meaning, or unpublished rules.
5. Use `EXPLANATION_EXAMPLES.md` as illustrative patterns, not as a closed catalogue of product copy.
6. When ownership is at stake, consult [`../authority/`](../authority/) — explain what that Model already authorises.
7. When conflict disposition is at stake, consult [`../conflict_resolution/`](../conflict_resolution/) — explain what that Framework already authorises.
8. When educational meaning is at stake, defer to Programme VI explainability — this corpus frames *who was permitted*, not *what the tutor meant*.
9. Do not implement behaviours that contradict this corpus without amending it first.
