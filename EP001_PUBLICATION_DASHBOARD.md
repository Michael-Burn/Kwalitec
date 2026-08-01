# EP-001 — Publication Dashboard (post RO-001)

**Programme:** EP-001 Wave 1 / HR-001 / RO-001 LIVE Release Operations  
**Subject:** IFoA CS1 · 2026  
**Measurement date:** 2026-08-01  
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
| Wave 5 | **Not started** (unblocked) |

**Programme state:** Wave 1 LIVE Verified · RO1-R1 closed · **Wave 2 LIVE-complete (RO-002 / PB-004)** · **Wave 3 LIVE-complete (RO-003 / PB-005)** · **Wave 4 LIVE-complete (RO-004 / PB-006)** (CS1-006 / Zeta · 2.3) · Wave 5 unblocked · not started.

---

## 8. Next actions

1. Keep Wave 0 Alpha/Beta Approver honesty gap open (not waived).  
2. Track RO4-R1 Home title collision + CZ-R1 chrome / Q6 residual as PI (does not block Wave 5 start).  
3. **Do not begin Wave 5** until a separate authorised programme starts (LIVE exit met; start not automatic).  
4. Next Continuity Front geography after Wave 4 LIVE: **2.4**.

---

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

Signed: Publication Dashboard · EP-001 · HR-001 · HR-002 · HR-003 · HR-004 · RO-001 · RO-002 · RO-003 · RO-004 · 2026-08-01  
**Publication decision (CS1-004):** APPROVED · LIVE Verified  
**Publication decision (CS1-003):** APPROVED · LIVE-complete (package path)  
**Publication decision (CS1-005):** **APPROVED** · LIVE-complete (package path)  
**Publication decision (CS1-006):** **APPROVED** · LIVE-complete (package path)  
**Wave 5:** Not started (unblocked)

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
