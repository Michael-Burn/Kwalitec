# PX-002 — Premium Experience Workstreams

**Programme:** PX-002 — Premium Experience Workstream Planning  
**Status:** Planning complete — **implementation not authorised**  
**Effective:** 2026-08-04  
**Authority:** `PX001_PREMIUM_BACKLOG.md` · `PX001_PROGRAMME_CHARTER.md` · `PX001_EXECUTION_PLAN.md` · `PX001_PREMIUM_PROGRAMME.md` · PB-017 PASS · Educational Content Freeze · EF-001  

**Rule:** Every open PX-B item maps to **exactly one** workstream. Parked PX-X-* items remain outside PX and are listed for completeness only. No Runtime, Educational Framework, recommendation, Twin, curriculum, or educational package changes.

---

## 1. Purpose of this document

Consolidate the PX-001 backlog into twelve coherent engineering workstreams so Version 1 Premium Experience can be commissioned, sequenced, and certified without losing backlog items or reopening educational law.

---

## 2. Coverage integrity

| Check | Result |
|-------|--------|
| Open PX-B items in backlog | PX-B-001 … PX-B-054 (**54**) |
| Items assigned to workstreams | **54** |
| Duplicate assignments | **0** |
| Unassigned open items | **0** |
| Parked PX-X-* in workstreams | **None** (remain parked) |

### 2.1 Master assignment matrix

| ID | Workstream |
|----|------------|
| PX-B-001 | WS-01 Trust & Navigation |
| PX-B-002 | WS-01 Trust & Navigation |
| PX-B-003 | WS-01 Trust & Navigation |
| PX-B-004 | WS-03 Revision Experience |
| PX-B-005 | WS-03 Revision Experience |
| PX-B-006 | WS-08 Reliability |
| PX-B-007 | WS-03 Revision Experience |
| PX-B-008 | WS-08 Reliability |
| PX-B-009 | WS-08 Reliability |
| PX-B-010 | WS-04 Home Experience |
| PX-B-011 | WS-04 Home Experience |
| PX-B-012 | WS-04 Home Experience |
| PX-B-013 | WS-04 Home Experience |
| PX-B-014 | WS-02 Session Workflow |
| PX-B-015 | WS-02 Session Workflow |
| PX-B-016 | WS-02 Session Workflow |
| PX-B-017 | WS-02 Session Workflow |
| PX-B-018 | WS-10 Premium Moments |
| PX-B-019 | WS-10 Premium Moments |
| PX-B-020 | WS-10 Premium Moments |
| PX-B-021 | WS-10 Premium Moments |
| PX-B-022 | WS-10 Premium Moments |
| PX-B-023 | WS-06 Accessibility |
| PX-B-024 | WS-06 Accessibility |
| PX-B-025 | WS-06 Accessibility |
| PX-B-026 | WS-06 Accessibility |
| PX-B-027 | WS-06 Accessibility |
| PX-B-028 | WS-06 Accessibility |
| PX-B-029 | WS-06 Accessibility |
| PX-B-030 | WS-06 Accessibility |
| PX-B-031 | WS-09 Performance |
| PX-B-032 | WS-09 Performance |
| PX-B-033 | WS-02 Session Workflow |
| PX-B-034 | WS-01 Trust & Navigation |
| PX-B-035 | WS-01 Trust & Navigation |
| PX-B-036 | WS-05 Mobile Experience |
| PX-B-037 | WS-05 Mobile Experience |
| PX-B-038 | WS-07 Microcopy & Identity |
| PX-B-039 | WS-07 Microcopy & Identity |
| PX-B-040 | WS-07 Microcopy & Identity |
| PX-B-041 | WS-07 Microcopy & Identity |
| PX-B-042 | WS-07 Microcopy & Identity |
| PX-B-043 | WS-07 Microcopy & Identity |
| PX-B-044 | WS-07 Microcopy & Identity |
| PX-B-045 | WS-07 Microcopy & Identity |
| PX-B-046 | WS-10 Premium Moments |
| PX-B-047 | WS-10 Premium Moments |
| PX-B-048 | WS-04 Home Experience |
| PX-B-049 | WS-10 Premium Moments |
| PX-B-050 | WS-04 Home Experience |
| PX-B-051 | WS-10 Premium Moments |
| PX-B-052 | WS-11 Founder Dogfooding |
| PX-B-053 | WS-12 Premium Certification |
| PX-B-054 | WS-01 Trust & Navigation |

---

## 3. Workstreams

### WS-01 — Trust & Navigation

| Field | Detail |
|-------|--------|
| **Purpose** | Make student-visible chrome tell one honest story about where the student is, what day/package is active, how long today is, and what the start verb means — so “the product knows where I am” holds after every sitting. |
| **Scope** | Finish/Home/title chrome identity; duration label unification (presentation resolver only); Profile exam-label projection; study-start verb family; ops expected-day labels kept out of student chrome. **Not** selection logic, Twin redesign, or duration-engine redesign (PX-X-05). |
| **Included PX-B items** | PX-B-001 · PX-B-002 · PX-B-003 · PX-B-034 · PX-B-035 · PX-B-054 |
| **Dependencies** | Founder decision on authoritative duration source (PX-B-035); package-bound chrome pattern from RO1-R1; must not change recommendation/selection. |
| **Estimated complexity** | **L** (six items; two S1 trust classes; Founder decision gate on duration) |
| **Regression risk** | **High** — wrong chrome/duration breaks Progressive Confidence soft-pass classes and student trust. |
| **Acceptance criteria** | Learning + Revision Finish/Home/title chrome resolve from package / journey identity; soft title-keyword chrome retired on student Home; same-day duration consistent across Home/Mission/Plan (or explained); Profile never shows “Not set” when active plan has exam; one canonical start/continue/resume verb family; ops detectors documented/isolated from student chrome. |
| **Definition of Done** | All six IDs Closed or Board-waived; targeted chrome/duration/profile regression tests green; sole-runtime screenshots filed; no educational selection change; EF-001 review N/A or YES-under-existing-law. |

---

### WS-02 — Session Workflow

| Field | Detail |
|-------|--------|
| **Purpose** | Give students one coherent mental model for starting, finishing, and recovering a study sitting — without dual-path confusion or premature controls. |
| **Scope** | Authoritative happy-path declaration (`session/*` vs `mission/*`); Complete-step honesty; Finish confirmation; password-recovery posture (copy/ops SLA; full auth reset is capacity-gated); interactive readiness of controls. **Not** new recommendation logic. |
| **Included PX-B items** | PX-B-014 · PX-B-015 · PX-B-016 · PX-B-017 · PX-B-033 |
| **Dependencies** | Founder decision on authoritative completion path (PX-B-014); shared confirm modal for PX-B-016; Ops ownership for recovery backend (PX-B-017). |
| **Estimated complexity** | **L** (PX-B-014 is L; others S–M) |
| **Regression risk** | **Medium–High** — completion path changes can break session tests and sole-runtime redirects. |
| **Acceptance criteria** | One student-authoritative completion path declared and other path aligned or hidden; phantom Complete step resolved; Finish uses confirm or documented low-stakes exception; recovery messaging honest with ops SLA; no control looks interactive before it works. |
| **Definition of Done** | All five IDs Closed or waived; session happy-path manual + automated checks pass; no educational body changes. |

---

### WS-03 — Revision Experience

| Field | Detail |
|-------|--------|
| **Purpose** | Make Revision sittings feel retrieval-correct and appear automatically after learning chains — students never depend on force-regenerate. |
| **Scope** | Revision Q6 / checklist presentation variants; tip-complete → terminal R1 regenerate; natural tip-complete Memory/Publication handoff re-verify. Presentation only for Q6; continuity handoff for regenerate — **not** package educational body or selection policy. |
| **Included PX-B items** | PX-B-004 · PX-B-005 · PX-B-007 |
| **Dependencies** | Continuity wiring at presentation/regenerate boundary; related reliability of tip-complete (PX-B-005 ↔ PX-B-007); Editorial voice check for PX-B-004. |
| **Estimated complexity** | **L** (PX-B-005 M–L; 007 re-verify M; 004 S–M) |
| **Regression risk** | **High** — PB-017 Rho class; force-R1 residual is S1. |
| **Acceptance criteria** | Natural tip-complete yields terminal Revision without force-R1; Memory/Publication handoff holds on natural enrolments with automated regression; Revision checklist/Q6 language names retrieval next steps. |
| **Definition of Done** | All three Closed or waived; PB-class regenerate regression evidence; no force-R1 required on dogfood natural path. |

---

### WS-04 — Home Experience

| Field | Detail |
|-------|--------|
| **Purpose** | Make Home (and adjacent Analytics/Journey surfaces) say one clear next action with honest density for day-zero, returning, and rich-history states. |
| **Scope** | Home composition hierarchy; Analytics KPI density and day-zero framing; Journey/History secondary craft; contextual density by account state; Coach panel information contract (Future). Protect explainability — compress, do not delete honesty. |
| **Included PX-B items** | PX-B-010 · PX-B-011 · PX-B-012 · PX-B-013 · PX-B-048 · PX-B-050 |
| **Dependencies** | Trust chrome (WS-01) should land first so Home composition builds on honest titles; PX-B-050 is Future capacity only. |
| **Estimated complexity** | **M–L** (010 High Impact M; 050 Future) |
| **Regression risk** | **Medium** — Home is primary CTA surface; must not hide authorised next action. |
| **Acceptance criteria** | One-composition hierarchy on Home; ≤4 KPIs / honest hour rounding on Analytics; day-zero Analytics non-punitive; Journey/History enriched without dashboard theatre; density varies by account state without re-selecting missions; Coach distinct or hidden (if executed). |
| **Definition of Done** | Non-Future IDs Closed or waived; before/after Home screenshots; explainability of primary CTA preserved. |

---

### WS-05 — Mobile Experience

| Field | Detail |
|-------|--------|
| **Purpose** | Establish one deliberate mobile navigation pattern and prove primary-path quality with live device evidence. |
| **Scope** | Canonical student-shell mobile nav decision; Founder phone + tablet dogfood with screenshot evidence and defect closure. Touch-target tokens live in WS-06 but must be verified on devices here. |
| **Included PX-B items** | PX-B-036 · PX-B-037 |
| **Dependencies** | Sole runtime; live device/emulator access; WS-06 touch targets (PX-B-025) for usable taps. |
| **Estimated complexity** | **M** |
| **Regression risk** | **Medium** — nav pattern change can affect desktop shells if not scoped. |
| **Acceptance criteria** | One mobile nav pattern for canonical student shell; live phone + tablet evidence filed; concrete defects from evidence closed or Board-owned. |
| **Definition of Done** | Both IDs Closed or waived; evidence pack under programme evidence paths; no dual-nav product strategy (PX-X-04 parked). |

---

### WS-06 — Accessibility

| Field | Detail |
|-------|--------|
| **Purpose** | Close primary-path exclusion risks: touch, contrast, focus, reduced motion, keyboard, modal resilience, and automated verification. |
| **Scope** | Confirm-modal resilience; session timer live region; touch-target tokens; focus-visible; reduced-motion completeness; sidebar label contrast; end-to-end keyboard audit; axe/Lighthouse + one AT pass. |
| **Included PX-B items** | PX-B-023 · PX-B-024 · PX-B-025 · PX-B-026 · PX-B-027 · PX-B-028 · PX-B-029 · PX-B-030 |
| **Dependencies** | CI capacity for PX-B-030; motion system (WS-10 / PX-B-018) must honour reduced motion (PX-B-027). |
| **Estimated complexity** | **L** (eight items; Foundation keyboard + automation) |
| **Regression risk** | **Medium** — CSS/focus changes are broad but usually local. |
| **Acceptance criteria** | Destructive actions fail visibly if modal unavailable; polite timer live region; ≥44px touch targets on icon/nav controls; focus-visible discipline; student-shell reduced-motion aligned; sidebar labels AA; keyboard primary path complete; automated a11y on primary routes + recorded AT pass. |
| **Definition of Done** | All eight Closed or risk-owned; a11y evidence in CI/logs; no WCAG full-conformance claim without audit language discipline. |

---

### WS-07 — Microcopy & Identity

| Field | Detail |
|-------|--------|
| **Purpose** | Replace Internal Alpha / tooling voice with lasting student identity and calm, useful language at first touch, session, help, return, and exam horizon. |
| **Scope** | “Education Operating System” decision; Alpha → student identity; session terminology; reflection framing; Help Centre FAQ (non-package); diagnostic disclosure; return-after-gap; exam-approach tone. Presentation microcopy only — **not** LO / package body. |
| **Included PX-B items** | PX-B-038 · PX-B-039 · PX-B-040 · PX-B-041 · PX-B-042 · PX-B-043 · PX-B-044 · PX-B-045 |
| **Dependencies** | Founder decisions on brand descriptor and Alpha badge (038, 039); PX-B-022 celebration craft coordination for relocating research chrome; must not invent catch-up recommendations (044). |
| **Estimated complexity** | **M** (mostly S–M; Help Centre M) |
| **Regression risk** | **Low–Medium** — test-pinned strings may need coordinated updates. |
| **Acceptance criteria** | Single-source product descriptor; student-grade Version 1 identity on student paths; practice/session language student-readable; reflection value framed at point of use; Help answers real how-do-I topics; build metadata collapsed to support disclosure; welcome-back and exam-horizon packs calm and authorised-next-action only. |
| **Definition of Done** | All eight Closed or waived; Editorial sign-off on identity pack; Educational Content Freeze held. |

---

### WS-08 — Reliability

| Field | Detail |
|-------|--------|
| **Purpose** | Keep ordinary students on the natural path under load and at campaign join — without ops heroics or educational-looking failures. |
| **Scope** | First-sitting campaign engagement race; Continue Session contention recovery; Render/API job latency with perceived-performance craft and ops SLOs. Student-facing dignity; never score infra as educational failure. |
| **Included PX-B items** | PX-B-006 · PX-B-008 · PX-B-009 |
| **Dependencies** | Hosting/Render; loading craft (WS-09 / PX-B-032); mission regeneration timing without selection policy change. |
| **Estimated complexity** | **M–L** |
| **Regression risk** | **High** under parallel PB ops; student path must remain idempotent. |
| **Acceptance criteria** | First sitting does not flash wrong campaign inventory; Continue Session recovers calmly under load; provision/job waits have honest progress and trimmed cold path where feasible. |
| **Definition of Done** | All three Closed or waived; PB simulation contention notes improved; no educational selection change. |

---

### WS-09 — Performance

| Field | Detail |
|-------|--------|
| **Purpose** | Make Home/Mission feel ready: measured student-path weight down, skeletons coherent, no blank paints that break premium calm. |
| **Scope** | Perceived performance on SSR student paths; loading/skeleton coherence on Home/Mission/Plan transitions. Complements WS-08 latency craft without owning job SLOs. |
| **Included PX-B items** | PX-B-031 · PX-B-032 |
| **Dependencies** | Asset hygiene; PX-B-009 (WS-08) for cold-path ops; measure before claim. |
| **Estimated complexity** | **M** |
| **Regression risk** | **Medium** — asset/template changes can affect paint and layout. |
| **Acceptance criteria** | Home/Mission perceived-performance Target vs `PREMIUM_QUALITY_ATTRIBUTES.md`; crafted skeletons on key transitions; no systematic blank-paint jumps on primary path. |
| **Definition of Done** | Both Closed or waived; before/after timing or scorecard notes filed. |

---

### WS-10 — Premium Moments

| Field | Detail |
|-------|--------|
| **Purpose** | Deliver restrained polish and honest celebration — presence without carnival, motivation without punishment. |
| **Scope** | Motion system; icon-only consistency; error Reference ID craft; sign-in brand; session-complete celebration; Continuity Front milestone acknowledgements; diligence reinforcement; preference stickiness UI; icon sourcing (Future). |
| **Included PX-B items** | PX-B-018 · PX-B-019 · PX-B-020 · PX-B-021 · PX-B-022 · PX-B-046 · PX-B-047 · PX-B-049 · PX-B-051 |
| **Dependencies** | Reduced-motion (WS-06 / PX-B-027) before/with motion (018); pilot feedback strategy for 022; Editorial for milestones; no XP/leaderboards (PX-X-07). |
| **Estimated complexity** | **M** (mix of Quick Wins and Nice to Have; 051 Future) |
| **Regression risk** | **Low–Medium** |
| **Acceptance criteria** | 2–3 house motions with reduced-motion honour; shared icon-only language; error ID tokenised + guidance; lockup-led sign-in; warm proportional completion without research chrome; light arc acknowledgements; gap-safe diligence cues; sticky preferences; icon library if capacity. |
| **Definition of Done** | Non-Future IDs Closed or waived; no pass promises; Celebration does not relocate educational authority. |

---

### WS-11 — Founder Dogfooding

| Field | Detail |
|-------|--------|
| **Purpose** | Detect chrome growth and diligence friction that only appear across multi-week real use. |
| **Scope** | Multi-week fatigue / chrome growth audit with logged observations feeding residual backlog or waiver. Complements WS-05 live mobile evidence (owned there). |
| **Included PX-B items** | PX-B-052 |
| **Dependencies** | Educational completion held; prior trust/home waves preferably landed so growth is measured against improved baseline. |
| **Estimated complexity** | **M** (study effort, calendar-bound) |
| **Regression risk** | **N/A** (observation programme — may spawn S2/S3 follow-ups) |
| **Acceptance criteria** | Founder dogfood across weeks completed; chrome-growth log filed; new defects classified under EF-001 operational review if needed. |
| **Definition of Done** | PX-B-052 Closed or Board-accepted residual; log linked from certification pack. |

---

### WS-12 — Premium Certification

| Field | Detail |
|-------|--------|
| **Purpose** | Re-score Version 1 Premium Experience against quality attributes with evidence — PASS / Conditional / Fail — so “premium” is not aspiration. |
| **Scope** | Full scorecard vs `PREMIUM_QUALITY_ATTRIBUTES.md`; evidence package; residual register empty or Board-accepted. |
| **Included PX-B items** | PX-B-053 |
| **Dependencies** | Prior workstream closures (especially WS-01…WS-09 High Impact / Foundation); WS-11 dogfood input. |
| **Estimated complexity** | **M** |
| **Regression risk** | **N/A** (assessment); Fail blocks premium claim, not educational freeze. |
| **Acceptance criteria** | Scorecard completed with evidence paths; Target+ on required surfaces per attributes; claim posture matches Charter (no until-exam trust via UX alone). |
| **Definition of Done** | PX-B-053 Closed with PASS or Conditional + owned residuals; programme completion report filed under implementation phase that executes certification. |

---

## 4. Parked items (not in workstreams)

| ID | Item | Rule |
|----|------|------|
| PX-X-01 … PX-X-09 | See `PX001_PREMIUM_BACKLOG.md` §K | Do not pull without separate programme |

---

## 5. Intra-programme priority (binding)

When capacity is tight across workstreams:

1. Trust / emotional honesty (WS-01, WS-03 S1 items)  
2. Consistency (verbs, durations, chrome)  
3. Accessibility blockers on primary path (WS-06)  
4. Visual / interaction craft  
5. Motivation / celebration (WS-10 Nice to Have)  
6. Delight that does not move diligence  

---

## 6. Hard out of scope (all workstreams)

Educational packages / LO wording · EF-001 law · recommendation / ranking / selection · Runtime / SCI / Twin authority · curriculum JSON · until-exam trust claims via UX alone · gamified shame / fake progress · LLM-owned selection UI.

---

## 7. Next artefacts

| Artefact | Role |
|----------|------|
| `PX002_DEPENDENCY_GRAPH.md` | Prerequisites, critical path, quick wins |
| `PX002_IMPLEMENTATION_PLAN.md` | Independently releasable waves |
| `PX002_TEST_STRATEGY.md` | Per-workstream verification |
| `PX002_SUCCESS_METRICS.md` | Version 1 quality metrics |
| `PX002_EXECUTION_REPORT.md` | PX-002 planning exit |

**STOP.** Await Founder approval before implementation of any workstream.

Signed: Product Experience · PX-002 Workstreams · 2026-08-04
