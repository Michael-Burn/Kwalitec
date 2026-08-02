# EP-001 — CS1 Educational Coverage Map

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Subject:** IFoA CS1 · Syllabus 2026 (`app/curriculum/data/ifoa/cs1/2026.json`)  
**Measurement date:** 2026-08-01  
**Coverage definition:** `CE001_CATALOGUE_COVERAGE.md` (consumed; not amended)  
**Governance:** `EP001_GOVERNANCE.md`  
**Authority:** EF-001 · PB-002 PASS · CE-001 Measurement COMPLETE  
**Wave 3 companion:** `EP003_COVERAGE_UPDATE.md` · `EP003_WAVE3_PLAN.md`  
**Wave 4 companion:** `EP004_COVERAGE_UPDATE.md` · `EP004_WAVE4_PLAN.md`  
**Wave 5 companion:** `EP005_COVERAGE_UPDATE.md` · `EP005_WAVE5_PLAN.md`

---

## 1. Honesty dual view

EP-001 reports two facts that must not be conflated:

| View | Meaning | Current headline |
|------|---------|------------------|
| **A — Approver credit (CE-001 Published)** | Volume ≥ `approved` by human Publication Approver | **36 / 72 (50.0%)** — CS1-004 (4) + CS1-003 (24) + CS1-005 (4) + CS1-006 (2) + CS1-007 (2) Learning LOs |
| **B — Live loader inventory** | Packages under `educational_packages/cs1/` with `status: publication_approved` | **51 packages** (8 Alpha/Beta + **5 Gamma** + **27 Delta** + **5 Epsilon** + **3 Zeta** + **3 Eta**; EA-006 orphan superseded) |

**Publication honesty gap:** CS1-001 and CS1-002 Volume dossiers remain `publication_ready` (Approver unsigned), while eight Alpha/Beta packages still load as `publication_approved`. CS1-004 Gamma, CS1-003 Delta, CS1-005 Epsilon, CS1-006 Zeta, and CS1-007 Eta hold Approver credit **and** LIVE package-path verification.

Orphan `4.2` is **superseded** by Campaign Delta (RO-002); Missing* for 4.2 cleared for catalogue coverage after LIVE supersession.

**Wave 4:** CS1-006 Zeta **LIVE-complete** (RO-004 / PB-006) for 2.3.1–2.3.2 + Rev.  
**Wave 5:** CS1-007 Eta **LIVE-complete** (RO-005 / PB-007) for 2.4.1–2.4.2 + Rev.

---

## 2. Executive measurement

| Metric | Value | Notes |
|--------|------:|-------|
| Official topics | **14** | Sections 1–5 |
| Official LOs | **72** | Primary grain |
| **Published (Approver credit)** | **36 / 72 (50.0%)** | CS1-004 · 2.1.3–2.1.6 + CS1-005 · 2.2.1–2.2.4 + CS1-006 · 2.3.1–2.3.2 + CS1-007 · 2.4.1–2.4.2 + CS1-003 · 4.1.1–5.1.9 |
| Awaiting Approval (Gate CG PASS · Volume `publication_ready`) | **9 / 72 (12.5%)** | CS1-001 + CS1-002 Learning LOs (Approver unsigned) |
| Under Review / Under Authoring | **0 / 72** | Wave 5 LIVE-complete; next pipeline not commissioned |
| Live loader packages (`publication_approved`) | **51** | Alpha 4 + Beta 4 + Gamma 5 + Delta 27 + Epsilon 5 + Zeta 3 + Eta 3 (orphan superseded) |
| Missing | **27 / 72** | Remaining spine (next LIVE open: **2.5**; sections 3 / 5.2+ etc.) |
| Continuity Front (Approver / LIVE) | **Closed through 2.4.2** / CH-R1 | RO-001 · RO-003 · RO-004 · RO-005 |
| Continuity Front (catalogue / pipeline) | **Open at 2.5** (not commissioned) | Wave 6 gated · not started |
| Trust Remediation Front | **4.1 → 4.2 → 5.1** | Wave 2 **LIVE Verified** (RO-002) — Missing* cleared for 4.2 |
| Pipeline (Under Authoring) | **0 Learning LOs** | Wave 5 LIVE-complete |

---

## 3. Volume / Campaign inventory

| volume_id | Campaign | Gate CG | EO status | Approver credit | Live loader | Syllabus span (Learning) |
|-----------|----------|---------|-----------|-----------------|-------------|--------------------------|
| **CS1-001** | `CS1-EP001-CAMPAIGN-ALPHA` | PASS | `publication_ready` | Not Published | 4 packages live | 1.1 · 1.2.1 · 1.2.2 (+ Rev) |
| **CS1-002** | `CS1-CS1002-CAMPAIGN-BETA` | PASS | `publication_ready` | Not Published | 4 packages live | 1.2.3 · 2.1.1 · 2.1.2 (+ Rev) |
| — | EA-006 `4.2-glm-structure` | Campaign absent | Grandfather | **Not coverage** | **Superseded (RO-002)** | absorbed into Delta CD-D6…CD-D8 |
| **CS1-004** | `CS1-EP001-CAMPAIGN-GAMMA` | PASS (HR-001) | `released` | **Published** (2.1.3–2.1.6) | **5 packages live** | 2.1.3–2.1.6 (+ Rev) — **Wave 1 LIVE** |
| **CS1-003** | `CS1-EP001-CAMPAIGN-DELTA` | PASS (HR-002) | `released` (RO-002) | **Published** (Approver+LIVE) | **27 packages live** | 4.1.1–5.1.9 (+ 3 Rev) — **Wave 2 LIVE** |
| **CS1-005** | `CS1-EP001-CAMPAIGN-EPSILON` | PASS (HR-003) | `released` (RO-003) | **Published** (Approver+LIVE) | **5 packages live** | 2.2.1–2.2.4 (+ Rev) — **Wave 3 LIVE** |
| **CS1-006** | `CS1-EP001-CAMPAIGN-ZETA` | PASS (HR-004) | `released` (RO-004) | **Published** | **3 packages live** | 2.3.1–2.3.2 (+ Rev) — **Wave 4 LIVE** |
| **CS1-007** | `CS1-EP001-CAMPAIGN-ETA` | PASS (HR-005) | `released` (RO-005) | **Published** | **3 packages live** | 2.4.1–2.4.2 (+ Rev) — **Wave 5 LIVE** |

---

## 4. Topic-level map

| Topic | Title | LOs | Approver status | Live loader note |
|-------|-------|----:|-----------------|------------------|
| 1.1 | Purpose and function of data analysis | 4 | Awaiting Approval | Alpha packages live |
| 1.2 | Exploratory data analysis | 3 | Awaiting Approval | Alpha + Beta PCA live |
| 2.1 | Univariate distributions / generation | 6 | Partial (**2.1.3–2.1.6 Published**; 2.1.1–2.1.2 AA) | Beta + **Gamma LIVE** |
| 2.2 | Jointly distributed RVs | 4 | **Published** (CS1-005 / RO-003) | LIVE CE-D1…CE-D4 |
| 2.3 | Expectations / conditional expectations | 2 | **Published** (CS1-006 / RO-004) | LIVE CZ-D1…CZ-D2 |
| 2.4 | Generating functions | 2 | **Published** (CS1-007 / RO-005) | LIVE CH-D1…CH-D2 |
| 2.5 | Central limit theorem | 2 | Missing | — |
| 2.6 | Random sampling / sampling distributions | 6 | Missing | — |
| 3.1 | Estimators and properties | 6 | Missing | — |
| 3.2 | Confidence and prediction intervals | 8 | Missing | — |
| 3.3 | Hypothesis testing and goodness of fit | 5 | Missing | — |
| 4.1 | Linear regression models | 5 | **Published** (CS1-003 / RO-002) | LIVE CD-D1…CD-D5 |
| 4.2 | Generalised linear models | 10 | **Published** (CS1-003 / RO-002) | LIVE CD-D6…CD-D15; orphan superseded |
| 5.1 | Bayesian statistics | 9 | **Published** (CS1-003 / RO-002) | LIVE CD-D16…CD-D24 |

---

## 5. LO-level map (Approver credit + live)

Statuses: **Published** (Approver) · **Awaiting Approval** · **Under Authoring** · **Missing** · **Missing\*** (orphan).  
**Live** = package resolves in `educational_packages/cs1/` as `publication_approved`.

| LO | Description (short) | Approver status | Live |
|----|---------------------|-----------------|------|
| 1.1.1 | Aims of a data analysis | Awaiting Approval | Yes (Alpha D1) |
| 1.1.2 | Stages and tools | Awaiting Approval | Yes |
| 1.1.3 | Sources / large data sets | Awaiting Approval | Yes |
| 1.1.4 | Reproducible research | Awaiting Approval | Yes |
| 1.2.1 | Summary statistics / EDA visuals | Awaiting Approval | Yes (Alpha D2) |
| 1.2.2 | Correlation measures | Awaiting Approval | Yes (Alpha D3) |
| 1.2.3 | Principal component analysis | Awaiting Approval | Yes (Beta D1) |
| 2.1.1 | Discrete distributions | Awaiting Approval | Yes (Beta D2) |
| 2.1.2 | Continuous distributions | Awaiting Approval | Yes (Beta D3) |
| 2.1.3 | Probabilities and quantiles | **Published** (CS1-004 · RO-001) | Yes (CG-D1) |
| 2.1.4 | Poisson process / exponential | **Published** (CS1-004 · RO-001) | Yes (CG-D2) |
| 2.1.5 | Generation (inverse transform) | **Published** (CS1-004 · RO-001) | Yes (CG-D3) |
| 2.1.6 | Generation (software) | **Published** (CS1-004 · RO-001) | Yes (CG-D4) |
| 2.2.1 | Marginal / conditional distributions | **Published** (CS1-005 · RO-003) | Yes (CE-D1) |
| 2.2.2 | Independence conditions | **Published** (CS1-005 · RO-003) | Yes (CE-D2) |
| 2.2.3 | Covariance, correlation, E[g(X,Y)] | **Published** (CS1-005 · RO-003) | Yes (CE-D3) |
| 2.2.4 | Mean/variance of linear combinations | **Published** (CS1-005 · RO-003) | Yes (CE-D4) |
| 2.3.1 | Conditional expectation given another RV | **Published** (CS1-006 · RO-004) | Yes (CZ-D1) |
| 2.3.2 | Mean/variance via conditioning | **Published** (CS1-006 · RO-004) | Yes (CZ-D2) |
| 2.4.1 | Moment and cumulant generating functions | **Under Authoring** (CS1-007) | No |
| 2.4.2 | Moments via series / differentiation of GF | **Under Authoring** (CS1-007) | No |
| 2.5.1–2.5.2 | CLT | Missing | No |
| 2.6.1–2.6.6 | Sampling distributions | Missing | No |
| 3.1.1–3.1.6 | Estimators | Missing | No |
| 3.2.1–3.2.8 | Intervals | Missing | No |
| 3.3.1–3.3.5 | Hypothesis testing | Missing | No |
| 4.1.1–4.1.5 | Linear regression | **Published** (CS1-003) | Yes (RO-002 package path) |
| 4.2.1–4.2.10 | GLM | **Published** (CS1-003); Missing* cleared | Yes — orphan superseded |
| 5.1.1–5.1.9 | Bayesian | **Published** (CS1-003) | Yes (RO-002 package path) |

---

## 6. Contiguity picture

```text
APPROVER CREDIT (Published Continuity Front LIVE):
  2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]──2.2.1──2.2.2──2.2.3──2.2.4──[CE-R1]──2.3.1──2.3.2──[CZ-R1]
  [======== CS1-004 LIVE ========][======== CS1-005 LIVE (RO-003) ========][== CS1-006 LIVE ==]
                                                                         │
                                                                         ▼ named handoff (not LIVE)
PIPELINE (Wave 5 Under Authoring — catalogue only):
                                                                      2.4.1──2.4.2──[CH-R1]
                                                                      [==== CS1-007 Eta ====]

PIPELINE (Awaiting Approval) + LIVE LOADER (Alpha/Beta):
  1.1.1──…──1.2.2──1.2.3──2.1.1──2.1.2──…
  [==== CS1-001 ====][==== CS1-002 ====]

TRUST FRONT (Wave 2 LIVE Verified — RO-002):
  4.1 (Published) ── 4.2 (Published; orphan superseded) ── 5.1 (Published) ── [CD-R1/R2/R3]
  [==================== CS1-003 Campaign Delta LIVE ====================]
```

### Continuity Front Register (current)

| Front | Location | Status | Source |
|-------|----------|--------|--------|
| **Opening Continuity Front (student LIVE)** | Closed through **2.4.2** / CH-R1 | LIVE Verified | RO-005 / PB-007 |
| **Opening Continuity Front (catalogue)** | Open at **2.5** (not commissioned) | Next Wave | Continuity Front law |
| **Next LIVE open after Wave 5 exit** | **2.5** (provisional) | Not commissioned | Continuity Front law |
| **Trust Remediation Front** | **4.1 → 4.2 → 5.1** | LIVE Verified | RO-002 / PB-004 |
| **Publication Front (Wave 0)** | CS1-001 / CS1-002 Approver | Open (honesty gap) | Not waived by Wave 5 |

### Bridge residual (honesty)

| Link | Observed | Risk |
|------|----------|------|
| CA-R1 `tomorrow_preview.next_topic_code` | `2.1` | May skip 1.2.3 (PCA) after Alpha Revision — package metadata residual (PB-002 / CE-001) |
| CB-R1 → CG-D1 | Selection resolves CG-D1 after Beta complete (RO-001) | Finish/Home tomorrow chrome residual RO1-R1 (stale 2.1.2 text) |
| CG-R1 → CE-D1 | Selection + LIVE verify PASS (RO-003) | CE-R1 chrome / Q6 residual RO3-R1 / RO3-R2 |
| CE-R1 → CZ-D1 | Selection + LIVE verify PASS (RO-004) | RO4-R1 Home title collision; CZ-R1 chrome / Q6 RO4-R2/R3 |
| CZ-R1 → CH-D1 | Selection + LIVE verify PASS (RO-005) | RO5-R1 label desync / Home collision class; CH-R1 chrome / Q6 RO5-R2/R3 |

---

## 7. Section roll-up (Approver credit)

| Section | LOs | Published | Awaiting Approval | Under Authoring | Missing | Live orphan note |
|--------:|----:|----------:|------------------:|----------------:|--------:|------------------|
| 1 | 7 | 0 | 7 | 0 | 0 | Alpha/Beta live |
| 2 | 22 | **12** | 2 | **0** | 8 | Gamma LIVE 2.1.3–2.1.6; Epsilon LIVE 2.2.1–2.2.4; Zeta LIVE 2.3.1–2.3.2; Eta LIVE 2.4.1–2.4.2 |
| 3 | 19 | 0 | 0 | 0 | 19 | — |
| 4 | 15 | **15** | 0 | 0 | 0 | orphan superseded (RO-002) |
| 5 | 9 | **9** | 0 | 0 | 0 | Delta LIVE |
| **Total** | **72** | **36** | **9** | **0** | **27** | — |

---

## 8. Map maintenance

1. Re-measure when Volume Approver signs (Awaiting Approval / Under Authoring → Published).  
2. Re-measure when Wave packages certify / approve / go LIVE.  
3. Never move Missing* to Published without Campaign Gate CG + Approver.  
4. Continuity Front LIVE closed through 2.4.2 (RO-005); next open at **2.5** (Wave 6 not started).  
5. Keep LO universe pinned to CS1 2026 JSON.

---

## 9. Closing

Wave 1 + Wave 2 + Wave 3 + Wave 4 + Wave 5 LIVE Approver credit stands at **36 / 72 (50.0%)**. Campaign Eta / CS1-007 is **LIVE-complete** for 2.4.1–2.4.2 + CH-R1. Student Continuity Front closed through **2.4.2** LIVE. Wave 6 not started. No forged seals. Until-exam trust not claimed.

**Companions:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` · `EP001_WAVE1_PLAN.md` · `EP001_WAVE2_PLAN.md` · `EP003_WAVE3_PLAN.md` · `EP003_COVERAGE_UPDATE.md` · `EP004_WAVE4_PLAN.md` · `EP004_COVERAGE_UPDATE.md` · `EP005_WAVE5_PLAN.md` · `EP005_COVERAGE_UPDATE.md` · `RO005_*` · `PB007_*` · `CE001_CATALOGUE_COVERAGE.md`

Signed notionally: Editorial Director · EP-001 · Coverage Map · 2026-08-02
