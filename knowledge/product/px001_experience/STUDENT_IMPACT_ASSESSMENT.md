# PX-001 — Student Impact Assessment

Template: `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | PX-001 (Educational Experience Integration) |
| **Title** | Surface Runtime C educational outputs on student Home / Journey |
| **Date** | 2026-07-27 |
| **Author** | Product engineering |
| **Student-visible change?** | Yes — gated to students with active Runtime C enrolment |
| **Production activation?** | Gated — requires Runtime C enrolment (PI-002A flags) |
| **Related KSI categories** | K2, K7, K8 |

---

## 1. Student problem

**Student problem:**  
The educational platform can already choose today’s topic, explain why, estimate duration, define completion, and project exam pacing — but students could not see any of that. After Published enrolment they landed on Home with empty or Runtime A-only chrome, so educational value felt invisible.

**Evidence:**  
EQ-001 completion report (UI non-goal); PI-002A enrolment redirects to Home without StudyPlan; PRD-001A roadmap P0/P1 “surface what already exists.”

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | Today’s topic + mission rationale on Home |
| How am I progressing? | Yes | Curriculum position + coverage % |
| What is stopping me? | Yes | Prerequisite status + honest pacing shortfall |
| What happens next? | Yes | Journey unlocks_next + suggested next action |

**Student benefit summary:**  
Runtime C students can read educational decisions without founder interpretation.

**Final Test:** Does this help students become better professionals? **Yes** — clearer syllabus-bound study decisions reduce wasted sessions.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Improves learning quality (not just activity)? | Yes — exposes objectives, completion definition, and honest non-mastery language |
| Curriculum-bound? | Yes — published syllabus position |
| Explainable? | Yes — EQ-001 envelopes rendered |

---

## 4. Success metrics

| Metric | How measured |
|---|---|
| Acceptance fields visible on Home/Journey | Automated HTTP markers in `test_acceptance.py` |
| Runtime A path unchanged without enrolment | Coexistence assertion |
| No Twin / cutover | Code review + fail-open Runtime C branch |

---

## 5. Risks

| Risk | Mitigation |
|---|---|
| Students with both runtimes see Runtime C Home | Documented coexistence rule; legacy routes remain Runtime A |
| Mission session write path still Runtime A | Known limitation — visibility first |
| Over-claiming readiness | No mastery / Exam Ready claims from mission alone |

---

## 6. Assumptions

- Active Runtime C enrolment identifies the educational experience student.
- EQ-001 generation quality remains certified upstream.
- Information architecture (not redesign) is sufficient for founding-cohort comprehension.
