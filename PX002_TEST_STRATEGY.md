# PX-002 — Premium Experience Test Strategy

**Programme:** PX-002 — Premium Experience Workstream Planning  
**Status:** Planning complete — **implementation not authorised**  
**Effective:** 2026-08-04  
**Authority:** `PX002_WORKSTREAMS.md` · `PX002_IMPLEMENTATION_PLAN.md` · `PX001_PREMIUM_BACKLOG.md` · PB-017 evidence patterns · EF-001  

**Rule:** This document defines **what must be verified when waves execute**. PX-002 planning itself runs **no tests**. No PB simulation execution in this planning phase.

---

## 1. Purpose

For every workstream, define regression tests, manual tests, accessibility verification, mobile verification, Founder dogfooding, PB simulation requirements, and release criteria — so implementation phases cannot claim Closed without evidence.

---

## 2. Global verification law

| Law | Rule |
|-----|------|
| Progressive Confidence | Coverage / confidence soft-pass regression → pause PX |
| Educational Content Freeze | No package body / LO assertions in PX tests |
| Selection policy | Tests assert presentation / regenerate handoff — not new ranking |
| Sole runtime | Primary evidence on student shell under SOLE_RUNTIME |
| Honesty | Do not mark educational PASS for infra/UX failures |
| EF-001 | Ambiguous defects → operational review before framework change |

### 2.1 Evidence classes

| Class | Examples |
|-------|----------|
| Automated | pytest presentation/chrome/duration/a11y; CI axe/Lighthouse when added |
| Manual | Checklist dogfood; keyboard path; confirm/finish flows |
| Device | Phone + tablet screenshots/video |
| PB / ops | Cohort simulation notes; force-R1 absence; contention recovery |
| Founder | Multi-week chrome-growth log; scorecard sign-off |

---

## 3. Per-workstream strategy

### WS-01 — Trust & Navigation

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Package-bound Finish/Home/tomorrow title chrome for Learning + Revision; soft-match keyword paths must not drive student Home titles; duration resolver same value/format across Home/Mission/Plan fixtures; Profile prefers active plan `examination_label` when present. |
| **Manual tests** | Multi-day walk Continuity → Memory → Publication; weekend / no-preferred-minutes duration path; Profile vs Plan exam label. |
| **Accessibility** | Title/duration changes must not remove heading structure or primary CTA accessible name. |
| **Mobile** | Chrome honesty visible on narrow viewport; titles do not truncate into wrong day identity. |
| **Founder dogfooding** | Spot-check after Wave 1: “does Home match what I just finished?” |
| **PB simulation** | Re-check soft-pass chrome classes from PB-016/017 audits; no new soft-fail on package-path identity. |
| **Release criteria** | PX-B-001, 002, 035, 054 Closed or waived; 034 if in wave; screenshots + tests filed. |

---

### WS-02 — Session Workflow

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Happy-path completion routing; step indicator matches reachable screens; Finish confirm modal behaviour (or documented exception); interactive controls disabled until ready where applicable. |
| **Manual tests** | `session/*` and `mission/*` paths after **D-SESSION-PATH**; accidental Finish prevented or accepted deliberately; lockout / recovery messaging review. |
| **Accessibility** | Confirm dialog roles; keyboard Finish → confirm → cancel/accept. |
| **Mobile** | Confirm modal usable on phone; Finish not fat-finger exclusive. |
| **Founder dogfooding** | Complete one sitting each authoritative path. |
| **PB simulation** | Not primary; note if path unify changes ops walk scripts. |
| **Release criteria** | Included wave IDs Closed; no dual-path student confusion on declared happy path. |

---

### WS-03 — Revision Experience

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Tip-complete → terminal Revision regenerate automated; Memory/Publication handoff natural enrolment; Revision Q6/checklist presentation variant selection (presentation-only assertions). |
| **Manual tests** | Natural tip-complete without force-R1; Revision sitting language review with Editorial. |
| **Accessibility** | Revision checklist still keyboard-operable; live regions not spammy. |
| **Mobile** | Revision completion chrome readable on phone. |
| **Founder dogfooding** | Complete learning chain → confirm R1 appears. |
| **PB simulation** | **Required** for regenerate class: Rho-equivalent tip-complete cohort (pattern from PB-017); assert zero force-R1 dependence for ordinary path. |
| **Release criteria** | PX-B-005, 007, 004 Closed; force-R1 emergency-only documented. |

---

### WS-04 — Home Experience

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Primary CTA present; Analytics KPI count/rounding helpers; day-zero empty framing not warning-coloured without history; Coach hide/contract if executed. |
| **Manual tests** | Rich-state Home density; day-zero vs returning composition; Journey/History enrichment without dashboard theatre. |
| **Accessibility** | Progressive disclosure controls labelled; heading order preserved. |
| **Mobile** | One-composition Home does not push CTA below fold without scroll cue. |
| **Founder dogfooding** | “Do I know what to do next in <5 seconds?” |
| **PB simulation** | Soft — ensure Home craft does not break package-path chrome tests from WS-01. |
| **Release criteria** | Non-Future IDs in wave Closed; explainability of next action preserved. |

---

### WS-05 — Mobile Experience

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Nav pattern CSS/markup smoke tests where feasible; no desktop-only breakage assertions. |
| **Manual tests** | Full primary path on phone and tablet; wrap vs drawer behaviour per decision. |
| **Accessibility** | Touch targets verified on device (≥44px); focus order with mobile nav. |
| **Mobile** | **Primary evidence class** — Founder phone + tablet screenshots/video pack (PX-B-037). |
| **Founder dogfooding** | Mandatory for PX-B-037; defects filed before PX-B-036 Closed. |
| **PB simulation** | Not required for nav decision; optional responsive capture in later PB. |
| **Release criteria** | Evidence pack filed; PX-B-036/037 Closed or Board-owned defects listed. |

---

### WS-06 — Accessibility

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Expand `tests/presentation/student/test_accessibility.py` (and peers); focus-visible rules; reduced-motion CSS presence; contrast token checks where automatable; CI axe/Lighthouse on primary routes (PX-B-030). |
| **Manual tests** | End-to-end keyboard checklist auth → home → mission → session → reflection → home; modal failure mode without JS. |
| **Accessibility** | **Primary** — WCAG-oriented checks on primary path; one recorded VoiceOver **or** NVDA pass. |
| **Mobile** | Touch-target verification overlaps WS-05. |
| **Founder dogfooding** | Keyboard-only sitting once per Foundation exit. |
| **PB simulation** | Not required; do not weaken educational audits. |
| **Release criteria** | PX-B-023–030 Closed or risk-owned; no silent “WCAG AA certified” marketing without audit scope statement. |

---

### WS-07 — Microcopy & Identity

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Update string-pinned tests for verbs/terminology; identity badges absent on student paths when decided; Help routes render FAQ sections. |
| **Manual tests** | Login/first-touch copy; reflection framing; return-after-gap; exam-horizon pack; Help “how do I…” topics. |
| **Accessibility** | Text alternatives and labels remain meaningful after copy changes. |
| **Mobile** | Long Help content readable; identity lockup not clipped wrongly. |
| **Founder dogfooding** | Identity pack sign-off (**D-EOS**, **D-IDENTITY**). |
| **PB simulation** | Not required for copy; ensure ops scripts not coupled to Alpha strings. |
| **Release criteria** | Editorial + Founder sign-off; Educational Content Freeze held (no LO edits). |

---

### WS-08 — Reliability

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Continue Session error handling / retry paths; first-sitting engagement gate; idempotent regenerate where touched. |
| **Manual tests** | Forced contention (parallel Continue Session); cold provision wait UX; wrong-inventory flash check at campaign join. |
| **Accessibility** | Error/retry messages in accessible live regions or focus move. |
| **Mobile** | Retry CTA tappable; no dead full-screen hang without message. |
| **Founder dogfooding** | Optional under load; rely on PB ops notes. |
| **PB simulation** | **Required pattern** from PB-014…017: document contention rate and recovery success; provision job SLO notes. |
| **Release criteria** | PX-B-006, 008, 009 Closed or waived with ops owner; infra failures not scored as educational fails. |

---

### WS-09 — Performance

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Asset budget smoke where exists; skeleton markup present on key templates. |
| **Manual tests** | Throttle CPU/network dogfood Home/Mission paint; layout jump check. |
| **Accessibility** | Skeletons not announced as real content; avoid assertive live spam. |
| **Mobile** | Perceived performance on phone radio. |
| **Founder dogfooding** | Score perceived performance vs `PREMIUM_QUALITY_ATTRIBUTES.md`. |
| **PB simulation** | Optional timing notes; not educational gate. |
| **Release criteria** | PX-B-031, 032 Closed or Target Conditional with owner. |

---

### WS-10 — Premium Moments

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Motion respects `prefers-reduced-motion`; celebration templates without research chrome; preference persistence. |
| **Manual tests** | Completion moment tone; milestone acknowledgement honesty; diligence cues without streak shame; sign-in brand. |
| **Accessibility** | Motion optional; celebration not sole information channel. |
| **Mobile** | Celebration and prefs usable on phone. |
| **Founder dogfooding** | Emotional tone check — calm professionalism. |
| **PB simulation** | Not required. |
| **Release criteria** | Non-Future IDs Closed; no pass promises / XP. |

---

### WS-11 — Founder Dogfooding

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | N/A (study) — may spawn tickets with tests later. |
| **Manual tests** | Multi-week protocol: log chrome growth, friction, motivation tone. |
| **Accessibility** | Note a11y regressions observed in the wild. |
| **Mobile** | Include at least intermittent phone use in the weeks. |
| **Founder dogfooding** | **Primary deliverable** (PX-B-052). |
| **PB simulation** | Optional companion; does not replace Founder weeks. |
| **Release criteria** | Log filed; residuals classified; PX-B-052 Closed or Board-accepted. |

---

### WS-12 — Premium Certification

| Layer | Requirement |
|-------|-------------|
| **Regression tests** | Aggregate: prior wave suites still green. |
| **Manual tests** | Scorecard walk of required surfaces in `PREMIUM_QUALITY_ATTRIBUTES.md`. |
| **Accessibility** | Cite WS-06 evidence in scorecard. |
| **Mobile** | Cite WS-05 evidence in scorecard. |
| **Founder dogfooding** | Founder signs PASS / Conditional / Fail. |
| **PB simulation** | Cite latest PB confidence posture; UX certification ≠ educational re-cert unless Board requires re-walk. |
| **Release criteria** | PX-B-053 Closed with evidence package; claim language matches Charter § claim posture. |

---

## 4. Wave → minimum test gate (summary)

| Wave | Minimum gate before release |
|------|-----------------------------|
| 1 | Chrome/duration/profile automated + screenshots |
| 2 | Tip-complete/R1 automated + PB-class regenerate check |
| 3 | String/a11y micro tests + decision records |
| 4 | Device evidence pack + keyboard checklist + CI a11y smoke |
| 5 | Home/celebration/Help manual + skeleton smoke |
| 6 | Contention notes + performance Target notes + path decision |
| 7 | Editorial tone sign-off + reduced-motion check |
| 8 | Dogfood log + scorecard signed |

---

## 5. Explicit non-tests (planning phase)

PX-002 planning **does not**:

- Run pytest, axe, Lighthouse, or PB simulations  
- Deploy or dogfood live  
- Modify application test code  

Those actions belong to authorised implementation waves.

Signed: Product Experience · PX-002 Test Strategy · 2026-08-04
