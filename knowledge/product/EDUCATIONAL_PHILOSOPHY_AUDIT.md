# Educational Philosophy Audit

**Classification:** Architecture / Educational Review  
**Status:** SUBMITTED — awaiting Architecture Review  
**Date:** 2026-07-15  
**Scope:** Current product implementation vs intended educational philosophy  
**Nature:** Analysis only — no application code was modified  

**Primary evidence sources**

- Product path: `PlanningService`, `StudyPlanService`, `CurriculumService`, `AdaptiveLearningService`, `LearningService`, `RecommendationService`, mission/study-plan/dashboard templates
- Educational Intelligence: domain Twin / Decision / Recommendation packages; Internal Alpha flags; dashboard recommendation projection
- Stabilization docs: IA-001, IA-002, IA-003, IA-004
- Empirical signal: `research/internal_alpha/week_001/` (trust collapse from topic mismatch + engineering copy)
- Regression spines: `tests/test_ia004_truthful_learning_progress.py`, `tests/test_ia003_student_centred_educational_messaging.py`

**Compliance scale**

| Rank | Meaning |
|------|---------|
| **FULL** | Student-facing behaviour consistently matches the principle |
| **PARTIAL** | Directionally correct; meaningful gaps remain |
| **NON-COMPLIANT** | Dominant behaviour contradicts the principle |

---

## Executive Summary

Kwalitec’s educational philosophy is **coherent in architecture and recently strengthened in product** (especially IA-003 terminology and IA-004 Learning Mode / Study Progress). The live learning journey now defaults to syllabus order, completion no longer invents mastery, and student surfaces largely avoid Digital Twin / engineering jargon.

Alignment is still **partial overall**. Educational Intelligence can advise a different focus from Today’s Learning Mission; student “Why?” copy is often generic; self-reported confidence can inflate Estimated Mastery; accept/dismiss coaching consent is not productized; and “Estimated” honesty is uneven outside mastery labels.

**Verdict for Internal Alpha:** the catastrophic week_001 trust failures have been substantially mitigated in code, but residual dual-path recommendation behaviour and incomplete coaching agency mean the educational contract is not yet safe enough to treat as deployment-complete without Architecture conditions.

---

## Overall Educational Alignment Score

**62 / 100 — Moderate alignment (PARTIAL-dominant)**

| Rank | Count | Principles |
|------|-------|------------|
| FULL | 3 | EP-001*, EP-002, EP-008 |
| PARTIAL | 12 | EP-003, EP-004, EP-005, EP-006, EP-007, EP-009, EP-010, EP-011, EP-012, EP-013, EP-014, EP-015 |
| NON-COMPLIANT | 0 | — |

\*EP-001 is FULL for **Today’s Mission / Learning Mode** authority; advisory dual-display residual is noted under Evidence and Release Risks (does not downgrade the primary learning path).

Score method (informal): FULL = 100, PARTIAL = 50, NON-COMPLIANT = 0; mean across EP-001…EP-015.

---

## Principle Assessments

---

### EP-001 — Learning is sequential

**Principle**  
Students normally learn topics in syllabus order. Adaptive behaviour should support learning, not unexpectedly replace it.

**Why it exists**  
Professional exam syllabuses are sequential. Unexpected jumps to already-completed or weak topics destroy the student’s mental model of “where I am” and undermine trust in the coach.

**Current implementation**  
Today’s Mission is selected under **Learning Mode** (`PlanningService._select_topic_for_today`): the first incomplete syllabus leaf via `CurriculumService.get_next_incomplete_topic` / ordered topics. Review and weak-topic interruption are deferred and must not replace the planned sequence. Week plans for curriculum-backed plans are paced from official topic order. Adaptive / weak / review signals may still appear on advisory dashboard surfaces without rewriting the persisted mission topic.

**Compliance:** **FULL**

**Evidence**

- `app/services/planning_service.py` — Learning Mode docstring and selection logic (no review-date interruption)
- `CurriculumService.get_next_incomplete_topic` — ordered incomplete leaf walk
- Mission UI: “In Learning Mode, today's mission follows your Current Learning Topic…”
- `tests/test_ia004_truthful_learning_progress.py` — review/weak topics must not preempt syllabus order
- `IA-004_TRUTHFUL_LEARNING_PROGRESS.md` — Learning Mode as sole mission topic authority
- Contrast (historical): week_001 and `IA-001_FOLLOWUP_TOPIC_SELECTION_RCA.md` documented pre–IA-004 review→weak→next cascade (e.g. 2.6 replacing 4.2)

**Recommended action**  
Retain Learning Mode as v1.0 mission authority. Ensure advisory recommendations never present themselves as *today’s mission* when they name a different topic. Defer adaptive interruption until explicit, explained Phase 1 UX exists.

---

### EP-002 — Study Progress answers “What have I studied?”

**Principle**  
Study Progress answers what has been studied — not what has been mastered.

**Why it exists**  
Students can honestly declare study completion. Declaring mastery confuses coverage with competence and trains false confidence.

**Current implementation**  
`TopicProgress.completed` and stage `Completed` record Study Progress. Wizard/edit copy asks for topics “already completed studying.” Mission completion sets `completed=True` and does **not** write `mastery_score`. Estimated Mastery UI is gated on `has_estimated_mastery` (`average_accuracy is not None`). Dashboard labels use **Study Progress**.

**Compliance:** **FULL**

**Evidence**

- `app/mission/routes.py` — Study Progress–only write path; mastery score untouched
- `StudyPlanService` wizard init — completed topics get `mastery_score=0.0`, not Mastered stage from checkbox
- `TopicProgress.has_estimated_mastery`
- Templates: `wizard_step_4.html`, `study_plan/view.html`, dashboard Study Progress metrics
- `IA-004` + `tests/test_ia004_truthful_learning_progress.py` (completion ≠ mastery; false-mastery template scan)

**Recommended action**  
Preserve separation under Architecture Review. Watch residual naming: mission completion still sets `confidence="High"` (see EP-012). Avoid reintroducing “Mastered” badges for completion.

---

### EP-003 — Mastery is estimated

**Principle**  
Students never declare mastery. Only educational evidence may increase confidence (educational / estimated mastery confidence).

**Why it exists**  
Self-declaration of mastery is unreliable and educationally dangerous for high-stakes exams. Mastery must be inferred from attempts and outcomes.

**Current implementation**  
Students cannot tick Mastery on the study-plan checklist. Estimated Mastery is computed by `AdaptiveLearningService` from study attempts (accuracy, self-reported confidence, revisions, mistakes). Mission complete does not set mastery. However, mission review forms expose a confidence choice valued `"Mastered"` (UI label “Very Confident”), which is persisted on attempts and weighted at **30%** in the mastery formula (`CONFIDENCE_NUMERIC["Mastered"] = 100`). Stages can become `STAGE_MASTERED` from score thresholds.

**Compliance:** **PARTIAL**

**Evidence**

- Compliant: IA-004 completion paths; Estimated Mastery labels; `has_estimated_mastery`
- Tension: `app/mission/forms.py` — `("Mastered", "Very Confident")`
- Tension: `app/services/adaptive_learning_service.py` — confidence 30% of mastery score; ≥90 → `STAGE_MASTERED`
- Architecture intent: Twin / EI docs require evidence-backed beliefs; self-report must not become validated truth alone

**Recommended action**  
Rename student self-report vocabulary away from `"Mastered"`. Cap or isolate self-report so it cannot alone push Estimated Mastery / stage Mastered. Prefer Twin evidence density over single-formula mastery when EI Progress is enabled.

---

### EP-004 — Recommendations must be explainable

**Principle**  
Every recommendation should answer *Why?*

**Why it exists**  
Explainability is how an educational coach earns trust. Opaque “next step” suggestions feel arbitrary and reduce adherence.

**Current implementation**  
Domain EI has strong machinery: Decision reason codes, `ExplanationChainPresentation`, mission attribution, warrant postures. Student-facing EI card shows a family-generic “Why this recommendation” string (`recommendation_card_builder._STUDENT_REASON_BY_FAMILY`). Legacy `RecommendationService` entries include reason/benefit text. Mission page has a static Learning Mode why blurb. Deep explainability UI is gated off (`ENABLE_EI_EXPLAINABILITY=False` in Internal Alpha).

**Compliance:** **PARTIAL**

**Evidence**

- Domain: `app/domain/recommendation/explanation.py`, `reasons.py`; `app/domain/decision/reason_codes.py`
- Presentation: `app/application/dashboard/recommendation_card_builder.py` — generic family reasons; warranty warnings suppressed
- Templates: dashboard “Why this recommendation”; mission “Why this mission?”
- `STUDENT_DIGITAL_TWIN.md` Explainability Contract (factor-level *why*) vs current family templates
- IA-003 tests assert “Based on… / You've completed…” presence — not factor citation

**Recommended action**  
Ship student-safe reason narration that cites syllabus position, progress, and (when warranted) review need — without dumping eng enums. Enable explainability only after IA-003-quality mapping of warrant honesty.

---

### EP-005 — Educational terminology must always be truthful

**Principle**  
Students must never see engineering terminology.

**Why it exists**  
Engineering language (“evidence_creating”, entity ids, “Digital Twin”) destroys comprehension and trust — validated by week_001 (0/5 confidence after `"18 evidence creating"`).

**Current implementation**  
IA-003 remapped EI recommendation titles/subtitles/reasons, settings “Learning profile status”, and banned presentation of intent enums / numeric entity ids. Domain retains engineering vocabulary internally. Residual student copy still uses **“study evidence”** on mission/dashboard/analytics empties. Analytics retains “Estimated Mastery” chart language (educational, not eng).

**Compliance:** **PARTIAL**

**Evidence**

- `IA-003_STUDENT_CENTRED_EDUCATIONAL_MESSAGING.md`
- `recommendation_card_builder.py` family maps
- `tests/test_ia003_student_centred_educational_messaging.py` — forbidden terms/patterns
- Settings: Learning profile status (not Digital Twin)
- Residual: “study evidence” in `mission/index.html`, dashboard/analytics empty states
- Known limitation: EI subtitle does not yet resolve human syllabus topic titles

**Recommended action**  
Replace remaining “study evidence” with student language (“practice results”, “study checks”). Resolve topic titles into EI card copy. Keep regression suite mandatory for student templates.

---

### EP-006 — Missions should reinforce learning

**Principle**  
Missions are not arbitrary tasks. Every mission should contribute directly to learning.

**Why it exists**  
Missions are the daily educational commitment. Arbitrary tasks waste scarce study time and break the coach metaphor.

**Current implementation**  
Product ORM missions follow Current Learning Topic (syllabus learning). Completion records Study Progress on that topic. Missions are plan-bound (`study_plan_id`). Domain Mission Intelligence exists with mandatory Decision attribution but is **not** the live student path (`ENABLE_EI_MISSIONS=False`). Dashboard still has competing advisory widgets (`MissionOptimizer` balanced mixes).

**Compliance:** **PARTIAL**

**Evidence**

- Learning Mode selection → next incomplete leaf
- Mission why copy ties mission to Current Learning Topic and Study Progress vs Estimated Mastery
- IA-001 / IA-002 plan scoping and synchronization
- Domain: `app/domain/mission/` attribution / evidence hooks (completion ≠ mastery)
- Competing signals: EI recommendation card; `MissionOptimizer.generate_balanced_mission`

**Recommended action**  
Keep Learning Mode as mission authority through v1.0. Remove or clearly label non–Learning Mode “mission-shaped” widgets. Do not enable EI missions until they reinforce — or explicitly negotiate interruption of — the learning sequence.

---

### EP-007 — Study Plan = learning progress; Digital Twin = understanding

**Principle**  
These concepts must never be mixed.

**Why it exists**  
Mixing coverage with understanding makes students believe they are exam-ready when they have only studied forward.

**Current implementation**  
Product vocabulary separates Study Progress / Learning Progress (coverage) from Estimated Mastery (understanding proxy). Wizard and mission completion enforce progress-only writes. Twin holds understanding domains behind EI; students do not interact with Twin as a labelled system. Residual blur: dashboard “Learning Progress” may show readiness/legacy composite paths described as “average topic progress” (`avg_mastery`), and ORM `mastery_score` coexists with Twin knowledge as dual stores.

**Compliance:** **PARTIAL**

**Evidence**

- IA-004 domain model table; wizard helper text
- Study Plan roadmap: Completed badge vs Estimated Mastery when `has_estimated_mastery`
- Settings: Current study plan vs Learning profile status as separate fields
- Twin constitution / EI architecture: Twin = understanding; Study Plan derived schedule
- Naming risk: “Learning Progress” over mastery-derived averages

**Recommended action**  
Audit every student metric label against {Study Progress, Learning Progress, Estimated Mastery}. Never show Twin contents as Study Plan metrics. Prefer one presentation-facing estimate store until Twin Progress is student-ready.

---

### EP-008 — The Digital Twin is invisible

**Principle**  
Students experience guidance, not implementation. The Digital Twin is invisible.

**Why it exists**  
Exposing the Twin invites students to game scores and confuses product with research infrastructure.

**Current implementation**  
Students see Study Plan, missions, recommendations, Estimated Mastery, readiness/progress. Twin is retrieved via `TwinProvider` / orchestrator and not named in student templates. Internal Alpha settings show only presence-style **Learning profile status** (`Ready` / `Not yet set up`). Warrant contents and Twin fields are not rendered. EI Missions / Explainability / Progress flags remain off.

**Compliance:** **FULL**

**Evidence**

- IA-003 + `test_settings_learning_profile_not_digital_twin`
- Grep: student templates avoid “Digital Twin”
- `InternalAlphaStatusService._twin_status_label` — presence labels only
- `ENABLE_EI_PROGRESS=False` / warnings composed to `None` for students

**Recommended action**  
Preserve invisibility when enabling Progress/Explainability. Never dump warrant tags, posture enums, or Twin schemas. Keep Learning profile status presence-only if retained for Internal Alpha operators.

---

### EP-009 — Educational Intelligence should advise

**Principle**  
EI should advise. It should not silently override the student’s learning journey.

**Why it exists**  
Silent override (week_001: mission 4.2 vs recommendation 2.6) feels like a dictator and collapses trust.

**Current implementation**  
EI does **not** rewrite Today’s Mission topic under Internal Alpha (`ENABLE_EI_MISSIONS=False`; Learning Mode owns ORM selection). Recommendation card CTA navigates to the mission page; it does not mutate mission persistence. Advisory divergence remains possible: EI card or legacy weak-topic lists can still *name* a different focus while the mission stays on Learning Mode. Week_001 experienced this as override even when engines differed.

**Compliance:** **PARTIAL**

**Evidence**

- `planning_service.py` Learning Mode; `internal_alpha.py` flags
- Dashboard: EI compose separate from `generate_today_mission`
- `recommendation_card_builder.py` — projection only; does not mutate Decisions/Missions
- Empirical: `research/internal_alpha/week_001/findings/educational.md` — mismatch destroyed trust
- IA-001 known residual: dual display/advisory paths

**Recommended action**  
Bind or subordinate EI recommendation presentation to Current Learning Topic for v1.0 / Internal Alpha Stage A, **or** explicitly label non-mission advice as “Optional review (not today’s learning)”. Never allow CTA “Start Today's Session” to imply accepting a contradictory topic.

---

### EP-010 — Trust is more important than optimisation

**Principle**  
Students should always understand why Kwalitec behaves as it does.

**Why it exists**  
Optimised-but-opaque recommendations fail commercial and educational adoption. Week_001 trust = 0/5 after opaque / wrong-topic advice.

**Current implementation**  
Mission and EI surfaces include Why copy. IA-003 removed worst engineering leaks. Trust is still vulnerable to: topic disagreement between surfaces; generic Why strings; suppressed warrant honesty; read-only Decision Journal without a write loop; dual recommendation stacks.

**Compliance:** **PARTIAL**

**Evidence**

- Mission / dashboard Why sections
- IA-003 fix of `"18 evidence creating"` class failures
- `ENABLE_EI_EXPLAINABILITY=False`
- Decision Journal UI present; product accept/dismiss loop incomplete (EP-015)
- Twin Constitution / EI Architecture: honesty and explainability principles

**Recommended action**  
Treat educational trust metrics (topic agreement, Why authenticity, jargon absence) as release gates. Prefer truthful Learning Mode messaging over adaptive optimisation until Phase 1 interruption is explained and optional.

---

### EP-011 — Educational evidence accumulates over time

**Principle**  
One completed mission never proves mastery.

**Why it exists**  
Mastery of professional syllabus topics requires repeated, varied performance — not a checkbox or a single session.

**Current implementation**  
Mission completion alone does not change `mastery_score` (FULL for that path). Estimated Mastery updates via StudyAttempt averages. Domain evidence hooks mark completion as non-mastery. Gap: a **single** strong study attempt can produce high `mastery_score` and even `STAGE_MASTERED` (≥90); `mastery_score >= 70` can auto-set `completed=True`. No minimum attempt count / density / spacing before high mastery stages.

**Compliance:** **PARTIAL**

**Evidence**

- `_apply_mission_topic_progress` leaves mastery unchanged; IA-004 tests
- `AdaptiveLearningService.update_mastery_after_attempt` — averages history but allows high scores from one attempt
- Auto-complete on high mastery score
- Mission copy: “Estimated Mastery grows from study evidence over time”

**Recommended action**  
Require evidence density (multiple attempts / spaced outcomes) before high Estimated Mastery stages. Never auto-flip Study Progress from a mastery formula without student-visible confirmation. Align product formula with Twin evidence doctrine over time.

---

### EP-012 — Student confidence ≠ Educational confidence

**Principle**  
Student confidence and Educational confidence are different concepts.

**Why it exists**  
Felt certainty and educational warrant must not collapse into one dial — otherwise the system confuses self-belief with readiness.

**Current implementation**  
Architecture (EI Confidence domain, Twin Constitution, ubiquitous language) separates felt confidence, recommendation warrant, and mastery. Product conflates them: `TopicProgress.confidence` is a system/stage-like field (often `"High"` on completion); `average_confidence` aggregates self-ratings into mastery math; form value `"Mastered"` labels “Very Confident”; no UI shows student self-rating vs educational estimate/warrant.

**Compliance:** **PARTIAL**

**Evidence**

- Docs: `EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md` § Confidence; Twin docs on calibration
- `mission/routes.py` — `progress.confidence = "High"` on Study Progress write
- `mission/forms.py` — Mastered / Very Confident
- `adaptive_learning_service.py` — self-report into mastery
- No student vs educational confidence comparison UI; Twin `ConfidenceState` incomplete relative to architecture reviews

**Recommended action**  
Separate vocabularies: student felt confidence vs Estimated Mastery vs warrant honesty. Stop writing `"High"`/`"Mastered"` onto progress as proxy mastery. Introduce calibration only when Twin Confidence is ready — never before naming is cleaned.

---

### EP-013 — Learning should feel continuous

**Principle**  
Switching study plans should never create educational discontinuity.

**Why it exists**  
Students manage multiple sittings/subjects. Losing progress or seeing stale wrong-plan missions feels broken and punitive.

**Current implementation**  
Active plan is DB source of truth; `set_active_plan` → `synchronize_student_surfaces` regenerates plan-scoped Today’s Mission (IA-001/IA-002). Topic progress is user+topic; re-init preserves existing rows. Returning to a prior curriculum reuses completed leaves. Gaps: deleting a study plan deletes curriculum-linked `TopicProgress` (attempts preserved); advisory weak/coverage lists may remain user-global; open tabs can show stale HTML until reload.

**Compliance:** **PARTIAL**

**Evidence**

- `StudyPlanService.set_active_plan` + surface sync
- Progress preservation on plan heal/create
- IA-001 mission `study_plan_id` binding; IA-002 tests (CS1↔CM1 switch)
- `delete_study_plan` deleting TopicProgress
- IA-002 documented stale-tab limitation

**Recommended action**  
Preserve Study Progress on plan delete (archive, don’t wipe). Scope all advisory lists by active plan. Prefer soft refresh / plan-version headers if multi-tab use is common in alpha.

---

### EP-014 — Communicate uncertainty honestly

**Principle**  
Use “Estimated” whenever certainty cannot be justified.

**Why it exists**  
False certainty is educationally unethical and commercially dangerous for exam products.

**Current implementation**  
Estimated Mastery / “% est.” / Estimated Time are widely used and gated. Calibration/wizard stress declarations ≠ mastery. Domain warrant postures exist (`honest_low`, `cold_start`, …). Student UI **suppresses** thin-warrant warnings. Some legacy recommendation/readiness copy asserts strong outcomes (“excellent coverage”, “complete exam confidence”) without estimated language.

**Compliance:** **PARTIAL**

**Evidence**

- Templates: Estimated Mastery titles and empty states
- `has_estimated_mastery` gate
- `_compose_warning` returns `None` — cold-start honesty not shown
- Overconfident progression/coverage phrases in legacy recommendation paths

**Recommended action**  
Narrate low-evidence situations in plain language (“We’re still learning how you’re doing on this topic”). Ban absolute confidence claims without evidence density. Prefer Estimated on all understanding/readiness projections that are not pure completion counts.

---

### EP-015 — The student remains in control

**Principle**  
Kwalitec is an educational coach, not an educational dictator.

**Why it exists**  
Agency sustains long exam journeys. Dictatorship produces dismissal, workarounds, and distrust.

**Current implementation**  
Students control study-plan creation/edit, completed-study checkboxes, active plan switching, mission start/complete/task toggles, and settings. Learning Mode reduces daily topic choice by coaching default. Recommendation accept/dismiss/defer exists in domain and `RecommendationService.record_decision`, and Decision Journal can display — but **no student HTTP flow records accept/dismiss**; EI card CTA only navigates. No setting to choose Learning Mode vs future adaptive interruption.

**Compliance:** **PARTIAL**

**Evidence**

- Study plan edit / wizard / set active plan
- Domain affordances ACCEPT|DISMISS|DEFER; card maps ACCEPT → “Start Today's Session” only
- `record_decision` called from tests, not student routes (as of audit)
- Tech debt: Decision Journal ↔ Learning Evidence loop deferred
- No dismiss control on EI recommendation card

**Recommended action**  
Add explicit Accept / Not today (dismiss) / Remind me later on recommendations without mutating mastery. Keep Learning Mode default; make future interruptions **opt-in or explicitly confirmed**. Never force review topics without disclosure.

---

## Overall Report

### Top Strengths

1. **Learning Mode sequential mission authority** — Today’s Mission follows syllabus order; adaptive preemption deferred (EP-001 / EP-006 / EP-009 core path).
2. **Truthful Study Progress vs Estimated Mastery** — Completion no longer invents mastery; UI and writes largely honor the distinction (EP-002 / EP-007 presentation).
3. **Digital Twin invisibility + terminology cleanup** — Twin contents hidden; IA-003 removed the worst engineering leaks that zeroed trust (EP-005 / EP-008).
4. **Architecture ahead of product** — Twin Constitution, Evidence Model, and EI principles correctly state confidence ≠ mastery, evidence accumulation, and coach (not dictator) posture.
5. **Deterministic, curriculum-first cores** — Recommendations and planning remain explainable in principle and free of LLM black boxes on core paths.

### Top Weaknesses

1. **Advisory dual path** — EI / legacy recommendations can still disagree with Today’s Learning Mission while sounding authoritative (EP-009 / EP-010).
2. **Self-report into mastery** — `"Mastered"` / “Very Confident” and 30% confidence weight allow students to inflate Estimated Mastery (EP-003 / EP-011 / EP-012).
3. **Shallow Why** — Family-generic reasons instead of factor-level educational explanation; warrant honesty suppressed (EP-004 / EP-014).
4. **Missing coaching consent loop** — Accept/dismiss Decision Journal not productized (EP-015).
5. **Plan-delete / continuity edges** — Study Progress wipe and global advisory lists weaken continuous learning (EP-013).

### Release Risks

| Risk | Severity | Linked EPs |
|------|----------|------------|
| Recommendation names Topic A while Mission is Topic B; CTA implies both | **P0** | EP-009, EP-010, EP-001 |
| Regression reintroducing completion→mastery writes | **P0** | EP-002, EP-003, EP-011 |
| Engineering terminology leak on EI card | **P0** | EP-005 |
| Enabling EI Missions without Learning Mode subordination | **P0** | EP-006, EP-009 |
| Enabling Explainability with raw warrant tags | **P1** | EP-005, EP-008, EP-014 |
| Mastery stage inflation from one attempt + self-report | **P1** | EP-003, EP-011, EP-012 |

### Educational Risks

- Students may **stop trusting** the coach again if advisory and learning paths diverge (week_001 pattern).
- Students may **overestimate readiness** if Estimated Mastery rises from sparse, confidence-heavy attempts.
- Students may **confuse covering the syllabus with understanding** if “Learning Progress” labels sit atop mastery-derived numbers.
- Without dismiss agency, disregarded advice cannot teach preference — the system may thrash when adaptive interruption returns.
- Silent optimisation pressure (MissionOptimizer / weak lists) can recreate pre–IA-004 educational confusion even while Learning Mode holds mission persistence.

### Required before Version 1.0

1. **Educational consistency gate:** Recommendation surfaces must not contradict Today’s Learning Mission without explicit “optional review” framing (EP-009 / EP-010).
2. **Preserve IA-004 completion semantics** under Architecture Review: completion ≠ mastery forever (EP-002 / EP-003 / EP-011).
3. **Preserve IA-003 messaging invariants** with regression tests on student templates (EP-005).
4. **Rename/decouple student self-report** from `"Mastered"` and prevent single-session mastery theatre (EP-003 / EP-012).
5. **Productize Accept / Dismiss** for recommendations → Decision Journal (preference only) (EP-015).
6. **Factor-level student Why** for the live recommendation path without engineering dumps (EP-004).
7. **Honest low-evidence language** when warrant is thin (EP-014).
8. **Plan continuity:** do not destroy Study Progress on plan delete; scope advisory lists to active plan (EP-013).

### Nice-to-have before Version 1.0

1. Human syllabus titles on EI recommendation subtitle (IA-003 known limitation).
2. Calibration UI once Twin Confidence is real (EP-012 — only after vocabulary cleanup).
3. Explained, optional Phase 1 review interruption — never silent (EP-001 / EP-009).
4. Unify or clearly retire legacy RecommendationService when EI packaging is primary.
5. Evidence-density thresholds before high Estimated Mastery badges.
6. Soft handling of multi-tab stale plan displays (IA-002).

### Final Recommendation

**NOT READY** for Internal Alpha deployment as an educationally trustworthy release.

**Meaning of this verdict**

- Architecture and recent IA-003 / IA-004 work show the **correct direction** and have mitigated the worst observed week_001 failures.
- Residual **dual-path recommendation behaviour**, **confidence conflation**, and **missing student coaching agency** remain sufficient to recreate educational distrust under real study conditions.
- Continued Internal Alpha **engineering testing** may proceed under Architecture Office constraints; **educational deployment confidence** should wait until Required-before-v1.0 items 1–3 (consistency + completion semantics + terminology) are Architecture-accepted and empirically re-validated with students.

---

## Method Notes

- This audit assesses **current implementation behaviour**, not roadmap aspiration.
- Domain EI depth was credited where it exists, but **student-facing paths** weight compliance more heavily than unused domain packages.
- Internal Alpha feature flags (`ENABLE_EI_RECOMMENDATIONS=True`, `ENABLE_EI_MISSIONS=False`, `ENABLE_EI_EXPLAINABILITY=False`, `ENABLE_EI_PROGRESS=False`) are treated as part of the live educational contract.
- No code, tests, or migrations were modified for this deliverable.

---

## Return

**Stop after this report.**  
**Return for Architecture Review.**
