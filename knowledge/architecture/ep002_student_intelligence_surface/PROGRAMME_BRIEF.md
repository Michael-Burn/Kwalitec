# EP-002 — Programme Brief

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone of this artefact:** Planning Workshop (no implementation)  
**Date:** 2026-07-26  
**Based on:** EP-001.5 Architectural Integration Review (accepted foundation)

---

## 1. EP-002 Vision

Kwalitec’s EP-001 programme delivered a coherent constitutional intelligence backbone:

```
Runtime A facts → CanonicalLearnerState (EP-001.1)
  → Adaptive Study Planner (EP-001.2)
  → Readiness Intelligence (EP-001.3)
  → Insight & Recommendation Layer (EP-001.4)
```

Under production defaults, that chain is **architecturally real and student-invisible**. Legacy HTTP still owns the student’s day (`generate_today_mission`, `get_overall_readiness`, `generate_recommendations`). Twin and Authority flags remain OFF.

**EP-002 vision:** turn that backbone into the student’s primary, explainable daily intelligence surface — so that what the student sees for “what should I do today, and why?” is projected from the same owned chain EP-001 already built — through **safe observation → dual-run → per-surface cutover**, not through a parallel planner, readiness brain, or recommender.

EP-002 is a **surface activation and consolidation programme**, not a redesign of EP-001.1–4.

### What “done” looks like for the programme

A student on Runtime A dashboard / mission / readiness surfaces receives:

1. **Today’s focus** and **next action** from Twin-gated planning + insight composition  
2. **Readiness context** and drivers from readiness intelligence (not a reinvented score)  
3. **Honest unavailable / limitation speech** when evidence is sparse (constitutional honesty preserved)  
4. **Traceable “why”** that cites planner / readiness / Foundation evidence — not opaque scores  

…while curriculum, Runtime A writes, V1/V2 traversal, and fail-open rollback remain intact.

---

## 2. Objectives

| ID | Objective | Success signal |
|---|---|---|
| O1 | Activate EP-001 consumer outputs on student-facing Runtime A surfaces without redesigning EP-001.1–4 | HTTP paths call Twin-gated `build_*` under gated rollout; legacy retained until proven |
| O2 | Preserve constitutional ownership | Twin owns learner-state read model; Planner owns plans; Readiness owns evaluation; Insight owns communication only |
| O3 | Make the consumer chain operationally observable before UX authority flips | Live counters / dual-run logs for `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` |
| O4 | Complete Twin / Authority soak prerequisites for Experience cutover | Non-prod Twin ON + Authority soak green; production remains fail-open until evidence |
| O5 | Collapse dual presentation without inventing a third narrator | Sequenced retirement of duplicate Insight vs `EducationalExplainabilityService` paths after cutover |
| O6 | Avoid duplicate architectures | No fourth Twin stack; no new planning/readiness/recommendation engines; extend MS-004 + Runtime A services only |

### Explicit non-objectives

- Redesign of EP-001.1–4 contracts or ownership  
- Merging Epic / V2 / EOS Twin into Foundation in one rewrite  
- Declaring MS-004 Twin Ready (T7) solely because EP-002 starts  
- Analytics platform work (owned by **EP-002 Analytics** — separate programme)  
- New educational write authorities or schema inventing mastery  
- Per-domain planner/readiness/insight feature flags unless independent rollout is proven necessary  

---

## 3. Highest-value student capability

### Candidates evaluated

| Capability | Builds on | Student impact | Dependency / risk | Verdict |
|---|---|---|---|---|
| **A. Explainable daily study guidance** (insights: focus, risk, next action, why) | EP-001.4 (+ 1.2/1.3) | Highest — answers “what now / why?” on every study day | Needs observability + dual-run; presentation dual-path debt | **Selected** |
| B. Twin-grounded daily mission / plan cutover | EP-001.2 | High — changes what the student is asked to do | Touches mission start / dashboard; MissionOptimizer orphan; higher blast radius | Second wave |
| C. Readiness intelligence on analytics / home surfaces | EP-001.3 | Medium–high — clarifies “am I ready?” | Collectors must keep legacy getters; recursion risk if mishandled | Parallel to A after dual-run; cutover after insights |
| D. Experience TwinPort Authority (Foundation as UX Twin) | EP-001.1 Authority | Medium — improves TwinPort fidelity for Experience | Requires soak; demo-seed policy; not the primary daily CTA | Prerequisite track, not the headline capability |
| E. New Twin facets / metric expansion | Product Twin V2 design | Speculative until cutover proves value | Violates “no speculative features” if done before surface proof | **Defer** to post-cutover product EP |

### Selection rationale

EP-001.5 states students do not see EP-001.2–4 outputs by default (**TD-PROD-01**) and recommends cutover order **recommendations → readiness → mission plan**. Insight is the communication apex: it already composes planner + readiness + Foundation without inventing evaluation or planning. Activating **explainable daily study guidance** therefore:

- maximises student-visible value per unit of architectural risk  
- exercises the full consumer chain under observation  
- creates the measurement surface needed for recommendation validation (product EP-001 WS4 / EP-003)  
- keeps ownership boundaries speakable in every UI string  

Mission-plan cutover (B) remains essential but is **higher blast radius** and should follow insight dual-run evidence.

---

## 4. Proposed workstreams

| WS | Name | Intent | Primary artefacts / surfaces | Depends on |
|---|---|---|---|---|
| **WS0** | Programme hygiene & quarantine | Twin-stack operator narrative; doc/code flag alignment; MissionOptimizer fate decision | Architecture notes; ADR-lite decision record | EP-001.5 debt register |
| **WS1** | Consumer-chain observability | Shadow/dual-run counters for `build_*` without UX authority change | Telemetry hooks on Runtime A `build_*`; dashboards/logs | Twin flag usable in non-prod |
| **WS2** | Foundation DI consolidation | Shared Foundation injection to cut nested re-assemble cost | Composition / service DI | WS1 (measure before/after) |
| **WS3** | Twin & Authority soak | Non-prod Twin ON → Authority ON; rollback drills; demo-seed policy | Soak health; Experience TwinPort | WS0 quarantine; MS-004 shadow health |
| **WS4** | Study Insights dual-run → cutover | Side-by-side legacy recommendations vs `build_study_insights`; then gated HTTP cutover on dashboard / home | `RecommendationService`, dashboard routes, templates | WS1, WS3 (non-prod proven) |
| **WS5** | Readiness intelligence surface | Dual-run then cutover readiness UI to `build_readiness_intelligence`; keep legacy getters for collectors | Analytics / readiness routes | WS4 started; collector invariant held |
| **WS6** | Daily plan / mission surface | Wire or retire MissionOptimizer; dual-run `build_daily_study_plan` vs `generate_today_mission`; gated cutover | Mission / planning routes | WS4–5 evidence; WS0 MissionOptimizer decision |
| **WS7** | Presentation consolidation | Retire duplicate EducationalExplainability vs Insight after WS4–6 stable | Explainability services / templates | WS4–6 cutover proven |
| **WS8** | Programme exit & handoff | Production readiness checklist; debt burn-down; handoff to effectiveness / private-beta measurement | Exit report | WS4–7 |

### Workstream ownership boundaries (binding)

| Concern | Owner during EP-002 | Must not |
|---|---|---|
| Learner-state read model | EP-001.1 Foundation / MS-004 | Invent mastery, mock performance, or a new Twin stack |
| Daily plan slots / workload | `PlanningService` + EP-001.2 | Let Insight or HTTP invent plans |
| Readiness score / drivers | `ReadinessService` + EP-001.3 | Wrap `get_overall_readiness` with intelligence (collector recursion) |
| Student guidance copy | `RecommendationService` + EP-001.4 | Invent evaluation or planning when Twin OFF |
| Runtime A writes | Existing SQL services | Write from Twin / insight / bridges |
| Curriculum order | `CurriculumService` | Duplicate traversal in cutover adapters |

---

## 5. Dependency map

```
EP-001.5 accept foundation
        │
        ▼
   ┌──────── WS0 Quarantine / MissionOptimizer decision
   │              │
   ▼              ▼
 WS1 Observability (build_* counters / dual-run logs)
   │              │
   ├──────────────┼──────────────► WS2 Shared Foundation DI
   │              │                      │
   ▼              ▼                      │
 WS3 Twin + Authority soak (non-prod) ◄──┘
   │
   ▼
 WS4 Insights dual-run → HTTP cutover   ◄── highest-value student path
   │
   ├──────────────► WS5 Readiness surface cutover
   │                      │
   └──────────────► WS6 Plan / mission surface cutover
                          │
                          ▼
                    WS7 Presentation consolidation
                          │
                          ▼
                    WS8 Programme exit / handoff
                          │
                          ▼
         Product measurement (EP-003 / private beta) can observe real guidance
```

### External dependencies

| Dependency | Relationship |
|---|---|
| MS-004 T0–T6 Twin substrate | Required substrate — extend, do not fork |
| Runtime A Planning / Readiness / Recommendation services | Host APIs for `build_*`; cutover targets |
| Experience TwinPort / Authority flag | WS3 gate for Experience fidelity |
| EP-002 Analytics (separate) | Orthogonal; may later emit recommendation events — does not block EP-002 Architecture WS1–4 |
| Product EP-001 / EP-003 validation frameworks | Consume EP-002 surfaces for effectiveness measurement; do not redefine Insight ownership |
| Collectors / Adaptive TwinInput | Must keep legacy readiness getters until explicit collector refactor (out of critical path) |

### Hard dependency integrity rules

1. Twin packages must not import planner / readiness / insight for authority.  
2. Insight must not invent readiness or plans when Twin OFF (limitation codes only).  
3. Do not put Foundation calls inside `get_overall_readiness`.  
4. Do not delete legacy HTTP paths as “cleanup” before dual-run proof.  
5. Do not add a fourth Twin stack for “better UX.”

---

## 6. Risks

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Premature HTTP cutover flips student UX to unproven `build_*` | Medium | High | Dual-run mandatory; per-surface flags or cohort gates; kill switch = Twin OFF |
| R2 | Premature Authority ON in production | Medium | High | Soak in non-prod; production Authority OFF until checklist |
| R3 | Operator / engineer confusion across Twin stacks during cutover | Medium | Medium | WS0 quarantine narrative; naming discipline |
| R4 | Nested Foundation assemble cost under insight composition | Medium | Medium | WS2 shared DI; measure via WS1 |
| R5 | Insight vs EducationalExplainability divergence confuses students | Medium | Medium | Dual-run comparison; WS7 only after WS4 stable |
| R6 | MissionOptimizer orphan causes plan/mission inconsistency | Medium | Medium | WS0 explicit wire-or-retire decision before WS6 |
| R7 | Accidental collector recursion via readiness intelligence | Low | High | Keep legacy getters for collectors; architecture tests |
| R8 | Programme ID collision with Analytics EP-002 | Medium | Low | Full titles in docs; separate directories |
| R9 | Scope creep into Twin facet expansion / Strategy / Adaptive authority | Medium | High | Non-objectives; milestone briefs forbid redesign |
| R10 | Treating EP-002 start as Twin Ready (T7) | Low | High | Explicit non-claim in every milestone report |

---

## 7. Success criteria

### Programme-level

| Criterion | Evidence |
|---|---|
| Students can receive EP-001.4 study insights on at least one primary Runtime A surface under gated rollout | Route + flag + dual-run report |
| Ownership matrix unchanged: Twin / Planner / Readiness / Insight / Curriculum / Runtime A writes | Authority check in exit report |
| No new Twin stack; no new planning/readiness/recommendation engine | Package inventory delta |
| Legacy paths remain until cutover proven; rollback = flags OFF | Rollback drill notes |
| Live observability exists for all three `build_*` APIs | Metrics / log samples |
| Dual presentation debt has an owned retirement path (completed or scheduled with criteria) | WS7 status |
| V1/V2 curriculum traversal untouched | N/A statement + no curriculum diffs |
| EP-001.1–4 not redesigned | Diff review against contracts |

### Student-impact criteria (capability A)

| Criterion | Evidence |
|---|---|
| Guidance answers focus / risk / next action / why without inventing scores | Sample payloads + UI copy review |
| Unavailable / limitation cases remain honest | Fixture tests + copy audit |
| Guidance is attributable to planner and/or readiness fields when present | Provenance / field mapping table |

### Exit ≠ claims we will not make

- Not Twin Ready (T7) by default  
- Not “recommendations scientifically validated” (needs product measurement programmes)  
- Not public launch readiness  

---

## 8. Implementation roadmap

| Phase | Milestones | Workstreams | Outcome | Approx. posture |
|---|---|---|---|---|
| **P0 — Plan** | This workshop | — | Programme authorised | Docs only |
| **P1 — See before change** | EP-002.1, EP-002.2 | WS0, WS1, WS2 | Observable chain; quarantine; cheaper assemble | Twin OFF in prod; ON in non-prod for observation |
| **P2 — Soak** | EP-002.3 | WS3 | Authority/Twin soak evidence | Non-prod Authority ON candidates |
| **P3 — Guidance live** | EP-002.4, EP-002.5 | WS4 | Insights dual-run then gated cutover | First student-visible EP-001 value |
| **P4 — Evaluation & plan surfaces** | EP-002.6, EP-002.7 | WS5, WS6 | Readiness + mission/plan cutover | Full daily intelligence surface |
| **P5 — Consolidate & exit** | EP-002.8, EP-002.9 | WS7, WS8 | Presentation debt burned; programme exit | Fail-open retained until GA decision |

### Suggested milestone breakdown

| Milestone | Title | Nature |
|---|---|---|
| **EP-002.1** | Consumer-chain observability + Twin quarantine note | Implementation (telemetry + docs); **no UX authority change** |
| **EP-002.2** | Shared Foundation DI + MissionOptimizer decision record | Implementation / decision |
| **EP-002.3** | Twin + Authority non-prod soak | Ops + evidence report |
| **EP-002.4** | Study Insights dual-run on dashboard / home | Implementation; legacy remains authoritative |
| **EP-002.5** | Study Insights gated HTTP cutover | Implementation; rollback drill |
| **EP-002.6** | Readiness intelligence dual-run → gated cutover | Implementation |
| **EP-002.7** | Daily plan / mission dual-run → gated cutover | Implementation |
| **EP-002.8** | Presentation path consolidation | Implementation |
| **EP-002.9** | Programme exit & production readiness assessment | Assurance |

Flags remain safe-by-default throughout; prefer cohort / env gates over permanent new per-domain flags unless dual-run proves independent rollout is required.

---

## 9. Recommended first milestone

### EP-002.1 — Consumer-chain observability & quarantine

**Why first**

1. EP-001.5’s top near-term recommendation and **TD-OPS-01**: no live HTTP observability of `build_*`.  
2. You cannot responsibly cut over the highest-value capability (insights) without seeing planner → readiness → insight behave in real environments.  
3. Zero student-facing authority change → lowest constitutional and product risk.  
4. Unlocks WS2 measurement and WS4 dual-run design.  
5. Quarantine narrative (**TD-ARCH-01**) reduces operator risk before any flag flips.

**In scope**

- Emit structured observability for `build_daily_study_plan`, `build_readiness_intelligence`, `build_study_insights` (success / None / limitation codes / latency) when Twin ON  
- Optional non-prod dual-run logger: legacy recommendation payload fingerprint vs insight payload fingerprint (log only)  
- Twin-stack quarantine note: MS-004+Foundation = Runtime A product path; Epic = domain vocab; V2/EOS = non-authority  
- Align Shadow / Adaptive TwinInput docs with bundled `KWALITEC_DIGITAL_TWIN` behaviour (**TD-ARCH-06**)  

**Out of scope**

- HTTP UX cutover  
- Authority ON in production  
- MissionOptimizer wiring  
- Redesign of EP-001 contracts  
- Analytics event catalogue changes (separate programme)

**Exit criteria for EP-002.1**

- Non-prod can demonstrate live `build_*` invocation metrics/logs  
- Quarantine note published under architecture knowledge  
- Production defaults still Twin OFF / legacy authoritative  
- No schema migrations; application changes limited to observability + docs  

**Then:** EP-002.2 (DI + MissionOptimizer decision) → EP-002.3 (soak) → EP-002.4 (insights dual-run).

---

## 10. Relationship to other programmes

| Programme | Relationship to EP-002 Student Intelligence Surface |
|---|---|
| Architecture EP-001.1–5 | Foundation — consume, do not reopen design |
| **EP-002 Analytics** | Parallel completed ops programme; naming collision only |
| Product EP-001 / EP-003 | Downstream measurement of guidance effectiveness once surfaces emit real insights |
| EP-004 Private beta | Benefits from EP-002.5+ gated guidance; does not replace cutover engineering |
| MS-003 / MS-005 / MS-006 | Do not absorb Adaptive / Strategy / Evidence authority into Insight cutover |

---

## 11. Planning workshop conclusion

| Question | Answer |
|---|---|
| Is EP-001 a suitable foundation? | **Yes** (EP-001.5) |
| Highest-value next student capability? | **Explainable daily study guidance** via Insight cutover |
| Programme shape? | Observation → soak → insights → readiness → plan/mission → consolidate |
| First implementation milestone? | **EP-002.1 — observability & quarantine** |
| Redesign EP-001? | **No** |
| Duplicate architectures allowed? | **No** |
