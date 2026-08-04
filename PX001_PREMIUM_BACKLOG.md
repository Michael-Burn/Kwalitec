# PX-001 — Premium Experience Backlog

**Programme:** PX-001 — Premium Experience  
**Phase:** Phase 1 Audit  
**Status:** Definitive Version 1 quality backlog — **implementation not started**  
**Effective:** 2026-08-04  
**Authority:** `PX001_PREMIUM_PROGRAMME.md` · `PX001_PROGRAMME_CHARTER.md` · EF-001 · Educational Content Freeze · PB-017 PASS  

**Rule:** Items below affect Version 1 **product quality** only. Educational package bodies, LOs, EF, recommendations, Twin, and curriculum are out of scope.

---

## How to read

| Field | Meaning |
|-------|---------|
| **ID** | Stable PX-B-### identifier |
| **Category** | Presentation · Workflow · UI/UX · Accessibility · Performance · Reliability · Consistency · Navigation · Visual polish · Microcopy · Technical debt · Testing |
| **Severity** | S1 critical trust/exclusion · S2 material friction · S3 polish/debt |
| **Frequency** | Always · Common · Occasional · Rare · Ops-only |
| **Effort** | S · M · L |
| **Priority** | Quick Win · High Impact · Foundation · Nice to Have · Future |
| **Current status** | Open · Partially mitigated · Re-verify · Parked (out of PX) |

**RO residual mapping:** Recurring RO1–RO15 findings are consolidated into residual **classes** with full ID trails in Evidence. RO1-R1 is **closed** and omitted as open.

---

## A. Residual class register (RO / PB)

### PX-B-001 — Finish / Home tomorrow chrome honesty

| Field | Detail |
|-------|--------|
| **ID** | PX-B-001 |
| **Category** | Presentation · Consistency |
| **Student impact** | After a sitting, Tomorrow Preview / Home chrome can diverge from the package the student just completed — erodes “the product knows where I am” even when the next mission is correct. |
| **Severity** | S1 |
| **Frequency** | Occasional on Learning days (e.g. PB-016 CP-D8 all 5 personas); Common soft-pass on Revision days |
| **Estimated effort** | M |
| **Dependencies** | Package-bound chrome path (RO1R1 pattern); must not change selection logic |
| **Suggested solution** | Bind all student-visible tomorrow / title chrome to package identity (`educational_package_id` / campaign_day), including Memory/Publication Front hinge and revision days; add regression tests for soft-match classes |
| **Evidence** | RO2-R2 · RO3-R2 · RO4-R3 · RO5-R3 · RO6-R3 · RO7-R3 · RO8-R3 · RO9-R3 · RO10-R3 · RO11-R3 · RO12-R3 · RO13-R3 · RO14-R1 · RO15 chrome soft-pass · PB16-R1/R3 · PB17-R2 · `PB016_CONFIDENCE_SCORE_AUDIT.md` · `PB017_CONFIDENCE_SCORE_AUDIT.md` |
| **Current status** | Open |
| **Owner** | Engineering (Presentation / SEI) |
| **Priority** | High Impact |

### PX-B-002 — Home / title soft-match vs package path

| Field | Detail |
|-------|--------|
| **ID** | PX-B-002 |
| **Category** | Presentation · Consistency |
| **Student impact** | Home may show Opening Front / prior-campaign titles while the sitting delivers the true Continuity / Memory / Publication package — student confusion about “what day is this?” |
| **Severity** | S1 |
| **Frequency** | Common across multi-day walks (ops + PB cohorts) |
| **Estimated effort** | M |
| **Dependencies** | PX-B-001; avoid keyword/title inference for student chrome |
| **Suggested solution** | Retire soft title-keyword chrome for student Home; always resolve display title from active package / journey state |
| **Evidence** | RO4-R1 · RO5-R1 · RO14-R1 · RO14-R2 · RO15-R2 · PB16-R4 · RO015_DEPLOYMENT_REPORT Known Limitations |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | High Impact |

### PX-B-003 — Ops expected-day label desync

| Field | Detail |
|-------|--------|
| **ID** | PX-B-003 |
| **Category** | Consistency · Technical debt |
| **Student impact** | Indirect — ops detectors run ahead/behind true package; can leak into student-facing “expected” framing if miswired; confuses support and verification. |
| **Severity** | S2 |
| **Frequency** | Common on Continuity / Memory / Publication multi-day walks |
| **Estimated effort** | M |
| **Dependencies** | Ops harness vs product chrome separation |
| **Suggested solution** | Keep ops labels out of student chrome; align ops detectors to package-path identity; document offset class so audits do not fail package-path PASS |
| **Evidence** | RO6-R1 · RO7-R1 · RO8-R1 · RO9-R1 · RO10-R1 · RO11-R1 · RO12-R1 · RO13-R1 · RO14-R2 · RO15-R2 · PB15-R2 · PB14-R3 |
| **Current status** | Open |
| **Owner** | Engineering + Ops |
| **Priority** | Foundation |

### PX-B-004 — Revision-day Q6 / reading rubric soft-pass

| Field | Detail |
|-------|--------|
| **ID** | PX-B-004 |
| **Category** | Presentation · Microcopy |
| **Student impact** | Revision completion chrome / checklist language still framed for Learning (“immediate next activity”) — feels slightly off after a retrieval day. |
| **Severity** | S3 |
| **Frequency** | Always on campaign Revision sittings in RO/PB cohorts |
| **Estimated effort** | S–M |
| **Dependencies** | Presentation templates only — **not** package educational body changes |
| **Suggested solution** | Revision-specific checklist / Q6 presentation variants that name retrieval next steps without rewriting LO content |
| **Evidence** | RO2-R1 · RO3-R1 · RO4-R2 · RO5-R2 · RO6-R2 · RO7-R2 · RO8-R2 · RO9-R2 · RO10-R2 · RO11-R2 · RO12-R2 · RO13-R2 · RO14-R3 · RO15-R4 · PB17-R1 · all PB*-R revision Q6 rows |
| **Current status** | Open |
| **Owner** | Engineering + Editorial (voice check) |
| **Priority** | Quick Win |

### PX-B-005 — Force-regenerate terminal Revision (R1)

| Field | Detail |
|-------|--------|
| **ID** | PX-B-005 |
| **Category** | Reliability · Workflow |
| **Student impact** | After completing a learning chain, CR-R1 (and class equivalents) may not appear until force-regenerate — student may see empty / wrong next mission until ops intervenes. |
| **Severity** | S1 |
| **Frequency** | Always on PB-017 Rho cohort (5/5); class known from RO15-R3 |
| **Estimated effort** | M–L |
| **Dependencies** | Continuity wiring; must not change educational selection policy — fix regenerate / tip-complete handoff |
| **Suggested solution** | Ensure tip-complete → terminal Revision regenerate is automatic and idempotent; remove student dependence on force-R1 |
| **Evidence** | RO15-R3 · PB17-R3 · `PB017_SIMULATION_REPORT.md` · `knowledge/evidence/releases/PB017/ops/force_r1_*.json` |
| **Current status** | Open |
| **Owner** | Engineering (Continuity / Runtime presentation boundary) |
| **Priority** | High Impact |

### PX-B-006 — First-sitting campaign engagement race

| Field | Detail |
|-------|--------|
| **ID** | PX-B-006 |
| **Category** | Reliability · Workflow |
| **Student impact** | First sitting before chain engagement can briefly deliver wrong inventory (e.g. non-Rho before Rho) — confusing first impression of a new campaign. |
| **Severity** | S2 |
| **Frequency** | Occasional at campaign joins (RO15-R1) |
| **Estimated effort** | M |
| **Dependencies** | Mission regeneration timing; package-path priority |
| **Suggested solution** | Gate first sitting until campaign chain engaged, or suppress premature inventory display |
| **Evidence** | RO15-R1 · `RO015_LIVE_VERIFICATION_REPORT.md` |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Foundation |

### PX-B-007 — Tip-complete continuity / seeded path class

| Field | Detail |
|-------|--------|
| **ID** | PX-B-007 |
| **Category** | Reliability · Workflow |
| **Student impact** | Natural tip-complete enrolments historically blocked Memory Front regeneration; seeded package-path used for verify — real students need the natural path. |
| **Severity** | S1 |
| **Frequency** | Occasional on tip-complete natural enrolments |
| **Estimated effort** | M |
| **Dependencies** | Related to PX-B-005 |
| **Suggested solution** | Confirm RO14 continuity fix holds for natural tip-complete; add automated regression for Memory/Publication handoff |
| **Evidence** | RO14-R4 · `RO014_RELEASE_DECISION.md` · RO014 deploy notes (`4ff8c95…`) |
| **Current status** | Partially mitigated — re-verify |
| **Owner** | Engineering |
| **Priority** | High Impact |

### PX-B-008 — Continue Session / LIVE contention recovery

| Field | Detail |
|-------|--------|
| **ID** | PX-B-008 |
| **Category** | Reliability · Error handling |
| **Student impact** | Under load, Continue Session can 500; student must abandon and re-provision — feels broken even when education is fine. |
| **Severity** | S2 |
| **Frequency** | Occasional under parallel load (PB-014…PB-017 ops) |
| **Estimated effort** | M |
| **Dependencies** | Infra / Render; student-facing error dignity |
| **Suggested solution** | Resilient Continue Session; calm retry UX with clear next step; never score as educational failure |
| **Evidence** | `PB016_SIMULATION_REPORT.md` · `PB014_SIMULATION_REPORT.md` · `PB017_SIMULATION_REPORT.md` |
| **Current status** | Open |
| **Owner** | Engineering + Ops |
| **Priority** | Foundation |

### PX-B-009 — Render / API job latency on student-path ops

| Field | Detail |
|-------|--------|
| **ID** | PX-B-009 |
| **Category** | Performance · Reliability |
| **Student impact** | Long waits on create-user / seed / backdate / force-R1 feel like product hangs; cold starts amplify. |
| **Severity** | S2 |
| **Frequency** | Common in PB verification; possible for support-provisioned students |
| **Estimated effort** | M |
| **Dependencies** | Hosting; loading craft (PX-B-032) |
| **Suggested solution** | Perceived-performance craft (skeletons, progress honesty); trim cold-path work; ops SLOs for provision jobs |
| **Evidence** | PB014–PB017 simulation infra notes · RP-001.4 perceived performance score 3 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Foundation |

---

## B. Presentation

### PX-B-010 — Home composition density

| Field | Detail |
|-------|--------|
| **ID** | PX-B-010 |
| **Category** | Presentation · Visual polish · UI/UX |
| **Student impact** | Home can stack many conditional blocks before the primary CTA — cognitive load on the one screen that should say “do this next.” |
| **Severity** | S2 |
| **Frequency** | Common on rich states |
| **Estimated effort** | M |
| **Dependencies** | Protect explainability; compress, do not delete honesty |
| **Suggested solution** | One-composition hierarchy: heading, duration, reason, primary CTA; progressive disclosure for secondary |
| **Evidence** | PX-003 N2 · `PREMIUM_BACKLOG.md` B1 · Epic 3 Stream C |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | High Impact |

### PX-B-011 — Analytics KPI density and false precision

| Field | Detail |
|-------|--------|
| **ID** | PX-B-011 |
| **Category** | Presentation · Visual polish |
| **Student impact** | Dense KPI rows and one-decimal hour figures read as false precision / dashboard theatre. |
| **Severity** | S3 |
| **Frequency** | Always on Analytics |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | ≤4 KPIs per row; round estimated hours honestly |
| **Evidence** | PX-003 N3 · PX-001 T2-3 · house UX density rules |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-012 — Day-zero Analytics “failure” framing

| Field | Detail |
|-------|--------|
| **ID** | PX-B-012 |
| **Category** | Presentation · Microcopy · Emotional |
| **Student impact** | Zero streak / backlog in warning colours without new-account framing feels like early failure. |
| **Severity** | S2 |
| **Frequency** | Always for new accounts visiting Analytics |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Neutral / encouraging empty framing until history warrants improvement language |
| **Evidence** | PX-003 N4 · `PREMIUM_BACKLOG.md` A5 |
| **Current status** | Open |
| **Owner** | Engineering + Editorial |
| **Priority** | Quick Win |

### PX-B-013 — Journey / History secondary craft

| Field | Detail |
|-------|--------|
| **ID** | PX-B-013 |
| **Category** | Presentation · Visual polish |
| **Student impact** | Populated Journey/History are calm but thin vs Mission — weaker long-term orientation. |
| **Severity** | S3 |
| **Frequency** | Always when history exists |
| **Estimated effort** | M |
| **Dependencies** | Presentation only |
| **Suggested solution** | Enrich with duration / why-next without dashboard theatre |
| **Evidence** | PX-003 N5 · `PREMIUM_BACKLOG.md` E1 |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | Nice to Have |

---

## C. Workflow

### PX-B-014 — Dual study-session mental models

| Field | Detail |
|-------|--------|
| **ID** | PX-B-014 |
| **Category** | Workflow · Consistency · UI/UX |
| **Student impact** | `session/*` linear flow vs `mission/*` flow differ in verbs, steps, and completion — “how a session ends” may not transfer. |
| **Severity** | S2 |
| **Frequency** | Occasional if both paths reached |
| **Estimated effort** | L (split) |
| **Dependencies** | Founder decision on authoritative happy path; sole-runtime claims |
| **Suggested solution** | Declare one student-authoritative completion path; align or hide the other; unify reflection/summary naming |
| **Evidence** | PX-003 N15 |
| **Current status** | Open |
| **Owner** | Founder + Engineering |
| **Priority** | Foundation |

### PX-B-015 — Phantom Complete step vs happy path

| Field | Detail |
|-------|--------|
| **ID** | PX-B-015 |
| **Category** | Workflow · UI/UX |
| **Student impact** | Step chrome advertises Complete; happy path returns Home without that screen — feels unfinished or inaccurate. |
| **Severity** | S3 |
| **Frequency** | Always on `session/*` happy path |
| **Estimated effort** | S |
| **Dependencies** | Product decision: show `complete.html` or drop step |
| **Suggested solution** | Route through crafted complete screen **or** remove phantom step from indicator |
| **Evidence** | PX-003 N16 · `PREMIUM_BACKLOG.md` B4 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-016 — Finish Study Session without confirmation

| Field | Detail |
|-------|--------|
| **ID** | PX-B-016 |
| **Category** | Workflow · UI/UX |
| **Student impact** | Accidental tap/Enter ends session with no confirm — inconsistent with plan delete / restore confirm modal. |
| **Severity** | S2 |
| **Frequency** | Always available during session |
| **Estimated effort** | S |
| **Dependencies** | Shared confirm modal |
| **Suggested solution** | Use shared confirm modal, or deliberate product note that Finish is low-stakes |
| **Evidence** | PX-003 N14 · `mission/session.html` |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-017 — Password recovery / lockout posture

| Field | Detail |
|-------|--------|
| **ID** | PX-B-017 |
| **Category** | Workflow · Reliability · Microcopy |
| **Student impact** | No self-service reset; failed-login lockout messaging absent — external cohorts stuck without coordinator. |
| **Severity** | S2 |
| **Frequency** | Rare path, high impact when hit |
| **Estimated effort** | S–M (copy) / L (full auth) |
| **Dependencies** | Ops ownership of backend; PX owns copy/UX |
| **Suggested solution** | Honest recovery messaging + operational SLA; optional later rate-limit UX |
| **Evidence** | PX-003 N9 · `PREMIUM_BACKLOG.md` E4 |
| **Current status** | Open |
| **Owner** | Product + Ops |
| **Priority** | Foundation |

---

## D. UI / UX & Visual polish

### PX-B-018 — Restrained motion system

| Field | Detail |
|-------|--------|
| **ID** | PX-B-018 |
| **Category** | Visual polish · UI/UX · Accessibility |
| **Student impact** | Motion is uneven across shells; premium presence lacks 2–3 intentional house patterns. |
| **Severity** | S3 |
| **Frequency** | Always |
| **Estimated effort** | M |
| **Dependencies** | `prefers-reduced-motion` coverage (PX-B-027) |
| **Suggested solution** | Define 2–3 house motions for hierarchy/presence; honour reduced motion |
| **Evidence** | `PREMIUM_BACKLOG.md` B7 · `PREMIUM_QUALITY_ATTRIBUTES.md` IX-5 |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | Nice to Have |

### PX-B-019 — Icon-only control visual consistency

| Field | Detail |
|-------|--------|
| **ID** | PX-B-019 |
| **Category** | Visual polish · Accessibility |
| **Student impact** | Appearance switcher, help triggers, compact nav icons vary in stroke/size — less polished, harder to tap. |
| **Severity** | S3 |
| **Frequency** | Always |
| **Estimated effort** | S |
| **Dependencies** | Touch-target token (PX-B-025) |
| **Suggested solution** | Shared stroke/size language for icon-only controls |
| **Evidence** | PX-003 N11 · `PREMIUM_BACKLOG.md` B8 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-020 — Error-page Reference ID colour / guidance

| Field | Detail |
|-------|--------|
| **ID** | PX-B-020 |
| **Category** | Visual polish · Microcopy |
| **Student impact** | Off-palette Reference ID colour; weak guidance on what to do with it. |
| **Severity** | S3 |
| **Frequency** | On every error |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Tokenised muted colour + one sentence of support guidance |
| **Evidence** | PX-001 T2-7 |
| **Current status** | Open — re-verify |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-021 — Sign-in brand redundancy

| Field | Detail |
|-------|--------|
| **ID** | PX-B-021 |
| **Category** | Visual polish · Microcopy |
| **Student impact** | First impression can feel unconfident from repeated brand naming. |
| **Severity** | S3 |
| **Frequency** | Always at login |
| **Estimated effort** | S |
| **Dependencies** | Brand decision |
| **Suggested solution** | Single lockup-led hero; coordinator mention once |
| **Evidence** | PX-001 T2-5 |
| **Current status** | Open — re-verify |
| **Owner** | Product Experience |
| **Priority** | Nice to Have |

### PX-B-022 — Honest session-complete celebration craft

| Field | Detail |
|-------|--------|
| **ID** | PX-B-022 |
| **Category** | UI/UX · Visual polish · Microcopy |
| **Student impact** | Best completion screen diluted by Internal Alpha / research chrome; celebration under-crafted elsewhere. |
| **Severity** | S2 |
| **Frequency** | Always after mission session |
| **Estimated effort** | M |
| **Dependencies** | Pilot feedback strategy decision |
| **Suggested solution** | Relocate instrumentation; warm proportional completion moment |
| **Evidence** | PX-003 N18 · `PREMIUM_BACKLOG.md` D1 |
| **Current status** | Open |
| **Owner** | Product Experience + Editorial |
| **Priority** | High Impact |

---

## E. Accessibility

### PX-B-023 — Confirm modal resilience if JS/Bootstrap fails

| Field | Detail |
|-------|--------|
| **ID** | PX-B-023 |
| **Category** | Accessibility · Reliability |
| **Student impact** | Destructive actions can become inert with no visible failure if Bootstrap missing. |
| **Severity** | S2 |
| **Frequency** | Rare (JS failure) |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Explicit dialog roles in markup + visible failure if modal unavailable |
| **Evidence** | PX-003 N6 · `PREMIUM_BACKLOG.md` C1 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Foundation |

### PX-B-024 — Session timer live region

| Field | Detail |
|-------|--------|
| **ID** | PX-B-024 |
| **Category** | Accessibility |
| **Student impact** | Screen-reader users get no periodic elapsed-time cue during sessions. |
| **Severity** | S3 |
| **Frequency** | Always during timed session |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Appropriate `aria-live` / `role="status"` pattern (polite, not every second spam) |
| **Evidence** | PX-003 N17 · accessibility review |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-025 — Touch-target token application

| Field | Detail |
|-------|--------|
| **ID** | PX-B-025 |
| **Category** | Accessibility · Navigation · Mobile |
| **Student impact** | Icon-only and nav controls under 44px — mis-taps on phone. |
| **Severity** | S2 |
| **Frequency** | Always on mobile |
| **Estimated effort** | S–M |
| **Dependencies** | None |
| **Suggested solution** | Apply `--touch-target-min` to appearance switcher, ctx-help, student nav |
| **Evidence** | PX-003 N11 · accessibility review §6 · `PREMIUM_BACKLOG.md` C3 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | High Impact |

### PX-B-026 — Focus-visible discipline on buttons

| Field | Detail |
|-------|--------|
| **ID** | PX-B-026 |
| **Category** | Accessibility · UI/UX |
| **Student impact** | Mouse click triggers keyboard-like transform styles — muddies focus signal. |
| **Severity** | S3 |
| **Frequency** | Always |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Reserve hover-like transforms for `:focus-visible` |
| **Evidence** | PX-003 N10 · `app.css` `:focus` rules |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-027 — Student-shell reduced-motion completeness

| Field | Detail |
|-------|--------|
| **ID** | PX-B-027 |
| **Category** | Accessibility |
| **Student impact** | Canonical student shell misses some transitions under `prefers-reduced-motion`. |
| **Severity** | S3 |
| **Frequency** | Always for reduced-motion users |
| **Estimated effort** | S |
| **Dependencies** | PX-B-018 |
| **Suggested solution** | Align `student.css` coverage with universal rule in `app.css` |
| **Evidence** | PX-003 accessibility review §7 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-028 — Sidebar section-label contrast

| Field | Detail |
|-------|--------|
| **ID** | PX-B-028 |
| **Category** | Accessibility · Navigation |
| **Student impact** | Section labels on dark sidebar remain low-contrast for low-vision users on Settings/Help/Plan shells. |
| **Severity** | S2 |
| **Frequency** | Always on legacy chrome screens |
| **Estimated effort** | S |
| **Dependencies** | None |
| **Suggested solution** | Raise label opacity/token to AA; verify with contrast tool |
| **Evidence** | PX-003 B6 (contrast) · `app.css` `.nav-section-label` still ~0.5 opacity |
| **Current status** | Open — partially improved historically; re-verify AA |
| **Owner** | Engineering |
| **Priority** | High Impact |

### PX-B-029 — Keyboard audit of primary student path

| Field | Detail |
|-------|--------|
| **ID** | PX-B-029 |
| **Category** | Accessibility · Testing |
| **Student impact** | Unknown residual keyboard traps/gaps on auth → home → mission → session → reflection → home. |
| **Severity** | S2 |
| **Frequency** | Always for keyboard users |
| **Estimated effort** | M |
| **Dependencies** | Welcome/drawer fixes already partially present |
| **Suggested solution** | End-to-end keyboard dogfood + checklist; close gaps |
| **Evidence** | `PREMIUM_BACKLOG.md` C5 · PX-003 a11y verification gap |
| **Current status** | Open |
| **Owner** | Engineering + Product Experience |
| **Priority** | Foundation |

### PX-B-030 — Automated accessibility / AT verification gap

| Field | Detail |
|-------|--------|
| **ID** | PX-B-030 |
| **Category** | Testing · Accessibility |
| **Student impact** | Product cannot honestly claim accessibility readiness; defects under-counted. |
| **Severity** | S2 |
| **Frequency** | Process always |
| **Estimated effort** | M |
| **Dependencies** | CI capacity |
| **Suggested solution** | axe/Lighthouse in CI on primary routes + one recorded VoiceOver/NVDA pass |
| **Evidence** | PX-003 accessibility “Verification gap” · `tests/presentation/student/test_accessibility.py` narrow |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Foundation |

---

## F. Performance & loading

### PX-B-031 — Perceived performance on SSR student paths

| Field | Detail |
|-------|--------|
| **ID** | PX-B-031 |
| **Category** | Performance |
| **Student impact** | Home/Mission can feel slow; Alpha scorecard rated perceived performance 3. |
| **Severity** | S2 |
| **Frequency** | Common |
| **Estimated effort** | M |
| **Dependencies** | Asset hygiene |
| **Suggested solution** | Measure + trim student-path weight; prioritise Home/Mission paint |
| **Evidence** | RP-001.4 · `PREMIUM_BACKLOG.md` C6 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Foundation |

### PX-B-032 — Loading / skeleton coherence

| Field | Detail |
|-------|--------|
| **ID** | PX-B-032 |
| **Category** | Performance · Presentation |
| **Student impact** | Slow paths risk blank paints / layout jump — not premium. |
| **Severity** | S2 |
| **Frequency** | Occasional |
| **Estimated effort** | M |
| **Dependencies** | PX-B-009 |
| **Suggested solution** | Crafted skeletons on Home / Mission / Plan transitions |
| **Evidence** | RP-001.4 loading Conditional · `PREMIUM_BACKLOG.md` B5 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | High Impact |

### PX-B-033 — Interactive readiness (no dead premature controls)

| Field | Detail |
|-------|--------|
| **ID** | PX-B-033 |
| **Category** | Performance · UI/UX |
| **Student impact** | Controls that look ready before they work destroy trust. |
| **Severity** | S2 |
| **Frequency** | Occasional |
| **Estimated effort** | M |
| **Dependencies** | Feature inventory |
| **Suggested solution** | Audit; classify Hidden / Coming Soon; disable until ready |
| **Evidence** | Epic 3 Stream C · `PREMIUM_BACKLOG.md` C7 |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | Foundation |

---

## G. Consistency & Navigation

### PX-B-034 — Unify primary study-start verbs

| Field | Detail |
|-------|--------|
| **ID** | PX-B-034 |
| **Category** | Consistency · Microcopy · Navigation |
| **Student impact** | “Start Session / Start Mission / Begin Session / Resume Study Session…” — same act, different words. |
| **Severity** | S2 |
| **Frequency** | Always across Home/Mission/Session/Revision |
| **Estimated effort** | M |
| **Dependencies** | Terminology matrix; test updates |
| **Suggested solution** | One canonical verb family for start / continue / resume |
| **Evidence** | PX-003 N1 · `PREMIUM_BACKLOG.md` A2 |
| **Current status** | Open |
| **Owner** | Editorial + Engineering |
| **Priority** | High Impact |

### PX-B-035 — Duration label / number consistency

| Field | Detail |
|-------|--------|
| **ID** | PX-B-035 |
| **Category** | Consistency · Presentation |
| **Student impact** | Same day’s study time can still diverge across Home / Mission / Plan (weekday vs weekend path; template fallbacks) — classic trust failure. |
| **Severity** | S1 |
| **Frequency** | Occasional (esp. weekends / no preferred minutes) |
| **Estimated effort** | M |
| **Dependencies** | Product decision on authoritative duration source; PX may unify **labels** after decision — engine redesign parked if deeper |
| **Suggested solution** | One resolver + one format everywhere; explain topic vs session minutes when both shown |
| **Evidence** | PX-003 B3 · PX-001 T1-2 · `PREMIUM_BACKLOG.md` X5 (parked engine) |
| **Current status** | Open |
| **Owner** | Founder (source decision) + Engineering |
| **Priority** | High Impact |

### PX-B-036 — Mobile navigation pattern decision

| Field | Detail |
|-------|--------|
| **ID** | PX-B-036 |
| **Category** | Navigation · Mobile · Consistency |
| **Student impact** | Student top nav wraps; legacy shells may drawer — inconsistent phone experience. |
| **Severity** | S2 |
| **Frequency** | Always on mobile |
| **Estimated effort** | M |
| **Dependencies** | Sole runtime; live mobile review (PX-B-037) |
| **Suggested solution** | One deliberate mobile nav pattern for canonical student shell |
| **Evidence** | PX-003 N12 · `PREMIUM_BACKLOG.md` B6 |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | High Impact |

### PX-B-037 — Live mobile / tablet rendering evidence

| Field | Detail |
|-------|--------|
| **ID** | PX-B-037 |
| **Category** | Testing · Navigation · Mobile |
| **Student impact** | Unknown real-device breakage; cannot certify mobile premium. |
| **Severity** | S1 |
| **Frequency** | Process always |
| **Estimated effort** | M (study) |
| **Dependencies** | Device/emulator access |
| **Suggested solution** | Founder dogfood on phone + tablet; file screenshots; close concrete defects |
| **Evidence** | PX-003 B7 · historical zero live mobile evidence |
| **Current status** | Open |
| **Owner** | Founder + Product Experience |
| **Priority** | Foundation |

---

## H. Microcopy

### PX-B-038 — Retire or decide “Education Operating System” first-touch framing

| Field | Detail |
|-------|--------|
| **ID** | PX-B-038 |
| **Category** | Microcopy |
| **Student impact** | First-touch jargon may alienate; or be intentional brand — needs one decision, then consistency. |
| **Severity** | S3 |
| **Frequency** | Always |
| **Estimated effort** | S |
| **Dependencies** | Product decision |
| **Suggested solution** | Single-source descriptor decision; apply across login, meta, sidebar, manifest |
| **Evidence** | PX-003 N7 · `brand_identity.py` · `version.py` |
| **Current status** | Open |
| **Owner** | Founder |
| **Priority** | Quick Win |

### PX-B-039 — Internal Alpha / pilot identity → lasting student identity

| Field | Detail |
|-------|--------|
| **ID** | PX-B-039 |
| **Category** | Microcopy · Consistency |
| **Student impact** | “Internal Alpha · Founding Cohort” and Internal Alpha feedback chrome read as developer programme on student paths. |
| **Severity** | S2 |
| **Frequency** | Always while flags/copy remain |
| **Estimated effort** | S–M |
| **Dependencies** | Product decision on badge/copy; PX-B-022 |
| **Suggested solution** | Student-grade identity for Version 1; relocate research chrome |
| **Evidence** | PX-003 N8 · N18 · login/help/settings templates · `PREMIUM_BACKLOG.md` E3 |
| **Current status** | Open |
| **Owner** | Founder + Editorial |
| **Priority** | High Impact |

### PX-B-040 — Student-grade session terminology

| Field | Detail |
|-------|--------|
| **ID** | PX-B-040 |
| **Category** | Microcopy |
| **Student impact** | Eyebrows like “Practice Outcome Capture” read as internal tooling. |
| **Severity** | S3 |
| **Frequency** | Always on practice outcome screen |
| **Estimated effort** | S–M |
| **Dependencies** | Test-pinned names may need coordinated updates |
| **Suggested solution** | Replace with student language |
| **Evidence** | PX-003 N13 · `session_practice_outcome.html` |
| **Current status** | Open |
| **Owner** | Engineering + Editorial |
| **Priority** | Quick Win |

### PX-B-041 — Reflection value framing at point of use

| Field | Detail |
|-------|--------|
| **ID** | PX-B-041 |
| **Category** | Microcopy · Workflow |
| **Student impact** | Reflection value may still be under-explained at the moment of use (historical lowest PR-001 category). |
| **Severity** | S2 |
| **Frequency** | Always on reflection |
| **Estimated effort** | S |
| **Dependencies** | Honesty with persistence (B1 closed — keep promise true) |
| **Suggested solution** | Reuse proven onboarding / Session Feedback tone on Reflection |
| **Evidence** | PX-001 T1-3 · `PREMIUM_BACKLOG.md` A1 |
| **Current status** | Re-verify (promise path fixed; framing may still need craft) |
| **Owner** | Editorial + Engineering |
| **Priority** | Quick Win |

### PX-B-042 — Help Centre as real student help

| Field | Detail |
|-------|--------|
| **ID** | PX-B-042 |
| **Category** | Microcopy · Workflow |
| **Student impact** | Help that is release theatre cannot answer “how do I…” — support load and confusion. |
| **Severity** | S2 |
| **Frequency** | When students seek help |
| **Estimated effort** | M |
| **Dependencies** | Content authoring (non-educational-package FAQ) |
| **Suggested solution** | FAQ topics: plan, readiness meaning, exam change, deferral; reinforce contextual help |
| **Evidence** | PX-001 T2-2 · `PREMIUM_BACKLOG.md` A6 |
| **Current status** | Open — re-verify current help.html |
| **Owner** | Product Experience + Editorial |
| **Priority** | High Impact |

### PX-B-043 — Technical / build metadata on student paths

| Field | Detail |
|-------|--------|
| **ID** | PX-B-043 |
| **Category** | Microcopy · Technical debt |
| **Student impact** | Commit/env/raw IDs / engine labels undermine premium calm. |
| **Severity** | S2 |
| **Frequency** | On Settings / diagnostic surfaces |
| **Estimated effort** | S |
| **Dependencies** | Support disclosure pattern |
| **Suggested solution** | Collapse to support-only diagnostic disclosure |
| **Evidence** | PX-001 T2-1 · PX-003 B10 class · settings templates |
| **Current status** | Partially mitigated — re-verify twin/status labels |
| **Owner** | Engineering |
| **Priority** | Quick Win |

### PX-B-044 — Calm return-after-gap copy system

| Field | Detail |
|-------|--------|
| **ID** | PX-B-044 |
| **Category** | Microcopy · Workflow |
| **Student impact** | Gaps risk guilt language; premium product welcomes back with one next action. |
| **Severity** | S2 |
| **Frequency** | Occasional |
| **Estimated effort** | M |
| **Dependencies** | Must not invent catch-up recommendations |
| **Suggested solution** | Welcome-back microcopy patterns; present authorised next action only |
| **Evidence** | `PREMIUM_BACKLOG.md` A8 · quality attributes EJ-5 |
| **Current status** | Open |
| **Owner** | Editorial |
| **Priority** | Nice to Have |

### PX-B-045 — Exam-approach tone pack

| Field | Detail |
|-------|--------|
| **ID** | PX-B-045 |
| **Category** | Microcopy |
| **Student impact** | Near-exam chrome without calm framing risks panic theatre. |
| **Severity** | S3 |
| **Frequency** | Near exam horizon |
| **Estimated effort** | M |
| **Dependencies** | Editorial; no strategy engine change |
| **Suggested solution** | Calm Home/Mission/Revision chrome pack |
| **Evidence** | `PREMIUM_BACKLOG.md` A9 |
| **Current status** | Open |
| **Owner** | Editorial |
| **Priority** | Nice to Have |

---

## I. Motivation / celebration / personalisation (presentation only)

### PX-B-046 — Continuity Front milestone acknowledgements

| Field | Detail |
|-------|--------|
| **ID** | PX-B-046 |
| **Category** | UI/UX · Microcopy |
| **Student impact** | Completing a certified arc day with no acknowledgement feels flat; over-claiming would harm trust. |
| **Severity** | S3 |
| **Frequency** | At arc milestones |
| **Estimated effort** | M |
| **Dependencies** | Editorial sign-off; never imply until-exam pass |
| **Suggested solution** | Light honest acknowledgement of completed certified arcs |
| **Evidence** | `PREMIUM_BACKLOG.md` D2 |
| **Current status** | Open |
| **Owner** | Editorial + Engineering |
| **Priority** | Nice to Have |

### PX-B-047 — Diligence motivation without streak punishment

| Field | Detail |
|-------|--------|
| **ID** | PX-B-047 |
| **Category** | UI/UX · Microcopy |
| **Student impact** | Motivation that punishes gaps collapses narrative; calm reinforcement supports diligence. |
| **Severity** | S3 |
| **Frequency** | Daily |
| **Estimated effort** | M |
| **Dependencies** | No leaderboards / XP |
| **Suggested solution** | Optional gentle reinforcement; gaps do not destroy narrative |
| **Evidence** | `PREMIUM_BACKLOG.md` D3 · quality attributes MO-* |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | Nice to Have |

### PX-B-048 — New-account / returning / exam-horizon presentation density

| Field | Detail |
|-------|--------|
| **ID** | PX-B-048 |
| **Category** | UI/UX · Presentation |
| **Student impact** | Same chrome density for day-zero and rich history; returning students lack “where you left off” craft. |
| **Severity** | S3 |
| **Frequency** | Common |
| **Estimated effort** | M |
| **Dependencies** | Must not re-select missions |
| **Suggested solution** | Contextual density + continuity presentation of authorised next action |
| **Evidence** | `PREMIUM_BACKLOG.md` D4–D6 |
| **Current status** | Open |
| **Owner** | Product Experience |
| **Priority** | Nice to Have |

### PX-B-049 — Preference clarity and stickiness UI

| Field | Detail |
|-------|--------|
| **ID** | PX-B-049 |
| **Category** | UI/UX · Workflow |
| **Student impact** | Preferences that are obscure or non-sticky frustrate returning students. |
| **Severity** | S3 |
| **Frequency** | Occasional |
| **Estimated effort** | S–M |
| **Dependencies** | None |
| **Suggested solution** | Obvious durable appearance / notification / study preferences |
| **Evidence** | `PREMIUM_BACKLOG.md` D7 |
| **Current status** | Open |
| **Owner** | Engineering |
| **Priority** | Nice to Have |

---

## J. Technical debt (student-affecting) & Testing

### PX-B-050 — Coach panel information contract

| Field | Detail |
|-------|--------|
| **ID** | PX-B-050 |
| **Category** | Technical debt · UI/UX |
| **Student impact** | Coach that paraphrases Mission wastes attention and confuses “why two panels?” |
| **Severity** | S3 |
| **Frequency** | When Coach shown |
| **Estimated effort** | M |
| **Dependencies** | Product decision — presentation only; no new recommendation logic |
| **Suggested solution** | Distinct evidence contract or hide until met |
| **Evidence** | PX-001 T2-8 |
| **Current status** | Open — re-verify |
| **Owner** | Founder + Product Experience |
| **Priority** | Future |

### PX-B-051 — Icon sourcing centralisation

| Field | Detail |
|-------|--------|
| **ID** | PX-B-051 |
| **Category** | Technical debt · Visual polish |
| **Student impact** | Drift risk over Version 1 maintenance — indirect. |
| **Severity** | S3 |
| **Frequency** | Always (maintainability) |
| **Estimated effort** | M |
| **Dependencies** | None |
| **Suggested solution** | Shared icon macro/library migration |
| **Evidence** | PX-001 T2-10 |
| **Current status** | Partially mitigated historically — re-verify |
| **Owner** | Engineering |
| **Priority** | Future |

### PX-B-052 — Multi-week fatigue / chrome growth audit

| Field | Detail |
|-------|--------|
| **ID** | PX-B-052 |
| **Category** | Testing · Presentation |
| **Student impact** | Chrome may grow noisier with use — long-horizon diligence risk. |
| **Severity** | S3 |
| **Frequency** | Multi-week |
| **Estimated effort** | M (study) |
| **Dependencies** | Educational completion held |
| **Suggested solution** | Founder dogfood across weeks; log chrome growth |
| **Evidence** | `PREMIUM_BACKLOG.md` E2 |
| **Current status** | Open |
| **Owner** | Founder |
| **Priority** | Foundation |

### PX-B-053 — Full Premium Experience scorecard certification

| Field | Detail |
|-------|--------|
| **ID** | PX-B-053 |
| **Category** | Testing |
| **Student impact** | Without rescore, “premium” remains aspiration. |
| **Severity** | S2 |
| **Frequency** | Programme exit |
| **Estimated effort** | M |
| **Dependencies** | Prior PX-B closures |
| **Suggested solution** | Re-score vs `PREMIUM_QUALITY_ATTRIBUTES.md`; PASS/Conditional/Fail with evidence |
| **Evidence** | Charter success definition · RP-001.4 baseline |
| **Current status** | Open |
| **Owner** | Product Experience + Founder |
| **Priority** | Foundation |

### PX-B-054 — Profile examination_label consistency

| Field | Detail |
|-------|--------|
| **ID** | PX-B-054 |
| **Category** | Consistency · Reliability |
| **Student impact** | Profile “Not set” while Plan shows exam destroys trust. |
| **Severity** | S1 |
| **Frequency** | Occasional (projection path) |
| **Estimated effort** | S–M |
| **Dependencies** | Presentation projection — not Twin authority redesign |
| **Suggested solution** | Prefer active plan exam label on Profile; never hardcode empty when plan exists |
| **Evidence** | PX-003 B2 · `student/profile.html` still uses `examination_label or 'Not set'` |
| **Current status** | Open — re-verify (home paths improved; profile risk remains) |
| **Owner** | Engineering |
| **Priority** | High Impact |

---

## K. Parked (out of PX — do not pull without separate programme)

| ID | Item | Why parked |
|----|------|------------|
| PX-X-01 | Recommendation / ranking / selection redesign | Charter hard out |
| PX-X-02 | Educational Framework changes | EF-001 |
| PX-X-03 | Runtime / SCI / Twin authority redesign | Architecture |
| PX-X-04 | Dual navigation stack as product strategy | Sole-runtime only |
| PX-X-05 | Duration engine redesign beyond label unify | Separate programme if needed after PX-B-035 decision |
| PX-X-06 | New exam-body expansion as engagement | EP / curriculum |
| PX-X-07 | Gamified leaderboards / pass-rate marketing UX | Honesty |
| PX-X-08 | LLM-owned educational selection UI | Rejected architecture |
| PX-X-09 | New educational packages / LO wording | Educational Content Freeze |

---

## Prioritisation groups

### Quick Wins

PX-B-004 · PX-B-011 · PX-B-012 · PX-B-015 · PX-B-016 · PX-B-019 · PX-B-020 · PX-B-024 · PX-B-026 · PX-B-027 · PX-B-038 · PX-B-040 · PX-B-041 · PX-B-043

### High Impact

PX-B-001 · PX-B-002 · PX-B-005 · PX-B-007 · PX-B-010 · PX-B-022 · PX-B-025 · PX-B-028 · PX-B-032 · PX-B-034 · PX-B-035 · PX-B-036 · PX-B-039 · PX-B-042 · PX-B-054

### Foundation

PX-B-003 · PX-B-006 · PX-B-008 · PX-B-009 · PX-B-014 · PX-B-017 · PX-B-023 · PX-B-029 · PX-B-030 · PX-B-031 · PX-B-033 · PX-B-037 · PX-B-052 · PX-B-053

### Nice to Have

PX-B-013 · PX-B-018 · PX-B-021 · PX-B-044 · PX-B-045 · PX-B-046 · PX-B-047 · PX-B-048 · PX-B-049

### Future

PX-B-050 · PX-B-051 · PX-X-* (parked)

---

## Recommended execution order

See `PX001_EXECUTION_PLAN.md` for wave mapping. Summary:

1. **Trust chrome & continuity** — PX-B-001, 002, 005, 007, 035, 054  
2. **Identity & microcopy Quick Wins** — PX-B-038, 039, 034, 040, 041, 004, 012, 043  
3. **Mobile & accessibility foundation** — PX-B-037, 025, 028, 029, 030, 036  
4. **Home / loading / celebration craft** — PX-B-010, 032, 022, 015, 016  
5. **Reliability & performance** — PX-B-008, 009, 031, 023, 006  
6. **Motivation / long-horizon** — PX-B-044–049, 052  
7. **Certification** — PX-B-053  

---

## Closed / not open (audit honesty)

| Item | Status |
|------|--------|
| RO1-R1 tomorrow chrome class-1 | **Closed** (`RO1R1_*`) |
| Reflection note persistence promise | **Closed** (code path present) |
| Onboarding gate under SOLE_RUNTIME | **Closed** |
| Legacy `/settings/` sole-runtime redirect | **Closed** |
| Welcome modal / drawer basic focus + `aria-expanded` | **Partially closed** — keep PX-B-029 for full path audit |

---

Signed: Product Experience · PX-001 Premium Backlog · Phase 1 Audit · 2026-08-04
