# EV-001 — Educational Validation Report

**Programme:** Educational Validation Programme EV-001  
**Phase:** Founder Educational Trust Validation  
**Environment:** Production — https://kwalitec.onrender.com  
**Live commit:** `613722cffa16e6badbdb3a1161e4feaa35fd02db`  
**Student:** ctshumba01@gmail.com  
**Subject:** CS1 (CS1) · Published · CERTIFIED_WITH_WARNINGS  
**Audit date:** 2026-08-01  
**Auditor stance:** IFoA tutor / examiner / curriculum reviewer / educational auditor  

**Authority cited:** RF-002 PASS · G1 Founder Validation · PRODUCT_BLUEPRINT.md · STUDENT_DIGITAL_TWIN.md · PRODUCT_EXPERIENCE_GUIDELINES.md · Version 1 Educational Principles  

**Constraint compliance:** Live deployment only as source of truth for student experience; production not modified or redesigned; observation and evidence only.

---

## One-question answer

**If a student follows Kwalitec every day until the examination, will they receive educational guidance of consistently high quality?**

**No.**

On the live CS1 journey for this student, educational quality is already insufficient at the current mission (4.2 GLM). Session pedagogy collapses to placeholders, Learning Episodes contain no teachable material, curriculum surfaces include a postal address as a topic, progress claims disagree with History/Revision, and recommendation explainability is boilerplate. Quality is not “good enough to improve later” — it fails the primary-study standard **now**, with further trust hazards still ahead.

---

## Journey position audited

```text
Enrolment / Choose Exam available
→ Baseline route presently redirects into study-plan wizard (not re-walked end-to-end today)
→ Active CS1 plan · Topic 13 of 15 · 80% first-pass claim · 255 days to exam
→ Today's Mission 4.2 GLM
→ Session overview + Reading activity (stuck)
→ Revision empty · History 0 sittings · Learning Journey empty
→ Decision Journal: 1.1 and 4.2 generic entries
→ Remaining: Singapore address node + 5.1 Bayesian
```

---

## Phase results (summary)

| Phase | Result | Headline |
|-------|--------|----------|
| 1 Mission audit | **Fail** | Syllabus-paste missions; weak narrative |
| 2 Curriculum alignment | **Fail** | Address node; LO shuffle; status incoherence |
| 3 Learning Episodes | **Fail** | Placeholder topic; empty reading; no advance |
| 4 Mission arc | **Fail** | Topic order OK; lived story broken |
| 5 Session timing | **Fail** | 1 h vs 30 min; depth empty |
| 6 Revision | **Fail** | Empty at 80% coverage |
| 7 Consistency | **Fail** | Generic from day-one journal; severe now |
| 8 Principles | **Fail** | Not tutor-like; explains platform; no memory feel |
| 9 Longitudinal trust | **Fail** | Confidence falls immediately and stays down |
| 10 Scores | See below | Overall confidence **Fail** |

---

## Phase 8 — Kwalitec principles (student-experienced)

| Principle question | Verdict | Live evidence |
|--------------------|---------|---------------|
| Feels like a personal tutor? | **No** | Placeholder session voice |
| Remembers previous learning? | **No** | Journey empty; History 0; journal vs home conflict |
| Every mission has purpose? | **Weak** | “Next incomplete topic” only |
| Recommendations feel intentional? | **No** | Identical “highest-value next step” |
| Avoids explaining the platform? | **No** | Mission≠mastery, readiness %, provisional copy |
| Guides rather than lectures? | **N/A/Fail** | Neither — empty guide |
| Educational continuity? | **Broken** | Address in remaining; 4.2 completed-yet-current |
| Remains calm? | **Partially** | Tone calm; content alarming |

---

## Educational quality scores (Phase 10)

Each score is /10. Evidence pointers refer to companion reports and `EV001_TRUST_BREAK_REGISTER.md`.

| Dimension | Score | Evidence anchor |
|-----------|------:|-----------------|
| Mission Quality | **2** | Home 4.2 = syllabus title; `EV001_MISSION_QUALITY_REPORT.md` |
| Learning Episode Quality | **1** | Session `lsr-18e4b384b9cc`; episode audit |
| Curriculum Fidelity | **3** | Map/Syllabus; address node; LO order |
| CMP Alignment | **2** | Truncated stems + publisher address contamination |
| Session Design | **2** | Skeleton OK; empty stages; stuck advance |
| Educational Progression | **4** | 1→4.2 topic spine sensible; narrative/status not |
| Revision Strategy | **1** | `/student/revision` empty at 80% |
| Consistency | **2** | Journal generics early; placeholders now |
| Tutor-like Behaviour | **1** | No teaching voice in session |
| Student Trust | **1** | Trust Break Register (14 entries) |
| **Overall Educational Confidence** | **1** | Cannot recommend primary reliance |

---

## Companion artefacts

| Deliverable | Path |
|-------------|------|
| Trust Break Register | `EV001_TRUST_BREAK_REGISTER.md` |
| Curriculum alignment | `EV001_CURRICULUM_ALIGNMENT_REPORT.md` |
| Mission quality | `EV001_MISSION_QUALITY_REPORT.md` |
| Learning episode audit | `EV001_LEARNING_EPISODE_AUDIT.md` |
| Longitudinal trust | `EV001_LONGITUDINAL_TRUST_REPORT.md` |
| Final recommendation | `EV001_FINAL_RECOMMENDATION.md` |

---

## What was intentionally not done

- No production repairs, redesigns, or curriculum republish  
- No source-code-led root-cause engineering (judgement from student surfaces)  
- No claim about local/dev behaviour — live only  

---

## Closing educational statement

Kwalitec’s live student path for CS1 currently behaves like a syllabus navigator with a broken lesson player — not like a tutor who can carry a candidate to the exam. An experienced IFoA tutor would **not** be comfortable telling a student to rely primarily on Kwalitec for this subject on this deployment.
