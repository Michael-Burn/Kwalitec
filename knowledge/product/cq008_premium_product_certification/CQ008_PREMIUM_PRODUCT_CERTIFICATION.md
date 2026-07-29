# CQ-008 — Premium Product Certification

**Programme:** CQ-008 — Premium Product Certification  
**Release Candidate:** `RC-2026.07.29-02`  
**Design Freeze:** `v2.0.0-design-freeze`  
**Authorities:** Design Freeze · DX-001 … DX-006A · DX-004A/B/C · DX-005A/B/C · Foundation Gate · UI Guardian · DX-006B phase reports · RC Login Polish  
**Method:** Independent live product audit (Playwright Chromium 1366×768 + template/architecture review). No application code was modified.  
**Date:** 2026-07-29  
**Reviewer stance:** External premium UX certification — not an engineering completion report.

---

## Executive Summary

Kwalitec’s **migrated page bodies** largely behave like one design system: Shared Foundation macros, one H1, one Primary, calm empty states, and no KPI theatre on Founder Home, Subjects, Student Home, Choose Exam discovery, or Session structure.

The **product chrome does not**. Under the current runtime (`KWALITEC_V2_SOLE_RUNTIME` unset / false), Student Home renders in the EOS topbar shell while Choose Exam — the next step of the same journey — renders in the legacy Learning Workspace sidebar. Founder Console, Session, and Sign In each introduce further chrome families. The Guardian primary directive (“every interface must feel like it belongs to the same product”) is not met.

**Pass criteria:** Overall ≥95 and no section below 9.  
**Result:** **61 / 100** — certification **FAIL**.

**Recommendation:** **NOT READY** for Founder Validation as one coherent premium product.

---

## Architecture Review

### Verdict

Page composition law is largely honoured inside migrated `<article>` bodies. Product architecture at the shell boundary is not.

### Evidence

| Surface | Shared Foundation body | Shell | Live notes |
|---|---|---|---|
| Founder Home | Yes (`ds_current_work`, empty operational) | Console sidebar | 1 H1 · 1 Primary · `design_system.css` |
| Founder Subjects | Yes (catalogue / empty) | Console sidebar | 1 H1 · 1 Primary · empty “No subjects yet.” |
| Founder Workspace | Yes (stage / persistent context — code) | Console sidebar | Upload / pipeline widgets still page-local + Bootstrap progress |
| Student Home | Yes (mission / empty) | EOS topbar | 1 H1 · 1 Primary “Choose Exam” |
| Choose Exam | Yes (Ready / Soon / Continue) | **Legacy workspace sidebar** | Body migrated; chrome is pre–EOS |
| Study Session | Yes (`session_body` Practice First) | Dedicated `ds-session-shell` | Structure sound; live Session not reached in this walk |
| Sign In | **No** (PX-001 / Bootstrap) | Auth split + RC2 footer | Crafted, outside Design System |

### Findings

1. **Shell fragmentation (critical).** Five chrome families across the certification scope: Console · EOS Student · Legacy Workspace · Session · Auth. Choose Exam extends `layouts/base.html`, which selects `legacy_workspace.html` when `SOLE_RUNTIME` is false — observed live with nav labels Dashboard / Study Plan / Session / Analytics.
2. **Shared Design System only — partial.** Bodies import `design_system/macros.html` and load `design_system.css`. Shells still load Bootstrap + legacy CSS (`app.css`, `founder_dashboard.css`, `student.css`, `wizard.css`).
3. **No KPI / StatisticTile / ProgressRing theatre** on migrated bodies — architectural win vs pre–DX-006B product.
4. **Workspace residual.** Document upload / pipeline chrome remains outside the catalogue (`doc-upload-*`, Bootstrap `.progress`).
5. **Sign In intentionally legacy** relative to DX-006B, but CQ-008 includes Public Sign In in product scope — it does not share Foundation primitives.
6. **DX-006B programme exit still open** in `PHASE_TRACKER.md` (Phase 6 IN REVIEW; exit checklist incomplete). This audit judges the live product, not tracker paperwork — and the live product still shows unfinished unification.

### Score: **7 / 10**

---

## Interaction Review

### Strengths

- **One Primary / One H1** held on every live-migrated surface inspected.
- Empty states follow Reason + Next Action (Founder Home, Subjects, Student Home).
- Primary vs ghost/secondary separation is clear inside DS bodies.
- Typography and spacing inside DS pages follow token rhythm.

### Weaknesses

- **Navigation model flips mid–student journey** (topbar → dense legacy sidebar).
- **Terminology drift:** Student Home CTA “Choose Exam” lands on a shell that highlights **Study Plan**.
- Student EOS nav exposes **seven** primary items (Home, Journey, Revision, History, Settings, Choose Exam, Help) against DX-005 guidance to keep shell attention narrow.
- Founder sidebar lists both **Subjects** and **Curriculum Studio** — overlapping catalogue/ops mental models.
- Choose Exam quiet steps retain Bootstrap form controls beside DS primary strip.
- Continue on discovery can appear muted/disabled until selection — correct behaviour, but contrast is soft.

### Score: **7 / 10**

---

## Founder Journey Review

```text
Home → Subjects → Workspace
```

### Observed

| Step | Result |
|---|---|
| Home | Clear Current Work empty state; single Primary **Create Subject**; calm Console identity |
| Subjects | Catalogue empty state; single Primary **Create Subject**; no dead end |
| Workspace | Not entered in live walk (empty catalogue; create form opens via create mode, not inline on empty). Template architecture matches DX-004C stage model |

### Confirmations

- No conflicting in-page nav on Home / Subjects bodies.
- Hierarchy Current Work → Queue → Recent (when present) is correct.
- Operational clarity of the **surface design** is strong.

### Residual journey risks (product as shipped)

- Dual entry **Subjects** vs **Curriculum Studio** can dilute “where do I work?”
- Workspace upload chrome is the least Foundation-faithful Founder surface.
- Publication pipeline operability was verified separately in EV-001 (engineering), not re-litigated here; this certification judges premium coherence, not gate wiring.

### Score: **8 / 10**

---

## Student Journey Review

```text
Home → Choose Exam → Session
```

### Observed

| Step | Result |
|---|---|
| Home | Excellent orientation: Current Mission empty → **Choose Exam** |
| Choose Exam | Discovery body correct: Ready / Coming Soon honesty, one Continue Primary |
| Quiet commitment steps | Date/sitting path on **legacy shell**; Bootstrap fields; H1 “When is your exam?” |
| Session | Template Practice First structure certified in Phase 6 report; this walk lost auth after commitment POST (redirected to Sign In) — journey fragility noted |

### Natural transitions

**Fail.** Leaving Student Home for Choose Exam feels like entering a different application: different nav IA, different brand chrome density, different footer, Appearance controls relocating into the legacy top bar. Commitment and execution cannot feel continuous while chrome resets.

### Score: **6 / 10**

---

## Public Experience Review

### Sign In / Landing

- Split hero + card remains the public face (no separate marketing route).
- RC-2026.07.29-02 polish: desktop laptop viewports fit without vertical scroll (measured overflow **0** at 1366×768).
- Compact footer chrome: Appearance · Alpha identity · Version/Build RC2.
- Theme Light / Dark / System switches `data-theme`.
- One H1 (“Sign in”), labelled fields, Remember me, invite-only copy — clear authentication presentation.
- Tablet/mobile still scroll when stacked (expected).

### Gaps

- Outside Shared Foundation / Lucide catalogue (inline decorative SVGs; gold accent on feature icons).
- Appearance option hit targets remain below 44px ideal (known RC residual).

### Score: **9 / 10**

---

## Accessibility Review

| Check | Assessment |
|---|---|
| Heading hierarchy | Strong on migrated bodies (single H1; section H2s) |
| Keyboard / focus | Login focus order intact; Console skip link present |
| Colour contrast | Generally sound; muted/disabled Continue and soft primary states need watch |
| ARIA / landmarks | Login main/footer; DS regions on migrated pages |
| Touch targets | Primary CTAs ≥44px; Appearance chrome ~32px |
| Responsive | Login adapts; Choose Exam scrolls on laptop due to Coming Soon length |

Not a full WCAG audit lab — structural and live spot checks only.

### Score: **8 / 10**

---

## Performance Review

- Migrated bodies feel light: no dashboard KPI grids, no duplicate hero stacks.
- Login visual stability on desktop is excellent (viewport-fit).
- No duplicate Primary rendering observed on inspected surfaces.
- Choose Exam page length introduces expected scroll; not a render thrash issue.
- Perceived responsiveness of static shell + DS CSS is adequate for alpha dogfood.

### Score: **9 / 10**

---

## Premium Experience Review

### What already feels premium

- Founder Home / Subjects empty states: Linear-like restraint, one decision, no theatre.
- Student Home mission emptiness: honest, quiet, actionable.
- Sign In: brand-forward, professional Internal Alpha tone, polished RC2 footer.
- Copy tone across DX bodies: calm, operational, non-gamified.

### What breaks premium coherence

- **Product identity fracture** between EOS Home and legacy Choose Exam.
- Multiple brand lockups and footer slogans (“What needs attention today?” vs “Reduce decisions…” vs version chrome).
- Incomplete shell migration reads as unfinished craft, not intentional variety.
- Session / Quick Check dual-CTA risk remains a structural premium hazard when embed is live.

Premium is not the average of pretty screens. It is whether the user trusts they are inside one finished product. Today they are not.

### Score: **7 / 10**

---

## Strengths

1. DX-006B page bodies successfully retire KPI theatre and multi-primary chaos on core surfaces.
2. Shared Foundation macros are the real composition language for Founder OS and Student Home.
3. Empty states are operationally honest (Reason + Action).
4. Choose Exam discovery content model (Ready vs Coming Soon) is clear and trustworthy.
5. Public Sign In after RC-2026.07.29-02 is a strong first impression on laptop viewports.
6. Guardian rules G-1 / G-2 / G-6 are largely held inside migrated bodies.
7. Professional, non-cheerful tone matches Design Freeze intent.

---

## Weaknesses

1. **Student shell split** (EOS ↔ legacy workspace) — single largest coherence failure.
2. `SOLE_RUNTIME` still false in the audited environment; layout router still dual-path.
3. Sign In remains outside Shared Design System while included in certification scope.
4. Workspace upload / pipeline UI still legacy-coupled.
5. Choose Exam quiet steps still Bootstrap-flavoured.
6. Student and Founder navigation breadth / duplication dilute attention.
7. DX-006B programme exit incomplete; Phase 6 still provisional for independent certification.
8. Live commitment walk exhibited auth drop back to Sign In — journey reliability residual.

---

## Recommended Improvements

Improvements are limited to **closing certification gaps already in scope** — not new features.

1. **Unify Student chrome for Home → Choose Exam → Session** under one shell (enable sole runtime path or migrate Choose Exam quiet steps onto EOS + Foundation forms).
2. **Retire legacy workspace presentation** from the certified student path so Study Plan sidebar cannot appear mid-journey.
3. **Bring Sign In onto Shared Foundation primitives** (or formally waive Public from DS law with Design Freeze amendment — today CQ-008 includes it).
4. **Remap Workspace upload/pipeline chrome** to catalogue components; remove Bootstrap progress as primary feedback.
5. **Narrow student primary nav** to the DX-005 attention budget.
6. **Resolve Subjects vs Curriculum Studio** as one Founder catalogue story in chrome.
7. **Close DX-006B programme exit** with independent Phase 5/6 live certification after shell unification.
8. **Re-verify commitment POST** does not eject to login under normal CSRF/session conditions.

---

## Risk Register

| ID | Risk | Severity | Certification impact |
|---|---|---|---|
| R1 | Student journeys cross two shells | Critical | Caps Architecture, Interaction, Student Journey, Premium |
| R2 | Founder Validation judges “one product” and sees fracture immediately | Critical | Blocks READY |
| R3 | Workspace upload looks unfinished vs Home/Subjects | High | Caps Architecture / Premium |
| R4 | Session Quick Check peer Primary (when embed live) | High | G-1 / Premium |
| R5 | Auth drop during Choose Exam commitment | High | Student Journey reliability |
| R6 | Appearance / dense nav a11y targets | Medium | Accessibility |
| R7 | Programme exit paperwork lag vs live gaps | Medium | Governance signal; not root cause |
| R8 | Public Sign In DS divergence | Medium | Public / Architecture coherence |

---

## Certification Score

| Section | Dimension | Score |
|---|---|---:|
| A | Architectural Integrity | **7** |
| B | Interaction Consistency | **7** |
| C | Founder Journey | **8** |
| D | Student Journey | **6** |
| E | Public Experience | **9** |
| F | Accessibility | **8** |
| G | Performance | **9** |
| H | Premium Experience | **7** |
| | **Overall** | **61 / 100** |

### Pass criteria

| Rule | Required | Actual | Result |
|---|---|---|---|
| Overall | ≥ 95 | 61 | **FAIL** |
| No section below 9 | All ≥ 9 | A–D, F, H below 9 | **FAIL** |

---

## Founder Validation Readiness

| Use | Suitable now? | Note |
|---|---|---|
| Internal Alpha (design dogfood on Founder OS bodies) | Conditional | Founder Home/Subjects are coherent enough for chrome feedback |
| Founder testing as premium product | **No** | Shell fracture will dominate perception |
| Daily operational usage (Founder) | Conditional | Surfaces usable; Workspace craft incomplete |
| Real curriculum creation | Outside this cert’s design score | EV-001 engineering path exists; not a premium-coherence pass |
| Daily study | **No** | Home → Choose Exam identity break |

---

## Recommendation

# NOT READY

Kwalitec does **not** yet behave as one coherent premium product.

The Design System migration of page bodies is real and valuable. Product certification fails because the authenticated experience still reveals multiple products stitched together — most damagingly on the Student journey that Founder Validation must trust.

Re-run CQ-008 after Student shell unification (and Workspace upload Foundation remap). Do not treat DX-006B body scores alone as product certification.

---

## Evidence

| Artefact | Path |
|---|---|
| Live walk metrics | `knowledge/product/cq008_premium_product_certification/_evidence/live_certification.json` |
| Follow-up / deep walk | `_evidence/live_certification_followup.json`, `_evidence/live_certification_deep.json` |
| Screenshots | `_evidence/screenshots/` |
| Walk scripts | `_evidence/cq008_live_walk.py`, `_evidence/cq008_followup_walk.py` |
| Authorities consulted | `knowledge/design/UI_GUARDIAN.md`, `knowledge/design/dx006a_design_system/`, `knowledge/implementation/dx006b/`, `knowledge/engineering/rc20260729_02_login_experience_polish/LOGIN_EXPERIENCE_POLISH_COMPLETION_REPORT.md` |

---

*Release Candidate: RC-2026.07.29-02 · Certification status: FAIL · Recommendation: NOT READY*
