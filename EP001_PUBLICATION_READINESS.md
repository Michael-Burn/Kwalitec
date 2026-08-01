# EP-001 — Publication Readiness (Campaign Alpha)

**Programme:** Educational Production Programme EP-001  
**Campaign:** `CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0`  
**Scope class:** Pilot Arc  
**Gate CG:** **PASS** (`EP001_CAMPAIGN_CERTIFICATION.md`)  
**Publication pattern:** AP-01 Certified Pilot Arc (`EA008_CAMPAIGN_PUBLICATION_POLICY.md`)  
**Date:** 2026-08-01  

---

## 1. Publication unit

The publication unit is the **Campaign** (ordered inventory + Revision Strategy), not any single day.

| Package ID | Day | Mode | Live auto-load today? |
|------------|-----|------|----------------------|
| `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | CA-D1 | Learning | **No** |
| `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | CA-D2 | Learning | **No** |
| `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | CA-D3 | Learning | **No** |
| `CS1-EP001-PKG-REV-PURPOSE-EDA` | CA-R1 | Revision | **No** |

Catalogue root:

`app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/`

Package status: `campaign_member_certified` (outside EA-006 live approval enum).

---

## 2. Forbidden patterns check (FP)

| ID | Pattern | Status |
|----|---------|--------|
| FP-01 Isolated Golden Day | **DENIED** — joint inventory |
| FP-02 Coverage mirage | **DENIED** — Pilot Arc claims only; PCA/spine not claimed |
| FP-03 Template filler neighbours | **DENIED** — all days certified substance |
| FP-04 Non-reciprocal bridges | **DENIED** — 100% bridge integrity |
| FP-05 Revision-absent | **DENIED** — CA-R1 present |
| FP-06 Silent orphan warning | **DENIED** — membership explicit |

---

## 3. Preconditions to enter Campaign Publication Approval

| # | Precondition | Status |
|---|--------------|--------|
| 1 | Gate CG PASS | **Met** |
| 2 | EA-002-class substance for every bundle | **Met** (Board desk certification) |
| 3 | CI + bridge integrity recorded | **Met** (CI 8.75; bridges 100%) |
| 4 | EV-001 / EA-007 regression checklists | **Met** (Certification Trust table) |
| 5 | Inventory 100% certified members | **Met** |
| 6 | Technical publish ≠ Campaign PASS stated | **Met** (this document) |
| 7 | Isolated Golden Day denied | **Met** |

**Campaign Publication Approval: READY TO REQUEST** for scoped Pilot Arc inventory.

---

## 4. Activation engineering note (outside EP-001 code scope)

EP-001 does **not** modify application code or Runtime. Live Learning Mode still resolves packages via `educational_packages/` loader (EA-006). To activate Campaign Alpha commercially after Board Approval:

1. Publication Approver signs Approval for `CS1-EP001-CAMPAIGN-ALPHA` `ep001-1.0.0`.  
2. Successor engineering programme (not EP-001) must support **multi-package same `topic_code`** (1.2 Day A vs Day B) or sequential day keys — current loader returns first match only.  
3. Copy or register approved packs with `publication_approved` only after (1)–(2).  
4. Do not activate a single Alpha day alone (would recreate FP-01).

Until then, Campaign Alpha remains **catalogue-certified, student-pathway gated**.

---

## 5. Claims allowed vs forbidden after Approval

| Allowed | Forbidden |
|---------|-----------|
| “Certified Pilot Arc for CS1 Data Analysis opening (1.1–1.2.2 + revision)” | “CS1 Educational Excellence campaign complete” |
| “Primary study endorsed for this Pilot Arc span” | “Semester / first-pass spine continuity PASS” |
| “Sets catalogue standard for future Campaigns” | “EA-007 FAIL cleared” |
| Honest deferral of PCA 1.2.3 | Silent claim that Chapter 1 is finished including PCA |
| 4.2 remains `pre-campaign-pilot` until absorbed | Treating Alpha as absorption of 4.2 |

---

## 6. Grandfather interaction

EA-006 CS1 4.2 package remains grandfathered `pre-campaign-pilot`. Campaign Alpha does **not** absorb it. Scale claims that cite 4.2 alone remain forbidden per EA-008 Policy §7.

---

## 7. Publication Approver worksheet

| Check | Initials / date |
|-------|-----------------|
| Gate CG evidence pack reviewed | _pending human Approver_ |
| FP-01…FP-06 denied | _pending_ |
| Activation engineering dependencies acknowledged | _pending_ |
| Marketing claims constrained to Pilot Arc | _pending_ |

**Board recommendation:** Approve Campaign publication **when** Approver signs and activation dependencies are scheduled — educational readiness is met; live pathway readiness is gated as above.

---

Signed notionally: Publication Readiness Author · EP-001 · 2026-08-01
