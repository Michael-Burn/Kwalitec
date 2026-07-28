# RP-001.2 — End-to-End Student Journey Certification

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.2 — End-to-End Student Journey Certification  
**Date:** 2026-07-28  
**Status:** Complete (documentation only)  
**Authority:** Code audit of auth → return-next-day student path under production Alpha flags (`render.yaml` + RP-001.1 inventory)  
**Companion artefacts:** `JOURNEY_TRANSITION_MATRIX.md`, `STUDENT_DECISION_POINTS.md`, `JOURNEY_RISK_REGISTER.md`

---

## Purpose

Certify that the complete Alpha student journey is coherent, intuitive, educationally consistent, and worthy of student trust.

**Educational principle audited:** The student should never wonder *"What am I supposed to do now?"* Every transition should lead naturally to the next educational step. Study Sensei should remain a consistent presence.

**Out of scope:** No new features, architecture changes, Twin/Recommendation Engine/curriculum/KSI modifications, flag activation, or service refactors.

---

## Production journey under audit

**Canonical Alpha path (flags as in production):**

```
Authentication
  → First Login (Alpha onboarding)
  → Study Plan Wizard (if no plan)
  → Calibration (Runtime A)
  → Student Home (+ welcome modal)
  → Daily Mission Intelligence (when recommendation exists)
  → Mission Commitment (start / defer)
  → Session Experience (overview → activity → reflection → summary → complete)
  → [Quick Check: NOT in default path — flags OFF]
  → Home return (day loop)
  → Decision Journal / Educational Timeline / History (archive)
  → Return the following day
```

**Default Alpha excludes:** Quick Check, Contextual Framing, Unified Journey, Experience Feedback, Runtime C enrolment, Twin cutover surfaces, push notifications.

---

## Overall Journey Certification

| Gate | Result |
|------|--------|
| First-time student can reach Home with a plan | **Pass** |
| Daily start → session → return Home is linear | **Pass** |
| Every transition documented | **Pass** |
| “What next?” clarity on canonical path | **Conditional Pass** |
| Study Sensei continuity across stages | **Conditional Pass** |
| Commitment / post-session reflection continuity | **Conditional Pass** (wiring gap) |
| Syllabus-complete → revision acknowledgement | **Fail** (UI unreachable under sole runtime) |
| Flag-gated journeys disclosed | **Pass** |
| Cohort validation executed | **Not done** (operational — JR-16 / R-16) |

**Overall RP-001.2:** **Conditional Pass**

A first-time student with a provisioned account **can** complete an entire study session without leaving the product, provided they have an active plan and an authorised recommendation. Several transitions introduce trust or continuity risks that must be disclosed and tracked; one lifecycle transition (revision acknowledgement) fails under the production sole-runtime posture.

---

## Stage assessments

### ST-01 — Authentication

| Field | Assessment |
|-------|------------|
| **Student Goal** | Sign in securely and reach the right next step for their account. |
| **Study Sensei Goal** | Establish trusted learner identity so plans, missions, and evidence belong to one student. |
| **Entry Conditions** | Direct `/auth/login`; or `@login_required` redirect with safe `?next=`. |
| **Exit Conditions** | Success → onboarding (first time), study-plan wizard (no plan), or canonical `/student/` (has plan). Failure → flash + stay on login. Logout → login. |
| **Explainability** | Why here: sign in. Why now: required gate. What next: product routes the student — login itself does not explain the educational journey (acceptable for auth). |
| **Trust Review** | Open redirects rejected. Invite-only note when Internal Alpha enabled. Invalid credentials flash is clear. Risk: founders diverted to Console (correct, not student path). |
| **Accessibility Review** | Labelled email/password; field errors `role="alert"`; redirect hint `role="status"`. Keyboard-usable form. Mobile: auth layout. |
| **Journey Risks** | JR-AUTH-01 credential confusion; operational admin-only provisioning. |
| **Certification** | **Pass** — secure, deterministic routing; no “what next?” trap on success. |

---

### ST-02 — First Login / Product Onboarding (ALPHA-001)

| Field | Assessment |
|-------|------------|
| **Student Goal** | Understand what Kwalitec is before configuring a plan or starting a mission. |
| **Study Sensei Goal** | Orient the learner to Study Sensei as a study companion (missions, explainability, reflection). |
| **Entry Conditions** | Post-login when `AlphaOnboardingService.should_show`; also gated from `student.home` GET. |
| **Exit Conditions** | Complete or skip POST → `canonical_home_url()` (then plan wizard or Home depending on plan). Help link available. |
| **Explainability** | Why here / why now: first-time orientation. What next: after complete/skip, product continues routing — skip may leave students under-oriented. |
| **Trust Review** | Dual chrome (V1 shell + EOS nav) can feel like two products (DEP-002). Copy uses “Kwalitec recommends…” more than branded “Study Sensei” — mild voice inconsistency. |
| **Accessibility Review** | V1 template; less EOS a11y coverage than Home. Keyboard forms OK. |
| **Journey Risks** | JR-02 dual chrome; skip without orientation. |
| **Certification** | **Conditional Pass** — educational purpose clear; dual chrome + skip residual. |

---

### ST-03 — Study Plan Wizard (Onboarding configuration)

| Field | Assessment |
|-------|------------|
| **Student Goal** | Declare exam, date, position, availability, and targets so Sensei can plan. |
| **Study Sensei Goal** | Collect deterministic planning inputs; curriculum-first syllabus binding. |
| **Entry Conditions** | Post-login / post-onboarding when no active plan (and no Runtime C enrolment). Also `/study-plan/` with no plan. |
| **Exit Conditions** | Linear steps 1→7→review; confirm → Calibration (Runtime A default). Error flashes keep student on step or rewind to step 1/2. |
| **Explainability** | Step titles explain *what* to enter; *why Sensei needs this* is weaker than Home MES. Review is the clarity peak. |
| **Trust Review** | Dual chrome. Unsupported exam flashes are honest. Abrupt if curriculum missing mid-flow. |
| **Accessibility Review** | Wizard forms labelled; V1 workspace chrome. Mobile usable but dense. |
| **Journey Risks** | JR-02 dual chrome; abandonment mid-wizard leaves incomplete onboarding. |
| **Certification** | **Conditional Pass** — coherent linear path; chrome and explainability conditions. |

---

### ST-04 — Calibration

| Field | Assessment |
|-------|------------|
| **Student Goal** | Declare what they already know so recommendations start fair. |
| **Study Sensei Goal** | Twin birth / declared mastery sync; avoid false cold-start. |
| **Entry Conditions** | After study-plan review confirm (`/calibration/after-plan/<id>`); resume via `/calibration/resume`. |
| **Exit Conditions** | Submit / beginner skip / persist-failure path → `/student/?welcome=1` (+ welcome eligibility). Abandon → home without Twin. Already-calibrated → home. |
| **Explainability** | Purpose is understandable; abandon path may leave “did I finish setup?” ambiguity. Persist-failure warning is honest. |
| **Trust Review** | Soft-fail on Twin persist with warning — good. Skip/abandon reduce Twin quality silently for later Tutor soft-fail. |
| **Accessibility Review** | Calibration alpha template; form labels present. |
| **Journey Risks** | JR-CAL-01 abandon without Twin; Tutor later soft-fails. |
| **Certification** | **Pass** — clear educational purpose; exits are defined. |

---

### ST-05 — Student Home (Today)

| Field | Assessment |
|-------|------------|
| **Student Goal** | Know what to study today and start (or defer) with confidence. |
| **Study Sensei Goal** | Single calm daily centre: what / why / how — one educational authority. |
| **Entry Conditions** | Canonical home under sole runtime; post-calibration; returning login; session finish; most sole-runtime redirects. |
| **Exit Conditions** | Primary CTA → session; defer → stay with deferred chrome; day_complete → “Return tomorrow”; empty recommendation → status copy + nav to Study Plan/Help. Welcome modal when eligible. |
| **Explainability** | When recommendation exists: Why / Why now / What next via MES + Mission Intelligence — **strong**. Empty Home: clear status but weak next action beyond browsing nav. |
| **Trust Review** | MES L1 + Mission Intelligence can feel duplicate (R-05). Non-interactive “guided reflection” preview spans adjacent to real controls risk confusion. Welcome CTA “Start Today's Session” returns to Home under sole runtime (extra click). |
| **Accessibility Review** | Skip link, `aria-current`, labelled hero/mission intelligence, empty `role="status"`, defer radios labelled, welcome dialog focus trap — **strongest surface**. |
| **Journey Risks** | JR-04 empty Home; JR-05 duplicate guidance; JR-PREVIEW fake controls. |
| **Certification** | **Conditional Pass** — canonical centre works when mission exists; empty/duplicate/preview residuals. |

---

### ST-06 — Daily Mission Intelligence

| Field | Assessment |
|-------|------------|
| **Student Goal** | Understand today’s mission focus and Sensei’s reasoning before committing. |
| **Study Sensei Goal** | Explainable mission presence; journal mirroring; Sensei voice on Home. |
| **Entry Conditions** | Embedded on Home when authorised recommendation / `has_mission`. Hidden during guided-session/reflection chrome. |
| **Exit Conditions** | Not a separate exit — feeds commitment CTA on same page. |
| **Explainability** | Focus question + Sensei copy support Why / Why now. Depends on recommendation existence. |
| **Trust Review** | Verbosity beside MES; empty “Study Sensei waits…” when no mission — honest but can feel idle. |
| **Accessibility Review** | `aside` + `aria-labelledby`. |
| **Journey Risks** | JR-05 duplication. |
| **Certification** | **Pass** (when visible) — **N/A as primary path stage** when no recommendation (covered under Home empty state). |

---

### ST-07 — Mission Commitment

| Field | Assessment |
|-------|------------|
| **Student Goal** | Explicitly accept today’s mission (or defer with a reason). |
| **Study Sensei Goal** | Record educational commitment arc: offered → committed → in_session → completed → reflected \| deferred. |
| **Entry Conditions** | Home when commit/defer affordances shown. |
| **Exit Conditions** | Start POST → `session.overview`. Defer POST → Home + flash. Ack reflection POST → Home. |
| **Explainability** | Commit path clear. Defer reasons labelled. Post-session Home reflection block may **not** appear after V2 session finish (see Trust). |
| **Trust Review** | **Critical continuity gap:** `RecommendationCommitmentService.mark_completed()` is called from legacy `app/mission/routes.py` only; V2 `session.finish` does not call it. Canonical Alpha path may skip completion → reflection chrome. Defer does not change ranking (expectation risk R-18). |
| **Accessibility Review** | Forms labelled; defer `<details>` + radios. |
| **Journey Risks** | **JR-01** commitment completion unwired on V2 session (High). |
| **Certification** | **Conditional Pass** — start/defer Pass; completion→reflection **Conditional** due to wiring gap. |

---

### ST-08 — Quick Check (conditional)

| Field | Assessment |
|-------|------------|
| **Student Goal** | Short adaptive check inside / beside mission (when enabled). |
| **Study Sensei Goal** | Calibrate understanding with framed assessment (ILE-001). |
| **Entry Conditions** | Flags `KWALITEC_ADAPTIVE_ASSESSMENT` + `KWALITEC_QUICK_CHECK` ON; embed on session overview/activity. |
| **Exit Conditions** | Completion → return to mission session surfaces. |
| **Explainability** | Strong when Contextual Framing ON; **absent from default Alpha** — must not be claimed. |
| **Trust Review** | Claiming QC in Alpha while OFF damages trust (R-03). Orphan `/assessment` is a separate path. |
| **Accessibility Review** | When ON: ILE-001A patterns, reduced-motion, keyboard JS. |
| **Journey Risks** | JR-03 flag honesty. |
| **Certification** | **Pass as excluded** from default Alpha journey. **Not Ready** as included Alpha stage until flags ON + re-certification. |

---

### ST-09 — Session Experience

| Field | Assessment |
|-------|------------|
| **Student Goal** | Complete today’s learning activities and leave with a clear wrap-up. |
| **Study Sensei Goal** | Deliver the committed mission as a linear educational session. |
| **Entry Conditions** | POST `student.start_session` or revision begin → `/session/<id>/…`. |
| **Exit Conditions** | overview → begin → activity loop → reflection → summary → complete → finish POST → `/student/`. Resume redirects if deep-linked mid-session. |
| **Explainability** | Surface sequence is clear; in-session reflection is educational continue, distinct from ILE-005 journal reflection. |
| **Trust Review** | Ownership 403/flash → Home. Port failures flash and stay. Durable store required for persistence. Gap: no commitment `mark_completed` on finish (JR-01). |
| **Accessibility Review** | Session primary CTAs; shared flash partial. Mobile session CSS. |
| **Journey Risks** | JR-01; JR-23 session orphaning (from inventory). |
| **Certification** | **Conditional Pass** — linear session **Pass**; post-session commitment continuity **Conditional**. |

---

### ST-10 — Reflection (multi-surface)

| Field | Assessment |
|-------|------------|
| **Student Goal** | Pause on what changed and what happens next. |
| **Study Sensei Goal** | Educational closure and (for ILE-005) calibration evidence — not engagement scoring. |
| **Entry Conditions** | (a) Session reflection surface mid-flow; (b) Home commitment reflection when `show_reflection`; (c) Decision Journal reflect when `can_reflect`; (d) optional Research check-in (product, not ILE-005). |
| **Exit Conditions** | Session → summary; Home ack → Home; Journal → stay with flash; Research → its own flow. |
| **Explainability** | Each surface explains itself locally. **Cross-journey:** no single student explanation of how reflections relate — risk of “another questionnaire?” |
| **Trust Review** | Home “guided reflection” preview spans are non-functional (“nothing is saved yet”) — confusing beside real session/journal reflection. Sensei review internal-only (correct, but invisible continuity). |
| **Accessibility Review** | Journal reflection uses fieldset/legend. Session reflection continue CTA clear. |
| **Journey Risks** | JR-REF-01 multiple reflection systems; JR-PREVIEW. |
| **Certification** | **Conditional Pass** — each path usable; continuity / multiplicity conditions. |

---

### ST-11 — Decision Journal

| Field | Assessment |
|-------|------------|
| **Student Goal** | See the audit trail of Sensei’s recommendations and their own choices. |
| **Study Sensei Goal** | Durable, explainable decision evidence (ILE-002). |
| **Entry Conditions** | History gateway links; direct `/student/decision-journal`. |
| **Exit Conditions** | Empty → CTA Home. Reflect POST → stay. Link to Educational Timeline. |
| **Explainability** | Arc (what/why/choice/afterwards) answers Why / What next well. Sparse early journal looks empty by design. |
| **Trust Review** | Not in JSON backup (R-08). Population depends on mission present / commitment wiring. |
| **Accessibility Review** | Timeline list `aria-label`; dl structure; reflection legends. |
| **Journey Risks** | JR-19 sparse early state; JR-01 may thin completion arcs. |
| **Certification** | **Pass** — coherent archive surface for Alpha. |

---

### ST-12 — Educational Timeline

| Field | Assessment |
|-------|------------|
| **Student Goal** | See recent educational momentum as a short narrative. |
| **Study Sensei Goal** | Compress journal into explainable beats (ILE-003). |
| **Entry Conditions** | From History / Journal; `/student/educational-timeline`. |
| **Exit Conditions** | Empty → CTA Journal. Section nav + back to Journal. |
| **Explainability** | Certainty label + beats; depends on journal population. |
| **Trust Review** | Empty early Alpha may feel “broken” (R-19). |
| **Accessibility Review** | `role="status"` certainty; labelled sections. |
| **Journey Risks** | JR-19. |
| **Certification** | **Pass** (with empty-state briefing). |

---

### ST-13 — History

| Field | Assessment |
|-------|------------|
| **Student Goal** | Review past sessions, commitment narrative, and archive gateways. |
| **Study Sensei Goal** | Continuity of learning evidence without competing analytics authority. |
| **Entry Conditions** | Nav History; `/analytics/` redirects here under sole runtime. |
| **Exit Conditions** | Links to Journal + Timeline; session cards; empty status. |
| **Explainability** | Clear as archive; charts from legacy analytics **not** ported — students expecting charts may wonder. |
| **Trust Review** | Analytics redirect honesty: History ≠ charts. |
| **Accessibility Review** | Stats `aria-label`; empty session status. |
| **Journey Risks** | Expectation mismatch vs legacy analytics. |
| **Certification** | **Conditional Pass** — archive Pass; analytics expectation condition. |

---

### ST-14 — Return the following day

| Field | Assessment |
|-------|------------|
| **Student Goal** | Resume study without re-doing setup; find today’s mission. |
| **Study Sensei Goal** | Fresh daily recommendation; preserve commitment/defer chrome; resume open sessions. |
| **Entry Conditions** | Login with active plan; onboarding already done. |
| **Exit Conditions** | Land on Home; start/resume or see day_complete / deferred states. **No push notifications** — return is student-initiated. |
| **Explainability** | Why here: daily centre. Why now: new day mission when available. What next: Start / Return tomorrow. |
| **Trust Review** | Profile may imply notifications that do not exist (R-07). Syllabus-complete revision ack never shown on EOS (JR-REV-01). |
| **Accessibility Review** | Same as Home. |
| **Journey Risks** | JR-REV-01; JR-07 notifications honesty; no re-engagement push. |
| **Certification** | **Conditional Pass** — daily loop Pass; revision lifecycle Fail subset; notification honesty condition. |

---

## Cross-Journey Review

| Dimension | Finding | Rating |
|-----------|---------|--------|
| **Terminology consistency** | Home/MES/Mission Intelligence mostly aligned; onboarding less “Sensei”-branded; Help/Research use product research language. Forbidden engineering terms guarded on EOS. | Conditional |
| **Navigation continuity** | Feature-mode nav (Home · Journey · Revision · History · Settings · Study Plan · Help) is stable under default flags. Dual chrome on wizard/settings/help breaks visual continuity. Unified Journey OFF avoids nav schema flip. | Conditional |
| **Educational continuity** | Curriculum → plan → calibration → daily mission is coherent. Post-session commitment reflection break weakens arc. | Conditional |
| **Sensei voice consistency** | Strongest on Home Mission Intelligence + MES. Weakest on auth, wizard steps, and internal-only Sensei review. | Conditional |
| **Decision continuity** | Journal mirrors present/defer when wired; completion arcs may miss V2 finish. | Conditional |
| **Mission continuity** | Start → session linear; finish → Home OK; commitment state machine incomplete on canonical finish. | Conditional |
| **Reflection continuity** | Three+ reflection concepts without student map. | Conditional |
| **History continuity** | History → Journal → Timeline gateway is clear. | Pass |
| **Timeline continuity** | Depends on Journal; empty early states OK if briefed. | Pass |
| **No duplicated educational authority** | Sole runtime removes legacy home competition **if** flag stays ON. MES + Mission Intelligence still dual-panel on Home. Runtime C / UJ must stay OFF. | Conditional |

---

## Conditional journeys (feature flags)

Documented in full in `JOURNEY_TRANSITION_MATRIX.md` § Conditional journeys.

| Flag set | Default Alpha | Journey effect if enabled |
|----------|---------------|---------------------------|
| Sole runtime + Student experience | **ON** | Canonical EOS path (audited) |
| Quick Check + Adaptive Assessment | **OFF** | Inserts assessment loop in session |
| Contextual Framing | **OFF** | Sensei framing inside Quick Check |
| Unified Journey | **OFF** | Nav schema + guided day chrome |
| Experience Feedback | **OFF** | Home “Your Journey” facts (needs UJ) |
| Runtime C enrolment | **OFF** | May skip calibration; alternate Home CTA |

**Certification rule:** Enabling any OFF journey above requires a delta certification — not covered by this Conditional Pass for the default path.

---

## Stage certification summary

| Stage | ID | Certification |
|-------|-----|---------------|
| Authentication | ST-01 | Pass |
| First Login / Onboarding | ST-02 | Conditional Pass |
| Study Plan Wizard | ST-03 | Conditional Pass |
| Calibration | ST-04 | Pass |
| Student Home | ST-05 | Conditional Pass |
| Daily Mission Intelligence | ST-06 | Pass (when present) |
| Mission Commitment | ST-07 | Conditional Pass |
| Quick Check | ST-08 | Pass as excluded |
| Session Experience | ST-09 | Conditional Pass |
| Reflection (multi) | ST-10 | Conditional Pass |
| Decision Journal | ST-11 | Pass |
| Educational Timeline | ST-12 | Pass |
| History | ST-13 | Conditional Pass |
| Return next day | ST-14 | Conditional Pass |

**Counts:** Pass 6 · Conditional Pass 8 · Fail (stage-level) 0 · Fail (named transition) 1 (revision acknowledgement under sole runtime) · Excluded Pass 1

---

## Answer to success criterion

> Can a first-time student complete an entire study session without confusion?

**Yes, with conditions.** On the production Alpha path — login → onboarding → plan → calibration → Home with recommendation → start session → finish → Home — the student has a continuous “what next” at each step **when** recommendation and session ports succeed. Confusion risks concentrate in: empty Home, dual chrome, non-interactive reflection preview, multiple reflection systems, missing post-session commitment reflection, and unreachable syllabus-complete acknowledgement.

---

## Evidence basis

- Routes: `app/auth/routes.py`, `app/alpha/routes.py`, `app/study_plan/routes.py`, `app/calibration/routes.py`, `app/presentation/student/routes.py`, `app/presentation/session/routes.py`, `app/mission/routes.py`, `app/dashboard/routes.py`
- Commitment: `app/application/student_experience/recommendation_commitment.py` (`mark_completed` callers)
- Lifecycle: `app/services/learning_lifecycle_service.py`; revision ack UI only in `dashboard/index.html`
- Flags / inventory: `FEATURE_FLAG_REGISTER.md`, `ALPHA_PRODUCT_INVENTORY.md`, `render.yaml`
- Templates: `student/home.html`, session templates, journal/timeline/history, onboarding, calibration, login

---

## Document control

| Item | Value |
|------|-------|
| Work package | RP-001.2 |
| Changes to application code | None |
| Educational reasoning changed | No |
| Next RP packages | Address journey risks; execute Internal Alpha validation pack |
