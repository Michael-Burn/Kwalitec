# OP-001 — Early Access Plan

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** Educational Content Freeze · EF-001 · PB-017 PASS · PX-007 Premium Conditional PASS · P-002.1 Release Readiness · KSI-003 NO-GO / Pending Evidence · KSI-002 Participant Protocol · `PRIVATE_BETA_PROTOCOL.md`

**This plan is operational only.** It does not improve the product, redesign UX, change educational packages, or modify Recommendation Engine, Student Twin, or Runtime.

---

## 1. Purpose

Build and freeze the **complete operational infrastructure** required before recruiting the first external Stage 1 Early Access participants — so that when Founder authorises invites, enrollment does not fail for lack of process (the failure mode recorded in KSI-003: accepted external N = 0).

Early Access under OP-001 is the **ops shell** that enables a subsequent protocol-compliant Stage 1 educational-effectiveness observation window under KSI-002. OP-001 itself does **not** recalculate KSI, declare Version 1 production-ready, or claim educational effectiveness GO.

---

## 2. Objectives

| ID | Objective | Done when |
|----|-----------|-----------|
| O1 | Define cohort targets and timeline | This plan approved |
| O2 | Freeze recruitment, onboarding, support, and communication procedures | Sibling OP-001 protocols approved |
| O3 | Specify ops dashboard funnel (no analytics engine) | `OP001_OPERATIONS_DASHBOARD.md` approved |
| O4 | Create empty evidence tree for future real artefacts | `knowledge/evidence/releases/OP001/` exists; no fake data |
| O5 | Provide a run checklist so the first cohort is executable | `OP001_EXECUTION_CHECKLIST.md` usable end-to-end |
| O6 | Hard stop before invites | Founder approval recorded **before** any external invitation is sent |

**Non-objectives (explicit):**

- Product / UX / Premium / educational package changes  
- Runtime, Recommendation, Student Twin, curriculum, migrations, feature work  
- Marketing claims, public registration, Version 1 release, KSI recalculation  
- Inventing participants, scorecards, or interview results  

---

## 3. Governing constraints

| Constraint | Binding rule |
|------------|--------------|
| Educational Content Freeze | Package bodies unchanged |
| EF-001 | No new Educational Framework design; ops gap ≠ framework failure |
| Invite-only | No public self-registration |
| Privacy | OR-01 Privacy Review signed; consents captured before KPI inclusion |
| KSI-002 | External N floors and consent layers remain law for study counting |
| KSI-003 | Effectiveness remains **NO-GO / PENDING EVIDENCE** until a real cohort runs |
| P-002.1 | Version 1 **not** production-ready; G1 still FAIL (KSI 64) |
| Claim discipline | No pass-rate, until-exam trust, or commercial launch claims in participant copy |

---

## 4. Participant targets

Aligned with `KSI002_PARTICIPANT_PROTOCOL.md` and EP-007.3 cohort design:

| Parameter | Target |
|-----------|--------|
| **Minimum accepted external (ITT-Accepted)** | **5** |
| **Target accepted external** | **5–10** |
| **Invite send buffer** | Invite **≥8–12** candidates expecting ~40–60% acceptance (adjust from observed rates) |
| **Selected reserve (pre-OP-001)** | 3 invite-pending (`BETA-PIL-001`…`003`) — **not** counted as accepted |
| **Stage 0 internal / staff** | Excluded from external N |
| **Maximum concurrent accepted under KSI-002** | 50 (ops will not approach this in cohort 1) |
| **Activation success (ops)** | ≥1 productive Session within **7 days** of acceptance |
| **Observation window (study, post-ops)** | ≥4 weeks from personal start (KSI-002) — owned by study execution, not OP-001 product work |
| **Interview floor (study GO path)** | Per KSI-002 (≥8 or ≥25% of active) — scheduled by ops; analysed under study protocol |

**Priority demographics / subjects:** IFoA (or designated) students preparing for in-scope loadable curricula; priority subjects historically **CM2** and/or **CS2**. See `OP001_RECRUITMENT_PROTOCOL.md`.

---

## 5. Timeline (ops phases)

Dates are **planning defaults** relative to Founder approval of OP-001. They are not invitations and do not start the study clock.

| Phase | Relative window | Ops outcome |
|-------|-----------------|-------------|
| **P0 — Package freeze** | Day 0 (this programme) | All OP-001 artefacts complete; **STOP** for Founder approval |
| **P1 — Pre-flight** | Approval + 0–3 days | Checklist § Pre-flight complete; accounts provisioned; consent log ready; support channel live |
| **P2 — Recruit & invite** | Approval + 3–14 days | Candidates screened; invitations sent **only after** Founder invite-send authorisation |
| **P3 — Accept & activate** | Invite + 0–14 days | Acceptance, first login, orientation; chase never-activated |
| **P4 — Cohort hold** | Acceptance wave closed when accepted N ≥5 (or Founder stops) | Dashboard funnel current; weekly ops cadence starts |
| **P5 — Hand-off to study ops** | When accepted ≥5 and personal starts defined | Evidence path ready for KSI-002 observation / scorecards / interviews (separate programme authority) |
| **P6 — Cohort close / exit** | Per exit criteria below | Withdrawals closed; thank-yous sent; ops package archived |

**Hard rule:** No Phase P2 invite send until Founder explicitly approves invitations (separate from approving this documentation package).

---

## 6. Recruitment strategy

Summary — detail in `OP001_RECRUITMENT_PROTOCOL.md`:

1. **Warm network first** — Founder / trusted contacts already preparing for in-scope exams.  
2. **Expand selection** beyond the 3 pending pilots until design floor of **5 accepted** is realistically reachable.  
3. **Screen against inclusion/exclusion** before provisioning.  
4. **Invite-only accounts** via controlled admin provisioning.  
5. **No public marketing**, ads, open registration, or pass-rate promises.  
6. **Track channel → invite → accept** in ops stores (pseudonymous IDs in git evidence).

---

## 7. Communication strategy

Summary — templates in `OP001_COMMUNICATION_TEMPLATES.md`:

| Principle | Rule |
|-----------|------|
| Tone | Study companion; educational honesty; bugs expected |
| Claims | **No** exam pass guarantee; **no** Version 1 / marketing launch language |
| Cadence | Invite → reminder (if needed) → acceptance → welcome → week check-ins (light) → interview invite → completion / withdrawal |
| Channel | Email (or Founder-approved equivalent); PII stays out of git |
| Consent | Privacy + measurement required for KPI inclusion; interview/quote optional |

Reuse / align with `knowledge/product/private_beta/STAGE1_INVITE_PACK.md` legal/notice text; OP-001 templates are the **ops mailing set**.

---

## 8. Support model

Summary — detail in `OP001_STUDENT_SUPPORT_PROTOCOL.md`:

| Severity | Response SLA |
|----------|--------------|
| P0 Security / privacy / data | Immediate |
| P1 Cannot study (login, broken session, wrong data) | Same business day |
| P2 Confusing guidance / non-blocking bugs | 1–2 business days |
| P3 Feature ideas / copy nits | Weekly batch |

**Owner:** Founder or designated Early Access operator until a support role exists.  
**Escalation:** P0 → Founder immediately; educational-algorithm requests → document only (no engine changes under OP-001).

---

## 9. Success criteria (ops programme)

OP-001 **succeeds as an operations programme** when **all** hold:

1. All ten mandated OP-001 artefacts exist and are consistent.  
2. Empty evidence structure is in place under `knowledge/evidence/releases/OP001/` with **no fabricated results**.  
3. Pre-flight checklist is executable without inventing product features.  
4. Dashboard specification covers the required funnel states.  
5. Founder approval gate for **invitations** is explicit and not silently skipped.  
6. Alignment with KSI-002 floors (accepted ≥5) and privacy/consent layers is documented.

OP-001 does **not** succeed by claiming educational effectiveness, KSI ≥ 80, or Version 1 release.

---

## 10. Exit criteria

### 10.1 Exit of OP-001 documentation phase (this milestone)

| Criterion | Status target |
|-----------|---------------|
| Operational package complete | Met by programme delivery |
| Founder review of package | **Awaiting** |
| Invites sent | **Forbidden** until separate Founder authorisation |

### 10.2 Exit of first Early Access cohort (ops)

| Criterion | Rule |
|-----------|------|
| Accepted external N | ≥5 **or** Founder-recorded stop with rationale |
| Never-activated chase | Completed for all accepted (7-day rule) |
| Withdrawals / consent changes | Logged; acknowledgements sent |
| Interview scheduling | Offered per KSI-002 timing for evaluable participants |
| Evidence | Real artefacts filed under OP001 / successor study folders — still no invention |
| Hand-off | Explicit hand-off note to study execution authority (e.g. future KSI wave) |

### 10.3 Individual participant exit

Withdrawal of consent, account closure, exam completion end of study window, or ops removal for abuse/safety — per Recruitment and Support protocols; data handling per Privacy Review.

---

## 11. Relationship to other programmes

| Programme | Relationship |
|-----------|--------------|
| KSI-002 | Participant / consent / interview law — OP-001 executes ops readiness under it |
| KSI-003 | Demonstrated enrollment failure; OP-001 addresses the **ops gap** |
| PB-017 / Content Freeze | Product educational inventory held; OP-001 does not reopen packages |
| PX-007 | Premium Conditional PASS unchanged; no Premium feature work |
| P-002.1 | Release readiness context; OP-001 does not declare production-ready |
| Private beta pack | Onboarding, support, invite pack — OP-001 consolidates Early Access ops |

---

## 12. STOP

**Await Founder approval of the OP-001 package.**  
**Do not send participant invitations** until Founder explicitly authorises invite send.

Signed: OP-001 Early Access Plan · 2026-08-04
