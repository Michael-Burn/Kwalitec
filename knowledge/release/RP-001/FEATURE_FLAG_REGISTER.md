# RP-001.1 — Feature Flag Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.1  
**Date:** 2026-07-28  
**Resolvers:** `app/application/config/v2_flags.py`, `internal_alpha.py`, `feature_flags.py`, `app/application/adaptive_assessment/feature_flags.py`, `app/infrastructure/analytics/feature_flag.py`, `app/application/platform_integration/flags.py`  
**Production source:** `render.yaml`

---

## Production-enabled flags (Render)

| Env var | Field / effect | Value | Student impact |
|---------|----------------|-------|----------------|
| `KWALITEC_V2_SOLE_RUNTIME` | `SOLE_RUNTIME` | `1` | Canonical home `/student/`; legacy homes redirect |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `ENABLE_STUDENT_EXPERIENCE` | `1` | `/student/*` active (also forced by sole) |
| `KWALITEC_V2_DURABLE_STORE` | `ENABLE_DURABLE_STORE` | `1` | Experience/Session SQL persistence |
| `KWALITEC_V2_INJECT_ENGINES` | `INJECT_PHASE_I_ENGINES` | `1` | Opaque engine bridges |
| `KWALITEC_V2_SEED_DEMO` | `SEED_DEMO_LEARNERS` | `0` | No demo seed |
| `KWALITEC_EI_INTERNAL_ALPHA` | EI orchestrator + recommendations | `1` | Twin-first recommendation path available to composers; EI missions/explainability/progress stay OFF |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | Founder console | `1` | **Not student-facing** |

---

## V2 / Experience flags (default OFF unless noted)

| Env var | Flag field | Default | Alpha posture | Student UX |
|---------|------------|---------|---------------|------------|
| `KWALITEC_V2_SOLE_RUNTIME` | `SOLE_RUNTIME` | OFF | **ON (prod)** | Home authority |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `ENABLE_STUDENT_EXPERIENCE` | OFF | **ON (prod)** | EOS surfaces |
| `KWALITEC_V2_DURABLE_STORE` | `ENABLE_DURABLE_STORE` | OFF | **ON (prod)** | Persistence |
| `KWALITEC_V2_INJECT_ENGINES` | `INJECT_PHASE_I_ENGINES` | OFF | **ON (prod)** | Bridges |
| `KWALITEC_V2_SEED_DEMO` | `SEED_DEMO_LEARNERS` | ON* | **OFF (prod)** | Demo data |
| `KWALITEC_MISSION_*_BRIDGE` / umbrella | Mission bridges | OFF | OFF unless env | Mission read/start/resume |
| `KWALITEC_JOURNEY_BRIDGE` | `ENABLE_JOURNEY_BRIDGE` | OFF | OFF | Journey port backing |
| `KWALITEC_HISTORY_BRIDGE` | `ENABLE_HISTORY_BRIDGE` | OFF | OFF | History port backing |
| `KWALITEC_ADAPTIVE_ENGINE` | `ENABLE_ADAPTIVE_ENGINE` | OFF | OFF | Adaptive construction |
| `KWALITEC_ADAPTIVE_ENGINE_SHADOW` | `ENABLE_ADAPTIVE_ENGINE_SHADOW` | OFF | OFF | Shadow compute |
| `KWALITEC_ADAPTIVE_AUTHORITY` | `ENABLE_ADAPTIVE_AUTHORITY` | OFF | OFF | Authoritative adaptive tips |
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | OFF | Twin DI / tutor dependency |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF | OFF | Twin as StudentTwinPort |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `ENABLE_STUDY_INSIGHTS_CUTOVER` | OFF | OFF | Twin insights on home/dashboard |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | OFF | OFF | Twin readiness cutover |
| `KWALITEC_DAILY_PLAN_CUTOVER` | `ENABLE_DAILY_PLAN_CUTOVER` | OFF | OFF | Twin daily plan cutover |
| `KWALITEC_UNIFIED_JOURNEY` | `ENABLE_UNIFIED_JOURNEY` | OFF | **OFF** | Journey-stage nav / guided day |
| `KWALITEC_EXPERIENCE_FEEDBACK` | `ENABLE_EXPERIENCE_FEEDBACK` | OFF | **OFF** | Home “Your Journey” facts |
| `KWALITEC_LEARNING_FEEDBACK` | `ENABLE_LEARNING_FEEDBACK` | OFF | OFF | Behavioural evidence recording |
| `KWALITEC_PERSONAL_LEARNING_PROFILE` | `ENABLE_PERSONAL_LEARNING_PROFILE` | OFF | OFF | Profile aggregation (no UI authority) |
| `KWALITEC_EVIDENCE_*` / advisory / recovery / simulation / trials | Various | OFF | OFF | Backend / advisory only |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | `ENABLE_FOUNDER_INTELLIGENCE` | OFF | ON (prod) | Founder only |

\* Default ON when durable store is OFF; when durable ON, seed defaults OFF unless env forces it.

---

## Educational Intelligence flags

| Control | Flags set | Default | Alpha posture |
|---------|-----------|---------|---------------|
| `FEATURE_FLAGS` singleton | All EI flags | All OFF | Overridden by internal alpha |
| `KWALITEC_EI_INTERNAL_ALPHA` | Orchestrator + Recommendations **ON**; Missions, Explainability, Progress **OFF** | OFF | **ON (prod)** |

Student note: under sole runtime, legacy dashboard EI card is redirected; Student Home uses Experience/MES paths. Internal Alpha still matters for Twin retrieval / composer wiring.

---

## Adaptive Assessment flags

| Env var | Flag | Default | Alpha posture | Student routes |
|---------|------|---------|---------------|----------------|
| `KWALITEC_ADAPTIVE_ASSESSMENT` | Master | OFF | **OFF** | Gates all |
| `KWALITEC_QUICK_CHECK` | Quick Check | OFF | **OFF** | `/adaptive-assessment/quick-check/*` |
| `KWALITEC_DEEP_CHECK` | Deep Check | OFF | OFF | **No routes** |
| `KWALITEC_RECOVERY_CHECK` | Recovery Check | OFF | OFF | **No routes** |
| `KWALITEC_CONFIDENCE_CHECK` | Confidence Check | OFF | OFF | **No routes** |
| `KWALITEC_READINESS_CHECK` | Readiness Check | OFF | OFF | **No routes** |
| `KWALITEC_CONTEXTUAL_FRAMING` | ILE-001C framing | OFF | **OFF** | Framing within Quick Check |
| `KWALITEC_ADAPTIVE_ASSESSMENT_SUBJECTS` | Subject allow-list | empty = all | unset | Opt-in filter when master ON |
| `KWALITEC_ADAPTIVE_ASSESSMENT_COHORTS` | Cohort allow-list | empty = none restricted | unset | Opt-in filter when master ON |

---

## Platform integration / Runtime C

| Env var | Default | Alpha posture | Student effect |
|---------|---------|---------------|----------------|
| `KWALITEC_FOUNDER_STUDENT_BRIDGE` | OFF | OFF | Umbrella |
| `KWALITEC_PUBLISHED_SUBJECT_DISCOVERY` | OFF | OFF | Published subjects in wizard |
| `KWALITEC_RUNTIME_C_ENROLMENT` | OFF | OFF | Runtime C Home/Journey projection |
| `KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST` | empty | unset | Subject routing |

---

## Analytics

| Env var | Default | Alpha posture | Student effect |
|---------|---------|---------------|----------------|
| `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1` | OFF | OFF | Passive event emit only — **no UI change** |

---

## Capabilities with no feature flag

Always available to authenticated students when routes are reachable:

- Authentication  
- Decision Journal (ILE-002)  
- Educational Timeline (ILE-003)  
- Daily Mission Intelligence panel (ILE-004) — visibility still needs a recommendation  
- Educational Feedback Loop reflection (ILE-005)  
- Mission commitment / deferral  
- Help / Alpha feedback / research check-in  
- Study Plan (core)  
- Standalone `/assessment`  
- EOS Profile / History / Journey / Revision pages (content richness may still depend on bridges)

---

## Alpha flag policy (certification)

1. **Do not change** production Render flags as part of RP-001.1 (inventory only).  
2. Any Alpha experiment that enables Quick Check, Unified Journey, Twin cutovers, or Runtime C **must** update this register and `ALPHA_PRODUCT_INVENTORY.md`.  
3. Sole-runtime OFF is a **rollback**, not an Alpha feature expansion — it re-exposes legacy homes (CAP-30 risk).  
4. `KWALITEC_EI_INTERNAL_ALPHA` must not be read as “all EI widgets ON” — missions/explainability/progress remain OFF by code.

---

## Related

- DEP-002 audit: `knowledge/product/dep002/FEATURE_FLAG_AUDIT.md`  
- Capability mapping: `CAPABILITY_MATRIX.md`  
- **Version 1 G12 matrix (EI-001.3):** `docs/production/VERSION_1_FLAG_MATRIX.md`
