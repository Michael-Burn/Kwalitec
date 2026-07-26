# EP-003.2 — Readiness Gap Analysis

**Programme:** EP-003.2 — Readiness Intelligence Enhancement  
**Date:** 2026-07-26  

---

## 1. Evaluation dimensions

| Dimension | Pre-EP-003.2 state | Gap | EP-003.2 treatment |
|---|---|---|---|
| Evidence sources | Composite components implicit; Twin drivers internal | Student-facing evidence list missing on legacy | Explicit `supporting_evidence` from components + weak areas + drivers |
| Confidence calculation | Twin: internal bands; Legacy: none | Not student-safe; unexplained | Map to P-001.2 labels; density heuristics |
| Uncertainty handling | EIP-003 cold-start refusal on presentation only | Inconsistent Twin/legacy | Service-level honest refusal schema |
| Readiness drivers | Twin only | Legacy empty drivers | Synthesise coverage / knowledge / review / evidence drivers |
| Calibration logic | Fixed 50·30·20; dual-run ±10 | Unexplained weight meaning | Surface weight notes in driver rationales (no silent reweight) |
| Explanation quality | Presentation re-narration | No mandatory schema at service | P-001.2 schema on surface + assessment |

---

## 2. Identified defects

### Missing evidence
- Legacy surface returned empty `readiness_drivers` / `explainability`.
- Twin driver `rationale` / `source` stripped by `_driver_evidence` to id+value only.

### Duplicated reasoning
- EIP-003 composite speech + Twin adapter speech + coverage narrative — three voices.
- 50·30·20 recomposed in ORM getter and CLS consumer (acceptable duality; student schema now cites same components).

### Weak calibration
- Internal `very_low`…`high` not mapped to student-safe honesty labels.
- Influence thresholds (70 / 40) undocumented to students.

### Unexplained score changes
- No delta / change_drivers on Runtime A path.

### Educational-value opportunities
- One primary next action tied to Mission or planner slot.
- Change reasoning from supportive vs risk-elevating drivers.
- Presentation pass-through restores single communication owner.

---

## 3. Non-gaps (intentionally preserved)

| Item | Why preserved |
|---|---|
| `get_overall_readiness` bare dict | Collector recursion safety |
| Coverage vs Estimated readiness separation | EIP / educational honesty |
| Structural domain `ReadinessAggregation` | Parallel Stage A coexistence; no hybrid formula |
| Cutover / dual-run flags | EP-002.6 governance |
