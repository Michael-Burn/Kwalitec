# Vision

**Status:** Active  
**Owner:** Product / Architecture Office  

## Purpose

This folder holds the **Executive Product Constitution** — the permanent statement of why Kwalitec exists and how product excellence is judged through 2030.

## Hierarchy

```
PRODUCT_VISION_2030.md     ← highest product-philosophy authority
        ↓ constrains
PRODUCT_BLUEPRINT.md       ← product strategy, model, roadmap (repo root)
        ↓ constrains
Educational Constitution   ← educational law (knowledge/educational/)
        ↓ constrains
Architecture / ADRs        ← structural decisions
        ↓ constrains
PRDs / features            ← delivery artefacts
```

Full decision hierarchy: [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md).

## Contents

| Document | Role |
|---|---|
| [`PRODUCT_VISION_2030.md`](PRODUCT_VISION_2030.md) | Executive Product Constitution — why, north star, philosophies, never-build list, final test |

## Relationship with Product Blueprint

| | Vision 2030 | Product Blueprint |
|---|---|---|
| **Answers** | Why we exist; what success means; what we refuse | How we operate; who we serve; what we ship next |
| **Owns** | Philosophy, north star, design/experience/AI principles | Audiences, educational model pillars, Digital Twin role, roadmap, product promise |
| **Does not own** | Release dates, epic backlogs, API shapes | Restated philosophy that would duplicate Vision |

If Vision and Blueprint appear to conflict: **Vision wins on philosophy**; amend Blueprint to align. If educational law conflicts with either: stop and amend via the Educational Constitution process (EGI).

## When to use each document

| Situation | Use |
|---|---|
| “Should we build this at all?” | Vision 2030 — Final Test + Never Build |
| “Does this improve pass probability / learning?” | Vision 2030 — North Star + Product Philosophy |
| “Who is this for and how does it fit the model?” | Product Blueprint |
| “Is this on the current roadmap?” | Product Blueprint — Product Roadmap |
| “Is this educationally lawful?” | Educational Constitution |
| “Where does this live in the codebase?” | `ARCHITECTURE.md` / ADRs |
| “How do we write a feature proposal?” | `knowledge/prd/` + Vision alignment section |

## Rules

1. Do not duplicate Vision philosophy into Blueprint, ADRs, or PRDs — **link** instead.
2. Do not invent a second north star. Trust and next-action language are expressions of the single north star (pass probability through better learning decisions).
3. Update Vision only through deliberate product strategy discussion (see Governance review process).
