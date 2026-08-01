# EP-003 — Coverage Update (Wave 3 LIVE-complete)

**Programme:** EP-001 Production Era · Wave 3 (EP-003 artefacts)  
**Measurement date:** 2026-08-01  
**Authority:** `CE001_CATALOGUE_COVERAGE.md` (consumed; not amended) · `EP001_COVERAGE_MAP.md` · `EP003_WAVE3_PLAN.md`  
**Prerequisites met:** Wave 1 COMPLETE · Wave 2 COMPLETE · HR-003 APPROVE · RO-003 PASS · PB-005 PASS  

---

## 1. Purpose

Record the Continuity Front advance into **2.2** under Wave 3 / Volume **CS1-005** after human Publication Approver + LIVE verification (RO-003).

---

## 2. Dual view

| View | Pre–Wave 3 LIVE | Wave 3 LIVE-complete (this update) |
|------|-----------------|-------------------------------------|
| **A — Approver credit (Published)** | **28 / 72 (38.9%)** | **32 / 72 (44.4%)** — +4 Learning LOs (2.2.1–2.2.4) |
| **B — Live loader** | 40 packages | **45** — +5 Epsilon `publication_approved` |

---

## 3. Wave 3 geography

| Item | Value |
|------|-------|
| Volume | **CS1-005** |
| Campaign | `CS1-EP001-CAMPAIGN-EPSILON` |
| Learning span | **2.2.1 · 2.2.2 · 2.2.3 · 2.2.4** |
| Revision | CE-R1 return 2.2.1–2.2.4 |
| Catalogue root | `app/curriculum/data/educational_campaigns/cs1/campaign-epsilon-cs1005/` |
| Pipeline stage | **LIVE-complete** (RO-003 / PB-005) |
| Approver-credit increase | **+4 Learning LOs** → **32 / 72 (44.4%)** |
| Out of scope this wave | 2.3+ · Chapter 2 trophy · spine · until-exam trust · Wave 4 |

---

## 4. Topic / LO status delta

| LO | Previous | Wave 3 LIVE-complete |
|----|----------|----------------------|
| 2.2.1 | Under Authoring / APPROVED | **Published** + LIVE (CE-D1) |
| 2.2.2 | Under Authoring / APPROVED | **Published** + LIVE (CE-D2) |
| 2.2.3 | Under Authoring / APPROVED | **Published** + LIVE (CE-D3) |
| 2.2.4 | Under Authoring / APPROVED | **Published** + LIVE (CE-D4) |
| 2.3.1–2.6.6 | Missing | Missing (unchanged) |

**Continuity Front (student LIVE):** closed through **2.2.4** / CE-R1 (RO-003).  
**Next open geography:** **2.3** (Wave 4 — not started).

---

## 5. Contiguity picture (Wave 3 LIVE)

```text
LIVE / Approver credit:
  …──2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]     CS1-004 LIVE
                         │
                         ▼ Continuity Front handoff (RO-003)
                      2.2.1──2.2.2──2.2.3──2.2.4──[CE-R1]
                      [======== CS1-005 Epsilon LIVE ========]
  4.1──4.2──5.1──[CD-R*]                      CS1-003 LIVE

NEXT OPEN:   2.3 …
```

---

## 6. Inventory checklist

| Package ID | Day | LO | LIVE status |
|------------|-----|----|-------------|
| `CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL` | CE-D1 | 2.2.1 | `publication_approved` · LIVE Verified |
| `CS1-EP001-PKG-2.2-INDEPENDENCE` | CE-D2 | 2.2.2 | `publication_approved` · LIVE Verified |
| `CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION` | CE-D3 | 2.2.3 | `publication_approved` · LIVE Verified |
| `CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS` | CE-D4 | 2.2.4 | `publication_approved` · LIVE Verified |
| `CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS` | CE-R1 | Rev | `publication_approved` · LIVE Verified (Q6 residual) |

Catalogue copies remain `campaign_member_certified` under `campaign-epsilon-cs1005/packages/`.

---

## 7. Evidence

- Deploy tip: `efe18ad7b6384f48e06190fd576c5240b704dfec`  
- `RO003_DEPLOYMENT_REPORT.md` · `RO003_LIVE_VERIFICATION_REPORT.md` · `PB005_PROGRESSIVE_CONFIDENCE_REPORT.md` · `RO003_RELEASE_DECISION.md`  
- `knowledge/evidence/releases/RO003/` · `knowledge/evidence/releases/PB005/`

---

## 8. Closing

Wave 3 Continuity Front into 2.2 is **LIVE-complete**. Wave 4 remains **not started**. Until-exam trust **not** claimed.

Signed: EP-003 Coverage Update · RO-003 · 2026-08-01
