# Educational Philosophy Audit — Version 2

**Capability ID:** EPA-002  
**Programme:** Educational Governance Initiative  
**Title:** Educational Philosophy Audit Version 2  
**Classification:** Educational Governance Baseline Review  
**Status:** SUBMITTED — awaiting Architecture Review  
**Date:** 2026-07-15  
**Scope:** Current product implementation vs Educational Governance framework  
**Nature:** Analysis only — no application code and no other documentation were modified  

**Governing authorities (applied as-written; not redesigned)**

| Authority | ID | Version | Path |
|-----------|-----|---------|------|
| Educational Constitution | EGI-001 | 1.0 | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| Educational Logic Registry | EGI-002 | 1.0 | `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` |
| Educational Governance Review Standard | EGI-003 | 1.0 | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` |

**Primary evidence sources**

- Product path: `PlanningService`, `StudyPlanService`, `CurriculumService`, `AdaptiveLearningService`, `LearningService`, `RecommendationService`, `ReadinessService`, mission / study-plan / dashboard / analytics / settings templates
- Educational Intelligence: Internal Alpha flags (`app/application/config/internal_alpha.py`); `RecommendationCardBuilder`; dashboard assembly
- Stabilisation doctrines: IA-001, IA-003, IA-004
- Diagnostic predecessor: `knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md` (EPA-001 / informal EP-xxx — superseded as baseline by this V2)
- Empirical signal: `research/internal_alpha/week_001/` (topic mismatch + engineering copy trust collapse)
- Regression spines: `tests/test_ia004_truthful_learning_progress.py`, `tests/test_ia003_student_centred_educational_messaging.py`

**Method**

This audit evaluates **student-visible educational meaning** and **decision authority** against Constitution Articles, Registry logics EL-001–EL-012, and Governance Categories A–H. Registry “Current Implementation Status” residuals are treated as **compliance debt**, not constitutional permission (EGI-003 §3 Category B). Recommendations state educational direction only — not implementation design.

---

## Executive Summary

Kwalitec’s Educational Governance framework is now complete enough to judge Version 1.0 educational trustworthiness objectively. Relative to that law, the live product shows a **correct Learning Mode spine** (Today’s Mission follows Current Learning Topic; Study Progress checkboxes no longer invent Mastered badges; Twin naming is largely invisible) and a **still-broken understanding/evidence spine** (self-reported “Mastered” confidence can mint mastery stages; mastery formulae can auto-write Study Progress; mission complete still triggers mastery recalculation; dual readiness meanings under one “Learning Progress” label; advisory surfaces can disagree with Learning Mode without mandatory optional-review disclosure).

**Overall Governance Score: 28 / 100 — Failed governance.**  
Categories A, B, and D are **NON-COMPLIANT** due to automatic triggers. Version 1.0 Educational Release Gate and Internal Alpha **educational deployment** both fail.

**Verdict:** **NOT READY** for Internal Alpha educational deployment.

---

## Surfaces Reviewed

| Educational Surface | Primary evidence locations |
|---------------------|----------------------------|
| Study Plan | `study_plan_service.py`, wizard/edit/view templates |
| Mission | `planning_service.py`, `mission/routes.py`, `mission/index.html` |
| Dashboard | `dashboard/index.html`, dashboard routes / assemblers |
| Recommendations | `recommendation_card_builder.py`, `recommendation_service.py` |
| Analytics | `analytics/index.html`, `analytics_service.py` |
| Educational Messaging | IA-003 templates + residual “study evidence” / form values |
| Adaptive Learning | `adaptive_learning_service.py` |
| Educational Evidence | Domain evidence packages vs live `StudyAttempt` → mastery path |
| Mission Completion | `complete_mission` → `LearningService.create_study_attempt` → `_apply_mission_topic_progress` |
| Current Learning Topic | `CurriculumService.get_next_incomplete_topic` via Learning Mode |
| Estimated Knowledge | Presentation labels sharing `mastery_score` (no distinct EL-006 surface) |
| Estimated Mastery | `TopicProgress.mastery_score` + `has_estimated_mastery` gate |
| Readiness | `ReadinessService.calculate_readiness` vs `get_overall_readiness` |
| Student Confidence | `mission/forms.py`, progress `confidence` writes |
| Educational Intelligence | Internal Alpha `ENABLE_EI_*` flags |
| Digital Twin boundary | Settings “Learning profile status”; Twin Progress gated off |

---

## Findings

---

### FINDING-001 — Mastery formula auto-writes Study Progress

**Educational Surface:** Adaptive Learning / Study Progress / Estimated Mastery  

**Description:**  
When Estimated Mastery reaches a numeric threshold, the product marks the topic as completed studying without a Study Progress declaration or coverage-mission completion intent.

**Current Behaviour:**  
`AdaptiveLearningService.update_mastery_after_attempt` sets `progress.completed = True` when `mastery_score >= 70`.

**Expected Behaviour:**  
Study Progress advances only by student declaration or lawful coverage completion (EL-001, Constitution IV.1 / VIII.1 / VIII.6). Estimated Mastery must never author coverage truth.

**Educational Impact:**  
Students can appear to have “completed studying” because a score crossed a threshold — collapsing coverage with competence and inventing journey progress from understanding estimates.

**Constitution Reference(s):** Article III §5; Article IV.1, IV.8, IV.14; Article VIII rules 1, 6, 14  

**Logic Registry Reference(s):** EL-001; EL-007; Educational State Ownership Matrix (Study Progress vs Estimated Mastery)  

**Governance Review Category(ies):** A, B, D, E, G, H  

**Severity:** Critical  

**Recommendation:**  
Educationally restore strict ownership: Estimated Mastery may inform review advice; it must never mint Study Progress. Coverage completion must remain a coverage event with student-honest meaning.

---

### FINDING-002 — Student-felt confidence can alone mint Mastered stage

**Educational Surface:** Student Confidence / Estimated Mastery / Mission Review  

**Description:**  
The mission review form stores student-felt “Very Confident” as internal value `"Mastered"`, which is weighted at 30% in the mastery formula and maps to numeric 100. With accuracy absent, confidence alone can drive stage `Mastered` (≥90).

**Current Behaviour:**  
`MissionReviewForm` choices include `("Mastered", "Very Confident")`. `CONFIDENCE_NUMERIC["Mastered"] = 100`. `calculate_mastery_score` weights confidence at 0.30 and redistributes weight when accuracy is missing. `determine_stage` returns `STAGE_MASTERED` at ≥90.

**Expected Behaviour:**  
Self-report is Rank-D soft signal only; it must never alone author “Mastered” / high Estimated Mastery certainty (Constitution IV.10, V §§3–4, VIII.3). Vocabulary for felt confidence must not reuse mastery tokens.

**Educational Impact:**  
Students can manufacture attainment theatre by reporting high felt confidence, training false exam readiness.

**Constitution Reference(s):** Article II §1.3, §1.6–7; Article III §§3–5; Article IV.8, IV.10; Article V §§2–5; Article VII §§3–4; Article VIII rules 3, 10–12  

**Logic Registry Reference(s):** EL-005; EL-007; EL-010; Ownership Matrix (Student-felt Confidence vs Estimated Mastery)  

**Governance Review Category(ies):** A, C, D, F, H  

**Severity:** Critical  

**Recommendation:**  
Educationally separate felt-confidence vocabulary from mastery tokens; treat self-report as calibrated soft input that cannot alone justify high Estimated Mastery language or Mastered stages.

---

### FINDING-003 — Mission completion still recalculates Estimated Mastery

**Educational Surface:** Mission Completion / Educational Evidence / Estimated Mastery  

**Description:**  
IA-004 correctly stopped `_apply_mission_topic_progress` from inventing mastery scores, but the live complete path still creates a `StudyAttempt` and always runs mastery update whenever a topic is linked.

**Current Behaviour:**  
`complete_mission` → `LearningService.create_study_attempt(...)` → `_update_progress_from_attempt` / `mark_reviewed` → `AdaptiveLearningService.update_mastery_after_attempt`. Bare completion with no scored questions still increments revision and may move `mastery_score` via baseline/revision logic, then `_apply_mission_topic_progress` sets Study Progress + `confidence="High"`.

**Expected Behaviour:**  
Mission completion updates mission lifecycle and may update Study Progress for coverage work. Estimated Mastery updates only from lawful Educational Evidence of sufficient quality — never from the completion checkbox alone (EL-004, Article V §4, VIII.1).

**Educational Impact:**  
Completion and estimate succession remain coupled. Students hear “completion ≠ mastery” while the system quietly revises mastery scores on complete.

**Constitution Reference(s):** Article III §§2–5; Article IV.4, IV.5, IV.14; Article V §2, §4; Article VIII rules 1, 7, 10–12  

**Logic Registry Reference(s):** EL-004; EL-005; EL-007  

**Governance Review Category(ies):** A, B, D, G  

**Severity:** High  

**Recommendation:**  
Educationally isolate Mission Completion from mastery succession unless a distinct, student-visible practice/assessment observation of recognised quality is recorded.

---

### FINDING-004 — Study Progress co-writes `confidence="High"`

**Educational Surface:** Study Plan / Mission Completion / Student Confidence  

**Description:**  
Coverage events write a system confidence field (`"High"`) onto the same progress row students associate with journey status, conflating felt/educational confidence with Study Progress.

**Current Behaviour:**  
Wizard init, `_sync_completed_topics`, and `_apply_mission_topic_progress` set `confidence="High"` whenever a topic becomes completed studying.

**Expected Behaviour:**  
Study Progress answers coverage only. Student-felt confidence is separately owned; educational warrant is Twin/estimate-owned (Constitution IV.1, IV.10; EL-001 residual; VIII.3).

**Educational Impact:**  
Coverage looks like rising confidence/competence. Educators cannot defend “High” as coverage metadata.

**Constitution Reference(s):** Article III §5; Article IV.1, IV.10; Article VII §4; Article VIII rules 3, 6  

**Logic Registry Reference(s):** EL-001; EL-010; Ownership Matrix  

**Governance Review Category(ies):** A, D, E, F  

**Severity:** High  

**Recommendation:**  
Educationally stop using confidence fields as Study Progress side-effects. Coverage writes coverage; confidence writes confidence only when the student reports it.

---

### FINDING-005 — Dual readiness meanings under “Learning Progress”

**Educational Surface:** Dashboard / Analytics / Readiness / Learning Progress  

**Description:**  
Two different readiness definitions compete. Dashboard “Learning Progress” prefers coverage-weighted syllabus complete, else falls back to a composite that embeds average mastery as “average topic progress”. Analytics KPI “Readiness” uses the composite.

**Current Behaviour:**  
`ReadinessService.calculate_readiness` = weighted completed syllabus % only. `get_overall_readiness` = coverage 50% + avg mastery 30% + review discipline 20%, counting `STAGE_MASTERED`. Dashboard template switches between them under one title.

**Expected Behaviour:**  
Learning Progress is a journey metric from Study Progress + syllabus scope — not Estimated Mastery (Constitution IV.2; VIII.14). Readiness is a preparedness judgement that must not silently mix coverage theatre with mastery or become next-action authority (IV.9; VIII.8). One educational story across surfaces (Category G).

**Educational Impact:**  
Students see different “how prepared / how far” numbers depending on surface and plan presence, and may read coverage as understanding.

**Constitution Reference(s):** Article III §1; Article IV.2, IV.9; Article VIII rules 8, 14; Article VII  

**Logic Registry Reference(s):** EL-001; EL-011; FEL-004 (reserved readiness expansion); EL-010  

**Governance Review Category(ies):** C, E, F, G, H  

**Severity:** High  

**Recommendation:**  
Educationally choose one student-facing meaning for Learning Progress and one for Readiness; never present mastery-derived composites as syllabus journey progress without estimate labelling and disclosure.

---

### FINDING-006 — Advisory recommendation can disagree with Learning Mode without disclosure

**Educational Surface:** Recommendations / Dashboard / Mission / Educational Intelligence  

**Description:**  
Under Internal Alpha, Learning Mode owns persisted Today’s Mission (`ENABLE_EI_MISSIONS=False`), while `ENABLE_EI_RECOMMENDATIONS=True` projects an EI card that may name a different educational focus. Family-generic Why copy and CTA “Start Today's Session” do not reliably label “optional review (not today’s learning)”. Legacy weak-topic lists remain when EI compose is absent.

**Current Behaviour:**  
EI card is presentation-only (does not mutate ORM mission). Titles/reasons map by `ActionFamily`. No student Accept/Dismiss HTTP write path. Legacy `RecommendationService` uses “critically weak topic(s)” and absolute confidence phrases (“complete exam confidence”).

**Expected Behaviour:**  
Intelligence advises; it does not silently commandeer. Divergence from Current Learning Topic must be labelled honestly (Constitution II §1.9; VI §4; EL-008; EL-009).

**Educational Impact:**  
Re-creates week_001 trust failure mode: students experience two authorities for “what should I do today?”.

**Constitution Reference(s):** Article II §1.4, §1.9; Article VI §§1–4; Article VII; Article VIII rules 7–9, 13, 15  

**Logic Registry Reference(s):** EL-002; EL-003; EL-008; EL-009; EL-010  

**Governance Review Category(ies):** A, B, C, F, G, H  

**Severity:** High  

**Recommendation:**  
Educationally enforce one coherent daily story: either bind advisory focus to Current Learning Topic for Version 1.0, or mandatorily frame non-mission advice as optional and non-authoritative.

---

### FINDING-007 — Estimated Mastery lacks evidence-density gate for high stages

**Educational Surface:** Estimated Mastery / Educational Evidence / Adaptive Learning  

**Description:**  
High Estimated Mastery / `STAGE_MASTERED` can appear from sparse attempt history (including confidence-heavy or single-session patterns). Constitutional accumulation rule is not enforced operationally.

**Current Behaviour:**  
`update_mastery_after_attempt` averages available attempts but does not require minimum attempt count, spacing, or Rank-A/B density before high stages. `has_estimated_mastery` gates display on `average_accuracy is not None` — preventing coverage-only display, but not thin objective history once any accuracy exists.

**Expected Behaviour:**  
Estimated Mastery absent until sufficient attempt/assessment evidence; high stages require accumulation (Constitution II §1.6; IV.8; V §5; VIII.10; EL-007).

**Educational Impact:**  
False confidence near exam-relevant topics; students mistake early practice luck for mastery.

**Constitution Reference(s):** Article II §1.3, §1.6–7; Article III; Article IV.8; Article V §§3–5; Article VIII rules 10–12  

**Logic Registry Reference(s):** EL-005; EL-007  

**Governance Review Category(ies):** C, D, H  

**Severity:** High  

**Recommendation:**  
Educationally require evidence density before high Estimated Mastery language; prefer honest absence over early Mastered stages.

---

### FINDING-008 — Educational Evidence domain not on the live student estimate path

**Educational Surface:** Educational Evidence / Digital Twin / Estimated Knowledge / Estimated Mastery  

**Description:**  
Constitutional Educational Evidence → Twin Knowledge State → estimates is not the live student path. Product interim path is `StudyAttempt` averages → `TopicProgress.mastery_score`, while Twin Progress remains gated (`ENABLE_EI_PROGRESS=False`).

**Current Behaviour:**  
Domain evidence packages exist; mission/learning routes do not hand off immutable Educational Evidence contracts into Twin succession for student estimates. Student copy refers to “study evidence” for the hybrid product path.

**Expected Behaviour:**  
Knowledge-oriented beliefs evolve only from lawful Educational Evidence interpretation (Article V; EL-005; EL-006; EL-012). Recommendations and completion checkboxes are not evidence of understanding.

**Educational Impact:**  
Understanding claims rest on an interim score store that can violate evidence ranking and Twin/Study Plan separation.

**Constitution Reference(s):** Article III; Article IV.5–8; Article V (entire); Article VIII rules 7, 10–12, 14  

**Logic Registry Reference(s):** EL-005; EL-006; EL-007; EL-012  

**Governance Review Category(ies):** B, D, E  

**Severity:** High  

**Recommendation:**  
Educationally treat the interim product estimate store as transitional debt: either subordinate it to Evidence ranking with honest understatement, or withhold strong estimate claims until Twin-backed succession is student-ready under messaging discipline.

---

### FINDING-009 — Plan delete silently erases Study Progress

**Educational Surface:** Study Plan / Study Progress / Learning continuity  

**Description:**  
Deleting a Study Plan hard-deletes curriculum-linked `TopicProgress`, destroying rightful coverage memory while preserving attempts/missions.

**Current Behaviour:**  
`StudyPlanService.delete_study_plan` deletes `TopicProgress` rows for the plan’s curriculum topics.

**Expected Behaviour:**  
Changing or removing study context must not silently erase rightful Study Progress without educational justification (Constitution II §1.8; EL-001; EL-011; VIII continuity concerns).

**Educational Impact:**  
Students lose “what I have completed studying” when managing plans — punitive discontinuity that breaks coach trust.

**Constitution Reference(s):** Article II §1.8; Article IV.1; Article IX §4  

**Logic Registry Reference(s):** EL-001; EL-011  

**Governance Review Category(ies):** E, G, H  

**Severity:** High  

**Recommendation:**  
Educationally preserve Study Progress across plan archive/delete unless the student explicitly authorises coverage reset with clear consequence language.

---

### FINDING-010 — Shallow Why and suppressed warrant honesty

**Educational Surface:** Recommendations / Educational Messaging / Educational Intelligence  

**Description:**  
Domain EI has reason codes and warrant postures, but student Why copy is family-generic and thin-warrant warnings are suppressed. Explainability remains off (`ENABLE_EI_EXPLAINABILITY=False`).

**Current Behaviour:**  
`recommendation_card_builder._STUDENT_REASON_BY_FAMILY` supplies generic reasons. Cold-start / thin-warrant honesty does not reach students.

**Expected Behaviour:**  
Guidance answers what / why / next in plain educational language; uncertainty named when warrant is thin (Constitution II §1.4, §1.7; III §3–4; VII; EL-008; EL-010).

**Educational Impact:**  
Advice feels arbitrary even when Learning Mode is correct — trust cannot deepen beyond “it told me to”.

**Constitution Reference(s):** Article II §1.4, §1.7; Article III §§3–4; Article VII; Article VIII rules 11–12, 15  

**Logic Registry Reference(s):** EL-008; EL-010  

**Governance Review Category(ies):** C, F, H  

**Severity:** Medium  

**Recommendation:**  
Educationally require student-safe, topic-truthful reasons and plain uncertainty language before treat recommendations as trust-bearing coaching.

---

### FINDING-011 — Residual forbidden / borderline student language

**Educational Surface:** Educational Messaging / Mission / Dashboard / Analytics  

**Description:**  
IA-003 removed catastrophic engineering leaks (`evidence_creating`, Digital Twin naming, entity ids). Residuals remain: “study evidence” on mission/dashboard/analytics; form internal `"Mastered"`; legacy “weak topic(s)” / absolute confidence phrases; soft “estimated knowledge” sometimes synonymous with mastery score.

**Current Behaviour:**  
Mission why: “Estimated Mastery grows from study evidence over time.” Tooltips: “Estimated Mastery from study evidence.” Settings correctly use “Learning profile status”.

**Expected Behaviour:**  
Prefer “practice results” / “study checks”; forbid Mastered as completion/confidence theatre; map strength language to estimates (Constitution VII; EL-010).

**Educational Impact:**  
Mild but real vocabulary blur; “study evidence” is better than week_001 jargon but still not plain educational speech.

**Constitution Reference(s):** Article VII §§2–5; Article III §4  

**Logic Registry Reference(s):** EL-010; EL-012  

**Governance Review Category(ies):** F, C  

**Severity:** Medium  

**Recommendation:**  
Educationally finish vocabulary discipline on remaining student surfaces using Constitution-permitted families only.

---

### FINDING-012 — Estimated Knowledge and Estimated Mastery share one scalar

**Educational Surface:** Estimated Knowledge / Estimated Mastery / Analytics / Dashboard  

**Description:**  
Constitution separates Estimated Knowledge (IV.7) from Estimated Mastery (IV.8). Product presents one `mastery_score` under both “Estimated Mastery” and “estimated knowledge” wordings.

**Current Behaviour:**  
Plan view uses Estimated Mastery when `has_estimated_mastery`. Dashboard/analytics speak of “Strongest estimated knowledge” / “Estimated knowledge appears here…” using the same score.

**Expected Behaviour:**  
Distinct meanings and honest labelling; neither from Study Progress alone (EL-006, EL-007).

**Educational Impact:**  
Students cannot tell “how well I understand now” from “how confidently I have mastered” — analytics vocabulary oscillates without new warrant.

**Constitution Reference(s):** Article III §4; Article IV.6–8; Article VIII rule 14  

**Logic Registry Reference(s):** EL-006; EL-007  

**Governance Review Category(ies):** C, E, G  

**Severity:** Medium  

**Recommendation:**  
Educationally pick one Version 1.0 student construct (prefer Estimated Mastery with estimate framing) or distinguish both with separate warrant rules — do not use interchangeable marketing synonyms for one score.

---

### FINDING-013 — Coaching agency (Accept / Dismiss) not student-productized

**Educational Surface:** Recommendations / Student Control / Educational Intelligence  

**Description:**  
Domain and `RecommendationService.record_decision` support accept/dismiss, and Decision Journal can display history, but no student HTTP flow records coaching consent for live EI recommendations. CTA only navigates to mission.

**Current Behaviour:**  
EI card Accept affordance maps to navigation; no dismiss/defer control.

**Expected Behaviour:**  
Intelligence advises; student remains in control of advisory uptake without mutating mastery (Constitution II §1.9; EL-008 Future Evolution; coach not dictator posture).

**Educational Impact:**  
Without dismiss, the system cannot learn preference and students experience advice as non-negotiable chrome.

**Constitution Reference(s):** Article I §4; Article II §1.9; Article VI §4  

**Logic Registry Reference(s):** EL-008  

**Governance Review Category(ies):** F, H  

**Severity:** Medium  

**Recommendation:**  
Educationally productize Accept / Not today / Later as preference signals only — never as mastery or Study Progress writes.

---

### FINDING-014 — MissionOptimizer remains a silent third advisory engine

**Educational Surface:** Dashboard / Recommendations / Adaptive Learning  

**Description:**  
`MissionOptimizer.generate_balanced_mission` is still computed and passed toward dashboard context even though current `dashboard/index.html` does not render it — latent dual-authority risk.

**Current Behaviour:**  
Computed; not student-visible in current template.

**Expected Behaviour:**  
No unregistered or undeclared educational decision path that can resurface as mission-shaped authority (Registry authority rule; Article VI; Category B).

**Educational Impact:**  
Latent regression risk: a future template rewire could revive pre–IA-004 confusion.

**Constitution Reference(s):** Article VI; Article IX §3  

**Logic Registry Reference(s):** EL-003; EL-008; EL-009  

**Governance Review Category(ies):** B, G  

**Severity:** Low  

**Recommendation:**  
Educationally retire or quarantine non–Learning Mode mission-shaped generators from Version 1.0 student authority surfaces.

---

### FINDING-015 — Learning Mode mission authority itself is constitutionally aligned

**Educational Surface:** Current Learning Topic / Today's Mission / Learning Mode  

**Description:**  
Positive finding recorded for balance: Version 1.0 Learning Mode mission topic selection follows first incomplete syllabus leaf; review/weak preemption deferred; missions plan-scoped.

**Current Behaviour:**  
`PlanningService._select_topic_for_today` uses Learning Mode + `CurriculumService.get_next_incomplete_topic`. IA-004 tests guard regression.

**Expected Behaviour:**  
Matches Constitution Article VI and EL-002 / EL-003 / EL-009.

**Educational Impact:**  
Primary daily commitment can earn trust if advisory dual-path and estimate integrity debts are closed.

**Constitution Reference(s):** Article II §1.1; Article IV.3–4; Article VI  

**Logic Registry Reference(s):** EL-002; EL-003; EL-009  

**Governance Review Category(ies):** A, B, G (compliant subset)  

**Severity:** N/A (strength)  

**Recommendation:**  
Preserve Learning Mode as sole Version 1.0 mission topic authority until Constitution Article X authorises another mode.

---

### FINDING-016 — Digital Twin naming boundary largely intact

**Educational Surface:** Digital Twin Boundary / Settings / Educational Messaging  

**Description:**  
Positive finding: students do not see “Digital Twin” labelling; settings use Learning profile status presence labels; Progress/Explainability depth gated.

**Current Behaviour:**  
Consistent with EL-012 / IA-003 for naming invisibility.

**Expected Behaviour:**  
Matches Constitution II §1.10; VII §5; EL-012.

**Educational Impact:**  
Avoids research-infrastructure theatre that destroyed week_001 comprehension.

**Constitution Reference(s):** Article II §1.10; Article VII §5; Article VIII rule 14  

**Logic Registry Reference(s):** EL-012; EL-010  

**Governance Review Category(ies):** F (compliant subset)  

**Severity:** N/A (strength)  

**Recommendation:**  
Preserve invisibility when enabling Progress/Explainability; student experience remains estimates and guidance only.

---

## Governance Review (Categories A–H)

Ratings use EGI-003 §4. Points use EGI-003 §5 weights.

---

### Category A — Constitution Compliance (Weight 15)

**Rating:** NON-COMPLIANT  
**Points:** 0 / 15  

**Evidence:**  
Automatic triggers fire: mastery asserted via confidence-weighted formula including confidence-alone path (FINDING-002); Study Progress mixed with Estimated Mastery via auto-complete `completed=True` at mastery ≥70 (FINDING-001); Learning Progress / readiness surfaces can embed mastery under journey language (FINDING-005). Learning Mode mission authority itself complies (FINDING-015) but does not clear automatic triggers.

| Question | Answer |
|----------|--------|
| A1 Comply with Constitution? | No — integrity and state-meaning violations on understanding/coverage spines |
| A2 Redefine terminology? | Effectively yes in places (confidence/Mastered; Learning Progress vs composite) |
| A3 New educational concepts? | No new constitutional concepts; interim estimate store behaves as undeclared hybrid |
| A4 Amended first? | N/A — behaviour should comply without amendment |

---

### Category B — Logic Registry Compliance (Weight 15)

**Rating:** NON-COMPLIANT  
**Points:** 0 / 15  

**Evidence:**  
Ownership matrix violated: estimate path writes Study Progress (FINDING-001). Mission Completion constraint “must not write Estimated Mastery from completion alone” violated by live complete → attempt → mastery update coupling (FINDING-003). Registry residuals correctly document several gaps; they are debt, not licence. Learning Mode selection follows EL-002/003/009.

| Question | Answer |
|----------|--------|
| B1 Follow registered logic? | Partial on Learning Mode spine; no on estimate/completion ownership |
| B2 Logic changed without Registry? | Behavioural divergences persist without Registry authorisation of meaning |
| B3 Registry updated before approval? | Gaps recorded, not authorised as compliant |
| B4 EL-IDs identified? | Yes — EL-001–EL-012 reviewed |

---

### Category C — Educational Truth (Weight 15)

**Rating:** PARTIAL  
**Points:** 7.5 / 15  

**Evidence:**  
Lawful types dominate Learning Mode narration (Observed/Derived facts for coverage and mission). Estimated Mastery gating (`has_estimated_mastery`) is directionally correct. Residual unlawful/theatrical claims remain: legacy absolute confidence phrases; interchangeable Estimated Knowledge / Mastery wording; advisory focus without always classifying divergent advice as Educational Advice distinct from mission authority (FINDING-006, 011, 012).

| Question | Answer |
|----------|--------|
| C1 Four claim types only? | Mostly on core path; residuals outside / blurred |
| C2 Estimates identified? | Often for mastery labels; uneven elsewhere |
| C3 Advice as advice? | Incomplete when topic diverges |
| C4 Statements outside four types? | Yes — legacy absolute confidence phrases |

---

### Category D — Evidence Integrity (Weight 15)

**Rating:** NON-COMPLIANT  
**Points:** 0 / 15  

**Evidence:**  
Automatic triggers: self-reported confidence alone can author Mastered stage (FINDING-002); completion path updates mastery scores (FINDING-003); mastery formula can write Study Progress (FINDING-001). Evidence domain not live (FINDING-008). Accumulation rule not operational for high stages (FINDING-007).

| Question | Answer |
|----------|--------|
| D1 Claim→evidence link? | Weak for estimate claims |
| D2 Completion→mastery incorrectly? | Yes |
| D3 Time⇒learning incorrectly? | Limited (revision baseline path) — secondary |
| D4 Confidence⇒knowledge incorrectly? | Yes |
| D5 Single attempt minting? | Possible for high stages |

---

### Category E — State Ownership (Weight 10)

**Rating:** PARTIAL  
**Points:** 5 / 10  

**Evidence:**  
Learning Mode mission ownership is single and sound (FINDING-015). Broken owners: Study Progress writable from estimate engine; dual readiness definitions; dual estimate stores (product mastery vs Twin); Confidence field overloaded (FINDING-001, 004, 005, 008).

| Question | Answer |
|----------|--------|
| E1 One owner per state? | Not for Study Progress vs estimates; readiness ambiguous |
| E2 Duplicated conflicting writers? | Yes — coverage vs mastery writers |
| E3 Conflicting authority for same question? | Yes — readiness / progress questions; advisory vs mission “what now?” |

---

### Category F — Student Communication (Weight 10)

**Rating:** PARTIAL  
**Points:** 5 / 10  

**Evidence:**  
IA-003 FULL for catastrophic jargon removal; Twin naming OK (FINDING-016). Residuals: “study evidence”, generic Why, suppressed thin-warrant honesty, Mastered form token, overconfident legacy rec phrases (FINDING-010, 011, 013).

| Question | Answer |
|----------|--------|
| F1 Plain educational language? | Mostly; residues remain |
| F2 What clear? | Mission yes; advisory sometimes muddy |
| F3 Why clear? | Often generic |
| F4 What next clear? | Mission path clear; advisory CTA can mislead |
| F5 Avoid false certainty? | Incomplete |

---

### Category G — Educational Consistency (Weight 10)

**Rating:** PARTIAL  
**Points:** 5 / 10  

**Evidence:**  
Mission surface and Learning Mode persistence agree. Dashboard/analytics readiness diverge (FINDING-005). EI advisory can disagree with mission without mandatory disclosure (FINDING-006). Plan delete breaks progress continuity (FINDING-009). Study Plan coverage vs Estimated Mastery badges are largely consistent on plan view.

| Question | Answer |
|----------|--------|
| G1 One educational story? | No across all surfaces |
| G2 Advisory divergence disclosed? | Not reliably |
| G3 Metric label discipline? | Partial |

---

### Category H — Educational Integrity (Weight 10)

**Rating:** PARTIAL  
**Points:** 5 / 10  

**Evidence:**  
Learning Mode and Study Progress honesty improvements would pass an educator review for the mission spine. Confidence→mastery and auto-complete coverage would fail educator review. A reasonable student can still believe high confidence or a completion event improved mastery more than constitution allows. Trust > optimisation is declared but advisory dual-path continues optimisation risk.

| Question | Answer |
|----------|--------|
| H1 Trust rising? | Mixed — improved since week_001; residual distrust modes remain |
| H2 Educator agreement? | No for estimate/confidence paths |
| H3 Student misunderstanding risk? | Yes — material |
| H4 Trust over optimisation? | Incomplete |

---

## Scoring

### Educational Governance Score

| Category | Rating | Weight | Points |
|----------|--------|--------|--------|
| A Constitution Compliance | NON-COMPLIANT | 15 | 0 |
| B Logic Registry Compliance | NON-COMPLIANT | 15 | 0 |
| C Educational Truth | PARTIAL | 15 | 7.5 |
| D Evidence Integrity | NON-COMPLIANT | 15 | 0 |
| E State Ownership | PARTIAL | 10 | 5 |
| F Student Communication | PARTIAL | 10 | 5 |
| G Educational Consistency | PARTIAL | 10 | 5 |
| H Educational Integrity | PARTIAL | 10 | 5 |
| **Total** | | **100** | **27.5 → reported 28 / 100** |

**Score band (EGI-003 §5):** 0–49 Failed governance  

**Formal outcome under EGI-003 §6:** **REJECTED**  
(Because Categories A, B, and D are NON-COMPLIANT and automatic NON-COMPLIANT triggers remain open.)

Rounding: display score **28 / 100** (exact sum 27.5).

### Overall Educational Alignment Score

Surface-balanced alignment (including strengths FINDING-015/016 and debts FINDING-001–014), distinct from Governance Score:

**42 / 100 — Weak educational alignment**

Interpretation: Learning Mode / Twin invisibility / Study Progress checkbox honesty raise the floor; Evidence Integrity and ownership collapses prevent moderate-or-better alignment.

### Overall Constitution Compliance

**NON-COMPLIANT** — automatic Article VIII / IV ownership and truth triggers remain open despite Article VI Learning Mode compliance on the mission path.

### Overall Logic Registry Compliance

**NON-COMPLIANT** — EL-001 / EL-004 / EL-007 operational constraints violated by live estimate and completion coupling; EL-002 / EL-003 / EL-009 Learning Mode path aligned.

### Educational Readiness for Version 1.0

**NOT READY**

EGI-003 §7 Educational Release Gate requires outcome **APPROVED**, Categories A–D **FULL**, Governance Score ≥ 90, and no open conditions. Present state is **REJECTED** with A/B/D NON-COMPLIANT.

---

## Prioritised Implementation Backlog

Ordered strictly by educational impact. Each capability solves **one** educational problem. Directions only — no implementation design.

| Order | Capability ID | Title | Educational Problem | Why it matters | Dependencies | Complexity |
|------:|---------------|-------|---------------------|----------------|--------------|------------|
| 1 | EGI-004 | Enforce Study Progress ≠ Estimated Mastery ownership | Mastery formulae auto-mark topics completed studying (FINDING-001) | Coverage truth is the syllabus spine; estimate-authored coverage destroys Learning Mode honesty | None (constitutional already) | Medium |
| 2 | EGI-005 | Decouple student-felt confidence from mastery tokens | `"Mastered"` / Very Confident can alone mint Mastered stages (FINDING-002) | High-stakes exams punish manufactured self-belief certificates | EGI-004 preferred first to avoid substitute paths | Medium |
| 3 | EGI-006 | Isolate Mission Completion from mastery succession | Completing a mission recalculates Estimated Mastery (FINDING-003) | Students cannot trust “completion ≠ mastery” messaging while succession couples | EGI-004; Evidence ranking clarity (EGI-008) | Medium |
| 4 | EGI-007 | Unify daily advisory with Learning Mode narration | EI/legacy advice can name a different focus without optional-review disclosure (FINDING-006) | Week_001 trust collapse pattern remains possible | Learning Mode spine (already present) | Medium |
| 5 | EGI-008 | Require evidence density before high Estimated Mastery | Sparse history can show high mastery stages (FINDING-007) | False readiness near exam topics | EGI-005; EGI-006 | High |
| 6 | EGI-009 | Unify student-facing Readiness vs Learning Progress meanings | Dual readiness definitions under Learning Progress / Analytics (FINDING-005) | One incoherent preparedness story across Dashboard vs Analytics | Constitution IV.2/IV.9 meaning (already) | Medium |
| 7 | EGI-010 | Stop coverage co-writing confidence fields | Study Progress writes `confidence="High"` (FINDING-004) | Coverage looks like competence | EGI-005 | Low |
| 8 | EGI-011 | Preserve Study Progress on plan delete/archive | Plan delete wipes TopicProgress (FINDING-009) | Continuity of rightful coverage is constitutional | EL-011 continuity posture | Medium |
| 9 | EGI-012 | Subordinate interim estimates to Evidence ranking honesty | Live path bypasses Educational Evidence → Twin succession (FINDING-008) | Understanding claims lack lawful observational chain | Twin Progress messaging discipline; EL-005 | High |
| 10 | EGI-013 | Student-safe factor-level Why + thin-warrant honesty | Generic Why; suppressed uncertainty (FINDING-010) | Explainability is trust fuel | EGI-007 (narration consistency first) | High |
| 11 | EGI-014 | Productize recommendation Accept / Not today / Later | No student coaching-consent loop (FINDING-013) | Coach metaphor requires agency without mastery mutation | EGI-007 | Medium |
| 12 | EGI-015 | Finish student vocabulary residue cleanup | “study evidence”, weak-topic, absolute confidence phrases (FINDING-011) | Remaining speech blur after IA-003 | EL-010 | Low |
| 13 | EGI-016 | Clarify Estimated Knowledge vs Estimated Mastery presentation | One scalar sold as two concepts (FINDING-012) | Prevent journey/understanding label oscillation | EGI-008 / EGI-012 | Medium |
| 14 | EGI-017 | Quarantine latent non–Learning Mode mission generators | MissionOptimizer still computed (FINDING-014) | Prevent silent authority regression | EGI-007 | Low |

---

## Version 1.0 Readiness Conclusion

### NOT READY

**for Internal Alpha educational deployment.**

**Justification under the Governance Standard (EGI-003):**

1. Categories **A, B, and D** are **NON-COMPLIANT** with open automatic triggers (Study Progress authored by mastery formulae; confidence-alone Mastered stages; completion→mastery succession).
2. Educational Governance Score **28 / 100** falls in the Failed band (< 50) → outcome **REJECTED** (§6).
3. Internal Alpha may proceed for **engineering testing** only if Architecture Office accepts time-bounded risk (§7 relationship note). That is not educational deployment confidence. Educational deployment requires at least **APPROVED WITH CONDITIONS** (score ≥ 75; no A–D NON-COMPLIANT) with conditions owned and gated — currently unavailable.
4. Version 1.0 Educational Release Gate additionally requires **APPROVED**, A–D **FULL**, score ≥ 90 — far from current state.

**Minimum educational conditions before reconsidering Internal Alpha educational deployment**

Clear **EGI-004, EGI-005, EGI-006, EGI-007** (ownership separation, confidence decoupling, completion isolation, advisory narration consistency), then re-run Categories A–D under this Standard.

---

## Known Strengths

1. **Learning Mode mission authority** is constitutionally correct and regression-tested (FINDING-015 / EL-009).
2. **Study Progress checkboxes** no longer present Mastered as coverage badges; Estimated Mastery display is gated on attempt-derived accuracy presence (IA-004 direction).
3. **Digital Twin naming invisibility** and IA-003 engineering-jargon removal restored basic speech dignity (FINDING-016).
4. **Curriculum-first / deterministic cores** remain free of black-box LLM mission selection.
5. **Governance stack itself** (Constitution + Registry + Review Standard) now provides an objective baseline absent from EPA-001’s informal EP-xxx scale.

## Known Weaknesses

1. **Evidence / estimate integrity collapse** — confidence and completion still feed mastery theatre (Critical/High findings 001–003, 007–008).
2. **Ownership blur** — Study Progress writable from estimates; confidence fields overloaded; dual readiness.
3. **Cross-surface story conflict** — advisory vs Learning Mode; Dashboard vs Analytics readiness.
4. **Thin coaching explainability and agency** — generic Why; no Accept/Dismiss product loop.
5. **Plan continuity** — delete destroys rightful Study Progress.

---

## Relationship to EPA-001

`knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md` remains a useful historical diagnostic. **This V2 document is the official educational baseline** for remaining Version 1.0 development because it binds every finding to Constitution Articles, Logic Registry IDs, and Governance Categories with scored release-gate impact.

---

## Automatic Trigger Check (EGI-003)

| Trigger | Status |
|---------|--------|
| Mastery from completion / confidence / time alone | **OPEN** (FINDING-001, 002, 003) |
| Adaptive interruption silently replacing Learning Mode | Closed (Learning Mode owns persistence) |
| Student-editable mastery as verified fact checkbox | Closed on study-plan coverage UI |
| Mixing Study Progress / Learning Progress with Estimated Mastery | **OPEN** (FINDING-001, 005) |
| Unregistered educational decision path students rely on | Partial — latent MissionOptimizer Low risk |
| Ownership matrix violated | **OPEN** (FINDING-001) |
| Estimates as validated proof / advice as silent mission replacement | **OPEN residual** (FINDING-002, 006) |
| Self-report alone authorizing mastered language | **OPEN** (FINDING-002) |
| Dashboard different Today’s Mission without advisory framing | Persistence OK; advisory dual-path **OPEN residual** (FINDING-006) |

---

## Method Notes

- Assessed **current implementation behaviour**, not roadmap aspiration.
- Student-facing paths weighted over unused domain packages when judging trust.
- Internal Alpha flag contract treated as live educational contract: Recommendations ON; Missions / Explainability / Progress OFF.
- No Constitution, Registry, Governance Standard, or application code was modified for this deliverable.

---

## Return

**Stop after this report.**  
**Return for Architecture Review.**  
**Do not begin implementation.**
