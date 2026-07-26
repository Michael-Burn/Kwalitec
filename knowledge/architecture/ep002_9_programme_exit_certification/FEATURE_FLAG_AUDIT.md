# EP-002.9 — Feature Flag Audit

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Code truth:** `app/application/config/v2_flags.py`  
**Docs truth:** `.env.example`

Legend: **O** · **E** · **C** · **R**

---

## 1. EP-002-related flags (implemented)

| Env var | Resolved field | Default | Requires | Production eligibility |
|---|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | **OFF** | — | Allowed for Twin DI / soak; does not alone flip HTTP cutover |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | **OFF** | Twin ON | Experience TwinPort only; recorded but not required by Runtime A cutovers |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `ENABLE_STUDY_INSIGHTS_CUTOVER` | **OFF** | Twin ON | **Hard-ineligible** when `APP_ENV`/`FLASK_ENV` ∈ {`production`,`prod`} |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | **OFF** | Twin ON | **Hard-ineligible** in production/prod |
| `KWALITEC_DAILY_PLAN_CUTOVER` | `ENABLE_DAILY_PLAN_CUTOVER` | **OFF** | Twin ON | **Hard-ineligible** in production/prod |

**E:** `v2_flags.py` AND-gates cutovers on Twin; cutover modules enforce `_PRODUCTION_ENVS`.  
**E:** `.env.example` documents all five flags.

---

## 2. Bundled behaviours (no separate flags)

| Documented historical name | Code reality |
|---|---|
| `KWALITEC_DIGITAL_TWIN_SHADOW` | Shadow validator wires when Twin ON |
| `KWALITEC_DIGITAL_TWIN_ADAPTIVE_INPUT` | TwinInput adapter wires when Twin ON |
| Per-`build_*` enable flags | Not implemented — Twin ON enables API availability |
| `ENABLE_STUDY_INSIGHTS_DUAL_RUN` | Explicitly rejected in EP-002.4 |
| `ENABLE_CONSUMER_CHAIN_SOAK` | Explicitly not added in EP-002.3 |

**C:** Under-flagging for Shadow/Adaptive-input is intentional bundling (TD-ARCH-06 closed at docs level in EP-002.1). Dual-run / soak use Twin + environment gates rather than permanent new flags.

---

## 3. Consumers by flag (post EP-002)

### `ENABLE_DIGITAL_TWIN`

| Consumer | ON | OFF |
|---|---|---|
| Composition Twin DI / Foundation / Shadow / TwinInput | Built | Absent |
| `build_daily_study_plan` / `build_readiness_intelligence` / `build_study_insights` | May assemble | Return `None` |
| Dual-run sidecars | Eligible in non-prod | Skipped |
| Cutover eligibility | Prerequisite | Ineligible |

### `ENABLE_DIGITAL_TWIN_AUTHORITY`

| Consumer | ON | OFF |
|---|---|---|
| Experience `composition.twin` | Foundation Authority port (fallback ExperienceTwinAdapter) | ExperienceTwinAdapter |
| Runtime A HTTP cutovers | Not required | N/A |

### Cutover flags

| Flag | Surfaces | Fail-open |
|---|---|---|
| Study Insights Cutover | Dashboard / home recommendations | `generate_recommendations` |
| Readiness Intelligence Cutover | Dashboard / analytics readiness | Legacy readiness surface |
| Daily Plan Cutover | Dashboard / missions display | `generate_today_mission` (+ ORM persistence unchanged) |

---

## 4. Rollout stages (post EP-002)

```
Stage 0 (production default): Twin OFF → zero Twin UX
Stage 1: Twin ON → Foundation + Shadow + TwinInput + build_* + observability
Stage 2: Twin Authority ON → Experience TwinPort Foundation (non-prod soaked; prod not authorised)
Stage 3: Per-surface HTTP cutover ON (non-prod only; production hard-ineligible)
Stage 4: Presentation consolidated (EP-002.8) — selection facade live regardless of flag values
Stage 5 (future): Production cutover eligibility change + GA decision (not authorised by EP-002)
```

**C:** Stages 0–4 architecture exist. Stage 5 is a successor ops/product decision.

---

## 5. Retirement strategy

| Flag / path | Retirement condition | Ready now? |
|---|---|---|
| Twin OFF fail-open | Never until production cutover proven + GA | **No** |
| ExperienceTwinAdapter default | After Authority soak in target env + demo-seed policy | **No** |
| Legacy `generate_recommendations` | After Insights cutover proven in target env + EI residual disposition | **No** |
| Legacy readiness getters | Keep for collectors indefinitely until collector refactor | **Partial** — UX may cut over; getters remain |
| Legacy `generate_today_mission` | Keep as ORM persistence authority even if display cut over | **Yes — retain** |
| MissionOptimizer | Hard-delete after quarantine soak | Deferred (`TD-DP-04`) |
| Cutover flags | Retire only after permanent cutover + monitoring replacement | **No** |

---

## 6. Governance rules (binding)

1. Default all EP-002 flags **OFF** in production.  
2. Never remove production hard-ineligibility without an explicit production go/no-go artefact.  
3. Prefer Twin kill switch for emergencies over partial cutover debugging under incident load.  
4. Do not add permanent per-domain dual-run flags unless independent rollout is proven necessary.  
5. Document any new Twin-related flag in `.env.example` and this audit’s successor.

---

## 7. Verdict

| Question | Answer |
|---|---|
| Flags sufficient for safe EP-002 exit? | **Yes** |
| Production defaults safe? | **Yes** (all OFF) |
| Over-flagging? | No — three surface cutovers are intentional |
| Under-flagging? | Shadow/Adaptive bundled (accepted) |
| Doc/code alignment? | **Aligned** for EP-002 cutover flags |
| Authorises production GA? | **No** |

**C:** Feature-flag governance is certified for Controlled Pilot posture, not GA.
