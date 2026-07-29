# Product Design Manifesto

**Programme:** DX-001 — Premium Design System & Product Design Manifesto  
**Status:** Permanent design authority  
**Audience:** Founders, product, engineering, and any agent implementing or reviewing UI  
**Effective:** 2026-07-29  

---

## Purpose

Kwalitec has reached **Alpha Candidate 1**. Engineering governance is mature. The next phase is **Design Excellence**.

This manifesto defines the visual language and interaction philosophy that every future screen must follow. It is the single source of truth for product design intent.

**No screen redesign is permitted until this programme’s corpus is complete and adopted.** Implementation of redesigns belongs to later DX programmes (DX-002 onwards).

---

## Who we design for

Primary users are highly educated professionals:

- Actuaries  
- Finance professionals  
- Consultants  
- Engineers  
- University students preparing for professional qualifications  

Assume intelligence. Never design as if teaching basic computer literacy. Prefer clarity and restraint over tutorial theatre.

---

## What “premium” means here

Premium is not decoration. Premium is:

- Immediate clarity about the next action  
- Calm hierarchy without visual noise  
- Respect for scarce attention  
- Consistency that builds trust across Founder Console, Curriculum Studio, and Student OS  

Reference *principles* (not copies) of:

| Reference | What we take |
|---|---|
| Apple | Restraint; typography and space over chrome |
| Linear | Efficiency; dense when useful, never cluttered |
| Notion | Organisation; progressive disclosure |
| Stripe | Professional calm; tables and precise copy |
| Raycast | Focus; one job, fast path to action |

We intentionally avoid:

- Colourful enterprise dashboards  
- Card overload and KPI grids  
- Tutorial-style interfaces  
- Unnecessary explanations  
- Metrics that do not change decisions  

---

## Product thesis in design terms

Kwalitec’s product thesis is: **Reduce decisions. Increase learning.**

Design must serve that thesis:

| Surface | One question the screen answers |
|---|---|
| Founder Console | What should I work on next? |
| Student Dashboard / Home | What should I study next? |
| Subject / Curriculum Workspace | What is the next publication task? |
| Session | What do I do in this sitting? |

If a screen cannot answer its one question in under three seconds, it fails.

---

## Authority and relationship to existing design docs

| Document | Role after DX-001 |
|---|---|
| **This corpus (`dx001_design_system/`)** | **Permanent product design language** for future UI work and redesign programmes |
| `BRAND_GUIDELINES.md` | Brand mark, lockups, brand colour HEX — unchanged |
| `UI_UX_IMPLEMENTATION_STANDARD.md` (UX-001) | Historical implementation standard; **where conflict exists, DX-001 wins for redesigns** |
| `UI_GUARDIAN.md` | Enforcement workflow; must consult DX-001 corpus before UI changes once redesign programmes begin |

Brand colours and logo rules remain owned by Brand Guidelines. Semantic UI roles, hierarchy policy, KPI policy, card policy, and premium scoring are owned by DX-001.

---

## Non-negotiables

1. **Minimal by default** — everything earns its place.  
2. **Professional first** — labels over paragraphs; never over-explain.  
3. **Action over analytics** — dashboards decide next work, not decorate statistics.  
4. **One screen, one purpose.**  
5. **Whitespace is a feature.**  
6. **Hierarchy before decoration** — type and space, not colour and shadow.  
7. **Progressive disclosure** — hide complexity until requested.  
8. **Consistency beats creativity** — reuse patterns; invent components only when necessary.  

---

## What DX-001 does not do

- No template, CSS, or component implementation  
- No screen redesigns  
- No new product features  
- No brand mark redesign  

DX-001 establishes law. Later programmes execute against it.

---

## How to use this corpus

Before any future UI change:

1. Read this manifesto.  
2. Apply `DESIGN_PRINCIPLES.md` and the relevant system docs (type, space, colour, components, content).  
3. Score the screen with `PREMIUM_DESIGN_CHECKLIST.md`.  
4. Anything below **9/10** on any dimension must be redesigned before ship.  

Next programme after exit criteria: **DX-002 — Product Information Architecture Review.**
