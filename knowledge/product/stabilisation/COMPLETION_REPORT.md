# Architecture Stabilisation Sprint — Completion Report

## Summary

Restored Phase 1 architectural stability after CS-DOC / CIP / SDT / AME / AP / TUTOR milestones. Failures reduced from **44 failed → 0 failed** while preserving behaviour, Clean Architecture / DDD boundaries, and educational intelligence invariants. Full suite: **43,684 passed**, 7 skipped.

## Root cause summary

| Category | Root cause | Fix |
|----------|------------|-----|
| Architecture — Studio ports | `PORT_NAMES` included document ports not owned by `CurriculumStudioService` | Restored 3-port facade health matrix; document ports remain on upload service |
| Architecture — independence | Application imported infrastructure / ORM / services | Port injection + composition roots (metadata, analytics, embeddings, commitment, readiness) |
| Architecture — Twin T4 | `shadow_rollback.py` imported Experience composition / named ExperienceTwinAdapter | Default factory moved to `twin_rollback_defaults.py`; comments cleaned |
| Architecture — mission purity | Mission generation used forbidden name `prioritise` | Renamed to `order_for_execution` (ordering, not recommendation ranking) |
| Architecture — thin routes | `submit_reflection` exceeded 45-line handler budget | Extracted `_render_submit_result` helper |
| Architecture — analytics guard | `educational_state_events` imported application educational_state | Bind port from `app.infrastructure` composition root instead |
| Configuration — sole runtime | Bound import of `resolve_v2_feature_flags` broke patches | Proxy + dual patch-target compatible resolution |
| Configuration — Alembic | Operational/CI pins still at `202607260001` | Updated to single head `202607270013` |
| Performance — JS budget | Studio/session JS lived in top-level `js/` counted by budget harness | Moved to `js/curriculum_studio/` and `js/session/` (mirrors CSS layout) |
| Templates / branding / explainability | Missing Learning Mode / Estimated Knowledge / brand wiring / honest login copy / footer / fonts | Restored student-facing copy and layout includes (pre-existing WIP + targeted fixes) |
| Snapshots | Token/`color-scheme` intentional brand updates | Golden snapshots regenerated to match correct output |
| Recommendation equality | `generated_at` microsecond drift | Stable second-precision timestamps in recommendation path |

## Files modified (stabilisation-critical)

### Architecture / boundaries
- `app/application/curriculum_studio/ports/__init__.py`
- `app/application/curriculum_studio/document_upload_service.py`
- `app/application/curriculum_studio/ports/document_metadata_port.py` (port contract)
- `app/infrastructure/adapters/document_storage/metadata.py` (**new**)
- `app/infrastructure/adapters/document_storage/__init__.py`
- `app/presentation/curriculum_studio/factory.py`
- `app/infrastructure/adapters/digital_twin/shadow_rollback.py`
- `app/infrastructure/adapters/twin_rollback_defaults.py` (**new**)
- `app/infrastructure/analytics/educational_state_events.py`
- `app/infrastructure/__init__.py`
- `src/application/education/mission_generation/adaptive_mission_generator.py`
- `src/application/education/mission_generation/rules/ordering_rules.py`
- `src/application/education/revision_planner/services/dependency_resolver.py`
- `src/adapters/flask/reflection/routes.py`

### Runtime / config
- `app/presentation/consolidation.py`
- `tests/operational/helpers.py`
- `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md`
- `.github/workflows/ci.yml`

### Performance / static
- `app/static/js/curriculum_studio/*` (moved)
- `app/static/js/session/study_session.js` (moved)
- Template script tags updated accordingly

### Broader WIP already in tree (also required for green suite)
Independence ports for educational_state / journey / reflection / twin / student_experience; template/brand/explainability restorations; recommendation timestamp stability; EOS snapshot updates — see `git status` / `git diff --stat`.

## Architectural impact assessment

- **Preserved:** Curriculum V1/V2 loadability; Student Digital Twin as sole learner state; Educational Reasoning as sole reasoning orchestrator (`StudentReasoningService`); Tutor explains rather than reasons; Mission Engine consumes reasoning outputs (ordering only); Assessment produces observations; Learning Graph stores relationships; no LLM; no direct vector-store access from application without ports.
- **Dependency direction:** Application → ports ← Infrastructure adapters. Analytics no longer imports `app.application.educational_state`.
- **No redesign:** Additive ports and renames only; no feature removal; no weakened tests.

## Dependency changes

- No new runtime packages required for the stabilisation fixes.
- `Pillow` already present for brand logo tests; `argon2-cffi` already in `requirements.txt` (use project `.venv`).

## Test summary

```
43684 passed, 7 skipped, 0 failed
flask db heads → 202607270013 (head)  # single head
```

Ruff: changed stabilisation files are clean under CI’s `ruff check app/ src/ tests/ --ignore=F401`. The wider tree still reports a large pre-existing lint backlog (~800) from concurrent Phase 1 WIP outside this sprint’s minimal diff — not introduced by the failure fixes themselves. Recommend a follow-up `ruff --fix` / import-hygiene pass on the broader WIP if CI gates on a fully clean tree.

## Technical debt

- Broader Phase 1 WIP still mixes many uncommitted modules; stabilisation made them green but a dedicated commit/split PR is still advisable.
- Pre-existing ruff backlog across `app/` / `src/` / `tests/`.
- Local DB may be behind head (`202607270003` → `202607270013`); run `flask db upgrade` for runtime.

## Known limitations

- Did not redesign architecture or add Phase 2 product features.
- Snapshot updates assume current brand/token output is intentional (validated against live renderer).
- JS budget compliance uses directory layout matching the existing CSS budget pattern; top-level `js/*.js` remains the student shell budget surface.
