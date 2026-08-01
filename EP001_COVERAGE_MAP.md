# EP-001 — CS1 Educational Coverage Map

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Subject:** IFoA CS1 · Syllabus 2026 (`app/curriculum/data/ifoa/cs1/2026.json`)  
**Measurement date:** 2026-08-01  
**Coverage definition:** `CE001_CATALOGUE_COVERAGE.md` (consumed; not amended)  
**Governance:** `EP001_GOVERNANCE.md`  
**Authority:** EF-001 · PB-002 PASS · CE-001 Measurement COMPLETE  

---

## 1. Honesty dual view

EP-001 reports two facts that must not be conflated:

| View | Meaning | Current headline |
|------|---------|------------------|
| **A — Approver credit (CE-001 Published)** | Volume ≥ `approved` by human Publication Approver | **4 / 72 (5.6%)** — CS1-004 LOs 2.1.3–2.1.6 (HR-001 APPROVE + RO-001 LIVE) |
| **B — Live loader inventory** | Packages under `educational_packages/cs1/` with `status: publication_approved` | **14 packages** (8 Campaign Alpha/Beta + 1 orphan + **5 Gamma**) |

**Publication honesty gap:** CS1-001 and CS1-002 Volume dossiers remain `publication_ready` (Approver unsigned), while eight Alpha/Beta packages and the EA-006 `4.2` grandfather already load as `publication_approved`. CS1-004 Gamma now holds Approver credit **and** LIVE package-path verification (RO-001; residual RO1-R1 on Finish/Home tomorrow chrome).

Orphan `4.2` remains **Missing\*** for catalogue coverage (no Campaign Gate CG membership) even when live-loaded.

---

## 2. Executive measurement

| Metric | Value | Notes |
|--------|------:|-------|
| Official topics | **14** | Sections 1–5 |
| Official LOs | **72** | Primary grain |
| **Published (Approver credit)** | **4 / 72 (5.6%)** | CS1-004 · 2.1.3–2.1.6 |
| Awaiting Approval (Gate CG PASS · Volume `publication_ready`) | **9 / 72 (12.5%)** | CS1-001 + CS1-002 Learning LOs (Approver unsigned) |
| Under Review | **0 / 72** | Wave 1 human seals complete |
| Live loader packages (`publication_approved`) | **14** | Alpha 4 + Beta 4 + EA-006 4.2 + **Gamma 5** |
| Missing (incl. Missing*) | **59 / 72** | Trust Front + remaining spine |
| Continuity Front (Approver / LIVE) | **Closed at 2.1.6** (package path); next open LO geography **2.2** | RO-001 |
| Trust Remediation Front | **4.1 → 4.2 → 5.1** | Orphan at 4.2 — Wave 2 not started |
| Pipeline (Under Review) | **0 LOs** | — |

---

## 3. Volume / Campaign inventory

| volume_id | Campaign | Gate CG | EO status | Approver credit | Live loader | Syllabus span (Learning) |
|-----------|----------|---------|-----------|-----------------|-------------|--------------------------|
| **CS1-001** | `CS1-EP001-CAMPAIGN-ALPHA` | PASS | `publication_ready` | Not Published | 4 packages live | 1.1 · 1.2.1 · 1.2.2 (+ Rev) |
| **CS1-002** | `CS1-CS1002-CAMPAIGN-BETA` | PASS | `publication_ready` | Not Published | 4 packages live | 1.2.3 · 2.1.1 · 2.1.2 (+ Rev) |
| — | EA-006 `4.2-glm-structure` | Campaign absent | Grandfather | **Not coverage** | 1 package live | 4.2 (orphan) |
| **CS1-004** | `CS1-EP001-CAMPAIGN-GAMMA` | PASS (HR-001) | `released` | **Published** (2.1.3–2.1.6) | **5 packages live** | 2.1.3–2.1.6 (+ Rev) — **Wave 1 LIVE** |
| **CS1-003** | Planned Wave 2 | — | Backlog — **not started** | — | — | 4.1 → 4.2 → 5.1 |

---

## 4. Topic-level map

| Topic | Title | LOs | Approver status | Live loader note |
|-------|-------|----:|-----------------|------------------|
| 1.1 | Purpose and function of data analysis | 4 | Awaiting Approval | Alpha packages live |
| 1.2 | Exploratory data analysis | 3 | Awaiting Approval | Alpha + Beta PCA live |
| 2.1 | Univariate distributions / generation | 6 | Partial (**2.1.3–2.1.6 Published**; 2.1.1–2.1.2 AA) | Beta + **Gamma LIVE** |
| 2.2 | Jointly distributed RVs | 4 | Missing | — |
| 2.3 | Expectations / conditional expectations | 2 | Missing | — |
| 2.4 | Generating functions | 2 | Missing | — |
| 2.5 | Central limit theorem | 2 | Missing | — |
| 2.6 | Random sampling / sampling distributions | 6 | Missing | — |
| 3.1 | Estimators and properties | 6 | Missing | — |
| 3.2 | Confidence and prediction intervals | 8 | Missing | — |
| 3.3 | Hypothesis testing and goodness of fit | 5 | Missing | — |
| 4.1 | Linear regression models | 5 | Missing | PB-002 withholds LO shell |
| 4.2 | Generalised linear models | 10 | Missing* | Orphan package live — not catalogue credit |
| 5.1 | Bayesian statistics | 9 | Missing | — |

---

## 5. LO-level map (Approver credit + live)

Statuses: **Published** (Approver) · **Awaiting Approval** · **Missing** · **Missing\*** (orphan).  
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
| 2.2.1–2.2.4 | Joint distributions family | Missing | No |
| 2.3.1–2.3.2 | Conditional expectation | Missing | No |
| 2.4.1–2.4.2 | MGF / CGF | Missing | No |
| 2.5.1–2.5.2 | CLT | Missing | No |
| 2.6.1–2.6.6 | Sampling distributions | Missing | No |
| 3.1.1–3.1.6 | Estimators | Missing | No |
| 3.2.1–3.2.8 | Intervals | Missing | No |
| 3.3.1–3.3.5 | Hypothesis testing | Missing | No |
| 4.1.1–4.1.5 | Linear regression | Missing | No (withhold) |
| 4.2.1–4.2.10 | GLM | Missing* | Yes (orphan only) |
| 5.1.1–5.1.9 | Bayesian | Missing | No |

---

## 6. Contiguity picture

```text
APPROVER CREDIT (Published):     2.1.3──2.1.4──2.1.5──2.1.6          4 LOs (CS1-004)
                                 [======== Wave 1 Gamma ========]

PIPELINE (Awaiting Approval) + LIVE LOADER (Alpha/Beta + Gamma):
  1.1.1──…──1.2.2──1.2.3──2.1.1──2.1.2──2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]
  [==== CS1-001 ====][==== CS1-002 ====][======== CS1-004 LIVE ========]
                                                                         │
                                                                         ▼ next open geography
                                                                      2.2 …

TRUST FRONT (parallel):
  4.1 (Missing) ── 4.2 (Missing* live orphan) ── 5.1 (Missing)
```

### Bridge residual (honesty)

| Link | Observed | Risk |
|------|----------|------|
| CA-R1 `tomorrow_preview.next_topic_code` | `2.1` | May skip 1.2.3 (PCA) after Alpha Revision — package metadata residual (PB-002 / CE-001) |
| CB-R1 → CG-D1 | Selection resolves CG-D1 after Beta complete (RO-001) | Finish/Home tomorrow chrome residual RO1-R1 (stale 2.1.2 text) |

---

## 7. Section roll-up (Approver credit)

| Section | LOs | Published | Awaiting Approval | Missing | Live orphan note |
|--------:|----:|----------:|------------------:|--------:|------------------|
| 1 | 7 | 0 | 7 | 0 | Alpha/Beta live |
| 2 | 22 | **4** | 2 | 16 | Gamma LIVE 2.1.3–2.1.6 |
| 3 | 19 | 0 | 0 | 19 | — |
| 4 | 15 | 0 | 0 | 15 (10× Missing*) | 4.2 orphan live |
| 5 | 9 | 0 | 0 | 9 | — |
| **Total** | **72** | **4** | **9** | **59** | — |

---

## 8. Map maintenance

1. Re-measure when Volume Approver signs (Awaiting Approval → Published).  
2. Re-measure when Wave packages certify / approve / go LIVE.  
3. Never move Missing* to Published without Campaign Gate CG + Approver.  
4. Update Continuity Front when Wave 1 closes 2.1.3–2.1.6.  
5. Keep LO universe pinned to CS1 2026 JSON.

---

## 9. Closing

Students may already encounter live Alpha/Beta package substance, but **certified catalogue dependence** under CE-001 remains **0% Published** until human Approver seals Volumes. EP-001 Wave 1 closes the Opening Continuity Front at 2.1.3 while reconciling that honesty gap.

**Companions:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` · `EP001_WAVE1_PLAN.md` · `CE001_CATALOGUE_COVERAGE.md`

Signed notionally: Editorial Director · EP-001 · Coverage Map · 2026-08-01
