# Profile Inputs

**Programme:** VI — Master Planner  
**Milestone:** MS002 — Student Educational Profile Model  
**Classification:** Origins of educational evidence and declarations for the Profile  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **where educational inputs to the Student Educational Profile originate**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `STUDENT_EDUCATIONAL_PROFILE.md`
3. `EDUCATIONAL_EVIDENCE_MODEL.md`
4. `EDUCATIONAL_EVIDENCE_AUTHORITY.md`
5. `planning/EDUCATIONAL_PLANNING_MODEL.md` (§5 inputs)
6. `PROFILE_DIMENSIONS.md`

This milestone documents educational requirements. It does **not** implement collection, storage, or Runtime A adapters.

> **Future implementations will collect these inputs.  
> Algorithms must not invent inputs this document does not authorise.**

---

## 1. Purpose

Diagnosis without inputs is fiction. Expert tutors ask questions and observe work; they do not invent a student’s history.

Profile Inputs name the lawful origins of facts, evidence, soft signals, and derived measures that feed Profile Dimensions.

---

## 2. Input Integrity Principles

1. **Prefer Observed Facts and student declarations** for coverage and calendar constraints.
2. **Prefer Educational Evidence** for understanding claims — never activity alone.
3. **Label soft signals as soft** — reflections and felt confidence remain subjective.
4. **Do not invent** exam dates, progress, hours, or prior attempts.
5. **When inputs conflict**, prefer continuity of lawful educational history and disclose uncertainty.
6. **Cold start is valid** — thin inputs produce cautious Profiles, not synthetic density.
7. **Guidance is not input** — missions and recommendations consume the Profile; they do not author Evidence of understanding by existing.
8. **Collection UX is out of scope** — the educational obligation to obtain inputs remains.

---

## 3. Input Classes

| Class | Definition | May feed |
|-------|------------|----------|
| **Declaration** | Student-stated fact or preference | Capacity, prior attempts, leave, concurrent load, coverage self-report |
| **Activity observation** | Durable record of study/practice action | Consistency, coverage (when lawful), practice depth |
| **Educational Evidence** | Authorised observation warranting understanding succession | Demonstrated understanding, question performance, educational confidence |
| **Soft signal** | Subjective report or engagement tone | Felt confidence, motivation |
| **Derived measure** | Deterministic computation from facts | Time remaining, coverage %, feasibility posture, planning reliability |
| **Assumption default** | Explicit Planning Assumption used when input missing | Only labelled as assumption — never as Observed Fact |

---

## 4. Input Catalogue

### I1 — Examination & Sitting Selection

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration (sometimes system-confirmed catalogue) |
| **Feeds** | D1, D7 |
| **Educational meaning** | Names the official subject and target sitting |
| **Mandatory for complete planning?** | Yes |
| **Must not** | Invent unsupported subjects as complete planner context |

### I2 — Available Weekly Study Time & Pattern

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration |
| **Feeds** | D6, D14, D17, D18 |
| **Educational meaning** | Sustainable capacity envelope and study-day shape |
| **Mandatory for complete planning?** | Yes |
| **Enrichments** | Session length preferences; morning/evening preference |

### I3 — Planned Leave & Known Interruptions

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration |
| **Feeds** | D7, D12, D17, D18 |
| **Educational meaning** | Calendar capacity that must not be pretended available |
| **Mandatory?** | Strongly expected when known |

### I4 — Study Completion / Coverage Events

| Attribute | Value |
|-----------|--------|
| **Class** | Activity observation / declaration |
| **Feeds** | D2, D16, D19 |
| **Educational meaning** | Lawful Study Progress advances — coverage only |
| **Examples** | Topic marked studied; lawful session/mission coverage close |
| **Must not** | Update Estimated Knowledge / Mastery by itself |

### I5 — Mission & Session Completion

| Attribute | Value |
|-----------|--------|
| **Class** | Activity observation |
| **Feeds** | D5, D14, D15 (engagement depth), D12 (re-engagement) |
| **Educational meaning** | Work was undertaken and closed; informs consistency and reliability |
| **Must not** | Imply mastery or exam readiness |

### I6 — Question / Practice Performance

| Attribute | Value |
|-----------|--------|
| **Class** | Educational Evidence (when authorised) / observation |
| **Feeds** | D3, D4, D10, D13, D15, D16 |
| **Educational meaning** | Application outcomes attributable to syllabus scope |
| **Examples** | Structured question results; practice set outcomes |
| **Must not** | Single favourable result mint absolute mastery theatre |

### I7 — Mock Exams & Exam Simulation

| Attribute | Value |
|-----------|--------|
| **Class** | Educational Evidence / high-stakes observation when conditions warrant |
| **Feeds** | D4, D8, D10, D15, D18 |
| **Educational meaning** | Timing, stamina, and integrated application evidence — not destiny |
| **Must not** | Treat one mock as pass/fail prophecy |

### I8 — Student Reflections

| Attribute | Value |
|-----------|--------|
| **Class** | Soft signal (may be low-quality observation) |
| **Feeds** | D11, coaching tone; weakly D13 if student reports forgetting |
| **Educational meaning** | Student narrative about difficulty, confidence, energy |
| **Must not** | Sole warrant for Estimated Knowledge |

### I9 — Felt Confidence Reports

| Attribute | Value |
|-----------|--------|
| **Class** | Soft signal |
| **Feeds** | D11 (distinct from D10) |
| **Educational meaning** | How the student feels — Constitution IV.10 posture |
| **Must not** | Co-write Study Progress or impersonate assessment Evidence |

### I10 — Motivation & Engagement Check-ins

| Attribute | Value |
|-----------|--------|
| **Class** | Soft signal |
| **Feeds** | D11; may colour D18 risk narration carefully |
| **Educational meaning** | Drive and willingness to continue under load |
| **Must not** | Override feasibility facts |

### I11 — Behavioural Consistency History

| Attribute | Value |
|-----------|--------|
| **Class** | Derived from activity observations |
| **Feeds** | D5, D12, D14 |
| **Educational meaning** | Cadence, gaps, burst patterns over time |
| **Examples** | Session frequency; days since last study; streak breaks |

### I12 — Time Available vs Time Used

| Attribute | Value |
|-----------|--------|
| **Class** | Derived (declarations × completions) |
| **Feeds** | D14, D18 |
| **Educational meaning** | Planning reliability — realised load vs declared capacity |
| **Must not** | Punitive framing |

### I13 — Previous Attempt History

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration / observed outcome when known |
| **Feeds** | D9, D18 |
| **Educational meaning** | Prior sittings and aftermath for risk posture |
| **Mandatory?** | Strongly expected when applicable |

### I14 — Strengths & Weaknesses (Declared)

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration (estimate-grade unless evidenced) |
| **Feeds** | Soft prior for D3/D4 emphasis until Evidence exists |
| **Educational meaning** | Student self-view of hard/easy topics |
| **Must not** | Override contrary Educational Evidence |

### I15 — Strengths & Weaknesses (Evidence-backed)

| Attribute | Value |
|-----------|--------|
| **Class** | Evidence-backed estimate |
| **Feeds** | D3, D4, D10, D16 |
| **Educational meaning** | Provisional topic-level understanding map |
| **Must not** | Present as Observed Fact |

### I16 — Revision & Spaced Return Activity

| Attribute | Value |
|-----------|--------|
| **Class** | Activity observation |
| **Feeds** | D8, D13, D19 |
| **Educational meaning** | Substance of consolidation and revision — not calendar labels alone |

### I17 — Concurrent Subjects & Competing Exams

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration |
| **Feeds** | D17, D6 (effective capacity), D18 |
| **Educational meaning** | Competing cognitive and calendar demands |

### I18 — Energy / Burnout History (when captured)

| Attribute | Value |
|-----------|--------|
| **Class** | Soft signal / derived load history |
| **Feeds** | D11, D18 intensity caution |
| **Educational meaning** | Sustainability risk beyond raw hours |
| **Must not** | Clinical diagnosis claims |

### I19 — Material Access Notes

| Attribute | Value |
|-----------|--------|
| **Class** | Declaration |
| **Feeds** | Reality-check only (not a Profile dimension core) |
| **Educational meaning** | CMP edition / notes availability — student responsibility |
| **Must not** | Authorise content generation to fill gaps |

### I20 — Calendar Now & Derived Horizon Metrics

| Attribute | Value |
|-----------|--------|
| **Class** | Derived measure |
| **Feeds** | D7, D18 |
| **Educational meaning** | Days remaining; whether remaining work fits capacity |
| **Must not** | Hide infeasibility |

---

## 5. Mapping: Inputs → Dimensions (Summary)

| Dimension | Primary inputs |
|-----------|----------------|
| D1 Examination Context | I1 |
| D2 Coverage | I4, (I14 cautiously) |
| D3 Understanding | I6, I7, I15 |
| D4 Question Performance | I6, I7 |
| D5 Consistency | I5, I11 |
| D6 Available Time | I2, I3, I17 |
| D7 Time Remaining | I1, I3, I20 |
| D8 Revision Maturity | I16, I7, I4 |
| D9 Previous Attempts | I13 |
| D10 Educational Confidence | I6, I7, I15 (evidence density) |
| D11 Felt Confidence & Motivation | I8, I9, I10, I18 |
| D12 Recovery History | I3, I11, I5 |
| D13 Retention & Decay | I16, I6, I4 (recency) |
| D14 Planning Reliability | I2, I5, I12 |
| D15 Practice Depth | I6, I7, I5 |
| D16 Foundation Integrity | I4, I6, I15 |
| D17 Concurrent Load | I17, I3 |
| D18 Feasibility & Risk | I20 + D2/D6/D7/D9/D14 synthesis |
| D19 Mode Posture | I4, I16 + lawful mode authority |
| D20 Explainability Readiness | Completeness across I1–I20 |

---

## 6. Intake Completeness Levels

| Level | Meaning | Planner consequence |
|-------|---------|---------------------|
| **Incomplete** | Missing mandatory I1/I2/I4 (coverage) or sitting | Diagnose as intake-incomplete; do not publish complete plan |
| **Minimal** | Mandatory present; understanding thin | Cautious plan; understate readiness; request practice evidence over time |
| **Enriched** | Strong evidence + reliability + prior attempts known | Full adaptive personalisation under Planning Model |
| **Assumption-filled** | Defaults used for gaps | Must disclose assumptions in explainability |

---

## 7. What Is Not a Profile Input

| Non-input | Why |
|-----------|-----|
| Optimiser scores / twin facet labels | Internal machinery |
| Recommendation acceptance alone | Guidance ≠ Evidence of understanding |
| Marketing persona tags | Not educational diagnosis |
| Fabricated demo history | Unconstitutional fiction |

---

## 8. Future Collection Note

Later milestones may implement intake wizards, Twin projections, and evidence pipelines. Those implementations must:

1. Map collected fields onto this catalogue;
2. Preserve claim types;
3. Refuse to treat soft signals as understanding Evidence;
4. Amend this document before inventing new educational input meanings.

---

## 9. Cross References

- `PROFILE_DIMENSIONS.md` — what inputs feed
- `PROFILE_EVOLUTION.md` — how new inputs rewrite the Profile
- `planning/PLANNING_ASSUMPTIONS.md` — lawful defaults when inputs missing
- `EDUCATIONAL_EVIDENCE_MODEL.md` — evidence hierarchy
