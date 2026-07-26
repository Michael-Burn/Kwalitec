# Profile Dimensions

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Educational dimensions of the Student Educational Profile  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **educational dimensions** required to understand an IFoA student’s academic state before long-term planning.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `STUDENT_EDUCATIONAL_PROFILE.md`
3. `KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`
4. `EDUCATIONAL_EVIDENCE_MODEL.md`
5. `planning/EDUCATIONAL_PLANNING_MODEL.md`

Dimensions are educational lenses — not database columns. Implementations may store supporting facts differently; they may not invent new educational meaning by renaming fields.

---

## 1. Purpose

An expert tutor does not reduce a student to one number. The tutor holds several distinct questions in mind at once.

These dimensions are those questions, made permanent and shareable so Master Planner algorithms diagnose the same way.

> **A complete Profile is the joint reading of these dimensions.  
> No dimension alone is the Profile.**

---

## 2. Dimension Classes

| Class | Meaning | Typical claim type |
|-------|---------|-------------------|
| **Hard educational facts** | Observed or derived from durable records / declarations | Observed Fact / Derived Fact |
| **Evidence-backed estimates** | Provisional beliefs warranted by Educational Evidence | Evidence-backed Estimate |
| **Capacity & calendar** | Life and exam horizon constraints | Observed Fact / Derived Fact |
| **Behavioural reliability** | Patterns of adherence and consistency | Derived Fact / Estimate |
| **Soft educational signals** | Subjective or engagement posture | Soft / labelled subjective |
| **Risk & history** | Prior attempts, recovery, feasibility warnings | Observed Fact / Derived Fact / Estimate |

Soft dimensions may inform coaching tone and cautious planning posture. They must never author understanding or mastery claims.

---

## 3. Dimension Catalogue

### D1 — Examination Context

**Educational question:** Which official examination and sitting is this Profile about?

**Meaning:** Subject / syllabus spine and target sitting date that anchor all other dimensions.

**Why tutors need it:** Without exam and date, “progress” and “readiness” have no educational horizon.

**Inputs (see PROFILE_INPUTS):** Examination selection; sitting / target date; syllabus version context when relevant.

**Must not:** Treat an unsupported subject as a complete Profile for planning; invent a sitting date.

---

### D2 — Current Syllabus Coverage

**Educational question:** What portion of the official syllabus has the student honestly studied so far?

**Meaning:** Study Progress / Learning Progress posture across syllabus units — coverage, not competence.

**Why tutors need it:** Sequencing and remaining first-pass load depend on starting coverage.

**Inputs:** Study completion; topic declarations; lawful coverage history.

**Must not:** Equate coverage with understanding, competence, or mastery.

---

### D3 — Demonstrated Understanding

**Educational question:** Where does evidence support provisional belief that the student understands material?

**Meaning:** Estimated Knowledge (and related understanding posture) only where Educational Evidence warrants it; thin elsewhere.

**Why tutors need it:** Adaptive emphasis and revision priorities need honest strength/weakness estimates — not coverage theatre.

**Inputs:** Question performance; assessment-like practice; authorised evidence succession.

**Must not:** Raise understanding from reading completion, mission close, or felt confidence alone.

---

### D4 — Question Performance

**Educational question:** How has the student performed when asked to apply syllabus material under practice or assessment conditions?

**Meaning:** Attributable practice and assessment outcomes — accuracy patterns, topic-linked strengths/weaknesses, exam-like behaviour where observed.

**Why tutors need it:** Application evidence is the primary warrant for understanding estimates and weakness maps.

**Inputs:** Structured question results; practice sets; mock outcomes (when educationally meaningful).

**Must not:** Treat a single lucky session as durable competence; ignore decay after long gaps.

---

### D5 — Consistency

**Educational question:** How steadily has the student engaged with study over time?

**Meaning:** Pattern of study cadence — regular engagement vs bursty or fragmented effort — independent of raw hours declared.

**Why tutors need it:** Sustainable plans fit real behaviour; heroic bursts followed by silence change diagnosis.

**Inputs:** Study/mission completion timestamps; session frequency; gap patterns.

**Must not:** Moralise inconsistency; confuse life interruption with “weak character.”

---

### D6 — Available Study Time

**Educational question:** How much study capacity can the student sustainably offer each week?

**Meaning:** Declared weekly hours, study-day pattern, session-length preferences, and known working constraints.

**Why tutors need it:** Feasibility and intensity envelopes are meaningless without capacity.

**Inputs:** Weekly hours; study-day pattern; work schedule; preferred session bands.

**Must not:** Assume declared hours equal realised hours without checking planning reliability (D14).

---

### D7 — Time Remaining

**Educational question:** How much calendar runway remains until the sitting?

**Meaning:** Days/weeks to examination; interaction of remaining syllabus work with capacity.

**Why tutors need it:** The same coverage looks different with twelve months left versus six weeks.

**Inputs:** Sitting date; current date; leave that consumes runway.

**Must not:** Hide infeasibility behind optimistic packing.

---

### D8 — Revision Maturity

**Educational question:** How far has the student moved from first-pass learning into genuine consolidation and exam-facing revision?

**Meaning:** Whether revision windows have begun in educational substance (return to studied material, deepening application) — not merely a calendar label.

**Why tutors need it:** Plans must protect revision; diagnosis must know whether revision has started, is premature, or is overdue.

**Inputs:** Revision-mode activity; spaced return history; proximity to exam; coverage completeness.

**Must not:** Call last-minute cramming “revision maturity”; treat early light consolidation as full Protected Revision.

---

### D9 — Previous Attempts

**Educational question:** Has the student sat this (or a related) examination before, and what educational aftermath remains?

**Meaning:** Pass/fail/history of prior sittings; residual topic strengths/weaknesses; emotional and strategic aftermath that changes risk posture.

**Why tutors need it:** Repeat candidates need different emphasis than first-time learners with the same coverage percentage.

**Inputs:** Declared prior attempts; prior exam outcomes when known; post-attempt study history.

**Must not:** Shame prior fails; assume a prior pass on a different subject transfers mastery.

---

### D10 — Educational Confidence

**Educational question:** How strongly may Kwalitec stand behind its educational beliefs about this student?

**Meaning:** Platform warrant strength — density and quality of evidence behind estimates — **not** the student’s felt confidence.

**Why tutors need it:** Thin warrant demands cautious speech and cautious planning; dense warrant allows firmer adaptive emphasis.

**Inputs:** Evidence quality levels; accumulation; recency; gaps.

**Must not:** Confuse with felt confidence (D11); present high educational confidence without evidence density.

---

### D11 — Felt Confidence & Motivation

**Educational question:** How does the student currently feel about their preparation and drive to continue?

**Meaning:** Soft subjective posture — self-reported confidence, motivation, engagement tone.

**Why tutors need it:** Coaching tone, recovery sensitivity, and adherence risk benefit from soft signals.

**Inputs:** Reflections; confidence self-reports; optional motivation check-ins.

**Must not:** Author Estimated Knowledge / Mastery; override hard facts about coverage or calendar.

---

### D12 — Recovery History

**Educational question:** What interruptions has the student experienced, and how have they returned?

**Meaning:** Breaks, illness, leave, abandoned intensity, and subsequent recovery trajectories.

**Why tutors need it:** Recovery is an educational state; plans and diagnosis must protect restart without false regression narratives.

**Inputs:** Gap detection; leave declarations; recovery missions/plans; re-engagement patterns.

**Must not:** Treat recovery as failure; invent lost coverage that lawful history still owns.

---

### D13 — Retention & Decay Posture

**Educational question:** Where is previously studied material likely still fresh vs at risk of fading?

**Meaning:** Provisional retention posture from spaced return, practice recency, and time since coverage — always estimated when not directly evidenced.

**Why tutors need it:** Consolidation and revision emphasis depend on decay risk, not only first-pass tick marks.

**Inputs:** Time since study; return practice; revision activity; performance recency.

**Must not:** Claim precise forgetting curves as Observed Fact without warrant; erase coverage because decay is suspected.

---

### D14 — Planning Reliability

**Educational question:** How well do the student’s realised study behaviours match what they declared they could sustain?

**Meaning:** Adherence of completed work and hours to declared capacity and plan intent — reliability of planning inputs themselves.

**Why tutors need it:** If declared ten hours/week but consistently completes three, diagnosis and future plans must recalibrate capacity — not scold in secret.

**Inputs:** Declared capacity vs completed load; missed planned weeks; repeated replan causes.

**Must not:** Punish; silently keep using false capacity assumptions.

---

### D15 — Practice Depth & Assessment Exposure

**Educational question:** Has the student moved beyond recognition into exam-like application and timed stamina?

**Meaning:** Depth of practice (guided vs mixed; timed vs untimed) and exposure to mock / simulation conditions.

**Why tutors need it:** Exam readiness posture requires more than topic ticks and untimed drills.

**Inputs:** Practice mode history; mock completion; timed attempt records.

**Must not:** Equate any practice with exam readiness; treat one mock as destiny.

---

### D16 — Prerequisite & Foundation Integrity

**Educational question:** Are early foundations intact enough for later topics to be educationally honest?

**Meaning:** Whether prerequisite topics show lawful coverage and, where evidenced, adequate understanding before advanced work is treated as secure.

**Why tutors need it:** Sequencing law and remediation diagnosis depend on foundation integrity.

**Inputs:** Coverage order history; weak early-topic evidence; declared skips.

**Must not:** Allow declared “ahead” status to hide missing prerequisites in diagnosis.

---

### D17 — Concurrent Load & Competing Demands

**Educational question:** What else competes for the student’s cognitive and calendar capacity?

**Meaning:** Other subjects, work peaks, caregiving, concurrent exams — declared competing demands.

**Why tutors need it:** Feasibility and intensity must respect real life beyond a single syllabus.

**Inputs:** Concurrent subject declarations; work/leave notes; competing exam dates.

**Must not:** Ignore declared concurrent load when narrating “available” capacity.

---

### D18 — Feasibility & Risk Posture

**Educational question:** Given coverage remaining, capacity, and time left, is the current trajectory educationally feasible — and where is risk concentrated?

**Meaning:** Derived diagnostic posture combining D2, D6, D7, D9, D12, D14 (and related) into honest risk language — not a pass guarantee.

**Why tutors need it:** Expert tutors surface risk early; they do not wait for plan failure.

**Inputs:** Derived from other dimensions; leave; prior attempts.

**Must not:** Present risk posture as a precise pass probability theatre; hide At Risk state behind cheerful copy.

---

### D19 — Learning Mode vs Revision Mode Posture

**Educational question:** Is the student primarily in first-pass learning, consolidation, or revision authority — educationally, not just by UI tab?

**Meaning:** Dominant lawful educational posture for current work (Learning Mode primacy vs Revision Mode substance).

**Why tutors need it:** Diagnosis of state (Practising vs Revising vs Exam Preparation) depends on mode substance.

**Inputs:** Current learning topic / mode authority; revision activity; phase markers from planning when present.

**Must not:** Let UI navigation redefine educational mode authority.

---

### D20 — Explainability Readiness

**Educational question:** Can Kwalitec currently explain this Profile in plain language with honest claim types?

**Meaning:** Whether inputs are sufficient to narrate diagnosis without inventing certainty; flags thin dimensions explicitly.

**Why tutors need it:** Unexplainable diagnosis is not trustworthy diagnosis.

**Inputs:** Completeness of mandatory/strong inputs; evidence density; assumption flags.

**Must not:** Ship confident state labels when Explainability Readiness says the warrant is thin.

---

## 4. Dimension Interactions (Educational, Not Algorithmic)

| Interaction | Educational rule |
|-------------|------------------|
| D2 × D3 | High coverage + thin understanding evidence → narrate progress, withhold readiness theatre |
| D6 × D14 | Declared capacity discounted by poor planning reliability |
| D7 × D18 | Short runway raises feasibility risk even with strong motivation (D11) |
| D8 × D15 | Revision maturity without assessment exposure remains incomplete for Exam Ready claims |
| D9 × D18 | Prior fails raise risk posture; they do not erase lawful coverage |
| D10 × D11 | Felt confidence may diverge from educational confidence — both may be true; neither replaces the other |
| D12 × D5 | Recovery after break may temporarily lower consistency without implying permanent unreliability |
| D13 × D8 | Suspected decay increases need for revision substance even if coverage looks complete |

---

## 5. Minimum Dimension Set for “Planner-Consumable” Profile

For Master Planner to personalise a **complete** long-term plan, the Profile must at least support:

| Required | Dimensions |
|----------|------------|
| Mandatory | D1, D2, D6, D7 |
| Strongly expected | D3 or explicit thin-understanding flag; D9 if applicable; D14 when history exists; D17 when declared |
| Soft enriching | D11, D12 detail, D15, D13 estimates |

Without the mandatory set, the Profile may exist as **intake-incomplete diagnosis** — useful for gathering facts, unlawful as a pretence of full planner input (aligned with MS001 §5).

---

## 6. Non-Dimensions (Forbidden Collapses)

The following are **not** Profile dimensions:

| Collapse | Why forbidden |
|----------|----------------|
| Single “readiness %” as the Profile | Hides claim types and axes |
| “Engagement score” replacing D5+D11+D14 | Mixes soft and hard unlawfully |
| Personality / learning-style typology as diagnosis | Not educational evidence for IFoA planning law |
| Optimiser internal cost vectors | Machinery, not educational meaning |

---

## 7. Cross References

- `STUDENT_EDUCATIONAL_PROFILE.md` — overview
- `PROFILE_INPUTS.md` — origins of dimension values
- `PROFILE_STATES.md` — states synthesised from dimensions
- `PROFILE_EVOLUTION.md` — how dimensions change
- `PROFILE_EXPLAINABILITY.md` — how dimensions are spoken
