# CQ-007 — Engineering Readiness

**Programme:** CQ-007 — Internal Alpha Readiness Review  
**Release Candidate:** `RC-2026.07.29-01`  
**Date:** 2026-07-29  
**Verdict:** **Ready for Internal Alpha** (conditions tracked; no P0)

---

## Scope

Engineering assessment of publication pipeline, student discovery, authority, validation, and reliability using prior programme evidence only.

---

## Publication pipeline

| Stage | Status | Evidence |
|---|---|---|
| Draft → Validated | Pass | EV-001; FV-001B Final on RC |
| Validated → Preview Ready | Pass | Same |
| Preview Ready → Approved | Pass | Same |
| Approved → Published | Pass | Same |
| Published → Ready (Subjects) | Pass | Ready · Current Version · Published Date |

**Authority chain (PI-002R):**

```text
Official Documents → CIP Extraction → Structure Preparation
    → Management Validation (publication gate)
    → Preview → Approval → Publication → Subject Catalogue Ready
```

**Prior failure (PI-002):** Studio AND-gated a synthetic Ingestion stub against CIP-extracted structure, so `validation_passed` never became true. **Remediated in PI-002R.** Stub ingestion no longer starts on reference-only upload; non-authoritative jobs are ignored at the publication gate.

**EV-002 note:** An earlier FV-001B Final NO-GO reflected a stale Flask process / polluted DB (Case D), not residual pipeline failure on the post–PI-002R image. RC-001 + FV-001B Final on RC supersede that NO-GO for Alpha judgement.

---

## Student discovery

| Check | Status | Evidence |
|---|---|---|
| Ready package materialised | Pass | EV-001; FV-001B Subjects Ready |
| Choose Exam loads (no 500) | Pass | EE-001 + FV-001C |
| Ready subject visible with version / date | Pass | FV-001C CS1V · 2026.1 · Updated 28 Jul 2026 |
| Subject selectable | Pass | FV-001C wizard advance |

EE-001 cleared EV-001’s `_format_release` `AttributeError` (authority `published_at` as ISO string). Publication pipeline code was not changed by EE-001.

---

## Authority

| Claim | Status | Evidence |
|---|---|---|
| Exactly one authoritative curriculum representation for Founder publication | Pass | PI-002R; EV-001 identity verification |
| Validation / Preview / Approval / Publication / Ready consume it | Pass | PI-002R exit criteria; EV-001 |
| No synthetic placeholder curriculum in publication gate | Pass | PI-002R |
| Publication safety gates intact | Pass | PI-002R regression (372 tests); EV-001 UI gate probes |

Curriculum identity on happy path: `CS1V` → workspace → Foundation version `2026.1` → active published package.

---

## Validation

| Claim | Status | Evidence |
|---|---|---|
| Management ValidationPolicy is the Founder publication gate | Pass | PI-002R Validation Authority Decision |
| Validate succeeds on RC with Official CMP + Syllabus | Pass | FV-001B Final |
| Findings projection maps `issues[]` | Pass | PI-002R |
| Validate without documents fails honestly | Pass | EV-001 regression probes |

**Residual (non-blocking):** Findings panel can still show a non-blocking learning-objectives reference while Validation status says passed / 0 errors (FV-001B UX-02). Does not prevent Approve/Publish on RC.

---

## Reliability

| Claim | Status | Evidence |
|---|---|---|
| Publish without approval refused | Pass | EV-001 / PI-002R |
| Approve without validation refused | Pass | Same |
| Preview without structure not ready | Pass | Same |
| Ready state durable after Publish | Pass | EV-001 package; FV-001B Subjects row |
| Environment reproducibility | Pass with conditions | RC-001 digest-bound RC |

**Reliability residual:** Long-lived Flask without reload caused false NO-GO historically (EV-002). Alpha operators must bind to certified runtime/DB or restart with documented identity — see RC certificate conditions.

---

## Operational posture (invite-only Alpha)

CQ-007 did not re-execute deployment drills. Inherited operational evidence:

| Area | Evidence inheritance | Alpha adequacy |
|---|---|---|
| Logging | `knowledge/release/OBSERVABILITY_GUIDE.md`; privacy-safe pipeline events | Adequate for invite-only |
| Error handling | Studio flash recovery (Approve vs Publish); standard Flask error pages | Adequate; findings honesty residual is product P1 |
| Recovery | Prior sole-runtime / session resume playbooks; GA recovery tests historically green | Adequate |
| Deployment | RC-001 local Flask certification + `/health` identity | Adequate for local/RC Alpha; host parity is a tracked risk |
| Rollback | Documented flag / sole-runtime / prior baseline rollback notes | Adequate without live commercial drill |
| Monitoring | `/health`, `/health/ready`, `/health/educational-intelligence` | Adequate for Alpha; continuous external monitoring not a gate |

Operational gaps are **P2**, not Alpha blockers. See [`KNOWN_ISSUES.md`](KNOWN_ISSUES.md) and [`RISK_REGISTER.md`](RISK_REGISTER.md).

---

## Engineering readiness summary

| Area | Ready for Alpha? | Blocks Alpha? |
|---|---|---|
| Publication pipeline | Yes | No |
| Student discovery | Yes | No |
| Authority | Yes | No |
| Validation | Yes (trust chrome P1) | No |
| Reliability | Yes (ops discipline P1) | No |
| Operational (invite-only) | Yes (monitoring/rollback P2) | No |

**Engineering conclusion:** Engineering is ready for Internal Alpha on **Release Candidate: RC-2026.07.29-01**.
