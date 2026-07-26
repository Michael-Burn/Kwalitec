# EP-002.5 — Architecture Discovery Report

**Milestone:** EP-002.5 — Study Insights Gated HTTP Cutover  
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
| EP-002.4 Completion Report | `knowledge/architecture/ep002_4_study_insights_dual_run/COMPLETION_REPORT.md` |
| Runtime A `RecommendationService` | `app/services/recommendation_service.py` |
| Dashboard / Home routes | `app/dashboard/routes.py` |
| Dual-run implementation | `app/infrastructure/adapters/consumer_chain/dual_run.py` |
| Consumer-chain telemetry | `app/infrastructure/adapters/consumer_chain/telemetry.py` |
| Feature flags | `app/application/config/v2_flags.py` |

---

## 2. Authority and product surface today

| Concern | Authoritative path | Twin / Insight path |
|---|---|---|
| Student-facing recommendations | `RecommendationService.generate_recommendations` | `build_study_insights` (dual-run side-car only; EP-002.4) |
| Dashboard / Home | `generate_today_recommendation` + `generate_recommendations` when EI card absent | **No HTTP cutover** yet |
| Production defaults | Twin OFF / Authority OFF / Cutover OFF | Insight unavailable to students |

**O:** EP-002 programme cutover order is recommendations → readiness → mission; WS4 selects Study Insights as first student-visible surface.  
**E:** EP-002.4 exit: “Safe to **plan** Study Insights gated HTTP cutover”; fingerprints diverge by shape (expected); topical alignment deferred to EP-002.5.  
**C:** EP-002.5 may flip HTTP authority **only** under gated eligibility with legacy fail-open.

---

## 3. RecommendationService entry points

| API | Role | Student influence (pre-EP-002.5) |
|---|---|---|
| `generate_recommendations(user_id, limit=…)` | Legacy Runtime A list | **Yes — authoritative** |
| `generate_today_recommendation(user_id)` | Wrapper → `limit=1` | Yes |
| `build_study_insights(user_id, …)` | EP-001.4 Insight packaging | No (diagnostic dual-run only) |

**O:** Dashboard calls today + list APIs when Educational Intelligence card is absent.  
**E:** `app/dashboard/routes.py` (~192–210); template loops `all_recommendations` expecting `title` / `priority` / `category` / `reason` / explainability fields.  
**C:** Cutover must either project Study Insights into the existing `list[dict]` card shape **or** change templates. Prefer projection to avoid template / EI dual-path rewiring.

**O:** Bridges / Founder also call `generate_recommendations`.  
**C / R:** Cutover must **not** silently change bridge/Founder behaviour. Host cutover in a **dashboard-facing** service method; leave `generate_recommendations` as legacy fail-open authority (dual-run retained when cutover flag OFF).

---

## 4. Dual-run inheritance (EP-002.4)

| Component | Behaviour | Implication for cutover |
|---|---|---|
| `is_dual_run_diagnostics_eligible` | Twin ON ∧ non-prod | Reuse env gate; cutover needs an **additional** explicit flag |
| `run_study_insights_dual_run` | Side-car after legacy; `influences_student=False` | When cutover ON, skip dual-run Twin call to avoid double assemble |
| Structured compare | Latency, codes, confidence, categories | Fingerprint divergence expected — **not** a cutover quality signal |
| Dual-run health | `ready_for_ep002_5_planning` | Planning green; not production go |

**O / E:** EP-002.4 §16 recommends topical alignment (topic_id / title heuristics) before cutover.  
**C:** EP-002.5 must implement semantic alignment reporting distinct from fingerprint match.

---

## 5. Feature flags

| Env | Flag | Default | Role for cutover |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | **Required** for Twin path |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF | Recorded; **not** required for Runtime A `build_study_insights` (Foundation path, not Experience TwinPort) |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `ENABLE_STUDY_INSIGHTS_CUTOVER` | OFF | **New** — student-payload flip gate |
| `APP_ENV` / `FLASK_ENV` | — | development | Must not be `production` / `prod` |

**O:** Programme prefers cohort/env gates over permanent new per-domain flags **unless** independent rollout is required.  
**E:** Dual-run correctly rejected a new flag because it did not change student payloads. HTTP cutover **does** change payloads.  
**C / R:** **Add** `KWALITEC_STUDY_INSIGHTS_CUTOVER` (default OFF). Kill switches = Cutover OFF **or** Twin OFF **or** production env.

---

## 6. Payload shape (projection requirement)

| Dimension | Legacy | Twin Study Insights |
|---|---|---|
| Shape | `list[dict]` rows | Single guidance `dict` with InsightField objects |
| Template contract | `title`, `priority`, `category`, `reason`, optional explainability | `todays_key_focus`, `recommended_next_action`, `greatest_risk`, … |
| Unavailable | Empty list possible | `None` when Twin OFF / CLS unavailable |
| Limitation codes | Not first-class | `limitations_codes` on guidance |

**C:** Eligible HTTP responses must project Twin guidance into legacy-compatible recommendation rows so `dashboard/index.html` needs no structural rewrite.  
**R:** Mark projected rows with `source_authority="study_insights"` and skip EducationalExplainability re-narration (Insight already owns communication).

---

## 7. Blocking limitation concept (new)

**O:** No `is_blocking` field exists today. Dual-run health `"blocked"` is an ops gate, not a per-request UX decision.  
**E:** Consumer unavailable reasons and field-level `*_unavailable` codes exist on guidance.  
**C:** EP-002.5 defines **blocking** codes that force legacy fallback:

| Blocking | Rationale |
|---|---|
| `twin_foundation_flag_off` | Twin path not authorised |
| `canonical_learner_state_unavailable` | No honest Twin grounding |
| `invalid_student_id` | Invalid request |
| Both focus + next-action absent / both field-unavailable | No actionable student guidance |

Non-blocking honesty codes (e.g. `sparse_evidence`, single-field unavailable when another actionable field remains) may still serve Twin projection with limitation speech preserved in row metadata.

---

## 8. Cutover insertion point

| Option | Verdict |
|---|---|
| Change `generate_recommendations` return to Twin | **Reject** — blast radius includes bridges / Founder / dual-run callers |
| Dashboard route only with inline Twin call | Incomplete / duplicates eligibility; harder to test |
| **New dashboard projection API + `consumer_chain` cutover module** | **Selected** — mirrors EI compose-or-None + fail-open idiom; keeps legacy method intact |

Pattern precedent: `EducationalDashboardComposer` gated by flag, returns `None` → route falls back to legacy.

---

## 9. Risk findings (discovery)

| ID | Risk | Mitigation direction |
|---|---|---|
| D-R1 | Accidental production cutover | Env gate excludes production; cutover flag default OFF |
| D-R2 | Double Twin assemble (dual-run + cutover) | Skip dual-run when cutover flag eligible |
| D-R3 | Template break from shape change | Project to `list[dict]` |
| D-R4 | Bridge inherits Twin payload | Do not cut over inside `generate_recommendations` |
| D-R5 | Fingerprint used as quality gate | Use topical alignment instead |
| D-R6 | Explainability overwrites Twin copy | Skip enrich for `source_authority=study_insights` |

---

## 10. Discovery conclusions

| Question | Answer |
|---|---|
| Where to cut over? | Dashboard/home recommendation path via new service method |
| What do eligible students receive? | Projected Study Insights rows |
| What do others receive? | Legacy `generate_recommendations` |
| Gate? | Twin ON ∧ Cutover ON ∧ non-prod ∧ Twin success ∧ no blocking limitation |
| New flag? | **Yes** — `KWALITEC_STUDY_INSIGHTS_CUTOVER` |
| Schema? | None |
| Ready to implement? | **Yes** — after Cutover Design, Eligibility Matrix, Rollback Plan, Risk Assessment |

---

## 11. Implementation authorisation

**Observation:** Prerequisites EP-002.1–4 are complete; gap is gated HTTP projection with fail-open + alignment.  
**Evidence:** This discovery + programme WS4 + EP-002.4 recommendation.  
**Conclusion:** Implementation of gated Study Insights HTTP cutover is authorised under documented constraints.  
**Recommendation:** Proceed per [`CUTOVER_DESIGN.md`](CUTOVER_DESIGN.md); no production-wide activation.
