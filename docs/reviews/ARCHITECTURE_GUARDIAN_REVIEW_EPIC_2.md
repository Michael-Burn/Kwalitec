# Architecture Guardian Review — Epic 2 Release

**Final decision:** APPROVED WITH CONDITIONS  
**Date:** 12 July 2026  
**Epic:** Epic 2 — Educational Intelligence  
**Release context:** v0.5.0  
**Review type:** Final architectural governance review before release — documentation only  
**Scope:** Repository as a whole (domain Educational Intelligence stack + product coexistence + governance artefacts)

**Upstream gates (all closed):**

| Artefact | Outcome |
|---|---|
| Recommendation Integrity Review | APPROVED WITH CONDITIONS |
| Mission Integrity Review | APPROVED WITH CONDITIONS |
| Epic 2 Completion Review | APPROVED WITH CONDITIONS |
| ADR-002 | Accepted |
| CHANGELOG v0.5.0 | Present |
| Technical Debt Register update | Active (post–Epic 2) |

**Governing decisions:**

- [`ADR-001-Curriculum-Hierarchy.md`](../architecture/ADR-001-Curriculum-Hierarchy.md) — Accepted  
- [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](../architecture/ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) — Accepted  
- [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](../architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
- [`ARCHITECTURE.md`](../../ARCHITECTURE.md)  
- [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md)

**Application / production code was not modified by this review. No tests. No migrations. STOP after this document.**

---

## Executive Summary

Epic 2 closes a coherent, framework-independent **structural Educational Intelligence architecture**. Learning Evidence evolves an immutable Student Digital Twin through registered Update Strategies; Readiness Aggregation, Decision Engine, Recommendation packaging, and Mission Intelligence form a disciplined read path that never writes beliefs. Domain ownership, write/read separation, explainability chain, Curriculum V1/V2 safety, and AST-enforced framework purity hold across `app/domain/`.

There is a **single educational authority inside the Twin-first domain stack** (Twin for state; Decision for next-action selection). There is **not** yet a single educational authority in the live product: Stage A dual truth remains — legacy `ReadinessService`, `RecommendationService`, and `PlanningService` / ORM missions still own student-facing behaviour, and no service layer currently imports `app.domain.*` Twin-first packages.

That dual truth is **named, documented, and non-hybrid**. It is an integration debt, not an architectural defect in the domain model. Unconditional release approval is therefore withheld; **APPROVED WITH CONDITIONS** is warranted for v0.5.0 as a domain Educational Intelligence release.

Governance maturity is high: ADR-001 and ADR-002 record the major decisions; integrity and completion reviews are consistent; CHANGELOG and Technical Debt Register align residual work with Epic 3 Product Integration. Residual risks are predominantly **integration and cutover**, not redesign of Educational Intelligence.

---

## Review Axes

### 1. Architectural layering

**PASS.**

Canonical stack:

```
Templates / JS
      ↓
Blueprints
      ↓
Services (orchestration / persistence / Stage A legacy peers)
      ↓
Domain: Evidence + Twin + Strategies + Readiness + Decision + Recommendation + Mission
      ↓
Models + Curriculum Engine
      ↓
DB / JSON
```

Domain packages under `app/domain/` (twin, evidence, readiness, decision, recommendation, mission) contain the Educational Intelligence cores. Spot-check: no Flask / SQLAlchemy / `app.services` imports in domain packages. Spot-check: no `app.services` modules currently import Twin-first domain engines — confirming Stage A coexistence rather than a layering breach.

**Gap (non-blocking for domain release):** Root [`ARCHITECTURE.md`](../../ARCHITECTURE.md) still describes the pre-domain service map and does not yet document `app/domain/` as the Educational Intelligence layer. Contributors must read ADR-002 / EI Architecture / Twin README to see the full picture.

### 2. Educational ownership

**PASS (domain); CONDITIONAL (product).**

| Concern | Owner (domain) | Does not own |
|---|---|---|
| Syllabus structure / weights | Curriculum Engine + `CurriculumService` | Twin / Decision |
| Learner educational state | Student Digital Twin | Plans, missions, HTTP |
| Belief evolution | Update Strategies via Pipeline | Readiness / Decision / Recommendation / Mission |
| Preparedness factors | Readiness Aggregation | Next-action selection |
| Highest-value next action | Decision Engine | Twin writes; mission packing |
| Packaging | Recommendation Engine | Re-ranking / second Decision |
| Session execution projection | Mission Intelligence | WeekPlan policy; filler; selection |

Anti-patterns (activity-as-mastery, completion-as-readiness, recommend/mission as second reasoners) are rejected in domain contracts and prior integrity reviews.

### 3. Domain boundaries

**PASS.**

Knowledge ≠ Memory ≠ Behaviour ≠ Performance. Readiness ≠ Decision. Recommendation ≠ Decision. Mission ≠ Decision ≠ Planning. Confidence remains incompletely separable (absorbed lineage under Knowledge) — tracked as intentional evolution debt (E2-EE-01), not a boundary collapse inside Recommendation/Mission.

### 4. Framework independence

**PASS.**

Educational Intelligence cores live in pure domain packages. Integrity reviews and Twin README document AST firewall tests across twin, readiness, decision, recommendation, and mission. Framework coupling is correctly deferred to future service orchestration adapters.

### 5. Twin write path integrity

**PASS (structural).**

```
Learning Evidence → Twin Update Pipeline → Strategies (K → M → B → P) → new Twin snapshot
```

Immutable aggregate; strategies return new snapshots; pipeline coordinates order and does not embed educational algorithms. Predictions slots exist; Prediction snapshot strategy and Confidence update path remain deferred by design.

**Residual:** No production Twin persistence / Evidence → pipeline service bridge (E2-PE-01). Write-path integrity holds in domain; production write loop is not live.

### 6. Read-side reasoning integrity

**PASS.**

```
Twin + Curriculum + Goals → ReadinessAggregation.derive(...)
      → DecisionEngine.evaluate(...)
      → RecommendationEngine.package(...)   (optional)
      → MissionIntelligence.compose(...)    (execution)
```

Read-side packages do not register Update Strategies or mutate belief domains. Recommendation Integrity and Mission Integrity reviews confirm no re-selection, no ranking invention, no filler under leftover capacity, and warrant inheritance with thin-warrant honesty.

### 7. Explainability chain

**PASS (structural).**

Mandatory chain:

```
Curriculum → Learning Evidence → Twin → Readiness → Decision → Recommendation → Mission
```

Decision reason codes, lineage, and warrant postures propagate into Recommendation and MissionTask attribution. Residual risk is presentation: structural tags are not yet bound to student-facing copy (E2-PX-03 / E2-PX-04).

### 8. Curriculum V1/V2 compatibility

**PASS.**

Domain contracts use format-aware `CurriculumContext` / Decision lineage. No global Section requirement. Epic 1 traversal invariants (`CurriculumService` helpers, `get_topics_flat`) remain the syllabus authority. Twin work does not fork syllabus trees. Wiring must continue to use canonical helpers — a cutover discipline, not a current domain failure.

### 9. Documentation consistency

**CONDITIONAL.**

| Artefact | Consistency |
|---|---|
| ADR-001 / ADR-002 | Aligned with shipped decisions |
| Epic 2 Completion + integrity reviews | Consistent narrative and conditions |
| CHANGELOG [0.5.0] | Accurately names Stage A limitations and Epic 3 next work |
| Technical Debt Register v0.5.0 | Aligned with roadmap (Epic 3 integration + evolution) |
| Twin README | Accurate call order and ownership |
| Educational Intelligence Architecture status table | **Drift** — still marks 2.5–2.10 as “Planned” while capabilities are shipped |
| Root `ARCHITECTURE.md` | **Drift** — omits `app/domain/` Educational Intelligence layer |

Documentation is sufficient for architectural understanding if contributors follow ADRs and reviews; status-table hygiene (E2-EN-01) remains a binding condition.

### 10. Governance maturity

**PASS (HIGH).**

Epic 2 followed Analysis → Architecture → Implementation → Review → Acceptance with midpoint and capability integrity gates. Charter principles (evidence before assumptions, architecture before implementation, trust before features) are reflected in ADR-002 and completion conditions. Debt is registered with priority, justification, and target Epic. This is a mature governance posture for a commercial educational product.

### 11. Risk of architectural drift

**MEDIUM (managed) — primarily at integration boundaries.**

Drift vectors to watch in Epic 3:

1. Deepening legacy readiness / recommendation / mission heuristics as Twin-first truth  
2. Hybrid averages (legacy % + Twin factors)  
3. Orchestration inventing a second coordinator or divergent strategy order  
4. UI stripping warrant / inventing Mid–High theatre  
5. Belief engines smuggled into Readiness Aggregation  
6. LLM ownership of educational selection  
7. Conflating `domain.Mission` with ORM `models.Mission`  
8. Treating structural postures as finished calibrated scores  

Domain firewalls and ADR-002 principles mitigate these if Stage B/C conditions are enforced. Drift risk rises if Epic 3 bypasses thin orchestration and jumps to UI features.

### 12. Readiness for Epic 3

**YES — under binding conditions.**

Epic 3 is correctly framed as **Product Integration & Experience**, not Educational Intelligence redesign (ADR-002 § Epic 3 Implications). The domain stack is a sound foundation for:

- Thin orchestration adapters  
- Twin / Decision Journal / Evidence persistence  
- Stage B named dual-truth → Stage C product authority cutover  
- Warrant-bound student-facing copy  
- Confidence and calibrated enrichment *inside* existing owners  

Epic 3 must not reopen the Evidence → Twin → Readiness → Decision → Recommendation → Mission chain.

---

## Specific Questions

### Is there a single educational authority?

**In the Twin-first domain stack: Yes.**

- Educational state authority: Student Digital Twin (evolved only via Learning Evidence → Strategies).  
- Syllabus authority: Curriculum Engine / `CurriculumService` (unchanged from ADR-001).  
- Next-action selection authority: Decision Engine.  
- Recommendation and Mission are projections / operationalisations, not second authorities.

**In the live product: No — named Stage A dual truth.**

Student-facing readiness, recommendations, and daily missions still flow through legacy services. Domain engines are not yet product-wired (`app.services` does not import Twin-first domain packages). Dual truth is intentional progressive integration, not a hybrid merge. Claiming a single product educational authority for v0.5.0 would be false.

### Can future contributors understand the architecture?

**Yes, with a documented map and one hygiene caveat.**

A contributor can reconstruct the system from:

1. ADR-001 (curriculum) + ADR-002 (Educational Intelligence)  
2. Educational Intelligence Architecture + Twin README  
3. Capability integrity / completion reviews  
4. Package boundaries under `app/domain/`  

Cognitive load is higher than a monolithic recommender (accepted consequence in ADR-002). The main obstacle is status drift in `ARCHITECTURE.md` and EI Architecture capability tables — not missing design intent. Syncing those docs is a short hygiene task, not an architectural rewrite.

### Do ADR-001 and ADR-002 sufficiently explain major decisions?

**Yes.**

| ADR | Decision recorded | Sufficiency |
|---|---|---|
| **ADR-001** | Canonical V2 hierarchy alongside V1; automatic format detection; centralised traversal; additive schema | Sufficient foundation for syllabus truth and V1/V2 safety |
| **ADR-002** | Educational Intelligence as authoritative reasoning architecture; write/read split; layer ownership; rejected alternatives (monolith recommender, planner-first, LLM-first, embed-in-Flask-services); Epic 3 implications | Sufficient to bind Epic 2 close and Epic 3 integration without redesign |

Together they explain *why* Kwalitec separated syllabus truth from learner-state intelligence, and *why* domain purity precedes product cutover. They do not need to encode scoring formulas; structure-before-scoring is an explicit principle.

### Is the Technical Debt Register aligned with the roadmap?

**Yes.**

Post–Epic 2 register (v0.5.0) cleanly separates:

| Bucket | Alignment |
|---|---|
| Product Integration (E2-PI-*) | Epic 3 Stage B/C — dual truth, legacy services, orchestration |
| Persistence (E2-PE-*) | Epic 3 adapters / journals / Evidence loops |
| Educational Evolution (E2-EE-*) | Epic 3+ enrichment inside owners (Confidence, scoring, metrics) |
| Product Experience (E2-PX-*) | Epic 3 Stage C UI / warrant binding |
| Engineering (E2-EN-01 + TD-001–007) | Hygiene and pre-existing framework debt |

No Critical items. High residuals are integration and Confidence-before-risk-framing — matching CHANGELOG “Next Release” and ADR-002 Epic 3 Implications. The register does **not** invent architectural defects in the domain stack.

### Are remaining risks architectural or integration-related?

**Primarily integration-related.**

| Class | Examples | Severity |
|---|---|---|
| **Integration / cutover** | Stage A dual authority; missing orchestration; Twin persistence; Evidence/Decision journal loops; UI warrant binding | High (program) |
| **Educational evolution (intentional)** | Confidence ownership; calibrated readiness/decision enrichment; belief bags | Medium–High for product claims; not domain defects |
| **Architectural redesign** | None required for Epic 2 close | — |
| **Documentation hygiene** | EI status tables; root ARCHITECTURE.md domain layer omission | Medium (hygiene) |

There is no evidence that the Evidence → Twin → Readiness → Decision → Recommendation → Mission model is wrong. Remaining High risk is shipping Twin-first *claims* while legacy services still own product behaviour, or deepening those legacy heuristics during cutover.

---

## Strengths

1. **Complete structural Educational Intelligence pipeline** (capabilities 2.1–2.10) with clear ownership.  
2. **Write/read firewall** — Strategies write; Readiness / Decision / Recommendation / Mission read and project.  
3. **Decision as sole next-action selector** in the Twin-first stack; packaging and mission execution do not re-rank.  
4. **Explainability by construction** — mandatory chain with reason codes, lineage, and warrant postures.  
5. **Framework-independent domain layer** with enforceable purity boundaries.  
6. **Curriculum-first reasoning** preserving V1/V2 loadability and traversal.  
7. **Honest cold-start / thin-warrant posture** — no Mid/High theatre under sparse evidence in domain contracts.  
8. **Named Stage A coexistence without hybrid averages** — dual truth is documented rather than silently merged.  
9. **Governance artefacts of release quality** — ADRs, integrity reviews, completion review, CHANGELOG, debt register.  
10. **Clear Epic 3 charter** — integration, not redesign.

---

## Residual Risks

| ID | Risk | Class | Severity |
|---|---|---|---|
| AG-01 | Dual educational authority live in product (readiness / recommend / missions) | Integration | High |
| AG-02 | Premature product claim that Epic 2 shipped Twin-first intelligence to students | Program / communications | High |
| AG-03 | Missing production orchestration and Twin / Evidence persistence before live consumers | Integration | High |
| AG-04 | Deepening legacy heuristics during Stage A/B instead of freezing them | Integration / drift | High |
| AG-05 | Confidence collapsed into Knowledge lineage before calibrated risk framing | Educational evolution | Medium–High |
| AG-06 | Presentation strips warrant or invents preparedness theatre | Product experience | Medium |
| AG-07 | Documentation drift obscures shipped vs planned (`ARCHITECTURE.md`, EI status tables) | Hygiene | Medium |
| AG-08 | `domain.Mission` vs `models.Mission` conflation at adapters | Integration hygiene | Medium |
| AG-09 | Belief engines smuggled into Readiness or LLM ownership of selection | Architectural drift | Medium (controlled if conditions held) |
| AG-10 | Treating structural Twin postures as finished calibrated scores | Educational fidelity | Medium |

No residual risk requires rejecting the domain architecture for v0.5.0.

---

## Recommendations

1. **Ship v0.5.0 as a domain Educational Intelligence release** under the binding conditions below — do not market it as Twin-first student experience.  
2. **Open Epic 3 as Product Integration** per ADR-002: thin orchestration first, then Stage B adapters, then Stage C cutover.  
3. **Freeze deepening** of legacy `ReadinessService` / `RecommendationService` / `PlanningService` mission-generation heuristics as Twin-first truth.  
4. **Preserve Decision sole selection authority** across Recommendation packaging and Mission composition.  
5. **Preserve write/read firewall** at every adapter; accept/dismiss and completion become Learning Evidence only.  
6. **Bind student-facing copy** to chain-supported warrant and reason codes before claiming explainable product recommendations.  
7. **Schedule Confidence separability** before calibrated over/underconfidence product narratives.  
8. **Sync documentation hygiene** — update EI Architecture capability status and root `ARCHITECTURE.md` to include the domain Educational Intelligence layer.  
9. **Keep Curriculum V1/V2 helpers** as the only syllabus traversal path at wiring boundaries.  
10. **Do not reopen ADR-002** for Epic 3 feature work; deepen within owners.

---

## Final Decision

### APPROVED WITH CONDITIONS

**Justification:** Repository architecture for Epic 2 is sound. The structural Educational Intelligence stack is complete, layered, explainable, curriculum-safe, and framework-independent. Major decisions are recorded in ADR-001 and ADR-002. Governance artefacts (integrity reviews, completion review, CHANGELOG, Technical Debt Register) are consistent and roadmap-aligned. Remaining High items are Stage A dual truth and missing product orchestration / persistence — integration work for Epic 3 — not defects that invalidate the Educational Intelligence architecture.

Unconditional **APPROVED** is withheld while:

- product surfaces remain on legacy educational authorities;  
- Twin-first orchestration and persistence are absent;  
- Confidence ownership and Evidence journal loops remain incomplete;  
- canonical architecture status docs still drift from shipped 2.1–2.10 reality.

**REJECTED** is not warranted: there is no architectural redesign required, no Curriculum V1/V2 breakage in the domain stack, and no integrity failure in Recommendation or Mission packaging/execution relative to Decision authority.

### Binding conditions for v0.5.0 / Epic 3 start

1. **Name Stage A honestly** — live legacy services are not Twin-first Educational Intelligence.  
2. **No hybrid truth** — never average legacy % / heuristics with Twin factors, Decision packaging, or Mission composition.  
3. **Decision remains sole selection authority** — Recommendation packages; Mission executes; neither re-ranks.  
4. **Write/read firewall** — no Twin belief mutation from Readiness, Decision, Recommendation, or Mission composition.  
5. **Explainability chain preserved** end-to-end; no opaque “recommended for you” / “today’s tasks” without Decision attribution.  
6. **Warrant and cold-start honesty** — never Mid/High theatre under thin warrant.  
7. **Curriculum V1/V2** via canonical helpers / lineage only.  
8. **Accept/dismiss and completion** are preference / Behaviour evidence — never mastery or readiness writes.  
9. **Stage B/C cutover planned** before claiming product Twin-first integrity.  
10. **Orchestration before live consumers** — Evidence → Pipeline → Twin; `CurriculumContext` builder; Decision → Recommendation → Mission; default strategy order K→M→B→P.  
11. **Confidence separability** before calibrated Confidence-as-risk product claims.  
12. **Documentation hygiene** — sync EI Architecture status and root `ARCHITECTURE.md` with shipped domain layer.  
13. **Epic 3 must not redesign** the Educational Intelligence chain recorded in ADR-002.

### Not in scope of this review

- Implementation, Stage B adapters, UI cutover, or persistence schemas  
- Alembic / Twin ORM / Decision Journal migrations  
- Belief-enrichment scoring engines  
- Deleting legacy readiness / recommendation / planning services  
- Application code changes, tests, or migrations (none performed)

---

## Architecture Compliance Summary

| Invariant | Status |
|---|---|
| Twin sole educational-state authority (domain) | Established |
| Evidence → Strategies → Twin write path | Preserved |
| Readiness read-side only | Preserved |
| Decision sole next-action selector (domain) | Preserved |
| Recommendation is Decision projection | Preserved |
| Mission operationalises Decision | Preserved |
| Framework-free domain layering | Preserved |
| Curriculum V1/V2 compatibility | Preserved |
| Warrant / cold-start honesty | Preserved structurally |
| Legacy Stage A coexistence (no hybrid) | Preserved / named |
| Single product educational authority | **Not yet** — Stage A dual truth |
| Product Twin-first cutover | **Not done** — Epic 3 condition |
| ADR / debt / changelog governance alignment | Preserved |
| Root architecture doc reflects domain layer | **Incomplete** — hygiene condition |

---

## Completion Report Sections (review milestone)

### Summary

Final Architecture Guardian Review for Epic 2 / v0.5.0. Domain Educational Intelligence architecture is approved with conditions; residual risks are integration-led; Epic 3 may proceed as Product Integration under ADR-002.

### Files Created

- `docs/reviews/ARCHITECTURE_GUARDIAN_REVIEW_EPIC_2.md`

### Files Modified

None (review-only).

### Tests Executed

None (documentation-only).

### Migration Impact

None.

### Architecture Compliance

Layering and curriculum V1/V2 invariants preserved in the domain Educational Intelligence stack. Product service convergence remains open under binding conditions. Application code intentionally untouched.

### Technical Debt

Aligned with [`docs/TECHNICAL_DEBT_REGISTER.md`](../TECHNICAL_DEBT_REGISTER.md) post–Epic 2 entries (E2-PI-*, E2-PE-*, E2-EE-*, E2-PX-*, E2-EN-01). Dominant residual: Stage A dual authority and missing production orchestration / persistence.

### Known Limitations

- Does not re-execute pytest or ruff.  
- Does not deep-audit every Evidence extractor beyond prior gate findings.  
- Does not design Stage B adapter schemas or UI copy systems.  
- Does not itself sync `ARCHITECTURE.md` or EI Architecture status tables (recommended under conditions).

---

## Stop

Architecture Guardian Review for Epic 2 Release complete. **No implementation. No migrations. No tests. No production file changes beyond this review document.**

### Final Decision

**APPROVED WITH CONDITIONS**

*End of Architecture Guardian Review — Epic 2 Release.*
