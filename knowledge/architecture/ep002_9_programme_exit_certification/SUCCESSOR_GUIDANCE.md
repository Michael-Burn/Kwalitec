# EP-002.9 — Successor Guidance

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26  
**Baseline:** [`AUTHORITATIVE_ARCHITECTURE_BASELINE.md`](AUTHORITATIVE_ARCHITECTURE_BASELINE.md)

---

## 1. Starting constraint

All successor work begins from the post-EP-002 authoritative architecture baseline. Do not reopen EP-001.1–4 ownership unless a superseding constitutional review and ADR require it.

---

## 2. Recommended successor tracks

| Track | Intent | Depends on | Must not |
|---|---|---|---|
| **S1 — Controlled Pilot Ops** | Staging soak pack, Foundation P95, alerting, rollback ownership | EP-002.9 Ready for Controlled Pilot | Change ownership; remove hard gates casually |
| **S2 — Production Go/No-Go** | Decide Limited Production eligibility (code + ops) | S1 evidence | Infer readiness from EP-002 exit alone |
| **S3 — Twin Ready (T7)** | Dedicated MS-004 T7 certification | `DIGITAL_TWIN_READINESS_REPORT` checklist | Treat EP-002 HTTP cutover as T7 |
| **S4 — Experience Narrator Consolidation** | `/student` ExplanationService under SOLE_RUNTIME | Product SOLE_RUNTIME decision | Invent a third Runtime A narrator |
| **S5 — EI Stage A Disposition** | Retire or formally co-govern Stage A card vs Insight | Product EI roadmap | Break mutual exclusion without replacement |
| **S6 — Daily Plan Alignment** | Resolve display vs ORM session topic (`TD-DP-01`) | Constitutional review if persistence changes | Twin ORM writes without ownership rewrite |
| **S7 — Effectiveness Measurement** | Product EP-001 / EP-003 / private beta measure guidance | Live Twin-served surfaces | Claim scientific validity from architecture |
| **S8 — Debt Burn-down** | Durable metrics; MissionOptimizer delete; heuristic alignment | S1 monitoring | Drive deletes that remove fail-open prematurely |

---

## 3. Governance rules for successors

1. Cite EP-002.9 baseline path in programme briefs.  
2. Keep production Twin / Authority / Cutover OFF until S2 explicitly authorises otherwise.  
3. Preserve collector-safe legacy readiness getters until an explicit collector refactor.  
4. Preserve MissionOptimizer quarantine until hard-delete milestone.  
5. Prefer extending `consumer_chain` + `presentation/intelligence_surface` over new parallel stacks.  
6. Separate **student-surface activation**, **Experience TwinPort Authority**, and **Twin Ready (T7)** in every go/no-go.  
7. Disambiguate **EP-002 Student Intelligence Surface** from **EP-002 Analytics** by full title.

---

## 4. Suggested first successor milestone

**Controlled Pilot Ops Pack (S1)**

In scope:

- Live staging evidence archive for Insights / Readiness / Daily Plan cutovers  
- Foundation assemble P95 under real collectors  
- Fallback-rate and limitation-code dashboards (durable)  
- Named rollback drill with incident notes  
- Explicit pilot cohort definition  

Out of scope:

- Production hard-gate removal  
- T7 declaration  
- EP-001 redesign  
- Experience `/student` rewrite  

Exit criteria:

- Staging pack archived  
- Rollback drill recorded  
- Go/no-go recommendation for Limited Production **or** explicit hold  

---

## 5. Handoff map

| Consumer | What they inherit |
|---|---|
| Architecture governance | Authoritative baseline + certifications |
| Runtime A / Experience engineering | Flag matrix, cutover modules, presentation facade |
| Ops / SRE | Rollback plans, soak harnesses, residual `TD-OPS-STAGING` |
| Product | Controlled Pilot recommendation; non-claims on effectiveness / GA / T7 |
| Private beta / measurement programmes | Gated surfaces capable of emitting real Twin guidance in non-prod |

---

## 6. Stop / start

**Stop:** Opening a redesign of EP-001 because EP-002 exited.  
**Stop:** Declaring Twin Ready (T7) from this handoff.  
**Start:** Controlled Pilot Ops Pack against the certified baseline.
