# EP-008.3A — Implementation Notes

**Programme:** EP-008.3A  
**Date:** 2026-07-26  

---

## UI pattern choice (UI_SPEC §2.1)

**Chosen: Pattern A — Combined Start Session + commitment.**

- Primary button remains **Start Session** (DR-050).
- Helper copy: “I’m doing this next.” / “Starting means you’re doing this next.” (`data-commitment="confirm"`).
- POST `/student/session/start` records preference commitment via `RecommendationCommitmentService.confirm_commitment` before / with session start.
- Defer remains a secondary disclosure (“Not today”) — not a competing primary CTA.

Rationale: minimise cognitive load while still recording conscious intent; Validation Plan watches load themes in Tier B.

---

## Persistence

Option A from Engineering Design: additive `recommendation_commitments` table + call existing `RecommendationService.record_decision` for Decision Journal continuity. No ranking edits.

---

## Observational metrics

New learning-feedback event types (research-only, fail-open):

- `commitment_confirmed`
- `commitment_deferred`
- `commitment_completed`
- `reflection_viewed`

Never fed into RecommendationService scoring inputs.

---

## Explicit non-goals respected

No Runtime A / ranking / Planning / Readiness reasoning changes; no LLM; no streaks/badges; no gamification; no metrics→ranking feedback.

---

**End of IMPLEMENTATION_NOTES**
