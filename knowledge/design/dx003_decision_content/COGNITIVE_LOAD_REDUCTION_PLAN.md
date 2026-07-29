# Cognitive Load Reduction Plan

**Programme:** DX-003  
**Status:** Binding execution plan for DX-004+  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** DX-001, DX-002, this corpus  

---

## Objective

Reduce unnecessary cognitive load by removing words, decisions, and statuses that do not serve Decision → Action → Feedback — without removing educational explainability or publication safety.

---

## Principles of reduction

1. **Delete before rewrite** — silence beats paraphrase.  
2. **One decision** — sequence stages; do not parallelise.  
3. **Labels replace paragraphs** — if copy teaches the control, fix the control in a later visual DX; still delete the paragraph now when implementing copy.  
4. **Statuses earn their place** — actionable or gone.  
5. **IA first where DX-002 already decided** — hub merge and Overview reshape unlock content cuts.

---

## Workstreams

### W1 — Founder content (DX-004 primary)

| Step | Action | Artefacts |
|---|---|---|
| 1 | Apply Decision Architecture sentences to Overview, Subjects, Studio, Workspace | `DECISION_ARCHITECTURE.md` |
| 2 | Execute inventory Delete/Merge on Workspace + hubs + Overview | `CONTENT_INVENTORY.md` |
| 3 | Shorten `recover_flash` / `FLASH_*` to Problem → Reason → Action | `SUCCESS_ERROR_COPY_GUIDE.md` |
| 4 | Collapse status chrome per Status System | `STATUS_SYSTEM.md` |
| 5 | Enforce terminology (Publish, Subject, Ready, Overview, Students) | `TERMINOLOGY_DICTIONARY.md` |
| 6 | Empty states → Reason + Next Action only | `EMPTY_STATE_STANDARDS.md` |

**Out of scope for W1:** CSS token remaps, new component library, student Home full rewrite (may take quiet wins only).

### W2 — Student content (post–DX-004 or parallel student DX)

| Step | Action |
|---|---|
| 1 | Home: one Mission Decision; one why; overflow secondaries |
| 2 | History: delete epistemology; archive-only |
| 3 | Help: delete ontology essays; keep search/contact |
| 4 | Remove Welcome modal |
| 5 | Login: ≤ one value sentence |
| 6 | Align `product_language.py` long constants — remove from templates |

### W3 — Guardian / authority updates

| Step | Action |
|---|---|
| 1 | Update `UI_GUARDIAN.md` to require DX-001 + DX-002 one-question + DX-003 Decision → Action → Feedback and terminology checks |
| 2 | Note ARP-004 / Product Language Guide superseded on tone density by DX-003 |
| 3 | Keep Brand Guidelines ownership of mark/HEX |

---

## Phased reduction targets

| Phase | Programme | Surfaces | Word Δ | Decision Δ | Status Δ |
|---|---|---|---|---|---|
| A | DX-004 | Overview, Subjects, Studio, Workspace, operator flashes | ~50–60% on those surfaces | → ≤1–3 | ~50% |
| B | Student content DX | Home, History, Help, Login, Welcome | ~45–55% | → 1 | ~40% |
| C | Polish DX | Session/wizard lean copy; secondary reports demotion labels | ~10–20% residual | Hold ≤3 | Hold |

**Cumulative primary-path target after A+B:** ~50% words, ~60–70% decisions, ~40–50% status messages.

---

## Screen-level playbooks (P0)

### Curriculum Workspace

```
Keep: subject, next step (1 line), stage Primary, blockers
Delete: upload anxiety paragraph, filler “ready for review”, Documents meta-tab,
        workflow tutorial card, L0 diagnostics
Merge: readiness KPIs → gate state; tabs → stage panels; Actions → Primary + overflow
Feedback: Published / Approved / Validation passed (short)
```

### Console Overview

```
Keep: top attention item + Primary + short list
Delete: platform summary, pulse essay, L0 build/timezone
Merge: Quick Actions into the one Primary
```

### Studio / Subjects

```
Keep: list + Create / Open
Delete: Curriculum workflow essay; peer hub pages; stray Studio jump CTA
```

### Student Home (later)

```
Keep: Mission title, Primary, duration, one why
Delete: welcome/greeting, trust badges, congratulations
Merge: why stack → disclosure; secondary CTAs → menu
```

---

## Measurement (definition of done per screen)

A screen is content-complete when:

1. One sentence summarises it (≤ one line).  
2. Decision density ≤ 3 (target 1).  
3. Reading flow is linear (no backwards loop).  
4. Inventory items for that screen are Keep/Rewrite only (no open Delete).  
5. Status set matches `STATUS_SYSTEM.md`.  
6. Empty/success/error copy matches guides.  
7. Terminology dictionary enforced (spot-check synonyms).

---

## Risks & guards

| Risk | Guard |
|---|---|
| Cutting educational why on Home | Keep exactly one why; disclose rest |
| Operators lose gate context | Keep Blocking findings + short recovery |
| Over-short errors lose actionability | Require Action beat always |
| Implementing layout in “content” PR | DX-003 forbids CSS/layout — copy and structure flags only until visual DX |

---

## Recommendations for DX-004

See completion report. Summary: Founder Experience Redesign executes W1 using this plan; no student-wide visual redesign in DX-004 unless explicitly scoped; still no CSS token remap until content cuts land on P0 Founder surfaces.
