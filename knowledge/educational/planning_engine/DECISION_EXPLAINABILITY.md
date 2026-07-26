# Decision Explainability

**Programme:** VI — Master Planner  
**Milestone:** MS004 — Planning Decision Engine  
**Classification:** Explainability contract for planning decisions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines how every planning decision produced by the Planning Decision Engine must be explained in **plain educational language**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` (EIP-003)
3. `PLANNING_DECISION_ENGINE.md`
4. `../planning/PLANNING_EXPLAINABILITY.md`
5. `../strategy/STRATEGY_EXPLAINABILITY.md`
6. `DECISION_PIPELINE.md`

This document specialises platform and planning explainability for **pre-schedule planning decisions**. It does not weaken claim-type rules (Observed Fact / Derived Fact / Evidence-backed Estimate / Educational Advice).

> **Explainability improves understanding of decisions already authorised.  
> It never invents educational certainty.**

---

## 1. Purpose

Future students should understand why Kwalitec selected each planning decision — before any timetable exists.

If revision is reserved, intensity is moderated, buffers appear, practice is emphasised, or a sitting is marked infeasible, the student must receive an educational reason they can believe.

Silent steering is forbidden.

---

## 2. Traceability Obligation (Architectural)

Every material planning decision must be traceable back to all three:

| Trace link | Student-facing role |
|------------|---------------------|
| **Student Educational Profile** | “Given where you are now…” |
| **Educational Strategy** | “Under this approach…” |
| **Educational Planning Model** | “Because a lawful plan must…” |

Internal IDs (PD-XX, ES-XX, O/C/D codes) may exist for algorithms and audits. They must not appear as student-facing jargon.

A decision with no educational justification is invalid — even if it would schedule conveniently.

---

## 3. Explainability Principles

1. **Every material decision explains itself.** Sequencing, intensity, revision, practice posture, buffers, recovery, milestones, risk mitigation, confidence protection, and feasibility outcomes are material.
2. **One primary educational reason** per decision surface — not a dump of every internal factor.
3. **Facts and estimates stay distinct.** Coverage, hours, leave, and exam dates are plain; weakness/readiness language is estimated or suggested.
4. **Trade-offs are spoken aloud** when the Priority Model forced a choice.
5. **Conflicts name what changed** after missed study, leave, or replan.
6. **Internal machinery stays invisible.** No optimiser names, twin facets, score vectors, or registry IDs in student speech.
7. **Uncertainty is named** when Profile evidence is thin or defaults are in use.
8. **Advice does not commandeer Learning Mode** without disclosure.
9. **Infeasibility is first-class speech**, not a buried footnote.
10. **Strategy is speakable** — students may hear the approach name in plain language when it helps understanding.

---

## 4. Four-Question Contract (Planning Decisions)

Every material decision in the package must answer:

| # | Question | Guidance |
|---|----------|----------|
| 1 | **What** was decided? | Concrete educational posture (e.g. “revision reserved before the exam”, “steady intensity”) |
| 2 | **Why** educationally? | One primary reason tied to Profile + Strategy + Planning Model law |
| 3 | **What follows** if I honour it? | Forward consequence (keeps revision intact, rebuilds rhythm, protects foundations, …) |
| 4 | **Known vs estimated?** | Calendar/capacity/coverage facts vs estimated weakness/readiness |

Optional fifth when relevant:

| # | Question | When required |
|---|----------|---------------|
| 5 | **What changed?** | After replan, missed weeks, leave, strategy transition, or evidence shock |

---

## 5. Claim Types in Decision Speech

| Claim type | Decision examples | Student cue |
|------------|-------------------|-------------|
| Observed Fact | Exam date; declared weekly hours; leave dates; topic marked studied | Plain factual language |
| Derived Fact | Days remaining; coverage progress; capacity vs remaining work | Plain derived measure |
| Evidence-backed Estimate | “Estimated weaker on topic X from recent practice” | *Estimated* / *Suggested* |
| Educational Advice | Optional denser consolidation; preferred mock window; sitting counsel | *Recommended* / *Optional* where appropriate |

Forbidden speech patterns:

- “You have mastered topic X because we decided to revise it.”
- “You will pass if you follow these decisions.”
- “Our engine scored priority 0.82.”
- “We shuffled topics to keep you engaged.”
- Silent swap of tonight’s mission topic “because the decision package says so” without Learning Mode authority/disclosure.

---

## 6. Standard Explanation Patterns

Exact copy may evolve; educational meaning must not. Patterns map to PD-XX in `DECISION_PIPELINE.md`.

### 6.1 Topic sequencing (PD-01)

**Pattern:**  
“You study topics in the official syllabus order so later material builds on earlier foundations.”

**Trace sketch:** Profile coverage position → Strategy refuses skip-ahead → Planning Model sequencing law.

**Do not say:** “Personalised shuffle for engagement.”

---

### 6.2 Revision reservation (PD-03)

**Pattern:**  
“Revision is reserved before the exam so first-pass learning does not consume it.”

**When trade-off exists:**  
“We protect revision time even if that means some first-pass topics wait — finishing everything without revision would leave you underprepared.”

---

### 6.3 Study intensity (PD-06)

**Pattern:**  
“Daily study stays within a sustainable range so you can keep the plan.”

**Recovery colouring:**  
“Intensity is lower for now so you can rebuild a rhythm you can keep.”

**Do not say:** “We doubled your load because you missed days.”

---

### 6.4 Practice intensity (PD-05)

**Pattern:**  
“You’ve studied enough of this material to practise it hard and learn from the evidence.”

**Guard:** Practise only on studied scope; label estimates from practice outcomes.

---

### 6.5 Recovery allowance (PD-07)

**Pattern:**  
“After dense study (or time away), we plan lighter work so learning and energy can recover.”

**Do not say:** “Rest means you fell behind as a person.”

---

### 6.6 Buffer allocation (PD-08)

**Pattern:**  
“We leave spare capacity for life interruptions so a missed week does not collapse the whole journey.”

---

### 6.7 Milestone positioning (PD-09)

**Pattern:**  
“We set clear checkpoints — for example when first-pass sections complete and when revision becomes the main story — so progress stays visible.”

---

### 6.8 Risk mitigation (PD-10)

**Pattern:**  
“Given the time left and what remains, we are prioritising what still counts educationally and being honest about what no longer fits.”

**Do not say:** “You are statistically likely to fail.”

---

### 6.9 Confidence protection (PD-11)

**Pattern:**  
“We set work you can finish truthfully so confidence grows from kept study promises — not from empty reassurance.”

**Do not say:** “You’re definitely ready — trust the process.” (when warrant is thin)

---

### 6.10 Feasibility judgement (PD-13)

**Feasible pattern:**  
“Given your available hours and leave, this sitting can still support an honest study journey.”

**Infeasible pattern:**  
“At your current hours, this sitting is not feasible without changing hours, scope, or sitting — here are lawful options.”

Infeasibility explanations are mandatory when PD-13 fails.

---

### 6.11 Catch-up / compression (PD-16)

**Pattern:**  
“Because study was missed, we use spare capacity and adjust intensity rather than packing an impossible catch-up.”

**If escalating:**  
“Buffers are used up — continuing as before would be unrealistic, so we need to change scope or timing.”

---

### 6.12 Strategy binding

**Pattern:**  
“Your current approach is {plain strategy name} — {one-sentence tutor meaning} — because {Profile-based reason}.”

Strategy explainability detail: `../strategy/STRATEGY_EXPLAINABILITY.md`.

---

## 7. Narrating Priority Trade-offs

When the Priority Model forced a choice, explanations must name both goods and the winner:

| Trade-off | Example student speech |
|-----------|------------------------|
| Readiness vs full syllabus completion | “We protect revision even if some topics wait — a complete-looking march without revision is not honest readiness.” |
| Consistency vs intensity | “We keep a sustainable rhythm rather than heroic spikes you would abandon.” |
| Recovery vs acceleration | “We restart gently first; speed returns after the rhythm does.” |
| Retention vs speed | “We return to recent topics so earlier learning does not fade while you continue forward.” |
| Confidence vs workload | “We choose completable work over overload dressed as seriousness.” |

Never hide the loser of the trade-off.

---

## 8. Narrating Conflict Resolutions

After conflict playbooks in `DECISION_CONFLICT_RESOLUTION.md`, use the fifth question:

| Conflict | “What changed?” sketch |
|----------|------------------------|
| Limited time | “Your available hours are lower than the previous plan assumed.” |
| Late completion | “Coverage is behind relative to the exam date, so we triage.” |
| Missed study | “Study was missed; we replan without punishment load.” |
| Unexpected leave | “Leave removed study capacity; decisions were redesigned around what remains.” |
| Repeated failure | “Previous attempts mean we emphasise consolidation and honesty over false speed.” |

---

## 9. Package-Level Explainability

Beyond per-decision patterns, the Planning Decision Package as a whole should support a short student-facing summary:

1. **Where you are** (Profile, plain language)
2. **Approach we are taking** (Strategy)
3. **What we decided that matters most** (3–5 material decisions)
4. **What we are protecting** (usually revision, sustainability, truth)
5. **What would change the picture** (triggers for replan)

This summary is educational coaching speech — not a dump of the full PD catalogue.

---

## 10. Audit Checklist

Before a package is considered explainable:

- [ ] Every material PD has a primary educational reason
- [ ] Each reason traces to Profile + Strategy + Planning Model
- [ ] Claim types are lawful
- [ ] Trade-offs from the Priority Model are spoken
- [ ] Feasibility outcome is explicit
- [ ] No forbidden speech patterns
- [ ] No numeric weight / score language in student speech
- [ ] Strategy meaning is speakable if presented

---

## 11. Cross References

- `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` — platform four-question framework
- `../planning/PLANNING_EXPLAINABILITY.md` — long-horizon plan feature patterns
- `../strategy/STRATEGY_EXPLAINABILITY.md` — strategy narration
- `../student_profile/PROFILE_EXPLAINABILITY.md` — diagnosis narration
- `DECISION_PIPELINE.md` — PD-XX catalogue
- `DECISION_PRIORITY_MODEL.md` — trade-off authority
