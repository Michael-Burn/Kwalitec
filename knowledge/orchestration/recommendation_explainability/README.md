# Recommendation Set Explainability

**Programme:** VII — Workstream 3 — Educational Recommendation Engine  
**Milestone:** MS003 — Recommendation Set Explainability  
**Classification:** Constitutional specification — how assembled educational recommendation sets are explained  
**Status:** APPROVED — governing for recommendation set explainability  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Purpose

This folder defines **how Kwalitec explains an assembled educational recommendation set** — why the set exists, how its constituent recommendations were organised, how the set should be interpreted, and what explanations must never invent.

It answers:

> **“Why does this recommendation set exist, how were its constituent recommendations assembled, and how should it be interpreted?”**

It does **not** create recommendations, alter ownership, resolve conflicts, execute workflows, implement Runtime A, or invent unpublished constitutional rules.

> **Recommendation set explanations communicate constitutional reasoning only.  
> They do not create recommendations, alter ownership, resolve conflicts, or execute workflows.**

## Authority

Subordinate to:

1. [`../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md) (EGI-001)
2. [`../../educational/EDUCATIONAL_LOGIC_REGISTRY.md`](../../educational/EDUCATIONAL_LOGIC_REGISTRY.md) (EGI-002) — especially EL-008 (Recommendations)
3. [`../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md`](../../educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md) (EIP-003)
4. [`../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md`](../../educational/EDUCATIONAL_CONTINUITY_STANDARD.md) (EIP-005)
5. [`../../educational/EDUCATIONAL_EVIDENCE_MODEL.md`](../../educational/EDUCATIONAL_EVIDENCE_MODEL.md) (EIP-002)
6. [`../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md`](../../educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md) (EIP-001) — mutation rights remain orthogonal
7. Programme VI constitutional corpora — **educational meaning authorities whose guidance may be framed by set speech; this corpus never redefines them**
8. [`../workflows/`](../workflows/) and siblings — Educational Workflow Engine (WS1) — **orchestration context explanations may reference; this corpus never invents stage order or executes flows**
9. [`../authority/`](../authority/) — Educational Authority Model (WS2 / MS001) — **ownership map explanations must faithfully describe**
10. [`../conflict_resolution/`](../conflict_resolution/) — Conflict Resolution Framework (WS2 / MS002) — **disposition law explanations must faithfully describe**
11. [`../authority_explainability/`](../authority_explainability/) — Authority Decision Explainability (WS2 / MS003) — **permission / refusal speech when ownership narration is material**
12. [`../recommendations/`](../recommendations/) — Educational Recommendation Model (WS3 / MS001) — **per-constituent artefact law and tip-level explainability**
13. [`../recommendation_assembly/`](../recommendation_assembly/) — Recommendation Assembly Framework (WS3 / MS002) — **set organisation law that explanations must faithfully describe**

Related (non-authoritative for recommendation set explainability law):

- [`../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md`](../recommendation_assembly/ASSEMBLY_EXPLAINABILITY.md) — MS002 set-organisation speech contract (RAQ-01…RAQ-04); this corpus generalises and binds the *full* recommendation-set explanation model (principles, components, boundaries, patterns)
- [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md) — per-constituent tip explainability (ERQ-01…ERQ-05); remains mandatory and is not replaced here
- [`../../version2/AUTHORITY_MATRIX.md`](../../version2/AUTHORITY_MATRIX.md) — Version 2 bounded-context authority; does not replace Programme VII explainability
- Educational Validation Framework — quality release lens, not set-narration law

## Contents

| Document | Role |
|---|---|
| [`RECOMMENDATION_SET_EXPLAINABILITY.md`](RECOMMENDATION_SET_EXPLAINABILITY.md) | Constitutional overview: what recommendation set explainability is, stack position, integrity |
| [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md) | Binding principles governing recommendation set explanations |
| [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md) | Information every recommendation set explanation should contain |
| [`EXPLANATION_BOUNDARIES.md`](EXPLANATION_BOUNDARIES.md) | What explanations may say and must never invent |
| [`EXPLANATION_EXAMPLES.md`](EXPLANATION_EXAMPLES.md) | Illustrative constitutional explanation patterns |

## Relationship in the Programme VII stack

| Horizon | Job |
|---------|-----|
| **Programme VI — Master Planner & coaches** | Define *educational meaning* and emit authorised recommendations |
| **Programme VII / WS1 — Workflow Engine** | Sequence, hand off, and conclude among owners — supplies orchestration context |
| **Programme VII / WS2 — Authority / Conflict / Permission speech** | Ownership, disposition, and why a component was *permitted* to decide |
| **Programme VII / WS3 / MS001 — Educational Recommendation Model** | Define *what a constitutional educational recommendation is* |
| **Programme VII / WS3 / MS002 — Recommendation Assembly Framework** | Define *how lawful recommendations are organised into a coherent set* |
| **Programme VII / WS3 / MS003 — this corpus** | Describe *why the set exists, how it was assembled, and how it should be interpreted* |

```
Educational Constitution / EIP
        │
        ▼
Programme VI meaning authorities
        │  emit educational guidance under coach / planner models
        ▼
Educational Authority Model + Conflict Resolution + Authority Explainability (WS2)
        │  ownership · disposition · permission speech
        ▼
Educational Workflow Engine (WS1)
        │  orchestration context the set may reference
        ▼
Educational Recommendation Model (WS3 / MS001)
        │  closes each single recommendation artefact (+ tip explainability)
        ▼
Recommendation Assembly Framework (WS3 / MS002)
        │  organises lawful artefacts into one coherent recommendation set
        ▼
Recommendation Set Explainability (this milestone)
        │  constitutional narration of set existence, assembly, and interpretation
        │  faithfully describes MS001 / MS002 — never invents tips, ownership, or disposition
        ▼
Speakable authorised recommendation set
        │  why exists · how assembled · how to interpret · provenance intact
```

Programme VI settles *educational meaning*.  
Programme VII Workstream 1 settles *orchestration flow*.  
Programme VII Workstream 2 settles *decision ownership, conflict disposition, and permission speech*.  
Programme VII Workstream 3 / MS001 settles *what a constitutional educational recommendation is*.  
Programme VII Workstream 3 / MS002 settles *how lawful recommendations form a coherent set*.  
Programme VII Workstream 3 / MS003 settles *how assembled recommendation sets are explained*.  
EIP-001 settles *state mutation rights*.  
EIP-003 settles *student-facing educational speech honesty* — this corpus specialises *recommendation-set* speech.

## Architectural requirement

Recommendation set explanations must **faithfully describe** how constitutionally valid recommendations were assembled.

They must **never**:

| Lawful | Unlawful |
|--------|----------|
| Describe why the set exists and how members relate | Invent recommendations or filler tips in speech |
| Reference constitutional provenance and sources | Imply newly created educational meaning from packaging |
| Name recommendation owners without absorbing them | Transfer or rewrite ownership by narration |
| Explain workflow context as orchestration situating | Claim the Workflow Engine or Recommendation Engine created tips |
| Reference conflict disposition already decided | Re-resolve conflicts or invent unpublished winners |
| Preserve and narrate constitutional evidence references | Reinterpret Evidence or mint mastery from set clarity |

If a proposed narration would require inventing tips, altering ownership, redefining meaning, re-resolving conflicts, or publishing undeclared rules, **amend the owning constitutional corpora first** — or refuse the narration. Explainability never gains authority by storytelling.

## Distinction from sibling corpora

| Corpus | Answers | Does not answer |
|--------|---------|-----------------|
| **WS3 / MS001 Educational Recommendation Model** | What a single constitutional tip *is* | How the *set* is explained as an organised package (this corpus) |
| **WS3 / MS001 `RECOMMENDATION_EXPLAINABILITY.md`** | Why *each tip* exists and is valid (ERQ-01…ERQ-05) | Full set-level explanation model spanning assembly and interpretation (this corpus) |
| **WS3 / MS002 Recommendation Assembly Framework** | How lawful tips are *organised* into a set | Unified explanation contract for set existence / assembly / interpretation (this corpus) |
| **WS3 / MS002 `ASSEMBLY_EXPLAINABILITY.md`** | Set-organisation speech themes (RAQ-01…RAQ-04) | Full principles / components / boundaries / pattern catalogue (this corpus specialises and binds) |
| **WS2 / MS003 Authority Decision Explainability** | Why a component was *permitted* to decide | Why recommendations *appear together* as a set (this corpus) |
| **WS1 Workflow / Transition / Completion explainability** | Why flow started, moved, or completed | Why a *recommendation set* exists and how to interpret its members (this corpus) |
| **Programme VI `*_EXPLAINABILITY.md`** | Why *this educational answer* emerged | Why *this packaging* is the live set (this corpus) |
| **This Recommendation Set Explainability** | Why the set exists / how assembled / how to interpret / what constitutional facts speech must carry | Algorithms, Runtime A, UI rendering, tip invention, ownership maps, meaning rewrites |

**Binding distinction:** MS001 owns the single-recommendation artefact. MS002 owns set organisation law. MS003 owns the **constitutional explanation contract** for assembled recommendation sets — without amending artefact law or assembly catalogues.

## Out of scope (MS003)

- Runtime A integration, feature flags, or services
- Rendering engines, UI components, navigation, templates, or notifications
- Explanation algorithms, ranking, scoring, or natural-language generation systems
- Database models, schemas, or ORM entities
- Analytics pipelines or telemetry schemas
- Serialisation formats or API contracts
- Amendments to Programme VI educational meaning
- Amendments to Authority Model domains, Conflict Resolution outcomes, or Assembly components by explanation fiat
- Workflow execution engines, sagas, job queues, or state machines in code
- Creating, ranking, or scoring recommendations

## How to use this corpus

1. Read `RECOMMENDATION_SET_EXPLAINABILITY.md` first.
2. Treat principles in `EXPLANATION_PRINCIPLES.md` as binding for every recommendation-set narration path.
3. Require the information set in `EXPLANATION_COMPONENTS.md` before student- or developer-facing set speech.
4. Enforce limits in `EXPLANATION_BOUNDARIES.md` — refuse narration that invents tips, ownership, meaning, or unpublished rules.
5. Use `EXPLANATION_EXAMPLES.md` as illustrative patterns, not as a closed catalogue of product copy.
6. For each constituent tip, also satisfy [`../recommendations/RECOMMENDATION_EXPLAINABILITY.md`](../recommendations/RECOMMENDATION_EXPLAINABILITY.md).
7. When set organisation is at stake, consult [`../recommendation_assembly/`](../recommendation_assembly/) — explain what that Framework already authorises.
8. When ownership or conflict disposition is at stake, consult [`../authority/`](../authority/), [`../conflict_resolution/`](../conflict_resolution/), and [`../authority_explainability/`](../authority_explainability/).
9. When educational meaning is at stake, defer to Programme VI explainability — this corpus frames *set packaging*, not *what the tutor meant*.
10. Do not implement behaviours that contradict this corpus without amending it first.
