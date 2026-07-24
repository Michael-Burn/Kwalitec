# V2-023 — Release Candidate (RC-1)

**Branch:** `feature/educational-architecture-consolidation`  
**Date:** 2026-07-23  
**Status:** RC-1 produced  
**Mode:** Controlled cleanup — presentation retirement + sole-runtime activation  
**Prerequisite:** V2-022 completeness corrections closed on this branch (Profile → EducationalState; nested LXP redirects)

**Authority:** [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) · [CANONICAL_RUNTIME_VALIDATION.md](CANONICAL_RUNTIME_VALIDATION.md) · [V2_020_RETIREMENT_RUNBOOK.md](../../knowledge/version2/V2_020_RETIREMENT_RUNBOOK.md)

---

## Recommendation

# GO (RC-1)

Activate sole runtime for production Render. Canonical Student Experience + Session Experience are the only live student educational UX. Legacy presentation entry points redirect. Protected educational engines are unchanged.

**Conditions (operator):**

1. Take a Postgres backup before deploy (runbook).  
2. Record product evidence observation on `/founder/evidence-gates` during soak (gate does not auto-pass).  
3. Keep legacy redirect shells for one soak window before physical template deletion.  
4. Rollback = unset `KWALITEC_V2_SOLE_RUNTIME` and restart.

---

## Summary

V2-023 retires competing student presentation entry under sole runtime and enables `KWALITEC_V2_SOLE_RUNTIME=1` on Render. Residual V2-021/V2-022 gaps closed: Profile projects through `EducationalStateService`; nested `/missions/<id>/session*` and review shims redirect to Student Dashboard when sole runtime is on. V1 sidebar under sole runtime mirrors the canonical nav tree. Dead `mission.js` removed. Educational calculators, Twin, Evidence, CMP, IFoA curriculum, and Mission engines were not deleted.

Educational outputs on the Experience path remain Twin/Adaptive/Journey/Mission projections via a shared Educational State snapshot — no new readiness/mastery formulas.

---

## Removed / retired components

| Component | Disposition |
|-----------|-------------|
| Dual-run Version 2 / “Back to Dashboard” CTAs | Already removed (Phase 1); verified absent |
| `app/static/js/mission.js` | **Deleted** (unreferenced presentation JS) |
| Legacy `/dashboard/`, `/analytics/`, `/missions/` list under sole | Redirect shells (templates retained for soak/rollback) |
| Nested LXP `/missions/<id>/session*` + review under sole | **Redirect to `student.home`** (new) |
| Competing V1 sidebar destinations under sole | Canonical nav labels (Dashboard · Journey · Revision · Analytics · Study Plan · Settings · Help) |

**Not removed (protected / READY FOR MIGRATION soak):**

- Twin, EducationalStateService, Learning Evidence, Recommendation/Adaptive engines  
- IFoA curriculum, CMP, domain models, Mission Engine / Adapter  
- `StudySessionService`, `ReadinessService` (dual-run rollback / evidence authority)  
- Legacy HTML templates for dashboard / analytics / LXP (redirect shells)

---

## Sole runtime activation

| Surface | Value |
|---------|-------|
| Production | `render.yaml` → `KWALITEC_V2_SOLE_RUNTIME=1` |
| Local default | Still **off** when unset (`.env.example` does not enable) |
| Alpha dual-run env helper | Still sole **off** for local soak |
| Index `/` | → `student.home` when sole on |

---

## Navigation (final)

1. Dashboard  
2. Journey  
3. Revision  
4. Analytics  
5. Study Plan  
6. Settings  
7. Help  

No student-visible Version 2 CTAs. No duplicate Session/Analytics products under sole runtime.

---

## Performance comparison

| Probe | V2-021 / GA reference | V2-023 measured | Verdict |
|-------|----------------------|-----------------|---------|
| Educational State assembly (avg) | &lt; 5 ms four-projection | **0.005 ms** load; **0.19 ms** five projections | No regression |
| Full session happy-path (pytest call) | ~30 ms | **~30 ms** | Identical |
| HTTP `/student/` avg | GA budget 2500 ms | **~6.5 ms** (test client) | Within budget |
| HTTP `/student/journey` avg | 2500 ms | **~3.7 ms** | Within budget |
| HTTP `/session/.../overview` avg | 2500 ms | **~3.2 ms** | Within budget |
| GA soft-budget suite | — | `tests/ga/test_performance_benchmarks.py` **13 passed** | Pass |

No significant regression vs V2-021 Experience path timings.

---

## Test summary

```bash
.venv/bin/python -m pytest \
  tests/application/educational_state/ \
  tests/presentation/student/ \
  tests/presentation/workflows/test_workflow_dual_run.py \
  tests/presentation/workflows/test_workflow_consistency.py \
  tests/presentation/workflows/test_workflow_student_session.py \
  tests/operational/test_alpha_smoke_student.py \
  tests/operational/test_alpha_sole_runtime_protection.py \
  tests/operational/test_alpha_configuration.py \
  tests/application/config/test_v2_flags.py -q
```

**Outcome:** **492 passed**.

Also: `tests/ga/test_performance_benchmarks.py` + operational suite → **78 passed**; **1 pre-existing fail** (`test_templates_reference_css` / founder CSS reference — unrelated to V2-023; also noted in Phase 1 consolidation report).

Ruff on touched Python paths: **clean**.

---

## Remaining risks / technical debt

| Risk | Severity | Mitigation |
|------|----------|------------|
| Product evidence gate still operator-recorded | Medium | Soak checklist; do not treat RC as educational proof |
| Analytics chart parity (History vs V1 charts) | Medium | History is canonical; chart parity is a follow-up programme |
| Legacy templates still on disk | Low | Redirect shells; delete after soak window |
| `StudySessionService` still present | Low (intentional) | Required for rollback; not student entry under sole |
| Projection fallbacks without EducationalState | Low | Unit-test compat only; production facade wires EducationalState |
| Founder asset lint failure (pre-existing) | Low | Track outside RC-1 student cutover |

---

## Rollback plan

1. Unset `KWALITEC_V2_SOLE_RUNTIME` (or set `0`) on Render / host.  
2. Redeploy / restart.  
3. Confirm `/` → `/dashboard/`.  
4. Leave V2 durable tables intact.  

Documented in `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` § Rollback and `V2_020_RETIREMENT_RUNBOOK.md`.

---

## Architecture compliance

- Curriculum V1/V2 loadability: **untouched**  
- Twin / Evidence / CMP / Adaptive / Journey / Mission engines: **preserved**  
- Layering: presentation redirects → application Educational State → ports → engines  
- No Alembic / schema changes  

**Migration impact:** None.

---

## Files created

- `docs/architecture/SYSTEM_ARCHITECTURE.md`  
- `docs/architecture/V2_023_RELEASE_CANDIDATE.md` (this file)

## Files modified (primary)

- `app/application/student_experience/profile_service.py` — EducationalState consumer  
- `app/application/student_experience/student_experience_service.py` — wire Profile  
- `app/mission/routes.py` — nested LXP / review sole-runtime redirects  
- `app/templates/partials/sidebar.html` — canonical nav under sole  
- `render.yaml` — `KWALITEC_V2_SOLE_RUNTIME=1`  
- `ARCHITECTURE.md`, `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md`  
- Operational / dual-run / educational_state tests  

## Files deleted

- `app/static/js/mission.js`

---

## Success criteria checklist

| Criterion | Met? |
|-----------|------|
| One runtime (production sole) | **Yes** |
| One navigation tree under sole | **Yes** |
| One educational state for Experience surfaces | **Yes** (incl. Profile) |
| One dashboard / journey / coach / analytics UX under sole | **Yes** |
| No live legacy presentation entry under sole | **Yes** (redirects) |
| Protected educational engines unchanged | **Yes** |
| Performance no significant regression | **Yes** |

---

## Next after soak

1. Physically delete legacy dashboard/analytics/LXP templates after soak evidence.  
2. Analytics chart parity programme (optional richness on History).  
3. Close founder CSS asset lint debt.  
4. Optional: remove EducationalState projection fallbacks once all unit call sites require the facade.
