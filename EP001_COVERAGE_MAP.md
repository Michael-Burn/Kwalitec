# EP-001 — CS1 Educational Coverage Map

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Subject:** IFoA CS1 · Syllabus 2026 (`app/curriculum/data/ifoa/cs1/2026.json`)  
**Measurement date:** 2026-08-02  
**Coverage definition:** `CE001_CATALOGUE_COVERAGE.md` (consumed; not amended)  
**Governance:** `EP001_GOVERNANCE.md`  
**Authority:** EF-001 · PB-002 PASS · CE-001 Measurement COMPLETE  
**Wave 3 companion:** `EP003_COVERAGE_UPDATE.md` · `EP003_WAVE3_PLAN.md`  
**Wave 4 companion:** `EP004_COVERAGE_UPDATE.md` · `EP004_WAVE4_PLAN.md`  
**Wave 5 companion:** `EP005_COVERAGE_UPDATE.md` · `EP005_WAVE5_PLAN.md`  
**Wave 6 companion:** `EP006_COVERAGE_UPDATE.md` · `EP006_WAVE6_PLAN.md`  
**Wave 7 companion:** `EP007_COVERAGE_UPDATE.md` · `EP007_WAVE7_PLAN.md`  
**Wave 8 companion:** `EP008_COVERAGE_UPDATE.md` · `EP008_WAVE8_PLAN.md`

---

## 1. Honesty dual view

EP-001 reports two facts that must not be conflated:

| View | Meaning | Current headline |
|------|---------|------------------|
| **A — Approver credit (CE-001 Published)** | Volume ≥ `approved` by human Publication Approver | **50 / 72 (69.4%)** — CS1-004 (4) + CS1-003 (24) + CS1-005 (4) + CS1-006 (2) + CS1-007 (2) + CS1-008 (2) + CS1-009 (6) + CS1-010 (6) Learning LOs |
| **B — Live loader inventory** | Packages under `educational_packages/cs1/` with `status: publication_approved` | **68 packages** (8 Alpha/Beta + **5 Gamma** + **27 Delta** + **5 Epsilon** + **3 Zeta** + **3 Eta** + **3 Theta** + **7 Iota** + **7 Kappa**; EA-006 orphan superseded) |

**Publication honesty gap:** CS1-001 and CS1-002 Volume dossiers remain `publication_ready` (Approver unsigned), while eight Alpha/Beta packages still load as `publication_approved`. CS1-004 Gamma, CS1-003 Delta, CS1-005 Epsilon, CS1-006 Zeta, and CS1-007 Eta hold Approver credit **and** LIVE package-path verification. CS1-008 Theta holds Approver credit **and** LIVE package-path verification (RO-006 / PB-008).

Orphan `4.2` is **superseded** by Campaign Delta (RO-002); Missing* for 4.2 cleared for catalogue coverage after LIVE supersession.

**Wave 5:** CS1-007 Eta **LIVE-complete** (RO-005 / PB-007) for 2.4.1–2.4.2 + Rev.  
**Wave 6:** CS1-008 Theta **LIVE-complete** (RO-006 / PB-008) for 2.5.1–2.5.2 + Rev.  
**Wave 7:** CS1-009 Iota **LIVE-complete** (RO-007 / PB-009) for 2.6.1–2.6.6 + Rev.  
**Wave 8:** CS1-010 Kappa **LIVE Verified (RO-008)** for 3.1.1–3.1.6 + Rev — PB-010 authorised · not executed.

---

## 2. Executive measurement

| Metric | Value | Notes |
|--------|------:|-------|
| Official topics | **14** | Sections 1–5 |
| Official LOs | **72** | Primary grain |
| **Published (Approver credit)** | **50 / 72 (69.4%)** | CS1-004 · 2.1.3–2.1.6 + CS1-005 · 2.2.1–2.2.4 + CS1-006 · 2.3.1–2.3.2 + CS1-007 · 2.4.1–2.4.2 + CS1-008 · 2.5.1–2.5.2 + CS1-009 · 2.6.1–2.6.6 + CS1-010 · 3.1.1–3.1.6 + CS1-003 · 4.1.1–5.1.9 — **advanced (RO-008)** |
| Awaiting Approval (Gate CG PASS · Volume `publication_ready`) | **9 / 72 (12.5%)** | CS1-001 + CS1-002 Learning LOs (Approver unsigned) |
| Under Review / Under Authoring | **0 / 72** | — |
| Live loader packages (`publication_approved`) | **61** | Alpha 4 + Beta 4 + Gamma 5 + Delta 27 + Epsilon 5 + Zeta 3 + Eta 3 + Theta 3 + Iota 7 (orphan superseded; Kappa absent) |
| Missing | **13 / 72** | Remaining spine after pipeline (3.2–3.3 etc.) |
| Continuity Front (Approver / LIVE) | **Closed through 3.1.6** / CK-R1 | RO-001 · RO-003 · RO-004 · RO-005 · RO-006 · RO-007 · RO-008 |
| Continuity Front (catalogue / pipeline) | **3.1 LIVE** (CS1-010); next **3.2** provisional | RO-008 · Wave 9 gated |
| Trust Remediation Front | **4.1 → 4.2 → 5.1** | Wave 2 **LIVE Verified** (RO-002) — Missing* cleared for 4.2 |
| Pipeline (Under Authoring) | **6 Learning LOs** | CS1-010 Kappa |

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
| **CS1-008** | `CS1-EP001-CAMPAIGN-THETA` | PASS (HR-006) | `released` (RO-006) | **Published** | **3 packages live** | 2.5.1–2.5.2 (+ Rev) — **Wave 6 LIVE** |
| **CS1-009** | `CS1-EP001-CAMPAIGN-IOTA` | PASS (HR-007) | `released` (RO-007) | **Published** | **7 packages live** | 2.6.1–2.6.6 (+ Rev) — **Wave 7 LIVE** |
| **CS1-010** | `CS1-EP001-CAMPAIGN-KAPPA` | PASS (HR-008) | `released` (RO-008) | **Published** | **7 packages live** | 3.1.1–3.1.6 (+ Rev) — **Wave 8 LIVE** |

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
| 2.5 | Central limit theorem | 2 | **Published** (CS1-008 / RO-006) | LIVE CT-D1…CT-D2 |
| 2.6 | Random sampling / sampling distributions | 6 | **Published** (CS1-009 / RO-007) | LIVE CI-D1…CI-D6 |
| 3.1 | Estimators and properties | 6 | **Published** (CS1-010 · RO-008) | LIVE Verified |
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
| 2.4.1 | Moment and cumulant generating functions | **Published** (CS1-007 · RO-005) | Yes (CH-D1) |
| 2.4.2 | Moments via series / differentiation of GF | **Published** (CS1-007 · RO-005) | Yes (CH-D2) |
| 2.5.1 | CLT for iid sequence | **Published** (CS1-008 · RO-006) | Yes (CT-D1) |
| 2.5.2 | Simulated samples vs Normal | **Published** (CS1-008 · RO-006) | Yes (CT-D2) |
| 2.6.1 | Random samples from a population | **Published** (CS1-009 · RO-007) | Yes (CI-D1) |
| 2.6.2 | Sampling distribution of a statistic | **Published** (CS1-009 · RO-007) | Yes (CI-D2) |
| 2.6.3 | Mean/var of sample mean; mean of sample variance | **Published** (CS1-009 · RO-007) | Yes (CI-D3) |
| 2.6.4 | Normal sampling distributions for mean/variance | **Published** (CS1-009 · RO-007) | Yes (CI-D4) |
| 2.6.5 | t-statistic for Normal samples | **Published** (CS1-009 · RO-007) | Yes (CI-D5) |
| 2.6.6 | F distribution for variance ratio | **Published** (CS1-009 · RO-007) | Yes (CI-D6) |
| 3.1.1 | Method of moments | **Published** (CS1-010 · RO-008) | Yes (CK-D1) |
| 3.1.2 | Maximum likelihood | **Published** (CS1-010 · RO-008) | Yes (CK-D2) |
| 3.1.3 | Efficiency, bias, consistency, MSE | **Published** (CS1-010 · RO-008) | Yes (CK-D3) |
| 3.1.4 | Estimator comparison via MSE | **Published** (CS1-010 · RO-008) | Yes (CK-D4) |
| 3.1.5 | Asymptotic distribution of MLEs | **Published** (CS1-010 · RO-008) | Yes (CK-D5) |
| 3.1.6 | Bootstrap for estimator properties | **Published** (CS1-010 · RO-008) | Yes (CK-D6) |
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
                                                                         ▼
                                                                      2.4.1──2.4.2──[CH-R1]
                                                                      [==== CS1-007 Eta LIVE ====]
                                                                         │
                                                                         ▼
                                                                      2.5.1──2.5.2──[CT-R1]
                                                                      [==== CS1-008 Theta LIVE ====]
                                                                         │
                                                                         ▼
                                                                      2.6.1──2.6.2──2.6.3──2.6.4──2.6.5──2.6.6──[CI-R1]
                                                                      [==== CS1-009 Iota LIVE (RO-007) ====]

CATALOGUE PIPELINE (Under Authoring — not Approver credit):
                                                                      3.1.1──3.1.2──3.1.3──3.1.4──3.1.5──3.1.6──[CK-R1]
                                                                      [==== CS1-010 Kappa UA (EP-008) ====]

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
| **Opening Continuity Front (student LIVE)** | Closed through **3.1.6** / CK-R1 | LIVE Verified | RO-008 |
| **Opening Continuity Front (catalogue)** | **3.1 LIVE** (CS1-010); next **3.2** | Wave 9 gated on PB-010 | Continuity Front law |
| **Next LIVE open after Wave 8 LIVE exit** | **3.2** (provisional) | Not commissioned | Continuity Front law |
| **Trust Remediation Front** | **4.1 → 4.2 → 5.1** | LIVE Verified | RO-002 / PB-004 |
| **Publication Front (Wave 0)** | CS1-001 / CS1-002 Approver | Open (honesty gap) | Not waived by Wave 8 |

### Student Reliance Coverage Register (operational metric)

| Metric | Value | Notes |
|--------|-------|-------|
| **Certified Educational Coverage (%)** | **69.4%** (50 / 72) | Approver-credited Published Learning LOs — **advanced (RO-008)** |
| **Continuity Front** | LIVE closed through **3.1.6**; next cliff **3.2** | Student-visible cliff at 3.2 until Wave 9 LIVE |
| **Student Reliance Coverage** | Contiguous first-pass CF reliance through **3.1.6** = **26** Learning LOs LIVE (Gamma→Kappa); Trust Front independent **24** LOs (Delta); Alpha/Beta live without Approver credit (honesty gap) | **Advanced (RO-008)** — EA-008 |
| **Until-examination status** | **NOT CLAIMED** | Open — spine / remainder unfinished |

**Definition:** Student Reliance Coverage reports how far a diligent student may place justified primary-study reliance on LIVE-certified, Approver-credited Continuity Front guidance without meeting Missing content — distinct from raw Approver % (includes non-contiguous Trust Front) and from until-exam trust.

### Bridge residual (honesty)

| Link | Observed | Risk |
|------|----------|------|
| CA-R1 `tomorrow_preview.next_topic_code` | `2.1` | May skip 1.2.3 (PCA) after Alpha Revision — package metadata residual (PB-002 / CE-001) |
| CB-R1 → CG-D1 | Selection resolves CG-D1 after Beta complete (RO-001) | Finish/Home tomorrow chrome residual RO1-R1 (stale 2.1.2 text) |
| CG-R1 → CE-D1 | Selection + LIVE verify PASS (RO-003) | CE-R1 chrome / Q6 residual RO3-R1 / RO3-R2 |
| CE-R1 → CZ-D1 | Selection + LIVE verify PASS (RO-004) | RO4-R1 Home title collision; CZ-R1 chrome / Q6 RO4-R2/R3 |
| CZ-R1 → CH-D1 | Selection + LIVE verify PASS (RO-005) | RO5-R1 label desync / Home collision class; CH-R1 chrome / Q6 RO5-R2/R3 |
| CH-R1 → CT-D1 | Selection + LIVE verify PASS (RO-006) | RO6-R1 label desync; CT-R1 chrome / Q6 RO6-R2/R3 |
| CT-R1 → CI-D1 | Selection + LIVE verify PASS (RO-007) | RO7-R1 residual class (PI) |
| CI-R1 → CK-D1 | Catalogue handoff authored (EP-008) | LIVE selection deferred until Approver + deploy |

---

## 7. Section roll-up (Approver credit)

| Section | LOs | Published | Awaiting Approval | Under Authoring | Missing | Live orphan note |
|--------:|----:|----------:|------------------:|----------------:|--------:|------------------|
| 1 | 7 | 0 | 7 | 0 | 0 | Alpha/Beta live |
| 2 | 22 | **20** | 2 | 0 | 0 | Gamma–Iota LIVE |
| 3 | 19 | **6** | 0 | 0 | **13** | Kappa LIVE 3.1 |
| 4 | 15 | **15** | 0 | 0 | 0 | orphan superseded (RO-002) |
| 5 | 9 | **9** | 0 | 0 | 0 | Delta LIVE |
| **Total** | **72** | **44** | **9** | **6** | **13** | — |

---

## 8. Map maintenance

1. Re-measure when Volume Approver signs (Awaiting Approval / Under Authoring → Published).  
2. Re-measure when Wave packages certify / approve / go LIVE.  
3. Never move Missing* to Published without Campaign Gate CG + Approver.  
4. Continuity Front LIVE closed through 3.1.6 (RO-008); Wave 9 gated on PB-010.  
5. Keep LO universe pinned to CS1 2026 JSON.  
6. Refresh Student Reliance Coverage Register whenever Continuity Front or Approver credit moves.  
7. Do not advance Certified Educational Coverage or Student Reliance past 3.1.6 until Wave 9 Approver + LIVE.

---

## 9. Closing

Wave 1–8 LIVE Approver credit stands at **50 / 72 (69.4%)**. Campaign Kappa / CS1-010 is **LIVE Verified (RO-008)** for 3.1.1–3.1.6 + CK-R1. Student Continuity Front / Student Reliance Coverage through **3.1.6** LIVE. PB-010 authorised · not executed. Wave 9 not started. No forged seals. Until-exam trust not claimed.

**Companions:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` · `EP001_WAVE1_PLAN.md` · `EP001_WAVE2_PLAN.md` · `EP003_WAVE3_PLAN.md` · `EP003_COVERAGE_UPDATE.md` · `EP004_WAVE4_PLAN.md` · `EP004_COVERAGE_UPDATE.md` · `EP005_WAVE5_PLAN.md` · `EP005_COVERAGE_UPDATE.md` · `EP006_WAVE6_PLAN.md` · `EP006_COVERAGE_UPDATE.md` · `EP007_WAVE7_PLAN.md` · `EP007_COVERAGE_UPDATE.md` · `EP008_WAVE8_PLAN.md` · `EP008_COVERAGE_UPDATE.md` · `RO007_*` · `PB009_*` · `CE001_CATALOGUE_COVERAGE.md`

Signed notionally: Editorial Director · EP-001 · Coverage Map · 2026-08-02
