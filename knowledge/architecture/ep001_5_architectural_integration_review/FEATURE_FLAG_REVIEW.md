# EP-001.5 — Feature Flag Review

**Milestone:** EP-001.5  
**Review area:** Twin-related flags, rollout, consumers, retirement  
**Date:** 2026-07-26

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Current Twin-related flags (implemented)

| Env var | Resolved flag | Default | Resolution notes |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | **OFF** | `v2_flags.py` |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | **OFF** | AND-gated: requires Twin ON |

**E:** `.env.example` documents both flags and EP-001.2–4 consumption under Twin ON (no separate planner/readiness/insight flags).

---

## 2. Documented but not separately implemented

| Flag (architecture docs) | Code reality |
|---|---|
| `KWALITEC_DIGITAL_TWIN_SHADOW` | Shadow validator wires when `ENABLE_DIGITAL_TWIN` ON — **no separate env flag** |
| `KWALITEC_DIGITAL_TWIN_ADAPTIVE_INPUT` | Twin input adapter wires when Twin ON — **no separate env flag** |

**C:** Doc/code drift is documentation debt, not behavioural defect. Behaviour is subsumed under `KWALITEC_DIGITAL_TWIN`.

**R:** Align architecture docs to state that Shadow and Adaptive TwinInput are bundled under Twin ON, or introduce separate flags only if independent rollout is required.

---

## 3. Consumers by flag

### `ENABLE_DIGITAL_TWIN`

| Consumer | Behaviour when ON | Behaviour when OFF |
|---|---|---|
| `StudentExperienceComposition` | Builds Twin adapter, facets, snapshot, explainability, twin_input, shadow, Foundation | All Twin DI `None` |
| `PlanningService.build_daily_study_plan` | Assembles Canonical plan | Returns `None` → legacy mission path |
| `ReadinessService.build_readiness_intelligence` | Assembles intelligence | Returns `None` → legacy getters |
| `RecommendationService.build_study_insights` | Assembles insights | Returns `None` → legacy recommendations |
| `TwinInputAdapter` | May enrich Adaptive bundles | Unavailable attachment |
| Dual-run / rollback verifiers | Expect Twin DI present | Expect Twin DI absent |

### `ENABLE_DIGITAL_TWIN_AUTHORITY`

| Consumer | Behaviour when ON | Behaviour when OFF |
|---|---|---|
| `composition.twin` | `StudentTwinFoundationAuthorityPort` (fallback ExperienceTwinAdapter) | `ExperienceTwinAdapter` |
| Runtime A `build_*` services | **Not checked** — gated by Twin only | N/A |

**C:** Authority is correctly narrower than Twin construction. EP-001.2–4 do not require Authority.

---

## 4. Rollout strategy (as designed)

```
Stage 0 (current default): Twin OFF → zero UX change
Stage 1: Twin ON (shadow + Foundation + Adaptive TwinInput + build_* APIs available)
Stage 2: Twin Authority ON → Experience StudentTwinPort serves Foundation
Stage 3 (not started): HTTP cutover to build_* surfaces
Stage 4 (future): Retire legacy duplicate presentation paths where safe
```

**O:** Stages 0–1 infrastructure exist; Stage 2 is optional and OFF; Stage 3 has no route wiring.

**C:** Rollout strategy is **safe and coherent**, but **incomplete as a product rollout**.

---

## 5. Retirement strategy

| Flag / path | Retirement condition | Ready now? |
|---|---|---|
| Twin OFF fail-open | Never retire until HTTP + Experience cutover proven | No |
| `ExperienceTwinAdapter` as default TwinPort | After Authority soak + demo-seed risk accepted/removed | No |
| Legacy `generate_recommendations` | After insight cutover + explainability consolidation | No |
| Legacy `get_overall_readiness` as UX score | After intelligence cutover; **must remain** for collectors until collector refactor | Partial — keep as collector fact path |
| Separate Shadow/Adaptive-input flags | N/A if bundled permanently | Clarify docs |

**R:** Do not retire Twin OFF fail-open prematurely. Treat collector-safe `get_overall_readiness` as a long-lived Runtime A fact API even after UX cutover.

---

## 6. Verdict

| Question | Answer |
|---|---|
| Flags sufficient for safe EP-001 rollout? | **Yes** |
| Over-flagging / under-flagging? | Under-documented separate Shadow/Adaptive flags (bundled in practice) |
| Consumers correctly gated? | **Yes** |
| Retirement path defined? | Directionally yes; execution blocked on cutover soak |
