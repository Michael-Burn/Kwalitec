# OP-001 — Student Support Protocol

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `SUPPORT_WORKFLOW.md` · `ISSUE_REPORTING.md` · `FEEDBACK_SYSTEM.md` · Privacy Review (OR-01) · EF-001

**Defines human support operations.** Does not add in-product support features, change educational packages, or modify Recommendation / Twin / Runtime.

---

## 1. Purpose

Give Early Access students a clear, honest path for bugs, questions, and incidents — with severity, SLAs, and escalation — without turning support into a product redesign programme.

---

## 2. Support ownership

| Role | Responsibility |
|------|----------------|
| **Early Access operator** | Intake, triage, first response, logging |
| **Founder** | P0 ownership; policy; invite/withdrawal exceptions; EF-001 checks |
| **Engineering (if engaged)** | Defect fixes under normal PR standards — **not** authorised by OP-001 to ship educational/algorithm changes |

Until a dedicated support hire exists, Founder may be the operator.

---

## 3. Intake channels

| Channel | Allowed for |
|---------|-------------|
| Reply to invite / welcome / support inbox | Bugs, questions, feature ideas, withdrawal, privacy requests |
| In-product feedback path (if already present) | Same — do not build new surfaces in OP-001 |
| Scheduled check-in / interview | Qualitative notes — separate from P0/P1 incidents |

**Record:** Pseudonymous ID, timestamp, channel, category, severity, status. PII stays in ops store.

---

## 4. Categories

### 4.1 Bug reporting

Student reports something broken or incorrect.

**Ops intake fields:**

- What were you trying to do?  
- What did you expect?  
- What happened instead?  
- When (date/time, timezone)?  
- Device / browser if known  
- Screenshot optional  
- Blocking study? (Y/N)

**Triage:** Reproduce if possible → severity → respond within SLA → fix or document → confirm with reporter.

**Hard rule:** Suspected educational-algorithm “bugs” that are actually design disagreements → **document only**; do not change Recommendation / Twin / Runtime / packages under OP-001. Apply EF-001 operational review if proposing product change later.

### 4.2 Feature requests

Ideas and enhancements.

- Thank the student.  
- Classify **P3** unless Founder elevates.  
- Batch weekly.  
- Do **not** promise delivery.  
- Do **not** treat requests as EF unfreeze justification without EF-001 review.

### 4.3 Student questions

How do I…? What does this mean? What should I study?

- Answer with **product-as-is** guidance (Home, Today’s Session, existing surfaces).  
- Do not invent new curriculum advice outside product.  
- Do not guarantee exam outcomes.  
- If question reveals UX confusion: log as P2 observation for later programmes — **no redesign in OP-001**.

### 4.4 Privacy / data requests

Export, deletion, consent withdrawal — follow Privacy Review SLAs (export **14 days**; analytics delete **30 days** after verified request, per Stage 1 pack). Escalate identity verification carefully.

---

## 5. Incident severity

| Severity | Definition | Examples |
|----------|------------|----------|
| **P0** | Security, privacy breach, data loss, account takeover, unlawful disclosure | Credential leak; another student’s data visible; production data wipe |
| **P1** | Cannot study / cannot access essential path | Login failure; session hard-broken; wrong student data on screen; cannot start Session |
| **P2** | Confusing or degraded but workaround exists | Unclear recommendation copy; navigation confusion; non-blocking UI glitch |
| **P3** | Suggestion, polish, non-urgent idea | Feature wish; copy nit; “would be nice if” |

If unsure between P1 and P2: ask “Can the student complete a study Session today with a reasonable workaround?” If **no** → P1.

---

## 6. Response SLA

| Severity | First response | Mitigation / resolution target (Early Access) |
|----------|----------------|-----------------------------------------------|
| **P0** | **Immediate** (best effort within 1 hour waking; asap overnight) | Contain immediately; Founder-led; written incident note same day |
| **P1** | **Same business day** | Restore study path as soon as practical; daily updates if open |
| **P2** | **1–2 business days** | Fix or document; close or defer with note |
| **P3** | **Weekly batch** | Acknowledge in batch; no delivery promise |

Business day = operator’s working calendar (state explicitly in welcome email if timezone-specific).

---

## 7. Escalation flow

```text
Intake
  → Operator triages severity + category
      → P0: notify Founder immediately; contain; privacy/security actions
      → P1: operator owns; escalate to Founder if blocked >1 business day
      → P2: operator owns; weekly summary to Founder
      → P3: weekly batch to Founder
  → If product defect fix needed: normal engineering path (out of OP-001 scope to implement)
  → If educational / Recommendation / Twin / Runtime change requested:
        STOP product change → EF-001 operational review template → Founder
  → Confirm outcome with student
  → Log under evidence support/ + incidents/ (pseudonymous)
```

**Kill criteria for unsafe continue:** Founder may pause invites or revoke access if P0 uncontained or trust irreparably broken.

---

## 8. Logging and evidence

| Artefact | Location |
|----------|----------|
| Bug tickets (ops) | Ops store + optional pointer in `knowledge/evidence/releases/OP001/support/bugs/` |
| Feature requests | `…/support/feature_requests/` |
| Questions log | `…/support/questions/` |
| Incidents (P0/P1) | `…/incidents/` and/or `…/support/incidents/` |

**Never** commit passwords, session cookies, full raw emails, or other students’ PII.

---

## 9. Student-facing support promise (copy constraints)

When describing support to students:

- Be reachable and honest about Early Access.  
- State SLAs at a high level (security immediate; can’t-study same day).  
- Do **not** claim 24/7 enterprise support unless true.  
- Do **not** claim the product is production-ready or Version 1 released.

---

## 10. Relationship to private beta docs

This protocol **governs Early Access cohort 1 support**. Detailed historical process notes remain in:

- `knowledge/product/private_beta/SUPPORT_WORKFLOW.md`  
- `knowledge/product/private_beta/ISSUE_REPORTING.md`  
- `knowledge/product/private_beta/FEEDBACK_SYSTEM.md`  

If conflict: **OP-001** wins for Early Access ops until Founder revises.

---

## 11. STOP

Support channels may be prepared before invites.  
Live external support load begins only after Founder-authorised invitations.

Signed: OP-001 Student Support Protocol · 2026-08-04
