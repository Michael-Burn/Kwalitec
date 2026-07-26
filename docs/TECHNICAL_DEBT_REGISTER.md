# Kwalitec Technical Debt Register

**Version:** v0.6.0

**Last Updated:** 23 July 2026

**Status:** Active (post–Architecture Consolidation)

**Governance:** `knowledge/GOVERNANCE.md` · Vision: `knowledge/product/vision/PRODUCT_VISION_2030.md`

---

# Purpose

This document records **intentional technical debt** within the Kwalitec codebase.

**Rule (post-consolidation):** No removals of legacy adapters, redirect shells, or deprecated services unless proven safe. Prefer register + recommend over deletion.

Technical debt differs from defects.

A defect is unintended incorrect behaviour.

Technical debt is an intentional engineering compromise accepted because the cost of immediate resolution exceeds the short-term value.

Every item recorded here should have:

- a clear description;
- business justification;
- engineering impact;
- priority;
- proposed resolution;
- target Epic or release.

This register shall be reviewed at the conclusion of every Epic.

---

# Priority Definitions

| Priority | Meaning |
|-----------|---------|
| Critical | Must be resolved before major production expansion. |
| High | Should be resolved within the next 1–2 Epics. |
| Medium | Improves maintainability but does not affect correctness. |
| Low | Desirable improvements with minimal operational impact. |

---

# Current Technical Debt

## TD-001 — SQLAlchemy 2.x Deprecations

**Priority:** High

**Category:** Framework Upgrade

### Description

Several services and tests still use legacy SQLAlchemy APIs.

Examples include:

- `Query.get()`
- legacy engine access patterns

### Impact

No immediate functional impact.

Future SQLAlchemy releases may remove compatibility.

### Justification

Deferred to avoid interrupting Curriculum Architecture work.

### Recommendation

Upgrade all code to SQLAlchemy 2.x APIs.

### Target

Maintenance Sprint after Epic 2.

---

## TD-002 — Large Route Modules

**Priority:** Medium

**Category:** Maintainability

### Description

Some blueprint route modules remain significantly larger than preferred.

Examples include:

- Study Plan routes

### Impact

Reduced readability.

More difficult code reviews.

### Recommendation

Split large route modules into feature-focused modules.

### Target

Future Architecture Improvement.

---

## TD-003 — Service Decomposition

**Priority:** Medium

**Category:** Architecture

### Description

Several services continue to grow as additional educational capabilities are introduced.

### Impact

Reduced cohesion over time.

### Recommendation

Continue decomposing services into narrowly focused domain services.

### Target

Epic 3+

---

## TD-004 — Remaining Lint Warnings

**Priority:** Medium

**Category:** Code Quality

### Description

A number of existing lint warnings remain outside the scope of Epic 1.

Examples include:

- formatting
- line length
- historical warnings

### Impact

No functional impact.

### Recommendation

Resolve incrementally during maintenance.

### Target

Ongoing.

---

## TD-005 — SQLAlchemy Warning Cleanup

**Priority:** High

**Category:** Framework Compatibility

### Description

Several SQLAlchemy warnings remain during test execution.

### Impact

Potential future compatibility issues.

### Recommendation

Remove deprecated patterns.

### Target

Maintenance Sprint.

---

## TD-006 — Architecture Guardian Findings

**Priority:** Medium

**Category:** Architecture

### Description

Architecture Guardian continues to report pre-existing issues including:

- large files
- business logic in routes
- dependency cycles

No new issues were introduced during Epic 1.

### Recommendation

Treat findings as architectural improvement work rather than release blockers.

### Target

Epic 3.

---

## TD-007 — Performance Optimisation

**Priority:** Low

**Category:** Performance

### Description

Curriculum queries currently prioritise correctness and clarity over optimisation.

### Impact

Negligible for current scale.

### Recommendation

Profile before optimising.

Introduce eager loading only where justified.

### Target

When supporting significantly larger curriculum libraries.

---

# Deferred Design Decisions

The following ideas were intentionally deferred because they do not yet provide sufficient educational value.

---

## Topic Progress at Learning Objective Level

**Status:** Deferred

Reason:

Topic-level progress provides the right balance between educational fidelity and usability.

---

## Graph-based Curriculum Relationships

**Status:** Deferred

Reason:

The canonical hierarchy is sufficient for current Educational Intelligence.

Prerequisite graphs may be introduced later without replacing the hierarchy.

---

## Section-weighted Recommendation Engine

**Status:** Superseded by Epic 2 structural Decision / Recommendation stack

Reason:

Curriculum weights and Decision authority landed in domain Educational Intelligence. Calibrated section-weighted scoring enrichment remains under Educational Evolution (E2-EE-05 / readiness–decision enrichment), not a separate Epic 2 blocker.

Target:

Epic 3+ (enrichment within Decision / Curriculum weight consumers)

---

## Behaviour Analytics

**Status:** Structural foundation delivered in Epic 2; calibrated analytics deferred

Reason:

Behaviour Update Strategy shipped structurally. Populated behaviour metrics and analytics remain Educational Evolution debt (E2-EE-03).

Target:

Epic 3+

---

## Memory Scheduling

**Status:** Structural foundation delivered in Epic 2; calibrated scheduling deferred

Reason:

Memory Update Strategy shipped structurally. Calibrated retention / scheduling engines remain intentional enrichment work, not an Epic 2 defect.

Target:

Epic 3+

---

# Debt Accepted During Epic 1

None.

All architectural compromises introduced during implementation were resolved before Epic completion.

---

# Debt Remaining After Epic 2

**Epic status:** Educational Intelligence domain stack (capabilities 2.1–2.10) closed — APPROVED WITH CONDITIONS ([`docs/reviews/EPIC_2_COMPLETION_REVIEW.md`](reviews/EPIC_2_COMPLETION_REVIEW.md), [`docs/architecture/ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](architecture/ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)).

**Summary:** Epic 2 leaves no known architectural defects. Remaining debt is primarily planned product integration (Stage A dual truth, orchestration, persistence) and intentionally deferred educational / product evolution. None of the items below are defects in the domain Educational Intelligence model.

Pre-existing engineering items TD-001 through TD-007 remain open as recorded above and are **not** duplicated here.

---

## 1. Product Integration

### E2-PI-01 — Stage A dual truth

**Priority:** High

**Description:** Live product surfaces still consume legacy readiness, recommendation, and mission/plan authorities while Twin-first Educational Intelligence exists only in `app/domain/`. Coexistence is named and hybrid averages are forbidden, but product Twin-first authority is not cut over.

**Reason deferred:** Epic 2 closed the domain stack under progressive integration (ADR-002). Immediate cutover was out of scope to preserve production behaviour.

**Target Epic:** Epic 3 (Stage B/C cutover)

---

### E2-PI-02 — Legacy ReadinessService

**Priority:** High

**Description:** `ReadinessService` / analytics remain the live preparedness authority beside domain Readiness Aggregation.

**Reason deferred:** Stage A coexistence; domain Readiness is structural and not yet wired as product truth.

**Target Epic:** Epic 3 (Stage B/C)

---

### E2-PI-03 — Legacy RecommendationService

**Priority:** High

**Description:** `RecommendationService` heuristic generators remain a parallel next-action authority beside Decision Engine + Recommendation packaging.

**Reason deferred:** Domain Recommendation packages Decision only; product cutover and freeze of legacy heuristic deepening belong to integration.

**Target Epic:** Epic 3 (Stage B/C)

---

### E2-PI-04 — Legacy MissionService / PlanningService

**Priority:** High

**Description:** ORM missions and `PlanningService` remain the live execution / planning authority beside domain Mission Intelligence. Planning retains multi-day WeekPlan ownership; mission generation dual authority is the cutover risk.

**Reason deferred:** Mission Intelligence is domain-complete; product operationalisation and persistence adapters were out of Epic 2 scope.

**Target Epic:** Epic 3 (Stage B/C)

---

### E2-PI-05 — Service orchestration adapters

**Priority:** High

**Description:** No production thin orchestration for Evidence → Pipeline → Twin; no `CurriculumContext` builder from `CurriculumService`; no Decision → (optional Recommendation) → Mission service path; no default registered pipeline factory (Knowledge → Memory → Behaviour → Performance).

**Reason deferred:** Domain packages correctly refuse Flask/ORM coupling; orchestration is the missing service-layer bridge before any live Twin-first consumer.

**Target Epic:** Epic 3 (first wiring / Stage B)

---

## 2. Persistence

### E2-PE-01 — Twin persistence

**Priority:** High

**Description:** No production Twin ORM persistence or Evidence → pipeline service bridge. Twin snapshots remain in-memory / domain-only for Epic 2.

**Reason deferred:** Structural Twin and strategies shipped without schema; persistence is an explicit integration milestone.

**Target Epic:** Epic 3 (persistence / adapter milestone)

---

### E2-PE-02 — Decision journal persistence

**Priority:** Medium

**Description:** Decision State materialisation is in-memory; Decision Journal recording (accept / dismiss / defer as preference evidence) is not shipped.

**Reason deferred:** Decision Engine authority closed structurally; journal schema and recording loop deferred to integration.

**Target Epic:** Epic 3 (recording milestone)

---

### E2-PE-03 — Mission persistence convergence

**Priority:** Medium

**Description:** `domain.Mission` vs `models.Mission` dual type identity; domain Mission composition is not yet the persistence path for live daily missions.

**Reason deferred:** Domain Mission Intelligence operationalises Decision without owning ORM; naming and adapter discipline deferred to cutover.

**Target Epic:** Epic 3 (Stage B/C adapters)

---

### E2-PE-04 — Evidence journal (completion / failure loops)

**Priority:** Medium

**Description:** Mission completion / failure → Behaviour Learning Evidence loop is not shipped. Accept/dismiss and completion must become Evidence, not mastery or readiness writes.

**Reason deferred:** Write-path contracts exist; product Evidence capture loops were out of Epic 2 scope.

**Target Epic:** Epic 3 (recording milestone)

---

## 3. Educational Evolution

Intentionally deferred calibrated / enrichment work. Not defects in the structural stack.

### E2-EE-01 — Confidence ownership

**Priority:** High (before calibrated risk framing)

**Description:** No `ConfidenceState` / Confidence update path. `CONFIDENCE_RATING` remains lineage-absorbed under Knowledge; readiness v1 omits Confidence.

**Reason deferred:** Structural-before-scoring; Confidence separability required before rich over/underconfidence product narratives (binding condition).

**Target Epic:** Epic 3+ (before calibrated Confidence-as-risk claims)

---

### E2-EE-02 — Readiness scoring

**Priority:** Medium

**Description:** Readiness Aggregation is factorable and structural; calibrated numeric preparedness scores and belief-content interpretation remain deferred. Structural postures must not be treated as finished scores.

**Reason deferred:** Structure first; avoid premature scoring complexity inside aggregation.

**Target Epic:** Epic 3+ (enrichment within Readiness ownership)

---

### E2-EE-03 — Behaviour metrics

**Priority:** Medium

**Description:** Behaviour metric / belief bags remain largely unpopulated; engagement theatre and streak UIs stay non-authoritative projections if added later.

**Reason deferred:** Behaviour Update Strategy ships structure; calibrated behaviour metrics deferred to enrichment strategies.

**Target Epic:** Epic 3+ (belief enrichment)

---

### E2-EE-04 — Performance scoring

**Priority:** Medium

**Description:** Performance remains assessment lineage without pass-probability invention; richer scored assessment claims and fact schemas deferred. Choice A Evidence Matrix Secondary columns remain documented omissions until Choice B.

**Reason deferred:** Structural Performance strategy before calibrated assessment engines.

**Target Epic:** Epic 3+ (enrichment; architecture note before Choice B)

---

### E2-EE-05 — Decision optimisation

**Priority:** Medium

**Description:** Decision Engine selects next action with structural priority postures and reason codes; numeric optimisers and belief-gap enrichment heuristics beyond structural gaps are deferred.

**Reason deferred:** Deterministic structural Decision authority closed; optimisation math deferred inside Decision ownership, not into Recommendation/Mission.

**Target Epic:** Epic 3+ (Decision enrichment)

---

## 4. Product Experience

### E2-PX-01 — Product wiring

**Priority:** High

**Description:** Twin-first readiness, recommendations, and missions are not live on student-facing surfaces. Claiming “Epic 2 complete for students” would overstate Stage A reality.

**Reason deferred:** Epic 2 was a domain epic; Stage B/C product authority cutover is Epic 3 work.

**Target Epic:** Epic 3 (Stage C)

---

### E2-PX-02 — Premium UI integration

**Priority:** Medium

**Description:** Premium product surfaces do not yet consume Twin / Decision / Recommendation / Mission projections as educational authority.

**Reason deferred:** Trust and domain architecture precede feature wiring (ADR-002); UI cutover out of Epic 2 scope.

**Target Epic:** Epic 3 (Stage C)

---

### E2-PX-03 — Student-facing warrant presentation

**Priority:** Medium

**Description:** Structural warrant and cold-start tags are not bound to student-facing copy. UI can still strip warrant or invent Mid/High theatre unless Stage C binds narration.

**Reason deferred:** Domain honesty contracts closed; presentation binding is cutover work.

**Target Epic:** Epic 3 (Stage C presentation)

---

### E2-PX-04 — Decision explanations in UI

**Priority:** Medium

**Description:** Explainability chain exists structurally through Decision → Recommendation → MissionTask attribution; student-facing explanation copy is not yet bound to reason codes and chain tags.

**Reason deferred:** Packaging and attribution are domain-complete; UI narration deferred to product cutover.

**Target Epic:** Epic 3 (Stage C)

---

## 5. Engineering

No new High engineering defects were introduced inside domain packages relative to approved plans. Framework and lint backlog remain the pre-existing register items (TD-001, TD-004, TD-005) — do not duplicate.

### E2-EN-01 — Canonical documentation status drift

**Priority:** Medium (hygiene)

**Description:** Epic 2 kickoff / Educational Intelligence Architecture / subsystem ownership docs can lag shipped 2.1–2.10 reality.

**Reason deferred:** Capability delivery prioritised over continuous status-table sync; called out as binding hygiene condition at Epic close.

**Target Epic:** Epic 3 kickoff / Epic 2 close documentation sync

---

# Review Process

At the completion of every Epic:

- Review each debt item.
- Update priority.
- Close resolved items.
- Add newly accepted debt.
- Remove completed entries.

No technical debt should remain undocumented.

---

# Summary

| Priority | Count |
|----------|------:|
| Critical | 0 |
| High | 3 (pre-Epic 2) + 8 (Epic 2 residual) |
| Medium | 4 (pre-Epic 2) + 11 (Epic 2 residual) |
| Low | 1 (pre-Epic 2) |

Epic 2 High residuals are Stage A dual truth, legacy service cutover, orchestration, Twin persistence, Confidence ownership, and product wiring — not architectural defects in the domain stack.

---

# Post-Consolidation Debt (Architecture Consolidation COMPLETE)

EOS is the canonical runtime. The following items are **inventory for safe retirement**, not invitations to redesign Twin, EducationalStateService, or educational algorithms under a “cleanup” cover.

## PC-001 — Sole-runtime redirect shells

**Priority:** Medium  
**Category:** Legacy surface  
**Removal:** Only when proven safe  

### Description

Legacy learner shells remain registered and redirect under `KWALITEC_V2_SOLE_RUNTIME` via `app.presentation.consolidation.redirect_if_sole_runtime`:

- `app/dashboard/routes.py` → Student Home
- `app/analytics/routes.py` → Student History
- `app/mission/routes.py` → Student Home / session entry

Marked READY FOR MIGRATION in code comments.

### Impact

Extra routes and templates to maintain; risk of bookmarks hitting redirects forever.

### Recommendation

Keep redirects until analytics of inbound legacy URLs is near-zero and beta communication complete; then remove behind an ADR.

### Target

Post–private-beta hardening (not a governance-docs programme).

---

## PC-002 — Temporary consolidation helper

**Priority:** Low  
**Category:** Compatibility shim  

### Description

`app/presentation/consolidation.py` exists specifically for sole-runtime gating.

### Recommendation

Retain while PC-001 shells exist; delete only with shells.

---

## PC-003 — Mission Adapter / dual mission engines

**Priority:** High  
**Category:** Dual authority (historical Stage A)  

### Description

`app/application/mission_adapter/` and parallel `mission_engine` / `mission_engine_v2` packages remain part of the cutover story. Related Epic 2 residuals: E2-PI-01…04, E2-PX-01.

### Recommendation

Do not remove until product Twin-first / single next-action authority is proven on live paths. Track under Epic 3-class integration — not opportunistic deletion.

---

## PC-004 — Legacy readiness / analytics / planning services

**Priority:** High  
**Category:** Dual truth residual  

### Description

`ReadinessService`, `AnalyticsService`, `PlanningService` (and related) remain in `app/services/` for coexistence / ops. See E2-PI-02…04.

### Recommendation

Freeze deepening; cut over consumers; remove only with proof no live authority remains.

---

## PC-005 — ProfileService Educational State bypass

**Priority:** High  
**Category:** One Educational State  

### Description

Validation / consolidation docs have flagged ProfileService paths that may bypass Educational State projections.

### Recommendation

STOP → Document → Recommend before changing Twin or EducationalStateService. Fix via authorised programme only.

---

## PC-006 — Deprecated founder research URLs

**Priority:** Low  
**Category:** Redirect  

### Description

`app/research/routes.py` and founder feedback handlers keep deprecated `/research/founder*` redirects to Founder Command Centre.

### Recommendation

Retain until inbound traffic is negligible.

---

## PC-007 — Deprecated static branding assets

**Priority:** Low  
**Category:** Dead assets  

### Description

`app/static/images/DEPRECATED.md` documents deprecated branding locations.

### Recommendation

Remove assets only after confirming no template references.

---

## PC-008 — TODO / FIXME hygiene

**Priority:** Low  
**Category:** Maintainability  

### Description

Post-consolidation scan: few `TODO`/`FIXME` markers in `app/`/`src/` hot paths relative to READY FOR MIGRATION comments. Debt is primarily structural (above), not comment sprawl.

### Recommendation

When encountering new TODOs that accept educational or security risk, promote them to numbered register entries.

---

# Overall Assessment

**Epic 2** left no known architectural defects in the domain Educational Intelligence stack; residuals were planned integration and deferred evolution.

**Architecture Consolidation** established EOS as canonical runtime. Remaining debt is primarily **safe-retirement inventory** (redirect shells, adapters, Stage A dual authorities) plus pre-existing TD-001–TD-007 and Epic 2 residual tables above.

None of the PC-* items authorise Twin redesign, EducationalStateService redesign, or educational algorithm changes in a documentation-only programme.

---

**Status:** Approved (post–Architecture Consolidation governance update)

**Next Review:** End of Epic 3 or next major release (earlier if sole-runtime shell removal is proposed)
