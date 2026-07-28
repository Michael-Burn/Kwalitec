# RI-002 — Runtime Inventory

**Programme:** RI-002 — Educational Intelligence Adoption & Readiness  
**Date:** 2026-07-28  
**Machine-readable:** [`runtime_inventory.json`](runtime_inventory.json)  
**Code:** `app/application/runtime_integration/runtime_inventory.py`

---

## Classification legend

| Status | Meaning |
|--------|---------|
| `active` | Still used in production educational selection or forced-compat control |
| `deprecated` | Wired but superseded by Preferred Authority; retain Temporary compatibility |
| `removable` | Quarantined / out-of-path; safe to delete in a later programme |
| `blocked` | Path missing while catalogue expected it active — investigate |

---

## Inventory summary

| entry_id | Component | Category | Status | Blocks retirement |
|----------|-----------|----------|--------|-------------------|
| `rec-service` | RecommendationService | runtime_a_recommendation | active | Yes |
| `rec-bridge` | RecommendationAdapter | compatibility_adapter | deprecated | No |
| `planning-selection` | PlanningService educational slots | runtime_a_planning | active | Yes |
| `stage-a-decision` | Stage A DecisionEngine / Orchestrator | legacy_recommendation | deprecated | No |
| `mission-optimizer` | MissionOptimizer | legacy_recommendation | removable | No |
| `runtime-c` | Runtime C / PX-001 fork | compatibility_consumer | deprecated | No |
| `sdt-educational-reasoning` | SDT-002 educational_reasoning | legacy_recommendation | deprecated | No |
| `ap002-decision-generator` | AP-002 DecisionGenerator | legacy_recommendation | active | Yes |
| `eos-src-engines` | EOS src/ recommendation engines | out_of_scope | removable | No |
| `ris-adapters` | RI-001 surface adapters | compatibility_adapter | active | No |
| `enable-flag` | ENABLE_RUNTIME_INTEGRATION | compatibility_control | active | Yes |
| `dashboard-legacy-rec` | Dashboard RecommendationService calls | legacy_recommendation | deprecated | No |

Regenerate JSON:

```bash
python3 -c "
from app.application.runtime_integration.runtime_inventory import RuntimeInventoryService
import json
print(json.dumps(RuntimeInventoryService().to_json_dict(), indent=2))
"
```
