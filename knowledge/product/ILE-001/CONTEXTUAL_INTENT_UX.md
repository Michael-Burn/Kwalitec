# Contextual Intent UX — ILE-001C

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001C — Contextual Intent & Educational Framing  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** ILE-001C0 Study Sensei Communication Framework; ILE-010; ILE-011; P-001.2; P-001.3  

---

## Purpose

Ensure every Adaptive Assessment entry answers three learner questions before asking for action:

1. Why am I seeing this?  
2. Why now?  
3. Why should I care?

Presentation and educational communication only — no Twin, Reasoning, selection, or Mission planning changes.

---

## Learner journey (when framing enabled)

```
Mission
  → Context Card
  → Quick Check questions
  → Reflection (observation → meaning → suggested action → student choice)
  → Educational Summary (+ recommendation framing)
  → Mission resumes
```

When `KWALITEC_CONTEXTUAL_FRAMING` is OFF, ILE-001B surfaces remain unchanged.

---

## Context Card

Before Begin, show a lightweight educational arc composed from the copy registry:

| Layer | Student question |
|---|---|
| Observation | What did we notice? |
| Educational meaning | What does that mean for learning? |
| Purpose | Why this check? |
| Expected benefit | Why bother? |
| Invitation | Begin when ready |

Optional expand: “Why am I seeing this?”

Implementation: `educational_framing.build_context_card` + `introduction.html`.

---

## Educational Summary

After reflection, replace generic thank-you chrome with:

| Layer | Content |
|---|---|
| What you worked on | Activity framing (not a score) |
| Evidence gathered | Formative signals collected |
| What this means | Mission alignment |
| What happens next | Calm continuity |

Never: scores, grades, pass/fail, mastery labels, motivational hype, false certainty.

---

## Recommendation framing

When a recommendation is shown:

Recommendation → Reason → Supporting evidence → Confidence (qualitative) → Expected benefit → Uncertainty (when applicable)

“Why this recommendation?” expands educational reasoning only — never algorithms, Twin fields, or AI terminology.

Insufficient / observation-only bands suppress a firm primary tip and use ILE-001C0 uncertainty language.

---

## Reflection

Expanded into:

Observation → Meaning → Suggested action → Student choice (accept / decide later / continue in my own way)

Recommendations remain guidance only.

---

## Feature flag

| Flag | Env | Default |
|---|---|---|
| Contextual framing | `KWALITEC_CONTEXTUAL_FRAMING` | OFF |

Requires Adaptive Assessment master switch + subject/cohort gates. Independent of session-type flags for the framing gate helper; Quick Check still requires its own enablement for the experience path.

---

## Telemetry (behavioural only)

| Event | When |
|---|---|
| `ContextViewed` | Context Card shown |
| `WhyRecommendationOpened` | Why-recommendation expanded |
| `ExplanationExpanded` | Other explanation expand |
| `RecommendationAccepted` | Learner accepts suggestion |
| `RecommendationDeferred` | Learner defers |
| `ReflectionCompleted` | Reflection submitted |

No educational outcomes, answers, or Twin state.

---

## Implementation map

| Concern | Location |
|---|---|
| Framing composition | `app/application/adaptive_assessment/educational_framing.py` |
| Experience wiring | `quick_check_experience.py` |
| Copy | `copy_registry.py` (`framing.*` keys) |
| Flag | `feature_flags.py` |
| Templates | `introduction.html`, `reflection.html`, `completion.html`, `components/recommendation_frame.html` |

---

## Explicit non-goals

- Adaptive selection / Twin / Reasoning / Tutor / readiness model changes  
- Decision Journal / Timeline  
- Curriculum logic changes  
- AI behaviour changes  

---

**End of CONTEXTUAL_INTENT_UX**
