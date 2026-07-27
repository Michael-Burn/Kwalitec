# DEP-002 — Feature Flag Audit

**Programme:** DEP-002  
**Resolver:** `app/application/config/v2_flags.py` → `resolve_v2_feature_flags()`  
**Presentation gate:** `app/presentation/consolidation.py`

---

## Flags in scope

| Env var | Flag field | Production (`render.yaml`) | Effect |
|---|---|---|---|
| `KWALITEC_V2_SOLE_RUNTIME` | `SOLE_RUNTIME` | `1` | Presentation cutover: `/` → student home; legacy home redirects; implies student experience |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `ENABLE_STUDENT_EXPERIENCE` | `1` | Enable student surfaces (also forced on when sole is on) |
| `KWALITEC_V2_DURABLE_STORE` | `ENABLE_DURABLE_STORE` | `1` | SQLAlchemy Experience/Session stores |
| `KWALITEC_V2_INJECT_ENGINES` | `INJECT_PHASE_I_ENGINES` | `1` | Wire opaque Phase I engine bridges |

Related (also on Render): `KWALITEC_V2_SEED_DEMO=0`, `KWALITEC_V2_FOUNDER_INTELLIGENCE=1`, `KWALITEC_EI_INTERNAL_ALPHA=1`.

---

## Where flags are read

| Location | Usage |
|---|---|
| `resolve_v2_feature_flags()` | Central env → dataclass |
| `consolidation.is_sole_runtime` / `redirect_if_sole_runtime` / `canonical_home_*` | Home + session-entry authority |
| `app/__init__.py` index route | `/` redirect |
| Dashboard / mission / analytics / settings.index | Call `redirect_if_sole_runtime` |
| Mission nested session helpers | `_sole_runtime_to_canonical()` |
| Template context `v2_flags` | Sidebar branch, dual-run links |
| `app/infrastructure/diagnostics/dual_run.py` | Ops label `sole-runtime-v2` |
| Auth / alpha / calibration / research / study_plan completion | Prefer `canonical_home_url` / `redirect_to_canonical_home` |

---

## Paths that ignore `SOLE_RUNTIME` (by design or gap)

| Path | Behaviour | Notes |
|---|---|---|
| Blueprint registration | Always registers legacy + EOS | Documented soak / rollback |
| Study Plan routes | No sole redirect; renders V1 templates | Shared product surface |
| Settings **subpages** | Index redirects; profile/preferences/data still render V1 | Partial gate |
| Alpha help / onboarding / feedback | Render V1 shell | Linked from EOS nav |
| Research check-in | Render V1 shell | Linked from settings / dual-run |
| Login no-plan branch | Redirects to `study_plan.wizard_step` | Does not use EOS home first |
| Dashboard onboarding check | Runs **before** sole redirect | `/dashboard/` → onboarding, not student, when pending |
| Educational engines / Runtime A | Unaffected | Sole is presentation-only (`EDUCATIONAL_RUNTIME_BRIDGE.md`) |
| Twin / Adaptive / Unified Journey cutovers | Separate flags; default OFF | Not required for dual-chrome observation |

---

## Does legacy bypass the flags?

**Partially, and intentionally.**

- Competing **homes** honour the flag (redirect).  
- Shared **V1 chrome surfaces** never consulted the flag for “do not render”.  
- Therefore legacy runtime is not a flag-failure; it is **out of the flag’s contract**.

Falsified claim: “`KWALITEC_V2_SOLE_RUNTIME` was not present at runtime.”  
Production `/` → `/student/` proves the flag is enforced for its defined scope.

---

## Implication

DEP-003 must either **extend the sole-runtime contract** (wrap shared surfaces in EOS chrome / redirect settings subpages) or **redefine Stage 1 expectations** (document dual chrome as accepted). Flag flipping alone cannot remove the second shell.
