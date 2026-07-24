# Product Analytics Architecture

**Version:** 1.0  
**Status:** Design only — **no implementation in this programme**  
**Authority:** Product analytics design (subordinate to Vision 2030 + Blueprint)  
**Related:** `knowledge/subsystems/analytics.md`, Vision success metrics, Educational State architecture  

---

## 1. Purpose

Design an analytics architecture that measures **learning**, not activity vanity — aligned with Vision 2030 Product Philosophy and Success Metrics.

This document specifies **what** to track, **where** truth lives, and **constraints**. It does not ship collectors, warehouses, or new dashboards.

---

## 2. Design principles

1. **Learning over activity** — prefer mastery, adherence, acceptance, readiness calibration over raw clicks or minutes alone.
2. **One Educational Truth** — metrics must project from Educational State / Twin / Evidence authorities; do not invent a parallel scoring brain.
3. **Reproducible & auditable** — same inputs → same aggregates; recommendations traced to evidence.
4. **Privacy** — student data belongs to the student; minimise PII; no silent exfiltration to opaque vendors without review.
5. **Explainability** — aggregates used for product decisions must be defensible educationally.
6. **No dual analytics surfaces** — canonical learner analytics remain Student History / Educational State projections; legacy `/analytics` is migration shell only.

---

## 3. Metric catalogue (required tracking)

| Metric | Definition (design) | Primary source of truth (intended) | Vision link |
|---|---|---|---|
| **Mission / Session completion** | Authoritative study commitment completed vs assigned | Mission / Session execution + Evidence | Consistency, learning |
| **Study consistency** | Presence of productive study across planned days/windows | Behaviour evidence + plan adherence | Consistency |
| **Session duration** | Elapsed time in learning session (supporting, not success alone) | Session runtime events | Context only |
| **Recommendation acceptance** | Accept / start vs dismiss / ignore of next-action recommendations | Decision journal / recommendation outcomes | Trust, guidance quality |
| **Topic mastery** | Evidence-backed mastery estimates (never self-certified alone) | Twin / Knowledge evidence | Learning |
| **Revision adherence** | Completed revision vs planned revision windows | Revision planner + completion evidence | Intelligent revision |
| **Journey completion** | Progress through structured learning journey milestones | Journey projections from Educational State | Progress clarity |
| **Reflection completion** | Completed reflections where product requires them | Reflection workflow ports | Reflect regularly |
| **Educational State evolution** | Material changes in unified educational snapshot over time | EducationalStateService snapshots / Twin updates | One Educational State |

**Explicit non-metrics (alone):** raw page views, undifferentiated “engagement”, gamification streaks as success.

---

## 4. Logical architecture (design)

```
┌─────────────────────────────────────────────────────────────┐
│ Learner / Founder product surfaces                          │
│ (projections only — no private metric math in templates)    │
└───────────────────────────┬─────────────────────────────────┘
                            │ read models
┌───────────────────────────▼─────────────────────────────────┐
│ Analytics Application (future)                              │
│ - metric definitions                                        │
│ - aggregation jobs / queries                                │
│ - privacy filters                                           │
└─────────────┬───────────────────────────────┬───────────────┘
              │                               │
┌─────────────▼─────────────┐   ┌─────────────▼───────────────┐
│ Educational authorities   │   │ Operational event log         │
│ Twin / Evidence / Mission │   │ (session timing, UI accept)   │
│ Journey / Revision /      │   │ append-only, auditable        │
│ Educational State         │   │                               │
└───────────────────────────┘   └───────────────────────────────┘
```

### Rules

- Educational claims (mastery, readiness, next action) **never** originate from the analytics store.
- Analytics may **summarise** educational authorities; it must not **override** them.
- Session duration may come from operational events; interpret only with educational context.
- Founder/ops dashboards consume the same definitions as product evaluation — no private founder scoring of student mastery.

---

## 5. Event sketch (not implemented)

Illustrative event names for a future instrumentation PRD:

| Event | Payload (minimal) | Notes |
|---|---|---|
| `session.started` / `session.completed` | user_id, session_id, mission_id, timestamps | Duration derived |
| `recommendation.shown` / `.accepted` / `.dismissed` | recommendation_id, reason_codes | Acceptance rate |
| `revision.planned` / `.completed` | window_id, topic_ids | Adherence |
| `journey.milestone_reached` | journey_id, milestone_id | Journey completion |
| `reflection.completed` | reflection_id | Reflection completion |
| `educational_state.snapshot` | snapshot_id, schema_version, hash | Evolution tracking (careful with PII) |

Schema versioning and retention policies are **TBD** in a future PRD (privacy review required).

---

## 6. Privacy & compliance constraints

- Prefer aggregates and educational IDs over free-text content in analytics stores.
- Retention and export/delete must support “student data belongs to the student”.
- No third-party analytics SDK without Security + Privacy review and CSP impact assessment.
- Private beta: prefer first-party logging already in-platform over new vendors.

---

## 7. Relationship to existing code (as-is)

| Component | Role today | Future |
|---|---|---|
| `AnalyticsService` / legacy `/analytics` | Legacy aggregation; sole-runtime redirect to Student History | Retire as educational authority; keep redirect until safe |
| Student History | Canonical learner analytics surface (consolidation) | Remain projection surface |
| EducationalStateService | Unified read model for experience | Source for Educational State evolution metrics |
| Founder observability | Ops / alpha signals | Must not become second educational brain |

---

## 8. Implementation gate (EP-001)

Programme authority: [`../ep001_product_validation/`](../ep001_product_validation/).  
Metric definitions: [`../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md`](../ep001_product_validation/EDUCATIONAL_VALIDATION_FRAMEWORK.md).  
Phase 1 PRD: [`../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md`](../../prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md).

Do **not** implement collectors until:

1. PRD-001 Status = Approved — **met (v1.1)**; start only via implementation milestone + Phase A ADR
2. Metric definitions frozen with educational governance where mastery/readiness involved (Framework PRD-001 freeze: O1, O2, O7)
3. Security review for any new dependency or egress (PRD-001 forbids third-party SDK)
4. Explicit non-modification of Twin / EducationalStateService contracts unless EP-001 programme authority granted for a named metric PRD
5. External cohort: `private_beta/PRIVACY_REVIEW.md` checklist signed

---

## 9. Open questions (STOP — do not guess)

1. ~~Exact retention windows and deletion workflow for event logs~~ — **Closed by PRD-001 v1.1 §7**
2. ~~Whether `educational_state.snapshot` stores payloads vs hashes only~~ — **Closed by PRD-001 v1.1: hash + metadata only**
3. Pass-rate measurement methodology (external exam results ingestion) — **future O9 PRD**
4. Whether recommendation acceptance uses Decision Journal persistence (E2-PE-02 debt) as sole source — **future O8 / recommendation PRD** (out of PRD-001 scope)

---

**Status:** Design complete for Programme 6; EP-001 PRD-001 **Approved** (v1.1)  
**Implementation:** Gated on implementation milestone citing PRD-001 (not on further PRD privacy ambiguity)
