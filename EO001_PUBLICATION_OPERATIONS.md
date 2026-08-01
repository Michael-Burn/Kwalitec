# EO-001 — Publication Operations

**Programme:** Educational Operations Programme EO-001 — Educational Publishing Operations  
**Status:** Binding — roles, authorities, and day-to-day publishing operations  
**Effective:** 2026-08-01  
**Authority:** EA-001 through EA-008 COMPLETE · EP-001 PASS  
**Nature:** Publishing operations law — not educational architecture redesign, not application code, not Runtime/SCI work, not educational content authoring  
**Parents:** `EO001_PUBLISHING_WORKFLOW.md` · `EO001_EDUCATIONAL_VOLUME_STANDARD.md` · `EO001_VERSIONING_GUIDE.md`  
**Reference quality bar:** Campaign Alpha (`CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0`)  

---

## 1. Purpose

Define how Educational Publishing Operations are **staffed, authorised, handed over, and run day to day** so Volumes remain at Campaign Alpha quality across years of production.

This document answers:

- Who does what?  
- Who may approve what?  
- When may a role hand work to another?  
- How are revision requests, errata, retirement, and archive operated?  

---

## 2. Operational roles

### 2.1 Role catalogue

| Role | Primary duty | Commercial Volume required? |
|------|--------------|----------------------------|
| **Educational Author** | Drafts Campaigns/packages and Volume Dossier workfile; patches defects | Yes (Author of Record) |
| **Educational Reviewer** | Peer Review of substance, craft, and Tutor Voice continuity | Yes (independent of sole Author) |
| **Academic Auditor** | Educational Audit of evidence, continuity metrics, trust regression, dossier honesty | Yes |
| **Founder** | Catalogue-bar judgement; commissions Volumes; acknowledges retirements | Yes (or Gate Owner designate) |
| **Publication Approver** | Final human APPROVED / REJECTED / PARTIAL HOLD / HOLD / RETIRED | Yes |
| **Future Subject Lead** | Series stewardship within charter once staffed; may commission within charter | Optional until staffed |
| **Maintenance Owner** | Watches triggers; opens revision requests; schedules recertification | Yes for released Volumes |
| **Quality Gate Owner** | Confirms nested gate evidence still valid | Yes at certification/approval |

EVF / validators may **FAIL** a published experience. They may **not** alone APPROVE Volume publication.

### 2.2 Separation of duties (commercial Volumes)

| Rule | Requirement |
|------|-------------|
| SD-01 | Author of Record ≠ Publication Approver |
| SD-02 | Prefer Author ≠ Educational Reviewer ≠ Academic Auditor |
| SD-03 | Prefer Academic Auditor ≠ Publication Approver |
| SD-04 | At minimum **two human signatures** on the certification-to-approval pack (EP/EA posture retained) |
| SD-05 | Founder may act as Tutor/Founder reviewer early; still should not be sole Approver when staffing allows |

When staffing is thin, document the dual-hat explicitly in the Approval record. Dual-hat is a **risk acknowledgement**, not a waiver of Alpha floor.

---

## 3. Approval authority matrix

| Decision | Educational Author | Educational Reviewer | Academic Auditor | Founder | Publication Approver | Subject Lead |
|----------|:------------------:|:--------------------:|:----------------:|:-------:|:--------------------:|:------------:|
| Open Authoring workfile | R | C | — | A (commission) | — | A (if chartered) |
| Declare Peer Review PASS | C | **A** | I | I | — | I |
| Declare Educational Audit PASS | C | C | **A** | I | — | I |
| Declare Founder Review PASS | C | I | C | **A** | I | C |
| Publication APPROVED / REJECTED / PARTIAL HOLD | C | I | C | C | **A** | C |
| Immediate HOLD / unpublish | I | I | C | C | **A** | C |
| Accept E1 errata notice | C | **A** | I | I | I | I |
| Accept E2 errata patch | C | C | C | I | **A** | C |
| Accept E3 emergency errata | C | C | C | C | **A** | C |
| Commission Replacement Volume | C | I | I | **A** | I | A (if chartered) |
| Sign RETIRED | C | I | C | **C/A** | **A** | C |
| Archive Acceptance | I | I | C | I | **A** | I |
| Marketing claim beyond claims-allowed | — | — | — | **A** deny | **A** deny | deny |

**Legend:** R = Responsible · A = Accountable (signs) · C = Consulted · I = Informed · — = not in path.

**Hard rule:** Only the Publication Approver may grant commercial student-pathway publication authority for a Volume version.

---

## 4. Handover criteria

A stage may hand to the next only when exit criteria are met and evidence is filed in the Volume Dossier.

### 4.1 Handover table

| From → To | Exit evidence | Receiver may refuse if |
|-----------|---------------|------------------------|
| Commission → Authoring | Commission brief; scope class; pins | Scope dishonest / FP-01 proposed |
| Authoring → Peer Review | AU-01…AU-06; Alpha self-check | Incomplete inventory; missing self-checks |
| Peer Review → Educational Audit | PR PASS + defect log closed | Nested EA-002 FAILs open |
| Educational Audit → Founder Review | Audit PASS; CI/bridges; claims draft | Evidence pack incomplete or inconsistent |
| Founder Review → Publication Approval | Founder PASS; catalogue-bar notes | Honesty / series-fit FAIL |
| Publication Approval → Release gate | APPROVED record; activation deps listed | Approval missing or PARTIAL HOLD misused |
| Release → Post-publish verification | Release stamp; inventory match | Inventory drift |
| Any → HOLD | Trust FAIL evidence | — (Approver may force) |
| Retirement → Archive | Retirement signature + redirect plan | Evidence pack incomplete |

### 4.2 Refusal protocol

Receiver returns work with:

1. Failed criterion IDs  
2. Defect severity  
3. Required return stage  
4. Whether Volume status must move to `hold` or remain `in_review`  

Silence is not acceptance. Handover requires explicit PASS/ACCEPT notation.

---

## 5. Day-to-day operating cadence

### 5.1 While producing a Volume

| Cadence | Activity |
|---------|----------|
| Continuous | Author maintains dossier + defect log |
| Per package | Nested gate desk certification |
| Per Campaign | Gate CG worksheet |
| Per Volume | Peer → Audit → Founder → Approver sequence |
| Before Approver | Publication Readiness pack (EP-001 pattern) |

### 5.2 While a Volume is released

| Cadence | Activity | Owner |
|---------|----------|-------|
| Continuous | Trigger watch (CMP, trust, bridges, complaints) | Maintenance Owner |
| Per incident | Revision request triage | Per severity matrix |
| Per CMP edition rumour / confirm | Dependency impact scan | Auditor + Author |
| Per longitudinal sample | EA-007-method spot journey | Auditor / EVF |
| Per edition planning cycle | Series roadmap vs Alpha bar | Founder / Subject Lead |

### 5.3 Status board (minimum fields)

Every active Volume appears on an operations status board with: `volume_id`, version, status, scope class, Gate CG, Approver state, activation state, open errata count, next review date.

---

## 6. Revision request operations

### 6.1 Intake fields

| Field | Required |
|-------|----------|
| `revision_request_id` | Yes |
| Source (student, Board, EVF, CMP, engineering, author) | Yes |
| Volume + version | Yes |
| Description + evidence | Yes |
| Suspected EV-001 / FP class if any | If known |
| Urgency | Yes |

### 6.2 Triage outcomes

| Outcome | When | Next |
|---------|------|------|
| **Reject** | Not a defect; out of scope; duplicate | Close with rationale |
| **Defer** | Real but scheduled into next edition | Link to edition plan |
| **Errata** | Released Volume; notice or patch path | Errata workflow |
| **Accept** | Requires versioned work | Assign change class; re-enter lifecycle |

### 6.3 Re-entry map

| Change class | Re-enter at |
|--------------|-------------|
| Cosmetic | Peer Review abbreviated → Approver note if already released |
| Educational | Authoring → Peer → (Audit if Auditor requires) → Approver |
| Structural | Authoring → full Peer → Educational Audit → Founder if arc reshaped → Approver |
| Truth-risk | HOLD first → Authoring → full chain including Founder → Approver |
| Retirement / Replacement | Commission Replacement or Retirement proposal |

---

## 7. Errata operations

### 7.1 Opening errata

1. Maintenance Owner or Approver opens `errata_id`.  
2. Severity class E1 / E2 / E3 assigned (`EO001_PUBLISHING_WORKFLOW.md` §14).  
3. Volume status may move to `errata_open` (required for E2/E3).  
4. Student-visible notice drafted when exposure continues.

### 7.2 Closing errata

| Class | Close when |
|-------|------------|
| E1 | Notice published + tracked for next minor |
| E2 | Patch version APPROVED + released + PV checks |
| E3 | HOLD cleared only after full recertify + Approver restore |

### 7.3 Errata vs new edition

Prefer errata when:

- Defect is localised  
- Scope class and Campaign membership unchanged  
- Alpha floor not structurally threatened  

Prefer new edition / Replacement when:

- CMP edition pin changes  
- Membership span changes  
- Continuity redesign required  
- Honesty claims must be rewritten at catalogue level  

---

## 8. Retirement, replacement, and archive operations

### 8.1 Retirement runbook

1. Open Retirement Proposal citing RT-01…RT-05.  
2. Impact inventory: pathways, dependent Volumes, in-flight students.  
3. Choose Replacement redirect **or** honest unavailable.  
4. Founder acknowledgement (commercial).  
5. Publication Approver signs RETIRED.  
6. Remove from student-reachable inventory.  
7. Update status board + claims registry.  
8. Submit Archive Acceptance pack.

### 8.2 Replacement runbook

1. Commission Replacement Volume (Stage 0).  
2. Produce to full lifecycle (no fast-track that skips Audit/Founder for commercial).  
3. On APPROVED+released: mark prior Volume `superseded`.  
4. Complete retirement of prior when redirect stable.  
5. Archive both with bidirectional links.

### 8.3 Archive pack (minimum)

- Final dossier snapshot  
- Approval history  
- Errata history  
- Retirement / supersession record  
- Membership version pins  
- Claims history  
- Alpha-bar comparison at last PASS  

---

## 9. Future Subject Lead — charter

When staffed, the **Subject Lead**:

| May | May not |
|-----|---------|
| Commission Volumes inside an approved subject series charter | Lower Alpha floor |
| Own series roadmap and sequence_in_series | APPROVE commercial publication alone |
| Act as consulted party on Audit/Founder packs | Bypass Publication Approver |
| Nominate Reviewers / Authors for the subject | Unpublish without Approver (except emergency escalate) |
| Refuse handover for series-fit collisions | Rewrite EA educational law by operations memo |

**Handover into Subject Lead existence:** Founder issues a Series Charter naming subject, reference bar, scope-class allowances, and Approver identity. Until then, Founder retains commission authority.

---

## 10. Campaign Alpha as operating template

EP-001 demonstrated the production pattern EO now industrialises:

| EP-001 artefact | EO operations analogue |
|-----------------|------------------------|
| Campaign Authoring | Authoring stage + dossier |
| Tutor Review | Peer Review (voice) |
| Certification / Auditor | Educational Audit |
| Founder Review | Founder Review |
| Publication Readiness | `publication_ready` + Approver worksheet |
| Catalogue-certified, pathway-gated | Status honesty (`approved` ≠ `released`) |

New Volumes should produce an equivalent evidence set, filed under Volume identity — not ad-hoc chat memory.

---

## 11. Non-goals (operations boundary)

Publication Operations do **not**:

- Redesign Runtime A/C, SCI, Twin, or recommendations  
- Author educational content in this programme  
- Amend EA-001–EA-008 educational architecture text  
- Treat technical CI green as educational PASS  
- Grant marketing permission beyond claims-allowed  

---

## 12. Closing rules

1. Roles are accountable by signature, not by title proximity.  
2. Handover is evidence-gated.  
3. Revision, errata, retirement, replacement, and archive are operated — not improvised.  
4. Subject Lead inherits charter, not unlimited authority.  
5. The Publication Approver remains the final commercial exposure authority.

**Operations exist so excellence survives the people who first produced it.**

Signed notionally: Editorial Director · EO-001 · Publication Operations · 2026-08-01
