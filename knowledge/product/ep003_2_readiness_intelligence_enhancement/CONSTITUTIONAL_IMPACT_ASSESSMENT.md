# EP-003.2 — Constitutional Impact Assessment

**Programme:** EP-003.2 — Readiness Intelligence Enhancement  
**Date:** 2026-07-26  

---

## 1. Authority stack consulted

```
Vision 2030 (Final Test; honest readiness)
        ↓
Educational Constitution / EIP (truth honesty — not amended)
        ↓
Architecture Constitution + EP-002.9 ownership baseline
        ↓
P-001.2 Explainability Standard
        ↓
ReadinessService (Runtime A readiness evaluation authority)
        ↓
RuntimeAPresentationAdapter (presentation only)
```

---

## 2. Ownership impact matrix

| Concern | Pre-EP-003.2 owner | EP-003.2 change | Violation risk |
|---|---|---|---|
| Readiness score / composite maths | ReadinessService | **Unchanged** — quality does not recalculate score | None |
| Readiness drivers / confidence / schema | Split (assembler internal + presentation speech) | **Consolidated into ReadinessService** via `readiness_quality` | Low — intended |
| Daily plan / mission persistence | PlanningService | **None** — mission title read for next-action labelling only | Low — fail-open |
| Recommendation selection | RecommendationService | **None** | None |
| Presentation narrator selection | RuntimeAPresentationAdapter | Pass-through when schema complete | None — remains presentation-only |
| Collector `get_overall_readiness` | ReadinessService | **Unchanged** — no quality wrap | Critical invariant preserved |

---

## 3. Hard rules check (EP-002.9 §2)

| Hard rule | Status |
|---|---|
| Twin packages must not import planner/readiness/insight for authority | Unaffected |
| Readiness must not invent learner state | **Pass** — consumes existing score/drivers |
| Do not wrap `get_overall_readiness` with Foundation (collector recursion) | **Pass** — quality applies only to surface / intelligence packaging |
| Presentation must not invent evaluation or planning | **Pass** — adapter pass-through strengthened |
| Recommendation must not recalculate readiness | Unaffected |

---

## 4. STOP conditions evaluated

| STOP condition | Triggered? | Notes |
|---|---|---|
| Final Test = No | No | Evidence-backed, confidence-honest readiness helps professional judgement |
| Conflict with Educational / Architecture Constitution | No | Does not invent mastery or hybrid posture+% |
| Ownership reopened for EP-001 redesign | No | Communication enhancement of authorised readiness |
| Presentation becomes third educational brain | No | Schema moves *out* of presentation compensation |
| Quality module generates missions or tips | No | Labels / selects among existing planner actions only |

**Verdict:** Proceed — no constitutional ownership violation.

---

## 5. Residual constitutional notes

- Coverage narrative (`calculate_readiness`) remains a separate Learning Progress fact — not merged into Estimated readiness.
- Next-action copy may cite Today’s Mission without replacing Planning authority.
- Honest refusal prefers “cannot yet be estimated” over fabricated cold-start percentages.
