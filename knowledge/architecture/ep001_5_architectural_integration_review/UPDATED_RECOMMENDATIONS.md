# EP-001.5 — Updated Recommendations

**Milestone:** EP-001.5  
**Date:** 2026-07-26

These recommendations supersede open follow-ups scattered across EP-001.1–4 completion reports for **architectural next steps**. They do not authorise product redesign inside this milestone.

---

## Immediate (do not block EP-001 closure)

1. **Accept EP-001 as architecturally complete foundation** — consumer chain, ownership, and fail-open design meet constitutional intent.
2. **Keep Twin and Authority OFF in production** until soak evidence exists.
3. **Do not delete legacy HTTP paths** as part of “cleanup.”

---

## Near-term consolidation (next milestones)

| Order | Recommendation | Addresses |
|---|---|---|
| 1 | Add shadow/observability counters for `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` without UX change | TD-OPS-01 |
| 2 | Publish Twin-stack quarantine note: MS-004+Foundation = Runtime A product path; Epic = domain vocab; V2/EOS = non-authority | TD-ARCH-01 |
| 3 | Align architecture docs: Shadow + Adaptive TwinInput bundled under `KWALITEC_DIGITAL_TWIN` | TD-ARCH-06 |
| 4 | Decide MissionOptimizer fate (wire or retire `generate_balanced_mission`) | TD-ARCH-03 |
| 5 | Inject shared Foundation from composition into Runtime A services | TD-ARCH-04, TD-OPS-03 |

---

## Cutover sequence (product-facing)

```
A. Twin ON in non-prod + shadow health green
B. Twin Authority ON in non-prod (Experience TwinPort) + demo-seed policy reviewed
C. Optional dual-run: dashboard renders legacy + logs Twin build_* side-by-side
D. HTTP cutover per surface (recommendations → readiness intelligence → mission plan)
E. Retire duplicate presentation path (EducationalExplainability vs Insight) only after D
F. Keep get_overall_readiness for collectors until collector refactor
```

---

## Explicit non-recommendations

- Do **not** merge Epic / V2 / EOS Twin into Foundation in one rewrite.
- Do **not** make Insight invent readiness or plans when Twin OFF.
- Do **not** put Foundation calls inside `get_overall_readiness`.
- Do **not** claim MS-004 T7 Twin Ready solely because EP-001.1–4 landed.
- Do **not** add per-domain flags for planner/readiness/insight unless independent rollout is proven necessary.

---

## Recommendation on EP-001 completeness

| Question | Recommendation |
|---|---|
| Is EP-001 architecturally complete as a constitutional implementation? | **Yes** |
| Is EP-001 ready as the foundation for future product capabilities? | **Yes**, with flag-gated consumption |
| Is EP-001 student-product complete? | **No** — cutover and presentation consolidation remain |
| Should a redesign of EP-001.1–4 be opened? | **No** — no justified architectural defect requiring redesign |

---

## Successor programme (authorised planning)

Near-term consolidation and cutover sequence above are programme-shaped under **EP-002 — Student Intelligence Surface** (planning workshop, 2026-07-26). First implementation milestone: **EP-002.1** (consumer-chain observability & quarantine). See [`../ep002_student_intelligence_surface/PROGRAMME_BRIEF.md`](../ep002_student_intelligence_surface/PROGRAMME_BRIEF.md).
