# EQ-001 — Implementation Plan

**Programme:** EQ-001 — Educational Quality Certification  
**Status:** Complete  
**Date:** 2026-07-27  

---

## Approach

1. **Define standards** for mission, study plan, journey, and explainability (product law).
2. **Enrich PI-001B derivation** so mission templates carry quality fields at source.
3. **Enrich PI-001C runtime projections** with mission quality envelopes, journey explanations, and exam-aware pacing — without UI redesign or Runtime A cutover.
4. **Automate certification** via `EducationalQualityCertifier` + `tests/certification/test_eq001_educational_quality.py`.

## Non-goals (honoured)

- No Runtime A cutover  
- No UI redesign  
- No Twin activation  
- No Alembic migration (quality derived at read/generation time)  
- Backward-compatible DTO extensions (optional `quality` field)

## Architecture touchpoints

```
Published package
    → EducationalArtefactDeriver (+ mission quality fields)
    → EducationalQualityCertifier.certify_artefacts
    → EducationalRuntimeEngineService.generate_daily_mission (+ envelope + prereq gate)
    → get_journey_explanation / project_pacing
    → EducationalQualityCertifier.certify_mission / journey / pacing
```
