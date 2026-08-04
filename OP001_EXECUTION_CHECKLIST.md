# OP-001 — Execution Checklist

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** Full OP-001 package · KSI-002 · Privacy Review (OR-01)

**Step-by-step ops runbook for the first cohort.** Check items in order. Do not skip the Founder gates.

Copy a dated instance into `knowledge/evidence/releases/OP001/checklists/` only when actually executing (not now).

---

## A. Documentation freeze (OP-001 delivery)

- [ ] `OP001_EARLY_ACCESS_PLAN.md` present
- [ ] `OP001_RECRUITMENT_PROTOCOL.md` present
- [ ] `OP001_ONBOARDING_PROTOCOL.md` present
- [ ] `OP001_STUDENT_SUPPORT_PROTOCOL.md` present
- [ ] `OP001_OPERATIONS_DASHBOARD.md` present
- [ ] `OP001_COMMUNICATION_TEMPLATES.md` present
- [ ] `OP001_RISK_REGISTER.md` present
- [ ] `OP001_EVIDENCE_STRUCTURE.md` present
- [ ] `knowledge/evidence/releases/OP001/` empty tree present
- [ ] `OP001_EXECUTION_REPORT.md` present
- [ ] **STOP — Founder reviews OP-001 package**
- [ ] Founder approval of OP-001 documentation recorded (date / note in ops store)

**Do not proceed to invites on documentation approval alone.**

---

## B. Pre-flight (before any invite)

- [ ] Privacy Review (OR-01) still **SIGNED**
- [ ] Enrollment / Stage 1 clearance posture confirmed (do not invite under known HOLD without Founder override note)
- [ ] Support inbox / channel live and monitored
- [ ] Ops consent capture log ready (EP-008.2B template or equivalent) — **outside git**
- [ ] Enrollment register ready (pseudonymous IDs + PII mapping in ops store)
- [ ] Dashboard counting convention frozen (personal-start weeks)
- [ ] Communication templates reviewed against claim discipline
- [ ] Stage 1 Privacy Notice + consent prompts attached to invite workflow
- [ ] Account provisioning path tested on a **non-external** dry account (optional but recommended)
- [ ] Kill / pause rule understood (P0 uncontained → pause invites)
- [ ] **Founder authorises invite send** (dated decision — separate from §A)

---

## C. Recruit

- [ ] Screen candidates against inclusion / exclusion
- [ ] Expand beyond pending pilots until invite buffer supports accepted ≥5
- [ ] Assign pseudonymous IDs
- [ ] Log channels (no emails in git)
- [ ] Select invite queue
- [ ] Founder confirms final invite list (ops store)

---

## D. Provision and invite

- [ ] Provision invite-only accounts
- [ ] Send **Invitation** emails (template §1) with notice + consents
- [ ] Mark dashboard **Invited**
- [ ] Log send (template version + date + pseudonymous ID) in ops / evidence `communications/sent_log/` pointers
- [ ] Schedule reminder cadence for non-responders

---

## E. Accept and consent

- [ ] Record acceptances with timestamps
- [ ] Capture C1 Privacy + C2 Measurement (required for KPI inclusion)
- [ ] Capture C3/C4 if offered (optional)
- [ ] Send **Acceptance** email
- [ ] Send **Welcome** email + orientation checklist
- [ ] Update dashboard **Accepted**
- [ ] Chase incomplete consent before tagging any KPIs

---

## F. Activate

- [ ] Confirm first login / support P1 if blocked
- [ ] Confirm ≥1 productive Session → **Activated**
- [ ] Day-7 never-activated chase (**Reminder** template)
- [ ] Log never-activated / dormant honestly

---

## G. Cohort hold (weeks 1–4)

- [ ] Maintain week bucket counts on dashboard
- [ ] File weekly ops notes under `weekly_ops/week_0N/` when real
- [ ] Triage support per severity SLAs
- [ ] Process withdrawals with acknowledgement template
- [ ] Do **not** change Runtime / Recommendation / Twin / packages / EF
- [ ] Do **not** recalculate validated KSI in this ops programme
- [ ] Optional light check-ins without pressure

---

## H. Interviews

- [ ] From week 4 of personal start, send **Interview invitation** to eligible consented participants
- [ ] Schedule → dashboard **Interview scheduled**
- [ ] Conduct per KSI-002 fixed instrument (no leading)
- [ ] Mark **Interview complete**; archive pseudonymous notes under study/evidence rules
- [ ] Declines logged; access retained

---

## I. Completion / exit

- [ ] Mark **Completed** when observation window ends (or Founder closes cohort)
- [ ] Send **Completion thank-you**
- [ ] Resolve open P0/P1 incidents
- [ ] Snapshot final dashboard (real counts only)
- [ ] Hand-off note to study authority (future KSI wave) with honest N flow
- [ ] Confirm non-claims: no GO, no V1 release, no marketing pass rates from ops alone

---

## J. Forbidden actions (standing)

- [ ] ~~Improve product / redesign UX under OP-001~~ **Forbidden**
- [ ] ~~Change educational packages~~ **Forbidden**
- [ ] ~~Modify Recommendation Engine / Student Twin / Runtime~~ **Forbidden**
- [ ] ~~Migrations / feature work / Premium changes~~ **Forbidden**
- [ ] ~~Send invites before Founder authorisation~~ **Forbidden**
- [ ] ~~Invent participants or metrics~~ **Forbidden**

---

## STOP (current programme state)

As of OP-001 delivery (2026-08-04):

- Section **A** is the deliverable of this programme.  
- Sections **B–I** remain **unchecked** until Founder approval + invite authorisation.  
- **No participant invitations are to be sent.**

Signed: OP-001 Execution Checklist · 2026-08-04
