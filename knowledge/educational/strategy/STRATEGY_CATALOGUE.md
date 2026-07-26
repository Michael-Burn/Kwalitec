# Strategy Catalogue

**Programme:** VI — Master Planner  
**Milestone:** MS003 — Educational Strategy Framework  
**Classification:** Named educational strategies for IFoA preparation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **catalogue of educational strategies** Kwalitec may adopt for a student on a named examination sitting.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_STRATEGY_FRAMEWORK.md`
3. `student_profile/STUDENT_EDUCATIONAL_PROFILE.md`
4. `planning/EDUCATIONAL_PLANNING_MODEL.md`
5. `KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md`

Strategies are educational meanings — not database enums, UI badges, optimiser modes, or engagement labels. Implementations may map storage labels onto these meanings; they may not redefine the meanings in code.

> **Strategies name educational approach.  
> They do not schedule work and do not mint mastery.**

---

## 1. Purpose

An expert IFoA tutor summarises approach in plain language: *build foundations*, *progress steadily*, *practise hard*, *revise intensively*, *recover*, *rescue the sitting*, *maintain readiness*.

This Catalogue makes those approaches permanent and shareable so Master Planner selection, planning bias, and student narration share one vocabulary.

---

## 2. Catalogue Principles

1. **Meaning before labels.** UI copy may vary; educational meaning must match this Catalogue.
2. **Need-shaped.** Each strategy exists because a recurring IFoA educational need exists — not because a product feature needs a name.
3. **Non-punitive.** Recovery, Confidence Restoration, Exam Rescue, and Late Starter are diagnostic approaches — never shame brands.
4. **Truth-preserving.** No strategy may redefine Study Progress as mastery or invent pass guarantees.
5. **Constraint-bound.** Every strategy operates under Planning Constraints (prerequisites, revision protection, feasible load).
6. **Explainable.** Every strategy has a tutor rationale and student-facing meaning (see `STRATEGY_EXPLAINABILITY.md`).
7. **Finite set.** New strategies require corpus amendment — no silent invention in algorithms.

---

## 3. Strategy Entry Schema

Each strategy records:

| Field | Meaning |
|-------|---------|
| **ID** | Stable catalogue identifier (ES-XX) |
| **Name** | Canonical educational name |
| **Educational meaning** | What approach this is |
| **Tutor reading** | One-sentence expert summarisation |
| **When it fits** | Profile / journey conditions that warrant it |
| **What it privileges** | Educational emphasis under planning |
| **What it refuses** | Dishonest or premature emphases |
| **Common Profile anchors** | Typical states / dimension patterns (guidance) |
| **Typical planning bias** | How MS001 phases / adaptive decisions lean |
| **Must not claim** | Forbidden educational theatre |
| **Common exits** | Natural successor strategies |

“When it fits” is educational guidance for selection — formal selection reasoning is in `STRATEGY_SELECTION_MODEL.md`.

---

## 4. Strategy Catalogue

### ES-01 — Foundation Building

**Educational meaning:** Prioritise honest first-pass coverage of early and prerequisite-heavy syllabus units so later topics have something real to stand on.

**Tutor reading:** “Foundations first — we build the spine before we sprint.”

**When it fits:** Early journey; low or early-mid coverage; Learning Mode posture dominant; understanding evidence thin; foundation integrity matters more than exam rehearsal.

**What it privileges:** Sequential syllabus coverage; prerequisite integrity; sustainable study cadence; cautious practice that supports learning without pretending mastery.

**What it refuses:** Jumping to advanced topics for “motivation”; revision-as-main-story while first-pass foundations are missing; mock-heavy theatre without coverage warrant.

**Common Profile anchors:** S1 Beginning Study; S2 Building Foundation; D2 early; D16 sensitive; D19 Learning Mode dominant.

**Typical planning bias:** Foundation & First-Pass phase dominates; light consolidation only; revision window still reserved but not yet the daily story.

**Must not claim:** Early chapter completion equals exam readiness; light practice proves competence.

**Common exits:** Steady Progression; Practice Intensive (on covered units); Knowledge Consolidation (as first-pass lengthens).

---

### ES-02 — Steady Progression

**Educational meaning:** Sustain reliable, sequential first-pass progress across the syllabus at an intensity the student can keep — the default honest long-horizon approach when foundations are underway and crisis is absent.

**Tutor reading:** “Keep moving honestly — consistency beats heroics.”

**When it fits:** Active first-pass with workable capacity and time; consistency acceptable; no dominant recovery, rescue, or late-start crisis; practice and consolidation appear as supporting habits, not the whole approach.

**What it privileges:** Sustainable weekly rhythm; official order; gradual coverage growth; light interleaved return without abandoning first-pass.

**What it refuses:** Boom–bust intensity as the primary plan; silent abandonment of sequence; packing first-pass by consuming protected revision.

**Common Profile anchors:** S2 Building Foundation; S3 Practising (as secondary colour); D5/D14 stable enough; D18 not dominating.

**Typical planning bias:** Balanced Foundation & First-Pass with Consolidation Windows; intensity inside declared capacity.

**Must not claim:** Steady progress alone is Exam Ready; coverage ticks equal understanding.

**Common exits:** Practice Intensive; Knowledge Consolidation; Revision Intensive; Weak Topic Reinforcement; Recovery Strategy (if trajectory breaks).

---

### ES-03 — Knowledge Consolidation

**Educational meaning:** Deliberately interleave return to recently studied material so retention does not collapse during a long first pass — without converting the whole journey into premature full revision.

**Tutor reading:** “We protect what you’ve already studied while first-pass continues.”

**When it fits:** Mid-to-late first-pass; rising decay / retention risk (D13); long syllabus runway; enough coverage that return is educationally meaningful.

**What it privileges:** Spaced return; short consolidation blocks; retention-protecting structure alongside continued first-pass.

**What it refuses:** Abandoning remaining first-pass entirely too early; “revision” labels without return substance; treating consolidation as proof of mastery.

**Common Profile anchors:** S3 Practising; S5 Revising (light/interleaved); D8 emerging; D13 elevated.

**Typical planning bias:** Consolidation Windows denser; Protected Revision still reserved for the true pre-exam window.

**Must not claim:** Consolidation invents coverage never studied; retention is guaranteed by scheduling alone.

**Common exits:** Steady Progression; Practice Intensive; Revision Intensive; Weak Topic Reinforcement.

---

### ES-04 — Practice Intensive

**Educational meaning:** Convert covered study into demonstrated application — question practice and assessment exposure become the dominant educational emphasis on material already studied.

**Tutor reading:** “We’ve studied enough of this material to practise it hard and learn from evidence.”

**When it fits:** Meaningful coverage on target units; need to form understanding estimates; thin practice depth (D15) relative to coverage; or practice is the honest next step before revision claims.

**What it privileges:** Question practice; feedback loops; evidence-backed strength/weakness estimates; exam craft on covered topics.

**What it refuses:** Practising topics never studied as if coverage existed; using practice volume to claim mastery; skipping prerequisites to chase question banks.

**Common Profile anchors:** S3 Practising; D2 partial-to-advanced on practised scope; D4/D15 active need; D3 forming.

**Typical planning bias:** Practice density rises within lawful Learning / practice posture; first-pass may continue elsewhere.

**Must not claim:** One strong practice set equals durable competence; practice completed the syllabus.

**Common exits:** Weak Topic Reinforcement; Knowledge Consolidation; Revision Intensive; Steady Progression; High Performer Optimisation.

---

### ES-05 — Revision Intensive

**Educational meaning:** Make consolidation of previously studied material the dominant approach — deepen application, protect retention, and prepare exam behaviour under Revision Mode educational substance as the sitting approaches.

**Tutor reading:** “Revision is now the main story — we deepen what was already studied.”

**When it fits:** First-pass substantially advanced or remaining first-pass fits inside protected learning capacity; revision maturity must rise; exam approach nearing; D19 Revision Mode substance warranted.

**What it privileges:** Protected revision capacity; weak-area prioritisation within revised material; exam-like application; freeze or tight limit on new first-pass expansion.

**What it refuses:** Consuming revision for new first-pass; revision theatre without prior coverage; inventing “revised” status for unstudied units.

**Common Profile anchors:** S5 Revising; S6 Exam Preparation; D8 rising; D7 shorter runway; D2 largely advanced.

**Typical planning bias:** Protected Revision and Final Approach dominate; mocks placed when educationally meaningful.

**Must not claim:** Calendar proximity equals Exam Ready; revision guarantees a pass.

**Common exits:** Exam Rescue (if feasibility collapses); Balanced Maintenance; High Performer Optimisation; Weak Topic Reinforcement.

---

### ES-06 — Weak Topic Reinforcement

**Educational meaning:** Deliberately reinforce fragile, weak, or uneven areas — foundations or evidenced weak topics — before treating progress as secure.

**Tutor reading:** “We strengthen what is shaky; we do not pretend even competence.”

**When it fits:** D3/D4/D16 show material weaknesses; poor mocks on covered topics; uneven estimates despite coverage; Strengthening state dominant.

**What it privileges:** Targeted return to weak units; foundation repair; practice focused on fragility; honest understatement of readiness until warrant improves.

**What it refuses:** Ignoring evidenced weakness to “stay on schedule theatre”; shaming the student for discovering gaps; expanding new topics while foundations are broken if integrity is at risk.

**Common Profile anchors:** S4 Strengthening; possibly S9 At Risk overlay; D3/D4 weak; D16 concerns.

**Typical planning bias:** Adaptive emphasis toward weak units within lawful sequence / revision rules; may pause aggressive first-pass expansion locally.

**Must not claim:** Reinforcement is punishment; weakness discovery means the student “failed the plan.”

**Common exits:** Practice Intensive; Steady Progression; Revision Intensive; Recovery Strategy; Confidence Restoration.

---

### ES-07 — Confidence Restoration

**Educational meaning:** Rebuild educational and felt confidence after setbacks, harsh mock feedback, anxiety spikes, or motivation collapse — while keeping hard educational facts honest.

**Tutor reading:** “We restore confidence with achievable, truthful wins — not false reassurance.”

**When it fits:** Soft signals fragile (D11); educational confidence uneven (D10); after fail/mock shock; student can study but trust in self or process is damaged; not primarily a coverage emergency.

**What it privileges:** Sustainable short wins; clear explainability; reduced cognitive load; practice or revision that rebuilds warrant without overwhelm; non-punitive narration.

**What it refuses:** Pass guarantees as pep talk; inflating readiness estimates to soothe; ignoring real feasibility risk while “being positive.”

**Common Profile anchors:** Soft D10/D11 distress; may overlay Practising / Revising / Recovering; previous attempt aftermath (D9).

**Typical planning bias:** Intensity moderated; emphasis on completable sessions; truth-preserving encouragement via explainability.

**Must not claim:** Felt confidence equals understanding; restored mood equals Exam Ready.

**Common exits:** Steady Progression; Practice Intensive; Revision Intensive; Recovery Strategy; Balanced Maintenance.

---

### ES-08 — Recovery Strategy

**Educational meaning:** Restore a viable study trajectory after interruption, illness, leave, burnout, or abandoned intensity — reduce load before inventing heroic catch-up; preserve lawful educational history.

**Tutor reading:** “Restart that still counts — without shame or false diagnosis.”

**When it fits:** S7 Recovering; active D12 recovery history; consistency/reliability disrupted; capacity needs recalibration; student returning to cadence.

**What it privileges:** Lower intensity; re-established rhythm; re-orientation to current coverage and evidence; protected what still counts; gradual rebuild.

**What it refuses:** Immediate “make up every lost hour”; erasing Study Progress because of a gap; At Risk branding as moral failure.

**Common Profile anchors:** S7 Recovering; S8 Returning After Break (often adjacent); D5/D14 disrupted; D12 active.

**Typical planning bias:** Recovery / Replan phase meaning; buffers; capacity re-intake; postpone rescue heroics until cadence returns.

**Must not claim:** Gap wiped progress; recovery requires punishment pace.

**Common exits:** Steady Progression; Foundation Building; Practice Intensive; Confidence Restoration; Returning path into Knowledge Consolidation / Revision Intensive.

---

### ES-09 — Exam Rescue

**Educational meaning:** Confront material danger to honest exam readiness under short runway — triage what still counts educationally, protect high-value revision/practice, and stop unlawful expansion that cannot finish truthfully.

**Tutor reading:** “Time is tight — we rescue what still matters and stop pretending everything fits.”

**When it fits:** S9 At Risk dominates near the sitting; D18 elevated with short D7; large remaining work vs capacity; previous plan infeasible; need triage not optimism theatre.

**What it privileges:** Feasibility honesty; high-value covered topics; revision/practice on what can still be strengthened; explicit trade-offs; possible sitting counsel as educational advice (not algorithmic destiny).

**What it refuses:** Impossible catch-up calendars; silent first-pass packing into revision; pass/fail probability theatre; shame narratives.

**Common Profile anchors:** S9 At Risk; S6 Exam Preparation under distress; D7 short + D2 remainder large and/or D14 collapse.

**Typical planning bias:** Final Approach / Recovery–Replan hybrid; freeze new frontiers; protect remaining revision substance.

**Must not claim:** Rescue guarantees a pass; numeric fail odds as product truth.

**Common exits:** Revision Intensive (if stabilised); Confidence Restoration; Recovery Strategy; Balanced Maintenance (rare, if rescued early); post-sitting replan (outside this sitting’s strategy).

---

### ES-10 — Late Starter Strategy

**Educational meaning:** Begin or re-scope preparation with unusually short runway relative to remaining syllabus — design an honest compressed approach that still respects prerequisites and revision minima, rather than a full leisurely first-pass fiction.

**Tutor reading:** “You are starting late for this sitting — we plan honestly for the time you have.”

**When it fits:** Early coverage with short D7 from the outset; late registration relative to syllabus length; capacity insufficient for full leisurely journey; student needs truth early.

**What it privileges:** Ruthless prioritisation within official order where lawful; early feasibility disclosure; protected minimum revision; sustainable intensity even under compression; possible sitting realism conversations.

**What it refuses:** Pretending a full standard journey fits; skipping prerequisites wholesale; “speedrun mastery”; hiding infeasibility until week six.

**Common Profile anchors:** S1/S2 with harsh D7/D18; M1 resolving into known short horizon; D6 limited.

**Typical planning bias:** Compressed Foundation & First-Pass with earlier triage checkpoints; revision still reserved (smaller but non-zero).

**Must not claim:** Compression equals equivalent readiness to a full journey; late start is the student’s moral failing.

**Common exits:** Steady Progression (if horizon eases — e.g. date change); Exam Rescue (if compression fails); Foundation Building (if more time appears); Recovery Strategy (if overload breaks adherence).

---

### ES-11 — High Performer Optimisation

**Educational meaning:** With strong coverage, practice depth, and evidence warrant already in place, optimise depth, exam craft, timing, and polish — not invent foundational work the student no longer needs.

**Tutor reading:** “Foundations and practice look strong — we refine for exam performance.”

**When it fits:** Advanced coverage; solid D3/D4/D15; revision mature or maturing; not At Risk; educational confidence sufficient; room to deepen rather than rescue.

**What it privileges:** Exam technique; timed practice; targeted weak-edge polish; mock calibration; efficiency without burnout.

**What it refuses:** Reinvention of beginner first-pass as “engagement”; restless strategy churn; readiness inflation beyond warrant.

**Common Profile anchors:** Near S6/S10 trajectory; strong D2/D8/D15; D18 calm.

**Typical planning bias:** Mock & Exam Simulation and Final Approach quality; light maintenance of retention.

**Must not claim:** High performer status is permanent identity; optimisation guarantees distinction or pass.

**Common exits:** Balanced Maintenance; Revision Intensive; Weak Topic Reinforcement (if a mock reveals a gap); Confidence Restoration (if a shock hits).

---

### ES-12 — Balanced Maintenance

**Educational meaning:** Maintain honest readiness when preparation is already in good shape — protect retention and exam sharpness without unnecessary upheaval or intensity escalation.

**Tutor reading:** “You’re in good shape — we maintain, we don’t reinvent.”

**When it fits:** Provisional Exam Ready or stable Exam Preparation with adequate warrant; consistency good; no new crisis; goal is preserve and lightly sharpen.

**What it privileges:** Light spaced return; modest practice; sleep and freshness protection; stable rhythm; avoid last-minute syllabus expansion.

**What it refuses:** Opening new first-pass frontiers lightly; panic intensity; changing strategy for novelty.

**Common Profile anchors:** S10 Exam Ready; stable S6; D18 not dominating; D5/D14 sound.

**Typical planning bias:** Final Approach stabilisation; minimal disruption.

**Must not claim:** Maintenance freezes readiness forever; no further practice needed permanently.

**Common exits:** Weak Topic Reinforcement; Exam Rescue; Confidence Restoration; Revision Intensive (if decay appears).

---

## 5. Strategy Families (Educational Grouping)

Families help tutors and algorithms reason about *kind* of approach without collapsing IDs.

| Family | Strategies | Shared educational job |
|--------|------------|------------------------|
| **Build** | ES-01 Foundation Building; ES-02 Steady Progression | Grow honest first-pass coverage |
| **Deepen** | ES-03 Knowledge Consolidation; ES-04 Practice Intensive; ES-06 Weak Topic Reinforcement | Turn coverage into durable, evidenced capability |
| **Approach** | ES-05 Revision Intensive; ES-11 High Performer Optimisation; ES-12 Balanced Maintenance | Prepare and stabilise for the sitting |
| **Restore** | ES-07 Confidence Restoration; ES-08 Recovery Strategy | Rebuild capacity, cadence, or confidence |
| **Triage** | ES-09 Exam Rescue; ES-10 Late Starter Strategy | Face short-horizon feasibility honestly |

A student moves among families as the Profile evolves. Family labels are for reasoning — student speech uses strategy names, not family jargon.

---

## 6. Relationship to Constitutional Modes

| Strategy emphasis | Typical lawful mode posture |
|-------------------|----------------------------|
| Foundation Building, Steady Progression, Late Starter (early) | Learning Mode dominant |
| Practice Intensive, Weak Topic Reinforcement | Learning Mode with practice substance; or disclosed practice emphasis |
| Knowledge Consolidation, Revision Intensive, Balanced Maintenance, High Performer Optimisation | Increasing Revision Mode substance as warranted |
| Recovery, Confidence Restoration | Mode follows capacity — often Learning Mode at reduced intensity |
| Exam Rescue | Often Revision / Final Approach substance; Learning Mode expansion tightly constrained |

Strategy does **not** silently override Learning Mode mission authority. Mode activation and disclosure remain constitutional. Strategy tells planning *what approach to design*; Runtime modes govern *daily topic authority* under Article VI.

---

## 7. Forbidden Pseudo-Strategies

| Pseudo-strategy | Why forbidden |
|-----------------|---------------|
| “Engagement shuffle” | Violates curriculum primacy |
| “Mastery grind from coverage ticks” | Conflates Study Progress with mastery |
| “Guaranteed pass path” | Invents certainty |
| “Punish missed days with double load” | Burnout and shame theatre |
| “Personality type track” | Not educational diagnosis |
| “Random weekly theme” | Non-deterministic approach without Profile warrant |

---

## 8. Extending the Catalogue

To add a strategy later:

1. Demonstrate a distinct IFoA educational need not covered by an existing entry.
2. Write full schema fields (meaning, privileges, refuses, anchors, exits).
3. Update selection, transitions, and explainability documents.
4. Preserve determinism and understatement rules.

Absence of a marketing name is not a reason to add a strategy.

---

## 9. Cross References

- `EDUCATIONAL_STRATEGY_FRAMEWORK.md` — constitutional overview
- `STRATEGY_SELECTION_MODEL.md` — how to choose among these
- `STRATEGY_TRANSITIONS.md` — succession among these
- `STRATEGY_EXPLAINABILITY.md` — how to speak these
- `../student_profile/PROFILE_STATES.md` — diagnostic anchors
- `../planning/EDUCATIONAL_PLANNING_MODEL.md` — journey phases strategy biases
