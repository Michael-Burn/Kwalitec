# EP-001 — Publication Dashboard (post RO-001)

**Programme:** EP-001 Wave 1 / HR-001 / RO-001 LIVE Release Operations  
**Subject:** IFoA CS1 · 2026  
**Measurement date:** 2026-08-03  
**Authority:** EF-001 · CE-001 coverage law · EP-001 Governance · PB-002 · HOLD-001 lifted  
**Companions:** `EP001_WAVE1_PUBLICATION_PACK.md` · `EP001_REVIEWER_CHECKLISTS.md` · `EP001_HUMAN_REVIEW_SUMMARY.md` · `EP001_PUBLICATION_DECISION_LOG.md` · `EP001_COVERAGE_MAP.md` · `RO001_DEPLOYMENT_REPORT.md` · `RO001_LIVE_VERIFICATION_REPORT.md` · `RO001_RELEASE_DECISION.md` · `RO001A_LIVE_EDUCATIONAL_VERIFICATION.md` · `RO001A_EDUCATIONAL_FIDELITY_REPORT.md` · `RO001A_RELEASE_CONFIRMATION.md`

---

## Hard honesty rule

| View | What it means | May claim educational credit? |
|------|---------------|-------------------------------|
| **Catalogue coverage** | Authored / certified / under review in campaign catalogue | **No** — not student-trusted LIVE path |
| **Approver credit** | Volume ≥ `approved` under CE-001 | Approver credit only — **not** student LIVE trust alone |
| **LIVE published coverage** | `publication_approved` in `educational_packages/` **and** LIVE verification complete | **Yes** — package path (RO-001); Finish/Home tomorrow chrome residual RO1-R1 |

**Student package-path educational trust for Wave 1 geography is authorised after RO-001.**  
Do **not** claim Finish/Home tomorrow_preview chrome honesty until RO1-R1 is closed.

---

## 1. Pipeline legend

| Stage | Meaning |
|-------|---------|
| **Authored** | Package JSON present in campaign catalogue |
| **Desk Certified** | Author desk MG/SS/LE/TP/(RV) self-check recorded |
| **Tutor / Founder / Auditor** | Human seals |
| **Approved** | Human Publication Approver signed Volume |
| **LIVE Verified** | Joint inventory live-loaded **and** delivery/CMP/continuity verification recorded |

---

## 2. Wave 1 (CS1-004) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.1-PROB-QUANTILES` | CG-D1 | 2.1.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.1-POISSON-PROCESS` | CG-D2 | 2.1.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.1-INVERSE-TRANSFORM` | CG-D3 | 2.1.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.1-SOFTWARE-GENERATION` | CG-D4 | 2.1.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION` | CG-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-gamma-cs1004/`  
**LIVE loader today:** Gamma packages **present** as `publication_approved` under `educational_packages/cs1/` (RO-001 tip `f1ff5dc5…`).  
**Residual:** RO1-R1 — Finish/Home tomorrow UI stale on shared `topic_code` multi-day (see `RO001_LIVE_VERIFICATION_REPORT.md`; **reconfirmed** `RO001A_EDUCATIONAL_FIDELITY_REPORT.md`).

---

## 3. Dual coverage board (must not conflate)

### 3.A Catalogue coverage (Wave 1 geography)

| LO | Catalogue status | Pipeline stage (headline) | Student LIVE credit? |
|----|------------------|---------------------------|----------------------|
| 2.1.3 | Present in CS1-004 catalogue | **LIVE Verified** (package path) | **Yes** (package path) |
| 2.1.4 | Present | same | **Yes** |
| 2.1.5 | Present | same | **Yes** |
| 2.1.6 | Present | same | **Yes** |
| CG-R1 return 2.1.1–2.1.6 | Present | same | **Yes** |

**Catalogue Continuity Front:** closed at 2.1.3–2.1.6 design.  
**Student Continuity Front (package path):** **closed** at LIVE Verified (RO-001).

### 3.B LIVE published coverage (Wave 1 geography)

| LO | LIVE `publication_approved`? | LIVE Verified? | Educational credit? |
|----|------------------------------|----------------|---------------------|
| 2.1.3 | **Yes** | **Yes** (package path) | **Yes** |
| 2.1.4 | **Yes** | **Yes** | **Yes** |
| 2.1.5 | **Yes** | **Yes** | **Yes** |
| 2.1.6 | **Yes** | **Yes** | **Yes** |

```text
CATALOGUE (Wave 1 authored / approved): 2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]
LIVE published (Wave 1):                2.1.3──2.1.4──2.1.5──2.1.6──[CG-R1]

Credit claim zone:                      ● Approved AND ● LIVE Verified (package path)
Chrome honesty:                         Finish/Home tomorrow residual RO1-R1 open
```

---

## 4. Stage counts (CS1-004)

| Stage | Count | Notes |
|-------|------:|-------|
| Authored | **5 / 5** | Four Learning + Revision |
| Desk Certified | **5 / 5** | Superseded by human Auditor PASS |
| Tutor PASS | **5 / 5** | HR-001 · 13:50 |
| Founder PASS | **1 Volume** | HR-001 · 14:05 |
| Auditor PASS | **5 packages + Gate CG** | HR-001 · 14:20 |
| Publication Approver APPROVE | **1 Volume** | HR-001 · 14:35 |
| Approved | **5 / 5** (Volume APPROVE) | Joint inventory |
| LIVE Verified | **5 / 5** | RO-001 package path; residual RO1-R1 |

**Wave 1 human publication gate:** **Met**.  
**Wave 1 LIVE exit:** **Met (package path)** — residual RO1-R1 registered.

---

## 5. Human seal board

| Role | Artefact | Decision | Educational credit unlocked? |
|------|----------|----------|------------------------------|
| Tutor | `CS1004_TUTOR_REVIEW.md` | **PASS** | No (voice gate only) |
| Founder | `CS1004_FOUNDER_REVIEW.md` | **PASS** | No |
| Auditor | `CS1004_CERTIFICATION_REPORT.md` | **PASS** | No |
| Publication Approver | `CS1004_PUBLICATION_READINESS.md` | **APPROVE** | Approver credit |
| LIVE Verifier (ops) | `RO001_LIVE_VERIFICATION_REPORT.md` | **PASS WITH RESIDUAL** | Package-path LIVE credit |
| LIVE Educational Verifier (RO-001A) | `RO001A_LIVE_EDUCATIONAL_VERIFICATION.md` | **PASS WITH RESIDUAL** | HR-001 fidelity confirmed; RO1-R1 open |

---

## 6. Context volumes (honesty)

| Volume | Catalogue / dossier | Approver credit | LIVE loader | LIVE Verified credit claimable? |
|--------|---------------------|-----------------|-------------|----------------------------------|
| CS1-001 Alpha | `publication_ready` | **Not Published** (UNSIGNED) | 4 packages live | **Honesty gap** |
| CS1-002 Beta | `publication_ready` | **Not Published** (UNSIGNED) | 4 packages live | Same honesty gap |
| EA-006 4.2 orphan | No Gate CG | **Not coverage** | 1 package live | **No** catalogue credit |
| CS1-004 Gamma | **APPROVED** (HR-001) | **Approver credit** | **5 packages live** | **Yes (package path)** · RO1-R1 residual |
| CS1-003 Delta | **APPROVED** (HR-002) | **Approver credit** (Volume ≥ approved) | **27 packages live** (orphan superseded) | **Yes (package path)** · RO2-R1 revision Q6 residual |
| CS1-005 Epsilon | **APPROVED** (HR-003) | **Approver credit** (Volume ≥ approved) | **5 packages live** | **Yes (package path)** · RO3-R1 revision Q6 residual |

---

## 7. Publication readiness verdict

| Criterion | Status |
|-----------|--------|
| Wave 1 human seals complete | **Met** — HR-001 |
| Wave 1 publication decision | **APPROVED** |
| Wave 1 LIVE Verified | **Met** (RO1-R1 closed) |
| Wave 2 human seals complete | **Met** — HR-002 |
| Wave 2 publication decision | **APPROVED** |
| Wave 2 educational packages unmodified in review | **Met** |
| Wave 2 joint LIVE deploy | **Executed (RO-002)** tip `b99b0a8f…` |
| Wave 2 LIVE Verified | **Met** (package path; residual RO2-R1) |
| Wave 3 human seals complete | **Met** — HR-003 |
| Wave 3 publication decision | **APPROVED** |
| Wave 3 educational packages unmodified in review | **Met** |
| Wave 3 joint LIVE deploy | **Executed (RO-003)** tip `efe18ad7…` |
| Wave 3 LIVE Verified | **Met** (package path; residual RO3-R1) |
| Wave 4 human seals complete | **Met** — HR-004 |
| Wave 4 publication decision | **APPROVED** |
| Wave 4 educational packages unmodified in review | **Met** |
| Wave 4 joint LIVE deploy | **Executed (RO-004)** tip `58096787…` |
| Wave 4 LIVE Verified | **Met** (package path; residual RO4-R1) |
| Wave 5 catalogue authored | **Met** — `campaign-eta-cs1007/` (3 packages) |
| Wave 5 human seals complete | **Met** — HR-005 |
| Wave 5 publication decision | **APPROVED** |
| Wave 5 educational packages unmodified in review | **Met** |
| Wave 5 joint LIVE deploy | **Executed (RO-005)** tip `40c487e54…` |
| Wave 5 LIVE Verified | **Met** (package path; residual RO5-R1) |
| Wave 6 catalogue authored | **Met** — `campaign-theta-cs1008/` (3 packages) |
| Wave 6 human seals complete | **Met** — HR-006 |
| Wave 6 publication decision | **APPROVED** |
| Wave 6 educational packages unmodified in review | **Met** |
| Wave 6 joint LIVE deploy | **Executed (RO-006)** tip `a931f236…` |
| Wave 6 LIVE Verified | **Met** (package path; residual RO6-R1) |
| Wave 7 catalogue authored | **Met** — `campaign-iota-cs1009/` (7 packages) |
| Wave 7 human seals complete | **Met** — HR-007 |
| Wave 7 publication decision | **APPROVED** |
| Wave 7 educational packages unmodified in review | **Met** |
| Wave 7 joint LIVE deploy | **Executed (RO-007)** tip `1c747f3…` |
| Wave 7 LIVE Verified | **Met** (package path; residual RO7-R1) |
| Wave 8 catalogue authored | **Met** — `campaign-kappa-cs1010/` (7 packages) |
| Wave 8 human seals complete | **Met** — HR-008 |
| Wave 8 publication decision | **APPROVED** |
| Wave 8 educational packages unmodified in review | **Met** |
| Wave 8 joint LIVE deploy | **Executed (RO-008)** tip `28a06b1…` |
| Wave 8 LIVE Verified | **Met** (package path; residual RO8-R1) |
| Wave 9 catalogue authored | **Met** — `campaign-lambda-cs1011/` (9 packages) |
| Wave 9 human seals complete | **Met** — HR-009 |
| Wave 9 publication decision | **APPROVED** |
| Wave 9 educational packages unmodified in review | **Met** |
| Wave 9 joint LIVE deploy | **Met** — RO-009 tip `5184675…` |
| Wave 9 LIVE Verified | **Met** — package path PASS WITH RESIDUAL (RO9-R1…R3) |
| Wave 9 | **LIVE-complete (RO-009 / PB-011)** · PB-011 **PASS** |
| Wave 10 catalogue authored | **Met** — `campaign-mu-cs1012/` (6 packages) |
| Wave 10 human seals complete | **Met** — HR-010 |
| Wave 10 publication decision | **APPROVED** |
| Wave 10 educational packages unmodified in review | **Met** |
| Wave 10 joint LIVE deploy | **Met** — RO-010 tip `c409ad2…` |
| Wave 10 LIVE Verified | **Met** — package path PASS WITH RESIDUAL (RO10-R1…R3) |
| Wave 10 | **LIVE-complete (RO-010 / PB-012)** · PB-012 **PASS** · Coverage **63 / 72** · Reliance through Topic **3.3** |
| Wave 11 catalogue authored | **Met** — `campaign-nu-cs1013/` (6 packages) |
| Wave 11 human seals complete | **Met** — HR-011 |
| Wave 11 publication decision | **APPROVED** |
| Wave 11 educational packages unmodified in review | **Met** |
| Wave 11 joint LIVE deploy | **Met** — RO-011 tip `a0d8df665fa…` · deploy `dep-d9nq43m1egvs738jn2c0` |
| Wave 11 LIVE Verified | **Met** — package path PASS WITH RESIDUAL (`RO011_LIVE_VERIFICATION_REPORT.md`) |
| Wave 11 | **LIVE-complete (RO-011 / PB-013)** · PB-013 **PASS** · Coverage **63 / 72 HELD** · Reliance through Topic **4.1** |
| Wave 12 catalogue authored | **Met** — `campaign-xi-cs1014/` (11 packages) |
| Wave 12 human seals complete | **Met** — HR-012 |
| Wave 12 publication decision | **APPROVED** |
| Wave 12 educational packages unmodified in review | **Met** |
| Wave 12 joint LIVE deploy | **Met** — RO-012 tip `a800c85…` · deploy `dep-d9o0dnu7bikc73cnt8o0` |
| Wave 12 LIVE Verified | **Met** — package path (`RO012_LIVE_VERIFICATION_REPORT.md`) |
| Wave 12 | **LIVE-complete (RO-012 / PB-014)** · PB-014 **PASS** · Coverage **63 / 72 HELD** · Reliance through Topic **4.2** |
| Wave 13 catalogue authored | **Met** — `campaign-omicron-cs1015/` (10 packages) |
| Wave 13 human seals complete | **Met** — HR-013 |
| Wave 13 publication decision | **APPROVED** |
| Wave 13 educational packages unmodified in review | **Met** |
| Wave 13 joint LIVE deploy | **Met** — RO-013 tip `8432f6a…` · deploy `dep-d9o9rdj7uimc738srkgg` |
| Wave 13 LIVE Verified | **Met** — package path (`RO013_LIVE_VERIFICATION_REPORT.md`) |
| Wave 13 | **LIVE-complete (RO-013 / PB-015)** · PB-015 **PASS** · Coverage **63 / 72 HELD** · Reliance through Topic **5.1** |
| Wave 14 catalogue authored | **Met** — `campaign-pi-cs1016/` (10 packages) |
| Wave 14 human seals complete | **Met** — HR-014 |
| Wave 14 publication decision | **APPROVED** |
| Wave 14 educational packages unmodified in review | **Met** |
| Wave 14 joint LIVE deploy | **Met** — RO-014 tip `4ff8c95…` · deploys `dep-d9oq45flk1mc739pad60` / `dep-d9oqhe0ae00c73b55i7g` |
| Wave 14 LIVE Verified | **Met** — package path (`RO014_LIVE_VERIFICATION_REPORT.md`) |
| Wave 14 | **LIVE-complete (RO-014 / PB-016)** · PB-016 **PASS** · Coverage **63 / 72 HELD** · Reliance through Topic **5.1 HELD** |
| Wave 15 catalogue authored | **Met** — `campaign-rho-cs1017/` (10 packages) |
| Wave 15 human seals complete | **Met** — HR-015 |
| Wave 15 publication decision | **APPROVED** |
| Wave 15 educational packages unmodified in review | **Met** |
| Wave 15 joint LIVE deploy | **Met** — RO-015 tip `272a095…` · deploy `dep-d9outfnqj5pc738dl8og` |
| Wave 15 LIVE Verified | **Met** — package path (`RO015_LIVE_VERIFICATION_REPORT.md`) |
| Wave 15 | **LIVE-complete (RO-015 / PB-017)** · PB-017 **PASS** · Coverage **72 / 72 Approver numerator** · Reliance through Topic **5.1 HELD** · Educational Content Freeze |

**Programme state:** Wave 1 LIVE Verified · RO1-R1 closed · **Wave 2 LIVE-complete (RO-002 / PB-004)** · **Wave 3 LIVE-complete (RO-003 / PB-005)** · **Wave 4 LIVE-complete (RO-004 / PB-006)** · **Wave 5 LIVE-complete (RO-005 / PB-007)** (CS1-007 / Eta · 2.4) · **Wave 6 LIVE-complete (RO-006 / PB-008)** (CS1-008 / Theta · 2.5) · **Wave 7 LIVE-complete (RO-007 / PB-009)** (CS1-009 / Iota · 2.6) · **Wave 8 LIVE-complete (RO-008 / PB-010)** (CS1-010 / Kappa · 3.1) · **Wave 9 LIVE-complete (RO-009 / PB-011)** (CS1-011 / Lambda · 3.2) · PB-011 PASS · **Wave 10 LIVE-complete (RO-010 / PB-012)** (CS1-012 / Mu · 3.3) · PB-012 PASS · **Wave 11 LIVE-complete (RO-011 / PB-013)** (CS1-013 / Nu · 4.1 CF-join) · PB-013 PASS · **Wave 12 LIVE-complete (RO-012 / PB-014)** (CS1-014 / Xi · 4.2 CF-join) · PB-014 **PASS** · **Wave 13 LIVE-complete (RO-013 / PB-015)** (CS1-015 / Omicron · 5.1 CF-join) · PB-015 **PASS** · **Wave 14 LIVE-complete (RO-014 / PB-016)** (CS1-016 / Pi Memory Front) · PB-016 **PASS** · **Wave 15 LIVE-complete (RO-015 / PB-017)** (CS1-017 / Rho Publication Front) · Coverage **72 / 72 Approver numerator** · PB-017 **PASS** · Educational Content Freeze · **PX-007 Premium Experience Conditional PASS** · **P-002.1 Release Readiness NO-GO (G1 FAIL; await Founder review)** · Wave 16 not started · Version 1 production-ready **NOT DECLARED**.

### Continuity Front Register (dashboard)

| Front | Location | Status |
|-------|----------|--------|
| Student LIVE Continuity Front | Closed through Topic **5.1** / CO-R1 | RO-013 |
| Catalogue Continuity Front | **5.1 LIVE** (Omicron CF-join) | RO-013 |
| Memory Front (LIVE) | Pi **LIVE** (CP-D1…CP-R1) · package path | RO-014 |
| Publication Front (LIVE) | Rho **LIVE** (CR-D1…CR-R1) · package path | RO-015 |
| Next after LIVE | PB-017 **PASS** · Educational Content Freeze · PX-003…PX-006 complete · **PX-007 Premium Experience Conditional PASS** · **P-002.1 NO-GO** (await Founder review of release readiness) · Wave 16 not started · Version 1 production-ready **NOT DECLARED** | Continuity Front law |

### Student Reliance Coverage Register (dashboard)

| Metric | Value |
|--------|-------|
| Certified Educational Coverage (%) | **100% Approver numerator** (72 / 72) — **HELD** |
| Continuity Front | LIVE through Topic **5.1** / CO-R1 |
| Student Reliance Coverage | Contiguous CF through Topic **5.1** — **HELD**; Trust Front 24 LOs independent; Alpha/Beta honesty gap bodies unmodified; Omicron LIVE; Pi **LIVE**; Rho **LIVE Verified** + PB-017 **PASS** |
| Until-examination status | **NOT CLAIMED** |

---

## 8. Next actions

1. Keep Approver-credit Δ for 1.1.1–2.1.2 deferred until RO-015 LIVE Verified evidence.  
2. Track RO6-R1…RO14-R1 label desync + chrome / Q6 residuals as PI (and prior residuals).  
3. Wave 6–14 LIVE-complete — held.  
4. Wave 10 **LIVE-complete (RO-010 / PB-012)** — Coverage **63 / 72 (87.5%)** · Reliance through Topic **3.3** · PB-012 **PASS**.  
5. Wave 11 **LIVE-complete (RO-011 / PB-013)** — Nu CF-join Topic 4.1 · Coverage **63 / 72 HELD** · Reliance through Topic **4.1** · PB-013 **PASS**.  
6. Wave 12 **LIVE-complete (RO-012 / PB-014)** — Xi CF-join Topic 4.2 · Coverage **63 / 72 HELD** · Reliance through Topic **4.2** · PB-014 **PASS**.  
7. Wave 13 **LIVE-complete (RO-013 / PB-015)** — Omicron CF-join Topic 5.1 · Coverage **63 / 72 HELD** · Reliance through Topic **5.1** · PB-015 **PASS**.  
8. Wave 14 **LIVE-complete (RO-014 / PB-016)** — CS1-016 / Campaign Pi Memory Front · Coverage **63 / 72 HELD** · Reliance through Topic **5.1 HELD** · PB-016 **PASS** (mean 8.90/9).  
9. Wave 15 **LIVE-complete (RO-015 / PB-017)** — CS1-017 / Campaign Rho Publication Front · Coverage **72 / 72 Approver numerator** · Reliance through Topic **5.1 HELD** · PB-017 **PASS** (mean 9.00/9) · Educational Content Freeze.  
10. Successor programme: **PX-001…PX-006** complete · **PX-007** (WS-11 · WS-12) **Conditional PASS**.  
11. **P-002.1** Release Readiness Validation complete — recommendation **NO-GO** (G1 FAIL). Await Founder review of `P002_1_RELEASE_READINESS_REPORT.md` + `P002_1_RELEASE_RECOMMENDATION.md`.  
12. Do **not** declare Version 1 production-ready; do **not** start Wave 16 until Founder reviews P-002.1.  
13. Do **not** claim until-exam educational trust, first-pass spine PASS, “100% CS1” slogan, commercial readiness, or Version 1 production-ready.  
14. Keep Alpha/Beta package bodies unmodified.  
15. Published Coverage held at **72 / 72 Approver numerator**; Student Reliance through Topic **5.1**.  
16. Premium Experience claim posture: **Conditional PASS** with Board-owned residuals (`PX007_RESIDUAL_REGISTER.md` · `P002_1_RESIDUAL_REGISTER.md`).

## 9. Wave 2 (CS1-003) — pipeline summary

| Block | Days | Authored | Desk Certified | Tutor | Founder | Auditor | Approver | LIVE |
|-------|------|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------:|:----:|
| 4.1 + CD-R1 | CD-D1…CD-D5, CD-R1 | ● | ● | ● | ● | ● | ● | ● |
| 4.2 + CD-R2 | CD-D6…CD-D15, CD-R2 | ● | ● | ● | ● | ● | ● | ● |
| 5.1 + CD-R3 | CD-D16…CD-D24, CD-R3 | ● | ● | ● | ● | ● | ● | ● |

**Catalogue:** `app/curriculum/data/educational_campaigns/cs1/campaign-delta-cs1003/`  
**LIVE loader:** 27 Delta packages `publication_approved` · tip `b99b0a8f…`  
**Companions:** `EP001_WAVE2_PLAN.md` · `CS1003_*` · `HR002_*` · `RO002_*` · `PB004_*`

---

## 10. Wave 3 (CS1-005) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL` | CE-D1 | 2.2.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.2-INDEPENDENCE` | CE-D2 | 2.2.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION` | CE-D3 | 2.2.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS` | CE-D4 | 2.2.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS` | CE-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-epsilon-cs1005/`  
**LIVE loader:** 5 Epsilon packages `publication_approved` · tip `efe18ad7…`  
**Companions:** `EP003_WAVE3_PLAN.md` · `EP003_COVERAGE_UPDATE.md` · `CS1005_*` · `HR003_*` · `RO003_*` · `PB005_*`

---

Signed: Publication Dashboard · EP-001 · HR-001 · HR-002 · HR-003 · HR-004 · HR-005 · HR-006 · HR-007 · HR-008 · HR-009 · HR-010 · RO-001 · RO-002 · RO-003 · RO-004 · RO-005 · RO-006 · RO-007 · EP-006 · EP-007 · EP-008 · EP-009 · EP-010 · 2026-08-02  
**Publication decision (CS1-004):** APPROVED · LIVE Verified  
**Publication decision (CS1-003):** APPROVED · LIVE-complete (package path)  
**Publication decision (CS1-005):** **APPROVED** · LIVE-complete (package path)  
**Publication decision (CS1-006):** **APPROVED** · LIVE-complete (package path)  
**Publication decision (CS1-007):** **APPROVED** · LIVE-complete (package path)  
**Publication decision (CS1-008):** **APPROVED** · **LIVE-complete (RO-006 / PB-008)**  
**Publication decision (CS1-009):** **APPROVED** · **LIVE-complete (RO-007 / PB-009)**  
**Publication decision (CS1-010):** **APPROVED** · **LIVE-complete (RO-008 / PB-010)**  
**Publication decision (CS1-011):** **APPROVED** · **LIVE-complete (RO-009 / PB-011)** · Coverage **58 / 72 (80.6%)** · Reliance through Topic **3.2** · PB-011 **PASS**  
**Publication decision (CS1-012):** **APPROVED** · **LIVE-complete (RO-010 / PB-012)** · Coverage **63 / 72 (87.5%)** · Reliance through Topic **3.3** · PB-012 **PASS**  
**Publication decision (CS1-013):** **APPROVED** · **LIVE-complete (RO-011 / PB-013)** · Coverage **63 / 72 HELD** · Reliance through Topic **4.1** · PB-013 **PASS**  
**Publication decision (CS1-014):** **APPROVED** · **LIVE-complete (RO-012 / PB-014)** · Coverage **63 / 72 HELD** · Reliance through Topic **4.2** · PB-014 **PASS**
**RO-009:** LIVE-complete WITH RESIDUAL  
**PB-011:** PASS · mean 9.00/9  
**RO-010:** LIVE-complete WITH RESIDUAL  
**PB-012:** PASS · mean 9.00/9  
**RO-011:** LIVE-complete WITH RESIDUAL  
**PB-013:** PASS · mean 9.00/9  
**Wave 10:** LIVE-complete (RO-010 / PB-012) · Coverage **63 / 72** · Reliance through Topic **3.3** · PB-012 PASS  
**HR-011:** Complete (APPROVED)  
**Wave 11:** **LIVE-complete (RO-011 / PB-013)** · Coverage **63 / 72 HELD** · Reliance through Topic **4.1** · PB-013 PASS  
**HR-012:** Complete (APPROVED)  
**RO-012:** LIVE-complete WITH RESIDUAL  
**PB-014:** PASS · mean 9.00/9  
**Wave 12:** **LIVE-complete (RO-012 / PB-014)** · Coverage **63 / 72 HELD** · Reliance through Topic **4.2** · PB-014 PASS · Wave 13 **LIVE-complete (RO-013 / PB-015)** · PB-015 **PASS**
---

## 11. Wave 4 (CS1-006) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.3-CONDITIONAL-EXPECTATION` | CZ-D1 | 2.3.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.3-MEAN-VARIANCE-CONDITIONING` | CZ-D2 | 2.3.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-CONDITIONAL-EXPECTATIONS` | CZ-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-zeta-cs1006/`  
**LIVE loader:** 3 Zeta packages `publication_approved` · tip `58096787…`  
**Companions:** `EP004_WAVE4_PLAN.md` · `EP004_COVERAGE_UPDATE.md` · `HR004_*` · `RO004_*` · `PB006_*`  
**Residual:** RO4-R1 Home title collision during late Epsilon; RO4-R2/R3 CZ-R1 Q6/chrome.

---

## 12. Wave 5 (CS1-007) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.4-MGF-CGF` | CH-D1 | 2.4.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.4-MOMENT-VIA-GF` | CH-D2 | 2.4.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-GENERATING-FUNCTIONS` | CH-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-eta-cs1007/`  
**LIVE loader:** 3 Eta packages `publication_approved` · tip `40c487e54…`  
**Companions:** `EP005_WAVE5_PLAN.md` · `EP005_COVERAGE_UPDATE.md` · `HR005_*` · `RO005_*` · `PB007_*`  
**Residual:** RO5-R1 Home / label desync during late Zeta; RO5-R2/R3 CH-R1 Q6/chrome.

---

## 13. Wave 6 (CS1-008) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.5-CLT` | CT-D1 | 2.5.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL` | CT-D2 | 2.5.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM` | CT-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-theta-cs1008/`  
**LIVE loader:** **3** Theta packages `publication_approved` · tip `a931f236…` (RO-006)  
**Companions:** `EP006_WAVE6_PLAN.md` · `EP006_COVERAGE_UPDATE.md` · `HR006_*` · `RO006_*` · `PB008_*`  
**Stop:** Wave 6 **LIVE-complete** — Wave 7 LIVE-complete.

---

## 14. Wave 7 (CS1-009) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-2.6-RANDOM-SAMPLES` | CI-D1 | 2.6.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.6-SAMPLING-DISTRIBUTION-STATISTIC` | CI-D2 | 2.6.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.6-MEAN-VAR-SAMPLE` | CI-D3 | 2.6.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.6-NORMAL-SAMPLE-MEAN-VAR` | CI-D4 | 2.6.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.6-T-STATISTIC` | CI-D5 | 2.6.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-2.6-F-DISTRIBUTION` | CI-D6 | 2.6.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS` | CI-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-iota-cs1009/`  
**LIVE loader:** **7** Iota packages `publication_approved` · tip `1c747f3…` (RO-007)  
**Companions:** `EP007_WAVE7_PLAN.md` · `EP007_COVERAGE_UPDATE.md` · `CS1009_*` · `HR007_*` · `RO007_*` · `PB009_*`  
**Stop:** Wave 8 **LIVE-complete (RO-008 / PB-010)** — Coverage **50 / 72** · Reliance through **3.1.6** · PB-010 PASS · Wave 9 not started.

---

## 15. Wave 8 (CS1-010) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS` | CK-D1 | 3.1.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD` | CK-D2 | 3.1.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE` | CK-D3 | 3.1.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.1-COMPARISON-MSE` | CK-D4 | 3.1.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE` | CK-D5 | 3.1.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR` | CK-D6 | 3.1.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-ESTIMATORS` | CK-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-kappa-cs1010/`  
**LIVE loader:** **7** Kappa packages `publication_approved` · tip `28a06b1…` (RO-008)  
**Companions:** `EP008_WAVE8_PLAN.md` · `EP008_COVERAGE_UPDATE.md` · `CS1010_*` · `HR008_*` · `EP008_WAVE8_EXECUTION_REPORT.md` · `RO008_*` · `PB010_*`  
**Stop:** Wave 8 **LIVE Verified** · Coverage **50 / 72** · Reliance through **3.1.6** · PB-010 **PASS** · Wave 9 **LIVE-complete (RO-009)** · Coverage **58 / 72**.

---

## 16. Wave 9 (CS1-011) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER` | CL-D1 | 3.2.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-PREDICTION-INTERVAL` | CL-D2 | 3.2.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION` | CL-D3 | 3.2.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE` | CL-D4 | 3.2.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON` | CL-D5 | 3.2.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-CI-TWO-SAMPLE` | CL-D6 | 3.2.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-CI-PAIRED-MEANS` | CL-D7 | 3.2.7 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL` | CL-D8 | 3.2.8 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS` | CL-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-lambda-cs1011/`  
**LIVE loader:** **9** Lambda packages `publication_approved` · tip `5184675…` (RO-009)  
**Companions:** `EP009_WAVE9_PLAN.md` · `EP009_COVERAGE_UPDATE.md` · `CS1011_*` · `HR009_*` · `EP009_WAVE9_EXECUTION_REPORT.md` · `RO009_*` · `PB011_*`  
**Stop:** Wave 9 **LIVE Verified** · Coverage **58 / 72 (80.6%)** · Reliance through Topic **3.2** · PB-011 **PASS** · Wave 10 **LIVE-complete (RO-010)**.

---

## 17. Wave 10 (CS1-012) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS` | CM-D1 | 3.3.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.3-BASIC-TESTS` | CM-D2 | 3.3.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.3-PERMUTATION-TESTS` | CM-D3 | 3.3.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.3-CHI-SQUARE-GOF` | CM-D4 | 3.3.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE` | CM-D5 | 3.3.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-HYPOTHESIS-TESTING` | CM-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-mu-cs1012/`  
**LIVE loader:** **6** Mu packages `publication_approved` · tip `c409ad2…` (RO-010)  
**Companions:** `EP010_WAVE10_PLAN.md` · `EP010_COVERAGE_UPDATE.md` · `CS1012_*` · `HR010_*` · `EP010_WAVE10_EXECUTION_REPORT.md` · `RO010_*` · `PB012_*`  
**Stop:** Wave 10 **LIVE Verified** · Coverage **63 / 72 (87.5%)** · Reliance through Topic **3.3** · PB-012 **PASS**.

---

## 18. Wave 11 (CS1-013) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY` | CN-D1 | 4.1.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE` | CN-D2 | 4.1.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CN-4.1-LEAST-SQUARES` | CN-D3 | 4.1.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT` | CN-D4 | 4.1.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION` | CN-D5 | 4.1.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU` | CN-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-nu-cs1013/`  
**LIVE loader:** **6** Nu packages `publication_approved` · tip `a0d8df6…` (RO-011) · inventory **89** approved.  
**Companions:** `EP011_WAVE11_PLAN.md` · `EP011_COVERAGE_UPDATE.md` · `CS1013_*` · `HR011_*` · `EP011_WAVE11_EXECUTION_REPORT.md` · `RO011_*`  
**Stop:** Wave 11 **LIVE-complete (RO-011 / PB-013)** · Coverage **63 / 72 (87.5%) HELD** · Reliance through Topic **4.1** · PB-013 **PASS** · EP-012 **Under Authoring**.

---

## 19. Wave 12 (CS1-014) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY` | CX-D1 | 4.2.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-MEAN-VARIANCE` | CX-D2 | 4.2.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-LINK-CANONICAL` | CX-D3 | 4.2.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS` | CX-D4 | 4.2.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR` | CX-D5 | 4.2.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION` | CX-D6 | 4.2.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-MODEL-CHOICE` | CX-D7 | 4.2.7 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-RESIDUALS` | CX-D8 | 4.2.8 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS` | CX-D9 | 4.2.9 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CX-4.2-FIT-INTERPRET` | CX-D10 | 4.2.10 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-GLM-XI` | CX-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-xi-cs1014/`  
**Campaign status:** `released`  
**Package status:** catalogue `campaign_member_certified` · LIVE copies `publication_approved`  
**LIVE loader:** Xi packages **present** · inventory **110** approved (post RO-013).  
**Companions:** `EP012_WAVE12_PLAN.md` · `EP012_COVERAGE_UPDATE.md` · `CS1014_*` · `HR012_*` · `RO012_*` · `PB014_*`  
**Stop:** Wave 12 **LIVE-complete (RO-012 / PB-014)** · Coverage **63 / 72 (87.5%) HELD** · Reliance through Topic **4.2** · PB-014 **PASS** · Wave 13 **LIVE-complete (RO-013 / PB-015)** · Reliance through Topic **5.1** · PB-015 **PASS**.

---

## 20. Wave 13 (CS1-015) — package pipeline

| Package | Day | LO | Authored | Desk Certified | Tutor | Founder | Auditor | Publication Approver | Approved | LIVE Verified |
|---------|-----|----|:--------:|:--------------:|:-----:|:-------:|:-------:|:--------------------:|:--------:|:-------------:|
| `CS1-EP001-PKG-CO-5.1-BAYES-THEOREM` | CO-D1 | 5.1.1 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR` | CO-D2 | 5.1.2 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE` | CO-D3 | 5.1.3 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS` | CO-D4 | 5.1.4 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS` | CO-D5 | 5.1.5 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM` | CO-D6 | 5.1.6 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY` | CO-D7 | 5.1.7 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES` | CO-D8 | 5.1.8 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CO-5.1-BAYES-VS-EB` | CO-D9 | 5.1.9 | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-BAYESIAN-OMICRON` | CO-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-omicron-cs1015/`  
**Campaign status:** `released` (RO-013)  
**Package status:** catalogue `campaign_member_certified` · LIVE copies `publication_approved`  
**LIVE loader:** **10** Omicron packages `publication_approved` · tip `8432f6a…` (RO-013) · inventory **130** approved (post RO-015).  
**Companions:** `EP013_WAVE13_PLAN.md` · `EP013_COVERAGE_UPDATE.md` · `CS1015_*` · `EP013_WAVE13_EXECUTION_REPORT.md` · `HR013_*` · `RO013_*`  
**Stop:** Wave 13 **LIVE-complete (RO-013 / PB-015)** · Coverage **63 / 72 (87.5%) HELD** · Reliance through Topic **5.1** · RO-013 **PASS WITH RESIDUAL** · PB-015 **PASS**.

---

## 21. Wave 14 pipeline — CS1-016 / Campaign Pi (Memory Front)

| Package ID | Day | LO | Authored | Desk MG | Desk SS/LE | Desk TP/RV | Tutor | Founder | Auditor | Approver | LIVE |
|------------|-----|-----|:--------:|:-------:|:----------:|:----------:|:-----:|:-------:|:-------:|:--------:|:----:|
| `CS1-EP001-PKG-CP-2.1-PROB-QUANTILES` | CP-D1 | 2.1.3 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-2.2-MARGINAL-CONDITIONAL` | CP-D2 | 2.2.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-2.5-CLT` | CP-D3 | 2.5.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-2.6-RANDOM-SAMPLES` | CP-D4 | 2.6.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-3.1-ESTIMATORS` | CP-D5 | 3.1.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-3.2-CI-SAMPLE` | CP-D6 | 3.2.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-3.3-HYPOTHESIS-TESTING` | CP-D7 | 3.3.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-4.1-LINEAR-REGRESSION` | CP-D8 | 4.1.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CP-5.1-BAYES-THEOREM` | CP-D9 | 5.1.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-SPINE-MEMORY-PI` | CP-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-pi-cs1016/`  
**Campaign status:** `released` (RO-014)  
**Package status:** catalogue `campaign_member_certified` · LIVE copies `publication_approved`  
**LIVE loader:** **10** Pi packages `publication_approved` · tip `4ff8c95…` (RO-014) · inventory **130** approved (post RO-015).  
**Companions:** `EP014_WAVE14_PLAN.md` · `EP014_COVERAGE_UPDATE.md` · `CS1016_*` · `EP014_WAVE14_EXECUTION_REPORT.md` · `HR014_*` · `RO014_*`  
**Stop:** Wave 14 **LIVE-complete (RO-014 / PB-016)** · Coverage **63 / 72 (87.5%) HELD** · Reliance through Topic **5.1 HELD** · RO-014 **PASS WITH RESIDUAL** · PB-016 **PASS**.

---

## 22. Wave 15 pipeline — CS1-017 / Campaign Rho (Publication Front)

| Package ID | Day | LO | Authored | Desk MG | Desk SS/LE | Desk TP/RV | Tutor | Founder | Auditor | Approver | LIVE |
|------------|-----|-----|:--------:|:-------:|:----------:|:----------:|:-----:|:-------:|:-------:|:--------:|:----:|
| `CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS` | CR-D1 | 1.1.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.1-STAGES-TOOLS` | CR-D2 | 1.1.2 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.1-DATA-SOURCES` | CR-D3 | 1.1.3 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.1-REPRODUCIBLE` | CR-D4 | 1.1.4 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.2-EDA-SUMMARIES` | CR-D5 | 1.2.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.2-CORRELATION` | CR-D6 | 1.2.2 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-1.2-PCA` | CR-D7 | 1.2.3 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-2.1-DISCRETE` | CR-D8 | 2.1.1 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-CR-2.1-CONTINUOUS` | CR-D9 | 2.1.2 | ● | ● | ● | ● | ● | ● | ● | ● | ● |
| `CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO` | CR-R1 | Rev | ● | ● | ● | ● | ● | ● | ● | ● | ● |

**Key:** ● = complete · ○ = not reached  

**Catalogue root:** `app/curriculum/data/educational_campaigns/cs1/campaign-rho-cs1017/`  
**Campaign status:** `released` (RO-015)  
**Package status:** catalogue `campaign_member_certified` · LIVE copies `publication_approved`  
**LIVE loader:** **10** Rho packages `publication_approved` · tip `272a095…` (RO-015) · inventory **130** approved.  
**Companions:** `EP015_WAVE15_PLAN.md` · `EP015_COVERAGE_UPDATE.md` · `CS1017_*` · `EP015_WAVE15_EXECUTION_REPORT.md` · `HR015_*` · `RO015_*`  
**Stop:** Wave 15 **LIVE-complete (RO-015 / PB-017)** · Coverage **72 / 72 Approver numerator** · Reliance through Topic **5.1 HELD** · RO-015 **PASS WITH RESIDUAL** · PB-017 **PASS** (mean 9.00/9) · Educational Content Freeze · **PX-007 Premium Experience Conditional PASS** · **P-002.1 Release Readiness NO-GO** (G1 FAIL · G7 HOLD) — await Founder review of `P002_1_RELEASE_READINESS_REPORT.md` + `P002_1_RELEASE_RECOMMENDATION.md` · do **not** declare Version 1 released / Wave 16 · Version 1 production-ready **NOT DECLARED**.

Signed: Publication Dashboard · EP-001 · HR-001…HR-015 · RO-001…RO-015 · PB-011…PB-017 · EP-009…EP-015 · PX-003…PX-007 · P-002.1 · 2026-08-04
