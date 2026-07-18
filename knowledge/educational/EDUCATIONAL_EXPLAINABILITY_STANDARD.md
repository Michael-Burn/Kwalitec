# Educational Explainability Standard

**Capability ID:** EIP-003  
**Programme:** Educational Integrity Programme  
**Classification:** Educational Communication Standard — subordinate specialised architecture  
**Status:** APPROVED — governing for student-facing educational speech  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This Standard defines how Kwalitec explains educational decisions to students.

It is subordinate to:

1. **KWALITEC_EDUCATIONAL_CONSTITUTION.md** (EGI-001) — highest educational authority  
2. **EDUCATIONAL_LOGIC_REGISTRY.md** (EGI-002) — especially EL-008, EL-009, EL-010  
3. **EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md** (EGI-003) — Categories C, F, G, H  
4. **EDUCATIONAL_EVIDENCE_MODEL.md** (EIP-002-DESIGN) — claim lawfulness of observations  
5. **EDUCATIONAL_STATE_AUTHORITY_MATRIX.md** (EIP-001) — ownership and lawful writers  

Authority order for educational speech:

> Constitution defines *that* guidance must be explainable.  
> The Logic Registry binds Messaging (EL-010) and Recommendations (EL-008).  
> **This Standard defines the student-facing explainability contract.**

This document:

- defines educational communication principles and narrative rules;
- does **not** redesign Educational Intelligence, the Digital Twin, Learning Mode, recommendations, or Educational Evidence;
- does **not** introduce new educational algorithms or scoring mathematics;
- binds presentation and coaching copy only.

**Explainability improves understanding of decisions already authorised.  
It never invents educational certainty.**

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Explainability Principles](#2-explainability-principles)
3. [Educational Communication Hierarchy](#3-educational-communication-hierarchy)
4. [Four-Question Explainability Framework](#4-four-question-explainability-framework)
5. [Narrative Rules](#5-narrative-rules)
6. [Student Language Rules](#6-student-language-rules)
7. [Surface Contracts](#7-surface-contracts)
8. [Good and Bad Messaging Examples](#8-good-and-bad-messaging-examples)
9. [Cross References](#9-cross-references)

---

## 1. Purpose

Students should never have to infer why Kwalitec made an educational decision.

Educational Explainability exists so that every material recommendation, mission, readiness indicator, and progress summary answers — in plain educational language — what is known, what is estimated, why guidance exists, and what to do next.

Without Explainability:

- recommendations feel opaque or commanding;
- estimates masquerade as validated proof;
- missions appear arbitrary;
- readiness percentages become theatre.

With Explainability:

- the student can trust the coach;
- claim types remain distinguishable;
- agency remains with the student for optional advice.

---

## 2. Explainability Principles

1. **Every educational decision must explain itself.** Silent steering is forbidden.
2. **Facts and estimates must be visibly distinct.** Estimates are always labelled as estimates (or equivalent honest language: Suggested, Recommended, provisional).
3. **One educational reason.** Prefer a single clear educational purpose over multi-factor jargon dumps.
4. **One clear next action.** Guidance reduces decision burden; it does not leave the student guessing.
5. **Educational language only.** Internal systems remain invisible (Constitution Article II §1.10; EL-010; EL-012).
6. **Uncertainty must be named.** Thin history and cold start require understatement, including “cannot yet be estimated” when warranted.
7. **Advice does not commandeer Learning Mode.** When advisory focus differs from Today’s Mission authority, that difference must be disclosed as advice — not mission replacement.
8. **No new algorithms in speech.** Copy may narrate authorised states; it must not invent scores, evidence, or mastery.

---

## 3. Educational Communication Hierarchy

Student-facing educational speech uses four lawful claim types (EGI-003 Category C):

| Rank | Claim type | Definition | Student cue |
|------|------------|------------|-------------|
| 1 | **Observed Fact** | A lawful record of something that happened or was declared as coverage | Plain statement of what occurred / what was completed studying |
| 2 | **Derived Fact** | A deterministic journey measure from Observed Facts + syllabus structure | Syllabus coverage %, Current Learning Topic position |
| 3 | **Evidence-backed Estimate** | Provisional knowledge, mastery, or readiness judgement | Prefixed with *Estimated* / *Suggested* / honest judgement language |
| 4 | **Educational Advice** | Optional coaching that does not rewrite Mission or Study Progress | Prefixed with *Recommended* / *Suggested* / *Optional* |

Hierarchy law:

```
Observed Fact / Derived Fact
        ↓  (interpretation; never invention)
Evidence-backed Estimate
        ↓  (coaching; never silent override)
Educational Advice
        ↓
Student Choice
```

Advice may never be presented as Observed Fact.  
Estimates may never be presented as validated proof.  
Coverage (Study Progress) may never be narrated as mastery.

---

## 4. Four-Question Explainability Framework

Every educational recommendation or decision presented to the student must answer:

### Q1 — What do we objectively know?

Only Observed Facts and Derived Facts.

Examples: topics completed studying; mission completed; Current Learning Topic name; syllabus coverage percentage.

### Q2 — What do we estimate?

Only evidence-backed estimates, clearly labelled.

Examples: Estimated Knowledge; Estimated readiness when a composite judgement is shown.

If estimation is not yet lawful or history is empty, say so: readiness / knowledge cannot yet be estimated.

### Q3 — Why are we recommending this?

One educational explanation. No engineering terminology.

### Q4 — What should the student do next?

One clear educational action (continue today’s mission, optionally review later, create a plan, mark session complete, etc.).

Surfaces may visualise these as labelled sections (Observed Facts / Estimates / Educational Advice / Next step) or as an equivalent coherent narrative that still answers all four questions.

---

## 5. Narrative Rules

The application must never:

1. Expose Digital Twin terminology on student surfaces  
2. Expose Educational Intelligence terminology on student surfaces  
3. Expose internal implementation concepts (warrant tags, cold_start, thin_warrant, pipeline, entity ids, intent enums, Knowledge State as machinery)  
4. Present estimates as facts  
5. Imply mastery without authorised Educational Evidence  
6. Imply that self-reported confidence equals understanding  
7. Replace Learning Mode Mission authority with undifferentiated “Recommended Mission” theatre  
8. Leave recommendations or missions without a reason  

Coherent story law (EIP-000 Capability 3):

```
Mission → Reason → Advice → Student Choice
```

Across Dashboard, Mission, Recommendations, Study Plan, Analytics, Readiness, and Settings educational copy, the student encounters one educational story with lawful claim types and clear authority roles.

---

## 6. Student Language Rules

### Prefer

| Concept | Prefer |
|---------|--------|
| Coverage | Completed studying, Study Progress, Learning Progress, syllabus coverage |
| Daily commitment | Today’s Mission, today’s focus, Current Learning Topic |
| Estimates | Estimated Knowledge, Estimated readiness |
| Advice | Suggested, Recommended, optional review (not today’s learning) |
| Practice signals | Practice results, study checks, practice scores |
| Continuity | Continue Learning, Start Today’s Session |

### Forbidden (student-facing)

| Family | Examples |
|--------|----------|
| Engineering / Twin / Intelligence | Digital Twin, Educational Intelligence, Knowledge State, warrant, cold_start, thin_warrant, evidence_creating, pipeline, classification enums, raw entity ids |
| False attainment from coverage | already mastered, you have mastered, mark as mastered, topics mastered (as Study Progress) |
| Bare strength under thin evidence | Known, Strong Topic, Weak Topic as unsupported factual labels |
| Evidence jargon leakage | Prefer *practice results* / *study checks* over *study evidence* where student-facing |

Internal domains may retain precise vocabulary. Presentation must map before render (EL-010).

---

## 7. Surface Contracts

### 7.1 Today’s Mission

Must communicate:

1. **Mission** — today’s topic / session title  
2. **Educational purpose** — why this session exists (advance Study Progress along the syllabus in Learning Mode)  
3. **Reason for selection** — Current Learning Topic / Learning Mode doctrine  
4. **Current educational position** — where the student is on the syllabus journey  
5. **Next action** — complete the session / next checklist step  

### 7.2 Recommendations

Must distinguish:

- Observed Facts  
- Evidence-backed Estimates  
- Educational Advice  

And provide one clear next action. Advisory divergence from Learning Mode must remain advice.

### 7.3 Readiness

If readiness is shown:

- explain what Observed / Derived Facts and/or estimates support it; **or**
- explain why readiness cannot yet be estimated.

Syllabus coverage and composite estimated readiness must not silently share one ambiguous label.

### 7.4 Progress summaries / Analytics / Settings

Progress and analytics copy must preserve Study Progress vs Estimated Knowledge distinctions. Settings educational concepts (preferences, learning profile status) must stay educational and non-engineering.

---

## 8. Good and Bad Messaging Examples

### Mission

| Bad | Good |
|-----|------|
| “Today’s Recommended Mission” (advice-shaped label on Learning Mode authority) | “Today’s Topic” / “Today’s Mission” |
| No Why block | Why: Learning Mode follows your Current Learning Topic — the next syllabus topic you have not yet completed studying |
| “Estimated Mastery grows from study evidence” | “Estimated Knowledge grows from practice results over time” |

### Recommendations

| Bad | Good |
|-----|------|
| Single undifferentiated paragraph mixing fact and theatre | Separate Observed Facts / Estimates / Educational Advice |
| “Reach 100% curriculum coverage for complete exam confidence.” | “Suggested next step: continue syllabus coverage so fewer topics remain unstudied.” |
| “critically weak topic(s)” as bare fact | “Estimated knowledge for X is below 30%. Suggested: practise these foundational topics.” |
| Recommendation with no Why | Always include educational reason + next action |

### Readiness

| Bad | Good |
|-----|------|
| Bare “Readiness 42%” with no support | “Estimated readiness 42%. Based on syllabus coverage, estimated knowledge averages, and recent review habits.” |
| Treating coverage % as mastery | “Syllabus coverage: you have completed studying topics representing 42% of official syllabus weighting. This is Study Progress — not Estimated Knowledge.” |
| Inventing confidence when history is empty | “Readiness cannot yet be estimated. Complete study sessions so we can summarise coverage and practice results.” |

### Mastery language

| Bad | Good |
|-----|------|
| “You have mastered this topic” after completion alone | “Completed studying” / “Study Progress recorded” |
| Stage badge “Mastered” without authorised evidence framing | “Strong estimated knowledge” / show Estimated Knowledge only when authorised |

---

## 9. Cross References

| Document | Role |
|----------|------|
| KWALITEC_EDUCATIONAL_CONSTITUTION.md | Articles II, III, VI, VII, VIII — philosophy, truth, Learning Mode, messaging |
| EDUCATIONAL_LOGIC_REGISTRY.md | EL-003 Mission, EL-008 Recommendations, EL-009 Readiness, EL-010 Messaging |
| EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md | Claim types; Categories C/F/G/H |
| EDUCATIONAL_EVIDENCE_MODEL.md | What may lawfully support estimates |
| EDUCATIONAL_STATE_AUTHORITY_MATRIX.md | Ownership; students never own Estimated Mastery as editable verified truth |
| EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md | Capability 3 — EIP-003 |

---

## Implementation status

**EIP-003** realises this Standard in student-facing presentation:

- `EducationalExplainabilityService` builds mission, recommendation, and readiness narratives;
- Mission, Dashboard, Analytics, Study Plan, and Settings educational copy follow this contract;
- regression tests prove absences of engineering theatre and presence of explainability structure.

Algorithms, Twin update strategies, and Educational Intelligence redesign remain out of scope.
