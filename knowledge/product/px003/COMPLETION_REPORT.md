# PX-003 — Independent Release Candidate Design Review: Completion Report

**Programme:** PX-003 — Independent Release Candidate Design Review (Analysis Only)
**Date:** 2026-07-26
**Predecessors reviewed against:** `knowledge/product/px001/` (Premium Experience Audit), `knowledge/product/px002a/` (Trust & Friction Resolution), `knowledge/product/px002b/` (Premium Refinement). This review was conducted with no assumed ownership of, or deference to, any of their conclusions — every "Resolved" claim inherited from those programmes that this review relied on was independently re-verified against current code before being treated as true.
**Does not:** modify application code, templates, or stylesheets; redesign any screen; invent features; commit any change; claim Version 1 production-readiness; claim validated KSI.

---

## Summary

PX-003 conducted an independent, adversarial, evidence-based release-candidate review of every reachable student-facing screen and state in Kwalitec ahead of the first external Stage 1 pilot, with an explicit mandate to reject the release if warranted rather than to improve the product. The review combined direct re-inspection of all major templates, routes, view models, presentation services, and CSS/JS under `app/`, cross-checked against the live production flag configuration in `render.yaml`, rather than relying on prior programmes' completion reports as ground truth. Ten of those prior findings and self-reported "resolved" statuses were independently re-verified; several were found to be either not resolved, or resolved only in wording/presentation while the underlying factual or structural defect remains. The review produced ten specific, code-cited release-blocking findings spanning trust/factual-integrity defects (a reflection note that is discarded despite an on-screen promise it is kept; a Profile screen that can contradict every other screen about the same student's own exam; a study-session duration figure that can still diverge between Home and Mission through two different, only-partially-unified code paths), accessibility failures on the two highest-stakes interaction points in the product (the first-session welcome modal; the only mobile navigation drawer), one live, un-redirected duplicate settings surface, one internal-engine-status label exposed to students outside its intended audience, an onboarding flow not reliably triggered on the production login path, and the confirmed absence of any live mobile or tablet rendering across the product's entire documented design-review history. Eighteen further findings were logged as real but non-blocking. The decision recorded in `PRE_RENDER_DECISION.md` is **REQUIRES ADDITIONAL WORK**.

## Files Created

- `knowledge/product/px003/RELEASE_BLOCKERS.md`
- `knowledge/product/px003/NON_BLOCKING_IMPROVEMENTS.md`
- `knowledge/product/px003/ACCESSIBILITY_REVIEW.md`
- `knowledge/product/px003/PRE_RENDER_DECISION.md`
- `knowledge/product/px003/COMPLETION_REPORT.md` (this file)

## Files Modified

None. This is a read-only review programme. No application code, template, stylesheet, or test file was modified while producing it.

## Tests Executed

None. This is a documentation/analysis-only programme; no test suite is applicable, and no code change was made for any suite to verify. Where this report or its companions cite behavior (e.g., "the note is never persisted," "the route has no redirect guard"), the citation is to the relevant source lines directly, not to a test run — this review did not execute the application or its test suite, consistent with a static-review scope.

## Migration Impact

None. No schema, Alembic, or data change was made or proposed for implementation under this programme.

## Architecture Compliance

N/A for curriculum V1/V2 engine or Runtime A changes — no code was changed. Where this review's findings touch architecture (the dual navigation/settings-shell residue in Blocker B9; the two independent duration-resolution call paths behind Blocker B3; the two parallel session-experience flows in N15), it cites existing code structure as evidence for a design/trust finding rather than proposing new architecture, consistent with this programme's analysis-only scope and with PX-001's precedent for the same kind of cross-cutting finding. Curriculum V1/V2 traversal and import compatibility were not touched and are not implicated by any finding in this review.

## Technical Debt

- This review relied on manual, static code inspection for every finding, with no automated accessibility scanning (axe-core/Lighthouse/WAVE), no live screen-reader session, and no live browser rendering at any viewport size. This is the same limitation PX-001 and PX-002B each disclosed independently; this review's contribution is to make explicit that, three review programmes in, that gap has never been closed, and to treat its continued existence as a release-blocking finding in its own right (`RELEASE_BLOCKERS.md` B7) rather than a repeated footnote.
- Several plausible contrast risks (`ACCESSIBILITY_REVIEW.md` §4 — alert-background text pairs, `--text-muted` at small sizes) are recorded as "plausible risk, not confirmed" rather than as pass or fail, because this review does not have a contrast-measurement tool available and chose not to assert a verdict it could not support. A future programme with such a tool should resolve these explicitly.
- This review did not attempt to determine which of the two duration-resolution call paths behind Blocker B3, or which of the two parallel session-experience flows behind N15, should be authoritative — those are Runtime-A/architecture-scope decisions this review does not have standing to make, consistent with PX-001's and PX-002A's own explicit deferral of the same question.
- The founder/admin console (`app/founder/dashboard/templates/`) was, as in all three prior programmes, treated as out of scope because it is not student-facing; the one native `confirm()` dialog this review found anywhere in the codebase lives there (`vision_entry_detail.html:150,154`) and is noted for completeness but not treated as a student-facing finding.

## Known Limitations

- This is a **design-quality, consistency, trust, and accessibility review**, not a usability test with real students and not Stage 1 pilot evidence. Every finding in this review is based on direct source inspection of the current working tree; none is corroborated by a real user session, and this review has no standing to claim it would generalize to actual pilot-student behavior — only that the code, as written, will produce the specific behavior described.
- This review inherited PX-001's and PX-002B's evidence gap on live mobile/tablet rendering and was not able to close it — see Blocker B7 for why that gap is treated as blocking rather than as an inherited footnote this time.
- Two review-brief benchmark instructions ("Apple HIG, Linear, Stripe — not appearance, quality/craft/consistency") were applied qualitatively, in the same spirit as PX-001's use of the same benchmark set against the product's own `UI_UX_IMPLEMENTATION_STANDARD.md`; this review did not produce a new, separate benchmark-comparison table, because the review brief's explicit instruction to judge only against usability/consistency/trust/accessibility/cognitive-load/craftsmanship/educational-focus (not "fashionable UI" or trend comparison) made a separate appearance-benchmarking exercise out of scope for a rejection-mandate review.
- This review did not independently re-verify every claim in PX-002A's and PX-002B's completion reports about test-suite pass/fail status (e.g., "43,097 passed, 42 failed") — that is an engineering-verification claim, not a design/UX claim, and the review brief states engineering completion is a given assumption for this programme. Where a test-suite claim was directly relevant to a design finding (e.g., whether `test_accessibility.py` actually covers contrast/focus/keyboard), this review read the test file itself rather than trusting a prior summary of it — see `ACCESSIBILITY_REVIEW.md` §"Verification gap."
- Six subagent research passes were used to gather breadth of evidence across the full screen inventory in parallel; every specific citation in `RELEASE_BLOCKERS.md` and `ACCESSIBILITY_REVIEW.md` that this report treats as load-bearing (B1–B10) was independently re-confirmed by this review's own direct file reads before being included, not accepted solely on a subagent's summary. Findings in `NON_BLOCKING_IMPROVEMENTS.md` rely more directly on subagent-reported citations and carry correspondingly lower — though still file-and-line-cited — confidence.

## Student Impact Assessment

N/A as a completed empirical assessment against `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md` — PX-003 is an internal, pre-render review programme with no student-facing product change. No student was exposed to any change under this programme; its output is a set of findings and a render/no-render recommendation, not a product change with its own student impact to assess.

## Estimated KSI contribution

**ΔKSI = 0.** PX-003 produced a review and a set of documented findings only; no student-facing product, copy, or behaviour change was made, and no validated or estimated KSI measurement was performed or claimed. If the ten blocking findings in `RELEASE_BLOCKERS.md` are subsequently fixed by an implementation programme, that programme — not this one — should estimate the resulting KSI delta, since the fixes (not this review) are what would change student experience.

## Evidence collected

- `app/templates/**/*.html`, `app/static/css/**/*.css`, `app/static/js/*.js`, `app/*/routes.py`, `app/presentation/**`, `app/application/**`, `app/infrastructure/adapters/**`, `app/services/**` (live code, read-only) — direct citations throughout `RELEASE_BLOCKERS.md`, `NON_BLOCKING_IMPROVEMENTS.md`, and `ACCESSIBILITY_REVIEW.md`.
- `render.yaml` — direct verification of the production flag configuration (`KWALITEC_V2_SOLE_RUNTIME`, `KWALITEC_EI_INTERNAL_ALPHA`, `APP_ENV`) used to determine which navigation/settings/branding surfaces actually reach a Stage 1 external pilot student.
- `tests/presentation/student/test_accessibility.py` — read in full to establish exactly what is, and is not, covered by existing automated accessibility checks.
- `knowledge/product/px001/*.md`, `knowledge/product/px002a/*.md`, `knowledge/product/px002b/*.md` — read in full as prior-programme context and as the source of every "previously reported as resolved" claim this review chose to re-verify rather than accept.
- Six parallel `explore`-subagent evidence-gathering passes, each scoped to a specific screen/system area (session & mission flow; settings/profile/help/errors; home/mission/journey/revision/history/analytics; accessibility tokens & base layout; responsive breakpoints & mobile; legacy-nav reachability & auth), each instructed to cite file:line for every claim — used as a breadth mechanism, with every load-bearing claim independently re-confirmed by this review before inclusion in the blocking findings.

## Lessons learned for student value

- The specific pattern this review found most instructive is that the product's three prior review programmes each correctly identified the same root-cause defect classes (factual duration contradictions; internal-language leakage; duplicate navigation homes) and each made real, verifiable progress against them — but in every one of the three cases this review checked deeply (duration, Profile examination label, Settings reachability), the fix closed the *specific instance* named in the prior report without closing the *underlying mechanism*, so a structurally identical defect reappeared on an adjacent screen the prior report did not happen to sample (Settings instead of Home/Analytics/Mission; the reflection *note* instead of the reflection *screen's copy*, which was the part actually fixed). The lesson for any future implementation programme is to look for and close the underlying mechanism (e.g., "every legacy index route must call the same redirect guard," "every duration-consuming template must call the same resolver," not "this one template now shows the right words") rather than treating each finding as a single-template patch.
- Verifying claims directly against current code, rather than trusting a prior completion report's account of what was fixed, changed this review's conclusion on at least three items (duration, native `confirm()` removal completeness, Settings reachability) from "confirmed resolved" to "resolved in the narrow case cited, not resolved as a class" — a concrete argument, consistent with PX-002A's own stated lesson from its own session, for treating "re-verify against the artifact, not the report about the artifact" as mandatory practice for any release-gating review.
- None of this review's findings were validated against a real student, and this review does not claim they would be. Its value is in reducing the number of code-verifiable, avoidable trust and accessibility defects a real student would otherwise be the first to discover.

## Explainability Review

N/A as a formal `EXPLAINABILITY_REVIEW_CHECKLIST.md` pass — PX-003 did not change any explanation, recommendation, or readiness-facing copy or logic; it only documented current-state findings for a future implementation programme to act on. Blocker B1 (Reflection) and Blocker B3 (duration) both touch surfaces explicitly in scope for that checklist per `knowledge/GOVERNANCE.md` §4.2; a future programme implementing either fix should run the Explainability Review Checklist at that time, since both affect what the product explains to a student and whether that explanation is true.

## Recommendation Quality Review

N/A as a formal `RECOMMENDATION_REVIEW_CHECKLIST.md` pass — PX-003 did not change ranking, selection, or recommendation copy/logic. Blocker B3's duration-consistency question is recommendation-adjacent (Today's Mission duration) in the same way PX-001 flagged its own T1-2 equivalent; a future programme resolving B3 should run this checklist per `knowledge/GOVERNANCE.md` §4.3, per PX-001's own precedent for the same finding.

## Version 1 readiness residual

This review does not close, and does not attempt to close, any gate in `VERSION_1_RELEASE_FRAMEWORK.md` (G1–G12); it has no gate-closing authority. It is directly relevant to whichever gate(s) govern student-facing design/UX/accessibility quality and pre-pilot readiness, and its explicit decision — **REQUIRES ADDITIONAL WORK**, not **APPROVED FOR RENDER** — should be read by whoever owns those gates as evidence that this review's applicable gate(s) are not yet satisfied, pending resolution of `RELEASE_BLOCKERS.md` B1–B10.

---

## Decision (restated from `PRE_RENDER_DECISION.md`)

**REQUIRES ADDITIONAL WORK**

Ten specific, code-verified, cited defects block this release candidate as of this review. None require a redesign; several are narrow, mechanical fixes the codebase already demonstrates the correct pattern for elsewhere. This review's mandate was to reject if warranted, and it was warranted: three of the ten findings are factual trust violations on the exact class of defect this product's own prior review programmes identified as its most damaging risk, and one (the absence of any live mobile/tablet verification, ever) is a missing-evidence blocker independent of any single code defect. Full evidence and reasoning are in `RELEASE_BLOCKERS.md`, `ACCESSIBILITY_REVIEW.md`, and `PRE_RENDER_DECISION.md`.
