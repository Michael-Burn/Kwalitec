# EP-002.6 — Architecture Discovery Report

**Milestone:** EP-002.6 — Readiness Intelligence Dual-Run & Gated HTTP Cutover  
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
| EP-002.1–5 Completion Reports | `knowledge/architecture/ep002_* /COMPLETION_REPORT.md` |
| `ReadinessService` | `app/services/readiness_service.py` |
| Readiness Intelligence adapters | `app/infrastructure/adapters/readiness_intelligence/` |
| Dashboard / analytics readiness surfaces | `app/dashboard/routes.py`, `app/analytics/routes.py` |
| Study Insights dual-run / cutover | `consumer_chain/dual_run.py`, `consumer_chain/cutover.py` |
| Consumer-chain telemetry | `app/infrastructure/adapters/consumer_chain/telemetry.py` |
| Feature flags | `app/application/config/v2_flags.py` |

---

## 2. Authority and product surface today

| Concern | Authoritative path | Twin / Intelligence path |
|---|---|---|
| Composite readiness score | `ReadinessService.get_overall_readiness` | `build_readiness_intelligence` (observability + soak only) |
| Weak / strong topics | `get_weakest_topics` / `get_strongest_topics` | `weakest_areas` / `strongest_areas` on assessment |
| Dashboard / Analytics HTTP | Direct legacy getters | **No dual-run / cutover** |
| Collectors / Adaptive TwinInput | Legacy getters only | Must remain legacy (recursion invariant) |
| Production defaults | Twin OFF / Cutover OFF | Intelligence unavailable to students |

**O:** EP-002 programme cutover order is recommendations → readiness → mission; WS5 selects readiness after Study Insights cutover.  
**E:** EP-002.5 exit recommends EP-002.6; Study Insights pattern is proven on dashboard recommendations.  
**C:** EP-002.6 may introduce dual-run + gated HTTP cutover for readiness under the same constitutional activation pattern.

---

## 3. ReadinessService entry points

| API | Role | Student influence (pre-EP-002.6) |
|---|---|---|
| `get_overall_readiness(user_id)` | Legacy composite score | **Yes — authoritative on dashboard/analytics** |
| `get_weakest_topics` / `get_strongest_topics` | Topic highlight lists | Yes |
| `get_review_backlog` / streaks / coverage | Adjacent readiness widgets | Yes (not intelligence cutover targets) |
| `calculate_readiness(curriculum)` | Syllabus-weight progress | Separate metric — out of intelligence cutover |
| `build_readiness_intelligence(user_id, …)` | EP-001.3 assessment | No student HTTP authority yet |

**O:** Dashboard and analytics call three primary getters for the readiness hero + topic lists.  
**E:** `dashboard/routes.py` (~150–168), `analytics/routes.py` (~34–49); templates expect `readiness.score`, coverage/mastery fields, and topic rows with `topic_id` / `topic_name` / `mastery_score`.  
**C:** Cutover must project intelligence into an existing surface DTO bundle (score + weak/strong lists) **or** change templates. Prefer projection.

**O:** `ReadinessCollector` and Adaptive TwinInput call `get_overall_readiness`.  
**C / R:** Cutover must **not** mutate `get_overall_readiness`. Host cutover in dashboard/analytics-facing service methods; leave legacy getters as collector-safe fail-open authority.

---

## 4. Study Insights inheritance (EP-002.4 / EP-002.5)

| Component | Behaviour | Implication for readiness |
|---|---|---|
| Dual-run eligibility | Twin ON ∧ non-prod | Reuse env gate; no dual-run flag |
| Cutover eligibility | Twin ON ∧ cutover flag ∧ non-prod | Add `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` |
| Fail-open | Twin None / exception / blocking → legacy | Copy verbatim |
| Semantic alignment | Topic overlap (not fingerprints) | Use readiness dimensions (score / confidence / limitations / areas) |
| Request-scoped cache | Today + list share one decision | Cache readiness surface bundle once per request |
| Skip dual-run when cutover active | Avoid double Twin assemble | Parallel readiness ContextVar |

**O / E:** EP-002.5 risk register explicitly deferred readiness cutover; collector recursion is the binding risk (R7 in programme brief).  
**C:** Dual-run + cutover modules live under `consumer_chain/`; hooks only on surface facades.

---

## 5. Feature flags

| Env | Flag | Default | Role |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | **Required** for Twin path |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF | Recorded; not required for Runtime A Foundation path |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | OFF | **New** — student-payload flip gate |
| `APP_ENV` / `FLASK_ENV` | — | development | Must not be `production` / `prod` |

**O:** Programme prefers cohort/env gates unless independent rollout is required.  
**E:** Study Insights required a dedicated cutover flag because HTTP payloads change.  
**C / R:** **Add** `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` (default OFF; requires Twin). Dual-run needs no new flag.

---

## 6. Payload shape (projection requirement)

| Dimension | Legacy HTTP | Twin Readiness Intelligence |
|---|---|---|
| Score | `readiness["score"]` | `readiness_score` + `confidence_level` |
| Drivers | Implicit in composite weights | `readiness_drivers[]` |
| Areas | Separate weak/strong list APIs | `weakest_areas` / `strongest_areas` with reasons |
| Unavailable | Zero/empty dicts | `None` when Twin OFF / CLS unavailable |
| Limitation codes | Not first-class | `limitations_codes` |
| Authority marker | none | `source_service: "readiness_intelligence"` |

**C:** Eligible HTTP responses must project Twin assessment into a legacy-compatible surface bundle so dashboard/analytics templates need no structural rewrite.  
**R:** Mark projected bundles with `source_authority="readiness_intelligence"`; skip EducationalExplainability re-narration when Twin owns communication (mirror Study Insights).

---

## 7. Surface scope

| Surface | In EP-002.6 scope? |
|---|---|
| `/dashboard` readiness score + weak/strong topics | **Yes** |
| `/analytics` readiness score + weak/strong topics | **Yes** |
| Review backlog / streaks / coverage widgets | No (adjacent; remain legacy) |
| `calculate_readiness` syllabus progress | No |
| `ReadinessCollector` / Adaptive TwinInput | **No — must stay on legacy getters** |
| Settings data export | No (ops baseline) |
| `/student` Experience home TwinPort | No (separate Experience path; not Runtime A ReadinessService) |
| Education OS `/eos/readiness/` | No |

---

## 8. Alignment design input

Fingerprint equality across legacy dict vs intelligence assessment will be rare (shape divergence — same as Study Insights).  
**R:** Dual-run records fingerprints + semantic readiness fields for ops. Cutover quality gate uses semantic dimensions:

| Dimension | Agreement rule |
|---|---|
| Readiness score | Absolute delta ≤ 10 points (or both absent/zero) |
| Confidence | Twin confidence present when score served |
| Limitations | Blocking codes drive limitation_fallback status |
| Areas | Topic-id overlap between legacy weak/strong and Twin areas |

---

## 9. Discovery conclusions

| Question | Answer |
|---|---|
| Is EP-001.3 ready for surface activation? | **Yes** — API + adapters + observability + soak exist |
| Insertion point? | New `get_dashboard_readiness_surface` / analytics alias + `consumer_chain/readiness_*.py` |
| New flag? | **Yes** — readiness cutover only |
| Collector risk? | Controlled by never wrapping `get_overall_readiness` |
| Production activation? | **No** |
| Implementation authorised? | **Yes** — after this discovery |

**R:** Proceed to cutover design + implementation mirroring EP-002.4/5 with readiness-specific projection and semantic alignment.
