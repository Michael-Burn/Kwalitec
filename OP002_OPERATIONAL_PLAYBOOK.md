# OP-002 — Operational Playbook

**Programme:** OP-002 — Early Access Pilot Operations  
**Version:** 1.0  
**Status:** TABLETOP REHEARSAL COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `OP001_EXECUTION_CHECKLIST.md` · `OP001_RECRUITMENT_PROTOCOL.md` · `OP001_ONBOARDING_PROTOCOL.md` · `OP001_STUDENT_SUPPORT_PROTOCOL.md` · KSI-002 · Educational Content Freeze · EF-001

**This playbook is a rehearsal artefact.** It does not recruit, invite, provision external accounts, or change Kwalitec, Runtime, Educational Packages, Recommendation Engine, or Student Twin.

---

## 1. Purpose

Walk the complete Early Access lifecycle as a **tabletop exercise** so every stage has a known owner, artefact set, decision gate, failure modes, recovery, and escalation **before** the first external participant is invited.

---

## 2. Roles (standing)

| Role | Owner in cohort 1 |
|------|-------------------|
| **Founder** | Invite-send authorisation; P0; withdrawals exceptions; EF-001 checks; cohort stop |
| **Early Access operator** | Intake, triage, funnel, chase, logging (may be Founder until a hire exists) |
| **Engineering** | Defect fixes only under normal PR path — **not** authorised by OP-002 to ship educational/algorithm changes |
| **Study authority** | Post-ops KSI observation / scorecards (successor programme — not OP-002) |

---

## 3. Hard gates (do not skip)

| Gate | Required before |
|------|-----------------|
| G-OP001 | Founder approval of OP-001 package |
| G-OP002 | Founder approval of OP-002 rehearsal package (this programme) |
| G-INVITE | **Separate** dated Founder invite-send authorisation |
| G-CONSENT | C1 Privacy + C2 Measurement recorded before any KPI inclusion |
| G-PAUSE | Founder may pause invites on uncontained P0 or support overload |

---

## 4. Lifecycle stages (tabletop)

For each stage: expected action · responsible owner · required artefacts · decision point · failure modes · recovery · escalation.

### 4.1 Invitation

| Field | Content |
|-------|---------|
| **Expected action** | After G-INVITE: provision invite-only accounts; send Invitation template (§1) with Stage 1 Privacy Notice + consent prompts; mark dashboard **Invited**; log send (template version + date + pseudonymous ID) |
| **Responsible owner** | Operator executes; Founder authorises list and send |
| **Required artefacts** | Final invite list (ops store); provisioned accounts (no credentials in git); `OP001_COMMUNICATION_TEMPLATES.md` §1; send log pointer under `communications/sent_log/`; dashboard Invited count |
| **Decision point** | Founder confirms final invite list and dated invite-send authorisation |
| **Failure modes** | Invite never sent (R-02); wrong recipient; credentials in git; claim-discipline breach in copy; Invited counted before email actually sent |
| **Recovery procedure** | Halt further sends; correct list; revoke/rotate exposed credentials; re-send only with Founder OK; correct dashboard honesty |
| **Escalation path** | Operator → Founder same day if send blocked >24h after G-INVITE |

---

### 4.2 Acceptance

| Field | Content |
|-------|---------|
| **Expected action** | Record acceptance reply/form + timestamp; confirm account reachable; send Acceptance email; update dashboard **Accepted** (= ITT-Accepted) |
| **Responsible owner** | Operator |
| **Required artefacts** | Acceptance timestamp in enrollment register; Acceptance template send; dashboard Accepted |
| **Decision point** | Is this person external ITT-Accepted (not Stage 0 / duplicate / failed registration)? |
| **Failure modes** | Soft “interested” without clear accept; duplicate account; staff counted as external; Accepted without reachable account |
| **Recovery procedure** | Clarify accept language; merge duplicates (earliest ID); exclude Stage 0; fix access before counting |
| **Escalation path** | Ambiguous eligibility → Founder before counting toward N≥5 |

---

### 4.3 Consent

| Field | Content |
|-------|---------|
| **Expected action** | Capture C1 Privacy + C2 Measurement (required); offer C3 Interview / C4 Quote (optional); record in ops consent log; chase incomplete before any KPI tag |
| **Responsible owner** | Operator; Founder owns Privacy Review posture |
| **Required artefacts** | Ops consent log (EP-008.2B or equivalent — **outside git**); optional pseudonymous Y/N flags in evidence; Privacy Notice version used |
| **Decision point** | May this participant enter KPI numerators? **Only if** C1+C2 recorded |
| **Failure modes** | KPI counting without C2; declining C3 treated as access loss; PII committed to git; unsigned Privacy Review wave |
| **Recovery procedure** | Strip from numerators until C1+C2 present; restore access if C3/C4 declined; purge PII from git; pause invites if OR-01 not held |
| **Escalation path** | Consent mishandling → Founder (P0-class privacy) |

---

### 4.4 Account creation

| Field | Content |
|-------|---------|
| **Expected action** | Create invite-only student account via admin/controlled path; assign pseudonymous ID; map ID↔account in ops store only; generate temp credentials / invite link |
| **Responsible owner** | Operator |
| **Required artefacts** | Provisioning completeness note (no passwords in git); ID mapping in ops store; enrollment register row |
| **Decision point** | Provision only after G-INVITE for the wave (or Founder-approved dry-run non-external account) |
| **Failure modes** | Public registration used; provision failure counted as Accepted; credentials leaked; wrong curriculum subject assigned without screen |
| **Recovery procedure** | Disable bad accounts; re-provision; rotate secrets; do not inflate Accepted |
| **Escalation path** | Systematic provisioning failure → Founder; pause invites |

---

### 4.5 First login

| Field | Content |
|-------|---------|
| **Expected action** | Participant signs in; operator may note “first login observed”; encourage password change if temp credentials; login failure = **P1** |
| **Responsible owner** | Participant acts; Operator supports |
| **Required artefacts** | First-login chase notes (pseudonymous); support ticket if blocked |
| **Decision point** | Is login blocked (P1) vs participant delay (chase)? |
| **Failure modes** | Wrong credentials in invite; product login defect; participant never attempts login |
| **Recovery procedure** | Same-business-day P1 response; re-issue credentials securely; soft check day 1–2 if no login |
| **Escalation path** | P1 open >1 business day → Founder |

---

### 4.6 First mission (productive Session)

| Field | Content |
|-------|---------|
| **Expected action** | Welcome + orientation checklist; participant completes in-product onboarding/calibration; starts Today’s Session; completes ≥1 productive Session → dashboard **Activated** |
| **Responsible owner** | Participant studies; Operator orients and chases |
| **Required artefacts** | Welcome email; orientation checklist; activation note; dashboard Activated |
| **Decision point** | Day-7: Activated vs **Never-activated** (chase Reminder) |
| **Failure modes** | Confused UX (document P2 — no redesign in ops); Session broken (P1); never-activated hollow cohort |
| **Recovery procedure** | Product-as-is guidance; P1 restore study path; day-7 Reminder; log never-activated honestly |
| **Escalation path** | Cohort activation rate collapse → Founder (extend chase / pause new invites — not product redesign under OP) |

**Product constraint:** Use existing Home / Session / Reflection surfaces. No Educational Package, Runtime, Recommendation, or Twin changes.

---

### 4.7 Support request

| Field | Content |
|-------|---------|
| **Expected action** | Intake via support inbox / reply; triage category + severity; respond within SLA; log pseudonymous ticket |
| **Responsible owner** | Operator; Founder for P0 |
| **Required artefacts** | Ticket fields (what/expected/actual/when/device/blocking); evidence under `support/` |
| **Decision point** | Severity P0–P3; can student complete a Session today? |
| **Failure modes** | Missed SLA; social DM as sole record; academic advice beyond product; silent backlog |
| **Recovery procedure** | Re-triage; Founder surge; pause invites if P1 backlog >48h |
| **Escalation path** | Per `OP001_STUDENT_SUPPORT_PROTOCOL.md` §7 |

---

### 4.8 Bug report

| Field | Content |
|-------|---------|
| **Expected action** | Capture bug intake fields; reproduce if possible; severity; respond; fix via normal engineering **or** document; confirm with reporter |
| **Responsible owner** | Operator triage; Engineering for approved defects; Founder if educational-algorithm change requested |
| **Required artefacts** | Bug ticket; incident note if P0/P1; optional pointer in `support/bugs/` |
| **Decision point** | Defect vs design disagreement vs EF change request? |
| **Failure modes** | “Fix” by changing Recommendation/Twin/Runtime/packages under ops authority; promising delivery dates; PII in tickets committed to git |
| **Recovery procedure** | STOP educational/algorithm change → EF-001 operational review → Founder; redact PII |
| **Escalation path** | Suspected educational “bug” that needs engine change → Founder + EF-001 template |

---

### 4.9 Participant withdrawal

| Field | Content |
|-------|---------|
| **Expected action** | Confirm identity + withdrawal type (measurement / full account / interview-only); update register + **Withdrawn**; send acknowledgement; file pseudonymous note |
| **Responsible owner** | Operator; Founder for ops removal (abuse/safety) |
| **Required artefacts** | Withdrawal type; acknowledgement template send; `withdrawals/` note; dashboard update |
| **Decision point** | Measurement-only vs full close vs interview decline (access retained) |
| **Failure modes** | Pressuring to stay for metrics; wrong type applied; deletion request mishandled |
| **Recovery procedure** | Correct classification; follow Privacy Review for delete/export; never invent continued consent |
| **Escalation path** | Contested identity / safety → Founder |

---

### 4.10 Interview scheduling

| Field | Content |
|-------|---------|
| **Expected action** | From ~week 4 of personal start: send Interview invitation to eligible consented participants; book time; dashboard **Interview scheduled** |
| **Responsible owner** | Operator schedules; interviewer per KSI-002 instrument (often Founder) |
| **Required artefacts** | C3 consent; interview invite template; calendar booking; scheduled log |
| **Decision point** | Eligible (active/evaluable posture per study law) and C3 present? Decline allowed without access loss |
| **Failure modes** | Leading questions; interviewing without C3; declining C3 treated as punishment |
| **Recovery procedure** | Reschedule with correct instrument; exclude invalid interview from archive; restore trust |
| **Escalation path** | Instrument deviation → Founder / study authority |

---

### 4.11 Study completion

| Field | Content |
|-------|---------|
| **Expected action** | Mark **Completed** when ≥4-week observation window ends or Founder closes cohort; send Completion thank-you; resolve open P0/P1 |
| **Responsible owner** | Operator; Founder closes cohort |
| **Required artefacts** | Completion email; final status in register; open-incident clearance |
| **Decision point** | Window end vs early Founder close (with rationale) |
| **Failure modes** | Claiming exam pass from completion; marking Completed while P0 open; fabricating Completed counts |
| **Recovery procedure** | Correct claims; hold Completed until P0/P1 clear or explicitly noted; zeros stay zeros |
| **Escalation path** | Premature “GO” language → Founder corrects; no KSI update from ops alone |

---

### 4.12 Evidence collection

| Field | Content |
|-------|---------|
| **Expected action** | File real artefacts under OP001 / OP002 / successor study folders: weekly ops, dashboard snapshots, support, withdrawals, interview pointers — **pseudonymous only** |
| **Responsible owner** | Operator |
| **Required artefacts** | Per `OP001_EVIDENCE_STRUCTURE.md`; honesty rules (no invention) |
| **Decision point** | Is this real evidence or rehearsal/simulation? Label simulations clearly |
| **Failure modes** | Fake N; PII in git; narrating empty tree as study progress; validating KSI from ops docs |
| **Recovery procedure** | Delete fabricated files; redact; relabel; restore zeros |
| **Escalation path** | Honesty breach → Founder; may invalidate study wave |

---

### 4.13 Study closure

| Field | Content |
|-------|---------|
| **Expected action** | Snapshot final dashboard; hand-off note to study authority with honest N flow; archive ops package; confirm non-claims (no GO, no V1 release, no marketing pass rates) |
| **Responsible owner** | Operator prepares; Founder signs hand-off |
| **Required artefacts** | Final snapshot; hand-off note; withdrawal/incident closure check; archived checklist instance |
| **Decision point** | Accepted ≥5 **or** Founder-recorded stop with rationale |
| **Failure modes** | Silent abandonment (KSI-003 pattern); hand-off without N honesty; declaring Version 1 from closure |
| **Recovery procedure** | Formal stop rationale; reopen recruitment only with new G-INVITE; no false GO |
| **Escalation path** | Closure disputes → Founder |

---

## 5. Stage sequence (ops view)

```text
G-OP001 / G-OP002
    → Pre-flight (checklist B)
        → G-INVITE
            → Account creation → Invitation
                → Acceptance → Consent
                    → First login → First mission (Activated)
                        → Support / Bug (as needed)
                            → Weeks 1–4 hold
                                → Interview scheduling → Interview complete
                                    → Study completion → Evidence collection → Study closure
```

Withdrawal and privacy deletion may interrupt any post-acceptance stage.

---

## 6. Cross-references

| Need | Document |
|------|----------|
| Incident simulations | `OP002_INCIDENT_RESPONSE_GUIDE.md` |
| Founder yes/no matrix | `OP002_FOUNDER_DECISION_GUIDE.md` |
| Participant-facing path | `OP002_PARTICIPANT_JOURNEY.md` |
| Calendar / clocks | `OP002_STUDY_TIMELINE.md` |
| Day-to-day checklist | `OP001_EXECUTION_CHECKLIST.md` |

---

## 7. STOP

**No invitations. No external participant accounts. No product changes.**  
Await Founder approval of OP-002 before recruiting the first participant. Invite send still requires separate G-INVITE.

Signed: OP-002 Operational Playbook · 2026-08-04
