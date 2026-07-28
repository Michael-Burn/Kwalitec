# FV-001 — Founder Validation Log (Issue Register)

**Programme:** FV-001 — Founder Validation & Dogfooding  
**Operator:** Founder (student sole-runtime path)  
**Rule:** Record every issue encountered during daily usage. No hypotheticals.

**Issue count:** **0**  
**Last entry:** —

---

## How to use

1. When friction, defect, or educational inconsistency appears, copy the **Issue template** below.  
2. Fill every field from what actually happened (cite journal session id).  
3. Classify severity with the daily-use test in [`VALIDATION_PROTOCOL.md`](VALIDATION_PROTOCOL.md).  
4. If Critical/Major, also open a row in [`REAL_WORLD_BLOCKER_REGISTER.md`](REAL_WORLD_BLOCKER_REGISTER.md) and [`UX_DEFECT_REGISTER.md`](UX_DEFECT_REGISTER.md).  
5. Tag `workflow` with an id from `flask fv-metrics` / `workflows.py`.

---

## Issue template

```
### FV-I-NNN — short title

| Field | Value |
|---|---|
| **Identifier** | FV-I-NNN |
| **Date** | YYYY-MM-DD |
| **Workflow** | e.g. study_session / dashboard / revision_planner |
| **Severity** | Critical / Major / Minor / Constraint |
| **Reproducibility** | Always / Often / Once / Unknown |
| **Screenshots** | path or — |
| **Educational impact** | What learning consequence? |
| **Proposed resolution** | Grounded in this observation |
| **Status** | Open / Watching / Fixed / Accepted constraint |
| **Journal session** | Journal N / — |
| **UX category** | Functional / Educational / UX / Performance / Reliability |
| **CRI domains** | e.g. CR1, CR3 — or None |
```

---

## Issues

_No issues recorded yet. Do not invent defects to exercise this register._

<!-- First real issue starts below this line -->

---

**End of Founder Validation Log**
