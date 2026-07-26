# EP-002.3 — Rollback Plan

**Milestone:** EP-002.3 — Twin & Authority Non-Production Soak  
**Goal:** Demonstrate that Twin OFF → Authority OFF returns the system to the pre-soak state without behavioural regressions.

---

## 1. Rollback sequence (binding)

```
Twin ON (± Authority ON)   ← soak posture
        │
        ▼
KWALITEC_DIGITAL_TWIN=0    ← removes Foundation / build_* participation
        │                     (Authority auto-resolves OFF when Twin OFF)
        ▼
KWALITEC_DIGITAL_TWIN_AUTHORITY=0   ← explicit Authority OFF (belt-and-braces)
        │
        ▼
Pre-soak state: ExperienceTwinAdapter UX TwinPort;
build_* return None / unavailable; legacy HTTP unchanged
```

**Note:** Flag resolver already ANDs Authority with Twin. Setting Twin OFF alone clears Authority. Explicit Authority OFF documents operator intent and matches programme language.

---

## 2. What “pre-soak” means

| Concern | Pre-soak expectation |
|---|---|
| `ENABLE_DIGITAL_TWIN` | False |
| `ENABLE_DIGITAL_TWIN_AUTHORITY` | False |
| Experience `StudentTwinPort` | `ExperienceTwinAdapter` |
| Twin DI (facet / snapshot / shadow / Foundation) | Absent from composition |
| `build_*` | Return `None` when Twin unavailable |
| HTTP routes / templates | Unchanged |
| Adaptive flags | Unchanged by Twin rollback |
| Schema / data | Unchanged (no migrations; no Twin writes) |

---

## 3. Verification steps

1. Build Experience composition with Twin ON + Authority ON (soak peak).  
2. Confirm TwinPort is Foundation Authority (or fail-open fallback path available).  
3. Flip Twin OFF; rebuild composition.  
4. Confirm Twin DI removed; TwinPort is ExperienceTwinAdapter; `build_*` unavailable.  
5. Flip Authority OFF (with Twin OFF); rebuild.  
6. Confirm flags match cell A; Adaptive flags independent.  
7. Spot-check legacy Runtime A service construction still succeeds.  
8. Record `rollback_success=True` only if all checks pass.

Automated by `verify_twin_authority_soak_rollback()` in `consumer_chain.soak_rollback`.

---

## 4. Emergency (non-prod ops)

| Symptom | Action |
|---|---|
| Unexpected Authority behaviour in staging | Set `KWALITEC_DIGITAL_TWIN=0` immediately |
| Confused TwinPort summaries | Confirm Authority OFF; ExperienceTwinAdapter resumes |
| Soak harness noise | Disable soak runners; telemetry is observational only |

Production: flags must never have been ON for this milestone. If accidentally set, same Twin OFF kill switch applies.

---

## 5. What rollback does **not** require

- Database restore  
- Schema reverse migration  
- Code redeploy beyond flag env (flags are process env)  
- Clearing student educational facts (Twin / Authority do not write Runtime A)

---

## 6. Success definition

**Observation:** Rollback is flag-driven fail-open.  
**Evidence:** Soak rollback verifier returns `ok=True`; regression tests for Twin OFF `build_*` → `None` remain green.  
**Conclusion:** System returns to pre-soak posture without behavioural regressions attributable to this soak.  
**Recommendation:** Treat rollback drill as mandatory exit gate for EP-002.3.
