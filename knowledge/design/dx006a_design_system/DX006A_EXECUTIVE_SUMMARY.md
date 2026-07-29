# DX-006A Executive Summary

**Programme:** DX-006A — Design System Implementation (Foundation First)  
**Status:** Complete (foundation architecture)  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01` (Alpha Candidate 1)  
**Implementation:** Foundation specification only — no page redesign; no surface migration  

---

## Verdict

DX-006A defines the **complete Kwalitec Design System** that Founder and Student surfaces will compose. Pages do not invent components. Components compose tokens. Tokens define the visual language. Hierarchy is binding: **L0 Tokens → L1 Primitives → L2 Layout → L3 Operational**. Premium certification target **≥9/10 on all dimensions** — **PASS**.

This programme builds the foundation. It does **not** redesign pages. Page migration is **DX-006B**.

---

## Design target

```
Tokens → Primitives → Layout → Operational → Pages (DX-006B)
```

Every component must answer: **Why does this exist?** If no clear answer exists, the component is removed.

---

## Authorities (non-negotiable)

| Authority | Binding role |
|---|---|
| **DX-001** | Visual language, tokens, one Primary, card/KPI policy, premium gate |
| **DX-002** | Screen purpose, surface types, navigation trees |
| **DX-003** | Decision → Action → Feedback, terminology, empty/status/error copy |
| **DX-004** | Founder OS — Home, Subjects, Workspace operational components |
| **DX-005** | Student OS — Home, Choose Exam, Study Session operational components |
| **Brand Guidelines** | Mark, HEX ownership, Inter, gold reserved |

No component may contradict these authorities. On conflict: surface structure from DX-004/005; tokens from DX-001; copy from DX-003; surface type from DX-002.

---

## Primary rules (enforced by Guardian)

- Exactly **one Primary** button per page  
- Exactly **one H1**  
- **No** decorative KPI cards  
- **No** decorative icons  
- **No** duplicate navigation  
- **No** orphan components  
- **No** hard-coded colours or spacing outside tokens  

---

## Hierarchy delivered

| Level | Scope |
|---|---|
| **L0** | Design tokens — colour, type, space, elevation, radius, motion, breakpoints, z-index, opacity, transitions |
| **L1** | Primitive components — Button, Input, Dialog, Toast, Empty/Loading/Error State, … |
| **L2** | Layout components — Page, Section, Container, Grid, Stack, Sidebar, Table, Card (justified only) |
| **L3** | Operational components — Persistent Context Header, Mission Card, Stage Indicator, Blocking Findings, … |

---

## Explicit rejections

Components without a clear product reason are **out of the foundation**, including legacy V3 contracts that encode dashboard theatre:

- `StatisticTile` / vanity KPI tiles  
- `ProgressRing` as Home/Console chrome  
- Decorative `Chip` / `Tag` proliferation  
- `RecommendationCard` as a peer that competes with Mission / Current Work  
- Page-specific one-off widgets in the shared foundation  

Full register: `COMPONENT_CATALOGUE.md` § Rejected.

---

## Token reconciliation

DX-001 **supersedes** UX-001 for redesign work:

| Concern | Canonical (DX-006A) |
|---|---|
| Type | Display 32 · Page 24 · Section 18 · Body 16 · Support 14 · Caption 12 |
| Spacing | 4 · 8 · 16 · 24 · 32 · 48 · 64 (product UI; 12 / 96 / 128 retired) |
| Colour | Semantic roles only; Brand HEX ownership unchanged |
| CSS source | `app/static/css/tokens.css` remapped to DX-001 names in Phase 1 of implementation |
| Python source | `src/presentation/design_system/` remapped to match |

Legacy aliases may remain temporarily for unmigrated pages; new work **must** use DX-001 tokens.

---

## Non-goals

- No Founder / Student page redesign (DX-006B)  
- No Study Session / Home / Subjects / Workspace UI execution in this programme  
- No new educational or planning logic  
- No inventing decorative themes  

---

## Exit

DX-006A is complete. The project may proceed to **DX-006B — Founder & Student Surface Migration** only after Guardian rules and this catalogue are treated as binding for all UI work.

---

*Release Candidate: RC-2026.07.29-01*
