# EP-001 — Wave 1 Plan (CS1-004 + Publication Honesty)

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Wave:** 1  
**Status:** Executable plan  
**Effective:** 2026-08-01  
**Authority:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` · EF-001 · PB-002 PASS  
**Do not begin Wave 2 from this plan.**

---

## 1. Wave 1 objectives

1. Reconcile publication honesty for CS1-001 / CS1-002 (Wave 0 ops).  
2. Produce Volume **CS1-004** covering Learning **2.1.3–2.1.6** + Revision.  
3. Complete educational review and assemble certification evidence (per package).  
4. Prepare Publication Approver dossier (human seal required).  
5. Deploy to LIVE **only after** human Approval.  
6. Verify LIVE delivery and targeted educational validation for the new geography.  
7. Update `EP001_COVERAGE_MAP.md`.  
8. **Stop** and await approval before Wave 2.

---

## 2. Stage 0 — Commission brief (CS1-004)

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-004** |
| `volume_title` | Univariate completion — From probability evaluation to generation |
| `campaign_id` | `CS1-EP001-CAMPAIGN-GAMMA` *(working ID)* |
| `scope_class` | `pilot_arc` |
| `subject_id` | CS1 |
| `curriculum` | IFoA CS1 2026 |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |
| `prior_volume_id` | CS1-002 |
| `reference_bar` | CS1-001 / Alpha `ep001-1.0.0` |
| `owner_role` | Founder (Subject Lead unstaffed) |
| `educational_transformation` | From *Beta distributional entry complete* → *2.1 lawfully finished* → *honest bridge toward 2.2 (or declared stop)* under one Sensei |

### Membership intent

| Order | Working day | Mode | Focus LO | Working package_id |
|------:|-------------|------|----------|-------------------|
| 1 | CG-D1 | Learning | **2.1.3** | `CS1-EP001-PKG-2.1-PROB-QUANTILES` |
| 2 | CG-D2 | Learning | **2.1.4** | `CS1-EP001-PKG-2.1-POISSON-PROCESS` |
| 3 | CG-D3 | Learning | **2.1.5** | `CS1-EP001-PKG-2.1-INVERSE-TRANSFORM` |
| 4 | CG-D4 | Learning | **2.1.6** | `CS1-EP001-PKG-2.1-SOFTWARE-GENERATION` |
| 5 | CG-R1 | Revision | Return 2.1.1–2.1.6 (+ Beta hinge as needed) | `CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION` |

### Forbidden claims

- Full Chapter 2 / 2.2+ complete  
- First-pass spine  
- 4.2 absorption / CS1-003 geography  
- Until-examination educational trust  
- Coverage mirage from drafts

### LO descriptions (syllabus)

| LO | Description |
|----|-------------|
| 2.1.3 | Evaluation of probabilities and quantiles associated with these distributions (calculation or statistical software as appropriate) |
| 2.1.4 | Poisson process and the connection between the Poisson process and the Poisson distribution |
| 2.1.5 | Generation of basic discrete and continuous RVs using the inverse transform method |
| 2.1.6 | Generation of discrete and continuous RVs using statistical software |

---

## 3. Workstream A — Publication honesty (Wave 0 ops)

### A1. Assemble Approver dossiers

Use existing readiness packs without inventing new educational substance:

| Volume | Readiness pack | Volume register |
|--------|----------------|-----------------|
| CS1-001 | `EP001_PUBLICATION_READINESS.md` | `PR001_VOLUME_REGISTER.md` |
| CS1-002 | `CS1002_PUBLICATION_READINESS.md` | `CS1002_EDUCATIONAL_VOLUME.md` |

Produce / update Approver worksheet fields: subject + version, artefact inventory, certification refs, gate results, claims allowed/forbidden, activation dependencies, **approver name/date = UNSIGNED — awaiting human**.

### A2. Live vs credit honesty record

Document in Wave 1 execution report:

- Eight Alpha/Beta packages already `publication_approved` in live loader.  
- Volumes remain `publication_ready` until human seal.  
- Orphan 4.2 live ≠ catalogue coverage.

### A3. After human seal (human action)

1. Advance Volume status to `approved` (then `released` when activation engineering completes).  
2. Update `EP001_COVERAGE_MAP.md` Approver credit (+9 LOs).  
3. Refresh CE-001 companion map if Board requires alignment.  

**Agent must not forge the seal.**

### A4. Bridge residuals in scope for Wave 1 wiring

| Item | Action in Wave 1 |
|------|------------------|
| CB-R1 → Continuity Front | Set CS1-004 CG-D1 as lawful successor; update CB-R1 `tomorrow_preview` to point at 2.1.3 package day / topic continuity line naming 2.1.3 |
| CA-R1 → 2.1 (skips PCA) | **Document** in honesty report; optional metadata fix only if it does not expand Wave 1 geography — prefer leave for ops note unless trivial |

---

## 4. Workstream B — Author CS1-004 packages

### B1. Artefact locations

| Kind | Path |
|------|------|
| Campaign catalogue | `app/curriculum/data/educational_campaigns/cs1/campaign-gamma-cs1004/` |
| Campaign manifest | `.../campaign.json` |
| Package JSON (catalogue) | `.../packages/*.json` with `status: campaign_member_certified` |
| Live copies (post-Approver only) | `app/curriculum/data/educational_packages/cs1/` with `status: publication_approved` |
| Volume dossier | `CS1004_EDUCATIONAL_VOLUME.md` |
| EJ justifications | `CS1004_JUSTIFICATION_*.md` or consolidated `CS1004_MISSION_JUSTIFICATIONS.md` |
| Certification report | `CS1004_CERTIFICATION_REPORT.md` |
| Tutor / Founder / Readiness | `CS1004_TUTOR_REVIEW.md`, `CS1004_FOUNDER_REVIEW.md`, `CS1004_PUBLICATION_READINESS.md` |

### B2. Package JSON shape (mirror Beta)

Each day must include: `package_id`, `status`, `campaign_id`, `campaign_day`, `volume_id`, `subject_id`, `topic_code` (`2.1`), `topic_focus_lo`, `mode`, `mission`, `session`, `reading_guidance`, `knowledge_checks`, `reflection`, `tomorrow_preview`, `certification_refs`, CMP edition pin.

### B3. Quality bar checklist (per package)

- [ ] EF-001 / Educational Excellence  
- [ ] CMP Partnership Q1–Q6  
- [ ] Educational Justification complete  
- [ ] Tutor Voice  
- [ ] Retrieval / revision coherence  
- [ ] Honest stop conditions (do not swallow next LO)  
- [ ] Natural `tomorrow_preview` to next mission  

### B4. Day educational intents (authoring brief)

| Day | Intent |
|-----|--------|
| CG-D1 (2.1.3) | Evaluate probabilities and quantiles for families already placed in Beta — calculation/software as appropriate; stop before Poisson process |
| CG-D2 (2.1.4) | Poisson process ↔ Poisson distribution connection; stop before inverse-transform generation |
| CG-D3 (2.1.5) | Inverse transform generation for basic discrete/continuous RVs; stop before software-generation LO as primary |
| CG-D4 (2.1.6) | Software generation of discrete/continuous RVs; stop before 2.2 joint distributions |
| CG-R1 | Retrieve 2.1.1–2.1.6 chain; protect Beta + Gamma memory; preview honest next (2.2 or declared stop) |

---

## 5. Workstream C — Review and certification (no batch-certify)

For **each** package independently:

1. Educational Review worksheet (ER-*).  
2. Desk certification: Gate MG, SS, LE, TP (RV for Revision).  
3. Defect/rework log if FAIL.  

Then Campaign-level:

4. Gate CG (continuity, bridges, revision strategy, CI).  
5. Tutor Review pack — **human PASS required**.  
6. Founder Review pack — **human PASS required**.  
7. Publication Readiness + Approver dossier — **human Approver required**.

Agent may assemble and perform desk self-checks. Signature lines remain:

```text
Approver name: __________________
Date: __________________
Decision: UNSIGNED — awaiting human
```

---

## 6. Workstream D — LIVE deploy (post-Approver only)

1. Copy certified packages to `educational_packages/cs1/`.  
2. Set `status: publication_approved`.  
3. Ensure `campaign_id` / `campaign_day` / `tomorrow_preview` support PB-002 selection from Beta into CG-D1…CG-R1.  
4. Update CB-R1 live package preview to land Continuity Front.  
5. Do **not** deploy CS1-004 live copies before Approver seal.

---

## 7. Workstream E — Verification

| Check | Pass condition |
|-------|----------------|
| LIVE delivery | Session substance resolves CS1-004 packages for authorised journey |
| CMP partnership | Reading guidance CMP-partnered (Q1–Q6) |
| Continuity | CB-R1 → CG-D1 → … → CG-R1 without cliff |
| No fallback | No LO-shell Reading on 2.1.3–2.1.6 path; PB-002 withhold still applies outside published span |
| Coverage map | `EP001_COVERAGE_MAP.md` reflects new statuses |
| Targeted validation | Focused educational validation on Wave 1 geography (not full until-exam PB) |

---

## 8. Exit criteria (Wave 1 complete)

Wave 1 completes only when **all** hold:

| # | Criterion |
|---|-----------|
| 1 | Educational content for CS1-004 independently certified (desk + Campaign Gate CG evidence assembled) |
| 2 | Human Publication gate dossier ready; LIVE claim only after human seal recorded |
| 3 | LIVE delivery verified for newly covered syllabus area (post-deploy) |
| 4 | Educational trust improved for 2.1.3–2.1.6 geography (Continuity Front closed) |
| 5 | Coverage map updated |
| 6 | Wave 2 **not** started |

If human Approver has not yet sealed: Wave 1 may reach **Approver-ready** state; LIVE verification and Published credit remain blocked — report status honestly.

---

## 9. Execution status log

| Step | Status |
|------|--------|
| Phase 1 roadmap docs | **Complete** — `EP001_GOVERNANCE.md`, `EP001_COVERAGE_MAP.md`, `EP001_PRODUCTION_ROADMAP.md`, `EP001_WAVE1_PLAN.md` |
| A — Honesty dossiers | **Complete (assembled)** — `EP001_WAVE1_HONESTY_RECONCILIATION.md`; Approver seals **UNSIGNED** |
| B — Author packages | **Complete (catalogue)** — `campaign-gamma-cs1004/` · 5 packages `campaign_member_certified` |
| C — Certification packs | **Complete (desk + human packs)** — `CS1004_*`; human Tutor/Founder/Auditor/Approver **UNSIGNED** |
| D — LIVE deploy | **Blocked** on human Approver — not copied to `educational_packages/` |
| E — Verification | **Blocked** on D |
| Wave 2 | **Forbidden** until Wave 1 LIVE exit + approval |
| Execution report | `EP001_WAVE1_EXECUTION_REPORT.md` |

---

## 10. Closing

Wave 1 closes the day-9 cliff at **2.1.3** under Alpha quality, reconciles Approver honesty for the opening arc, and stops. Exam-horizon coverage remains Waves 2–5.

Signed notionally: Editorial Director · EP-001 · Wave 1 Plan · 2026-08-01
