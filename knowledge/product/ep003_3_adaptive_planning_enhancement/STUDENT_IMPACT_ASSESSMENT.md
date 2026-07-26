# Student Impact Assessment — EP-003.3

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-003.3 |
| **Title** | Adaptive Planning Enhancement |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | Yes — Today's Mission / daily plan surfaces carry why-this-plan, evidence, confidence, balanced priorities, and recovery-aware days when Twin planning is active |
| **Production activation?** | Gated — inherits existing Runtime A / Twin / daily-plan cutover flags; no new production-only flag |
| **Related KSI categories** | K1 (primary), K8 (supporting), K4 (personalisation), K7 (revision/recovery) |

**Template:** [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

---

## 1. Student problem

**Student problem:**

> Students often know they have a “plan for today” but not *why* those priorities were chosen, whether the day is realistically completable after a missed session, or how the plan relates to readiness and study tips. Planning usefulness is Partial (K1 = 62), with duration/coherence friction in the baseline.

**Evidence:**

> P-001.1 `BASELINE_KSI_ASSESSMENT.md` §3.1 (K1 = 62); EP-001.2 / EP-002.7 delivered Twin daily plans without P-001.2 schema; `mission_missed_count` unused pre-EP-003.3.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | One `suggested_next_action` from primary plan slot / mission |
| How am I progressing? | Partial | Plan judgement + change reasoning (not a full progress narrative) |
| What is stopping me? | Yes | Recovery mode after missed sessions; readiness-informed lighter load |
| What happens next? | Yes | Review point after mission completion or missed day |

**Student benefit summary:**

> Students get a clearer, evidence-backed explanation of today’s study priorities, balanced minute allocation across focuses, and a gentler recovery day after misses — without inventing a plan when none exists.

---

## 3. Learning benefit

- Protects spaced repetition (review) and weak-topic recovery before adding new progression after misses.
- Keeps Today’s Mission as plan authority while labelling alignment with readiness/tips.
- Improves trust via mandatory explanation schema (K8 support for K1).

---

## 4. Success metrics

| Metric | Target (estimated) | Measurement |
|---|---|---|
| Schema completeness on plan surfaces | 100% of quality-wrapped surfaces | Unit tests |
| Recovery activates when missed &gt; 0 | Deterministic | Assembler unit tests |
| Student comprehension of “why this plan” | Improve on dogfood | Pending live re-score |
| K1 category lift | +6 to +8 estimated | KSI impact assessment |

---

## 5. Risks to students

| Risk | Mitigation |
|---|---|
| Recovery day feels like punishment | Frame as rebuilding rhythm; keep due review; lighter load |
| Tip alignment confuses Mission authority | Copy states tips remain advisory |
| Cold start refusal feels empty | Honest refusal + activate-plan next action |

---

## 6. Assumptions

- Twin Foundation / daily-plan cutover flags remain the activation path for enriched adaptive plans.
- Legacy Learning Mode syllabus fidelity remains intentional (no silent weak interruption).
- Live KSI re-score will follow dogfood; this programme under-claims.

---

## 7. Architectural blast radius (supplement)

| Surface | Change |
|---|---|
| `PlanningService.build_daily_study_plan` | Quality schema + assembler recovery/balance |
| `PlanningService.get_dashboard_mission_surface` | Quality schema on cutover + legacy |
| `RuntimeAPresentationAdapter.mission_narrative` | Pass-through when schema complete |
| Readiness / Recommendation services | Unchanged owners; Planning consumes bare readiness + tip titles only |
