# EA-001 — Participant Register

**Programme:** EA-001 — Early Access Cohort 1 Recruitment  
**Wave:** `EA-COHORT-1`  
**As of:** 2026-08-04  
**Authority:** `OP001_RECRUITMENT_PROTOCOL.md` · `KSI002_PARTICIPANT_PROTOCOL.md` · G-INVITE 2026-08-04  
**Privacy:** Pseudonymous IDs only. PII lives in `ops/STAGE1_PILOT_MAP.local.md` (gitignored).

**Note:** Filename prefix `EA001_` here means **Early Access Cohort 1**, not Educational Foundations EA-001.

---

## 1. Funnel definitions (ops)

| State | Definition |
|-------|------------|
| Selected | Screened eligible; may be provisioned; **not** Invited until email sent |
| Invited | Invitation email sent |
| Accepted | Invite accepted + account reachable (ITT-Accepted) |
| Declined | Explicit decline of invite |
| Pending | Invited; no accept/decline yet |
| Activated | Accepted + ≥1 productive Session |
| Never-activated / No-show | Accepted but no productive Session within 7 days (chase) |
| Withdrawn | Measurement / study / account withdrawal logged |
| Excluded | Failed inclusion or hit exclusion — not external N |

---

## 2. External cohort register (live)

| ID | Subject | Channel | Inclusion | Status | Invited | Accepted | Activated | Consent C1+C2 | Notes |
|----|---------|---------|-----------|--------|---------|----------|-----------|---------------|-------|
| BETA-PIL-001 | CM1 | Founder network (prior OR-07) | Pass (Founder-selected; non-CM2/CS2 OK) | **Selected** | — | — | — | Pending | Account provisioned pre-wave; invite **not sent** |
| BETA-PIL-002 | CB2 | Founder network (prior OR-07) | Pass (Founder-selected) | **Selected** | — | — | — | Pending | Account provisioned pre-wave; invite **not sent** |
| BETA-PIL-003 | CS1 | Founder network (prior OR-07) | Pass (Founder-selected) | **Selected** | — | — | — | Pending | Account provisioned pre-wave; invite **not sent** |
| BETA-EA-004 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-005 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-006 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-007 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-008 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-009 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-010 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-011 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |
| BETA-EA-012 | TBD | TBD | Not screened | **Open slot** | — | — | — | — | Buffer expansion |

**Exceptions documented:** Priority subjects in OP-001 are CM2/CS2. `BETA-PIL-001`…`003` use CM1/CB2/CS1 under **prior Founder selection (OR-07)** — retained for Cohort 1 without inventing new eligibility. Further invites should prefer CM2/CS2 when available (D5 expansion).

---

## 3. Stage 0 (excluded from external N)

| ID | Role | Status | Counts toward Accepted? |
|----|------|--------|-------------------------|
| BETA-INT-001…003 | Internal / staff dogfood | Active (pre-existing) | **No** |

---

## 4. Counts (honest)

| Metric | N |
|--------|--:|
| Selected (ready for invite) | **3** |
| Open buffer slots | **9** |
| Invited | **0** |
| Accepted | **0** |
| Declined | **0** |
| Pending (post-invite) | **0** |
| Activated | **0** |
| Never-activated / No-show | **0** |
| Withdrawn | **0** |
| Excluded this wave | **0** |

Selected ≠ Invited ≠ Accepted. Do not narrate Selected as Accepted.

---

## 5. Inclusion / exclusion application

Screening against `OP001_RECRUITMENT_PROTOCOL.md` §§3–4 applies to every new candidate before Select. No exceptions without a dated Founder note in `knowledge/evidence/releases/EA001/registers/exclusions/`.

---

## 6. Update rule

Operator updates this register when:

1. Candidate screened → Selected or Excluded  
2. Invite email sent → Invited  
3. Reply received → Accepted / Declined / Pending chase  
4. Productive Session observed → Activated  
5. Day-7 miss → Never-activated (chase logged)  
6. Withdrawal → Withdrawn  

**Never invent rows or timestamps.**

Signed: EA-001 Participant Register · 2026-08-04
