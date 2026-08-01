# DSH-001 — Current Baseline (CS1)

**Programme:** Strategic Educational Metrics — DSH-001  
**Subject:** IFoA CS1 · Syllabus 2026  
**Measurement date:** 2026-08-01  
**Definition:** `DSH001_METRIC_SPECIFICATION.md`  
**Coverage companion:** `CE001_CS1_COVERAGE_MAP.md` · `CE001_CATALOGUE_COVERAGE.md`  
**Authority:** EA-001…EA-008 (Frozen) · EP-001 · EO-001 · PR-001 · DX-001 · CE-001  

---

## 1. Executive verdict

| Metric | Value | Interpretation |
|--------|------:|----------------|
| **Dependable Study Horizon (DSH)** | **0 study days** | No Publication-Approved Volume on the opening path |
| DSH (hours) | **0.0 h** | — |
| Horizon Tip (Opening Continuity Front) | **Day 1 / LO 1.1.1** | Opening path not yet Published — tip is the first Learning day |
| **Certified Inventory Horizon (CIH)** | **8 study days** | CS1-001 + CS1-002 · Awaiting Approval only — **not DSH** |
| CIH (hours, midpoints) | **≈ 7.7 h** (6.4–8.9 h band) | Package duration budgets |
| CIH Horizon Tip | **LO 2.1.3** | Named handoff after CS1-002 Revision (DX-001 CF-05) |
| Published LO Coverage (CE-001) | **0 / 72 (0%)** | Consistent with DSH = 0 |
| Pipeline LOs (Awaiting Approval) | **9 / 72** | Does not extend DSH |

### One-line baseline

> **CS1 DSH today is zero.** Eight authored, Gate-CG-certified, DX-validated study days exist in inventory — but until Publication Approver seals convert them to Published, a student cannot *depend* on them as Kwalitec’s certified companion path.

---

## 2. Measurement method applied

Per `DSH001_METRIC_SPECIFICATION.md` §5:

1. Opening path ordered from Campaign Alpha CA-D1 (LO family 1.1).  
2. Eligibility E1–E7 applied day-by-day.  
3. E4 fails immediately: both CS1-001 and CS1-002 remain `publication_ready` (Approver **PENDING**).  
4. Therefore \(\mathrm{DSH}_{\text{days}} = 0\).  
5. CIH walk (E4 relaxed to `publication_ready`) yields **8** contiguous days ending before **2.1.3**.

**Excluded from DSH and CIH:** drafts, placeholders, EA-006 orphan `4.2` (`Missing*`), uncommissioned CS1-003/CS1-004, any mid-spine island.

---

## 3. Opening path inventory (day walk)

| Order | Day | Volume | Package | Mode | Primary LOs | Duration (min) | Gate CG | Volume status | DSH eligible? | CIH eligible? |
|------:|-----|--------|---------|------|-------------|----------------|---------|---------------|---------------|---------------|
| 1 | CA-D1 | CS1-001 | Purpose / function | Learning | 1.1.1–1.1.4 | 45–65 | PASS | `publication_ready` | **No** (E4) | Yes |
| 2 | CA-D2 | CS1-001 | EDA summaries | Learning | 1.2.1 | 50–70 | PASS | `publication_ready` | No | Yes |
| 3 | CA-D3 | CS1-001 | EDA association | Learning | 1.2.2 | 50–70 | PASS | `publication_ready` | No | Yes |
| 4 | CA-R1 | CS1-001 | Revision Purpose–EDA | Revision | return 1.1 · 1.2.1–1.2.2 | 40–55 | PASS | `publication_ready` | No | Yes |
| 5 | CB-D1 | CS1-002 | PCA | Learning | 1.2.3 | 50–70 | PASS | `publication_ready` | No | Yes |
| 6 | CB-D2 | CS1-002 | Discrete distributions | Learning | 2.1.1 | 55–75 | PASS | `publication_ready` | No | Yes |
| 7 | CB-D3 | CS1-002 | Continuous distributions | Learning | 2.1.2 | 55–75 | PASS | `publication_ready` | No | Yes |
| 8 | CB-R1 | CS1-002 | Revision PCA–distributions | Revision | return 1.2.2–1.2.3 · 2.1.1–2.1.2 | 40–55 | PASS | `publication_ready` | No | Yes |
| — | **Front** | — | — | — | **2.1.3** | — | — | Missing | Ends horizon | Ends CIH |

**Bridge integrity (CIH path):** 100% internal (DX-001); Alpha→Beta PASS with documented CF-01 mild foreshadow.  
**Delivery quality (CIH path):** DX-001 PASS (DQI ≈ 8.8/10) — quality proven; dependence not yet Publication-sealed.

### Duration roll-up (CIH only)

| Band | Minutes | Hours |
|------|--------:|------:|
| Minimum | 385 | 6.4 |
| Midpoint | 460 | 7.7 |
| Maximum | 535 | 8.9 |

---

## 4. Volume contribution worksheet

| volume_id | Campaign | Study days | If Approved contiguous | Current DSH contribution | Notes |
|-----------|----------|----------:|------------------------|-------------------------:|-------|
| **CS1-001** | Alpha `ep001-1.0.0` | 4 | +4 days from day 1 | **0** | Approver PENDING · PR-001 VD-01 |
| **CS1-002** | Beta `cs1002-1.0.0` | 4 | +4 days after CS1-001 | **0** | Requires CS1-001 Approved first (FR-03 continuity) |
| CS1-004 (planned) | Opening Front closer | TBD | Extends past 2.1.3 | 0 | Not commissioned (CE-001 P1) |
| CS1-003 (planned) | Mid-spine absorption | TBD | Trust Band only until Front reaches §4 | 0 | Parallel geography (CE-001 P2) |
| EA-006 `4.2` orphan | — | — | **Never** Opening DSH alone | 0 | Missing* · FP-01 |

**Projected DSH if Approvers sign CS1-001 then CS1-002 (and path later released):** **8 study days** · Horizon Tip **2.1.3**.

That projection is **CIH realisation**, not a present claim.

---

## 5. Continuity picture

```text
DSH (Published dependence):     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0 days

CIH (Awaiting Approval only — NOT DSH):
  J1──J2──J3──J4──J5──J6──J7──J8
  [==== CS1-001 Alpha ====][==== CS1-002 Beta ====]
                                                   │
                                                   ▼ Horizon Tip (CIH)
                                                2.1.3 ── 2.1.4 … (Missing)

TRUST BAND:                     (none Published; 4.2 orphan does not form a band)
```

---

## 6. Evidence register

| Evidence | Path / fact |
|----------|-------------|
| Metric law | `DSH001_METRIC_SPECIFICATION.md` |
| Coverage = 0 Published | `CE001_CS1_COVERAGE_MAP.md` |
| CS1-001 status `publication_ready` | `PR001_VOLUME_REGISTER.md` §3 · Approver PENDING |
| CS1-002 status `publication_ready` | `CS1002_EDUCATIONAL_VOLUME.md` · `CS1002_PUBLICATION_READINESS.md` |
| Eight-day contiguous walk | `DX001_STUDENT_JOURNEY_AUDIT.md` · `DX001_CONTINUITY_FINDINGS.md` |
| Continuity Front 2.1.3 | CS1-002 CB-R1 terminal · DX-001 CF-05 · CE-001 |
| Duration budgets | Campaign package JSON `estimated_study_time_minutes` |
| Orphan exclusion | `EA006_PUBLICATION_REPORT.md` · CE-001 Missing* |
| Syllabus universe | `app/curriculum/data/ifoa/cs1/2026.json` (72 LOs) |

---

## 7. Student / Founder / commercial snapshot

| Audience | What to say today |
|----------|-------------------|
| **Student** | Do **not** quote a Dependable Study Horizon number. Certified opening days are not yet Publication-approved / released. |
| **Founder** | **DSH = 0**. CIH = 8. Red status light: sealed inventory waiting on Approver. Next DSH-extending acts: Approve CS1-001 → Approve CS1-002 → release; then commission CS1-004 at 2.1.3. |
| **Commercial** | Report **0 dependable study days** published. Disclose 8-day certified inventory as *pipeline*, never as live horizon. |

---

## 8. Baseline change log

| Date | DSH | CIH | Event |
|------|----:|----:|-------|
| 2026-08-01 | **0** | **8** | DSH-001 inaugural baseline |

---

## 9. Closing

Educational quality on the opening eight days is not the open question — EP-001, CS1-002, and DX-001 already held that bar. **Dependence** is the open question. Until Approver seals land, Kwalitec’s Dependable Study Horizon for CS1 remains honestly **zero**.

Signed notionally: Chief Academic Officer · DSH-001 Current Baseline · 2026-08-01
