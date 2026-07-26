# PRD-001 Design Review

**Document:** `PRD_001_REVIEW.md`  
**Subject:** [`PRD-001_LEARNING_ANALYTICS_PHASE1.md`](PRD-001_LEARNING_ANALYTICS_PHASE1.md)  
**Review type:** Mandatory governance design review  
**Review date:** 2026-07-24  
**Reviewer:** Architecture / Product governance (EP-001)  
**Constraint:** No implementation. No event generation. No runtime code changes.

---

## Executive verdict

**Recommendation: APPROVE WITH CHANGES** *(superseded for document status — see revision)*

> **Supersession (2026-07-24):** Mandatory changes were applied in PRD-001 **v1.1**. See [`PRD_001_REVISION_SUMMARY.md`](PRD_001_REVISION_SUMMARY.md). PRD status is now **Approved**. This review document is retained as the audit trail of the original blockers.

---

## REVIEW 1 — Vision Alignment

**Authority:** `knowledge/product/vision/PRODUCT_VISION_2030.md`

| Vision requirement | PRD-001 posture | Verdict |
|---|---|---|
| Improves learning (not activity vanity) | Instruments Session/reflection/journey/state evolution; rejects page-view success | **Pass** |
| Measurable educational benefit | Ties to Validation Framework O1–O8 leading indicators | **Pass with caveat** — benefit is operational/product-loop; student-facing daily benefit is indirect (acceptable if stated honestly) |
| Explainable | Does not introduce opaque AI recommendations; N/A for ranking | **Pass** |
| Student privacy | First-party only; no free-text in analytics; hashes preferred | **Conditional** — retention & deletion not closed (see Reviews 4 & 7) |
| One Educational Truth | Explicit: analytics must not own mastery / relocate scoring | **Pass** |
| Final Test | Helps professionals via outcome-driven improvement | **Pass** |
| Never Build | Avoids gamification streaks, opaque AI, activity-as-success | **Pass** |
| Data principles (belongs to student; reproducible; auditable) | Stated intent; export/delete “must support” | **Conditional** — workflows not specified |

### Design-question mapping (Vision / Blueprint UX)

PRD §2 does not map to the four design questions. Instrumentation supports **“How am I progressing?”** and product improvement of **“What should I do now?”** indirectly. Acceptable for a non-learner-facing subsystem if amended to say so explicitly.

### Vision alignment score

**Aligned in intent. Not fully satisfied until privacy open questions close.**

---

## REVIEW 2 — Blueprint Alignment

**Authority:** `PRODUCT_BLUEPRINT.md`

| Blueprint theme | Assessment | Verdict |
|---|---|---|
| Outcomes before engagement | Matches; duration is derived context, not success | **Pass** |
| Evidence before opinion | Observes authorities; does not invent Twin beliefs | **Pass** |
| Digital Twin / Educational State | Read / hash only; no algorithm change | **Pass** |
| One Runtime / Navigation | Preserves legacy `/analytics` as shell | **Pass** |
| Roadmap (advanced analytics later) | Phase 1 = private-beta instrumentation, not Epic 4 warehouse | **Pass** |
| Terminology Mission / Session | Uses Session in narrative; `mission_id` in payloads | **Pass** if Product Language Guide respected in UI (none claimed) |
| Duplicated responsibility | Non-goals forbid replacing Student History / second brain | **Pass** |
| Conflicting objectives | **Issue:** §3 claims revision adherence; §6 omits revision events; §10 rollout validates O3 | **Fail (scope)** |

### Blueprint alignment score

**Consistent on strategy; inconsistent on Phase 1 scope vs stated educational benefits.**

---

## REVIEW 3 — Architecture Review

**Authorities:** Analytics Architecture, System Architecture, Twin docs, Educational Validation Framework, PRD template Twin/ESS forbidden-unless-authority rule.

| Claim to confirm | Finding | Verdict |
|---|---|---|
| EducationalStateService remains sole *unified educational read model* for experience | PRD: read / snapshot hash only; no contract rewrite | **Pass** (clarify wording: ESS assembles One Educational State; Twin/Evidence/Mission remain domain authorities — ESS is not “sole educational authority” for all beliefs) |
| Analytics only observe | Emit/summarise; append-only operational log | **Pass** (intent) |
| Analytics never calculate educational truth | Forbidden to relocate scoring; architecture test required | **Pass** (intent; must be enforced in tests) |
| Twin remains authoritative | No Twin math change; `twin.evolved` is observation | **Pass** |
| Recommendation engine unchanged | Explicitly out of Phase 1 (except optional Decision Journal thin emit) | **Pass** |
| ADR if new persistence | Required at implementation start | **Pass** (process) |
| Analytics Architecture open Q1–Q2 | Still listed as open in PRD §11 | **Fail (gate)** |
| Validation Framework Phase 1 freeze | Framework freezes O1, O2, **O3**, O7, **O8 acceptance** under PRD-001; PRD omits revision events and defers recommendation acceptance | **Fail (scope)** |

### Architecture clarification (required in PRD amendment)

Use precise language:

- **Twin / Evidence / Mission / Revision / Journey** — educational authorities for their domains.  
- **EducationalStateService** — sole assembler of the unified Educational State snapshot for experience surfaces.  
- **Analytics event store** — operational observation + aggregation only; never origin of mastery, readiness, or next action.

### Architecture score

**Sound boundaries; blocked by unresolved Analytics Architecture gate items and Framework scope mismatch.**

---

## REVIEW 4 — Data Governance

| Topic | PRD-001 state | Required for APPROVE | Verdict |
|---|---|---|---|
| Retention | **TBD**; beta default “18 months or account deletion” | Named schedule + legal basis for beta vs production | **Fail** |
| Consent | Not specified (invite-only beta implied) | Privacy notice: analytics events in-platform; purpose limitation | **Fail** |
| PII | Prefer IDs + hashes; no exam PII; no reflection free-text | Explicit PII inventory per event field | **Partial** |
| Hash vs payload | Deferred for `educational_state.snapshot` | **Decide** for Phase 1 (Architecture §9.2) | **Fail** |
| Aggregation | Reproducible, user-scoped | Define aggregation keys & founder rollup rules | **Partial** |
| Deletion policy | “Must support” student ownership | Document path (manual OK for beta) + cascade for event rows | **Fail** |
| Auditability | Append-only | Immutable writes, who can read aggregates, schema_version | **Partial** |

Analytics Architecture §8–§9 and Privacy Review checklist require these closed **before** collectors. Leaving them as “do not guess in code” is correct engineering hygiene but **insufficient for PRD approval**.

### Data governance score

**Not satisfied.**

---

## REVIEW 5 — Performance

PRD-001 contains **no** performance budget. Estimates below are review guidance for the amended PRD (not implementation).

| Concern | Estimate / risk | Guidance |
|---|---|---|
| Event overhead | ~1 synchronous insert per lifecycle point (Session start/complete, reflection, milestone) | Prefer same DB transaction as educational write, or async outbox; target **&lt;5 ms** p95 insert on staging |
| Snapshot cost | Hash-only: hash of serialised snapshot once per material ESS/Twin change | Avoid hashing on every page view; emit only on material evolution; target **&lt;20 ms** CPU for hash of typical snapshot |
| Payload snapshots | **High risk** if payloads stored — size & PII | Phase 1 should default **hash-only** unless Privacy proves need |
| Storage growth | Order: `O(sessions + reflections + milestones + twin evolutions)` per user | Beta 50 users × ~20 events/week × 18 months ≈ low tens of thousands of rows — fine; still need retention purge job |
| Request latency | If emit is inline and fails open vs fail closed | Must not add multi-hundred-ms to Session complete; feature-flag + fail-open logging acceptable for beta if educational commit already succeeded |
| Network impact | First-party only; no third-party beacon | **Negligible** external network |

### Performance score

**Unspecified in PRD — must add budgets before APPROVE.**

---

## REVIEW 6 — Security

| Topic | Assessment | Verdict |
|---|---|---|
| Sensitive data | Educational IDs + timestamps + hashes; reflection text excluded | **Good intent**; need field allowlist |
| Injection | ORM/bound params assumed; unknown event names rejected | **Pass** if write path validates enum + schema |
| Authentication | Implicit via existing `@login_required` lifecycle | **Pass** if no new public ingest endpoint |
| Authorisation | Founder aggregates role-gated; student own projections only | **Partial** — specify roles/capabilities |
| Tampering | Append-only not defined (who can UPDATE/DELETE?) | **Fail** — require no UPDATE; DELETE only via deletion workflow |
| Replay | Client-driven emit could duplicate Session completes | **Fail** — idempotency keys / dedupe on (event_type, entity_id, occurred_at) or server-side emit only |
| CSP / vendors | No third-party SDK | **Pass** |
| Secrets / egress | No new egress claimed | **Pass** |

GA security posture (RBAC, CSRF, headers) must be preserved; analytics must not introduce unauthenticated write APIs.

### Security score

**Insufficient threat controls in PRD — amend before APPROVE.**

---

## REVIEW 7 — Privacy

| Topic | Determination | Verdict |
|---|---|---|
| Minimum data collection | Phase 1 event set is mostly minimal; revision omission is scope issue, not privacy excess | **Conditional** |
| Retention schedule | Unresolved | **Fail** |
| Student visibility | Students do not see raw analytics; History remains projection | **Pass** (intent) |
| Export policy | Not specified | **Fail** — even manual beta export path required by Privacy Review |
| Deletion policy | Not specified beyond principle | **Fail** |
| Hash vs payload | Unresolved; hash-only is privacy-preferable | **Recommend hash-only for Phase 1** |
| Cross-border / DPA | Out of scope for multi-country 2030 — OK if limited to invite-only beta jurisdiction notice | **Note** |

Vision: “Student data belongs to the student. Privacy is not optional.”

### Privacy score

**Not satisfied for APPROVE.**

---

## REVIEW 8 — Test Strategy

PRD §9 is a starting point. Required strategy for amended PRD:

### Unit tests

- Event schema validation (required fields, enum event names, reject unknown).
- Idempotency / dedupe helpers.
- Hash computation stability (same snapshot → same hash).
- Duration derivation from start/complete timestamps.
- Privacy: serializers never include reflection free-text or exam PII fields.

### Integration tests

- Session complete path emits `session.completed` exactly once.
- Navigation-only views emit nothing.
- Reflection complete emits `reflection.completed` with flags, no body.
- Journey milestone emit on authoritative milestone only.
- ESS/Twin material change emits snapshot/evolved with hash only (once decision locked).
- AuthZ: student cannot read other users’ events; founder aggregate endpoints gated.

### Load tests

- Burst Session completions (e.g. 50 concurrent) — p95 educational path latency regression within Quality Manual soft budgets.
- Storage insert rate smoke on staging.

### Failure tests

- Event write failure after educational commit: educational outcome preserved; emit fail-open with structured log (policy explicit).
- Invalid payload rejected; no partial corrupt rows.
- Clock skew / duplicate submit does not double-count completion metrics.

### Regression tests

- Architecture: analytics packages must not import Twin mastery/readiness calculators to recompute truth.
- Sole runtime / Student History unchanged as learner surface.
- No recommendation ranking behaviour change.
- Curriculum V1/V2 traversal unaffected.

### Test strategy score

**Incomplete in PRD — expandable; not a sole blocker if other gates fixed.**

---

## REVIEW 9 — Risks

| Category | Risk | Likelihood | Impact | Mitigation (required in PRD) |
|---|---|---|---|---|
| Architectural | Analytics becomes second educational brain via “helpful” aggregates | Medium | High | Architecture tests; forbidden imports; One Educational Truth checklist |
| Architectural | Scope drift: recommendation/revision half-in Phase 1 | High | Medium | Align event list with Framework freeze or amend Framework |
| Operational | Event write failures silent → false educational validation | Medium | High | Monitoring, integrity checks, fail policy documented |
| Educational | Claiming O3/O8 validated without events | High | High | Fix scope; no V1 educational claims without data |
| Privacy | Retention TBD → over-retention or unlawful processing narrative | High | High | Close Q1; export/delete path |
| Privacy | Snapshot payloads store sensitive educational profiles | Medium | High | Phase 1 hash-only decision |
| Performance | Inline emit adds latency to Session complete | Medium | Medium | Budgets; same-txn or outbox; fail-open |
| Security | Client-replay doubles completions | Medium | Medium | Server-side emit + idempotency |
| Commercial | Premature “validated learning” marketing from incomplete instrumentation | Medium | High | V1 exit criteria; Framework sample floors |

---

## REVIEW 10 — Decision

### Options considered

| Option | When appropriate |
|---|---|
| **APPROVE** | Every governance requirement satisfied |
| **APPROVE WITH CHANGES** | Concept lawful; mandatory amendments before implementation |
| **REJECT** | Vision/Blueprint/Architecture conflict irreparable without different product |

### Recommendation

# APPROVE WITH CHANGES

**Not APPROVE:** privacy/data-governance gate items and Framework scope conflicts remain open; PRD template Risks/Metrics/DoD missing; security/performance underspecified.

**Not REJECT:** Problem statement, One Educational Truth posture, Twin/ESS non-modification, first-party constraint, and Vision Final Test alignment are sound.

### Mandatory changes before Status = Approved

1. **Close Analytics Architecture open questions for Phase 1**
   - Retention window + deletion workflow (beta vs production).
   - `educational_state.snapshot` / `twin.evolved`: **hash-only** (recommended) or justified payload with PII review.
2. **Align Phase 1 event catalogue with Educational Validation Framework freeze**
   - Either add `revision.planned` / `revision.completed`, **or** remove O3 from PRD educational-benefit and rollout validation claims and amend Framework §9 freeze text.
   - Either include thin `recommendation.*` / Decision Journal emit for O8, **or** amend Framework freeze so O8 acceptance is explicitly Phase 2 / PRD-002.
3. **PII field inventory** per event (allowlist).
4. **Consent / privacy notice** text for invite-only beta analytics purpose.
5. **Export + deletion** procedures (manual acceptable for beta; named owner).
6. **Security:** server-side emit preference, no UPDATE on event rows, idempotency/dedupe, AuthZ matrix for aggregate reads.
7. **Performance budgets** (insert overhead, snapshot hash cost, fail-open policy).
8. **Add PRD template sections:** Metrics, Risks, Definition of Done (and map Vision design questions in Student Benefit).
9. **Clarify architecture wording:** ESS = sole unified snapshot assembler; Twin/Evidence/Mission remain domain authorities; analytics never authoritative.
10. **Role approvals** completed in §12 (Product, Architecture, Privacy, Educational) after amendments.

### Optional (non-blocking) improvements

- Companion `EVENT_CATALOGUE.md` draft linked from PRD.
- Explicit feature-flag name and rollout metric.
- Reference Quality Manual educational-validation release gate.

### Implementation ban

**Confirmed:** Do not implement. Do not generate events. Do not modify runtime code until PRD-001 reaches **Approved** after the mandatory changes above.

---

## Traceability

| Governance artefact | Used in |
|---|---|
| PRODUCT_VISION_2030 | Review 1 |
| PRODUCT_BLUEPRINT.md | Review 2 |
| PRODUCT_ANALYTICS_ARCHITECTURE.md | Reviews 3–4, 7, 10 |
| EDUCATIONAL_VALIDATION_FRAMEWORK.md | Reviews 3, 9, 10 |
| SYSTEM_ARCHITECTURE / Twin docs | Review 3 |
| PRIVACY_REVIEW.md (private beta) | Reviews 4, 7 |
| SECURITY_REVIEW.md (GA) | Review 6 |
| QUALITY_MANUAL / PRD_TEMPLATE | Reviews 5, 8, 10 |
| GOVERNANCE.md | Decision hierarchy |

---

**Review status:** Complete  
**Next action:** Amend PRD-001 per mandatory changes → re-review delta → approve roles → then implementation milestone.
