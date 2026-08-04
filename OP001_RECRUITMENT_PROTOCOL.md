# OP-001 — Recruitment Protocol

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `KSI002_PARTICIPANT_PROTOCOL.md` · EP-007.3 `COHORT_DESIGN.md` · `PRIVATE_BETA_PROTOCOL.md` · Privacy Review (OR-01)

**Defines how to recruit.** Does not send invitations. Does not change the product.

---

## 1. Purpose

Recruit a closed, invite-only Early Access cohort that can become **protocol-eligible Stage 1 external participants** under KSI-002 — without public launch, marketing claims, or inventing enrollment.

---

## 2. Eligibility (summary)

A candidate is **eligible to be invited** only if screening suggests they can meet KSI-002 **inclusion** after acceptance and consent. Invitation ≠ accepted N.

---

## 3. Inclusion criteria

Invite / accept toward **external** N only if **all** are expected to hold (confirm at acceptance):

1. Preparing for an **in-scope** professional exam subject loadable on V1/V2 curricula.  
2. Willing to use an **invite-only** account (no public self-registration).  
3. Able and willing to acknowledge the **privacy notice** and provide **measurement consent** before KPI inclusion.  
4. Not acting solely as staff / Founder dogfood (Stage 0 internal).  
5. Agrees to closed Early Access expectations: bugs possible; **no pass guarantee**; honest feedback preferred.  
6. Privacy Review for the study wave remains **signed** before invite send.  
7. Available for approximately **≥4 weeks** of ordinary study use after personal start (study window — not a product feature).  
8. Communicates in the language used for support (English unless Founder designates otherwise).

---

## 4. Exclusion criteria

Do **not** count toward external Early Access N (may still receive discretionary access only with Founder note):

1. Cannot consent to privacy / measurement terms.  
2. Assigned to recommendation A/B or other interventional ranking trials (out of KSI-002 protocol).  
3. Automated test / persona-only accounts.  
4. Duplicate accounts (same person / normalised email) — retain earliest accepted ID unless Founder directs otherwise.  
5. Failed registrations that never reach invite-accepted state.  
6. Public influencers recruited primarily for marketing content (conflicts with claim discipline).  
7. Participants whose primary goal is product consulting / sales partnership rather than studying for an in-scope exam.  
8. Minors (under 18) — out of scope for this Early Access wave unless a separate privacy package is approved.

---

## 5. Target demographics

| Dimension | Target posture |
|-----------|----------------|
| Audience | Students preparing for designated professional exams (IFoA priority historically) |
| Priority subjects | **CM2** and/or **CS2** (loadable V1/V2); other in-scope subjects only with Founder OK |
| Exam timing | Prefer known exam proximity when available (aids later M8/M9 interpretation under study protocol) — do **not** require a near exam to invite |
| Experience mix | Prefer a mix of first-time and returning exam candidates; avoid all-staff networks |
| Geography | Single-regime Stage 1 privacy package; expanding jurisdictions requires updated Privacy Review |
| Cohort size | Design floor **5 accepted**; target **5–10**; invite buffer **≥8–12** candidates |

**Honesty:** Warm-network bias is expected; record channel and disclose in later study limitations. Do not pretend the sample is population-representative.

---

## 6. Recruitment channels

| Channel | Allowed? | Notes |
|---------|----------|-------|
| Founder personal / professional network | **Yes** | Primary for cohort 1 |
| Trusted tutor / class peer referrals | **Yes** | Screen individually; no blast to unknown lists |
| Prior selected pilots (`BETA-PIL-001`…`003`) | **Yes** | Still invite-pending until Founder authorises send |
| Existing internal alpha students dual-marked external | **Only with Founder** | Disclose prior exposure |
| Public ads / SEO / social campaigns | **No** | Marketing launch out of scope |
| Open registration / waitlist site | **No** | Invite-only |
| Paid lead vendors | **No** | Privacy + claim risk |
| University mass email without opt-in relationship | **No** unless Founder + privacy update |

**Channel log (ops store, not git):** channel ID, date contacted, outcome (declined / interested / screened out / selected), pseudonymous candidate ID.

---

## 7. Screening workflow

1. **Identify** candidate via allowed channel.  
2. **Screen** against inclusion / exclusion (short call or structured email).  
3. **Assign** pseudonymous ID (e.g. `BETA-EA-###` or continue `BETA-PIL-###`).  
4. **Select** into invite queue only if eligible.  
5. **Provision** invite-only account (admin / controlled creation) — **after** Founder invite-send authorisation for the wave.  
6. **Invite** using `OP001_COMMUNICATION_TEMPLATES.md` + Stage 1 notice pack.  
7. **Capture consents** in ops consent log (template: EP-008.2B `CONSENT_CAPTURE_LOG_TEMPLATE.md`) — **never** commit PII to git.  
8. **Update dashboard counts** (Invited → Accepted → …).

**Minimum accepted:** Continue recruiting until **accepted external N ≥ 5**, or Founder records a stop with rationale (stop ≠ inventing N).

---

## 8. Participant expectations

Communicate clearly at invite and welcome:

| Expectation | Detail |
|-------------|--------|
| Purpose | Closed Early Access study companion for exam preparation — **not** a public product launch |
| Use | Log in, complete in-product onboarding/calibration, use Home / Today’s Session, Sessions, Reflections when prompted |
| Duration | Ordinary study over ≥4 weeks preferred for study evaluation |
| Feedback | Bugs and confusion are valuable; feature wish-lists are optional |
| Interviews | Optional structured interview ~week 4; declining does not remove access |
| Claims | No guaranteed pass; product may change later; current educational packages are frozen for this wave |
| Support | Use designated support channel; severity SLAs apply |
| Data | Privacy notice + measurement consent for KPI inclusion; export/delete rights per Privacy Review |

---

## 9. Withdrawal policy

| Type | Effect |
|------|--------|
| **Study / measurement withdrawal** | Exclude from KPI numerators; may keep studying unless they also close the account |
| **Full withdrawal / account close** | Stop access; handle data per Privacy Review deletion workflow |
| **Interview / quote decline or withdrawal** | Does **not** remove study access |
| **Ops removal (abuse / safety)** | Founder decision; log incident; acknowledge |

**Process:**

1. Participant requests withdrawal (email / support).  
2. Operator confirms identity and withdrawal type.  
3. Update enrollment register and dashboard (**Withdrawn**).  
4. Send withdrawal acknowledgement template.  
5. File pseudonymous note under evidence `withdrawals/` (no raw emails in git).  
6. Do **not** pressure participants to stay for metrics.

Inactivity alone is **not** withdrawal — classify never-activated / inactive / dormant per KSI-002.

---

## 10. ID and privacy rules

- Pseudonymous IDs only in repository evidence.  
- PII (names, emails, phones) only in approved ops stores outside git.  
- Do not paste invite lists into OP-001 markdown.  
- Duplicate detection: normalised email / ops-confirmed same person.

---

## 11. STOP

Recruitment **planning** may proceed after Founder approves OP-001.  
**Invitation send** requires separate Founder authorisation.

Signed: OP-001 Recruitment Protocol · 2026-08-04
