# PX-002 — Premium Experience Implementation Plan

**Programme:** PX-002 — Premium Experience Workstream Planning  
**Status:** Planning complete — **implementation not authorised**  
**Effective:** 2026-08-04  
**Authority:** `PX002_WORKSTREAMS.md` · `PX002_DEPENDENCY_GRAPH.md` · `PX001_EXECUTION_PLAN.md` · `PX001_PREMIUM_BACKLOG.md` · EF-001 · Educational Content Freeze  

**Rule:** Waves are **independently releasable**. Each wave may ship under sole-runtime student shell without waiting for later waves. No wave reopens Educational Content Freeze, EF-001, recommendations, Twin, Runtime authority, or curriculum.

---

## 1. Purpose

Divide Version 1 Premium Experience into eight implementation waves plus a Future lane. Aligns with `PX001_EXECUTION_PLAN.md` phases while making each release shippable and rollback-safe.

| PX-001 phase (illustrative) | Waves here |
|-----------------------------|------------|
| Implementation Phase 1 (trust · identity · QW) | Wave 1–3 |
| Phase 2 (mobile · a11y · Home · loading) | Wave 4–5 |
| Phase 3 (reliability · performance · workflow) | Wave 6 |
| Phase 4 (motivation · long-horizon · certification) | Wave 7–8 |
| Future capacity | Future lane |

---

## 2. Global wave rules

1. **Education first** — Progressive Confidence / chrome regression → pause wave.  
2. **EF-001** — complete operational review only if classification ambiguous; expect AW/PI/EC under existing law.  
3. **Independently releasable** — wave exit does not depend on Nice-to-Have later waves.  
4. **Evidence** — before/after screenshots + targeted tests per `PX002_TEST_STRATEGY.md`.  
5. **Rollback** — prefer feature-flag / template revert / CSS revert; no schema migrations planned for PX.  
6. **Must not claim** Version 1 production-ready or until-exam trust from any single wave.

---

## Wave 1 — Trust Chrome & Continuity Identity

| Field | Detail |
|-------|--------|
| **Goal** | Bind Finish/Home/title chrome and Profile/duration displays to honest package / plan identity. |
| **Workstreams** | WS-01 (PX-B-001 · PX-B-002 · PX-B-035 · PX-B-054); start PX-B-034 if capacity |
| **Expected student benefit** | After a sitting, tomorrow/title chrome matches the package just completed; Profile exam label matches Plan; same-day duration no longer contradicts itself across surfaces. |
| **Regression risk** | **High** — soft-pass chrome classes (PB-016/017); duration presentation. |
| **Acceptance gates** | Learning + Revision chrome match package identity on dogfood path; Profile never “Not set” with active plan exam; duration consistent or explicitly explained; no selection-logic change; targeted regression tests green. |
| **Rollback strategy** | Revert presentation resolvers/templates to last known soft-match behaviour **only** if release breaks Progressive Confidence; keep RO1-R1 closed class intact; hotfix package-id binding rather than keyword inference. |
| **Estimated effort** | **M–L** (≈ 1–2 engineering weeks + Founder **D-DURATION** decision) |

---

## Wave 2 — Terminal Revision & Tip-Complete Continuity

| Field | Detail |
|-------|--------|
| **Goal** | Eliminate student dependence on force-R1; lock natural tip-complete Memory/Publication handoff; ship Revision Q6 presentation. |
| **Workstreams** | WS-03 (PX-B-005 · PX-B-007 · PX-B-004) |
| **Expected student benefit** | After finishing a learning chain, the terminal Revision appears automatically; Revision completion language feels like retrieval, not a mismatched Learning checklist. |
| **Regression risk** | **High** — PB-017 Rho 5/5 force-R1 class; Continuity regenerate boundary. |
| **Acceptance gates** | Natural tip-complete → terminal Revision without force-R1; Memory/Publication handoff automated regression; Revision Q6 presentation variants live; educational selection policy unchanged. |
| **Rollback strategy** | Disable new regenerate trigger behind ops-safe flag if false positives; retain documented force-R1 as emergency-only; revert Q6 templates independently of regenerate. |
| **Estimated effort** | **M–L** (≈ 1–2 engineering weeks + continuity verification) |

---

## Wave 3 — Identity, Verbs & Interaction Quick Wins

| Field | Detail |
|-------|--------|
| **Goal** | Student-grade identity and language; finish/complete honesty; micro a11y and polish Quick Wins. |
| **Workstreams** | WS-07 (PX-B-038 · PX-B-039 · PX-B-034 · PX-B-040 · PX-B-041 · PX-B-043); WS-04 (PX-B-012 · PX-B-011); WS-02 (PX-B-015 · PX-B-016); WS-06 (PX-B-024 · PX-B-026 · PX-B-027); WS-10 (PX-B-019 · PX-B-020) |
| **Expected student benefit** | Product no longer reads as Internal Alpha tooling; start verbs consistent; Finish/Complete behaviour matches chrome; Analytics day-zero calm; small a11y/polish wins land early. |
| **Regression risk** | **Low–Medium** — string-pinned tests; confirm-modal behaviour. |
| **Acceptance gates** | **D-EOS**, **D-IDENTITY**, **D-COMPLETE-STEP**, **D-FINISH-CONFIRM** recorded; listed Quick Wins Closed or waived; Editorial sign-off on identity pack; Educational Content Freeze held. |
| **Rollback strategy** | Revert copy/templates per surface; confirm-modal change isolated from regenerate/chrome; keep research chrome relocatable via flag if needed. |
| **Estimated effort** | **M** (≈ 1 engineering week after decisions; parallelisable) |

---

## Wave 4 — Mobile Evidence & Accessibility Foundation

| Field | Detail |
|-------|--------|
| **Goal** | Prove live mobile/tablet quality; close primary-path a11y blockers; decide mobile nav. |
| **Workstreams** | WS-05 (PX-B-037 · PX-B-036); WS-06 (PX-B-025 · PX-B-028 · PX-B-029 · PX-B-030 · PX-B-023) |
| **Expected student benefit** | Phone use is deliberately navigable and tappable; keyboard and AT users can complete auth → home → mission → session → reflection → home; product can claim accessibility evidence, not aspiration. |
| **Regression risk** | **Medium** — nav pattern and CSS breadth. |
| **Acceptance gates** | Live phone + tablet evidence pack; one mobile nav pattern; touch targets + contrast AA; keyboard checklist complete; axe/Lighthouse on primary routes + one AT recording; modal resilience. |
| **Rollback strategy** | Nav pattern behind CSS/template scope to student shell; revert token applications surface-by-surface; keep CI a11y non-blocking until stable then gate. |
| **Estimated effort** | **L** (≈ 2 engineering weeks + Founder device dogfood calendar) |

---

## Wave 5 — Home Composition, Loading & Celebration

| Field | Detail |
|-------|--------|
| **Goal** | One-composition Home; coherent skeletons; honest session-complete celebration; real Help Centre. |
| **Workstreams** | WS-04 (PX-B-010); WS-09 (PX-B-032); WS-10 (PX-B-022); WS-07 (PX-B-042) |
| **Expected student benefit** | Home leads with one next action; slow paths feel crafted not blank; completion feels warm and student-facing; Help answers how-do-I questions. |
| **Regression risk** | **Medium** — Home is the primary CTA; Help content authoring. |
| **Acceptance gates** | Home hierarchy Target; skeletons on Home/Mission/Plan transitions; celebration without Internal Alpha research chrome; Help FAQ topics live (plan, readiness meaning, exam change, deferral). |
| **Rollback strategy** | Progressive disclosure toggles; skeleton CSS independent of data; Help content revert to prior help.html; celebration chrome relocatable. |
| **Estimated effort** | **M** (≈ 1–1.5 engineering weeks + Editorial for Help/celebration) |

---

## Wave 6 — Reliability, Performance & Session Unify

| Field | Detail |
|-------|--------|
| **Goal** | Ordinary students stay on natural path under load; Home/Mission feel faster; session mental model unified; ops labels isolated. |
| **Workstreams** | WS-08 (PX-B-008 · PX-B-009 · PX-B-006); WS-09 (PX-B-031); WS-02 (PX-B-014 · PX-B-017 · PX-B-033); WS-01 (PX-B-003) |
| **Expected student benefit** | Continue Session recovers calmly; first campaign sitting does not flash wrong inventory; waits feel honest; one way to finish a session; recovery messaging when lockout hits. |
| **Regression risk** | **High** under parallel load; **Medium–High** for path unify (**D-SESSION-PATH**). |
| **Acceptance gates** | Contention recovery UX + engineering fix; first-sitting gate/suppress; perceived-performance Target; interactive readiness audit; session path declared; ops expected-day isolated from student chrome; recovery copy + SLA. |
| **Rollback strategy** | Retry UX can ship without deep infra; path unify behind sole-runtime routing flags; ops detector changes do not touch student templates in same deploy if risk high — split deploys. |
| **Estimated effort** | **L** (≈ 2–3 engineering weeks; infra-dependent) |

---

## Wave 7 — Motivation, Long-Horizon Craft & Preferences

| Field | Detail |
|-------|--------|
| **Goal** | Calm long-horizon presentation: return, exam tone, milestones, diligence without punishment, Journey craft, motion, preferences. |
| **Workstreams** | WS-07 (PX-B-044 · PX-B-045); WS-10 (PX-B-046 · PX-B-047 · PX-B-018 · PX-B-021 · PX-B-049); WS-04 (PX-B-013 · PX-B-048) |
| **Expected student benefit** | Gaps welcome students back; near-exam chrome stays calm; arc completion acknowledged lightly; Journey orients; motion feels intentional; preferences stick. |
| **Regression risk** | **Low–Medium** — must not invent catch-up recommendations or pass promises. |
| **Acceptance gates** | Editorial sign-off; no XP/leaderboards; authorised next action only; reduced-motion held with PX-B-018; contextual density without mission re-selection. |
| **Rollback strategy** | Copy packs and motion CSS independently revertible; preferences UI behind settings surface. |
| **Estimated effort** | **M** (≈ 1–2 weeks; Nice to Have — deferrable without blocking Critical Path trust exits) |

---

## Wave 8 — Founder Dogfooding & Premium Certification

| Field | Detail |
|-------|--------|
| **Goal** | Multi-week chrome-growth evidence; re-score Premium Experience; close programme claim honestly. |
| **Workstreams** | WS-11 (PX-B-052); WS-12 (PX-B-053) |
| **Expected student benefit** | Indirect — product only claims “premium” when evidence supports it; long-horizon noise is found before wider cohorts. |
| **Regression risk** | **N/A** (assessment); Fail blocks claim language, not educational freeze. |
| **Acceptance gates** | Multi-week dogfood log filed; scorecard vs `PREMIUM_QUALITY_ATTRIBUTES.md` PASS or Conditional with owned residuals; claim posture matches Charter. |
| **Rollback strategy** | N/A for assessment; Conditional residuals return to backlog with owners — do not silently claim PASS. |
| **Estimated effort** | **M** (calendar-bound dogfood + ≈ 0.5–1 week certification write-up) |

---

## Future lane (capacity only — not a release wave)

| IDs | Workstream | Rule |
|-----|------------|------|
| PX-B-050 | WS-04 | Requires **D-COACH**; presentation-only |
| PX-B-051 | WS-10 | Maintainability; ship only if capacity |
| PX-X-* | — | Separate programme required |

---

## 3. Wave independence matrix

| Wave | Can ship without later waves? | Must not ship before |
|------|-------------------------------|----------------------|
| 1 | Yes | Founder authorisation of implementation |
| 2 | Yes | Prefer Wave 1 chrome baseline; may parallel if Continuity ownership clear |
| 3 | Yes | Decision gates for included items |
| 4 | Yes | Prefer Waves 1–3 for less noisy dogfood |
| 5 | Yes | Prefer Wave 1 titles honest before Home craft |
| 6 | Yes | Prefer Waves 1–2 for continuity stability |
| 7 | Yes | Prefer trust exits; **not** required for Critical Path S1 close |
| 8 | Yes as certification | High Impact / Foundation Closed or Board-waived |

---

## 4. Effort rollup (planning estimate)

| Wave | Effort band |
|------|-------------|
| 1 | M–L |
| 2 | M–L |
| 3 | M |
| 4 | L |
| 5 | M |
| 6 | L |
| 7 | M |
| 8 | M |
| **Programme total** | **≈ 10–16 engineering weeks** calendar-spread with Founder dogfood and decision latency |

Estimates are planning only — not a staffing commitment.

---

## 5. Immediate next step

**Await Founder approval** to commission **Wave 1** (or a Board-approved subset).

**STOP.** Do not implement backlog items under this planning programme.

Signed: Product Experience · PX-002 Implementation Plan · 2026-08-04
