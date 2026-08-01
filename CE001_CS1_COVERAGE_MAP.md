# CE-001 — CS1 Coverage Map

**Programme:** Catalogue Expansion Programme CE-001  
**Subject:** IFoA CS1 · Syllabus 2026 (`app/curriculum/data/ifoa/cs1/2026.json`)  
**Measurement date:** 2026-08-01  
**Definition:** `CE001_CATALOGUE_COVERAGE.md`  
**Authority:** EA-001…EA-008 (Frozen) · EP-001 · EO-001 · PR-001 · COMMISSION-CS1-002 · DX-001  

---

## 1. Executive measurement

| Metric | Value | Notes |
|--------|------:|-------|
| Official topics | **14** | Sections 1–5 |
| Official learning objectives (LOs) | **72** | Primary coverage grain |
| **Published (counts toward coverage)** | **0 / 72 (0.0%)** | No Publication Approver signature on any Volume |
| Awaiting Approval | **9 / 72 (12.5%)** | CS1-001 + CS1-002 Gate CG PASS · `publication_ready` |
| Certified (not yet Approver-queued) | **0** | — |
| Under Review | **0** | — |
| Under Authoring | **0** | — |
| Missing | **63 / 72 (87.5%)** | Includes 10× `Missing*` at 4.2 |
| Topics fully Published | **0 / 14** | — |
| Topics fully Awaiting Approval | **2 / 14** | `1.1`, `1.2` |
| Topics partial (pipeline) | **1 / 14** | `2.1` (2 of 6 LOs in CS1-002) |
| Estimated study minutes — Published | **0** | — |
| Estimated study minutes — Awaiting Approval | **≈ 1,418 / 11,999 (11.8%)** | Curriculum minute estimates |

### Verdict

**Certified Catalogue Coverage for CS1 is objectively 0% Published.**  
Pipeline inventory of nine LOs (Campaign Alpha + Campaign Beta) sits at **Awaiting Approval**. That inventory is education-certified and DX-validated, but **does not yet count** under CE-001 coverage rules.

**Continuity Front (opening path):** `2.1.3` — Evaluation of probabilities and quantiles (named handoff from CS1-002 Revision).  
**Trust Remediation Front:** `4.1 → 4.2 → 5.1` (EA-006 orphan at 4.2; EA-007 FAIL).

---

## 2. Volume / Campaign inventory (operational)

| volume_id | Campaign | Gate CG | EO status | Map status | Syllabus span (Learning) | Student-reachable? |
|-----------|----------|---------|-----------|------------|--------------------------|-------------------|
| **CS1-001** | `CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0` | **PASS** (CI 8.75) | `publication_ready` | **Awaiting Approval** | 1.1 · 1.2.1 · 1.2.2 (+ Rev) | **No** |
| **CS1-002** | `CS1-CS1002-CAMPAIGN-BETA` · `cs1002-1.0.0` | **PASS** (CI 8.69) | `publication_ready` | **Awaiting Approval** | 1.2.3 · 2.1.1 · 2.1.2 (+ Rev) | **No** |
| — | EA-006 package `4.2-glm-structure` | **Campaign absent** | Package live grandfather | **Missing\*** | 4.2 (orphan) | Live path only — **not catalogue coverage** |
| CS1-003 | Mid-spine absorption (planned) | — | `backlog` | Under Authoring **not started** | Intent: 4.1→4.2→5.1 | — |
| CS1-004+ | Contiguous first-pass arcs (planned) | — | `backlog` | Missing / not commissioned | See Production Priority | — |

Evidence: `PR001_VOLUME_REGISTER.md` · `EP001_CAMPAIGN_CERTIFICATION.md` · `CS1002_CERTIFICATION_REPORT.md` · `CS1002_PUBLICATION_READINESS.md` · `EA006_PUBLICATION_REPORT.md`.

---

## 3. Topic-level Coverage Map

| Section | Topic | Title | LOs | Catalogue status | Volume / note |
|---------|-------|-------|----:|------------------|---------------|
| 1 | 1.1 | Describe the purpose and function of data analysis | 4 | **Awaiting Approval** | CS1-001 Alpha |
| 1 | 1.2 | Complete exploratory data analysis | 3 | **Awaiting Approval** | CS1-001 (1.2.1–1.2.2) + CS1-002 (1.2.3) |
| 2 | 2.1 | Basic univariate distributions / sample generation | 6 | **Partial** | 2.1.1–2.1.2 Awaiting Approval (CS1-002); **2.1.3–2.1.6 Missing** ← Continuity Front |
| 2 | 2.2 | Jointly distributed random variables | 4 | **Missing** | — |
| 2 | 2.3 | Expectations and conditional expectations | 2 | **Missing** | — |
| 2 | 2.4 | Generating functions | 2 | **Missing** | — |
| 2 | 2.5 | Central limit theorem | 2 | **Missing** | — |
| 2 | 2.6 | Random sampling and sampling distributions | 6 | **Missing** | — |
| 3 | 3.1 | Estimators and properties | 6 | **Missing** | — |
| 3 | 3.2 | Confidence and prediction intervals | 8 | **Missing** | — |
| 3 | 3.3 | Hypothesis testing and goodness of fit | 5 | **Missing** | — |
| 4 | 4.1 | Linear regression models | 5 | **Missing** | Required neighbour for 4.2 absorption |
| 4 | 4.2 | Generalised linear models | 10 | **Missing\*** | EA-006 grandfather package; Campaign not certified |
| 5 | 5.1 | Bayesian statistics | 9 | **Missing** | Required neighbour for 4.2 absorption |

---

## 4. LO-level Coverage Map

Statuses per `CE001_CATALOGUE_COVERAGE.md` §3.  
`Missing*` = orphan package evidence present; still **not** coverage.

| LO | Description (short) | Status | Evidence |
|----|---------------------|--------|----------|
| 1.1.1 | Aims of a data analysis | Awaiting Approval | CS1-001 / Alpha D1 |
| 1.1.2 | Stages and tools for data analysis | Awaiting Approval | CS1-001 / Alpha D1 |
| 1.1.3 | Sources of data / large data sets | Awaiting Approval | CS1-001 / Alpha D1 |
| 1.1.4 | Reproducible research | Awaiting Approval | CS1-001 / Alpha D1 |
| 1.2.1 | Summary statistics and EDA visualisations | Awaiting Approval | CS1-001 / Alpha D2 |
| 1.2.2 | Correlation measures (Pearson / Spearman / Kendall) | Awaiting Approval | CS1-001 / Alpha D3 |
| 1.2.3 | Principal component analysis | Awaiting Approval | CS1-002 / Beta D1 |
| 2.1.1 | Discrete distributions (geometric, binomial, …) | Awaiting Approval | CS1-002 / Beta D2 |
| 2.1.2 | Continuous distributions (normal, lognormal, …) | Awaiting Approval | CS1-002 / Beta D3 |
| 2.1.3 | Probabilities and quantiles for univariate distributions | **Missing** | Continuity Front — Beta terminal handoff |
| 2.1.4 | Poisson process / exponential connection | **Missing** | — |
| 2.1.5 | Generation of basic discrete and continuous RVs | **Missing** | — |
| 2.1.6 | Generation using inverse transform / other methods | **Missing** | — |
| 2.2.1 | Marginal / joint distributions | **Missing** | — |
| 2.2.2 | Independence conditions | **Missing** | — |
| 2.2.3 | Covariance, correlation, E[g(X,Y)] | **Missing** | — |
| 2.2.4 | Mean/variance of linear combinations | **Missing** | — |
| 2.3.1 | Conditional expectation | **Missing** | — |
| 2.3.2 | Mean/variance via conditioning | **Missing** | — |
| 2.4.1 | MGF / CGF | **Missing** | — |
| 2.4.2 | Moments via expansion / differentiation | **Missing** | — |
| 2.5.1 | Central limit theorem | **Missing** | — |
| 2.5.2 | Simulated sample comparison to CLT | **Missing** | — |
| 2.6.1 | Random samples from a population | **Missing** | — |
| 2.6.2 | Sampling distribution of a statistic | **Missing** | — |
| 2.6.3 | Mean/variance of sample mean (and related) | **Missing** | — |
| 2.6.4 | Basic sampling distributions (mean / variance) | **Missing** | — |
| 2.6.5 | t-statistic distribution | **Missing** | — |
| 2.6.6 | F distribution for variance ratio | **Missing** | — |
| 3.1.1 | Method of moments | **Missing** | — |
| 3.1.2 | Maximum likelihood | **Missing** | — |
| 3.1.3 | Efficiency, bias, consistency, MSE | **Missing** | — |
| 3.1.4 | Estimator comparison via MSE | **Missing** | — |
| 3.1.5 | Asymptotic distribution of MLEs | **Missing** | — |
| 3.1.6 | Bootstrap for estimator properties | **Missing** | — |
| 3.2.1 | Confidence interval for a parameter | **Missing** | — |
| 3.2.2 | Prediction interval | **Missing** | — |
| 3.2.3 | CI using asymptotic methods | **Missing** | — |
| 3.2.4 | CI for normal mean / variance | **Missing** | — |
| 3.2.5 | CI for binomial / Poisson | **Missing** | — |
| 3.2.6 | Two-sample CIs | **Missing** | — |
| 3.2.7 | CI for difference of means | **Missing** | — |
| 3.2.8 | Bootstrap confidence intervals | **Missing** | — |
| 3.3.1 | Null / alternative hypotheses; test errors | **Missing** | — |
| 3.3.2 | Basic one- and two-sample tests | **Missing** | — |
| 3.3.3 | Permutation non-parametric tests | **Missing** | — |
| 3.3.4 | Chi-square goodness of fit | **Missing** | — |
| 3.3.5 | Contingency tables / chi-square association | **Missing** | — |
| 4.1.1 | Response and explanatory variables | **Missing** | CS1-003 neighbour |
| 4.1.2 | Simple regression model | **Missing** | CS1-003 neighbour |
| 4.1.3 | Least squares slope / intercept | **Missing** | CS1-003 neighbour |
| 4.1.4 | Fit linear regression with software | **Missing** | CS1-003 neighbour |
| 4.1.5 | Model-fit measures / variable selection | **Missing** | CS1-003 neighbour |
| 4.2.1 | Exponential family distributions | **Missing\*** | EA-006 orphan only |
| 4.2.2 | Mean, variance, variance function, scale | **Missing\*** | EA-006 orphan only |
| 4.2.3 | Link / canonical link | **Missing\*** | EA-006 orphan only |
| 4.2.4 | Variables, factors, interactions | **Missing\*** | EA-006 orphan only |
| 4.2.5 | Linear predictor | **Missing\*** | EA-006 orphan only |
| 4.2.6 | Deviance / scaled deviance | **Missing\*** | EA-006 orphan only |
| 4.2.7 | Model choice via deviance analysis | **Missing\*** | EA-006 orphan only |
| 4.2.8 | Pearson / deviance residuals | **Missing\*** | EA-006 orphan only |
| 4.2.9 | Acceptability tests for GLM | **Missing\*** | EA-006 orphan only |
| 4.2.10 | Fit GLM and interpret | **Missing\*** | EA-006 orphan only |
| 5.1.1 | Bayes’ theorem / conditional probabilities | **Missing** | CS1-003 neighbour |
| 5.1.2 | Prior / posterior / conjugate | **Missing** | CS1-003 neighbour |
| 5.1.3 | Posterior in simple cases | **Missing** | CS1-003 neighbour |
| 5.1.4 | Loss functions / Bayesian estimators | **Missing** | CS1-003 neighbour |
| 5.1.5 | Credible intervals | **Missing** | CS1-003 neighbour |
| 5.1.6 | Credibility premium formula | **Missing** | CS1-003 neighbour |
| 5.1.7 | Bayesian credibility | **Missing** | CS1-003 neighbour |
| 5.1.8 | Empirical Bayes credibility | **Missing** | CS1-003 neighbour |
| 5.1.9 | Bayesian vs empirical Bayes differences | **Missing** | CS1-003 neighbour |

---

## 5. Section roll-up

| Section | Title | LOs | Published | Awaiting Approval | Missing | LO coverage (Published) |
|--------:|-------|----:|----------:|------------------:|--------:|------------------------:|
| 1 | Data analysis | 7 | 0 | 7 | 0 | 0% |
| 2 | Random variables and distributions | 22 | 0 | 2 | 20 | 0% |
| 3 | Statistical inference | 19 | 0 | 0 | 19 | 0% |
| 4 | Regression theory and applications | 15 | 0 | 0 | 15 (10× Missing*) | 0% |
| 5 | Bayesian statistics | 9 | 0 | 0 | 9 | 0% |
| **Total** | | **72** | **0** | **9** | **63** | **0.0%** |

---

## 6. Contiguity picture (opening spine)

```text
PUBLISHED COVERAGE (counts):     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  0 LOs

PIPELINE (Awaiting Approval):
  1.1.1──1.1.2──1.1.3──1.1.4──1.2.1──1.2.2──1.2.3──2.1.1──2.1.2
  [======== CS1-001 Alpha ========][==== CS1-002 Beta ====]
                                                              │
                                                              ▼ Continuity Front
                                                           2.1.3 ── 2.1.4 ── 2.1.5 ── 2.1.6 ── 2.2 … ── 5.1
                                                           [==================== MISSING ====================]

TRUST REMEDIATION (parallel geography):
  4.1 (Missing) ── 4.2 (Missing* orphan) ── 5.1 (Missing)
```

DX-001 confirms delivery PASS across the eight Alpha+Beta days **inside** the pipeline inventory. Exam-horizon continuity remains **not certifiable** until the Front advances and Volumes are Approved/released.

---

## 7. Gap register (priority-relevant)

| ID | Gap | Severity for student continuity | Disposition |
|----|-----|----------------------------------|-------------|
| G-01 | Zero Published LOs (Approver pending on CS1-001 / CS1-002) | **Critical** — certified journey unreachable | Ops — see Production Priority P0 |
| G-02 | Opening Front open at **2.1.3** after Beta terminal | **Critical** — day-9 cliff if released without successor | Next contiguous Volume |
| G-03 | Topic 2.1 only 2/6 LOs in pipeline | High — chapter honesty | Same as G-02 |
| G-04 | Sections 2 (rest), 3, 4, 5 entirely Missing | High — exam-horizon gap | Series of contiguous Volumes |
| G-05 | 4.2 Missing* orphan excellence | High — trust / EA-007 | CS1-003 absorption Campaign |
| G-06 | No Under Authoring Volumes active | Medium — cadence risk | Commission next Volume |
| G-07 | Joint activation engineering absent | High for release (not coverage credit) | Engineering successor (outside CE-001) |

---

## 8. Map maintenance

1. Re-measure when Volume status changes (especially Approver signature → Published).  
2. Do not move Missing* to Published without Campaign Gate CG + Approver.  
3. Update Continuity Front when a successor Volume certifies the next contiguous LOs.  
4. Keep LO universe pinned to CS1 2026 JSON; syllabus edition changes require a new map edition.

---

## 9. Closing

CS1 currently offers a **nine-LO certified opening arc** that is **not yet Publication-approved**. Coverage that students may depend on is therefore **0%**. The Editorial task is not to prove quality again — Alpha and Beta already hold Gate CG PASS — but to approve what exists, then expand from `2.1.3` without abandoning mid-spine trust remediation.

**Companions:** `CE001_CATALOGUE_COVERAGE.md` · `CE001_PRODUCTION_PRIORITY.md` · `CE001_IMPLEMENTATION_REPORT.md`

Signed notionally: Editorial Director · CE-001 · CS1 Coverage Map · 2026-08-01
