# EP-008.1 — UI Specification

**Programme:** EP-008.1 — Recommendation Trust  
**Date:** 2026-07-26  
**Status:** Presentation contract for sole-runtime student surfaces  
**Canonical shell:** Student Home (`app/templates/student/home.html`) + Coach panel  
**Design system:** Preserve existing student CSS classes; no new visual language / purple-glow theatre  
**Authority:** Pass-through of authored MES only

---

## 1. Design principles (UI)

1. **One primary tip** — single recommendation hero + one Start Session CTA (DR-050).  
2. **One composition** — first viewport answers what / why / why now / benefit / next.  
3. **Progressive disclosure** — evidence, confidence, alternatives, review in one `<details>` (or equivalent).  
4. **Honesty over polish** — refusal state must look deliberately incomplete, not “loading tip…”.  
5. **No cards for decoration** — use existing `student-*` patterns; add structure only when it aids interaction (disclosure, Start Session).  
6. **Educational language only** — no Twin / pipeline / warrant / enum leakage.

---

## 2. Information architecture — Home hero (schema-complete)

### 2.1 First viewport (Level 1)

| Order | Block | Content | Data attribute |
|---|---|---|---|
| 1 | Title | Mission-aligned recommendation title | `data-mes-field="title"` |
| 2 | Duration / meta | Existing minutes row | existing |
| 3 | Why it exists | `why_recommended` | `data-mes-field="why_recommended"` `data-mes-level="1"` |
| 4 | Why it matters now | `timeliness_line` | `data-mes-field="timeliness"` `data-mes-level="1"` |
| 5 | Expected improvement | Short `expected_benefit` | `data-mes-field="expected_benefit"` `data-mes-level="1"` |
| 6 | Next | `suggested_next_action` | `data-mes-field="suggested_next_action"` `data-mes-level="1"` |
| 7 | Plan relationship | Coherence badge / one line | `data-mes-field="plan_coherence"` `data-mes-level="1"` |
| 8 | Primary CTA | Start Session (enabled when lawful) | existing |

**L1 length budget:** Primary explanation cluster (items 3–6) should remain skimmable; prefer ≤ ~40 words for the combined why+now+next core where authored text allows. Benefit may be a separate short sentence.

### 2.2 Plan coherence presentation

| Authored state | UI |
|---|---|
| Aligned with Today’s Mission | Quiet affirmative line, e.g. authored `plan_coherence_label` (“Supports today’s mission”) |
| Advisory divergence | Visible label that this is **advice** relative to the mission — never silent conflict |
| Missing label | Omit block — do not invent |

### 2.3 Level 2 disclosure (“Why this tip?”)

Reuse / extend `explanation_card`:

| Block | Field |
|---|---|
| Evidence bullets | `evidence_points` / `supporting_evidence` |
| Confidence | `confidence_label` + `confidence_basis` |
| Full expected benefit | if truncated at L1 |
| Review point | `review_point` (completion → future tips) |
| Alternatives | up to 2: title + why (+ optional benefit) |
| EIP-003 split | Optional: observed / estimates / advice if already on projection — do not require for EP-008.1 if Home card already covers evidence |

**Alternatives rules:**

- Header: “Other options considered” (or authored equivalent).  
- Not selectable re-rank controls — informational agency only (accept UI = EP-008.3).  
- Each alternative: title + one why line; no nested heavy cards unless Revision pattern reused lightly.

---

## 3. Honest refusal variant

When `honest_refusal` / `trust_state=refusal`:

| Element | Behaviour |
|---|---|
| Title | Authored refusal title (e.g. “No recommendation yet”) |
| Why | Authored thin-evidence why |
| Why now | Optional: “We need a little practice first” only if authored / composed without false precision |
| Benefit | Hide or show humble “Build evidence for a better tip” if authored |
| Next | Authored next toward mission / calibration |
| Coherence badge | Hide unless authored for refusal path |
| Alternatives | **Hidden** |
| Confidence | “Cannot yet be estimated” (authored) |
| CTA | Start Session / continue mission if available — restorative, not shame |

---

## 4. Coach panel

Replace opaque single-paragraph compression when schema-complete:

```
Coach insight
  • Why: {why_recommended}
  • Why now: {timeliness_line}
  • Next: {suggested_next_action}
  • Benefit: {expected_benefit}   # omit if empty
```

Rules:

- Same strings as Home — no second narration.  
- May remain visually secondary to the hero.  
- On refusal: show humility copy, not motivational theatre.  
- Do not clip away the only copy of why/next (EP-006.2 clip policy preserved).

---

## 5. Readiness relationship (Home)

Keep existing readiness panel (EP-006.4).

Optional **one** bridge sentence under tip benefit when data exists:

- Example pattern (authored numbers only): “Expected readiness change from tonight’s focus: {label}.”  
- Never “You will become Exam Ready.”  
- If readiness MES incomplete, omit bridge sentence.

---

## 6. Mission surface

| Element | Spec |
|---|---|
| Mission hero | Existing planning MES (next, drivers, review) |
| Trust add | If recommendation label ≠ mission topic, show coherence / advice label from authored fields |
| CTA | Unchanged mission start/continue |

Do not duplicate full Home alternatives list on Mission unless space already exists — prefer Home as trust HQ.

---

## 7. Revision surface

| Element | Spec |
|---|---|
| Primary | Existing primary + `explanation_card` |
| Alternatives | For each option, show why + expected benefit (compact); prefer explanation_card pattern over title-only rows |

---

## 8. Completion / outcome feedback

| Surface | Spec |
|---|---|
| Session outcome | Echo `review_point` when available |
| Fallback (no review_point) | Honest static line: practice updates what we suggest next — **no claim of personal model** |
| Return to Home | Tip regenerates via Runtime A as today; no client-side “you accepted” state until EP-008.3 |

---

## 9. Accessibility & telemetry

| Concern | Spec |
|---|---|
| Disclosure | Native `<details>`/`<summary>` or existing a11y pattern |
| Contrast | Existing student tokens |
| Telemetry | Keep `provenance_expanded` on disclosure open; **no** accept/dismiss events in this programme |
| `data-mes-*` | Required on new bindings for contract tests |

---

## 10. Wireframe (text)

### Schema-complete

```
┌─────────────────────────────────────────────┐
│  Tonight: {title}              {minutes}    │
│  Why: {why_recommended}                     │
│  Why now: {timeliness_line}                 │
│  You’ll work toward: {expected_benefit}     │
│  Next: {suggested_next_action}              │
│  {plan_coherence_label}                     │
│           [ Start Session ]                 │
│  ▸ Why this tip? (evidence, confidence,     │
│      review, other options)                 │
├─────────────────────────────────────────────┤
│  Readiness … (existing panel)               │
├─────────────────────────────────────────────┤
│  Coach: Why / Why now / Next / Benefit      │
└─────────────────────────────────────────────┘
```

### Refusal

```
┌─────────────────────────────────────────────┐
│  {refusal title}                            │
│  Why: {why}                                 │
│  Confidence: Cannot yet be estimated        │
│  Next: {next toward mission}                │
│           [ Start Session ]                 │
└─────────────────────────────────────────────┘
```

---

## 11. Copy anti-patterns (forbidden)

- “AI recommends…” / “Our model is highly confident…” without authored confidence  
- Guaranteed exam outcomes  
- Streak shame on refusal  
- Fake alternatives when refusal  
- Re-ordered tip list presented as “you chose #2” without EP-008.3  
- Internal codes (`plan_coherence=ALIGNED` raw enums)

---

## 12. Dogfood checklist (manual)

- [ ] Schema-complete user sees why, why now, benefit, next, coherence in first viewport  
- [ ] Disclosure shows evidence, confidence, review, ≤2 alternatives  
- [ ] Refusal user sees humble state; no alternatives; CTA restorative  
- [ ] Coach matches Home strings  
- [ ] Completing a session surfaces review / loop honesty  
- [ ] No internal terminology leaked  
- [ ] Single primary CTA  

---

**End of UI_SPECIFICATION**
