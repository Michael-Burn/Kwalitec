# OP-002 — Incident Response Guide

**Programme:** OP-002 — Early Access Pilot Operations  
**Version:** 1.0  
**Status:** TABLETOP REHEARSAL COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_STUDENT_SUPPORT_PROTOCOL.md` · `OP001_RISK_REGISTER.md` · `OP001_RECRUITMENT_PROTOCOL.md` · Privacy Review (OR-01) · EF-001 · `OP002_OPERATIONAL_PLAYBOOK.md`

**Tabletop simulations only.** No live incidents. No invitations. No product changes authorised by this guide.

---

## 1. Purpose

Rehearse failure and stress cases so the operator and Founder already know severity, first moves, recovery, and escalation **before** external participants exist.

---

## 2. Standing severity (recap)

| Sev | Meaning | First response |
|-----|---------|----------------|
| **P0** | Security / privacy / data loss / unlawful disclosure | Immediate → Founder |
| **P1** | Cannot study (login, Session hard-broken, wrong data) | Same business day |
| **P2** | Confusing / degraded with workaround | 1–2 business days |
| **P3** | Ideas / polish | Weekly batch |

---

## 3. Universal response skeleton

1. **Detect** — channel, timestamp, pseudonymous ID.  
2. **Classify** — category + severity (+ EF-001 class if product change urged).  
3. **Contain** — especially P0 (access, disclosure, invite pause).  
4. **Communicate** — honest student reply within SLA; no pass-rate / V1 claims.  
5. **Act** — restore study path **or** document; educational/algorithm change = STOP → EF-001 review.  
6. **Log** — ops store + pseudonymous evidence under `incidents/` / `support/`.  
7. **Close / hand-off** — confirm with participant; Founder sign-off on P0.

---

## 4. Simulated incidents

Each simulation: scenario · classification · expected action · owner · artefacts · decision · failure modes · recovery · escalation.

### S1 — Participant never responds

| Field | Content |
|-------|---------|
| **Scenario** | Invite sent; no accept, no login, no reply after reminder window |
| **Classification** | Ops funnel — **not** Withdrawn; not Accepted |
| **Expected action** | Reminder template at planned cadence; after Founder-defined chase limit (e.g. 2 reminders / 14 days), mark interest closed; keep Invited history honest; do not invent Accepted |
| **Owner** | Operator |
| **Artefacts** | Send log; Reminder send; enrollment note “no response” |
| **Decision** | Continue chase vs release invite slot for next candidate |
| **Failure modes** | Counting as Accepted; endless chase burning Founder time; second invite without closing first |
| **Recovery** | Correct dashboard; recruit buffer candidates |
| **Escalation** | If Invited≫0 and Accepted=0 past wave window → Founder (R-01 / R-02) |

---

### S2 — Participant accepts then disappears

| Field | Content |
|-------|---------|
| **Scenario** | Accepted (+ maybe C1/C2); no productive Session by day 7; silent |
| **Classification** | **Never-activated** (KSI-002); support outreach — not automatic withdrawal |
| **Expected action** | Day-7 Reminder; offer P1 help if login suspected; log chase; keep ITT-Accepted honest; optional T14 light check-in if briefly activated then dormant |
| **Owner** | Operator |
| **Artefacts** | Chase log; Reminder; never-activated flag |
| **Decision** | Continue soft support vs participant-initiated withdrawal later |
| **Failure modes** | Silent drop from ITT; shaming messages; fake Session events |
| **Recovery** | Restore honest counts; re-open support without pressure |
| **Escalation** | Cohort-wide never-activated spike → Founder (pause new invites; not redesign under ops) |

---

### S3 — Participant reports a bug

| Field | Content |
|-------|---------|
| **Scenario** | Student reports broken or incorrect behaviour during study |
| **Classification** | Bug; severity by blocking study (P1 vs P2); P0 if security/data |
| **Expected action** | Full intake fields; reproduce; SLA response; engineering defect path **or** document workaround; confirm with reporter |
| **Owner** | Operator triage; Engineering for approved fix; Founder if P0 or algorithm change requested |
| **Artefacts** | Bug ticket; incident note if P0/P1 |
| **Decision** | Defect vs design disagreement vs EF change? |
| **Failure modes** | Shipping Recommendation/Twin/Runtime/package changes under OP authority; delivery promises; PII in git |
| **Recovery** | Revert unauthorised educational changes; EF-001 review if still needed; redact |
| **Escalation** | P0 → Founder immediate; algorithm change urge → EF-001 + Founder |

---

### S4 — Participant asks for academic advice

| Field | Content |
|-------|---------|
| **Scenario** | “What should I study tonight?” / “Will this topic come up?” / “Am I ready to pass?” |
| **Classification** | Student question (usually P2); **not** a defect |
| **Expected action** | Guide to **product-as-is** (Home, Today’s Session, existing surfaces); **no** invented curriculum outside product; **no** exam outcome guarantee; log question |
| **Owner** | Operator |
| **Artefacts** | Questions log |
| **Decision** | Answer within product bounds vs escalate policy edge cases to Founder |
| **Failure modes** | Becoming a private tutor that contradicts frozen packages; pass promises; changing Recommendation mid-wave to “help” |
| **Recovery** | Correct prior over-claim in writing; restate companion purpose |
| **Escalation** | Repeated pressure for guarantees → Founder; any urge to change engines → EF-001 |

---

### S5 — Participant misunderstands the study

| Field | Content |
|-------|---------|
| **Scenario** | Believes Early Access is public launch, paid product, guaranteed pass, or mandatory research with no exit |
| **Classification** | Expectation mismatch (R-08); P2 communication |
| **Expected action** | Correct with claim-discipline language; restate closed pilot, voluntary, no pass guarantee, withdrawal rights; resend Privacy Notice summary if needed |
| **Owner** | Operator; Founder if trust severely damaged |
| **Artefacts** | Clarification email; optional incident note if distress |
| **Decision** | Continue with corrected understanding vs invite withdrawal |
| **Failure modes** | Leaving misunderstanding uncorrected; over-correcting into marketing |
| **Recovery** | Written clarification; offer withdrawal without blame |
| **Escalation** | Public posting of false claims → Founder (comms + pause if needed) |

---

### S6 — Participant wants their data deleted

| Field | Content |
|-------|---------|
| **Scenario** | Export and/or deletion request |
| **Classification** | Privacy / data — treat as **P0-adjacent urgency** for intake; execute per Privacy Review SLAs (export **14 days**; analytics delete **30 days** after verified request per Stage 1 pack) |
| **Expected action** | Verify identity carefully; confirm scope (export / analytics delete / full account); update consent/withdrawal; execute Privacy Review workflow; acknowledge; log pseudonymous completion |
| **Owner** | Founder (Privacy Owner capacity) with Operator assist |
| **Artefacts** | Verified request record (ops store); withdrawal/privacy note; no raw dumps in git |
| **Decision** | Scope of deletion vs measurement withdrawal only |
| **Failure modes** | Deleting without verification; ignoring SLA; refusing lawful request; committing export files with PII to git |
| **Recovery** | Halt bad deletion; secure exports; Privacy Review update if process failed |
| **Escalation** | Any disclosure during process → P0 Founder incident |

---

### S7 — Participant misses multiple study days

| Field | Content |
|-------|---------|
| **Scenario** | Activated earlier; then several days/weeks silent; still has access |
| **Classification** | Inactive / dormant (KSI-002) — **not** automatic withdrawal |
| **Expected action** | Optional light check-in (no pressure); keep funnel honest; do not fabricate activity; offer support if blocked |
| **Owner** | Operator |
| **Artefacts** | Optional check-in send log; dormancy note |
| **Decision** | Leave alone vs soft outreach vs later interview eligibility judgment under study law |
| **Failure modes** | Guilt messaging; inventing Sessions; removing from ITT quietly |
| **Recovery** | Restore honest status; apologise if outreach felt coercive |
| **Escalation** | Mass dormancy → Founder (recruitment quality / timing — not EF redesign) |

---

### S8 — Render outage during a study session

| Field | Content |
|-------|---------|
| **Scenario** | Participant mid-Session; app/hosting unavailable or Session hard-broken |
| **Classification** | **P1** (cannot study); **P0** if data loss/corruption suspected |
| **Expected action** | Acknowledge same business day; status honesty; restore path as soon as practical; daily updates if open; do **not** tell them to “just use a different product feature we invent”; log incident |
| **Owner** | Operator comms; Engineering restore; Founder if prolonged or data loss |
| **Artefacts** | Incident note; student updates log |
| **Decision** | Workaround exists? Pause new invites if widespread? |
| **Failure modes** | Silence; blaming student; shipping educational redesign as “fix” |
| **Recovery** | Restore hosting/session path; confirm with reporters; post-mortem pseudonymous |
| **Escalation** | >1 business day unrestored or data loss → Founder; consider invite pause |

---

### S9 — Founder unavailable for 48 hours

| Field | Content |
|-------|---------|
| **Scenario** | Founder offline; cohort live or invites pending |
| **Classification** | Ops continuity risk (R-05 related) |
| **Expected action** | **Pre-agreed cover rules (rehearsal default):** Operator may continue P1/P2 responses within protocol; **must not** send new invites, approve educational/algorithm changes, close cohort, or execute irreversible deletion without Founder — except pre-written Privacy Review emergency steps if already delegated in writing. P0: contain (revoke sessions, pause public exposure) and queue Founder; do not invent legal positions |
| **Owner** | Designated Operator (or pause ops if none) |
| **Artefacts** | Cover note in ops store; queued decisions list |
| **Decision** | Continue hold vs **freeze invites and non-urgent P3** until Founder returns |
| **Failure modes** | Operator exceeds authority; P0 ignored; invite send without G-INVITE |
| **Recovery** | Founder reviews queue within 24h of return; ratify or reverse |
| **Escalation** | If no Operator designated: **auto-pause** new invites and non-critical changes until Founder available |

---

## 5. Combined drill checklist (tabletop)

Before first invite, Founder + Operator verbally walk:

- [ ] S1 never responds  
- [ ] S2 accepts then disappears  
- [ ] S3 bug  
- [ ] S4 academic advice  
- [ ] S5 study misunderstanding  
- [ ] S6 data deletion  
- [ ] S7 missed days  
- [ ] S8 render outage  
- [ ] S9 Founder 48h unavailable  

Record drill completion under `knowledge/evidence/releases/OP002/rehearsal/` (this programme).

---

## 6. Kill / pause criteria (recap)

Founder **pauses invites** or freezes access when:

- P0 uncontained  
- Privacy Review not held  
- P1 backlog >48h with no surge plan  
- Trust irreparably broken for the wave  

---

## 7. STOP

Simulations are not live incidents. **No invitations** until Founder approval of OP-002 and separate G-INVITE.

Signed: OP-002 Incident Response Guide · 2026-08-04
