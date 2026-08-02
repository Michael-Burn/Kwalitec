# EP-006 — Coverage Update (Wave 6 LIVE-complete)

**Programme:** EP-001 Production Era · Wave 6 (EP-006 artefacts)  
**Measurement date:** 2026-08-02  
**Authority:** `CE001_CATALOGUE_COVERAGE.md` (consumed; not amended) · `EP001_COVERAGE_MAP.md` · `RO006_RELEASE_DECISION.md`  
**Prerequisites met:** HR-006 APPROVE · RO-006 Deployment PASS · RO-006 LIVE Verified · PB-008 PASS  

---

## 1. Purpose

Record Continuity Front advance through **2.5** under Wave 6 / Volume **CS1-008** after joint LIVE activation and verification. Approver + LIVE Verified credit applied for Learning LOs **2.5.1–2.5.2**.

---

## 2. Dual view

| View | Pre–Wave 6 LIVE | Wave 6 LIVE-complete (this update) |
|------|-----------------|--------------------------------------|
| **A — Approver credit (Published)** | **36 / 72 (50.0%)** | **38 / 72 (52.8%)** — +2 Learning LOs |
| **B — Live loader** | 51 packages | **54** — +3 Theta |
| **Pipeline (Under Authoring)** | 2 Learning LOs | **0** |

**Honesty:** LIVE Verified credit requires Approver + joint LIVE + verification — **met** for 2.5 (RO-006 / PB-008).

---

## 3. Wave 6 geography

| Item | Value |
|------|-------|
| Volume | **CS1-008** |
| Campaign | `CS1-EP001-CAMPAIGN-THETA` |
| Learning span | **2.5.1 · 2.5.2** |
| Revision | CT-R1 return 2.5.1–2.5.2 |
| Catalogue root | `app/curriculum/data/educational_campaigns/cs1/campaign-theta-cs1008/` |
| Pipeline stage | **LIVE-complete** |
| Approver-credit increase (this cycle) | **+2** → **38 / 72 (52.8%)** |
| Out of scope this wave | 2.6+ · Chapter 2 trophy · Chapter 3 inference · spine · until-exam trust · Wave 7 start |

---

## 4. Topic / LO status delta

| LO | Previous | Wave 6 LIVE-complete |
|----|----------|----------------------|
| 2.4.1–2.4.2 | Published + LIVE (CS1-007 · RO-005) | Unchanged |
| 2.5.1 | Under Authoring / APPROVED | **Published + LIVE** (CT-D1) |
| 2.5.2 | Under Authoring / APPROVED | **Published + LIVE** (CT-D2) |
| 2.6.1–2.6.6 | Missing | Missing (unchanged) |
| 3.1.1–3.3.5 | Missing | Missing (unchanged — Continuity Front law) |

**Continuity Front (student LIVE):** closed through **2.5.2** / CT-R1 (RO-006).  
**Next LIVE open after Wave 6 exit (provisional):** **2.6**.

---

## 5. Contiguity picture (Wave 6 LIVE)

```text
LIVE / Approver credit:
  …──2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]     CS1-004 LIVE
                         │
                         ▼
                      2.2.1──2.2.2──2.2.3──2.2.4──[CE-R1]
                      [======== CS1-005 Epsilon LIVE ========]
                                                                         │
                                                                         ▼
                      2.3.1──2.3.2──[CZ-R1]
                      [======== CS1-006 Zeta LIVE ========]
                                                                         │
                                                                         ▼
                      2.4.1──2.4.2──[CH-R1]
                      [======== CS1-007 Eta LIVE ========]
                                                                         │
                                                                         ▼
                      2.5.1──2.5.2──[CT-R1]
                      [======== CS1-008 Theta LIVE ========]

  4.1──4.2──5.1──[CD-R*]                      CS1-003 LIVE

NEXT OPEN AFTER WAVE 6 LIVE:   2.6 …
NOT THIS WAVE:                 3.1 … (inference series deferred)
NOT CLAIMED:                   Chapter 2 complete · until-exam trust · Wave 7 started
```

---

## 6. Inventory checklist

| Package ID | Day | LO | Catalogue status | LIVE status |
|------------|-----|----|------------------|-------------|
| `CS1-EP001-PKG-2.5-CLT` | CT-D1 | 2.5.1 | `campaign_member_certified` | **`publication_approved`** |
| `CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL` | CT-D2 | 2.5.2 | `campaign_member_certified` | **`publication_approved`** |
| `CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM` | CT-R1 | Rev | `campaign_member_certified` | **`publication_approved`** |

Campaign manifest status: `released`.

---

## 7. Operational metric registers (this update)

### 7A. Certified Educational Coverage Register

| Metric | Value |
|--------|-------|
| **Certified Educational Coverage (Approver credit)** | **38 / 72 (52.8%)** |
| Pipeline Under Authoring (Learning) | **0 / 72** |
| Live loader packages | **54** |

### 7B. Continuity Front Register

| Front | Location | Status |
|-------|----------|--------|
| Student LIVE Continuity Front | Closed through **2.5.2** / CT-R1 | LIVE Verified (RO-006) |
| Catalogue Continuity Front | Next open **2.6** (provisional) | Not commissioned |
| Next after Wave 6 LIVE (provisional) | **2.6** | Not commissioned |

### 7C. Student Reliance Coverage Register

| Metric | Value | Notes |
|--------|-------|-------|
| **Certified Educational Coverage (%)** | **52.8%** (38 / 72) | Approver-credited Published Learning LOs |
| **Continuity Front** | LIVE closed through **2.5.2** | Student-visible cliff now at 2.6 |
| **Student Reliance Coverage** | Contiguous first-pass CF reliance through **2.5.2** = **14** Learning LOs LIVE (Gamma→Theta); Trust Front independent **24** LOs (Delta); Alpha/Beta live loader without Approver credit (honesty gap) | EA-008: reliance follows contiguous certified journeys |
| **Until-examination status** | **NOT CLAIMED** | Open — spine / remainder unfinished |

---

## 8. Evidence

- Plan: `EP006_WAVE6_PLAN.md`  
- Catalogue: `app/curriculum/data/educational_campaigns/cs1/campaign-theta-cs1008/`  
- LIVE ops: `RO006_*` · `PB008_*`  
- Evidence: `knowledge/evidence/releases/RO006/` · `knowledge/evidence/releases/PB008/`  
- Tip: `a931f23628ba145b1bebbb190c53f2c555590110` · Deploy `dep-d9nclt2jnfac73aqle0g`  

---

## 9. Closing

Wave 6 Continuity Front through **2.5** is **LIVE-complete**. Approver credit **38 / 72 (52.8%)**. Student LIVE Continuity Front through **2.5.2**. Wave 7 **not started**. Until-exam trust **not** claimed. No forged seals.

```text
STOP — Wave 6 LIVE-complete · Wave 7 unblocked · not started · until-exam trust not claimed.
```

Signed: EP-006 Coverage Update · Wave 6 LIVE-complete · 2026-08-02
