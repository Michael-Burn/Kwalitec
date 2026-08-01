# EP-001 — Publication Dashboard (post RO-001)

**Programme:** EP-001 Wave 1 / HR-001 / RO-001 LIVE Release Operations  
**Subject:** IFoA CS1 · 2026  
**Measurement date:** 2026-08-01  
**Authority:** EF-001 · CE-001 coverage law · EP-001 Governance · PB-002 · HOLD-001 lifted  
**Companions:** `EP001_WAVE1_PUBLICATION_PACK.md` · `EP001_REVIEWER_CHECKLISTS.md` · `EP001_HUMAN_REVIEW_SUMMARY.md` · `EP001_PUBLICATION_DECISION_LOG.md` · `EP001_COVERAGE_MAP.md` · `RO001_DEPLOYMENT_REPORT.md` · `RO001_LIVE_VERIFICATION_REPORT.md` · `RO001_RELEASE_DECISION.md`

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
**Residual:** RO1-R1 — Finish/Home tomorrow UI stale on shared `topic_code` multi-day (see `RO001_LIVE_VERIFICATION_REPORT.md`).

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

---

## 6. Context volumes (honesty)

| Volume | Catalogue / dossier | Approver credit | LIVE loader | LIVE Verified credit claimable? |
|--------|---------------------|-----------------|-------------|----------------------------------|
| CS1-001 Alpha | `publication_ready` | **Not Published** (UNSIGNED) | 4 packages live | **Honesty gap** |
| CS1-002 Beta | `publication_ready` | **Not Published** (UNSIGNED) | 4 packages live | Same honesty gap |
| EA-006 4.2 orphan | No Gate CG | **Not coverage** | 1 package live | **No** catalogue credit |
| CS1-004 Gamma | **APPROVED** (HR-001) | **Approver credit** | **5 packages live** | **Yes (package path)** · RO1-R1 residual |
| CS1-003 | Backlog | — | — | Wave 2 **not started** |

---

## 7. Publication readiness verdict

| Criterion | Status |
|-----------|--------|
| Human seals complete | **Met** — HR-001 |
| Publication decision | **APPROVED** |
| Educational packages unmodified in review | **Met** |
| Joint LIVE deploy | **Met** — RO-001 |
| LIVE Verified (package path) | **Met** |
| Finish/Home tomorrow chrome | **Residual RO1-R1** |
| Wave 2 not started | **Met** |

**Programme state:** **LIVE Verified (package path)** · residual RO1-R1 · **not Wave 2**.

---

## 8. Next actions

1. Founder acknowledge residual RO1-R1 (Finish/Home tomorrow UI).  
2. Optional SEI: bind Finish/Home tomorrow to sitting package `tomorrow_preview` (out of educational content scope).  
3. **Stop** — do not begin Wave 2 until residual disposition is recorded.

---

Signed: Publication Dashboard · EP-001 · HR-001 · RO-001 · 2026-08-01  
**Publication decision:** APPROVED  
**Credit claim (student LIVE package path):** Authorised for 2.1.3–2.1.6 + CG-R1  
**Wave 2:** Not started
