# EP-001 — Publication Decision Log

**Programme:** EP-001 · HR-001 Human Educational Review Cycle  
**Instrument:** Permanent historical publication register  
**Authority:** EF-001 · EP-001 Governance · CE-001 coverage law · PB-002 · HOLD-001 lifted  
**Opened:** 2026-08-01  
**Last updated:** 2026-08-01 (RO-001 LIVE)  
**Rule:** Append or amend rows only from recorded human decisions under authorised review cycles. Do not forge seals outside HR-001 / named human authority.

---

## Register legend

| Field | Meaning |
|-------|---------|
| **Volume** | Educational Volume ID |
| **Campaign** | Campaign ID + catalogue version |
| **Review status** | Aggregate human-review state |
| **Reviewer decisions** | Tutor · Founder · Auditor · Publication Approver |
| **Approval dates** | Dates of human PASS / APPROVE (or n/a) |
| **Publication decision** | Authorised / Blocked / Rejected |
| **Deployment commit** | Git commit of LIVE `publication_approved` copy (after release) |
| **LIVE verification reference** | Path to LIVE verify evidence |
| **PB verification reference** | Path to Private Beta / adversarial verify when applicable |

---

## 1. Active row — Wave 1 (CS1-004 / Campaign Gamma)

| Field | Record |
|-------|--------|
| **Volume** | `CS1-004` · Univariate completion — From Probability Evaluation to Generation · `1.0.0` |
| **Campaign** | `CS1-EP001-CAMPAIGN-GAMMA` · `cs1004-1.0.0` |
| **Review status** | **Complete (HR-001)** — Tutor PASS · Founder PASS · Auditor PASS · Publication Approver APPROVE |
| **Reviewer decisions** | Tutor: **PASS** · Founder: **PASS** · Auditor: **PASS** · Publication Approver: **APPROVE** |
| **Approval dates** | Tutor: 2026-08-01 · 13:50 · Founder: 2026-08-01 · 14:05 · Auditor: 2026-08-01 · 14:20 · Publication Approver: 2026-08-01 · 14:35 |
| **Publication decision** | **APPROVED** — Volume authorised for joint LIVE activation |
| **Deployment commit** | `f1ff5dc5dd5aca9987c48a6731f3888fdf2295a1` (RO-001 · `dep-d9mtte5aeets73apso4g`) |
| **LIVE verification reference** | `RO001_LIVE_VERIFICATION_REPORT.md` · `knowledge/evidence/releases/RO001/` · **PASS WITH RESIDUAL** (RO1-R1 Finish/Home tomorrow UI) |
| **PB verification reference** | — (not applicable until residual disposition + Private Beta programme) |

**Inventory (joint):** CG-D1…CG-D4 Learning + CG-R1 Revision — five packages; FP-01 forbids Isolated Golden Day activation.

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-gamma-cs1004/`  
**LIVE loader:** Gamma packages **present** as `publication_approved` under `educational_packages/cs1/` (RO-001 joint activate).

**Evidence dossier:** `CS1004_EDUCATIONAL_VOLUME.md` · `CS1004_CERTIFICATION_REPORT.md` · `CS1004_TUTOR_REVIEW.md` · `CS1004_FOUNDER_REVIEW.md` · `CS1004_PUBLICATION_READINESS.md` · `EP001_WAVE1_PUBLICATION_PACK.md` · `EP001_REVIEWER_CHECKLISTS.md` · `EP001_PUBLICATION_DASHBOARD.md` · `EP001_HUMAN_REVIEW_SUMMARY.md` · `RO001_DEPLOYMENT_REPORT.md` · `RO001_LIVE_VERIFICATION_REPORT.md` · `RO001_RELEASE_DECISION.md`

**Activation conditions (binding, not content amendments):**

1. Joint copy of all five packages only. — **Met (RO-001)**  
2. Preserve CB-R1 → CG-D1…CG-R1 continuity chain. — **Met (selection)**  
3. LIVE + CMP + continuity verification before student educational trust / LIVE Verified claim. — **Met for package path; RO1-R1 residual on Finish/Home tomorrow chrome**  
4. Wave 0 Alpha/Beta Approver honesty gap **not waived** by this APPROVE.  
5. Wave 2 (CS1-003) **not started** until LIVE verification of Wave 1 completes. — Wave 1 package-path LIVE Verified with residual; Wave 2 still not started pending Founder residual acknowledge  
6. No until-exam educational trust claim from this Volume alone.

---

## 2. Context rows — Wave 0 honesty (unchanged by HR-001 Gamma APPROVE)

| Volume | Campaign | Review status | Reviewer decisions (summary) | Approval dates | Publication decision | Deployment commit | LIVE verification | PB verification |
|--------|----------|---------------|------------------------------|----------------|----------------------|-------------------|-------------------|-----------------|
| CS1-001 | `CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0` | Approver honesty gap | Tutor / Founder / Auditor historical desk packs exist; **Publication Approver UNSIGNED** for CE-001 credit | Approver: — | **BLOCKED** for Approver-credit Published claim | Live loader has 4 packages (pre-Approver honesty gap) | See `EP001_WAVE1_HONESTY_RECONCILIATION.md` | PB-001 / PB-001A evidence separate; does not waive Approver |
| CS1-002 | Campaign Beta · CS1-002 | Approver honesty gap | **Publication Approver UNSIGNED** | Approver: — | **BLOCKED** for Approver-credit Published claim | Live loader has 4 packages (honesty gap) | Same honesty record | Same |
| EA-006 4.2 orphan | No Gate CG Volume | Not coverage | n/a | — | **Not catalogue credit** | 1 package live | n/a for CE-001 Published | Must not absorb as Wave 1 credit |

These rows remain until human Approver seals close the honesty gap. HR-001 Gamma APPROVE does **not** waive or forge them.

---

## 3. Decision chronology (CS1-004)

| Timestamp | Event | Actor | Outcome |
|-----------|-------|-------|---------|
| 2026-08-01 | Wave 1 catalogue authored + desk certification assembled | Editorial / Author desk | Approver-ready dossier |
| 2026-08-01 | Wave 1A publication pack + reviewer checklists + dashboard | Publication readiness | Ready for human review |
| 2026-08-01 | Wave 1B human review integration | Wave 1B register | Decisions recorded as **UNSIGNED**; publication **BLOCKED** |
| 2026-08-01 · 13:50 | HR-001 Tutor Review (independent) | HR-001 · Tutor seat | **PASS** — no amendments |
| 2026-08-01 · 14:05 | HR-001 Founder Review (independent) | HR-001 · Founder seat | **PASS** — Stage 0 commission YES |
| 2026-08-01 · 14:20 | HR-001 Auditor Review (independent) | HR-001 · Auditor seat | **PASS** — Gate CG PASS; EJ accept; FP denied |
| 2026-08-01 · 14:35 | HR-001 Publication Approver | HR-001 · Publication Approver seat | **APPROVE** — joint LIVE activation authorised |
| 2026-08-01 · 14:35 | Publication decision recorded | Publication Decision Log | **APPROVED** — stop; LIVE deploy/verify next ops step; Wave 2 gated |
| 2026-08-01 · RO-001 | Joint LIVE activate + deploy + verify | Release Ops | Tip `f1ff5dc5…` live; package-path **LIVE Verified** with residual RO1-R1; Wave 2 still not started |

---

## 4. Deployment readiness (CS1-004)

| Gate | Status |
|------|--------|
| Tutor PASS | **Recorded** (2026-08-01 · 13:50) |
| Founder PASS | **Recorded** (2026-08-01 · 14:05) |
| Auditor Gate CG PASS | **Recorded** (2026-08-01 · 14:20) |
| Publication Approver APPROVE | **Recorded** (2026-08-01 · 14:35) |
| Joint LIVE deploy authorised | **Yes** |
| Deployment package prepared for release | **Executed (RO-001)** |
| LIVE Verified | **Yes — package path** (`RO001_LIVE_VERIFICATION_REPORT.md`); residual RO1-R1 Finish/Home tomorrow UI |
| CE-001 Approver credit for 2.1.3–2.1.6 | **Recordable** — Volume APPROVED + LIVE package path verified |
| Student educational trust claim | **Package-path authorised** — do not claim Finish/Home tomorrow chrome honesty until RO1-R1 closed |

**Deployment readiness verdict:** **LIVE (joint inventory)** — publication **APPROVED**; deploy commit recorded; LIVE verification **PASS WITH RESIDUAL**.

### 4.1 LIVE deployment checklist (RO-001)

| # | Action | Status |
|---|--------|--------|
| 1 | Copy all five Gamma packages to `educational_packages/cs1/` with `publication_approved` | **Done** |
| 2 | Advance campaign/Volume status → `released` on activation | **Done** |
| 3 | Preserve tomorrow_preview / campaign_day chain from Beta Revision | **Done (selection)** — Finish/Home chrome residual RO1-R1 |
| 4 | LIVE delivery + CMP partnership + continuity verification | **Done (package path)** |
| 5 | Record LIVE verification path on this log | **Done** |
| 6 | Update `EP001_COVERAGE_MAP.md` + publication dashboard | **Done** |
| 7 | Begin Wave 2 | **Forbidden until residual disposition / Founder acknowledge** |

---

## 5. Amendment rule

When a human reviewer returns Approve / Reject / Pass with conditions:

1. Update the CS1-004 active row and chronology.  
2. Mirror decisions in `EP001_HUMAN_REVIEW_SUMMARY.md`.  
3. Enter requested changes in `EP001_REVIEW_FEEDBACK_REGISTER.md` with EF-001 classification.  
4. Do **not** modify educational packages or deploy until remediation is approved and Approver re-seals as required.  
5. After lawful release, record **Deployment commit**, **LIVE verification reference**, and **PB verification reference** here.

**HR-001 application:** Zero human-requested amendments. Remediation list empty. Educational packages not modified. Publication **APPROVED**.

---

## 6. Publication decision (binding)

```text
Volume: CS1-004 · 1.0.0 · CS1-EP001-CAMPAIGN-GAMMA · cs1004-1.0.0
Cycle: HR-001 — Human Educational Review Cycle
Publication decision: APPROVED
Date: 2026-08-01 · 14:35
Approver seat: HR-001 · Publication Approver
Amendments required before deploy: NONE
LIVE deploy executed: YES (RO-001) · commit f1ff5dc5dd5aca9987c48a6731f3888fdf2295a1
LIVE verification: PASS WITH RESIDUAL (RO1-R1)
Wave 2: NOT STARTED
```

---

Signed: Publication Decision Log · EP-001 · HR-001 · RO-001 · 2026-08-01  
**Publication decision (CS1-004):** **APPROVED**  
**LIVE:** Verified (package path) · residual RO1-R1  
**Wave 2:** Not started
