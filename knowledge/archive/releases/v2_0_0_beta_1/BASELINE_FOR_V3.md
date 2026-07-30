# BASELINE FOR V3 — Comparison Measurements

**Baseline release:** Kwalitec `2.0.0-beta.1` (Private Beta)  
**Purpose:** Objective measurements future releases (including any Version 3 line) should compare against.  
**Rule:** Define what to measure — not targets that invent unproven success. Where beta.1 evidence is empty or unknown, record **baseline = not yet measured** honestly.

---

## 1. Performance

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Health endpoints | `/health`, `/health/live`, `/health/ready` → 200 / ok (RC-001) | Same endpoints must remain healthy under load |
| DB latency (prod smoke) | ~3 ms connected (RC-001 environment review) | Track p50/p95 query and health DB check |
| Static assets | Fingerprinted CSS with long cache; large static = 3 branding PNGs >500KB (non-blocking) | Bundle size, LCP, static count |
| Lighthouse / lab scores | **Not measured** on production in UX-001 | Attach lab scores for Home, Session, Journey, Tutor, KG |
| Deploy cutover | Brief connection reset during Render swap; recovered | Downtime duration per release |

---

## 2. Mission completion

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Cohort mission start rate | 0% (PB-001 empty cohort) | % of enrolled users starting ≥1 mission |
| Session completion rate | 0% (PB-001) | % completing ≥1 study session |
| Avg missions / user | 0.0 | Mean missions started & completed |
| Certified mission provenance | EI-002B stamps certified LO selection on `MISSION_GENERATED` | Regressions if missions lose certified node IDs |

---

## 3. Tutor adoption

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Tutor usage (cohort) | Insufficient evidence (PB-001) | % users opening Tutor; messages / user |
| Grounding integrity | Certified context filter rejects foreign IDs (EI-002B) | Rate of ungrounded / rejected contexts |
| Tutor surface availability | Route smoke 200 on production (RC-001) | Uptime / error rate on `/student/tutor` |

---

## 4. Knowledge Map usage

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| KG usage (cohort) | Insufficient evidence (PB-001) | % users opening Knowledge Map; expand depth |
| Graph source | Package structure parent_of / requires / LO relations | Structural drift vs certified package |
| Route availability | Smoke 200 (RC-001) | Error rate on `/student/knowledge_graph` |

---

## 5. Retention

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Daily return rate | 0.0% (PB-001) | D1 / D7 return |
| Weekly active users | 0 | WAU / enrolled |
| Return within one week (gate) | 0% vs 70% threshold (FAIL — empty cohort) | Same gate once cohort ≥ target size |

---

## 6. Learning outcomes

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Validated learning-outcome efficacy | **Not established** at beta.1 (no cohort) | Pre/post mastery, exam outcomes, LO mastery deltas — only with evidence |
| Certified hierarchy (CS1) | 5 chapters · 15 topics · 73 LOs active after RR-001 | Structure stability / certification status of active package |
| Certification authority | `certified_snapshot` on active publish path (RR-001) | Must not silently fall back to uncertified noisy extracts |

---

## 7. Architecture stability

| Measure | Beta.1 baseline | How to compare later |
|---|---|---|
| Layering invariant | Blueprints → services → engine/models (ARCHITECTURE.md) | No domain math leaking into routes |
| Curriculum V1/V2 loadability | Both formats supported | Both remain loadable |
| Alembic head | `202607300005` | Forward-only additive preference; document breaks |
| Sole student runtime | EOS under V2 flags | Dual-runtime regressions |
| Version identity | `2.0.0-beta.1` in `VERSION`, pyproject, `/health`, login chrome | Semver / changelog discipline |
| Feature-freeze scope (RC-001) | No new educational architecture in release packaging | Distinguish archive baseline from later intentional architecture change |

---

## 8. Operational / product gates (reference thresholds from PB-001)

These were **definitional gates** for Private Beta validation — not achieved at empty cohort:

| Gate | Threshold | Beta.1 actual |
|---|---:|---:|
| Create study plans | 90% | 0% |
| Start a mission | 90% | 0% |
| Complete a study session | 80% | 0% |
| Return within one week | 70% | 0% |
| Critical bugs | ≤5 | 0 |

Future releases should report the same columns.

---

## 9. Comparison protocol (suggested)

For any later tagged release `vX`:

1. Diff architecture invariants vs `architecture/ARCHITECTURE_AT_V2.md`.  
2. Diff Alembic head and table count vs `metrics/VERSION_STATISTICS.md`.  
3. Re-run Private Beta metrics with identical definitions vs PB-001.  
4. Confirm active published curricula remain certified-authority where claimed.  
5. Attach performance lab numbers that beta.1 lacked.  
6. Record whether known limitations from `KNOWN_LIMITATIONS.md` closed, persisted, or worsened — without rewriting that file.

---

*AR-001 objective baseline for future comparison.*
