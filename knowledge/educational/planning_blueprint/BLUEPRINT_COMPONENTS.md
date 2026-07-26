# Blueprint Components

**Programme:** VI — Master Planner  
**Milestone:** MS005 — Planning Blueprint Model  
**Classification:** Educational building-block catalogue for Planning Blueprints  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **educational building blocks** that compose Planning Blueprint phases.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `PLANNING_BLUEPRINT_MODEL.md`
3. `BLUEPRINT_PHASES.md`
4. `../planning_engine/PLANNING_DECISION_ENGINE.md`
5. `../planning_engine/DECISION_PIPELINE.md`
6. `../planning/PLANNING_DECISION_MODEL.md`

Components **realise package decisions** as structure. They introduce **no new educational reasoning** and allocate **no dates**.

---

## 1. Purpose

Phases alone are too coarse for scheduling engines. Schedulers need educational building blocks — learning stretches, practice stretches, revision stretches, recovery capacity, buffers, milestones, checkpoints, and transition points — whose meanings were already settled in the Planning Decision Package.

This document catalogues those blocks so packing code places *authorised components*, not invented task types.

---

## 2. Component Principles

1. **Package-derived.** Every component instance traces to one or more PD-XX / D-class decisions.
2. **Educationally typed.** Type names educational job, not UI widget or calendar cell.
3. **Envelope-bound.** Intensity, practice density, and recovery load stay inside package bands.
4. **Composable.** Components nest inside phases; some (buffers, recovery, transitions) may span phase boundaries.
5. **Explainable.** Material components inherit package explainability (see `BLUEPRINT_EXPLAINABILITY.md`).
6. **Non-mastery-minting.** Completing a learning or practice block advances honest work; it does not create mastery claims.
7. **Date-free.** Components describe *what* and *why*; scheduling later decides *when*.

---

## 3. Component Catalogue

Identifiers (BC-XX) exist for traceability. Educational meaning is binding; display labels may vary.

| ID | Component | Educational job | Primary package warrants |
|----|-----------|-----------------|--------------------------|
| BC-01 | Learning block | First-pass study of syllabus units in lawful sequence | PD-01, PD-02, PD-06 |
| BC-02 | Practice block | Question practice / application on studied material | PD-05 |
| BC-03 | Consolidation block | Spaced return to recent topics during first-pass | PD-14 / D11 |
| BC-04 | Revision block | Consolidation under revision emphasis | PD-03, PD-04, D16 |
| BC-05 | Mock / exam-simulation block | Timed exam craft rehearsal | PD-15 / D15 |
| BC-06 | Recovery capacity | Lighter-load allowance after dense work, mocks, or disruption | PD-07, D13 |
| BC-07 | Buffer period | Spare educational capacity for slip, illness, replan | PD-08 / D12 |
| BC-08 | Milestone | Legible educational checkpoint | PD-09 / D14 |
| BC-09 | Review checkpoint | Focused check of recent learning / revision quality (not mastery fiat) | PD-09, PD-14, D16 families |
| BC-10 | Transition point | Explicit change of educational mission between phases or postures | PD-04; phase boundaries |
| BC-11 | Rest / freshness capacity | Planned light or zero-study capacity beyond declared leave | D17 (when in package) |
| BC-12 | Intensity envelope | Sustainable daily/weekly load band attached to active components | PD-06 / D7 / D10 |
| BC-13 | Risk-protection posture | Structural caution for short runway, thin evidence, prior fails | PD-10 / D20 |
| BC-14 | Confidence-protection posture | Earned-confidence structure (completable wins, truthful narration) | PD-11 |

Milestone examples (Learning blocks, Practice blocks, Revision blocks, Recovery capacity, Milestones, Review checkpoints, Buffer periods, Transition points) map onto BC-01…BC-10.

---

## 4. Component Specifications

### BC-01 — Learning block

| Aspect | Specification |
|--------|----------------|
| **What** | A contiguous educational unit of first-pass syllabus study under Learning Mode posture |
| **Why** | Coverage honesty requires dedicated learning work in official order |
| **Contains** | One or more syllabus topics/units from the package sequencing policy, starting from lawful coverage position |
| **Phase home** | Primarily BP-01; must not silently appear as primary work inside BP-04/BP-06 without package warrant |
| **Envelope** | Bounded by BC-12 intensity envelope |
| **Must not** | Skip prerequisites; re-teach completed coverage as new without educational reason; claim mastery on completion |

---

### BC-02 — Practice block

| Aspect | Specification |
|--------|----------------|
| **What** | Structured question practice / application on material already studied |
| **Why** | Coverage without application produces false readiness |
| **Contains** | Practice on studied scope at density set by PD-05 |
| **Phase home** | BP-02; also interleaved with BP-01 or inside BP-04 on revised scope when package warrants |
| **Must not** | Practise never-studied units as coverage substitute; mint mastery from practice volume alone |

---

### BC-03 — Consolidation block

| Aspect | Specification |
|--------|----------------|
| **What** | Light-to-moderate return to recently studied topics during first-pass |
| **Why** | Long syllabuses punish one-way marching; retention is part of readiness |
| **Contains** | Spaced return activities without abandoning sequence |
| **Phase home** | BP-03 windows interleaved with BP-01 |
| **Must not** | Convert the whole journey into early permanent revision without PD-04 |

---

### BC-04 — Revision block

| Aspect | Specification |
|--------|----------------|
| **What** | Study under Protected Revision emphasis — breadth and/or weak-area depth per D16 |
| **Why** | Exam readiness requires consolidation time that first-pass must not consume |
| **Contains** | Revision work inside the reserved revision region (PD-03) |
| **Phase home** | BP-04; high-value subset may continue into BP-06 |
| **Must not** | Be cannibalised for unfinished first-pass by default (F2) |

---

### BC-05 — Mock / exam-simulation block

| Aspect | Specification |
|--------|----------------|
| **What** | Timed exam-like simulation component |
| **Why** | Exam craft needs rehearsal when coverage makes it meaningful |
| **Contains** | Simulation intent from PD-15; paired recovery expectation via BC-06 when package requires |
| **Phase home** | BP-05; may sit adjacent to BP-04 or before BP-06 |
| **Must not** | Be narrated as pass/fail prophecy |

---

### BC-06 — Recovery capacity

| Aspect | Specification |
|--------|----------------|
| **What** | Structural lighter-load allowance after dense work, mocks, illness, leave, or abandoned intensity |
| **Why** | Learning and life interruption require cognitive and calendar recovery; punishment pacing is forbidden |
| **Phase home** | BP-07; also attached after BC-05 when PD-07 warrants |
| **Must not** | Be replaced by heroic make-up-every-hour compression as the default answer |

---

### BC-07 — Buffer period

| Aspect | Specification |
|--------|----------------|
| **What** | Spare educational capacity reserved for slip, illness, and replan |
| **Why** | Real candidates interrupt; buffers make recovery educationally possible |
| **Package rule** | Amount adaptive (PD-08); non-zero policy strongly expected when horizon allows; triage may shrink but must name residual risk |
| **Must not** | Be silently spent to hide infeasibility |

---

### BC-08 — Milestone

| Aspect | Specification |
|--------|----------------|
| **What** | Legible educational checkpoint (e.g. section coverage complete, revision start, final approach, mock window) |
| **Why** | Progress must be understandable; earned confidence needs visible structure (O7) |
| **Package warrant** | PD-09 / D14 — milestones expected; exact calendar position deferred to scheduling |
| **Must not** | Imply mastery or guaranteed readiness merely by being reached |

---

### BC-09 — Review checkpoint

| Aspect | Specification |
|--------|----------------|
| **What** | Focused educational check on recent learning or revision quality |
| **Why** | Supports honest self-knowledge and adaptive emphasis without inventing cold-start diagnosis as fact |
| **Distinct from BC-08** | Milestones mark journey structure; review checkpoints probe quality/retention of recent work |
| **Must not** | Assign definitive weak/strong labels without evidence or labelled declaration |

---

### BC-10 — Transition point

| Aspect | Specification |
|--------|----------------|
| **What** | Explicit structural marker that educational mission changes |
| **Why** | Students need a clear change of mission — not silent topic hopping dressed as “revision” |
| **Primary warrant** | PD-04 first-pass ↔ revision boundary; also recovery re-entry and final-approach freeze |
| **Must not** | Be omitted when PD-04 boundary is active; be hidden from explainability |

---

### BC-11 — Rest / freshness capacity

| Aspect | Specification |
|--------|----------------|
| **What** | Planned light or zero-study capacity beyond declared leave |
| **Why** | Sustainability and cognitive freshness; prevents seven-day grind as default |
| **Package warrant** | D17 when present; especially relevant in BP-06 |
| **Must not** | Be filled with punishment load after honest rest |

---

### BC-12 — Intensity envelope

| Aspect | Specification |
|--------|----------------|
| **What** | Sustainable daily/weekly intensity band and posture attached to active work components |
| **Why** | Keepable intensity compounds; heroic overload trains abandonment |
| **Package warrant** | PD-06 / D7 / D10 — band mandatory; posture within band adaptive |
| **Applies to** | BC-01…BC-05 primarily; recovery/rest components intentionally sit below the working band |
| **Must not** | Exceed declared available capacity; use intensity as discipline for missed days |

---

### BC-13 — Risk-protection posture

| Aspect | Specification |
|--------|----------------|
| **What** | Structural expression of PD-10 / D20 — caution under short runway, thin evidence, previous fails, weak foundations, adherence collapse |
| **Why** | Expert tutors name danger early; they do not publish optimistic theatre |
| **Appears as** | Tightened first-pass ambition, earlier revision emphasis, earlier feasibility disclosure, reduced buffer honesty labels — *as the package decided* |
| **Must not** | Hide infeasibility behind complete-looking component inventories |

---

### BC-14 — Confidence-protection posture

| Aspect | Specification |
|--------|----------------|
| **What** | Structural expression of PD-11 — completable intensity, clear next steps, truthful narration |
| **Why** | Confidence without warrant is dangerous; despair without guidance is useless |
| **Appears as** | Completable milestones, moderated envelopes under Confidence Restoration, honest understatement when evidence is thin |
| **Must not** | Deliver false reassurance or readiness inflation |

---

## 5. Composition Rules

1. **Phase containment.** Every BC-01…BC-05 instance belongs to an active phase (or an authorised interleave).
2. **Envelope attachment.** Working blocks without BC-12 are incomplete structure.
3. **Revision integrity.** BC-04 instances live inside the protected revision region created by PD-03.
4. **Mock + recovery.** When PD-15 and PD-07 co-warrant, BC-05 should be paired with BC-06 in structure (dates still deferred).
5. **Buffer visibility.** If PD-08 sets non-zero buffer policy, BC-07 must appear in the blueprint inventory.
6. **Transition honesty.** Active PD-04 requires a BC-10 transition point in the blueprint.
7. **No orphan components.** Components without package warrant are invalid.
8. **No forbidden components.** Structures that encode F1–F14 behaviours are invalid even if named innocently.

---

## 6. Mapping: Package Decisions → Components

| Package decision | Components typically realised |
|------------------|-------------------------------|
| PD-01 / PD-02 | BC-01 sequenced from starting coverage |
| PD-03 / PD-04 | BC-04 region + BC-10 transition |
| PD-05 | BC-02 density |
| PD-06 | BC-12 on working blocks |
| PD-07 | BC-06 |
| PD-08 | BC-07 |
| PD-09 | BC-08 (and often BC-09) |
| PD-10 | BC-13 colouring |
| PD-11 | BC-14 colouring |
| PD-14 | BC-03 |
| PD-15 | BC-05 (+ BC-06 when required) |
| PD-16 | May consume BC-07, enlarge BC-06, shrink non-critical BC-03, or escalate feasibility — never invent impossible BC-01 density |

---

## 7. What Scheduling May Do With Components

| Scheduling may… | Scheduling must not… |
|-----------------|----------------------|
| Place components onto days/hours inside phase regions | Invent component types with new educational jobs |
| Split a learning block across multiple study days | Change sequencing order inside BC-01 for “engagement” |
| Honour BC-12 minutes within declared capacity | Exceed envelopes or steal BC-04/BC-07 silently |
| Leave BC-07 unused until slip occurs | Delete buffers to make an infeasible plan look complete |

---

## 8. Cross References

- `PLANNING_BLUEPRINT_MODEL.md` — derivation rule
- `BLUEPRINT_PHASES.md` — phase homes for components
- `BLUEPRINT_PROGRESSION.md` — when components insert or change
- `BLUEPRINT_EXPLAINABILITY.md` — explaining component roles
- `../planning_engine/DECISION_PIPELINE.md` — PD-XX meanings
- `../planning/PLANNING_DECISION_MODEL.md` — D-class catalogue
