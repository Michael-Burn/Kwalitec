# EP-008.3 — UI Specification

**Programme:** EP-008.3 — Recommendation Commitment & Follow-through  
**Date:** 2026-07-26  
**Status:** Presentation contract for commitment / defer / reflection / history  
**Canonical shell:** Student Home + Mission / unified journey + session outcome + History  
**Design system:** Preserve existing student CSS; no new visual language, purple-glow, or gamification chrome  
**Authority:** Pass-through of authored MES + preference/intent commitment state  

---

## 1. Design principles (UI)

1. **Educational commitment, not AI acceptance** — label is “I’m doing this next.”  
2. **One primary educational CTA** — Start Session remains primary (DR-050); commitment must not create a competing equal-weight “do this now.”  
3. **Honesty over conversion** — defer is calm, first-class, and unpunished.  
4. **Trust Contract stays** — T1–T11 speech remains; commitment sits *after* understanding.  
5. **One composition** — first viewport still answers what / why / why now / benefit / next; commitment is the agency step.  
6. **No streaks, badges, points, or shame** — never “you broke your streak by deferring.”  
7. **Educational language only** — no Twin / pipeline / warrant / enum leakage.  
8. **Plan continuity** — every commit / defer / reflection reinforces one continuous study plan.

---

## 2. Home — schema-complete (commitment offered)

### 2.1 First viewport (Level 1) — unchanged trust order + agency

Retain EP-008.1 order (title, duration, why, why now, benefit, next, coherence), then:

| Order | Block | Content | Data attribute |
|---|---|---|---|
| … | Trust L1 | Existing T1–T9 | existing `data-mes-*` |
| 9 | Commitment confirm | “I’m doing this next.” | `data-commitment="confirm"` |
| 10 | Primary CTA | **Start Session** (enabled when lawful) | existing |
| 11 | Defer entry | Text link: “Not today” / “I can’t do this now” | `data-commitment="defer-open"` |

**Preferred interaction patterns (pick one in delivery; document choice):**

| Pattern | Behaviour |
|---|---|
| **A — Combined** | Start Session POST also records commitment (single button; confirm copy in helper text: “Starting means you’re doing this next.”) |
| **B — Explicit then start** | Lightweight “I’m doing this next.” sets C1; Start Session remains primary and enabled after or alongside |

Pattern A minimises cognitive load; Pattern B maximises conscious agency. **Validation watches cognitive-load themes either way.**

### 2.2 Level 2 disclosure

Keep Trust L2 (evidence, confidence, review, ≤2 alternatives).  
Add optional short line: “Your recent study choices” link to History narrative — not a second tip list.

### 2.3 Committed chrome (C1 / C2)

When `state=committed` or `in_session`:

```
Committed for today: {title}
{plan_continuity_line}
[ Continue Session ]   # or Start Session if not started
```

- Quiet affirmative — no confetti.  
- Defer still available until session completes (optional; if deferred after commit, treat as restorative cancel without shame).

---

## 3. Deferred commitment UI

### 3.1 Defer panel (disclosure or modal-lite)

Trigger: “Not today” / “I can’t do this now.”

| Element | Spec |
|---|---|
| Title | “What’s getting in the way?” |
| Options | Radio list from catalogue (Design §6.3) |
| Optional note | Free text ≤140 chars when `other` |
| Primary action | “Save and continue” |
| Cancel | Dismiss panel; tip unchanged |
| After save | Calm ack + continuity line; tip may remain visible as advice |

**Forbidden copy:**

- “This will hurt your readiness.”  
- “Top students never skip.”  
- Streak / points loss language.  
- Fake substitute tip invented in the client.

### 3.2 Post-defer Home

| Element | Behaviour |
|---|---|
| Trust speech | Remains available (advice still inspectable) |
| Commitment CTA | Hidden or replaced with “Change your mind?” (optional restore to C0) |
| Continuity | “Your study plan continues — we’ll meet you when you’re ready.” |
| Start Session | Still available if student chooses mission work anyway — commitment is intent, not a lock |

---

## 4. Honest refusal nights

When `trust_state=refusal` / `honest_refusal`:

| Element | Behaviour |
|---|---|
| Commitment CTA | **Hidden** |
| Defer panel | **Hidden** (nothing to defer) |
| Start Session | Restorative, as EP-008.1 |
| Copy | No “commit to learning” theatre |

---

## 5. Coach panel

- Keep structured trust summary (why / now / next / benefit).  
- **Do not** add a second Commit button in Coach.  
- Optional one-line status: “Committed for today” when C1+ — secondary muted text only.

---

## 6. Mission / unified journey

| Element | Spec |
|---|---|
| Mission hero | Existing planning MES |
| Commitment echo | If committed, show “Today’s commitment: {title}” + continuity |
| CTA | Unchanged start/continue |
| Coherence | Existing advice label when tip ≠ mission topic |

Do not duplicate full defer catalogue on Mission unless Home is unavailable — Home remains commitment HQ.

---

## 7. Completion reflection

### 7.1 Placement

Session outcome screen and/or Home reflection branch after completion (existing `reflection_active` patterns).

### 7.2 Layout (brief — one screen)

```
┌─────────────────────────────────────────────┐
│  Session complete                           │
│  What you did: {what_you_did}               │
│  What changed: {what_changed}               │
│  Why it mattered: {why_it_mattered}         │
│  What we updated: {what_was_learned}        │  ← humble frame
│  What happens next: {what_happens_next}     │
│  {plan_continuity_line}                     │
│           [ Got it ]                        │
└─────────────────────────────────────────────┘
```

Rules:

- Prefer authored `review_point` / `expected_benefit` / mission completion labels.  
- “What we updated” must **not** claim a personal AI model. Prefer: “Tonight’s practice updates the educational state that shapes tomorrow’s tip.”  
- One primary ack CTA.  
- No share/streak celebration.

---

## 8. Recommendation history (educational narrative)

### 8.1 Surface

Student History page (extend existing) — section title: **“Recent study choices”** (or equivalent).

### 8.2 Entry cards (not audit rows)

| Kind | Presentation |
|---|---|
| Completed | “Completed · {title} · {date} · {why it mattered short}” |
| Deferred | “Deferred · {title} · {reason label} · plan continues” |
| Committed incomplete | “Committed · not finished · {title}” — restorative tone |

Rules:

- Cap ≤10 entries / ~14 days.  
- No internal ids, enums, or operator fields.  
- Not a decision journal dump.

---

## 9. Plan continuity copy bank (canonical)

Use consistent continuity lines (compose; do not invent educational facts):

| Moment | Example |
|---|---|
| Commit | “This is part of your continuous study plan.” |
| Defer | “Your study plan continues — we’ll meet you when you’re ready.” |
| Reflection | “Tomorrow’s tip will reflect tonight’s work as part of the same plan.” |
| History header | “Choices you’ve made inside one study plan.” |

When `plan_coherence_label` is authored, show it alongside — never invent coherence.

---

## 10. Accessibility & telemetry

| Concern | Spec |
|---|---|
| Forms | WTForms / CSRF; keyboard-operable radios |
| Disclosure | Native `<details>` or existing a11y pattern for defer |
| Contrast | Existing student tokens |
| Telemetry | Observational: `commitment_confirmed`, `commitment_deferred`, `reflection_viewed`, session-link complete — **research only** |
| `data-*` | `data-commitment`, `data-defer-reason`, `data-reflection-field` for contract tests |

---

## 11. Wireframes (text)

### Schema-complete offered

```
┌─────────────────────────────────────────────┐
│  Tonight: {title}              {minutes}    │
│  Why / Why now / Benefit / Next / Coherence │
│  I’m doing this next.                       │
│           [ Start Session ]                 │
│  Not today ▸                                │
│  ▸ Why this tip? …                          │
└─────────────────────────────────────────────┘
```

### Deferred

```
┌─────────────────────────────────────────────┐
│  Deferred for today · {reason}              │
│  Your study plan continues.                 │
│  Tip remains visible as advice (optional)   │
└─────────────────────────────────────────────┘
```

### Reflection

```
┌─────────────────────────────────────────────┐
│  What you did / changed / mattered / next   │
│  Continuity line                            │
│           [ Got it ]                        │
└─────────────────────────────────────────────┘
```

---

## 12. Copy anti-patterns (forbidden)

- “Accept AI recommendation” / “Our model chose correctly”  
- Guaranteed exam outcomes  
- Streak shame on defer  
- Points / badges for commitment rate  
- Fake alternatives presented as re-ranked tips  
- “The AI learned your personality”  
- Internal codes (`not_enough_time` raw enum in UI)

---

## 13. Dogfood checklist (manual)

- [ ] Schema-complete: understand tip, then commit or defer without confusion  
- [ ] Single primary Start Session CTA (no equal competing primary)  
- [ ] Defer reasons calm; no punishment after save  
- [ ] Refusal night: no commit/defer theatre  
- [ ] Completion shows reflection fields without Twin theatre  
- [ ] History shows completed + deferred narrative  
- [ ] Continuity language present on commit, defer, reflection  
- [ ] Coach does not add a second Commit button  
- [ ] No streak / points / gamification  
- [ ] Trust L1 fields still visible  

---

**End of UI_SPECIFICATION**
