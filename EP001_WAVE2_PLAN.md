# EP-001 — Wave 2 Plan (CS1-003 Trust Remediation)

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Wave:** 2  
**Status:** Executable plan — Under Authoring  
**Effective:** 2026-08-01  
**Authority:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` §5 · EF-001 · RO-001 / RO-001A / RO1-R1 / PB-003 PASS  
**Namespace note:** User mission title “EP-002 Wave 2” is Wave 2 under **EP-001 Production Era** — not architectural EP-002 (`knowledge/architecture/ep002_*`).  
**Do not begin Wave 3 from this plan.**

---

## 1. Wave 2 objectives

1. Produce Volume **CS1-003** covering contiguous Learning **4.1 → 4.2 → 5.1** + Revision memory.  
2. Absorb EA-006 grandfather `4.2` into Gate CG Campaign membership (clear Missing*).  
3. Complete educational review and assemble certification evidence (per package — no batch-certify).  
4. Prepare Publication Approver dossier (human seal required).  
5. Deploy to LIVE **only after** human Approval.  
6. Verify LIVE delivery and targeted educational confidence for Trust Front geography.  
7. Update `EP001_COVERAGE_MAP.md`.  
8. **Stop** and await approval before Wave 3.

---

## 2. Stage 0 — Commission brief (CS1-003)

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-003** |
| `volume_title` | Mid-spine absorption — From classical linear models through GLM into Bayesian foundations |
| `campaign_id` | `CS1-EP001-CAMPAIGN-DELTA` |
| `scope_class` | `pilot_arc` |
| `subject_id` | CS1 |
| `curriculum` | IFoA CS1 2026 |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |
| `prior_volume_id` | Independent Trust Front (EA-006 orphan absorbed; not Continuity Front successor of CS1-004) |
| `reference_bar` | CS1-001 / Alpha `ep001-1.0.0` |
| `owner_role` | Founder (Subject Lead unstaffed) |
| `educational_transformation` | From *orphan premium at 4.2* → *contiguous 4.1 → 4.2 → 5.1 journey* under one Sensei with Revision |

### Membership intent (LO-per-day)

| Order | Working day | Mode | Focus LO | Working package_id |
|------:|-------------|------|----------|-------------------|
| 1–5 | CD-D1…CD-D5 | Learning | **4.1.1–4.1.5** | `CS1-EP001-PKG-4.1-*` |
| 6 | CD-R1 | Revision | Return 4.1 | `CS1-EP001-PKG-REV-LINEAR-MODELS` |
| 7–16 | CD-D6…CD-D15 | Learning | **4.2.1–4.2.10** | `CS1-EP001-PKG-4.2-*` (D6–D8 absorb EA-006 structure) |
| 17 | CD-R2 | Revision | Return 4.1–4.2 | `CS1-EP001-PKG-REV-REGRESSION-GLM` |
| 18–26 | CD-D16…CD-D24 | Learning | **5.1.1–5.1.9** | `CS1-EP001-PKG-5.1-*` |
| 27 | CD-R3 | Revision | Return 4.1–5.1 | `CS1-EP001-PKG-REV-MIDSPINE` |

### Forbidden claims

- First-pass spine PASS from mid-arc alone  
- Isolated Golden Day republication of 4.2  
- Opening Continuity Front / Chapter 2 complete  
- Until-examination educational trust  
- Coverage mirage from drafts  

### LO descriptions (syllabus)

| LO | Description (short) |
|----|---------------------|
| 4.1.1 | Response and explanatory variables |
| 4.1.2 | Simple and multiple linear regression models |
| 4.1.3 | Least squares slope / intercept (simple LM) |
| 4.1.4 | Fit LM with software; inference; fit; prediction; residuals |
| 4.1.5 | Model-fit measures / variable selection |
| 4.2.1 | Exponential family (binomial, Poisson, exp, gamma, normal) |
| 4.2.2 | Mean, variance, variance function, scale |
| 4.2.3 | Link and canonical link |
| 4.2.4 | Variables, factors, interactions |
| 4.2.5 | Linear predictor form |
| 4.2.6 | Deviance / scaled deviance / parameter estimation |
| 4.2.7 | Model choice via analysis of deviance |
| 4.2.8 | Pearson and deviance residuals |
| 4.2.9 | Pearson χ² and likelihood-ratio tests |
| 4.2.10 | Fit GLM and interpret output |
| 5.1.1 | Bayes’ theorem / conditional probabilities |
| 5.1.2 | Prior / posterior / conjugate |
| 5.1.3 | Posterior in simple cases |
| 5.1.4 | Loss functions / Bayesian estimators |
| 5.1.5 | Credible intervals |
| 5.1.6 | Credibility premium formula |
| 5.1.7 | Bayesian credibility |
| 5.1.8 | Empirical Bayes credibility |
| 5.1.9 | Bayes vs Empirical Bayes differences |

---

## 3. Workstream A — Grandfather absorption (EA-006)

| Item | Action |
|------|--------|
| Live orphan | `educational_packages/cs1/4.2-glm-structure-ea006.json` (`CS1-EA005-PKG-4.2-GLM-STRUCTURE`) |
| Catalogue absorption | Rewrite structure excellence into CD-D6…CD-D8 (4.2.1–4.2.3) under Delta membership |
| FP-01 | Never republish 4.2 alone as commercial journey maturity |
| Post-Approver LIVE | Supersede orphan as student primary path; clear Missing* after Gate CG + Approver |
| EA-007 | Trust-break disposition: absorption Campaign, not spine re-audit claim |

---

## 4. Workstream B — Author CS1-003 packages

### B1. Artefact locations

| Kind | Path |
|------|------|
| Campaign catalogue | `app/curriculum/data/educational_campaigns/cs1/campaign-delta-cs1003/` |
| Campaign manifest | `.../campaign.json` |
| Package JSON | `.../packages/*.json` · `status: campaign_member_certified` |
| Live copies (post-Approver only) | `app/curriculum/data/educational_packages/cs1/` · `status: publication_approved` |
| Volume dossier | `CS1003_EDUCATIONAL_VOLUME.md` |
| EJ justifications | `CS1003_MISSION_JUSTIFICATIONS.md` |
| Certification | `CS1003_CERTIFICATION_REPORT.md` |
| Tutor / Founder / Readiness | `CS1003_TUTOR_REVIEW.md`, `CS1003_FOUNDER_REVIEW.md`, `CS1003_PUBLICATION_READINESS.md` |

### B2. Quality bar checklist (per package)

- [ ] EF-001 / Educational Excellence  
- [ ] CMP Partnership Q1–Q6  
- [ ] Educational Justification complete  
- [ ] Tutor Voice  
- [ ] Retrieval / revision coherence  
- [ ] Honest stop conditions  
- [ ] Natural `tomorrow_preview` to next mission  

---

## 5. Workstream C — Review and certification

For **each** package independently: Educational Review → desk MG/SS/LE/TP (+ RV) → defect log if FAIL.  
Then Campaign Gate CG → Tutor → Founder → Auditor → Publication Approver.

Signature lines remain:

```text
Approver name: __________________
Date: __________________
Decision: UNSIGNED — awaiting human
```

---

## 6. Workstream D — LIVE deploy (post-Approver only)

1. Copy certified packages to `educational_packages/cs1/`.  
2. Set `status: publication_approved`.  
3. Disposition EA-006 orphan (supersede; document).  
4. Do **not** deploy before Approver seal.

---

## 7. Workstream E — Verification

| Check | Pass condition |
|-------|----------------|
| LIVE delivery | Session substance resolves CS1-003 packages |
| CMP partnership | Reading guidance CMP-partnered (Q1–Q6) |
| Continuity | CD-D1 → … → CD-R3 without cliff inside Trust Front |
| No fallback | No LO-shell Reading on 4.1–5.1 path |
| Missing* cleared | 4.2 catalogue credit after Approver |
| Coverage map | Updated |
| Targeted confidence | PB-003-class progressive claim on Wave 2 geography only |

---

## 8. Exit criteria (Wave 2 complete)

| # | Criterion |
|---|-----------|
| 1 | CS1-003 independently certified (desk + Campaign Gate CG evidence) |
| 2 | Human Publication gate sealed before LIVE claim |
| 3 | LIVE delivery verified for 4.1–5.1 path |
| 4 | Missing* cleared for 4.2; orphan excellence anti-pattern ended |
| 5 | Coverage map updated |
| 6 | Wave 3 **not** started |

---

## 9. Execution status log

| Step | Status |
|------|--------|
| Stage 0 plan + Volume dossier | **Complete** — `EP001_WAVE2_PLAN.md` · `CS1003_EDUCATIONAL_VOLUME.md` |
| B — Author packages | **Complete (catalogue)** — `campaign-delta-cs1003/` · 27 packages `campaign_member_certified` |
| C — Certification packs | **Complete (desk + HR-002 human seals)** — `CS1003_*` · `HR002_*`; Publication **APPROVED** |
| D — LIVE deploy | **Authorised — not executed** (HR-002 stop after publication decision) |
| E — Verification | **Blocked** on D |
| Wave 3 | **Forbidden** until Wave 2 LIVE exit + approval |
| Execution report | `EP001_WAVE2_EXECUTION_REPORT.md` · human gate closed by HR-002 |

---

Signed notionally: Editorial Director · EP-001 · Wave 2 Plan · 2026-08-01
