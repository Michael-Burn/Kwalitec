# Educational Governance Review Standard

**Capability ID:** EGI-003  
**Programme:** Educational Governance Initiative  
**Classification:** Mandatory Educational Governance Standard  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This Standard defines **how educational implementation is evaluated** before approval.

It is subordinate only to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001) — defines **WHAT** is educationally true;
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002) — defines **HOW** educational logic operates.

This Standard does not redefine educational meaning. It does not invent educational logic. It establishes objective review criteria so that educational correctness is validated with the same discipline as engineering quality.

**No educational implementation should be approved without passing this Standard.**

This Standard is mandatory for:

- Architecture Reviews;
- Educational Reviews;
- Internal Alpha Reviews;
- Version 1.0 Release Reviews;
- Future Educational Intelligence capabilities and related educational workstreams.

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Review Philosophy](#2-review-philosophy)
3. [Educational Governance Checklist](#3-educational-governance-checklist)
4. [Educational Compliance Rating](#4-educational-compliance-rating)
5. [Educational Governance Score](#5-educational-governance-score)
6. [Review Outcomes](#6-review-outcomes)
7. [Educational Release Gate](#7-educational-release-gate)
8. [Capability Review Template](#8-capability-review-template)
9. [Governance Lifecycle](#9-governance-lifecycle)
10. [Future Evolution](#10-future-evolution)
11. [Cross References](#11-cross-references)

---

## 1. Purpose

Educational Governance Review exists because **implementation quality is not sufficient**.

A capability may be:

- technically correct;
- architecturally layered;
- covered by tests;
- operationally deployable;

and still be **educationally false**.

Educational falsity includes, without limitation:

- communicating certainty that evidence does not warrant;
- treating Study Progress as Mastery;
- treating time, confidence, or completion as understanding;
- duplicating educational state ownership;
- changing educational meaning in code before governing documents are amended;
- presenting conflicting educational stories across Study Plan, Dashboard, Mission, Recommendations, and Analytics.

Kwalitec’s commercial and educational obligation is student trust. Trust collapses when surfaces appear polished while educational meaning is incoherent.

Therefore every educational capability must be evaluated against:

1. the Educational Constitution (lawful meaning);
2. the Educational Logic Registry (lawful behaviour);
3. this Review Standard (lawful approval criteria).

**Engineering correctness answers:** *Does it work?*  
**Educational Governance Review answers:** *Does it tell the educational truth?*

---

## 2. Review Philosophy

Educational Governance Review is not a preference exercise. It is an integrity examination.

Reviewers adopt the following mindset:

### Governing Questions

1. **Does this implementation strengthen student trust?**  
   If a careful student used the product honestly, would trust rise, hold, or fall?

2. **Does it communicate educational truth?**  
   Is every material educational statement lawful under the claim categories in Category C?

3. **Does it comply with the Constitution?**  
   Does meaning match Articles III–VIII, especially state definitions, integrity rules, and messaging honesty?

4. **Does it comply with the Educational Logic Registry?**  
   Does decision behaviour match registered educational logic (EL-001 onward), with ownership and visibility preserved?

### Review Posture

- Prefer **understatement** over confident theatre when warrant is thin.
- Prefer **one coherent educational story** over surface-local optimisation.
- Prefer **explicit amendment** of governing documents over silent redefinition in code or copy.
- Prefer **educator-defensible behaviour** over engagement tricks that confuse meaning.
- Treat student misunderstanding of educational meaning as a **failure condition**, even when engineers understand the internal model.

### What This Review Is Not

- Not a substitute for engineering review, security review, or architecture layering review.
- Not a redesign of Educational Intelligence, Digital Twin, Adaptive Learning, or Founder Intelligence.
- Not a licence to invent new educational concepts without Constitutional amendment.
- Not a subjective brand-quality critique. Criteria below are objective and pass/fail capable.

---

## 3. Educational Governance Checklist

Every educational capability review **must** complete Categories A–H.

For each category, record:

- **Findings** (evidence from code, templates, services, tests, or docs);
- **Compliance Rating** (FULL / PARTIAL / NON-COMPLIANT — see Section 4);
- **Category Score** (0–weight points — see Section 5);
- **Conditions / Defects** (if any).

Failure to complete any category voids APPROVED outcomes.

---

### Category A — Constitution Compliance

**Weight:** 15  

**Purpose:** Ensure implementation does not redefine educational law by stealth.

**Mandatory questions**

| ID | Question |
|----|----------|
| A1 | Does the implementation comply with the Educational Constitution? |
| A2 | Does it redefine educational terminology (e.g. Learning Progress, Mastery, Mission, Evidence)? |
| A3 | Does it introduce new educational concepts? |
| A4 | If A2 or A3 is yes — has the Constitution been amended first under Article X? |

**Pass expectations**

- Terminology and state meaning match Article IV.
- Integrity rules in Article VIII are not violated in behaviour or student wording.
- Decision Hierarchy / Learning Mode authority (Article VI) is respected where missions are selected.
- New educational concepts appear in the Constitution **before** they appear as product meaning.

**Automatic NON-COMPLIANT triggers**

- Mastery asserted from completion, confidence, or time alone.
- Adaptive interruption silently replacing Learning Mode mission authority while Adaptive Mode remains deferred.
- Student-editable mastery presented as verified fact.
- Mixing Study Progress / Learning Progress meaning with Estimated Mastery or Knowledge State.

---

### Category B — Logic Registry Compliance

**Weight:** 15  

**Purpose:** Ensure operational educational behaviour follows registered logic.

**Mandatory questions**

| ID | Question |
|----|----------|
| B1 | Does implementation follow registered educational logic for every educational decision it performs? |
| B2 | Has educational logic been changed (inputs, outputs, ownership, decision process, visibility, constraints)? |
| B3 | If B2 is yes — has the Educational Logic Registry been updated **before** implementation approval? |
| B4 | Are all touched Educational Logic IDs (EL-xxx) identified and verified? |

**Pass expectations**

- Mission selection, progress narration, evidence handling, estimates, recommendations, messaging, and plan behaviour map to Registry sections.
- Current Implementation Status differences in the Registry are not treated as Constitutional permission; they are recorded debt, not licence.
- No new educational decision path exists in code without a Registry entry.

**Automatic NON-COMPLIANT triggers**

- Unregistered educational decision path that students rely on.
- Registry superseded by implementation convenience.
- Ownership matrix violated (e.g. Twin owning Study Progress declarations as verified knowledge).

---

### Category C — Educational Truth

**Weight:** 15  

**Purpose:** Ensure every educational statement is a lawful claim type.

Kwalitec may communicate educational statements only when each statement is classified as one of the following:

| Claim Type | Meaning | Typical markers / behaviour |
|------------|---------|-----------------------------|
| **Observed Fact** | A lawful record of something that happened or was declared as coverage — not competence theatre. | Completed studying; mission completed; attempt submitted; score recorded as outcome. |
| **Derived Fact** | A deterministic journey or structural measure derived from Observed Facts and syllabus structure. | Learning Progress as coverage-through-syllabus; Current Learning Topic from ordered incomplete units. |
| **Evidence-Based Estimate** | A provisional knowledge-, mastery-, readiness-, or similar judgement warranted by Educational Evidence. | Estimated Knowledge; Estimated Mastery; readiness summaries labelled as estimates / judgements. |
| **Educational Advice** | A suggestion or recommendation that does not itself become evidence or mission authority by silence. | Recommended; Suggested; advisory focus distinct from Today’s Mission when different. |

**Mandatory questions**

| ID | Question |
|----|----------|
| C1 | Does every material educational statement represent an Observed Fact, Derived Fact, Evidence-Based Estimate, or Educational Advice? |
| C2 | Are estimate statements identified as estimates (or equivalent honest language)? |
| C3 | Is advice presented as advice rather than as mission authority or as evidence? |
| C4 | Is any statement outside the four claim types present on student-facing surfaces? |

**Pass expectations**

- No unclassified “mastered / known / strong / weak” factual theatre without warrant.
- Cold start and thin evidence use understatement.
- Advisory Dual-display (if present) does not overwrite Learning Mode mission authority.

**Automatic NON-COMPLIANT triggers**

- Any material educational claim that is none of the four types.
- Estimates presented as validated proof.
- Advice presented as Observed Fact or as silent mission replacement.

---

### Category D — Evidence Integrity

**Weight:** 15  

**Purpose:** Protect the chain from observation → estimate → speech.

**Mandatory questions**

| ID | Question |
|----|----------|
| D1 | Can every educational claim identify its evidence (or correctly disclose absence of evidence)? |
| D2 | Does completion affect mastery incorrectly (Completion ≠ Mastery)? |
| D3 | Does time imply learning incorrectly (Time ≠ Learning)? |
| D4 | Does confidence imply knowledge incorrectly (Confidence ≠ Understanding)? |
| D5 | Does a single attempt improperly mint success, readiness, or mastery language? |

**Pass expectations**

- Alignment with Constitution Article V evidence quality ranking and Article VIII integrity rules.
- Inference interprets evidence; inference does not invent evidence.
- Absence of evidence is disclosed as uncertainty, not filled with confident fiction.

**Automatic NON-COMPLIANT triggers**

- Mission or Study Progress completion writing Estimated Mastery as fact.
- Self-reported confidence alone authorizing “known” / “mastered” language.
- Duration or streak alone establishing understanding claims.

---

### Category E — State Ownership

**Weight:** 10  

**Purpose:** Ensure every educational state has exactly one owner of meaning.

**Mandatory questions**

| ID | Question |
|----|----------|
| E1 | Does every educational state have one owner consistent with the Constitution and Registry ownership matrix? |
| E2 | Is any educational state duplicated with conflicting writers of meaning? |
| E3 | Is there conflicting authority for the same student-facing educational question? |

**Pass expectations**

- Study Progress, Current Learning Topic, Educational Evidence, Knowledge State / Twin belief, Estimated Mastery, Mission, Recommendations each retain single meaning ownership.
- Storage relocation is allowed; meaning ownership is not.
- Students never own Estimated Mastery as editable verified truth.

**Automatic NON-COMPLIANT triggers**

- Two services independently asserting different “today’s focus” with equal authority.
- Parallel progress metrics that mix coverage and mastery under one label.
- Twin-visible machinery competing with student-centred educational language as if both were educational law.

---

### Category F — Student Communication

**Weight:** 10  

**Purpose:** Ensure students can act with clarity.

**Mandatory questions**

| ID | Question |
|----|----------|
| F1 | Does the application communicate clearly in plain educational language? |
| F2 | Can students understand **What** (focus / claim)? |
| F3 | Can students understand **Why** (educational reason)? |
| F4 | Can students understand **What next** (lawful next step)? |
| F5 | Does wording avoid false certainty? |

**Pass expectations**

- Messaging aligns with EL-010 and Constitution Articles III and VIII.
- Engineering / Twin jargon is not student-facing educational copy.
- Why-copy is specific enough to be educationally meaningful, not generic theatre.

**Automatic NON-COMPLIANT triggers**

- Student-facing Digital Twin / internal score jargon as educational guidance.
- Certainty language without warrant.
- Mission or recommendation text that answers What without Why when the change is material.

---

### Category G — Educational Consistency

**Weight:** 10  

**Purpose:** Protect one educational story across product surfaces.

**Mandatory questions**

| ID | Question |
|----|----------|
| G1 | Do Study Plan, Dashboard, Mission, Recommendations, and Analytics communicate one educational story? |
| G2 | Where advisory content differs from mission authority, is the difference disclosed? |
| G3 | Do metrics labels preserve Study Progress vs Estimated Mastery vs Learning Progress distinctions? |

**Pass expectations**

- Surfaces may emphasise different roles (plan vs mission vs advice vs analytics) without contradicting meaning.
- Cross-surface contradiction on “what am I learning now?” fails review.

**Automatic NON-COMPLIANT triggers**

- Dashboard asserting a different Today’s Mission topic than the Mission surface without clear advisory framing.
- Analytics treating coverage as mastery.
- Plan coverage controls labelled or behaving as mastery certification.

---

### Category H — Educational Integrity

**Weight:** 10  

**Purpose:** Final trust and educator-defensibility check.

**Mandatory questions**

| ID | Question |
|----|----------|
| H1 | Does this capability increase (or at least preserve) student trust? |
| H2 | Would an educator agree with the educational behaviour? |
| H3 | Would a reasonable student misunderstand the educational meaning? |
| H4 | When integrity conflicts with optimisation, does trust win? |

**Pass expectations**

- Behaviour is defensible to a qualified educator familiar with official syllabus preparation.
- Known misunderstanding risks are eliminated or explicitly conditioned with user-visible clarity.
- Optimisation that confuses meaning is rejected even if engagement metrics improve.

**Automatic NON-COMPLIANT triggers**

- Clever diversion that silently breaks Learning Mode continuity.
- Educator would reject the claim type as dishonest.
- Student would reasonably believe mastery was earned without evidence.

---

## 4. Educational Compliance Rating

Each Category A–H receives exactly one rating.

| Rating | Definition | Scoring conversion |
|--------|------------|--------------------|
| **FULL** | Requirements for the category are met consistently across relevant behaviour, student-facing communication, and supporting evidence. No material defect remains. Minor documentation polish may remain if it does not affect educational meaning. | 100% of category weight |
| **PARTIAL** | Directionally compliant; material gaps remain that can mislead, conflict across surfaces, or leave warrant thin — but dominant behaviour does not systematically redefine educational law. | 50% of category weight |
| **NON-COMPLIANT** | Dominant behaviour contradicts Constitutional meaning, Registry logic, claim-type lawfulness, ownership, or integrity rules — or an automatic NON-COMPLIANT trigger fires. | 0% of category weight |

### Rating Discipline

1. Rate by **student-visible educational meaning** and **decision authority**, not by intent documentation alone.
2. Tests and docs support a FULL rating; they cannot manufacture FULL when product behaviour contradicts meaning.
3. Historical debt recorded in Registry Current Implementation Status does not upgrade PARTIAL to FULL.
4. When uncertain between PARTIAL and NON-COMPLIANT, choose NON-COMPLIANT if an automatic trigger is present; otherwise choose PARTIAL and state the residual risk.

---

## 5. Educational Governance Score

Subjective “looks good educationally” judgement is replaced by a weighted score out of **100**.

### Category Weights

| Category | Name | Weight |
|----------|------|--------|
| A | Constitution Compliance | 15 |
| B | Logic Registry Compliance | 15 |
| C | Educational Truth | 15 |
| D | Evidence Integrity | 15 |
| E | State Ownership | 10 |
| F | Student Communication | 10 |
| G | Educational Consistency | 10 |
| H | Educational Integrity | 10 |
| | **Total** | **100** |

### Score Calculation

For each category:

```
category_points = weight × rating_factor
```

where `rating_factor` is:

- FULL → `1.0`
- PARTIAL → `0.5`
- NON-COMPLIANT → `0.0`

```
Educational Governance Score = sum(category_points)   // maximum 100
```

### Score Bands (informative)

| Score | Band | Typical implication |
|-------|------|---------------------|
| 90–100 | Strong governance | Eligible for APPROVED if no automatic rejection trigger and no blocking condition remains |
| 75–89 | Conditional governance | Usually APPROVED WITH CONDITIONS |
| 50–74 | Weak governance | Usually REQUIRES REVISION |
| 0–49 | Failed governance | REJECTED unless rework restores category compliance |

Bands inform outcome selection; Section 6 criteria control the official outcome.

---

## 6. Review Outcomes

Every Educational Governance Review concludes with exactly one outcome.

| Outcome | Objective criteria |
|---------|-------------------|
| **APPROVED** | No category is NON-COMPLIANT; no automatic NON-COMPLIANT trigger remains open; Educational Governance Score ≥ 90; Categories A–D are FULL; residual notes are documentation-only and do not affect educational meaning. |
| **APPROVED WITH CONDITIONS** | No open automatic rejection under REJECTED rules; Educational Governance Score ≥ 75; at most one of Categories A–D is PARTIAL and none of A–D is NON-COMPLIANT; written conditions are specific, owned, and must be closed before Version 1.0 release (or before the stated gate). |
| **REQUIRES REVISION** | Educational Governance Score 50–74, **or** two or more PARTIAL ratings among Categories A–D, **or** any PARTIAL that leaves a material student-trust defect without an approved temporary containment; capability may proceed only after corrective revision and re-review. |
| **REJECTED** | Any of Categories A–D is NON-COMPLIANT; **or** any automatic NON-COMPLIANT trigger in Categories A–H remains; **or** Educational Governance Score < 50; **or** implementation redefined Constitution/Registry meaning without prior amendment. |

### Outcome Rules

1. Conditions must state **what**, **why**, and **gate** (e.g. before Version 1.0 release / before Internal Alpha continuation / before Architecture approval).
2. APPROVED WITH CONDITIONS is not a permanent state for Version 1.0 Release Gate — conditions must clear to APPROVED (or an explicit Architecture Office waiver recorded against this Standard, which itself requires Constitutional authority if meaning is affected).
3. Re-reviews after revision recompute the full score; prior scores are historical only.

---

## 7. Educational Release Gate

### Principle

Version 1.0 release is educationally unlawful unless the release candidate passes **all three** gates:

1. **Engineering Review** — correctness, tests, security, operability;
2. **Architecture Review** — layering, curriculum invariants, structural compliance;
3. **Educational Governance Review** — this Standard, with outcome **APPROVED** (conditions cleared).

### Gate Requirements for Educational Governance

Before Version 1.0 release:

| Requirement | Mandatory |
|-------------|-----------|
| Educational Governance Review completed using Section 8 template | Yes |
| Outcome is APPROVED | Yes |
| Categories A–D are FULL | Yes |
| Educational Governance Score ≥ 90 | Yes |
| No open Educational Governance conditions | Yes |
| Constitution and Logic Registry versions cited | Yes |
| Touched EL-xxx IDs listed and verified | Yes |

### Relationship to Other Reviews

- Passing Engineering or Architecture Review alone does **not** unlock release.
- Internal Alpha may proceed under APPROVED WITH CONDITIONS when Architecture Office accepts time-bounded educational risk; Version 1.0 Release Gate still requires cleared APPROVED.
- Feedback from Internal Alpha may motivate Governance Amendment; data does not itself waive this gate.

---

## 8. Capability Review Template

Every future Architecture / Educational / Release Educational Governance Review **must** use this template (copy into the review record).

```markdown
# Educational Governance Review

## Header
- Capability / Change ID:
- Title:
- Review Date:
- Reviewer(s):
- Constitution Version:
- Logic Registry Version:
- Review Standard Version: 1.0
- Surfaces / components in scope:
- Educational Logic IDs touched (EL-xxx):

## Scope Statement
- Educational behaviour introduced or changed:
- Explicit non-goals:

## Category Findings

### A — Constitution Compliance (Weight 15)
- A1–A4 answers:
- Findings / evidence:
- Rating: FULL | PARTIAL | NON-COMPLIANT
- Points:

### B — Logic Registry Compliance (Weight 15)
- B1–B4 answers:
- Findings / evidence:
- Rating:
- Points:

### C — Educational Truth (Weight 15)
- Claim inventory (Observed Fact / Derived Fact / Evidence-Based Estimate / Educational Advice):
- C1–C4 answers:
- Findings / evidence:
- Rating:
- Points:

### D — Evidence Integrity (Weight 15)
- D1–D5 answers:
- Findings / evidence:
- Rating:
- Points:

### E — State Ownership (Weight 10)
- E1–E3 answers:
- Findings / evidence:
- Rating:
- Points:

### F — Student Communication (Weight 10)
- What / Why / What next assessment:
- F1–F5 answers:
- Findings / evidence:
- Rating:
- Points:

### G — Educational Consistency (Weight 10)
- Study Plan / Dashboard / Mission / Recommendations / Analytics consistency:
- G1–G3 answers:
- Findings / evidence:
- Rating:
- Points:

### H — Educational Integrity (Weight 10)
- Trust / educator / misunderstanding assessment:
- H1–H4 answers:
- Findings / evidence:
- Rating:
- Points:

## Educational Governance Score
- Total: __ / 100
- Score band:

## Automatic Trigger Check
- List any automatic NON-COMPLIANT triggers fired (or “None”):

## Outcome
- APPROVED | APPROVED WITH CONDITIONS | REQUIRES REVISION | REJECTED

## Conditions (if any)
- Condition:
- Owner:
- Gate:
- Acceptance criteria:

## Release Gate Impact
- Eligible for Version 1.0 Educational Release Gate? Yes / No
- Rationale:

## Governance Follow-ups
- Constitution amendment required? Yes / No
- Logic Registry update required? Yes / No
- Internal Alpha observation hooks (if any):
```

---

## 9. Governance Lifecycle

Educational meaning and approval follow a single lifecycle. Implementation never leads law.

```text
Constitution
    ↓
Logic Registry
    ↓
Architecture
    ↓
Implementation
    ↓
Governance Review  (this Standard)
    ↓
Release Review
    ↓
Internal Alpha
    ↓
Feedback
    ↓
Governance Amendment  (Constitution and/or Registry as required)
    ↓
(return to Architecture / Implementation under amended law)
```

### Lifecycle Rules

1. **Constitution first.** Meaning changes require Article X amendment before product meaning changes.
2. **Registry second.** Behavioural educational logic changes require Registry update before approval of changed decision paths.
3. **Architecture third.** Designs must cite Constitution + Registry + this Standard.
4. **Implementation fourth.** Code realises governed behaviour; it does not invent educational law.
5. **Governance Review fifth.** Apply Categories A–H, score, and outcome.
6. **Release Review sixth.** Version 1.0 requires Engineering + Architecture + Educational Governance APPROVED.
7. **Internal Alpha seventh.** Empirical use stress-tests trust and consistency under controlled conditions.
8. **Feedback eighth.** Observations are classified; they inform priorities.
9. **Governance Amendment ninth.** Only explicit amendment changes educational law; then the cycle resumes.

Skipping upward stages is a governance defect and grounds for REJECTED or REQUIRES REVISION.

---

## 10. Future Evolution

This Standard reserves space for future educational programmes without defining their implementation.

When those programmes reach Architecture Review, expand this Standard with dedicated checklist appendices. Until then, Categories A–H already bind them by Constitution, Registry, and educational communication rules.

### Reserved Review Domains

| Domain | Review intent (reserved) | Do not define here |
|--------|--------------------------|--------------------|
| **Educational Intelligence** | Decision / coaching advice integrity; non-commandeering of Learning Mode | Algorithms, models, UI redesign |
| **Adaptive Learning** | Lawful interruption, disclosure, mode authority transitions | Scheduling formulae, Phase UX detail |
| **Digital Twin** | Invisibility; evidence → belief succession; non-confusion with Study Progress | Twin schemas, update engines |
| **Founder Intelligence** | Operator insight without redefining student-facing educational meaning | Dashboards, telemetry products |

### Evolution Discipline

1. Future sections may add category weights only by versioned amendment of this Standard.
2. Future capabilities may not claim APPROVED by inventing parallel review checklists that weaken Categories A–D.
3. Expansion of claim types beyond Observed Fact, Derived Fact, Evidence-Based Estimate, and Educational Advice requires Constitutional amendment first.

---

## 11. Cross References

**Superior authorities**

- `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001)
- `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002)

**This Standard**

- `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` (EGI-003)

**Consumers (must apply this Standard)**

- Architecture Reviews for educational capabilities;
- Educational Reviews;
- Internal Alpha Reviews and doctrines (IA-001 onward);
- Version 1.0 Release Reviews;
- Future Educational Intelligence, Adaptive Learning, Digital Twin, and Founder Intelligence educational workstreams.

**Diagnostic (do not override this Standard)**

- `knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md` and successors — findings inform review evidence; they do not redefine approval criteria.

---

## Closing

The Constitution states what educational truth is.  
The Registry states how educational decisions behave.  
This Standard states how compliance is judged.

Together they form objective educational governance for Kwalitec.

**End of Educational Governance Review Standard — Version 1.0**
