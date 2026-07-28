# RP-001.1 — Alpha Product Inventory

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.1 — Product Inventory Certification  
**Date:** 2026-07-28  
**Status:** Certified inventory (documentation only)  
**Authority:** Student-facing surface audit against code, `render.yaml` production env, feature-flag resolvers, and ILE/EP completion reports  

---

## Purpose

This document is the definitive inventory of every student-facing capability in the Alpha candidate. It answers:

> What exactly is included in Alpha?

No features were implemented. No educational behaviour was changed. Maturity and release recommendations are evidence-based.

---

## Production posture (Alpha runtime)

| Control | Production (`render.yaml`) | Effect |
|---------|----------------------------|--------|
| `KWALITEC_V2_SOLE_RUNTIME` | `1` | Canonical home = Education OS `/student/`; legacy homes redirect |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | `1` | `/student/*` surfaces active |
| `KWALITEC_V2_DURABLE_STORE` | `1` | Experience/Session persistence |
| `KWALITEC_V2_INJECT_ENGINES` | `1` | Opaque engine bridges wired |
| `KWALITEC_V2_SEED_DEMO` | `0` | No demo learner seed |
| `KWALITEC_EI_INTERNAL_ALPHA` | `1` | EI orchestrator + recommendations ON; EI missions / explainability / progress remain OFF |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | `1` | Founder console only (not student) |
| All other student UX flags | unset → OFF | Quick Check, Unified Journey, Twin cutovers, Runtime C, etc. |

**Registration:** Not publicly exposed. Login and logout only (`app/auth/routes.py`).

**Internal Alpha cohort validation:** Pack exists (`knowledge/release/INTERNAL_ALPHA_RELEASE_VALIDATION.md`); execution not started.

---

## Inventory summary

| Category | Count |
|----------|------:|
| Capabilities reviewed | 32 |
| Ready for Alpha student use | 16 |
| Ready with Conditions | 11 |
| Not Ready (blocked / not activated / not implemented) | 5 |

See `CAPABILITY_MATRIX.md` for the compact readiness table and `RISK_REGISTER.md` for cross-cutting risks.

---

## Capability records

### CAP-01 — Authentication (Login / Logout)

| Field | Value |
|-------|-------|
| **Capability Name** | Authentication |
| **Owner Programme** | auth |
| **Current Version** | V1 production path |
| **Feature Flag** | None |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/auth/login`; POST `/auth/logout` |

**Educational Purpose.** Establishes a trusted learner identity so study plans, missions, and evidence belong to one student. Without authentication there is no personal learning continuity.

**Product Purpose.** Gate for all authenticated Study Sensei surfaces; post-login routing to onboarding, study-plan wizard, or canonical home.

**Dependencies.** Application: Flask-Login, User model. Infrastructure: session cookies, `SECRET_KEY`. External: none for login itself.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** No public registration (admin / bootstrap only). Open redirects rejected for `next`.

**Risks.** Educational: low. Trust: credential handling must remain secure. Technical: session fixation mitigated by Flask-Login patterns. Operational: admin bootstrap via env. Accessibility: standard form labels on login template.

**Testing Status.** Unit: auth forms/routes covered in suite. Integration: operational smoke requires login. Presentation: login templates. Accessibility: basic form. Regression: smoke. Certification: not separately certified beyond platform readiness.

**Release Recommendation.** **Ready** — required Alpha entry path; production-enabled; no flag gate.

---

### CAP-02 — Internal Alpha Onboarding

| Field | Value |
|-------|-------|
| **Capability Name** | Product Onboarding |
| **Owner Programme** | ALPHA-001 |
| **Current Version** | Implemented |
| **Feature Flag** | None |
| **Student Visible** | Yes (first-login gate) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/alpha/onboarding` (complete / skip POSTs) |

**Educational Purpose.** Orients the student to Study Sensei as a study companion before the first mission, reducing confusion about what the product is for.

**Product Purpose.** One-time product orientation; gates home until completed or skipped.

**Dependencies.** Application: `AlphaOnboardingService`. UI: V1 alpha templates. Educational: none beyond orientation copy.

**Current Maturity.** Integrated.

**Known Limitations.** Once per user. Uses V1 shell (dual chrome with EOS nav — DEP-002).

**Risks.** Educational: skip may leave students under-oriented. Trust: low. Technical: low. Operational: low. Accessibility: V1 templates, less EOS a11y coverage.

**Testing Status.** Unit/integration via alpha services; operational auth flow; presentation partial. Accessibility: limited. Certification: referenced in Internal Alpha validation pack (not executed).

**Release Recommendation.** **Ready with Conditions** — ship for Alpha; condition: dual-chrome accepted for Alpha; cohort validation should cover onboarding once.

---

### CAP-03 — Student Home (Today)

| Field | Value |
|-------|-------|
| **Capability Name** | Student Home |
| **Owner Programme** | EP-007.1 / EP-008 / PX-003 / ILE-004 (panel) |
| **Current Version** | Sole-runtime canonical home |
| **Feature Flag** | `KWALITEC_V2_SOLE_RUNTIME` (prod ON); optional `ENABLE_UNIFIED_JOURNEY`, `ENABLE_EXPERIENCE_FEEDBACK` |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.home` → `/student/` |

**Educational Purpose.** One calm daily centre: what to study today, why, and how to start — without competing educational authorities.

**Product Purpose.** Primary Alpha destination; hosts recommendation, commitment, Daily Mission Intelligence, coach/readiness disclosure, welcome modal.

**Dependencies.** Educational: authorised recommendation / MES, Decision Journal mirror. Technical: Student Experience composition, durable store, bridges as configured. UI: `home.html`, EOS shell. Application: `StudentExperienceService`, commitment services. Infrastructure: Postgres persistence when durable ON.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Empty when no authorised recommendation. ILE-004 panel may feel verbose beside MES L1. Welcome modal only on EOS home. Onboarding gate may intercept before home.

**Risks.** Educational: empty-state clarity. Trust: competing copy if MES + mission intelligence duplicate. Technical: bridge/fail-open paths. Operational: sole-runtime misconfig returns legacy home. Accessibility: hero/commitment ARIA covered in presentation tests.

**Testing Status.** Unit: view models. Integration: experience services. Presentation: extensive (`test_routes`, MES, commitment, trust, mission intelligence). Accessibility: `test_accessibility.py`. Regression: `test_regression.py`, operational smoke. Certification: platform EI certified separately; Home UX cohort validation pending.

**Release Recommendation.** **Ready** — canonical Alpha surface under production sole runtime.

---

### CAP-04 — Daily Mission Intelligence

| Field | Value |
|-------|-------|
| **Capability Name** | Daily Mission Intelligence |
| **Owner Programme** | ILE-004 (Complete 2026-07-28) |
| **Current Version** | 1.0 Complete |
| **Feature Flag** | None (composes from existing Home recommendation) |
| **Student Visible** | Conditional (when authorised recommendation exists) |
| **Production Enabled** | Yes (when recommendation present) |
| **Navigation Entry Point** | Embedded on `student.home` |

**Educational Purpose.** Explain today’s primary mission: what / why / what next / uncertainty — so students trust the guidance.

**Product Purpose.** Explainability panel on Home; does not re-select tips.

**Dependencies.** Educational: authorised Runtime A / MES recommendation. Technical: `daily_mission_intelligence_service`, domain compose. UI: labelled `aside` on Home. Application: home view model projection.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Does not change selection. May duplicate MES L1 lines. Absent when no recommendation.

**Risks.** Educational: verbosity fatigue. Trust: duplication may feel inconsistent. Technical: low (deterministic compose). Operational: low. Accessibility: `ILE-004/ACCESSIBILITY.md`; labelled panel.

**Testing Status.** Domain compose tests; service tests; presentation `test_daily_mission_intelligence.py`. Accessibility: documented + presentation. Certification: explainability/recommendation reviews in ILE-004 pack.

**Release Recommendation.** **Ready** — complete programme; production-visible when recommendation exists.

---

### CAP-05 — Journey (Exam Readiness / Topic Progress)

| Field | Value |
|-------|-------|
| **Capability Name** | Journey |
| **Owner Programme** | Student Experience / EP-007.1; Runtime C: PX-001 |
| **Current Version** | V2 Experience surface |
| **Feature Flag** | `ENABLE_JOURNEY_BRIDGE` (backend); Runtime C flags optional |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.journey` → `/student/journey` |

**Educational Purpose.** Shows progress toward exam readiness by topic so students see where they stand in the syllabus journey.

**Product Purpose.** Second primary EOS surface; progress and readiness cards.

**Dependencies.** Educational: curriculum topic ordering via Experience ports. Technical: journey port / bridge. UI: `journey.html`, progress/readiness components. Application: journey view models; terminology guards.

**Current Maturity.** Integrated.

**Known Limitations.** May empty if ports unavailable. Runtime C educational panel only when enrolment flags ON (currently OFF in prod).

**Risks.** Educational: empty progress undermines confidence. Trust: forbidden learner terms guarded. Technical: bridge gaps. Operational: low. Accessibility: progressbar ARIA when present.

**Testing Status.** Presentation routes/nav/view models; operational smoke. Accessibility: progress ARIA tests. Certification: not separately.

**Release Recommendation.** **Ready** — core Alpha navigation surface.

---

### CAP-06 — Revision

| Field | Value |
|-------|-------|
| **Capability Name** | Revision |
| **Owner Programme** | Student Experience / Adaptive Decision port |
| **Current Version** | Implemented |
| **Feature Flag** | Adaptive engine/authority flags (backend); surface always registered |
| **Student Visible** | Yes |
| **Production Enabled** | Yes (page loads; content depends on adaptive port) |
| **Navigation Entry Point** | `student.revision` → `/student/revision`; POST `begin_revision` |

**Educational Purpose.** Surfaces the highest-value revision option so students can recover or consolidate deliberately.

**Product Purpose.** Dedicated revision destination in EOS nav.

**Dependencies.** Educational: adaptive recommendation port availability. Technical: revision service. UI: `revision.html`.

**Current Maturity.** Implemented.

**Known Limitations.** Degrades/empty when adaptive port unavailable. Adaptive authority flags default OFF.

**Risks.** Educational: empty revision page. Trust: “why this revision” may be thin without adaptive authority. Technical: port dependency. Operational: low. Accessibility: standard EOS shell.

**Testing Status.** Presentation routes/regression. Accessibility: shell. Certification: none dedicated.

**Release Recommendation.** **Ready with Conditions** — include in Alpha; condition: accept empty/degraded content when adaptive authority is OFF, or enable adaptive path intentionally before claiming revision quality.

---

### CAP-07 — History

| Field | Value |
|-------|-------|
| **Capability Name** | History |
| **Owner Programme** | Student Experience; EP-008 commitment narrative |
| **Current Version** | V2 Experience surface |
| **Feature Flag** | `ENABLE_HISTORY_BRIDGE`; sole runtime redirects `/analytics/` here |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.history` → `/student/history` |

**Educational Purpose.** Lets students review completed sessions and readiness trend — memory of study, not vanity metrics.

**Product Purpose.** Archive surface; gateway to Decision Journal and Educational Timeline.

**Dependencies.** Educational: session completion records, commitment narrative. Technical: history port/bridge. UI: `history.html`. Application: history view models.

**Current Maturity.** Integrated.

**Known Limitations.** Empty without sessions. Rich legacy analytics charts not ported.

**Risks.** Educational: thin archive early in Alpha. Trust: low. Technical: bridge. Operational: low. Accessibility: stats grid ARIA; empty `role="status"`.

**Testing Status.** Presentation routes/templates. Accessibility: history labels. Certification: none dedicated.

**Release Recommendation.** **Ready** — core Alpha archive surface.

---

### CAP-08 — Decision Journal

| Field | Value |
|-------|-------|
| **Capability Name** | Decision Journal |
| **Owner Programme** | ILE-002 (Complete 2026-07-28) |
| **Current Version** | 1.0 Complete |
| **Feature Flag** | None |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.decision_journal` → `/student/decision-journal` (via History) |

**Educational Purpose.** Records guidance decisions (accept/defer/outcome) so students can see what Study Sensei recommended and what they chose — professional learning through reflective memory.

**Product Purpose.** Continuity of educational decisions; feeds Timeline and Feedback Loop.

**Dependencies.** Educational: Home commitment/defer mirrors. Technical: `decision_journal_service`, ORM. UI: `decision_journal.html`. Application: DTOs, invariants.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Retrospective only. Evidence events not in JSON backup. Not all ILE-011 Decision IDs wired.

**Risks.** Educational: incomplete decision coverage. Trust: missing entries feel like the system “forgot.” Technical: migration present. Operational: backup gap. Accessibility: timeline entry styles; philosophy docs.

**Testing Status.** Domain invariants; service; presentation `test_decision_journal.py`. Accessibility: documented behaviour. Certification: ILE-002 completion.

**Release Recommendation.** **Ready** — complete and production-visible.

---

### CAP-09 — Educational Timeline

| Field | Value |
|-------|-------|
| **Capability Name** | Educational Timeline |
| **Owner Programme** | ILE-003 (Complete 2026-07-28) |
| **Current Version** | 1.0 Complete |
| **Feature Flag** | None |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.educational_timeline` → `/student/educational-timeline` |

**Educational Purpose.** Narrative continuity of learning decisions over time — “my educational story,” not a raw log dump.

**Product Purpose.** Student-facing narrative projection of journal entries.

**Dependencies.** Educational: Decision Journal entries. Technical: `educational_timeline_service`. UI: `educational_timeline.html`.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Empty until journal entries exist. 14-day momentum heuristic; cap of 8 beats.

**Risks.** Educational: sparse early Alpha. Trust: heuristic narrative must stay honest. Technical: low. Operational: low. Accessibility: `ILE-003/ACCESSIBILITY.md`.

**Testing Status.** Domain/service/presentation timeline tests. Accessibility: documented. Certification: ILE-003 completion.

**Release Recommendation.** **Ready**.

---

### CAP-10 — Educational Feedback Loop (Student Reflection)

| Field | Value |
|-------|-------|
| **Capability Name** | Educational Feedback Loop — optional student reflection |
| **Owner Programme** | ILE-005 (Complete 2026-07-28) |
| **Current Version** | 1.0 Complete |
| **Feature Flag** | None |
| **Student Visible** | Conditional (`can_reflect` on journal entries) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | POST `student.decision_journal_reflect`; UI on Decision Journal |

**Educational Purpose.** Lets students say whether guidance was useful — closing the honesty loop without changing selection.

**Product Purpose.** Optional reflection; internal Sensei review is not student-visible.

**Dependencies.** Educational: Decision Journal outcomes. Technical: `educational_feedback_loop_service`, migration `202607280002`. UI: reflection form on journal. Application: domain review/reflection models.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Optional only. Sensei educational review is internal. Mission-complete review uses completion entry only.

**Risks.** Educational: low uptake. Trust: students must not think reflection changes ranking (it does not). Technical: migration required. Operational: migration deploy. Accessibility: labelled radio groups.

**Testing Status.** Domain review; service; presentation `test_educational_feedback_loop.py`. Accessibility: form labels. Certification: ILE-005 explainability/recommendation reviews.

**Release Recommendation.** **Ready** — ship with journal; ensure migration applied.

---

### CAP-11 — Mission Commitment / Deferral / Reflection Ack

| Field | Value |
|-------|-------|
| **Capability Name** | Recommendation Commitment Flow |
| **Owner Programme** | EP-008.3 (mirrored to ILE-002) |
| **Current Version** | Integrated |
| **Feature Flag** | None |
| **Student Visible** | Yes (Home chrome) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | POST `student.start_session`, `defer_commitment`, `acknowledge_reflection` |

**Educational Purpose.** Makes starting today’s mission a conscious professional choice (or an honest deferral with reason).

**Product Purpose.** Commitment states on Home: confirm → committed → in-session → completion reflection → deferred.

**Dependencies.** Educational: authorised recommendation. Technical: `RecommendationCommitmentService`, persistence. UI: Home commitment blocks. Application: EP-008 contracts.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Defer is preference only — no ranking change.

**Risks.** Educational: defer reasons unused for adaptation (by design). Trust: students may expect defer to change tomorrow’s tip. Technical: low. Operational: low. Accessibility: labelled commitment/reflection blocks.

**Testing Status.** Application commitment tests; presentation trust/commitment contracts. Certification: EP-008 contracts.

**Release Recommendation.** **Ready**.

---

### CAP-12 — Session Experience

| Field | Value |
|-------|-------|
| **Capability Name** | Guided Study Session |
| **Owner Programme** | V2-019 Session Experience |
| **Current Version** | Integrated |
| **Feature Flag** | Durable store / completion bridges |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/session/<session_id>/overview` … `/complete` |

**Educational Purpose.** Delivers the study session as a coherent learning episode (overview → activity → reflection → summary).

**Product Purpose.** Execution path after Home start / revision begin.

**Dependencies.** Educational: mission/session content from Experience. Technical: session experience application + durable store. UI: `app/templates/session/*`. Application: session routes. Infrastructure: DB when durable ON.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** Quick Check embed fail-open if adaptive flags OFF.

**Risks.** Educational: session quality depends on mission content. Trust: resume/continuity. Technical: durable store required in prod. Operational: session orphaning. Accessibility: session CSS/base template.

**Testing Status.** Operational smoke (linear surfaces, resume). Presentation: partial vs Home. Accessibility: session shell. Certification: none dedicated beyond smoke.

**Release Recommendation.** **Ready** — required Alpha study path under durable store.

---

### CAP-13 — Quick Check (Adaptive Assessment)

| Field | Value |
|-------|-------|
| **Capability Name** | Quick Check |
| **Owner Programme** | ILE-001B / ILE-001C |
| **Current Version** | Complete (flag-gated) |
| **Feature Flag** | `KWALITEC_ADAPTIVE_ASSESSMENT` + `KWALITEC_QUICK_CHECK` (+ optional `KWALITEC_CONTEXTUAL_FRAMING`) — **all default OFF; not in Render** |
| **Student Visible** | Conditional (when flags ON and embedded) |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | `/adaptive-assessment/quick-check/*` via session/mission embed |

**Educational Purpose.** Short, honest assessment as a learning instrument — evidence without mastery theatre.

**Product Purpose.** Mission-embedded check; feeds assessment evidence pipeline when enabled.

**Dependencies.** Educational: registered assessment copy; optional contextual framing. Technical: adaptive assessment application. UI: adaptive_assessment templates. Application: feature flag resolver.

**Current Maturity.** Implemented (not production-activated).

**Known Limitations.** Deep/Recovery/Confidence/Readiness session types have flags but no student routes. Production flags unset.

**Risks.** Educational: Alpha without Quick Check lacks assessment-in-mission. Trust: enabling without cohort briefing. Technical: flag misconfiguration. Operational: subject/cohort allow-lists. Accessibility: ILE-001A checklist, reduced-motion, keyboard JS.

**Testing Status.** Strong application/architecture suite; presentation via adaptive assessment tests. Accessibility: ILE-001A. Certification: ILE-001B/C complete as programmes; **not activated for Alpha runtime**.

**Release Recommendation.** **Ready with Conditions** — capability is built; **condition for Alpha inclusion:** explicitly enable flags in the Alpha environment and brief testers, **or** document Alpha as “Quick Check not activated” (current production posture). Do not claim Alpha includes Quick Check until flags are ON.

---

### CAP-14 — Contextual Educational Framing

| Field | Value |
|-------|-------|
| **Capability Name** | Contextual Educational Framing (Study Sensei Context Card) |
| **Owner Programme** | ILE-001C |
| **Current Version** | Complete (flag-gated) |
| **Feature Flag** | `KWALITEC_CONTEXTUAL_FRAMING` (default OFF) |
| **Student Visible** | Conditional |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | Within Quick Check / assessment framing surfaces |

**Educational Purpose.** Frames why this check exists educationally — honesty before answers.

**Product Purpose.** Presentation-only framing; no selection change.

**Dependencies.** Educational: Quick Check. Technical: contextual framing modules. UI: framing cards.

**Current Maturity.** Implemented (not activated).

**Known Limitations.** Useless without Quick Check enabled.

**Risks.** Educational: framing without check confuses. Trust: low if OFF. Technical: flag coupling. Operational: low. Accessibility: covered with Quick Check.

**Testing Status.** `test_contextual_framing.py` and related. Certification: ILE-001C.

**Release Recommendation.** **Ready with Conditions** — same activation decision as CAP-13.

---

### CAP-15 — Standalone Learning Check (`/assessment`)

| Field | Value |
|-------|-------|
| **Capability Name** | Assessment Delivery (Learning Check) |
| **Owner Programme** | Assessment Delivery presentation |
| **Current Version** | Implemented |
| **Feature Flag** | None dedicated |
| **Student Visible** | Yes if URL known — **not in primary nav** |
| **Production Enabled** | Yes (routes live) |
| **Navigation Entry Point** | `assessment.entry` → `/assessment/` |

**Educational Purpose.** Standalone learning check outside mission embed.

**Product Purpose.** Alternate assessment entry; separate from Quick Check.

**Dependencies.** Application: assessment presentation. UI: `app/templates/student/assessment/*`. Educational: assessment items. Twin/reasoning: explicitly not integrated per route docs.

**Current Maturity.** Implemented.

**Known Limitations.** No primary nav entry. No Twin/reasoning integration. Less presentation test coverage than Quick Check.

**Risks.** Educational: two assessment paths may confuse. Trust: orphan URL discovery. Technical: dual systems. Operational: support burden. Accessibility: shared assessment base.

**Testing Status.** Limited presentation coverage. Certification: none as Alpha primary.

**Release Recommendation.** **Ready with Conditions** — keep available; **condition:** do not market as primary Alpha assessment path; prefer documenting mission-embedded Quick Check (when activated) or Session activity as the Alpha assessment story.

---

### CAP-16 — Study Plan Wizard & Management

| Field | Value |
|-------|-------|
| **Capability Name** | Study Plan |
| **Owner Programme** | V1 Study Plan; PI-002A subject discovery when flagged |
| **Current Version** | V1 integrated |
| **Feature Flag** | Optional `ENABLE_PUBLISHED_SUBJECT_DISCOVERY`, Runtime C enrolment |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `study_plan.index`; wizard steps 1–7; login without plan → wizard |

**Educational Purpose.** Curriculum-bound study plan from official syllabus structure — the foundation of personalised pacing.

**Product Purpose.** Required for new students; list/edit/archive/set-active.

**Dependencies.** Educational: curriculum engine V1/V2. Technical: study plan models/services. UI: V1 templates (dual chrome). Application: wizard validation. Infrastructure: DB.

**Current Maturity.** Alpha Candidate.

**Known Limitations.** V1 shell under sole runtime (DEP-002). Runtime C pilots may skip wizard re-loop.

**Risks.** Educational: wizard complexity. Trust: dual chrome inconsistency. Technical: curriculum V1/V2 must both work. Operational: plan CRUD. Accessibility: V1 wizard (less EOS coverage).

**Testing Status.** Study plan modules; Alpha validation pack mandates Study Plans area. Certification: curriculum invariants elsewhere.

**Release Recommendation.** **Ready with Conditions** — required for Alpha; **condition:** accept dual chrome for Alpha Stage 1 (DEP-002/003 posture).

---

### CAP-17 — Student Calibration (Twin Birth)

| Field | Value |
|-------|-------|
| **Capability Name** | Post-Plan Calibration |
| **Owner Programme** | Student Calibration / EP-001.1 foundation |
| **Current Version** | Implemented |
| **Feature Flag** | Uses EI internal alpha for Twin retrieval after birth |
| **Student Visible** | Yes (after plan path) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/calibration/after-plan/<id>`, `/calibration/resume` |

**Educational Purpose.** Birth an honest Twin from calibration so later guidance has a grounded learner model.

**Product Purpose.** Post-plan Twin foundation; presentation-only path (does not invoke recommendation engines directly).

**Dependencies.** Educational: study plan. Technical: calibration coordinator, Twin repository. Application: EI internal alpha for retrieval. UI: calibration templates.

**Current Maturity.** Integrated.

**Known Limitations.** Twin UX cutovers (insights/readiness/daily plan) remain flag-OFF. Tutor explain soft-fails without Twin.

**Risks.** Educational: Twin absent if skipped. Trust: “system doesn’t know me yet” honesty. Technical: Twin repository. Operational: resume path. Accessibility: calibration templates.

**Testing Status.** Application calibration integration tests. Certification: Twin foundation programmes (separate).

**Release Recommendation.** **Ready** — include in Alpha onboarding/plan path.

---

### CAP-18 — Student Profile (EOS Settings destination)

| Field | Value |
|-------|-------|
| **Capability Name** | Student Profile |
| **Owner Programme** | Student Experience / DEP-003 |
| **Current Version** | Integrated |
| **Feature Flag** | Sole runtime redirects `/settings/` → profile |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `student.profile` → `/student/profile` |

**Educational Purpose.** Shows goals and learning statistics so students own their study identity.

**Product Purpose.** Settings nav destination; links to account/data subpages.

**Dependencies.** UI: `profile.html`. Application: profile snapshot. Educational: goals/progress projections.

**Current Maturity.** Integrated.

**Known Limitations.** Notifications/reminders shown as read-only Enabled/Disabled — **no push notification system**. Account edits still on V1 settings subpages.

**Risks.** Educational: low. Trust: “notifications enabled” may imply push that does not exist. Technical: dual chrome. Operational: low. Accessibility: labelled DL; goal progress ARIA.

**Testing Status.** Presentation routes. Accessibility: profile labels. Certification: none.

**Release Recommendation.** **Ready with Conditions** — **condition:** copy must not imply push notifications; dual chrome accepted.

---

### CAP-19 — Settings Subpages (Account / Preferences / Data / Export)

| Field | Value |
|-------|-------|
| **Capability Name** | Account Settings & Data Controls |
| **Owner Programme** | V1 settings; RIP-001 link; PX-003 labelling |
| **Current Version** | V1 integrated |
| **Feature Flag** | None |
| **Student Visible** | Yes (from Profile) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/settings/profile`, `/preferences`, `/data`, `/internal-alpha`, export/import |

**Educational Purpose.** Learner control of identity, preferences, and data — professional ownership of study records.

**Product Purpose.** Account maintenance, PDF/backup export, internal alpha status, research check-in entry.

**Dependencies.** Application: settings routes/services. UI: V1 settings templates. Infrastructure: export generation.

**Current Maturity.** Integrated.

**Known Limitations.** Dual chrome. Preferences partially session-only (`daily_goal_hours`). Profile POST stub behaviour documented in settings. Share-feedback redirects to research check-in.

**Risks.** Educational: low. Trust: data export completeness (journal evidence gap noted under CAP-08). Technical: import restore. Operational: backup/restore support. Accessibility: V1 forms.

**Testing Status.** Settings suite coverage (broader). Certification: none.

**Release Recommendation.** **Ready with Conditions** — dual chrome + export gaps disclosed to Alpha testers.

---

### CAP-20 — Help & Alpha Feedback

| Field | Value |
|-------|-------|
| **Capability Name** | Help Centre & Alpha Feedback Channels |
| **Owner Programme** | ALPHA-001 |
| **Current Version** | Implemented |
| **Feature Flag** | None |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/alpha/help`; feedback routes under `/alpha/feedback/*`; POST `/alpha/telemetry` |

**Educational Purpose.** Students can report unclear explanations and unhelpful missions — protecting trust during Alpha.

**Product Purpose.** Support and structured product feedback; allowlisted client telemetry.

**Dependencies.** Application: `AlphaFeedbackService`, `PresentationTelemetryService`. UI: V1 alpha templates.

**Current Maturity.** Integrated.

**Known Limitations.** V1 shell. Telemetry allowlisted events only.

**Risks.** Educational: feedback not closing the loop to students. Trust: silence after report. Technical: low. Operational: triage capacity. Accessibility: V1.

**Testing Status.** Telemetry service tests; operational/alpha config. Certification: validation pack forms.

**Release Recommendation.** **Ready**.

---

### CAP-21 — Product Check-in (Research)

| Field | Value |
|-------|-------|
| **Capability Name** | Daily Reflection & Product Check-in |
| **Owner Programme** | RIP-001 |
| **Current Version** | Implemented |
| **Feature Flag** | None |
| **Student Visible** | Yes |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | `/research/checkin` |

**Educational Purpose.** Captures how study felt — research signal for product usefulness, distinct from ILE-005 educational reflection.

**Product Purpose.** Eligibility-gated product research check-in.

**Dependencies.** Application: `ResearchFeedbackService`. UI: research templates (V1 shell).

**Current Maturity.** Integrated.

**Known Limitations.** Post-study invitation gated by eligibility. Dual chrome.

**Risks.** Educational: confusion with Decision Journal reflection. Trust: survey fatigue. Technical: low. Operational: research data handling. Accessibility: V1.

**Testing Status.** Research route tests. Certification: none.

**Release Recommendation.** **Ready with Conditions** — disclose distinction from ILE-005 reflection to testers.

---

### CAP-22 — Welcome Modal & Revision Acknowledgement

| Field | Value |
|-------|-------|
| **Capability Name** | Welcome Modal & Syllabus-Complete Revision Ack |
| **Owner Programme** | PX-003 |
| **Current Version** | Integrated |
| **Feature Flag** | None |
| **Student Visible** | Conditional |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | Modal on Home; POST `dashboard.dismiss_welcome`, `dashboard.acknowledge_revision` |

**Educational Purpose.** First-run orientation and honest acknowledgement when syllabus phase completes.

**Product Purpose.** Lifecycle UX chrome on canonical home.

**Dependencies.** Application: `WelcomeService`, `LearningLifecycleService`. UI: `welcome_modal.html`, `app.js` focus trap.

**Current Maturity.** Integrated.

**Known Limitations.** Welcome only on student home (not legacy dashboard under sole runtime).

**Risks.** Educational: low. Trust: low. Technical: low. Operational: low. Accessibility: dialog ARIA + focus trap tested.

**Testing Status.** `test_accessibility.py`. Certification: PX-003.

**Release Recommendation.** **Ready**.

---

### CAP-23 — Intelligent Tutor — Explain Mission

| Field | Value |
|-------|-------|
| **Capability Name** | Explain Today’s Mission (Tutor) |
| **Owner Programme** | TUTOR-001 / EP-001.1 |
| **Current Version** | Partial student surface |
| **Feature Flag** | Implicit Twin availability (`StudentDigitalTwinService`); `KWALITEC_DIGITAL_TWIN` not in Render |
| **Student Visible** | Conditional (button when Twin available) |
| **Production Enabled** | Conditional |
| **Navigation Entry Point** | POST `student.tutor_explain_mission` |

**Educational Purpose.** Short explanation of why today’s mission matters — tutor voice without a full chat product.

**Product Purpose.** Flash-based explain on Home; no dedicated student tutor page.

**Dependencies.** Educational: Twin birth. Technical: `IntelligentTutorService`. UI: Home button + flash.

**Current Maturity.** Prototype → Implemented (partial).

**Known Limitations.** Soft-fails without Twin. Flash-only. Founder tutor diagnostics are not student-facing.

**Risks.** Educational: missing explain when Twin absent. Trust: inconsistent availability. Technical: Twin dependency. Operational: low. Accessibility: flash messages.

**Testing Status.** Limited dedicated presentation tests. Certification: tutor programmes separate.

**Release Recommendation.** **Ready with Conditions** — soft-fail acceptable for Alpha; do not claim full Tutor experience.

---

### CAP-24 — Navigation (Education OS Chrome)

| Field | Value |
|-------|-------|
| **Capability Name** | Student Navigation |
| **Owner Programme** | Student Experience / DEP-003; P2-MS001 unified journey (optional) |
| **Current Version** | Integrated |
| **Feature Flag** | Default feature mode; `ENABLE_UNIFIED_JOURNEY` for journey-stage labels (OFF) |
| **Student Visible** | Yes |
| **Production Enabled** | Yes (feature-mode nav) |
| **Navigation Entry Point** | Global EOS nav: Home · Journey · Revision · History · Settings · Study Plan · Help |

**Educational Purpose.** One coherent educational OS — students always know where they are in the learning product.

**Product Purpose.** Canonical chrome; maps surfaces to endpoints; History covers Journal/Timeline.

**Dependencies.** Application: `navigation.py`, experience surfaces. UI: base student template. Feature: unified journey optional.

**Current Maturity.** Alpha Candidate (feature mode).

**Known Limitations.** Unified journey mode OFF in production. Dual chrome on shared V1 pages.

**Risks.** Educational: dual chrome confuses IA. Trust: “two products.” Technical: flag. Operational: low. Accessibility: `aria-current="page"` tested.

**Testing Status.** `test_navigation.py`, accessibility, responsive. Certification: DEP-003 posture.

**Release Recommendation.** **Ready** — feature-mode nav is Alpha default.

---

### CAP-25 — Accessibility Features

| Field | Value |
|-------|-------|
| **Capability Name** | Accessibility (cross-cutting) |
| **Owner Programme** | PX / ILE-001A / ILE-003 / ILE-004 |
| **Current Version** | Integrated (EOS + Quick Check docs) |
| **Feature Flag** | None (CSS reduced-motion for Quick Check when present) |
| **Student Visible** | Yes (platform behaviour) |
| **Production Enabled** | Yes |
| **Navigation Entry Point** | N/A (cross-cutting) |

**Educational Purpose.** Every student can access learning guidance regardless of sensory/motor constraints — educational equity.

**Product Purpose.** ARIA landmarks, focus management, progress semantics, terminology honesty, responsive layout.

**Dependencies.** UI: student CSS, session CSS, templates. Application: forbidden-term guards. Tests: accessibility suite.

**Current Maturity.** Integrated.

**Known Limitations.** V1 dual-chrome pages have less coverage than EOS. Full WCAG audit not claimed.

**Risks.** Accessibility risk: dual-chrome gaps; Quick Check a11y unused while flags OFF. Educational: low. Trust: terminology leaks. Technical: low. Operational: low.

**Testing Status.** `test_accessibility.py`, `test_responsive.py`, `test_terminology.py`; ILE a11y docs. Certification: not a formal a11y certificate.

**Release Recommendation.** **Ready with Conditions** — EOS core Ready; **condition:** Alpha does not claim WCAG conformance; dual-chrome pages are residual risk.

---

### CAP-26 — Feature Flags (Student-Affecting Controls)

| Field | Value |
|-------|-------|
| **Capability Name** | Feature Flag System |
| **Owner Programme** | V2 flags / EI internal alpha / Adaptive Assessment / Analytics |
| **Current Version** | Integrated |
| **Feature Flag** | N/A (meta) |
| **Student Visible** | Indirect (gates surfaces) |
| **Production Enabled** | Yes (resolvers live) |
| **Navigation Entry Point** | None (ops/env) |

**Educational Purpose.** Progressive enablement so unfinished educational experiences stay hidden until ready.

**Product Purpose.** Safe defaults; production sole-runtime + EI internal alpha subset ON.

**Dependencies.** `v2_flags.py`, `internal_alpha.py`, `adaptive_assessment/feature_flags.py`, analytics flag. Infrastructure: Render env.

**Current Maturity.** Certified (as control plane for Alpha inventory).

**Known Limitations.** Many student capabilities exist in code but OFF. Dual chrome out of sole-runtime contract (DEP-002).

**Risks.** Operational: mis-set flags change Alpha scope silently. Trust: “works on my machine.” Educational: activating unfinished paths. Technical: flag matrix complexity. Accessibility: N/A.

**Testing Status.** `test_internal_alpha.py`, `test_alpha_configuration.py`, flag unit tests. Certification: this work package.

**Release Recommendation.** **Ready** — register is authoritative (`FEATURE_FLAG_REGISTER.md`).

---

### CAP-27 — Unified Journey Chrome

| Field | Value |
|-------|-------|
| **Capability Name** | Unified Journey Navigation & Guided Day |
| **Owner Programme** | P2-MS001–004 |
| **Current Version** | Implemented |
| **Feature Flag** | `KWALITEC_UNIFIED_JOURNEY` (default OFF) |
| **Student Visible** | Conditional |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | Replaces nav labels when ON |

**Educational Purpose.** Journey-stage language (Today / Planning / Exam Readiness…) for a single learning story.

**Product Purpose.** Alternate chrome; guided session attributes on Home.

**Dependencies.** `unified_journey` application; navigation builder.

**Current Maturity.** Implemented (not activated).

**Known Limitations.** Default OFF per EP-007.1. Experience Feedback requires this flag too.

**Risks.** Educational: activating mid-Alpha changes IA overnight. Trust: label churn. Technical: mapping bugs. Operational: support scripts. Accessibility: needs re-validation when ON.

**Testing Status.** Unified journey + navigation tests. Certification: programme complete; not Alpha-activated.

**Release Recommendation.** **Not Ready** for Alpha default — keep OFF unless a controlled Alpha experiment is approved.

---

### CAP-28 — Experience Feedback on Home (“Your Journey”)

| Field | Value |
|-------|-------|
| **Capability Name** | Experience Feedback Summaries |
| **Owner Programme** | P2-MS008 |
| **Current Version** | Implemented |
| **Feature Flag** | `ENABLE_EXPERIENCE_FEEDBACK` + requires Unified Journey |
| **Student Visible** | Conditional |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | Home section when enabled |

**Educational Purpose.** Factual evidence summaries of the student’s journey — display only.

**Product Purpose.** Home “Your Journey” facts; no adaptation.

**Dependencies.** Unified Journey ON; evidence read models.

**Current Maturity.** Implemented (not activated).

**Known Limitations.** Requires two flags. Display-only.

**Risks.** Educational: mistaken for recommendations. Trust: factual vs advisory confusion. Technical: flag coupling. Operational: low. Accessibility: unvalidated in prod posture.

**Testing Status.** Application unified journey / feedback tests. Certification: not Alpha-activated.

**Release Recommendation.** **Not Ready** for Alpha default (depends on CAP-27).

---

### CAP-29 — Runtime C Educational Experience Panel

| Field | Value |
|-------|-------|
| **Capability Name** | Runtime C Published Syllabus Context |
| **Owner Programme** | PX-001 / PI-002A |
| **Current Version** | Implemented |
| **Feature Flag** | `KWALITEC_RUNTIME_C_ENROLMENT`, published subject discovery (default OFF) |
| **Student Visible** | Conditional (enrolled) |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | Embedded Home/Journey via Runtime C page path |

**Educational Purpose.** Educational context from published syllabus enrolment — curriculum-first for Runtime C pilots.

**Product Purpose.** Fail-open to Runtime A when not enrolled.

**Dependencies.** Platform integration flags; educational experience service.

**Current Maturity.** Implemented (not activated).

**Known Limitations.** Flags OFF in Render. Separate mission-complete POST for Runtime C.

**Risks.** Educational: dual runtime confusion if partially enabled. Trust: fail-open honesty. Technical: enrolment allow-list. Operational: pilot ops. Accessibility: educational experience templates.

**Testing Status.** Application educational experience tests. Certification: not Alpha-activated for general cohort.

**Release Recommendation.** **Not Ready** for general Alpha — pilot-only if flags intentionally set.

---

### CAP-30 — Legacy Runtime A Homes (Dashboard / Missions / Analytics)

| Field | Value |
|-------|-------|
| **Capability Name** | Legacy Dashboard, Missions Hub, Analytics Charts |
| **Owner Programme** | V1 Runtime A; EP-002.x cutovers |
| **Current Version** | Soak / rollback shells |
| **Feature Flag** | Sole runtime redirects away |
| **Student Visible** | Dual-run only; redirected in production |
| **Production Enabled** | Registered but redirected |
| **Navigation Entry Point** | `/dashboard/`, `/missions/`, `/analytics/` → EOS destinations |

**Educational Purpose.** Historical V1 study surfaces; not the Alpha educational story under sole runtime.

**Product Purpose.** Rollback and dual-run coexistence.

**Dependencies.** Legacy blueprints still registered.

**Current Maturity.** Integrated (as rollback), not Alpha primary.

**Known Limitations.** Competing home if sole runtime unset. Charts not on History.

**Risks.** Educational: contradiction if sole runtime fails. Trust: two homes. Technical: redirect bugs. Operational: rollback procedure. Accessibility: legacy templates.

**Testing Status.** Operational sole-runtime protection tests. Certification: DEP-002 audit.

**Release Recommendation.** **Not Ready** as Alpha primary — must remain redirected; rollback only.

---

### CAP-31 — Notifications

| Field | Value |
|-------|-------|
| **Capability Name** | Student Notifications / Push Reminders |
| **Owner Programme** | N/A (port stub) |
| **Current Version** | Not implemented |
| **Feature Flag** | None |
| **Student Visible** | No (profile shows read-only Enabled/Disabled defaults only) |
| **Production Enabled** | **No** |
| **Navigation Entry Point** | None |

**Educational Purpose.** Would support study cadence reminders — **not available**.

**Product Purpose.** Preference projection only; `NotificationProvider` port unwired for student UI.

**Dependencies.** None live.

**Current Maturity.** Prototype (port only).

**Known Limitations.** No notification centre. No push. Flash messages and alpha feedback are not a notification product.

**Risks.** Trust: profile “notifications enabled” misleads. Educational: none (absent). Technical: none. Operational: none. Accessibility: N/A.

**Testing Status.** N/A product. Certification: explicitly excluded from Alpha.

**Release Recommendation.** **Not Ready** — out of Alpha scope; disclose preference UI as non-functional for push.

---

### CAP-32 — Progress Surfaces (Composite)

| Field | Value |
|-------|-------|
| **Capability Name** | Progress Surfaces (composite view of where progress appears) |
| **Owner Programme** | Cross-cutting (Home, Journey, History, Profile, Session, Plan) |
| **Current Version** | Integrated |
| **Feature Flag** | Various bridge/cutover flags affect richness |
| **Student Visible** | Yes |
| **Production Enabled** | Yes (EOS surfaces) |
| **Navigation Entry Point** | See CAP-03, 05, 07, 18, 12, 16 |

**Educational Purpose.** Students see syllabus-bound progress and readiness without mastery theatre.

**Product Purpose.** Distributed progress — not a single analytics product under sole runtime.

**Dependencies.** Experience ports, curriculum, session completion, plan structure.

**Current Maturity.** Integrated.

**Known Limitations.** Legacy analytics charts redirected away. Twin readiness cutover OFF. Early Alpha may look sparse.

**Risks.** Educational: sparse progress early. Trust: inconsistent numbers across surfaces. Technical: bridge gaps. Operational: low. Accessibility: progressbar semantics on Journey/Profile.

**Testing Status.** Covered via surface tests. Certification: composite inventory only.

**Release Recommendation.** **Ready** — as the distributed EOS progress story; do not claim legacy Analytics charts in Alpha.

---

## Explicitly out of Alpha student scope

| Item | Reason |
|------|--------|
| Public registration | By design disabled |
| Founder / console / diagnostics | Admin only |
| ILE-010 / ILE-011 | Philosophy/framework docs — no student runtime |
| ILE-006 Study Intelligence | Not implemented as product surface |
| Push notifications | Not implemented |
| Deep / Recovery / Confidence / Readiness Checks | Flags only; no routes |
| EI missions / explainability / progress widgets | Flags always OFF even under internal alpha |
| Twin study-insights / readiness / daily-plan cutovers | Default OFF; not in Render |
| Unified Journey + Experience Feedback | Default OFF |

---

## Related deliverables

| Document | Role |
|----------|------|
| `CAPABILITY_MATRIX.md` | Compact readiness matrix |
| `FEATURE_FLAG_REGISTER.md` | All student-affecting flags |
| `DEPENDENCY_MATRIX.md` | Cross-capability dependencies |
| `RISK_REGISTER.md` | Consolidated risks |
| `RP001_1_COMPLETION_REPORT.md` | Certification outcome |

---

## Certification statement

As of 2026-07-28, this inventory is the authoritative statement of Alpha candidate student-facing capability scope and readiness. Changes to flags or surfaces after this date require a delta to this package.
