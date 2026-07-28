# ILE-001C — Implementation Notes

**Milestone:** ILE-001C — Contextual Intent & Educational Framing  
**Date:** 2026-07-28  

---

## Design choices

1. **Presentation intent context** — Framing composes from `PresentationIntentContext` (focus label + qualitative evidence band). No Twin or Reasoning calls. Default band is `emerging` so guidance stays provisional until later programmes supply richer presentation inputs.

2. **Copy-driven arcs** — All learner speech resolves through `copy_registry` keys (`framing.*`), converging toward ILE-001C0 microcopy patterns without hard-coding example paragraphs in templates.

3. **Backward compatibility** — `ENABLE_CONTEXTUAL_FRAMING` defaults OFF. With Quick Check on and framing off, ILE-001B introduction / completion / reflection templates render as before.

4. **Phase names unchanged** — INTRODUCTION and COMPLETION phases remain; Context Card and Educational Summary attach as optional snapshot contracts when framing is on.

5. **Recommendation honesty** — `insufficient` and `observation_only` bands set `suppress_primary` and surface ILE-001C0 uncertainty phrases instead of inventing certainty.

---

## Architecture traceability

| Layer | Role in ILE-001C |
|---|---|
| Templates / JS | Render framing contracts; expand telemetry via fetch |
| Blueprint routes | Thin HTTP; mark context viewed; recommendation choice |
| Application framing | Deterministic copy composition |
| Application experience | State machine + behavioural telemetry |
| Educational Intelligence | Untouched |

Curriculum V1/V2: not affected (no curriculum engine changes).

---

## Enabling for dogfood

```bash
export KWALITEC_ADAPTIVE_ASSESSMENT=1
export KWALITEC_QUICK_CHECK=1
export KWALITEC_CONTEXTUAL_FRAMING=1
# optional: KWALITEC_ADAPTIVE_ASSESSMENT_SUBJECTS=...
# optional: KWALITEC_ADAPTIVE_ASSESSMENT_COHORTS=...
```

---

## Follow-ups (out of scope here)

- Wire presentation intent band from Mission / Twin-visible eligibility signals without moving educational authority into the experience layer (ILE-001C roadmap residual / later slice).  
- Density / time-gate visibility when product gates exist.  
- Analytics bridge for in-memory telemetry sink.

---

**End of IMPLEMENTATION_NOTES_ILE001C**
