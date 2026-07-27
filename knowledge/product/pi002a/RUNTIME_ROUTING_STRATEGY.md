# PI-002A — Runtime Routing Strategy

**Programme:** PI-002A — Platform Integration: Founder → Student Bridge  
**Date:** 2026-07-27  

---

## Decision order

`RuntimeRoutingService.resolve(subject_code, category_code)` applies:

1. If `ENABLE_RUNTIME_C_ENROLMENT` is **false** → **Runtime A**  
   (`reason=runtime_c_enrolment_disabled`)
2. If no active published package → **Runtime A**  
   (`reason=no_active_published_package`)
3. If category is `Published` **or** subject is on
   `RUNTIME_C_SUBJECT_ALLOWLIST` → **Runtime C**  
   (`reason=published_category_selection` | `subject_allowlist`)
4. Otherwise → **Runtime A**  
   (`reason=legacy_catalogue_defaults_to_runtime_a`)

Runtime A remains the default for all legacy catalogue selections.

---

## Why this shape

| Risk | Mitigation |
|---|---|
| Publishing CS1 silently migrates live students | Legacy IFoA path stays Runtime A |
| Accidental Runtime C enrolment | Enrolment flag defaults OFF |
| Unclear which runtime owns a student | Immutable routing audit per enrolment |
| Progressive rollout of overlapping subjects | Optional allowlist without code change |

---

## Audit record

Each decision persists:

| Field | Meaning |
|---|---|
| `runtime_authority` | `json_bundled` or `published_curriculum` |
| `decision_reason` | Why that authority was chosen |
| `flags_json` | Snapshot of bridge flags at decision time |
| `enrolment_id` / `study_plan_id` | Link to Runtime C or Runtime A artefact |
| `published_package_id` | Active package when present |

---

## Coexistence with PI-001C

`RuntimeCoexistencePolicy` remains the **engine-level** check used by
`EducationalRuntimeEngineService`. Student-facing flag gating and catalogue
routing live in PI-002A (`platform_integration`). Direct engine enrolment
(tests / ops) is unchanged; the live wizard uses the bridge.
