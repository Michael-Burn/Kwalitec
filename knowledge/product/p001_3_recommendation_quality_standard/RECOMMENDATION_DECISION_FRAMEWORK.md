# Recommendation Decision Framework

**Programme:** P-001.3 — Recommendation Quality Standard  
**Version:** 1.0  
**Status:** Active — permanent prioritisation authority for competing student-facing recommendations  
**Effective:** 2026-07-26  
**Companion:** [`RECOMMENDATION_QUALITY_STANDARD.md`](RECOMMENDATION_QUALITY_STANDARD.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Specify **how RecommendationService (and product reviewers) should prioritise competing recommendations** when more than one lawful tip is available.

The framework answers:

> Given several valid educational signals, which single primary recommendation should the student see *now*, and why?

It does **not** invent educational meaning. It ranks guidance already authorised under the Educational Recommendation Model, Programme VI warrants, and WS2 ownership / conflict disposition.

---

## 2. Hard gates (before ranking)

A candidate is **ineligible** as the primary student-facing recommendation if any gate fails:

| Gate | Fail condition |
|---|---|
| G1 Lawful warrant | No Programme VI / constitutional owner warrant; tip would invent meaning |
| G2 Correctness | Conflicts with syllabus truth, Educational Evidence honesty, or known student state |
| G3 Plan coherence | Silently replaces Learning Mode / Today’s Mission / Canonical Study Plan without advice labelling |
| G4 Explainability readiness | Cannot satisfy P-001.2 schema at the surface default level |
| G5 Proportionality floor | Implied effort grossly exceeds available session time with no adjustable scope |
| G6 Honest refusal | Evidence too thin → prefer “no recommendation yet” over a fabricated primary tip |

Ineligible candidates may still appear as secondary / deferred advice when lawfully labelled — never as the conflicting “today” story.

---

## 3. Priority ladder (default)

When multiple candidates pass hard gates, apply this ladder **top-down**. Stop at the first decisive winner unless a documented exception applies (§5).

| Rank | Priority class | Intent |
|---:|---|---|
| 1 | **Safety / integrity recovery** | Restore a broken study loop (missed-session recovery that unblocks today’s plan; contradictory guidance repair; empty-plan rescue) |
| 2 | **Authorised today’s focus** | Reinforce or clarify Learning Mode / Today’s Mission / active Canonical Study Plan — do not compete with it |
| 3 | **Blocking educational deficit** | Weak prerequisite or weak topic that blocks planned progress *today* |
| 4 | **Time-critical exam preparation** | Short-term exam proximity revision / practice when exam window lawfully elevates urgency |
| 5 | **Weak-topic repair** | Targeted practice on evidenced weak areas when not blocking today’s mission |
| 6 | **New learning progression** | Advance coverage along syllabus order when readiness and plan allow |
| 7 | **Routine revision / spaced reinforcement** | Maintain prior learning when no higher deficit or exam urgency applies |
| 8 | **Workload / wellbeing adjustment** | Reduce load, shorten session, or suggest break when overload evidence exists — never as cover for inventing tips |
| 9 | **Motivation / reinforcement** | Positive reinforcement only after educational substance; never as primary substitute for missing guidance |

**Default bias:** Protect the authorised daily loop first; repair blockers second; optimise long-term mastery third; never sacrifice honesty for engagement.

---

## 4. Worked comparisons

### 4.1 Weak topic vs missed session

| Situation | Prefer | Why |
|---|---|---|
| Student missed yesterday’s session; today’s Mission is still valid | **Missed-session recovery** that restores today’s loop (Rank 1–2) | Consistency beats opportunistic weak-topic jumps that orphan the plan |
| Mission complete; clear weak topic blocks next planned topic | **Weak-topic repair** (Rank 3 or 5) | Educational deficit is now the primary blocker |
| Missed session *and* weak topic on the same Mission topic | **Recovery into that topic** with weak-topic framing | One story: resume the authorised focus and repair it |
| Missed session but Mission superseded by plan refresh | Follow **new authorised today** (Rank 2); mention missed work as secondary context | Do not invent catch-up theatre that fights the new plan |

**Anti-pattern:** Surfacing a glamorous weak-topic Insight while Today’s Mission is ignored or contradicted.

---

### 4.2 Revision vs new learning

| Situation | Prefer | Why |
|---|---|---|
| Topic never studied; coverage incomplete | **New learning** (Rank 6) | Revision without first learning is theatrical |
| Topic studied; spacing / decay / practice weakness evidenced | **Revision / reinforcement** (Rank 5 or 7) | Maintain and deepen understanding |
| Exam window open; topic previously covered | **Exam-oriented revision / practice** (Rank 4) when warrant exists | Short-term readiness may outrank further coverage |
| Student requests “just revise everything” | Keep **plan-coherent** slice; refuse overwhelm dumps | Proportionality (Q6) |

**Anti-pattern:** “Revise Topic X” when X has no completed studying / coverage evidence.

---

### 4.3 Readiness improvement vs workload reduction

| Situation | Prefer | Why |
|---|---|---|
| Readiness thin because of missing practice; student has capacity | **Targeted practice / readiness-building action** aligned to plan (Ranks 3–6) | Improves educational signal quality |
| Overload / fatigue / impossible duration vs available time | **Workload reduction / scope cut** (Rank 8) as primary | A correct topic with impossible effort fails quality |
| Low readiness *and* overload | **Shorter, high-priority slice** of authorised focus | Combine Rank 2/3 with Rank 8 — do not stack a marathon repair |
| Readiness score packaging vs actual next action | Prefer **actionable study step**; readiness narration is supporting context | Recommendations are decisions, not score theatre |

**Anti-pattern:** Pushing “improve readiness” with a heavier session when the student already cannot finish today’s plan.

---

### 4.4 Short-term exam preparation vs long-term mastery

| Situation | Prefer | Why |
|---|---|---|
| Exam far away; coverage gaps material | **Long-term mastery path** — new learning / weak-topic repair per plan (Ranks 3, 5, 6) | Premature exam mode harms foundations |
| Exam imminent; coverage largely done | **Exam preparation** — timed practice, revision of weak examined topics (Rank 4) | Time-critical usefulness |
| Exam imminent; critical coverage still missing | **Minimum viable coverage of examined gaps**, then revise | Do not pure-revise while core topics unread |
| Marketing / panic “cram mode” without warrant | **Refuse** | Exam theatre fails Educational Constitution honesty |

**Anti-pattern:** Calendar-only exam panic that abandons Canonical Study Plan without Exam Coach / planner warrant.

---

## 5. Tie-breakers

When two candidates share the same priority class:

1. **Higher expected educational impact** on the student’s stated exam / syllabus goal.  
2. **Lower student effort** for similar impact (proportionality).  
3. **Higher confidence** given evidence density (prefer Moderate/High over Low when both are lawful).  
4. **Sooner review trigger** if confidence is low (prefer tips that will be reassessed quickly).  
5. **Explainability clarity** — prefer the tip with a clearer single next action.  
6. If still tied → keep the **authorised plan’s order**; do not shuffle for novelty.

---

## 6. Multi-recommendation surfaces

| Surface pattern | Rule |
|---|---|
| Single primary CTA (Dashboard / Mission start) | Exactly **one** primary recommendation |
| Insights / Coach list | Ordered by this ladder; mark primary vs secondary; no conflicting “today” |
| Plan day breakdown | Topic order must match prioritisation reasons cited that day |
| Warnings + tips | Warning recovery (Rank 1) outranks cosmetic tips |

Secondary items must not visually or verbally override the primary authorised action.

---

## 7. Service implementation note (non-binding on runtime in P-001.3)

Future RecommendationService changes should:

1. Collect candidate tips with owner, evidence, effort, confidence, review trigger.  
2. Apply hard gates (G1–G6).  
3. Rank by priority ladder (§3) then tie-breakers (§5).  
4. Emit one primary recommendation + optional ranked secondary list.  
5. Attach P-001.2 explanation fields before presentation.  
6. Record decision class for Runtime A consistency (same winner across surfaces that day unless plan state changes).

This programme **does not** implement the above. It defines the permanent decision contract for when implementation programmes do.

---

## 8. Explicit non-goals

- Scoring tips by click-through or engagement  
- Merging conflicting coach meanings into one mega-tip without WS2 disposition  
- Silent plan rewrites  
- Guaranteeing exam passes  

---

**End of RECOMMENDATION_DECISION_FRAMEWORK**
