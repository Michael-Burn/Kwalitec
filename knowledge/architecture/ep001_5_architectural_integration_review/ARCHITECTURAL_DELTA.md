# EP-001.5 — Architectural Delta

**Milestone:** EP-001.5  
**Date:** 2026-07-26

Compares the learning architecture **before EP-001** (post MS-004 T0–T6) vs **after EP-001.1–4**.

---

## 1. Dependency graph — before

```
Curriculum → Runtime A writes
                ↓
         Runtime A services (planning / readiness / recommendations)
                ↓
              HTTP / Experience
                ↑
MS-004 Twin (facets / snapshot / explain / TwinInput / projection / shadow)
  — parallel optional enrichment; not canonical learner-state consumer API for planning/readiness/insight
```

**Characteristics:**
- Twin existed as MS-004 enrichment + Experience projection port
- Planning / readiness / recommendations each read ORM / AdaptiveLearning directly
- No shared CanonicalLearnerState contract across those three domains
- Experience UX TwinPort = ExperienceTwinAdapter (demo-capable)

---

## 2. Dependency graph — after EP-001.1–4

```
Curriculum → Runtime A writes
                ↓
         MS-004 collectors / evidence
                ↓
         EP-001.1 CanonicalLearnerState  ←── optional Authority → Experience TwinPort
                ↓
         ┌──────┼──────────────┐
         ↓      ↓              ↓
      EP-001.2 EP-001.3     (direct)
      Planner  Readiness
         ↓      ↓
         └──→ EP-001.4 Insight
                ↓
         Runtime A build_* APIs (flag-gated)
                ╎
                ╎ (not yet wired)
                ↓
         HTTP still on legacy Runtime A APIs
```

**Characteristics:**
- Clear consumer chain with ownership boundaries
- Twin Foundation is the learner-state SoT for new APIs
- Legacy paths preserved for fail-open and collectors
- Experience Authority optional

---

## 3. What changed

| Area | Before | After |
|---|---|---|
| Learner-state consumer API | Implicit / fragmented | `CanonicalLearnerState` |
| Planner Twin consumption | None (direct ORM) | `build_daily_study_plan` |
| Readiness Twin consumption | Collectors only (pass-through) | `build_readiness_intelligence` |
| Recommendation Twin consumption | None as integrated chain | `build_study_insights` |
| Experience TwinPort | ExperienceTwinAdapter only | + Foundation Authority option |
| Flags | Twin (+ docs for Shadow/Adaptive) | Twin + Authority |
| LOC added (EP-001 packages approx.) | — | ~4.2k lines across foundation/authority + three consumer packages |

---

## 4. What did not change

- Runtime A remains transactional write SoT
- Curriculum remains syllabus SoT
- Legacy HTTP routes and formulas
- V1/V2 curriculum traversal
- No Alembic / schema
- Epic / V2 / EOS Twin stacks still present
- MS-004 T7 Twin Ready not declared

---

## 5. Complexity delta

| Dimension | Delta | Notes |
|---|---|---|
| Conceptual ownership clarity | **Improved** | Explicit SoT per concern |
| Code surface area | **Increased** | New packages + dual APIs |
| Runtime paths in production (default) | **Unchanged** | Twin OFF |
| Operator cognitive load | **Slightly increased** | More flags/docs; defaults safe |
| Risk of inventing learner state in consumers | **Decreased** | Projection contracts + unavailable honesty |

**C:** EP-001 **increased local structural complexity** in exchange for **decreased ambiguity** and safer future cutover. Net architectural quality improved; net operational simplicity maintained under defaults.

---

## 6. Constitutional posture delta

| Invariant | Before | After |
|---|---|---|
| No fabricated mastery/mocks | MS-004 rule | Preserved through EP-001 consumers |
| No fourth Twin stack | Risk | Preserved (extended MS-004) |
| Communication does not invent evaluation | Informal | EP-001.4 explicit |
| Planning does not own learner state | Informal | EP-001.2 explicit |
