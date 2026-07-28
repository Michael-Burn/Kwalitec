# CP-001 — Decision Journal Privacy Model

**Programme:** CP-001 — Capability Programme  
**Version:** 1.0  
**Status:** Active — privacy architecture (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP001_DECISION_JOURNAL_ARCHITECTURE.md`, `CP001_DOMAIN_MODEL.md`  
**Constraint:** No retention jobs, erasure UX, schema, or analytics pipelines modified by this programme.

---

## 1. Purpose

Define **privacy boundaries, sensitivity classes, retention, consent, and research-extract rules** for the Decision Journal capability so educational continuity does not become surveillance, coercion, or silent exfiltration.

Aligned with Vision data principles, OM-001 Measurement Standard §10, Product Analytics privacy posture, and ILE-002 retention baseline.

---

## 2. Privacy principles

| # | Principle | Rule |
|---|-----------|------|
| **DJ-P1** | Student ownership | Journal data is personal educational data scoped to the learner |
| **DJ-P2** | Minimisation | Record significant decisions only — never clickstream in the journal |
| **DJ-P3** | Purpose limitation | Use for continuity, agency, explainability, and lawful OM measurement — not ads or opaque vendor profiling |
| **DJ-P4** | Agency without punishment | Defer / reject / dismiss must not create punitive scores or shame artefacts |
| **DJ-P5** | Sensitivity elevation | Reflection free text and open rationales are elevated sensitivity |
| **DJ-P6** | Transparency | Student can read their journal; exports prefer student-safe narratives |
| **DJ-P7** | No silent purge | Do not delete educational memory for storage hygiene without a lawful erasure path |
| **DJ-P8** | Research separation** | Research extracts use opaque keys; L4 exam linkage requires explicit consent |

---

## 3. Data classes

| Class | Examples | Default handling |
|-------|----------|------------------|
| **DJ-A Operational educational memory** | GuidanceSnapshot, disposition, timestamps, curriculum refs, Mission links | Account-lifetime retention; student-readable |
| **DJ-B Structured rationale tags** | TIME, ENERGY, PLAN_CONFLICT, … | Account-lifetime; preferred Twin/ops input over free text |
| **DJ-C Free-text rationale** | Open “why I deferred” | Elevated; default exclude from Twin and research extracts |
| **DJ-D Reflection content** | Guided reflection free text / summaries | Elevated; OM-REF sensitivity; default non-Twin until ADR + consent model |
| **DJ-E Measurement metadata** | EvaluationStub, metric membership flags | Ops; no PII beyond learner key |
| **DJ-F Out of journal** | Clickstream, item traces, raw telemetry | Must not enter Decision Journal (separate analytics retention) |

---

## 4. Access boundaries

| Actor | May | Must not |
|-------|-----|----------|
| **Student (owner)** | Read chronology; export backup; soft-archive visibility | Access another learner’s journal |
| **Authenticated services (same user)** | Write eligible entries; append evidence; record choice | Cross-user joins without ownership checks |
| **Operators / support** | Level-3 diagnostic behind operator auth when lawfully needed | Browse free-text reflection casually; export PII to vendors |
| **Research / trials** | Aggregates / opaque-key extracts under protocol | Personal identifiers on trial DTOs; silent free-text export |
| **Third-party AI vendors** | None by default | Receive journal bodies without security/privacy review |

Authorization posture matches product security rules: scope queries to current user; 403/404 without leaking foreign resource existence.

---

## 5. Consent and lawful use

| Use | Consent / basis posture (design) |
|-----|----------------------------------|
| In-product Decision Journal for study continuity | Covered by product educational service / privacy notice for invite cohort |
| Structured tags → Twin behaviour inputs | Prefer disclose in privacy notice; no free text by default |
| Free text → Twin | **Requires explicit consent + ADR** (default OFF) |
| Free text / reflection → research extracts | **Requires protocol consent** |
| Exam outcome linkage (L4) | **Explicit consent + Privacy Owner capacity review** (OM-001) |
| Analytics event mirroring | Obey Product Analytics flags / privacy filters; journal ≠ analytics outbox |

CP-001 does not invent a new consent UI. Future privacy programmes own UX.

---

## 6. Retention policy (architecture)

Builds on ILE-002 `RETENTION_POLICY.md` without amending application behaviour here.

| Artefact | Default retention | Notes |
|----------|-------------------|-------|
| DecisionRecords + EvidenceEvents | Life of learner account | Soft archive never deletes |
| Structured rationale tags | With parent record | |
| Free-text rationale / reflection | With parent record until erasure programme | Elevated care on export |
| Soft-archived entries | Remain readable | Filterable; not destructive |
| Measurement aggregates | Per OM / analytics retention windows | Prefer opaque keys |

### 6.1 Continuity vs plan deletion

Journal rows are keyed by learner identity, **not** study-plan id. Plan deletion must not erase educational memory (Educational Continuity).

### 6.2 Erasure

Account-level erasure (when productised) must treat journal rows as personal educational data. Until an explicit privacy programme defines erasure UX and legal basis handling:

- Do **not** silently purge for hygiene.  
- Soft archive is **not** erasure.  
- Backup/export inclusion remains a student-control affordance (ILE-002 settings backup list posture).

### 6.3 Relationship to analytics retention

Product Analytics raw events may follow separate windows (e.g. 18-month patterns in analytics ops). Decision Journal educational memory is **not** governed by analytics raw retention by default — different purpose, different class.

---

## 7. Twin and recommendation boundaries

| Boundary | Rule |
|----------|------|
| Preference ≠ mastery | Journal dispositions never mutate Estimated Knowledge |
| Behaviour only | Twin may consume structured disposition/tag signals as Behaviour domain inputs |
| No psych profiling | Free text must not train opaque personality models |
| No coercion metrics | Acceptance rate must not become a student “compliance grade” in UI |
| Recommendation engines | May read aggregate quality signals via OM packs — not punish individuals for reject |

---

## 8. Research and OM extracts

Aligned with OM Measurement Standard §10:

1. Prefer opaque student keys (`trialstu-…` pattern or equivalent).  
2. No personal identifiers on trial observation / advisory outcome DTO surfaces.  
3. Reflection / free-text default **excluded** from extracts.  
4. Exam outcome linkage requires consent + capacity review.  
5. Provenance ids (decision_id, recommendation_ref) allowed when non-identifying in combination with policy.  
6. Metrics must not create coercive gamification Vision forbids.

---

## 9. Security notes (architecture)

| Topic | Posture |
|-------|---------|
| Secrets | None in journal bodies; secrets stay in env |
| Logging | Do not log free-text reflection or full journal payloads in application logs |
| CSRF / auth | Future write endpoints remain login-required, CSRF-protected, user-scoped |
| SQL | ORM / bound params only — never concatenate user rationale into SQL |
| CSP / third-party | No silent CDN exfiltration of journal content |

CP-001 does not change `app/__init__.py` security headers or auth routes.

---

## 10. Incident classes (design)

| Incident | Example | Response posture |
|----------|---------|------------------|
| Cross-user leak | Journal id guessable across users | Security incident; ownership fix |
| Reflection over-persistence | Free text written where policy forbade | OM-REF-03; privacy review |
| Vendor exfiltration | Journal body sent to opaque LLM API | STOP; security/privacy review |
| Coercion theatre | UI shames reject rate | Product Constitution PC-01/PC-11 violation |
| Silent purge | Cron deletes journal for disk | Forbidden without erasure programme |

---

## 11. Explicit non-goals

- Implementing retention cron or erasure UX in this programme  
- Amending analytics privacy code  
- Declaring GDPR/legal sufficiency (legal review remains separate)  
- Enabling Twin free-text ingestion  

---

**End of CP001_PRIVACY_MODEL**
