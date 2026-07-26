# Beta Cohort Registry

**Programme:** EP-004 — Workstream 1  
**Version:** 1.0  
**Status:** Active — Stage 0 populated; Stage 1 early-access wave **selected** (N=3 external + founder Stage 0)  
**Updated:** 2026-07-26 (OR-07 early-access selection)  
**Authority:** Product / Beta ops  
**Privacy:** Pseudonymous IDs only in this artefact — no emails, names, or raw PII  
**Governing protocol:** [`../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md`](../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md)  
**Private ops map:** emails ↔ Pilot IDs live **outside git** only

---

## 1. Eligibility

| Rule | Spec | EP-004 application |
|---|---|---|
| Audience | IFoA (or designated professional exam) students preparing for an in-scope subject | Stage 1–2 invitees only |
| Cohort size | Target **20–50** external invite-only students (EP-001 / EP-003) | Stage 2 target; Stage 1 = small pilot (5–10) |
| Account model | Invite-only; **no** public self-service registration | Enforced |
| Platform | Version 1 Platform Baseline | Required |
| Staff / dogfood | Count toward N only if marked **participant** | Stage 0 = internal; labelled separately |
| Consent | Cannot consent → ineligible | Hard gate before productive measurement |
| Conflict | Anyone unable to accept measurement / privacy notice | Excluded |

**Provisioning:** admin / controlled account creation only. Align with Vision Data Principles.

---

## 2. Recruitment

| Stage | Method | Owner | Status |
|---|---|---|---|
| Stage 0 — Internal | Founder / eng dogfood accounts marked participant | Product | **COMPLETE** |
| Stage 1 — Small pilot | Personal invite from founder network; IFoA CM2 / CS2 priority | Product | **OR-07 early access** — 3 external selected; invites pending |
| Stage 2 — Expanded private beta | Controlled expansion to 20–50; no marketing site | Product | **HOLD** — Stage 1 exit GO required |

### Recruitment checklist (Stage 1+)

- [x] Privacy Review checklist signed (`../private_beta/PRIVACY_REVIEW.md`) — 2026-07-26
- [x] Privacy notice text finalized and attached to invite (`../private_beta/STAGE1_INVITE_PACK.md`)
- [x] Measurement consent + optional interview / quote consent **process** ready (`../ep008_2b_stage1_pilot_readiness_closure/CONSENT_CAPTURE_LOG_TEMPLATE.md`) — live capture at invite
- [x] Subject / exam date recorded — per invitee (ops store) — **start at provision**; TBD until ops map filled
- [x] Onboarding pack prepared (`../private_beta/BETA_ONBOARDING.md` + `STAGE1_INVITE_PACK.md`)
- [x] Support channel linked (`../private_beta/SUPPORT_WORKFLOW.md` — fill live address in invite §3)

### OR-07 early-access selection (2026-07-26)

| Decision | Value |
|---|---|
| Founder / operator | Remains **Stage 0** (`BETA-INT-001`) — early access yes; **does not** count toward external Stage 1 N |
| External early-access students | **3** → `BETA-PIL-001` … `003` |
| Design target | Stage 1 design prefers **5–10**; this wave is **N=3** labelled **exploratory / early access** (honest under-size) |
| Measurement | **C2** — `manual` / `exploratory`; analytics OFF |
| Privacy regime | Prefer single regime for all three (confirm in ops map) |

---

## 3. Consent model

| Consent type | Required for measurement reporting? | Notes |
|---|---|---|
| Privacy notice acknowledged | Yes (external) | Stage 0 uses internal alpha rules |
| Measurement consent (M1–M9 aggregates) | Yes | Withdrawal → stop including in KPI numerators |
| Interview consent | Optional | Decline does not remove study access |
| Quote consent | Optional | Anonymous quotes in internal reports only |

Analytics flag activation for external invitees follows [`ANALYTICS_ACTIVATION.md`](ANALYTICS_ACTIVATION.md) and EP-002 go-live checklist.

---

## 4. Participant register

**ID scheme:** `BETA-{STAGE}-{NNN}` where STAGE ∈ `INT` | `PIL` | `EXT`.

| Participant ID | Stage | Role | IFoA subject (or scope) | Region | Consent | Onboarding | Exit | Notes |
|---|---|---|---|---|---|---|---|---|
| BETA-INT-001 | 0 | Founder / Product participant | CM2 (dogfood) | EU | Internal alpha | Complete (≥1 Session) | Active | Early access operator; **not** toward external N |
| BETA-INT-002 | 0 | Engineering participant | CS2 (dogfood) | EU | Internal alpha | Complete (≥1 Session) | Active | Same as above |
| BETA-INT-003 | 0 | Educational governance dogfood | CM2 (dogfood) | EU | Internal alpha | In progress | Active | Orientation week |
| BETA-PIL-001 | 1 | External early-access student | CM1 | TBD (ops) | Pending | Not started | Reserved | Selected + account provisioned 2026-07-26; invite pending |
| BETA-PIL-002 | 1 | External early-access student | CB2 | TBD (ops) | Pending | Not started | Reserved | Selected + account provisioned 2026-07-26; invite pending |
| BETA-PIL-003 | 1 | External early-access student | CS1 | TBD (ops) | Pending | Not started | Reserved | Selected + account provisioned 2026-07-26; invite pending |
| BETA-PIL-004 … 010 | 1 | Reserved | TBD at invite | TBD | Pending | Not started | Reserved | Optional expansion toward design N=5–10 |
| BETA-EXT-001 … 050 | 2 | Reserved | TBD at invite | TBD | Pending | Not started | Reserved | Expand only after Stage 1 ops exit |

### Cohort counts (2026-07-26)

| Population | N | Counts toward EP-003 exit N (20–50)? |
|---|---|---|
| Stage 0 active participants | 3 | **No** (staff / dogfood) |
| Stage 1 selected (accounts provisioned; invites pending) | **3** | — |
| Stage 1 invited | 0 | — |
| Stage 2 invited | 0 | — |
| External active (measurement) | **0** | Exit criterion #1 **OPEN**; Stage 1 early wave under-size vs 5–10 design |

---

## 5. Onboarding status definitions

| Status | Meaning |
|---|---|
| Not started | Invite not sent or not accepted |
| Invited | Account provisioned; welcome sent |
| Accepted | Login confirmed |
| Onboarding | Calibration / first Session in progress |
| Complete | ≥1 productive Session completion within 7 days of acceptance (protocol success) |
| Stalled | No productive Session within 7 days — ops follow-up |

---

## 6. Exit status definitions

| Status | Meaning | Data handling |
|---|---|---|
| Active | Participating | Retain per Privacy Review |
| Withdrawn (measurement) | Measurement consent withdrawn; may still study | Exclude from KPI; honour export/delete |
| Withdrawn (full) | Left product | Export/delete path |
| Exam complete | Natural end of study window | Retain aggregates if consented |
| Removed (ops) | Abuse / safety | Per support + privacy |

---

## 7. Subject & region mix (targets)

| Dimension | Stage 1 target | Stage 2 target |
|---|---|---|
| Subjects | Prefer CM2 and/or CS2 (in-scope curricula loadable) | Mix reflecting Vision IFoA focus; document any waiver |
| Region | Prefer single primary privacy regime for first pilot | Expand only with Privacy Review update |
| Exam proximity | Prefer students with a dated exam window when possible | Same — supports M8/M9 interpretation |

---

## 8. Exit criteria (WS1)

| Criterion | Status |
|---|---|
| Eligibility documented | COMPLETE |
| Recruitment plan staged | COMPLETE |
| Participant ID scheme + Stage 0 rows | COMPLETE |
| Consent / subject / region / onboarding / exit fields | COMPLETE |
| External cohort 20–50 | **OPEN** — gated on privacy + Stage 1 |

---

## References

- [`../private_beta/BETA_ONBOARDING.md`](../private_beta/BETA_ONBOARDING.md)
- [`../private_beta/PRIVACY_REVIEW.md`](../private_beta/PRIVACY_REVIEW.md)
- [`ROLLOUT.md`](ROLLOUT.md)
