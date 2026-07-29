# DX-003 Executive Summary

**Programme:** DX-003 — Decision & Content Architecture  
**Status:** Complete  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** None (documentation-only; no CSS, layouts, or route changes)

---

## Verdict

Kwalitec’s product language still reads like orientation software: tutorial paragraphs, duplicate statuses, synonym drift, and multi-decision screens. DX-003 defines the content architecture that turns every screen into a **Decision → Action → Feedback** surface — professional software for highly educated users.

---

## What this programme establishes

| Pillar | Binding artefact |
|---|---|
| Decision model for every primary screen | `DECISION_ARCHITECTURE.md` |
| Visual reading sequence | `READING_FLOW.md` |
| Word-level keep / rewrite / merge / delete | `CONTENT_INVENTORY.md` |
| Density & reduction targets | `CONTENT_REDUCTION_REPORT.md`, `DECISION_DENSITY_AUDIT.md` |
| One name per concept | `TERMINOLOGY_DICTIONARY.md` |
| Actionable status system | `STATUS_SYSTEM.md` |
| Empty / success / error / voice standards | `EMPTY_STATE_STANDARDS.md`, `SUCCESS_ERROR_COPY_GUIDE.md`, `CONTENT_STYLE_GUIDE.md` |
| Execution plan for DX-004+ | `COGNITIVE_LOAD_REDUCTION_PLAN.md` |

---

## Core philosophy (binding)

The interface should read like **professional software**.

Not educational software. Not onboarding software. Not marketing. Not documentation.

Assume users are intelligent. Explain only what cannot be inferred.

**Decision before description. Labels before paragraphs. Silence is acceptable.**

Every screen has **one sentence**. If that sentence wraps, the screen contains too much.

---

## Estimated impact (when executed in DX-004+)

| Metric | Current (primary paths) | Target | Reduction |
|---|---|---|---|
| Visible words (P0 screens) | ~4,800–5,500 | ~2,200–2,600 | **~50–55%** |
| Independent decisions per screen | Often 4–9 | 1 (max 3) | **~60–70%** |
| Permanent status / badge chrome | High duplication | Actionable only | **~40–50%** of status messages |

Highest-impact removals: Curriculum Workspace tutorial + readiness KPI essays; Studio hub “Curriculum workflow” repeats; History epistemology paragraph; Home multi-why stack; Console Overview KPI labelling; Welcome modal; verbose operator flash essays.

---

## Authority chain

```
DX-001  Design system (visual / component law)
DX-002  Information architecture (one question / nav trees)
DX-003  Decision & content architecture (what words deserve to exist)  ← this programme
DX-004  Founder Experience Redesign (first implementation programme)
```

On copy conflicts for redesigns: **DX-003 wins** over ARP-004 / `PRODUCT_LANGUAGE_GUIDE.md` tone where DX-003 is stricter (quiet, non-encouraging, shorter flashes). Canonical nouns remain aligned with `TERMINOLOGY_DICTIONARY.md` (extends lexicon; does not invent parallel vocabularies).

---

## Non-goals

- No layout redesign  
- No CSS / token remaps  
- No component redesign  
- No route or nav implementation  
- No algorithm changes  

Architecture only. DX-004 executes Founder surfaces first.

---

## Exit

All exit criteria in `DX003_COMPLETION_REPORT.md` are met. The project may proceed to **DX-004 — Founder Experience Redesign**.
