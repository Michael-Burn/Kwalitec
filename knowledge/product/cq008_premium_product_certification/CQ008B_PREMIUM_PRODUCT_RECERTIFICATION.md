# CQ-008B — Premium Product Recertification

**Programme:** DX-006B · Premium Product Recertification  
**Certification ID:** CQ-008B  
**Status:** FINAL CERTIFICATION  
**Date:** 2026-07-29  
**Board stance:** Independent Premium Product Certification Board — not implementation review; not commit review.  
**Method:** Fresh product evaluation from repository state + RC-2026.07.29-03…06 evidence. Prior CQ-008 scores were not reused or anchored.

---

## Executive Summary

The product available today presents as **one authenticated Student application** and **one Founder Console**, plus a polished public Sign In face. The critical identity fracture that previously split Student Home from Choose Exam (legacy Learning Workspace chrome mid-journey) is **gone**: legacy workspace layouts are deleted; `layouts/base.html` and Session always extend the EOS Student shell; live RC-05 evidence shows `.student-shell` continuity through wizard → calibration → Study Session.

Student Home now reflects an active exam and mission after plan creation (RC-06 HTTP/DOM evidence: IFoA CM1 + Start Session). Founder Home / Subjects / Workspace remain calm, operational, and free of Student-shell leakage.

Residual issues are real but **not product-identity blockers**: navigation breadth, Founder Subjects ↔ Curriculum Studio overlap, ~5px Session horizontal overflow, Sign In outside Shared Foundation primitives, and Twin write lag mitigated by Study Plan fallback. Playwright PNG for RC-06 was unavailable in the agent environment; functional synchronisation is verified by Flask test-client + HTML capture.

**Overall Score:** **51 / 60** (**85%**)  
**Recommendation:** **COMMERCIAL READY WITH MINOR CONDITIONS**

---

## Strengths

1. **Student chrome is unified.** Home, Choose Exam (study-plan wizard), and Study Session share `student-topbar`, brand lockup, Appearance, Sign out, and footer (“Reduce decisions. Increase learning.”). RC-05: shell continuity Pass; no legacy sidebar observed.
2. **Legacy Learning Workspace retired.** `layouts/legacy_workspace.html`, `partials/sidebar.html`, and `partials/topnav.html` are absent from the tree; `base.html` unconditionally extends `eos_student.html`.
3. **Mission continuity after commitment.** RC-06 corrects empty “No exam selected…” projection when a Study Plan + mission exist; verified `after_mission_panel`, `after_has_exam_name`, refresh and re-login still non-empty.
4. **Founder OS bodies remain premium-calm.** One H1, one Primary, honest empty states on Home / Subjects / Curriculum Studio; Console chrome intact and isolated.
5. **Public Sign In is investor-credible.** Split brand hero, clear invite-only Alpha framing, Appearance + version footer (RC-02 / RC-05 logout shot).
6. **Runtime blocker cleared.** RC-04 traced the wizard HTTP 500 to a stale in-memory template path after legacy deletion; restarted process restored wizard → review → calibration → session with no 5xx in RC-05.
7. **Tone and composition law hold on migrated bodies.** No KPI theatre on certified Home surfaces; Design System macros drive Student Home and quiet wizard steps.

---

## Resolved Findings

Verified against today’s product — these prior certification failures are **not** treated as open.

| Prior issue | Resolution evidence |
|---|---|
| Student Home → Choose Exam shell fracture (EOS ↔ legacy workspace) | RC-03 unification; RC-05 `.student-shell=true` on Home + Session; wizard extends `layouts/base.html` → EOS; legacy templates deleted |
| Study Session as separate chrome family (`ds-session-shell`) | `session/base.html` extends `eos_student.html`; RC-05 Session shots share `student-topbar` |
| Wizard Step 2 HTTP 500 blocking journey | RC-04: stale Flask template graph; post-restart 200/302 through wizard; RC-05 full journey Pass |
| Student Home empty after successful plan + mission | RC-06: Study Plan exam identity + mission panel; `evidence.json` `pass: true`; HTML shows IFoA CM1 + Start Session |
| Auth drop / journey stop before Session | RC-05 reached `/missions/23/session`; refresh preserved auth; logout → Sign In clean |

**Note on RC-03 early screenshot `06_choose_exam.png`:** that capture shows legacy sidebar chrome and `has .student-shell: False`. It belongs to the **pre-restart / blocked** acceptance attempt. Current product law and RC-05 evidence supersede it. This board does **not** certify against that stale frame.

**Note on RC-03 Manual Walkthrough:** the manual template remains unchecked / pending. It is **not** used as positive or negative product evidence.

---

## Remaining Findings

### Critical

None verified in current evidence.

### High

None verified in current evidence.

### Medium

1. **Student primary navigation breadth.** EOS topbar exposes seven destinations (Home · Journey · Revision · History · Settings · Choose Exam · Help). Calm premium products usually keep shell attention narrower; density competes with “one next action” on Home.
2. **Founder catalogue dual entry.** Console sidebar lists both **Subjects** and **Curriculum Studio**. Workspace empty state Primary still reads **Create Subject** under a “Workspaces” section — naming/IA friction for a first Founder demo.
3. **Study Session horizontal overflow.** RC-05 instrumented `scrollWidth − clientWidth ≈ 5` at 1366 / 1100 / 900 / tablet. No hard clipping in screenshots; still a polish defect.
4. **CSS stack still dual-path.** EOS shell loads Bootstrap + `app.css` / `wizard.css` beside tokens and `design_system.css`. Bodies are largely Foundation; chrome/forms still carry legacy CSS gravity.

### Low

1. **Public Sign In outside Shared Foundation catalogue** (intentional RC-02 craft). Premium as a first impression; not the same primitive set as Student/Founder DS pages.
2. **Experience Twin not written on plan create.** Home fail-opens to Study Plan identity (correct behaviour); Twin can remain empty until a later sync programme (RC-06 known risk).
3. **Session entry path posture.** Under the RC-05 flag posture, session was entered via `/missions/<id>/session` rather than sole-runtime `/student/session/start`. Shell continuity held; path duality is residual architecture posture, not chrome fracture.
4. **Active-nav nuance.** RC-05 narrative noted Choose Exam visual emphasis after return-to-Session; machine `activeNav` on Session captures reported Home. Treat as low-confidence interaction polish, not shell failure.
5. **RC-06 Playwright PNG gap.** Functional sync verified; visual screenshot of post-plan Home not attached from the agent run (SIGSEGV). Local PNG re-run remains a documentation condition, not a product failure.
6. **Duplicate hidden inputs** in RC-06 HTML Start Session form (`mission_id` / `session_id` duplicated). Not observed as a runtime failure; form hygiene residual.

---

## Category Scores

### 1. Brand Identity — **9 / 10**

**Evidence**

- Consistent Kwalitec lockup on Student topbar, Console sidebar, and Sign In hero (RC-05 shots `01`–`06`, `08`).
- Colour system: navy shell / Console neutrals / primary blue CTAs; gold reserved largely for Alpha badges and logo accents on Sign In.
- Typography: single modern sans hierarchy; page H1 weight consistent across Student and Founder bodies.
- Spacing: generous whitespace on empty states and Session card; premium restraint.
- Role-appropriate chrome differences (Student dark topbar vs Console sidebar) read as one brand family, not two products — once Student mid-journey fracture is removed.

**Deduction:** Student Appearance cluster + seven nav labels crowd the brand bar; Session status “In Progress” uses a warm yellow pill adjacent to gold-reserved territory.

---

### 2. Design System — **8 / 10**

**Evidence**

- Student Home and quiet wizard use Design System macros / `ds-page` composition (`student/home.html`, `study_plan/wizard_base.html`).
- Founder empty states follow Reason + one Primary pattern (RC-05 `04`–`06`).
- Interaction language: primary solid blue vs ghost/outline secondaries; Session Finish clearly primary among Pause / Back.
- Responsive: tablet Session stacks and remains readable (`07_responsive.png`); overflow gate fails by ~5px.

**Deduction:** Bootstrap + legacy CSS still in the authenticated Student shell; Session body is coherent but not fully catalogue-pure; overflow residual.

---

### 3. Founder Experience — **8 / 10**

**Evidence**

- **Home:** Current Work empty → Create Subject; one H1; Console identity clear (`04_founder_home.png`).
- **Subjects:** No subjects yet → Create Subject (`05_founder_subjects.png`).
- **Workspace:** Curriculum Studio / Workspaces empty → Create Subject (`06_founder_workspace.png`).
- Navigation stable; `.student-shell` false on all three Founder captures; no Student chrome leak (RC-05 Founder regression Pass).

**Deduction:** Subjects vs Curriculum Studio dual destinations; Workspace CTA label mismatches section noun (“Workspaces” / “Create Subject”). Acceptance Founder account was empty-catalogue — operational publication depth not re-scored here (EV-001 is separate engineering authority).

---

### 4. Student Experience — **9 / 10**

**Evidence**

- Journey completed live: onboarding → wizard 1–3 → review → calibration → mission → Study Session (RC-05 journey log).
- Shell continuous; Session feels like continuation of Home (RC-05 certification Q1–Q2: YES).
- Choose Exam quiet path uses EOS via `wizard_base.html` → `layouts/base.html` → `eos_student.html` (repository verification).
- Post-plan Home shows exam + Start Session (RC-06 HTML + `evidence.json`); empty state reserved for genuine new learners.
- Refresh preserves auth; logout returns to Sign In with branding intact.

**Deduction:** Seven-item nav attention budget; ~5px Session overflow; Twin write lag (mitigated); session URL posture under flags.

---

### 5. Product Architecture — **9 / 10**

**Evidence**

- Authenticated Student shell model is singular (EOS). Legacy workspace path removed from disk and from `base.html`.
- Founder Console remains a separate intentional shell (correct SaaS admin/learner split).
- Information architecture: Student journey no longer crosses chrome families; Founder catalogue still has overlapping Subjects / Studio entries.
- State consistency: Home now binds Study Plan exam identity (shared helper with Profile); mission panel when startable.
- Navigation model: one Student nav tree rendered from `student/components/navigation.html`.

**Deduction:** `SOLE_RUNTIME` still governs home redirects (not shell); Twin not authoritative after plan create; Bootstrap remains in EOS head.

---

### 6. Product Quality — **8 / 10**

**Evidence**

- Polish: Sign In, Founder empties, Student empty and mission panels read finished and calm.
- Discoverability: one Primary on Home (Choose Exam or Start Session); Founder Create Subject always present when empty.
- Empty states: honest Reason + Next Action pattern held.
- Transitions: wizard progressed without 5xx after RC-04 restart; no console/network errors in RC-05 successful run.
- Confidence: a Founder can walk Student end-to-end without explaining a chrome reset.

**Deduction:** Overflow; nav density; Founder IA duplication; RC-06 visual PNG not in package; minor form-field duplication in captured HTML.

---

## Overall Score

| Category | Score |
|---|---:|
| Brand Identity | 9 |
| Design System | 8 |
| Founder Experience | 8 |
| Student Experience | 9 |
| Product Architecture | 9 |
| Product Quality | 8 |
| **Overall** | **51 / 60** |
| **Overall %** | **85%** |

---

## Commercial Readiness

**Estimate: 85%**

Suitable for Internal Alpha dogfood and structured Founder Validation demos. Not yet “ship to paying strangers without caveats”: navigation breadth, Founder catalogue IA, and Session overflow remain visible under scrutiny. Engineering publication depth and curriculum coverage remain outside this premium-coherence board’s pass/fail, but do not presently block a Founder demo of product identity.

---

## Founder Readiness

**Ready for Founder Validation — with minor conditions tracked.**

A Founder can demonstrate Sign In → Student journey → Session → return Home (with exam context) → Founder Console without the previous “two applications” embarrassment. Conditions below should be acknowledged, not hidden.

---

## Premium Readiness

**Mostly premium; minor craft residuals.**

Premium is judged as trust that the user is inside one finished product. On the Student path, that trust now holds. Founder Console is independently premium-calm. Cross-role chrome difference is acceptable. Remaining Medium items reduce “finished craft” slightly, not coherence.

---

## Recommendation

# COMMERCIAL READY WITH MINOR CONDITIONS

### Conditions (ranked)

| Rank | Condition |
|---|---|
| Medium | Narrow or stage Student primary nav toward a smaller attention budget for Validation demos |
| Medium | Resolve Founder Subjects vs Curriculum Studio as one catalogue story; align Workspace empty CTA naming |
| Medium | Fix Study Session ~5px horizontal overflow |
| Medium | Continue reducing Bootstrap/legacy CSS gravity inside EOS Student pages |
| Low | Attach local Playwright `student_home_after_plan.png` for RC-06 visual completeness |
| Low | Plan Twin write-on-plan-create (Home already fail-opens correctly) |
| Low | Clarify sole-runtime vs missions session-entry posture for Validation scripts |

No Critical or High conditions remain from verified current evidence.

---

## Final Questions

### 1. Does the application now present as a single, cohesive premium product?

**YES**

Within the Student authenticated journey, chrome and identity are continuous. Founder Console is a coherent second shell of the same brand (normal for premium SaaS). Public Sign In is on-brand. The prior mid-journey Student fracture is resolved.

### 2. Would a Founder confidently demonstrate this application to investors?

**YES**

With Internal Alpha framing disclosed, and with awareness of Medium polish/IA conditions. The demo no longer requires apologising for a chrome reset between Home and Choose Exam / Session.

### 3. Are the remaining issues cosmetic, functional, or architectural?

**Primarily cosmetic and information-architecture**, with **light architectural residuals** (Twin write lag; session-entry posture; Bootstrap still in shell). No verified functional journey blocker remains on the certified Student path after RC-04/05/06.

### 4. Estimate overall Commercial Readiness (%).

**85%**

### 5. Would you certify this product for Founder Validation?

**YES**

---

## Evidence Index

| Source | Path / artefact |
|---|---|
| RC-03 Student Shell Unification | `knowledge/engineering/rc20260729_03_student_shell_unification/RC20260729_03_STUDENT_SHELL_UNIFICATION_REPORT.md` |
| RC-03 Browser Acceptance (partial; stale Choose Exam frame superseded) | `…/RC20260729_03_BROWSER_ACCEPTANCE_REPORT.md` + `_evidence/browser_acceptance/` |
| RC-04 Runtime Investigation | `knowledge/engineering/rc20260729_04_runtime_failure/RC20260729_04_RUNTIME_FAILURE_REPORT.md` |
| RC-05 Browser Acceptance Final | `knowledge/engineering/rc20260729_05_browser_acceptance_final/RC20260729_05_BROWSER_ACCEPTANCE_FINAL.md` + `_evidence/browser_acceptance/evidence.json` + screenshots `01`–`08` |
| RC-06 Student Home State Sync | `knowledge/engineering/rc20260729_06_student_home_state_sync/RC20260729_06_STUDENT_HOME_STATE_SYNC_REPORT.md` + `evidence.json` + `student_home_after_plan.html` |
| Layout law (repo) | `app/templates/layouts/base.html`, `eos_student.html`, `session/base.html`; legacy workspace **deleted** |
| Wizard → EOS | `app/templates/study_plan/wizard_base.html` extends `layouts/base.html` |

---

## Board Statement

This recertification evaluates **the software that exists today**. It does not average prior CQ-008 scores, does not grade commits, and does not treat remediation effort as quality. On that basis the board finds the product **commercially ready for Founder Validation under minor conditions**, and **no longer blocked** by multi-shell Student identity failure.

---

*CQ-008B · DX-006B · Recommendation: COMMERCIAL READY WITH MINOR CONDITIONS · Overall 51/60 (85%)*
