# Premium Design Checklist

**Programme:** DX-001  
**Status:** Binding gate for future UI / redesign work  

---

## Rule

Every future screen must be scored on each dimension below from **1–10**.

**Anything below 9/10 on any dimension must be redesigned before ship.**

Record scores in the programme’s review or completion artefacts. Do not average away a failing dimension.

---

## Scorecard

| # | Dimension | 9–10 means | Common failure (≤8) |
|---:|---|---|---|
| 1 | **Visual Hierarchy** | Next action and importance are obvious within 3 seconds | Competing heroes; equal-weight panels |
| 2 | **Typography** | Body dominates; Page Heading restrained; scale followed | Oversized titles; stacked duplicate headings |
| 3 | **Spacing** | 4–64 scale; hierarchy via gaps | Arbitrary padding; cramped or randomly sparse |
| 4 | **Information Density** | Dense where useful (tables); never cluttered | KPI grids; card walls; L3 leakage |
| 5 | **Professional Tone** | Respects expert users; calm precise copy | Tutorial voice; cheerleading; condescension |
| 6 | **Minimalism** | Every element earns its place | Decorative cards; filler widgets |
| 7 | **Accessibility** | Contrast, focus, labels, keyboard | Icon-only critical actions; low contrast |
| 8 | **Consistency** | Reuses system patterns and tokens | One-off components; mixed icon sets |
| 9 | **Task Focus** | Answers the screen’s one question | Multi-purpose dashboard mashup |
| 10 | **Premium Feel** | Quiet confidence; Linear/Stripe/Apple restraint | Enterprise colourful; shadow/chrome theatre |

---

## Scoring guidance

| Score | Meaning |
|---:|---|
| 10 | Exemplary; reference quality for the product |
| 9 | Ships; minor polish only |
| 8 | Noticeable defect — **must redesign** |
| 5–7 | Clear hierarchy/content failure |
| 1–4 | Wrong product language; reject |

---

## Mandatory checks (pass/fail alongside scores)

Before scoring, confirm:

- [ ] One Primary action (or justified none for pure read-only detail)  
- [ ] KPI policy respected (no vanity metrics)  
- [ ] Cards only for justified grouping  
- [ ] Empty state = why + next action only  
- [ ] Lucide only; Inter only  
- [ ] Semantic colour only; Gold not used as UI chrome  
- [ ] No implementation leakage in primary UI  
- [ ] Motion ≤250ms and purposeful  

Any unchecked item caps **Consistency** and **Premium Feel** at ≤8 (fail).

---

## Template

```text
Screen: ____________________
Reviewer: __________________
Date: ______________________

Visual Hierarchy:     _/10
Typography:           _/10
Spacing:              _/10
Information Density:  _/10
Professional Tone:    _/10
Minimalism:           _/10
Accessibility:        _/10
Consistency:          _/10
Task Focus:           _/10
Premium Feel:         _/10

Mandatory checks: PASS / FAIL
Verdict: SHIP (≥9 all) / REDESIGN
Notes:
```

---

## Authority

This checklist is the permanent quality gate for Design Excellence programmes (DX-002+). UX-001 / UI Guardian workflows must incorporate these scores when redesign programmes begin.
