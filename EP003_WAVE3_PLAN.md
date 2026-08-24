# EP-003 — Wave 3 Plan (CS1-005 Chapter 2 Continuity)

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Wave:** 3  
**Status:** Executable plan — Under Authoring → human review gate  
**Effective:** 2026-08-01  
**Authority:** `EP001_GOVERNANCE.md` · `EP001_PRODUCTION_ROADMAP.md` §6 · EF-001 · RO-002 PASS · PB-004 PASS · Wave 1 COMPLETE · Wave 2 COMPLETE  
**Namespace note:** User mission title “EP-003 Wave 3” is Wave 3 under **EP-001 Production Era** — not product/architecture EP-003 (`knowledge/product/ep003_*`). Artefacts use `EP003_*` / `CS1005_*` naming for this wave; governance remains EP-001.  
**Do not begin Wave 4 from this plan.**

---

## 0. EF-001 operational review (mandatory before intervention)

| Field | Entry |
|-------|-------|
| **1. Observation** | After Wave 1 LIVE (2.1.3–2.1.6) and Wave 2 LIVE (4.1–5.1), the next open Continuity Front Learning geography on the first-pass spine is **2.2** (jointly distributed RVs). Students finishing Gamma Revision meet Missing content at joint distributions. |
| **2. Classification** | **EC** — Educational Content (catalogue gap on Continuity Front) |
| **3. Severity** | **S1** — educationally blocking for contiguous first-pass dependence past 2.1 |
| **4. Evidence** | `EP001_COVERAGE_MAP.md` · `CE001_PRODUCTION_PRIORITY.md` Priority 3 · RO-002 / PB-004 PASS on independent Trust Front |
| **5. Smallest Effective Intervention** | Author Volume **CS1-005** Pilot Arc: Learning **2.2.1–2.2.4** + Revision; standard Author → … → Approver → LIVE → Verify pipeline; Alpha quality bar |
| **6. EF-001 Check** | **YES** — resolvable under frozen Educational Law (EA/EO/EJ/EW) without modifying the Educational Framework |

---

## 1. Wave 3 objectives

1. Produce Volume **CS1-005** covering contiguous Learning **2.2.1–2.2.4** + Revision memory.  
2. Bridge honestly from CS1-004 terminal (CG-R1 → first CS1-005 Learning day).  
3. Complete educational review and assemble certification evidence (per package — no batch-certify).  
4. Prepare Publication Approver dossier (human seal required).  
5. Deploy to LIVE **only after** human Approval.  
6. Verify LIVE delivery and targeted educational confidence for Continuity Front geography **2.2**.  
7. Update coverage maps (`EP003_COVERAGE_UPDATE.md` · `EP001_COVERAGE_MAP.md`).  
8. **Stop** at the human review gate in this cycle — await Tutor → Founder → Auditor → Publication Approver before LIVE.

---

## 2. Stage 0 — Commission brief (CS1-005)

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-005** |
| `volume_title` | Joint distributions entry — From marginals through dependence to linear combinations |
| `campaign_id` | `CS1-EP001-CAMPAIGN-EPSILON` |
| `scope_class` | `pilot_arc` |
| `subject_id` | CS1 |
| `curriculum` | IFoA CS1 2026 |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |
| `prior_volume_id` | CS1-004 (Campaign Gamma — Continuity Front successor) |
| `reference_bar` | CS1-001 / Alpha `ep001-1.0.0` |
| `owner_role` | Founder (Subject Lead unstaffed) |
| `educational_transformation` | From *univariate completion LIVE* → *2.2 lawfully entered and finished* → *honest bridge toward 2.3 (or declared stop)* under one Sensei |

### Membership intent (LO-per-day)

| Order | Working day | Mode | Focus LO | Working package_id |
|------:|-------------|------|----------|-------------------|
| 1 | CE-D1 | Learning | **2.2.1** | `CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL` |
| 2 | CE-D2 | Learning | **2.2.2** | `CS1-EP001-PKG-2.2-INDEPENDENCE` |
| 3 | CE-D3 | Learning | **2.2.3** | `CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION` |
| 4 | CE-D4 | Learning | **2.2.4** | `CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS` |
| 5 | CE-R1 | Revision | Return **2.2.1–2.2.4** (+ Gamma hinge as needed) | `CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS` |

**Commission scope decision:** Wave 3 closes topic **2.2** only (+ Revision). Topics **2.3+** remain Missing — Continuity Front advances to 2.3 after Wave 3 LIVE exit + approval. Do not extend commission into 2.3 to inflate coverage.

### Forbidden claims

- Full Chapter 2 / 2.3+ complete  
- First-pass spine PASS  
- Until-examination educational trust  
- Coverage mirage from drafts or catalogue-only status  
- Weakening Alpha / EA gates to accelerate LO %  

### LO descriptions (syllabus)

| LO | Description |
|----|-------------|
| 2.2.1 | Probability function or density function for marginal and conditional distributions of jointly distributed random variables |
| 2.2.2 | The conditions under which random variables are independent |
| 2.2.3 | Covariance, the correlation and the expected value of a function of two jointly distributed random variables |
| 2.2.4 | Mean and variance of linear combinations of random variables |

---

## 3. Workstream A — Continuity bridge (from Gamma)

| Item | Action |
|------|--------|
| Prior terminal | CS1-004 CG-R1 (`CS1-EP001-PKG-REV-DISTRIBUTIONS-GENERATION`) — LIVE Verified (RO-001) |
| Successor | CE-D1 (2.2.1) named as Continuity Front handoff |
| Preview honesty | CE-R1 / CE-D4 previews must not claim 2.3 complete; honest stop or named 2.3 successor |
| Wave 0 residual | Alpha/Beta Approver honesty gap remains open — Wave 3 does not clear it |
| Trust Front | CS1-003 remains independent LIVE inventory — do not conflate with Continuity Front credit |

---

## 4. Workstream B — Author CS1-005 packages

### B1. Artefact locations

| Kind | Path |
|------|------|
| Campaign catalogue | `app/curriculum/data/educational_campaigns/cs1/campaign-epsilon-cs1005/` |
| Campaign manifest | `.../campaign.json` |
| Package JSON | `.../packages/*.json` · `status: campaign_member_certified` |
| Live copies (post-Approver only) | `app/curriculum/data/educational_packages/cs1/` · `status: publication_approved` |
| Generator | `scripts/generate_cs1005_campaign.py` |
| Volume dossier | `CS1005_EDUCATIONAL_VOLUME.md` |
| EJ justifications | `CS1005_MISSION_JUSTIFICATIONS.md` |
| Certification | `CS1005_CERTIFICATION_REPORT.md` |
| Tutor / Founder / Readiness | `CS1005_TUTOR_REVIEW.md`, `CS1005_FOUNDER_REVIEW.md`, `CS1005_PUBLICATION_READINESS.md` |
| Wave artefacts | `EP003_WAVE3_PLAN.md` · `EP003_COVERAGE_UPDATE.md` |

### B2. Quality bar checklist (per package)

- [ ] EF-001 / Educational Excellence  
- [ ] CMP Partnership Q1–Q6  
- [ ] Educational Justification complete  
- [ ] Tutor Voice  
- [ ] Retrieval / revision coherence  
- [ ] Honest stop conditions  
- [ ] Natural `tomorrow_preview` to next mission  

### B3. Day educational intents

| Day | Intent |
|-----|--------|
| CE-D1 (2.2.1) | Marginal and conditional distributions from a joint — stop before independence as primary |
| CE-D2 (2.2.2) | Independence conditions — stop before covariance/correlation as primary |
| CE-D3 (2.2.3) | Covariance, correlation, E[g(X,Y)] — stop before linear-combination mean/variance as primary |
| CE-D4 (2.2.4) | Mean and variance of linear combinations — stop before 2.3 conditional expectation |
| CE-R1 | Retrieve 2.2.1–2.2.4 chain; protect Gamma hinge as needed; preview honest next (2.3 or declared stop) |

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
7. Auditor certification — **human PASS required**.  
8. Publication Readiness + Approver dossier — **human Approver required**.

Agent may assemble and perform desk self-checks. Signature lines remain:

```text
Approver name: __________________
Date: __________________
Decision: UNSIGNED — awaiting human
```

**Pipeline (unchanged):**  
Author → Tutor → Founder → Auditor → Publication Approver → LIVE Deploy → LIVE Verify → Confidence Verify.

---

## 6. Workstream D — LIVE deploy (post-Approver only)

1. Copy certified packages to `educational_packages/cs1/`.  
2. Set `status: publication_approved`.  
3. Ensure selection from CG-R1 into CE-D1…CE-R1 via `campaign_day` / `tomorrow_preview`.  
4. Do **not** deploy before Approver seal.  
5. Do **not** activate a single Epsilon day alone (FP-01).

---

## 7. Workstream E — Verification

| Check | Pass condition |
|-------|----------------|
| LIVE delivery | Session substance resolves CS1-005 packages |
| CMP partnership | Reading guidance CMP-partnered (Q1–Q6) |
| Continuity | CG-R1 → CE-D1 → … → CE-R1 without cliff |
| No fallback | No LO-shell Reading on 2.2.1–2.2.4 path |
| Coverage map | Updated after Approver + LIVE |
| Targeted confidence | Progressive claim on Wave 3 geography only — not until-exam |

---

## 8. Exit criteria (Wave 3 complete)

| # | Criterion |
|---|-----------|
| 1 | CS1-005 independently certified (desk + Campaign Gate CG evidence) |
| 2 | Human Publication gate sealed before LIVE claim |
| 3 | LIVE delivery verified for 2.2 path |
| 4 | Educational trust improved for joint-distributions Continuity Front |
| 5 | Coverage map updated |
| 6 | Wave 4 **not** started |

If human Approver has not yet sealed: Wave 3 may reach **Approver-ready** state; LIVE verification and Published credit remain blocked — report status honestly.

---

## 9. Execution status log

| Step | Status |
|------|--------|
| Stage 0 plan + EF-001 review | **Complete** — `EP003_WAVE3_PLAN.md` |
| B — Author packages | **Complete (catalogue)** — `campaign-epsilon-cs1005/` · 5 packages `campaign_member_certified` |
| C — Certification packs | **Complete (desk + human packs)** — `CS1005_*`; human Tutor/Founder/Auditor/Approver **UNSIGNED** |
| D — LIVE deploy | **Blocked** on human Approver — not copied to `educational_packages/` |
| E — Verification | **Blocked** on D |
| Wave 4 | **Forbidden** until Wave 3 LIVE exit + approval |
| Coverage update | `EP003_COVERAGE_UPDATE.md` · `EP001_COVERAGE_MAP.md` refreshed for Under Authoring |

---

## 10. Closing / stop instruction

Wave 3 opens the Continuity Front at **2.2** under Alpha quality after Wave 1/2 LIVE success — **without shortcuts**. This cycle **stops at the human review gate**.

```text
STOP — awaiting human Tutor → Founder → Auditor → Publication Approver.
Do not copy packages to educational_packages/.
Do not begin Wave 4.
Do not forge seals.
```

Signed notionally: Editorial Director · EP-001 / EP-003 Wave 3 Plan · 2026-08-01
