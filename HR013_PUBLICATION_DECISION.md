# HR-013 — Publication Decision (Campaign Omicron / CS1-015)

**Programme:** HR-013 — Wave 13 Human Educational Review Cycle  
**Volume:** `CS1-015` · `1.0.0`  
**Campaign:** `CS1-EP001-CAMPAIGN-OMICRON` · `cs1015-1.0.0`  
**Scope class:** Pilot Arc (Continuity Front join into 5.1)  
**Publication pattern:** AP-01 Certified Pilot Arc  
**Approver role:** Human Publication Approver  
**Decision recorded:** 2026-08-03 · 15:45  
**Decision:** **APPROVE**  
**Authority:** EO-001 · EA-008 AP-01 · EF-001 · EP-001 Governance · Continuity Front Law · RO-012 PASS · PB-014 PASS · HR-012 APPROVED  
**Desk companion:** `CS1015_PUBLICATION_READINESS.md` (UNSIGNED desk — this human APPROVE is authoritative) · `EP013_WAVE13_PLAN.md` · `EP013_COVERAGE_UPDATE.md`  
**Constraint:** Educational packages unmodified during review · no LIVE deployment in this programme · no Wave 14 work · RO-013 not executed · PB-015 not started  

---

## 1. Prerequisites

| Prerequisite | Status |
|--------------|--------|
| Tutor PASS | **PASS** — `HR013_TUTOR_REVIEW.md` · 2026-08-03 · 15:00 |
| Founder PASS | **PASS** — `HR013_FOUNDER_REVIEW.md` · 2026-08-03 · 15:15 |
| Auditor Gate CG PASS | **PASS** — `HR013_AUDITOR_REPORT.md` · 2026-08-03 · 15:30 |
| Per-package certification reviewed | **Met** (10/10 independent human inspection) |
| EJ acceptance | **Met** |
| FP-01…FP-06 denied | **Met** |
| Publication dossier complete | **Met** (HR-013 artefacts + Wave 13 plan/coverage + CS1015_* packs) |
| Dashboard distinguishes catalogue vs LIVE | **Met** |
| Wave 12 LIVE-complete (RO-012 / PB-014) | **Met** |

---

## 2. Publication unit

Joint inventory of **10** days (9 Learning + 1 Revision). **Do not** activate a single Omicron day alone (FP-01).

| Block | Days | Mode | LIVE today? |
|-------|------|------|-------------|
| 5.1 Learning | CO-D1…CO-D9 | Learning | **No** |
| CO-R1 | Revision | Revision | **No** |

Catalogue: `app/curriculum/data/educational_campaigns/cs1/campaign-omicron-cs1015/`  
Live loader: Omicron packages **absent** at Approver seal (correct).  
Trust Front note: CS1-003 Delta 5.1 packages remain LIVE independently.

---

## 3. Approver worksheet

| Check | Initials / date |
|-------|-----------------|
| Gate CG evidence pack reviewed | HR-013 PA · 2026-08-03 · 15:45 |
| Tutor / Founder / Auditor PASS reviewed | HR-013 PA · 2026-08-03 · 15:45 |
| FP-01…FP-06 denied | HR-013 PA · 2026-08-03 · 15:45 |
| Continuity with CS1-014 acknowledged | HR-013 PA · 2026-08-03 · 15:45 |
| Trust Front (CS1-003) not wholly absorbed | HR-013 PA · 2026-08-03 · 15:45 |
| Continuity Front law (5.1 join, not whole-Delta swallow) held | HR-013 PA · 2026-08-03 · 15:45 |
| Certified Coverage honesty (63/72 held; no +Δ / no double-count) acknowledged | HR-013 PA · 2026-08-03 · 15:45 |
| Student Reliance honesty (through Topic 4.2 held until LIVE) acknowledged | HR-013 PA · 2026-08-03 · 15:45 |
| Claims allowed/forbidden accepted | HR-013 PA · 2026-08-03 · 15:45 |
| Joint 10-day activation only | HR-013 PA · 2026-08-03 · 15:45 |
| Activation engineering dependencies acknowledged (incl. Omicron+Delta coordination) | HR-013 PA · 2026-08-03 · 15:45 |
| Wave 0 Alpha/Beta Approver honesty gap acknowledged (not waived) | HR-013 PA · 2026-08-03 · 15:45 |
| No until-exam trust claim | HR-013 PA · 2026-08-03 · 15:45 |
| Wave 14 gated on Wave 13 LIVE exit + approval | HR-013 PA · 2026-08-03 · 15:45 |
| LIVE not claimed before seal | HR-013 PA · 2026-08-03 · 15:45 |
| RO-013 not executed in this cycle | HR-013 PA · 2026-08-03 · 15:45 |
| PB-015 not started | HR-013 PA · 2026-08-03 · 15:45 |

---

## 4. Claims after Approval

| Allowed | Forbidden |
|---------|-----------|
| Certified Pilot Arc for 5.1.1–5.1.9 + revision (CF-join) | First-pass spine PASS |
| Continuity Front join advanced through Bayesian (progressive, after LIVE Verified) | Until-exam educational trust |
| Honest deferral of Wave 0 / spine re-audit | Coverage mirage from catalogue alone |
| Honest stop after CO-R1 | Wave 14 started from Approver alone |
| | Trust Front whole-Delta absorb |
| | Published Coverage increase (5.1 already counted) |
| | Student Reliance past 4.2 from Approver alone |

---

## 5. Binding publication decision

```text
Volume: CS1-015 · 1.0.0 · CS1-EP001-CAMPAIGN-OMICRON · cs1015-1.0.0
Cycle: HR-013 — Wave 13 Human Educational Review Cycle
Publication decision: APPROVED
Date: 2026-08-03 · 15:45
Approver seat: HR-013 · Publication Approver
Amendments required before deploy: NONE
LIVE deploy executed in this programme: NO
Wave 14: NOT STARTED
RO-013: NOT EXECUTED
PB-015: NOT STARTED
```

**Volume status after decision:** `approved` (human) — catalogue remains non-LIVE until successor ops copies joint inventory.

---

## 6. Activation conditions (binding — not content amendments)

Authorised for successor LIVE ops programme (**RO-013**) only:

1. Copy **all 10** Omicron packages jointly to `educational_packages/cs1/` with `status: publication_approved`.  
2. Preserve `campaign_day` / `tomorrow_preview` chain CO-D1…CO-R1 (selection continuity from CX-R1 → CO-D1).  
3. Never activate a single Omicron day alone (FP-01).  
4. Coordinate CF-join path with existing CS1-003 Delta 5.1 LIVE inventory (no Isolated Golden Day; no double-serve theatre).  
5. Advance campaign/Volume status records to `approved` (then `released` on activation).  
6. Run LIVE + CMP + continuity verification; record evidence on the Publication Decision Log.  
7. Update `EP001_COVERAGE_MAP.md` / `EP013_COVERAGE_UPDATE.md` — Approver numerator remains **63 / 72** (no double-count of 5.1); LIVE Verified columns only with evidence.  
8. Student Reliance may advance through Topic 5.1 only after LIVE Verified + separate reliance register update.  
9. Wave 0 Alpha/Beta Approver honesty gap **not waived**.  
10. **Do not begin Wave 14** until LIVE verification of Wave 13 completes + approval (RO-013 / successor PB).  
11. No until-exam educational trust claim from this Volume alone.  
12. Trust Front (CS1-003) credit not conflated with Continuity Front join credit.  
13. Certified Educational Coverage remains **63 / 72** and Student Reliance through Topic **4.2** until LIVE Verified evidence advances Reliance (Coverage stays held — 5.1 already counted).  
14. **Do not execute RO-013 in this HR-013 cycle** — stop after publication decision.  
15. **Do not begin PB-015** from this cycle.

---

## 7. Decision block

```text
Publication Approver name: HR-013 · Publication Approver seat
Date: 2026-08-03 · 15:45
Volume: CS1-015 · 1.0.0 · CS1-EP001-CAMPAIGN-OMICRON
Decision: APPROVE
Conditions: Joint 10-day LIVE only; LIVE verify before student trust; Wave 0 honesty gap not waived; Wave 14 gated on Wave 13 LIVE exit; Coverage/Reliance honesty held until LIVE; Omicron+Delta coordination required; RO-013 not executed here; PB-015 not started
Requested content amendments: None
Signature: SIGNED — HR-013 Publication Approver
```

| If APPROVE (this outcome) | Next |
|---------------------------|------|
| Volume authorised for joint LIVE | Schedule deploy + verify in **RO-013** |
| Educational student trust still blocked until LIVE Verified | Do not begin Wave 14 |
| LIVE deploy in HR-013 | **Not executed** — stop after publication decision |

---

### Summary

Publication Approver **APPROVES** CS1-015 / Campaign Omicron for joint LIVE activation. Prerequisites (Tutor · Founder · Auditor) met. No content amendments. LIVE deployment, RO-013, progressive confidence, and Wave 14 remain outside this programme. Published Coverage remains **63 / 72**. Student Reliance remains through Topic **4.2**. Wave 13 status: **Awaiting LIVE**.

Signed: HR-013 · Human Publication Approver · CS1-015 · 2026-08-03 · 15:45  
**Publication decision:** **APPROVED**  
**LIVE deploy/verify:** Authorised to prepare — **not executed**  
**Successor programme only:** **RO-013** — Wave 13 LIVE Release Operations (**not executed**)  
**Wave 14:** Not started  
**PB-015:** Not started  
**Published Coverage:** **63 / 72 (87.5%)** — **HELD**  
**Student Reliance:** Through Topic **4.2** — **HELD**  
**Wave 13:** **Awaiting LIVE**
