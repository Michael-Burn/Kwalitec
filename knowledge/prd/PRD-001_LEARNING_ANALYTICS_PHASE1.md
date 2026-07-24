# PRD-001 — Learning Analytics Phase 1

**PRD ID:** PRD-001  
**Title:** Learning Analytics Phase 1 — Educational event instrumentation  
**Version:** 1.1  
**Status:** Approved  
**Revised:** 2026-07-24  
**Author:** EP-001 programme  
**Owners:** Product / Engineering / Educational / Privacy  

**Design review:** [`PRD_001_REVIEW.md`](PRD_001_REVIEW.md) (2026-07-24 — APPROVE WITH CHANGES)  
**Revision summary:** [`PRD_001_REVISION_SUMMARY.md`](PRD_001_REVISION_SUMMARY.md)  

**Implementation:** Prohibited until an implementation milestone cites this Approved PRD and opens a persistence ADR. Role countersignatures in §22 record document approval.

---

## 1. Problem Statement

Product Analytics Architecture defines learning metrics but ships **no collectors**. Without first-party events for Session, reflection, journey, Educational State, and Twin evolution, EP-001 cannot measure Validation Framework outcomes **O1, O2, O7** (and observe O4 evolution via snapshots) during private beta.

Evidence: `knowledge/VERSION_1_READINESS.md` — Analytics instrumentation NOT STARTED; architecture Design only; [`PRD_001_REVIEW.md`](PRD_001_REVIEW.md) blocked Draft/Review on privacy and scope.

**Outcomes O3 (revision adherence) and O8 (recommendation acceptance) are explicitly deferred** to a future approved PRD — not delivered by PRD-001.

---

## 2. Student Benefit

Students do **not** see raw analytics events. Benefit is indirect: product and beta decisions grounded in real study behaviour.

| Vision design question | How PRD-001 helps |
|---|---|
| What should I do now? | Indirect — better next-action quality after product uses measured Session/reflection/journey data |
| How am I progressing? | Indirect — enables honest progress measurement (O1/O2/O7); learner surface remains Student History |
| What is stopping me? | Indirect — abandonment vs completion visible in Session events |
| What happens next? | Indirect — journey + Educational State / Twin evolution observability |

---

## 3. Educational Benefit

Enables measurement of:

| Delivered by PRD-001 | Validation Framework | Not claimed |
|---|---|---|
| Study consistency (leading) | O1 | — |
| Mission / Session completion | O2 | — |
| Reflection completion | O7 | — |
| Journey progression (milestones) | Journey metric | — |
| Educational State / Twin evolution (observe) | O4 leading via snapshots | Mastery recalculation |
| — | — | **O3 revision adherence** |
| — | — | **O8 recommendation acceptance / benefit** |
| — | — | O5/O6/O9 full validation |

Reinforces Vision educational principles: consistency, feedback, reflection. Does **not** claim revision or recommendation validation.

---

## 4. Vision Alignment

| Check | Answer |
|---|---|
| Final Test | Yes — outcome-driven product improvement without vanity metrics |
| North Star | Yes — leading indicators O1, O2, O7 (not pass-rate claims) |
| Never Build | No violation — first-party learning events; no opaque AI; no activity-as-success |
| AI recommendations | N/A — recommendation engine unchanged; no recommendation events |
| Links | Vision Success Metrics; Blueprint outcomes-before-engagement; Analytics Architecture; EP-001 WS2 |

---

## 5. Architecture Impact

| Area | Impact | Notes |
|---|---|---|
| Educational OS (`src/`) | Read | Observe domain lifecycle; must not own mastery |
| Flask `app/` | Write (thin) | Server-side emit at existing lifecycle points only |
| Digital Twin | **Read / hash metadata only** | No algorithm change; `twin.evolved` observes version/hash |
| EducationalStateService | **Read / hash metadata only** | Sole unified Educational State **assembler** for experience; no contract rewrite; no educational math in analytics |
| Educational algorithms | None | Forbidden to relocate scoring into analytics |
| Recommendation engine | None | Unchanged; events excluded |
| One Runtime / Navigation | Preserve | Legacy `/analytics` remains migration shell; Student History remains learner analytics surface |
| Curriculum V1/V2 | None | |
| Persistence / Alembic | Yes | Append-only event store — ADR required at Phase A |
| New ADR | **Required** | Persistence, idempotency keys, retention jobs |

### Authority clarification (binding)

- **Twin / Evidence / Mission / Journey / Reflection workflows** — domain educational authorities.  
- **EducationalStateService** — sole assembler of One Educational State snapshot for experience.  
- **Analytics event store** — operational observation + aggregation only; **never** origin of mastery, readiness, or next action.

---

## 6. Scope — events in / out

### In scope (Phases B–E)

| Event | Validation link |
|---|---|
| `session.started` | O1, O2 |
| `session.completed` | O1, O2 |
| `reflection.completed` | O7 |
| `educational_state.snapshot` | O4 observe |
| `journey.milestone_reached` | Journey progression |
| `twin.evolved` | Twin evolution observe |

### Out of scope (future PRD required)

- `revision.planned` / `revision.completed` (**O3 deferred**)
- `recommendation.shown` / `.accepted` / `.dismissed` / `.completed` (**O8 deferred**)
- Revision effectiveness, mastery/confidence progression aggregates, pass-rate ingestion
- Product executive dashboard UI (WS7 — consumes data later)
- Third-party analytics SDK / CDP / warehouse

---

## 7. Data governance (CRITICAL — no ambiguity)

### 7.1 Retention policy

| Data class | Retention period | Justification |
|---|---|---|
| **Raw events** | **18 months** from `occurred_at`, or until account deletion (whichever sooner) | Private-beta measurement window covering a typical exam cycle; Analytics Architecture privacy preference for first-party limited retention |
| **Aggregated metrics** (weekly rollups keyed by user or cohort) | **36 months** from aggregation week-end, or until account deletion for user-keyed rows | Longer trend for V1 exit / EP-001 reporting without retaining raw detail |
| **Snapshot records** (`educational_state.snapshot`, `twin.evolved`) | Same as **raw events** (18 months / account deletion) | Hash/metadata only — no educational payload retained in analytics store |

Scheduled purge job MUST enforce these windows (Phase A delivers job skeleton; must run before private-beta cohort expansion beyond dogfood).

### 7.2 Deletion policy

| Trigger | Behaviour |
|---|---|
| **Student-requested deletion** | Within **30 days** of verified request: delete all raw events, snapshot rows, and user-keyed aggregates for `user_id`; write audit log entry `analytics.user_deleted`; educational domain data deletion follows existing account/support workflow (out of scope to redefine here, but analytics cascade is mandatory) |
| **Scheduled deletion** | Daily job deletes rows past retention; audit count of rows purged |
| **Cascade** | Deleting a user account **must** cascade to analytics event tables for that `user_id`. Aggregated cohort rows that are anonymised (no `user_id`) are retained until aggregate retention expires |

No silent soft-delete that leaves queryable educational analytics for deleted students.

### 7.3 Export policy

| Export type | Format | Contents | Who |
|---|---|---|---|
| **Student export** | JSON (UTF-8) download or secure support delivery | That student’s raw events + user-keyed weekly aggregates; **no** other users; hashes as stored (not reversed) | Student (self-serve when built) or Support on verified request (manual OK in beta) |
| **Administrative export** | CSV/JSON | Cohort aggregates only (counts, rates); **no** free-text; minimise `user_id` — prefer opaque research tokens if shared outside founder ops | Founder / Admin with `console` capability |
| **Audit export** | JSON lines | Append-only audit log: emit failures, deletions, export requests, purge runs | Security / Founder |

SLA for student export in private beta: **14 days** manual fulfilment until automated path exists.

### 7.4 Payload policy (per event — mandatory)

Legend:

- **Full payload** — structured fields listed (never free-text reflection body, never exam results).  
- **Hashed** — cryptographic hash (SHA-256 hex) of canonical serialisation of educational snapshot/twin state; **not** reversible to Twin beliefs.  
- **Metadata only** — ids, enums, timestamps, flags, hashes, schema_version.

| Event | Full payload fields | Hashed | Metadata only | Justification |
|---|---|---|---|---|
| `session.started` | `event_id`, `event_type`, `user_id`, `session_id`, `mission_id`, `occurred_at`, `idempotency_key`, `schema_version` | — | All listed fields are metadata | Enough to measure starts without curriculum/content |
| `session.completed` | As started + `started_at` (for duration derive) + `completion_status` (`completed` \| `abandoned_after_start`) | — | Same | Duration = derived context only; status distinguishes productive completion (O2) |
| `reflection.completed` | `event_id`, `event_type`, `user_id`, `reflection_id`, `required_flag` (bool), `quality_flag` (bool), `occurred_at`, `idempotency_key`, `schema_version` | — | Same; **no body, no free-text** | O7 completion + structured quality without storing reflective content (Vision privacy) |
| `journey.milestone_reached` | `event_id`, `event_type`, `user_id`, `journey_id`, `milestone_id`, `occurred_at`, `idempotency_key`, `schema_version` | — | Same | Milestone progression without journey narrative text |
| `educational_state.snapshot` | `event_id`, `event_type`, `user_id`, `snapshot_id`, `schema_version`, `content_hash`, `occurred_at`, `idempotency_key` | **`content_hash` required** | **Hash + metadata only — full Educational State payload FORBIDDEN in analytics store** | Closes Analytics Architecture §9.2; prevents parallel educational truth and PII-rich profiles in analytics |
| `twin.evolved` | `event_id`, `event_type`, `user_id`, `twin_snapshot_id`, `twin_version`, `reason_code` (enum), `content_hash`, `occurred_at`, `idempotency_key`, `schema_version` | **`content_hash` required** | **Hash + metadata only — Twin payload FORBIDDEN** | Observe evolution; Twin remains authoritative in its store |

**Maximum payload size:** 8 KiB per event row (enforced at write). Hash-only snapshot/twin events must stay well under this.

---

## 8. Privacy (HIGH)

| Principle | PRD-001 rule |
|---|---|
| **Minimum data collection** | Only fields in §7.4; no page views; no keystrokes; no reflection text; no exam PII |
| **Purpose limitation** | Private-beta educational validation (O1, O2, O7, journey/state observation) and release health — **not** advertising, **not** resale, **not** opaque vendor profiling |
| **Student visibility** | Students do not browse raw event tables. Learner analytics remain Student History / Educational State projections. Students may request export (§7.3) |
| **Consent assumptions** | Invite-only private beta: account invitation + privacy notice stating first-party learning analytics events are collected for product validation. No separate marketing consent. Expanding jurisdictions requires Privacy Review update |
| **Deletion workflow** | Support ticket or settings request → verify identity → cascade delete per §7.2 within 30 days → audit log |
| **Privacy review checkpoint** | Before cohort > dogfood (or any external IFoA invitees): complete `knowledge/product/private_beta/PRIVACY_REVIEW.md` sign-off citing this PRD §7–§8 |

No third-party analytics SDK. No new CSP script hosts.

---

## 9. Security (HIGH)

| Control | Specification |
|---|---|
| **Event authenticity** | Events emitted **only server-side** from trusted lifecycle services after authentication. No public/client ingest API in PRD-001 |
| **Tamper detection** | Event rows are **append-only**: application UPDATE of event body forbidden. DB role should deny UPDATE if feasible. Optional `row_hmac` (HMAC-SHA256 of canonical payload with server secret) for integrity verification on read |
| **Replay protection** | `idempotency_key` unique per `(user_id, event_type, entity_key)` where `entity_key` is `session_id` / `reflection_id` / `milestone_id` / `snapshot_id` / `twin_snapshot_id`. Duplicate insert → no-op success |
| **Idempotency** | Same as replay protection; required for all events |
| **Access control** | Write: system only. Read raw events: owning student (export path) or Founder/Admin with console capability. Cohort aggregates: Founder/Admin only. Students never read other users’ events |
| **Audit logging** | Log: purge runs, user deletion cascades, admin exports, emit failures (structured). Retain audit log **36 months** |
| **Failure handling** | If educational transaction committed and emit fails: **fail-open** for student UX — educational outcome preserved; structured error `analytics.emit_failed`; retry via outbox (Phase A). Never roll back learning completion solely because analytics failed |
| **Injection** | ORM / bound parameters only; `event_type` enum allowlist; reject unknown types |
| **CSRF** | No new browser POST endpoints for ingest; existing lifecycle routes keep CSRF |

---

## 10. Performance budgets (HIGH — measurable)

| Budget | Maximum | How measured |
|---|---|---|
| Event generation latency (emit call) | **5 ms** p95 synchronous insert or outbox enqueue | Staging PROFILE / pytest timing harness |
| Educational State / Twin hash overhead | **20 ms** p95 per material snapshot | Staging; hash only on material evolution, not every request |
| Storage growth | **≤ 2 KiB** average raw event; **≤ 50 events/user/week** alert threshold | Weekly ops query |
| Payload size | **8 KiB** hard reject | Write-path validation |
| Batch size (purge / retry) | **1 000** rows per transaction | Job config |
| Processing delay (outbox → persisted event) | **60 s** p95 | Outbox lag metric |
| Session-complete path regression | **No >10% p95 regression** vs pre-flag baseline on staging smoke | GA/performance soft budgets |

Exceeding budgets → fix, feature-flag off, or Technical Debt with owner before expanding cohort.

---

## 11. Implementation phases (MEDIUM)

Independent, separately shippable. Each phase has its own tests and flag if needed.

| Phase | Scope | Exit |
|---|---|---|
| **A — Infrastructure only** | Event store schema (Alembic), repository, idempotency, outbox/retry, purge job skeleton, architecture import guard, feature flag `ANALYTICS_EVENTS_V1`, ADR | Migrations + unit tests green; **no domain emits** |
| **B — Session events** | `session.started` / `session.completed` | Integration tests; O2 measurable for flagged users |
| **C — Reflection events** | `reflection.completed` | O7 measurable |
| **D — Educational State snapshots** | `educational_state.snapshot` (hash + metadata) | Emit only on material ESS assembly change |
| **E — Journey + Twin evolution** | `journey.milestone_reached`, `twin.evolved` | Milestone + twin version observability |

**Recommendation events:** excluded — future PRD.  
**Revision events:** excluded — future PRD.

---

## 12. Metrics

| Metric | Baseline | Target | How measured |
|---|---|---|---|
| Event emit success rate (Phases B–E) | n/a | ≥ 99.5% of eligible lifecycle points | emit_failed / eligible |
| Session completion events coverage | 0% | 100% of authoritative Session completes when flag on | Compare mission completion rows vs events |
| O1 weekly consistency (flagged cohort) | Unknown | Reportable within 2 weeks of Phase B | Framework O1 formula |
| O2 completion rate | Unknown | Reportable | Framework O2 |
| O7 reflection completion | Unknown | Reportable after Phase C | Framework O7 |
| Analytics → Twin import violations | 0 | 0 | Architecture test |
| p95 emit latency | n/a | ≤ 5 ms | §10 |

Activity vanity (page views, raw minutes alone) are **not** success metrics. Session duration may be derived as **context only**.

---

## 13. Success criteria

- [ ] Phases A–E complete per §11 with tests green  
- [ ] Data governance §7 enforced (retention job runnable; deletion/export documented)  
- [ ] Privacy §8 checkpoint satisfied before external cohort  
- [ ] Security §9 controls implemented and tested  
- [ ] Performance §10 budgets measured on staging  
- [ ] O1, O2, O7 reportable for flagged users; **no** O3/O8 claims  
- [ ] One Educational Truth preserved (architecture tests)  
- [ ] EVENT_CATALOGUE.md (or Analytics Architecture update) matches §7.4  

---

## 14. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Analytics becomes second educational brain | Medium | High | Hash-only snapshots; architecture import tests; no mastery math in analytics |
| Fail-open emit loss undercounts O1/O2 | Medium | High | Outbox retry; emit_failed alerts; coverage metric §12 |
| Privacy over-retention | Low | High | 18-month raw retention + purge job |
| Scope creep (O3/O8) | Medium | Medium | Explicit out of scope; Framework freeze amended |
| Performance regression on Session complete | Medium | Medium | Budgets §10; flag off |
| Premature “validated learning” marketing | Medium | High | V1 exit + Framework sample floors; no O9 claims |

---

## 15. Definition of Done

This PRD’s implementation is Done when:

- [ ] Acceptance criteria §16 met for shipped phases  
- [ ] Engineering Standards PR checklist satisfied  
- [ ] Tests green: unit, integration, architecture guard, failure/idempotency (§17)  
- [ ] Documentation updated (EVENT_CATALOGUE / Analytics Architecture; VERSION_1_READINESS)  
- [ ] Accessibility N/A (no new learner UI) unless dashboard later  
- [ ] Security + performance gates §9–§10 met or debt-owned  
- [ ] No unexplained recommendations introduced (engine unchanged)  
- [ ] Technical debt recorded (or none)  
- [ ] Product Language Guide respected (no learner-facing “analytics event” jargon required)  
- [ ] Rollback strategy §19 verified on staging once  

---

## 16. Acceptance criteria

### Cross-cutting

- [ ] Append-only store; idempotent writes; unknown `event_type` rejected  
- [ ] No third-party SDK; no reflection free-text; no exam PII in analytics tables  
- [ ] Twin / EducationalStateService educational math unchanged  
- [ ] Student History remains canonical learner analytics surface  
- [ ] Architecture test: analytics must not import Twin calculators to recompute mastery  

### Phase A

- [ ] Alembic migration + ADR merged  
- [ ] Repository, idempotency, outbox, purge skeleton, feature flag  

### Phase B

- [ ] `session.started` / `session.completed` on authoritative paths only  
- [ ] No emit on navigation-only views  

### Phase C

- [ ] `reflection.completed` with `required_flag` / `quality_flag`; no body  

### Phase D

- [ ] `educational_state.snapshot` with `content_hash` + metadata only  

### Phase E

- [ ] `journey.milestone_reached` on authoritative milestones  
- [ ] `twin.evolved` with version + `content_hash` + `reason_code`  

---

## 17. Test strategy

| Layer | Required |
|---|---|
| **Unit** | Schema validation; idempotency; hash stability; duration derive; serializer privacy (no free-text) |
| **Integration** | Session/reflection/journey/ESS/twin emit paths; AuthZ on export/admin read |
| **Load** | 50 concurrent Session completes — emit within §10; no >10% path regression |
| **Failure** | Emit fail after educational commit → outcome preserved + outbox; duplicate submit → single row |
| **Regression** | Architecture import guard; sole runtime History surface; recommendation behaviour unchanged; curriculum V1/V2 unaffected |

---

## 18. Out of scope

- O3 revision events and revision adherence claims  
- O8 recommendation events and acceptance/benefit claims  
- O5/O6/O9 instrumentation and pass-rate ingestion  
- Replacing Student History; second educational brain; vendor CDP/warehouse  
- Product executive dashboard UI (WS7)  
- Twin/ESS algorithm changes  
- Client-side event beacons  

---

## 19. Rollback strategy

1. Feature flag `ANALYTICS_EVENTS_V1` = off → stop new emits immediately.  
2. Educational paths unaffected (fail-open design).  
3. Optional: leave historical rows; purge via retention job if required by Privacy.  
4. Do **not** drop Twin/ESS/mission tables as part of analytics rollback.  
5. Document rollback in release notes for any phase that enabled the flag in production/beta.

---

## 20. Release strategy

1. Merge Phase A behind flag off.  
2. Enable flag in staging → run §10 budgets + §17.  
3. Dogfood (internal) Phases B→E incrementally.  
4. Privacy Review checklist sign-off before external IFoA invites.  
5. Expand private beta; report O1/O2/O7 only.  
6. WS7 dashboard and O3/O8 require separate PRDs.

Align with `knowledge/RELEASE_PLAYBOOK.md` and Quality Manual educational-validation gate (no O3/O8 claims from this PRD).

---

## 21. Dependencies / references

| Dependency | Role |
|---|---|
| Vision 2030 | Philosophy, success metrics, data principles |
| PRODUCT_BLUEPRINT.md | Outcomes before engagement; Twin/ESS posture |
| PRODUCT_ANALYTICS_ARCHITECTURE.md | Metric catalogue; One Educational Truth |
| EDUCATIONAL_VALIDATION_FRAMEWORK.md | O1, O2, O7 (O3/O8 deferred) |
| private_beta/PRIVACY_REVIEW.md | Cohort expansion checkpoint |
| PRD_001_REVIEW.md | Mandatory design review |
| Future PRD-00x | Revision (O3) and recommendation (O8) events |
| Implementation ADR | Persistence (Phase A) |

**Closed by this PRD (Analytics Architecture §9):**

1. Retention + deletion workflow → §7.1–§7.2  
2. Snapshot hash vs payload → **hash + metadata only** (§7.4)  

**Remains for future PRD (not blockers for PRD-001):**

3. Pass-rate methodology (O9)  
4. Decision Journal as sole recommendation acceptance source (O8)

---

## 22. Requirement traceability (MEDIUM)

| ID | Requirement | Vision | Blueprint | Validation objective | Acceptance test | Owner | Review gate |
|---|---|---|---|---|---|---|---|
| R1 | Session events | Success: Session completion; consistency | Outcomes before engagement | O1, O2 | Phase B integration | Engineering | Architecture |
| R2 | Reflection events | Reflect regularly | Evidence before opinion | O7 | Phase C integration | Engineering | Educational |
| R3 | ESS snapshot hash | One Educational State; privacy | ESS unified truth | O4 observe | Phase D; no payload in DB | Engineering | Architecture + Privacy |
| R4 | Journey milestone | Progress clarity | One Runtime experience | Journey metric | Phase E | Engineering | Architecture |
| R5 | Twin evolved hash | Evidence-driven Twin; privacy | Twin authoritative | Twin evolution observe | Phase E; no Twin math change | Engineering | Architecture |
| R6 | Retention/deletion/export | Student data belongs to student | Professional quality | Governance | Purge + deletion tests; export procedure doc | Privacy + Eng | Privacy |
| R7 | Security controls | Auditable; privacy | Reliability | — | Idempotency + AuthZ tests | Engineering | Security |
| R8 | Performance budgets | — | Professional quality | — | Staging budget harness | Engineering | Quality |
| R9 | No O3/O8 in scope | Honesty | No dual claims | O3/O8 deferred | PR review checklist | Product | Product |
| R10 | No second brain | One Educational Truth | Evidence before opinion | — | Architecture import test | Architecture | Architecture |

---

## 23. Decision

| Role | Decision | Date |
|---|---|---|
| Product | **Approved** (v1.1 revision directive) | 2026-07-24 |
| Architecture | **Approved** (v1.1) | 2026-07-24 |
| Privacy | **Approved** (policies §7–§8 as written; cohort still needs PRIVACY_REVIEW checklist) | 2026-07-24 |
| Educational | **Approved** (scope limited to O1/O2/O7; O3/O8 deferred) | 2026-07-24 |

**Status = Approved.**

Implementation may begin only via a dedicated milestone that: (1) cites this PRD v1.1, (2) lands Phase A ADR, (3) keeps `ANALYTICS_EVENTS_V1` off until staging budgets pass. External cohort expansion additionally requires Privacy Review checklist sign-off.
