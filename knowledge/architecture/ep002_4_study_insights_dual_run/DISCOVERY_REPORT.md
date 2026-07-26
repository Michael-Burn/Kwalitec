# EP-002.4 — Architecture Discovery Report

**Milestone:** EP-002.4 — Study Insights Dual-Run  
**Date:** 2026-07-26  
**Nature:** Mandatory discovery before implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Scope of discovery

Reviewed:

| Artefact | Path / location |
|---|---|
| EP-001.5 Architectural Integration Review | `knowledge/architecture/ep001_5_architectural_integration_review/` |
| EP-002 Programme Brief | `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md` |
| EP-002.1 Completion Report | `knowledge/architecture/ep002_1_consumer_chain_observability/COMPLETION_REPORT.md` |
| EP-002.2 Completion Report | `knowledge/architecture/ep002_2_shared_foundation_di/COMPLETION_REPORT.md` |
| EP-002.3 Completion Report | `knowledge/architecture/ep002_3_twin_authority_soak/COMPLETION_REPORT.md` |
| Runtime A `RecommendationService` | `app/services/recommendation_service.py` |
| `generate_recommendations` / `build_study_insights` | same module |
| Dashboard / Home routes | `app/dashboard/routes.py` |
| Consumer-chain observability | `app/infrastructure/adapters/consumer_chain/` |
| Feature flags | `app/application/config/v2_flags.py` |

---

## 2. Authority and product surface today

| Concern | Authoritative path | Twin / Insight path |
|---|---|---|
| Student-facing recommendations | `RecommendationService.generate_recommendations` | `build_study_insights` (Twin ON only; returns `None` when OFF) |
| Dashboard / Home | Calls legacy `generate_today_recommendation` + `generate_recommendations` when Educational Intelligence card is absent | **No HTTP callers** of `build_study_insights` (EP-001.5 IF-06) |
| Production defaults | Twin OFF / Authority OFF | Insight unavailable |

**O:** Programme WS4 selects Study Insights as the first dual-run surface; cutover order remains recommendations → readiness → mission.  
**E:** EP-002.3 soak exit: “Safe to begin Study Insights dual-run planning; not ready for production Authority or HTTP cutover.”  
**C:** EP-002.4 may wire observational dual-run; must **not** flip HTTP authority (that is EP-002.5).

---

## 3. RecommendationService entry points

| API | Role | Student influence |
|---|---|---|
| `generate_recommendations(user_id, limit=…)` | Legacy Runtime A list of category/priority rows | **Yes — authoritative** |
| `generate_today_recommendation(user_id)` | Thin wrapper → `generate_recommendations(limit=1)` | **Yes** |
| `build_study_insights(user_id, …)` | EP-001.4 Insight packaging via Foundation + planner + readiness | **No** (not HTTP-wired) |

**O:** Dashboard may call both today + list APIs on one request (two legacy invocations).  
**E:** `app/dashboard/routes.py` lines ~192–201.  
**C:** Dual-run must dedupe within a request so Twin insight is not assembled twice per page load.

**O:** Bridge / Adaptive soak also call `generate_recommendations`.  
**C:** Wiring dual-run at the service method (not only the dashboard route) maximises observation coverage without template changes.

---

## 4. Existing dual-run infrastructure (EP-002.1)

| Component | Behaviour | Gap for EP-002.4 |
|---|---|---|
| `is_dual_run_diagnostics_eligible` | Twin ON ∧ `APP_ENV` ∉ {production, prod} | Reuse as sole gate |
| `compare_legacy_vs_build` | Opaque SHA fingerprints only | Too thin — need latency, codes, confidence, categories |
| `diagnostic_compare_study_insights` | Ops helper; **not** wired to HTTP/`generate_*` | Must become live side-car |
| `ConsumerChainTelemetry.emit_dual_run` | Fingerprint match fields | Extend for structured comparison |
| `observe_build_api` | Latency / outcome / limitations on `build_*` | Twin side already observed when invoked |

**O / E:** EP-002.1 decision: “Dual-run is fingerprint compare helper, not auto-wired into HTTP/`build_*`.”  
**C:** EP-002.4’s job is to **wire** the helper into the legacy recommendation path and enrich comparison capture — without changing return values.

---

## 5. Feature flags

| Env | Flag | Default | Role for dual-run |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | **Required** for Twin path eligibility |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF (requires Twin) | Recorded in telemetry; does **not** gate `build_study_insights` |
| (none new) | — | — | — |

**O:** Programme prefers cohort/env gates over permanent new per-domain flags.  
**E:** Non-prod eligibility already expressed as Twin ON + non-production `APP_ENV`.  
**C / R:** **No new feature flag.** Kill switch = Twin OFF (and/or production `APP_ENV`).

---

## 6. Payload shape divergence (comparison method)

| Dimension | Legacy `generate_recommendations` | Twin `build_study_insights` |
|---|---|---|
| Shape | `list[dict]` with `category`, `priority`, `title`, … | Single guidance `dict` (`todays_key_focus`, `recommended_next_action`, `limitations_codes`, `confidence` via readiness, …) |
| Unavailable | Empty list possible | `None` when Twin OFF / CLS unavailable |
| Limitation codes | Not first-class on list rows | `limitations_codes` on guidance |
| Confidence | Not first-class | `confidence_level` / nested readiness fields when present |

**C:** Fingerprint equality will rarely match — expected. Dual-run success is **structured observational compare**, not byte-identity. Divergence rate is an ops signal for EP-002.5 cutover readiness, not a failure of dual-run itself.

**R:** Compare extracted fields (categories, limitation codes, confidence, availability, latencies, flags, correlation), keep fingerprints as opaque secondary signal.

---

## 7. Consumer-chain & Foundation DI reuse

| Predecessor | Reuse |
|---|---|
| EP-002.1 | `observe_build_api`, dual-run eligibility, telemetry events |
| EP-002.2 | Shared CLS injection when insight composes planner/readiness |
| EP-002.3 | Soak evidence that Twin ON / Authority ON are operable in non-prod; rollback drills |

**C:** No new Twin / planner / readiness / recommendation engine. Extend `consumer_chain` + thin hook in `RecommendationService`.

---

## 8. Risk findings (discovery)

| ID | Risk | Mitigation direction |
|---|---|---|
| D-R1 | Dual-run flips student payload | Return legacy only; Twin path fail-open / swallow |
| D-R2 | Double Twin assemble per dashboard load | Request-scoped dedupe |
| D-R3 | Production accidental dual-run cost | Eligibility excludes production/prod |
| D-R4 | Recursive dual-run via ops helpers | Context / skip guard; dual-run calls `build_study_insights` only |
| D-R5 | New flag proliferation | Do not add flags |
| D-R6 | Premature EP-002.5 cutover | Explicit non-goal; HTTP templates untouched |

---

## 9. Discovery conclusions

| Question | Answer |
|---|---|
| Where to execute Twin? | After legacy `generate_recommendations` succeeds in computing its list; call `build_study_insights` diagnostically |
| What does the student receive? | **Only** the legacy list (unchanged) |
| Gate? | Existing Twin ON + non-production `APP_ENV` |
| New flag? | **No** |
| HTTP / templates? | Unchanged |
| Schema? | None |
| Comparison fields? | Latency, limitation codes, confidence, categories, unavailable, correlation IDs, flags (+ fingerprints) |
| Ready to implement? | **Yes** — after Dual-Run Design, Gap Analysis, and Rollback Plan are recorded |

---

## 10. Implementation authorisation

**Observation:** Prerequisites EP-002.1–3 are complete; gaps are wiring + structured compare.  
**Evidence:** This discovery + programme WS4 + EP-002.3 recommendation.  
**Conclusion:** Implementation of observational Study Insights dual-run is authorised.  
**Recommendation:** Proceed per [`DUAL_RUN_DESIGN.md`](DUAL_RUN_DESIGN.md); stop before HTTP cutover (EP-002.5).
