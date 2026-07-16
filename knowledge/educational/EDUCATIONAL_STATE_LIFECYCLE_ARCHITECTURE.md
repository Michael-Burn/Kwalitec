# Educational State Lifecycle Architecture

**Capability ID:** EIP-005-DESIGN  
**Programme:** Educational Integrity Programme  
**Title:** Educational State Lifecycle Architecture  
**Classification:** Specialised Educational Architecture — subordinate design specification  
**Status:** APPROVED — architecture implemented under EIP-005 (`EDUCATIONAL_CONTINUITY_STANDARD.md`)  
**Version:** 1.1  
**Date:** 2026-07-15  
**Nature:** Architecture reference — continuity implementation realises §4–5 without redesigning Twin / EI algorithms  

---

## Authority

This document defines **how every educational state evolves** across the student learning journey.

It complements and is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001) — highest educational authority; defines *what* educational states mean  
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002) — operational behaviour of educational decisions  
3. `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` (EIP-001) — ownership and lawful writers  
4. `EDUCATIONAL_EVIDENCE_MODEL.md` (EIP-002-DESIGN) — what Educational Evidence *is*  
5. `EDUCATIONAL_EVIDENCE_AUTHORITY.md` (EIP-002) — which observations may enter Evidence for Twin updates  
6. `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` (EIP-000) — programme sequencing  

Authority order for this subject:

> Constitution defines educational **meaning**.  
> State Authority Matrix defines **who may mutate**.  
> Evidence Model and Evidence Authority define **what may warrant understanding**.  
> **This Architecture defines lifetime, transition, persistence, dependence, deletion, and continuity.**

This document:

- does **not** amend the Constitution, Registry, or other governance documents;
- does **not** redesign Twin algorithms, Educational Intelligence, or product surfaces;
- does **not** implement code or prescribe storage schemas;
- governs future EIP continuity / readiness work that realises lifecycle integrity.

**The Educational State Lifecycle Architecture is the architectural reference for future Educational Integrity implementation of continuity and state succession.  
Implementation never invents lifecycle rules absent from this Architecture (or from higher EGI authorities).**

---

## Table of Contents

1. [Educational Lifecycle Philosophy](#1-educational-lifecycle-philosophy)
2. [Educational State Catalogue](#2-educational-state-catalogue)
3. [Lifecycle Diagrams](#3-lifecycle-diagrams)
4. [Deletion Rules](#4-deletion-rules)
5. [Educational Continuity](#5-educational-continuity)
6. [Knowledge vs Mastery Relationship](#6-knowledge-vs-mastery-relationship)
7. [Version 1 Boundaries](#7-version-1-boundaries)
8. [Cross References](#8-cross-references)

---

## 1. Educational Lifecycle Philosophy

### 1.1 The Educational Chain

Every material educational outcome in Kwalitec must be traceable to one succession chain:

```
Educational Activity
         ↓
Educational Observation
         ↓
Educational Evidence          ← only when authorised (EIP-002)
         ↓
Educational State Updates     ← only under State Authority Matrix
         ↓
Educational Guidance          ← advice / missions / readiness narration
```

This chain is educational law, not an implementation pipeline. Skipping a link invents certainty or mutates the wrong state.

| Stage | Meaning | Typical examples | What it may lawfully do |
|-------|---------|------------------|-------------------------|
| **Educational Activity** | Something the student or system did or scheduled | Open topic, start mission, mark coverage, accept advice, attempt questions | May create Observation; may update Study Progress when coverage is warranted; never writes Twin-owned estimates by itself |
| **Educational Observation** | Durable historical record of an activity or soft signal | Study Attempt row, confidence self-report, session duration, reflection | May be retained as history; does **not** by itself rewrite Estimated Knowledge / Mastery |
| **Educational Evidence** | Observation authorised to warrant understanding claims | Structured question results; future quiz / mock / mission-assessment / official exam outcomes | Necessary input for Twin-owned estimate succession |
| **Educational State Updates** | Lawful mutation of educational states | Coverage advance; estimate revision; Current Learning reconcile; mission lifecycle | Only Permitted Writers under EIP-001 |
| **Educational Guidance** | Advice and commitments built from state | Today’s Mission, Recommendations, Readiness summaries | Never becomes Evidence of understanding |

### 1.2 Binding principles

1. **Activity is not understanding.** Completing work advances coverage or records Observation; it does not mint knowledge.
2. **Observation is not Evidence of understanding until authorised.** Soft signals remain history without Twin write rights (Evidence Authority).
3. **Evidence succeeds into estimates; estimates do not rewrite Evidence.** History is not edited to fit a preferred belief.
4. **Guidance consumes state; guidance never authors Evidence.** Recommendations and missions are judgements/actions, not observations of competence.
5. **Educational history belongs to the learner**, not to a disposable Study Plan container.
6. **Continuity is constitutional.** Changing study context must not invent discontinuity or silently erase rightful progress without clear educational justification (Constitution II §1.8).
7. **Silence is preferred to unlawful certainty.** Thin history keeps estimates unchanged rather than inventing scores.

### 1.3 Two parallel spines

The learning journey runs on two spines that must never collapse:

| Spine | Primary question | Core states |
|-------|------------------|-------------|
| **Coverage spine** | What have I studied / what am I studying now? | Study Progress → Current Learning → Mission (Learning Mode) |
| **Understanding spine** | What observations support claims about how well I know this? | Study Attempt → Observation → Evidence → Estimated Knowledge / Estimated Mastery → Readiness (as factor) / Recommendation (advisory) |

Mission Completion may connect the spines only as **coverage advancement** on the first spine, and as an **opportunity to gather Observation/Evidence** on the second — never as automatic mastery.

---

## 2. Educational State Catalogue

For each state below, **Owner** and **Authority** follow the Educational State Authority Matrix and Constitution Article IV. Where the Matrix has not yet listed a state, ownership follows the Constitution and this Architecture; writers remain those constitutionally permitted.

---

### 2.1 Study Progress

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Answer “What have I completed studying?” as honest syllabus coverage, never competence. |
| **Owner** | Student for declarations; Application / Study Plan domain for recording consistency (EIP-001: Study Plan). |
| **Authority** | Mission Completion (coverage); Manual Topic Completion. |
| **Persistence** | Durable per student + syllabus unit identity (topic / curriculum unit). Must survive plan reorganisation when continuity rules apply (Section 5). |
| **Creation** | Created incomplete when a unit enters the student’s active study context (plan scope / curriculum enrolment). |
| **Update** | Incomplete → completed studying via lawful coverage writers only. Remains Study Progress when later Evidence revises estimates. |
| **Deletion** | Must **not** disappear solely because a Study Plan is deleted or archived (Section 4). Explicit student-authorised coverage reset may erase or reopen coverage with disclosed consequence. |
| **Dependencies** | Official syllabus structure; active study context for *presentation*; Mission Completion / manual completion for *mutation*. Does **not** depend on Estimated Mastery. |
| **Student Visibility** | Highly visible as completed / not completed studying. |
| **Future Evolution** | Stronger multi-plan continuity; archive semantics; never rewrite coverage when Revision Mode activates. |

---

### 2.2 Current Learning

*(Constitution name: Current Learning Topic)*

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Answer “What am I learning now?” — authorised next learning focus under Learning Mode. |
| **Owner** | Study Plan / Application, subordinate to syllabus order and Study Progress. |
| **Authority** | Learning Mode (reconciliation from Study Progress + syllabus). |
| **Persistence** | Derived or lightly persisted pointer into syllabus order for the active study context. Pointer may refresh; underlying Study Progress must remain. |
| **Creation** | Established when an active Study Plan / study context exists and Learning Mode resolves the first incomplete unit (or equivalent lawful focus). |
| **Update** | Advances when Study Progress completes the current unit; resynchronises when active study context lawfully changes. |
| **Deletion** | Pointer may clear when no active plan exists. Clearing the pointer must not erase Study Progress or Evidence history. |
| **Dependencies** | Study Progress; official syllabus order; active Study Plan context. Recommendations must not mutate this state. |
| **Student Visibility** | Highly visible as today’s learning focus under Learning Mode. |
| **Future Evolution** | Revision / Diagnostic / Adaptive Modes may lawfully redirect focus only when activated, disclosed, and constitutionally authorised — without rewriting Study Progress. |

---

### 2.3 Educational Observation

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Retain durable history of educationally relevant happenings and soft signals so the system can later decide which observations become Evidence. |
| **Owner** | Application educational history / recording pathways (distinct from Twin ownership of estimates). |
| **Authority** | Lawful activity recorders (attempts, reflections, soft signals, session metadata) — **not** recommendation engines writing fake observations. |
| **Persistence** | Durable learner history. Soft or engagement observations may remain even if they never become Understanding Evidence. |
| **Creation** | Created when an Educational Activity yields a recordable happening (e.g. Study Attempt started/submitted, confidence captured, duration recorded). |
| **Update** | Generally append-only. Corrections for clerical error must preserve audit honesty; estimates never rewrite Observations to fit preferred conclusions. |
| **Deletion** | Soft signals may be user-cleared only under explicit privacy/educational rules. Performance Observations that fed Evidence must not be silently scrubbed to invent higher competence. Account erasure is a separate privacy regime. |
| **Dependencies** | Educational Activity; student + educational context attribution. |
| **Student Visibility** | Students experience practice results, feedback, and reflections — not “Observation” jargon. |
| **Future Evolution** | Richer observation taxonomy; explicit decay/weighting policies; clearer separation from Evidence stores. |

---

### 2.4 Educational Evidence

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Supply the only lawful observational input from which knowledge-oriented beliefs may evolve. |
| **Owner** | Educational Evidence Pipeline / domain (EIP-001). |
| **Authority** | Assessment Results; Mission Assessment Results; Quiz Results; Mock Examination Results; and Version 1 authorised Structured Question Results (Evidence Authority). |
| **Persistence** | Durable, attributable, retained as history. Interpretable repeatedly; not silently rewritten. |
| **Creation** | Created only when an Educational Observation is authorised for understanding claims (EIP-002 gate). |
| **Update** | Accumulation and lawful supersession / de-weighting only by named educational rules — never by recommendation convenience. |
| **Deletion** | Must not disappear because a Study Plan is deleted. Must not be deleted to “clean” a preferred estimate. Privacy/account deletion is a separate regime with disclosed consequence. |
| **Dependencies** | Qualifying Educational Observation; Evidence Model quality ranking; Evidence Authority catalogue. |
| **Student Visibility** | Plain language (practice results, study checks). Internal domains may retain the term Evidence. |
| **Future Evolution** | Expand authorised pathways (quiz, mock, official exam); evidence density floors; dual Twin stores without collapsing meaning. |

---

### 2.5 Estimated Knowledge

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Communicate provisional current understanding without claiming certified knowledge. |
| **Owner** | Digital Twin / authorised estimation paths. |
| **Authority** | Educational Evidence only (via Twin-permitted writers). |
| **Persistence** | Current estimate posture (scalar or structure). Must remain distinguishable from Study Progress even if co-located in storage. |
| **Creation** | Born thin or absent. May first appear only after lawful Evidence interpretation — never from coverage alone. |
| **Update** | Rises, falls, or stays unchanged as Evidence accumulates. Absence of Evidence ⇒ no artificial write (correct silence). |
| **Deletion** | Estimates may be superseded by newer Estimates. History of supporting Evidence must remain. Plan deletion must not wipe Knowledge posture as a side-effect of clearing plan rows without continuity design. |
| **Dependencies** | Educational Evidence; Twin / authorised estimator. Forbidden writers: Completion, Confidence, Study Progress, Recommendations. |
| **Student Visibility** | Visible when material, always as an **estimate**. |
| **Future Evolution** | Separation from Estimated Mastery presentation/stores where product debt currently shares one scalar; richer Knowledge State structure without student Twin theatre. |

---

### 2.6 Estimated Mastery

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Support long-horizon preparation judgement of how confidently a unit is mastered — always provisional and evidence-derived. |
| **Owner** | Digital Twin / authorised estimation paths. Students never own edit rights to declare mastery as fact. |
| **Authority** | Educational Evidence only. |
| **Persistence** | Current mastery estimate / stage. Distinct meaning from Study Progress and from Estimated Knowledge (Section 6). |
| **Creation** | Absent until sufficient attempt or assessment Evidence exists. High stages require accumulation, not theatre. |
| **Update** | Evidence-driven succession only. Mission completion and student-felt confidence must not author mastery. |
| **Deletion** | Same continuity principles as Estimated Knowledge. Never auto-deleted by coverage reset unless student explicitly authorises a wider educational reset with disclosure. |
| **Dependencies** | Accumulated Educational Evidence; Twin estimation. Must never write Study Progress. |
| **Student Visibility** | Visible only when estimate exists; labelled Estimated Mastery (or equivalent honest language). |
| **Future Evolution** | Density floors; stage policy; review scheduling consumers; still never checkbox mastery. |

---

### 2.7 Readiness

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Answer “How prepared am I becoming?” as an explainable preparedness posture — not a next-action engine. |
| **Owner** | Readiness authority within Educational Intelligence / authorised readiness services. |
| **Authority** | Derived judgement writers under readiness services; consume coverage, estimates, plan/time context, and related factors with warrant. Must not mutate Study Progress, Evidence, or Twin estimates. |
| **Persistence** | Typically derived / recomputed. Snapshot persistence is optional and subordinate to live inputs. |
| **Creation** | Appears when enough lawful inputs exist to compute a preparedness posture; otherwise “not yet estimable.” |
| **Update** | Continuously revised as Study Progress, Evidence-informed estimates, and plan context change. |
| **Deletion** | Derived readiness evaporates when inputs are gone — but rightful input history must not be erased merely to force a different readiness story. |
| **Dependencies** | Study Progress (coverage factor); Estimated Knowledge / Mastery when warranted; plan and time context; Review habits where used. Must not silently become Today’s Mission. |
| **Student Visibility** | Plain readiness summaries; uncertainty disclosed when warrant is thin. Always framed as estimated/preparedness language when composite. |
| **Future Evolution** | Single student-facing readiness meaning; specialised Registry logic (FEL-004); eliminate dual competing algorithms under one label. |

---

### 2.8 Recommendation

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Advise what the student might do next, with explainability — without commandeering Learning Mode. |
| **Owner** | Recommendation / advisory authority (Educational Intelligence advisory path). |
| **Authority** | Recommendation Engine may create/update **recommendation artefacts** only. Forbidden from writing Study Progress, Current Learning, Mission (Learning Mode persistence), Evidence, or Twin estimates. |
| **Persistence** | Advisory artefacts and optional Decision Journal (accept/dismiss) as preference history — not Evidence of understanding. |
| **Creation** | Generated from lawful educational inputs (coverage, estimates, readiness factors, plan context) under explainability standards. |
| **Update** | Regenerated or revised as state changes; student accept/dismiss records preference, not competence. |
| **Deletion** | Advisory artefacts may expire or be superseded freely. Preference history may be retained. Must not erase Evidence or Study Progress when dismissed. |
| **Dependencies** | Consumers of educational state (read-only for understanding/coverage). Learning Mode primacy in Version 1. |
| **Student Visibility** | Visible as suggestions; What / Why / Next; optional vs Learning Mode disclosed. |
| **Future Evolution** | Stronger Decision Journal productisation; mode-aware advice when Revision / Adaptive Modes exist. |

---

### 2.9 Mission

*(Includes Today’s Mission under Learning Mode)*

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Translate educational state into one actionable study commitment for the day/session. |
| **Owner** | Planning Service for Learning Mode persistence (EIP-001). |
| **Authority** | Learning Mode / PlanningService mission generation and mission lifecycle status updates. |
| **Persistence** | Persisted daily/session commitment for the study day. Distinct from Recommendation artefacts. |
| **Creation** | Generated from Current Learning Topic and plan context under Learning Mode (Version 1). |
| **Update** | Task/status lifecycle (in progress, completed, abandoned, superseded). Completion may update Study Progress for covered units; may open Observation/Evidence pathways when outcomes are recorded. |
| **Deletion** | Mission rows may complete lifecycle and archive. Historical missions that produced Attempts/Evidence should remain reconstructable for educational history. Plan deletion must not erase attempt/evidence history that missions helped create. |
| **Dependencies** | Current Learning (Version 1); Study Plan context; Study Progress. Recommendations must not retarget Learning Mode missions. |
| **Student Visibility** | Primary daily surface (“Today’s Mission” or equivalent). |
| **Future Evolution** | Mode-gated focus under Revision / Adaptive Mode with disclosure; Mission Intelligence only under Decision Hierarchy. |

---

### 2.10 Study Attempt

*(Constitution name: Attempt)*

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Capture a discrete practice/performance episode that may yield Observation and, when authorised, Educational Evidence. |
| **Owner** | Student performs; Application records; Evidence domain consumes authorised outcomes. |
| **Authority** | Attempt recording pathways (mission study sessions, quizzes when implemented, etc.). |
| **Persistence** | Durable learner history. Version 1 interim understanding pathway relies on structured question results on Study Attempts. |
| **Creation** | Started when the student begins a bounded attempt/session against educational material. |
| **Update** | Submitted/completed with outcomes (questions attempted/correct, scores, soft signals). Outcomes feed Observation; authorised accuracies may enter Evidence and permit Twin estimate updates. |
| **Deletion** | Must not disappear solely because a Study Plan is deleted. Attempts are educational history belonging to the learner. |
| **Dependencies** | Mission or other practice surface; topic/curriculum context; optional structured scoring. Attempt alone is not Study Progress completion or mastery. |
| **Student Visibility** | Practice results, scores, feedback — never automatic mastery certificates. |
| **Future Evolution** | Richer assessment types; clearer separation of attempt Observation vs authorised Evidence subsets. |

---

## 3. Lifecycle Diagrams

### 3.1 Full succession (understanding + coverage)

```
Study Topic (syllabus unit in active context)
         │
         ├──────────────────────────────────────────┐
         ▼                                          │
  Study Progress                              Current Learning
  (coverage incomplete → completed)           (authorised focus)
         │                                          │
         │                                          ▼
         │                                       Mission
         │                                   (Today’s commitment)
         │                                          │
         │                          Attempt Questions / practice
         │                                          │
         │                                          ▼
         │                              Educational Observation
         │                                          │
         │                     ┌── authorised? ─────┤
         │                     │ no                 │ yes
         │                     ▼                    ▼
         │              Remain history      Educational Evidence
         │              (soft / engagement)         │
         │                                          ▼
         │                               Estimated Knowledge
         │                                          │
         │                                          ▼
         │                               Estimated Mastery
         │                                          │
         │                                          ▼
         │                                    Readiness
         │                                   (preparedness)
         │                                          │
         │                                          ▼
         │                                 Recommendation
         │                              (advisory guidance)
         │
         └── Mission Completion may advance Study Progress (coverage)
             without writing Estimated Knowledge / Mastery
```

### 3.2 Coverage-only path (lawful silence)

```
Study Topic
    ↓
Mission / Manual completion studying
    ↓
Study Progress = completed studying
    ↓
Current Learning advances (Learning Mode)
    ↓
Estimated Knowledge / Mastery unchanged
    (no authorised Evidence → correct silence)
```

### 3.3 Evidence-bearing attempt path

```
Mission (study commitment)
    ↓
Study Attempt (questions attempted / correct)
    ↓
Educational Observation (attempt retained)
    ↓
Authorised Educational Evidence (Structured Question Results)
    ↓
Twin estimate path
    ↓
Estimated Knowledge / Estimated Mastery may update
    ↓
Readiness / Recommendation factors may revise
    (Study Progress unchanged by score alone)
```

### 3.4 Guidance consumption (no reverse authorship)

```
Educational States (coverage + estimates + plan context)
    ↓
Readiness (derived posture)
    ↓
Recommendation (advice)
    ↓
Student choice
    ↓
Preference / Decision Journal (not Evidence of understanding)

Mission under Learning Mode remains owned by Planning / Current Learning,
not by Recommendation acceptance.
```

---

## 4. Deletion Rules

### 4.1 Constitutional posture

> **Educational history belongs to the learner, not the Study Plan.**

A Study Plan is a planning container and Learning Mode context. It is not the ontological owner of rightful Study Progress, Attempts, Observations, or Evidence.

### 4.2 What may disappear

| Artefact | May disappear / expire when | Conditions |
|----------|----------------------------|------------|
| **Recommendation artefacts** | Superseded, expired, or dismissed | Preference history optional; never erase Evidence/Study Progress as a side-effect |
| **Current Learning pointer** | Active study context ends | Coverage and Evidence remain |
| **Active Mission lifecycle status** | Day ends; mission completed/abandoned/superseded | Historical reconstructability of attempts preserved |
| **Derived Readiness snapshots** | Recalculated away | Inputs remain; thin-input silence restores “not yet estimable” |
| **Provisional Estimates** | Superseded by newer Evidence-driven Estimates | Supporting Evidence history retained |
| **Study Progress (coverage)** | Only under **explicit student-authorised educational reset** with clear consequence language | Never silent plan-delete side-effect |
| **Soft Observations** (confidence, reflection) | Privacy / user-clear policies when educationally defined | Must not masquerade as wiping mastery guilt |

### 4.3 What must never disappear (educational integrity)

| Artefact | Why |
|----------|-----|
| **Lawful Educational Evidence** | Understanding claims require retained observational warrant |
| **Study Attempts that produced Evidence** | Attempt history grounds estimate honesty |
| **Rightful Study Progress** across ordinary plan delete/archive | Continuity of “what I completed studying” (Constitution II §1.8; EL-001 gap) |
| **Attribution binding** (student + syllabus unit identity) | Orphaned scores without topic identity are educationally useless |
| **Explainability warrant for past advice** (where Decision Journal exists) | Trust requires reconstructable Why, without treating advice as Evidence |

### 4.4 Forbidden deletion patterns

1. **Plan delete cascading wipe of TopicProgress coverage** without student-authorised reset disclosure.  
2. **Wiping Attempts/Evidence to “fix” Estimated Mastery** or reverse an unwelcome score.  
3. **Deleting Evidence because Recommendations changed.**  
4. **Clearing Current Learning and calling it a Study Progress reset.**  
5. **Account convenience shortcuts that redefine mastery by omission of history.**

### 4.5 Privacy and account erasure

Legal privacy / full account deletion may remove educational history. That regime is outside educational coaching convenience. When executed, the product must not pretend remaining empty estimates are “mastered” cold-start theatre — absence remains uncertainty.

---

## 5. Educational Continuity

### 5.1 Across Study Plan deletion

| State | Continuity rule |
|-------|-----------------|
| **Study Progress** | Preserve per learner + syllabus unit unless student explicitly authorises coverage reset. |
| **Study Attempt / Observation / Evidence** | Preserve as learner history. |
| **Estimated Knowledge / Mastery** | Preserve estimate posture; do not invent zeros by deleting backing history. |
| **Current Learning / Mission** | May clear or require new active plan; regenerating Learning Mode context must resynchronise from preserved Study Progress + syllabus. |
| **Recommendation / Readiness** | Recompute from preserved inputs after a new plan is active. |

**Implemented under EIP-005 / `EDUCATIONAL_CONTINUITY_STANDARD.md`:** ordinary Study Plan hard-delete no longer erases curriculum-linked Study Progress. Planning metadata and week schedules remain disposable; mission plan pointers detach without destroying Mission / Attempt history.

### 5.2 Across Curriculum migration (V1 ↔ V2 / syllabus version change)

| Principle | Rule |
|-----------|------|
| **Identity mapping** | Continuity requires lawful mapping of syllabus unit identity (topic codes / structural equivalents). Unmapped units remain honest unknowns — do not fabricate coverage or mastery. |
| **Coverage** | Study Progress follows mapped unit identity; unmapped prior coverage is retained as historical or legacy where design allows, never silently relabelled as mastery. |
| **Evidence** | Evidence remains attributable; remapping attaches observations to new unit ids without rewriting outcomes. |
| **Estimates** | After remap, Twin estimates may recompute from remapped Evidence; until then prefer silence over invented confidence. |
| **Traversal** | Both flat (V1) and structured (V2) curricula remain loadable; lifecycle rules must not break either. |

### 5.3 Across Future Revision Mode

Revision Mode (FEL-001) consolidates previously studied material when **activated and disclosed**. Continuity principles:

1. **Study Progress meaning unchanged** — revision does not redefine coverage as mastery.  
2. **Current Learning may lawfully redirect** only under mode authority; Learning Mode ownership rules are amended by constitutional mode activation, not by silent recommendation.  
3. **Evidence and Estimates continue to accumulate** from revision Attempts the same way — Observation → authorised Evidence → Twin updates.  
4. **Prior Learning Mode history remains** — mode switch must not erase evidence of first-pass learning.  
5. **Student-facing language** must mark revision as revision when focus is not first-pass Current Learning Topic work.

Until Revision Mode is authorised in Constitution / Registry behaviour, Version 1 Learning Mode continuity rules remain sole mission focus authority.

---

## 6. Knowledge vs Mastery Relationship

### 6.1 Conceptual distinction (documentation only)

This section documents constitutional meaning. It does **not** redesign Twin implementation, scoring mathematics, or product storage.

| Concept | Educational question | Temporal posture | Evidence demand | Student language |
|---------|----------------------|------------------|-----------------|------------------|
| **Estimated Knowledge** | How well do I **currently understand** this? | Near-term understanding posture | Evidence of recent/credible performance may move it; still provisional | “Estimated knowledge…”, “how well you seem to understand…” |
| **Estimated Mastery** | How confidently is this treated as **mastered** for long-horizon preparation? | Longer-horizon confidence / consolidation | Requires accumulation and higher warrant; one attempt is not mastery theatre | “Estimated mastery…”, never checkbox “Mastered” as Study Progress |

Both are:

- Twin-owned (or authorised estimation paths serving Twin meaning);
- Evidence-driven only;
- Estimates, never certified exam results;
- Forbidden writers: Study Progress, Completion alone, Confidence alone, Recommendations.

### 6.2 Relationship

```
Educational Evidence (accumulated)
         │
         ├──────────────► Estimated Knowledge
         │                  (current understanding estimate)
         │
         └──────────────► Estimated Mastery
                            (longer-horizon mastery estimate;
                             typically stricter / denser warrant)
```

Knowledge and Mastery are **sibling interpretations** of Evidence history, not a pipeline where Study Progress creates Knowledge and Knowledge creates Mastery by fiat.

- Raising Estimated Mastery never writes Study Progress.  
- Completing Study Progress never writes Estimated Mastery.  
- Product may currently present related or shared scalars; constitutionally the **meanings** remain distinct even if storage is co-located (documented debt — not redesign here).

### 6.3 Cold start

No Evidence ⇒ no lawful strong Knowledge or Mastery speech. Coverage may still narrate Study Progress honestly.

---

## 7. Version 1 Boundaries

### 7.1 What Version 1 implements (educational lifecycle scope)

| Area | Version 1 posture |
|------|-------------------|
| **Lifecycle philosophy** | Activity → Observation → Evidence → State Updates → Guidance as binding educational chain |
| **Coverage spine** | Study Progress + Current Learning + Learning Mode Mission authority |
| **Understanding spine** | Study Attempt structured question results as interim authorised Evidence pathway; Twin estimate writes only when authorised |
| **Ownership** | EIP-001 State Authority Matrix for listed states |
| **Evidence meaning** | Evidence Model + Evidence Authority catalogues |
| **Explainability** | EIP-003 student-facing What / Why / Next and claim typing |
| **Guidance** | Recommendations advisory; must not retarget Learning Mode Mission |
| **Readiness** | Preparedness narration consuming lawful factors; not next-action authority |
| **Continuity target** | Educational history belongs to the learner; Study Plan hard-delete preserves Study Progress / Attempts / estimate posture (EIP-005) |
| **Continuity productisation** | Confirm UX and remapping by official topic code; informed educational reset reserved for explicit student authorisation |

### 7.2 What Version 1 does **not** claim complete

| Gap / deferral | Notes |
|----------------|-------|
| Explicit student-authorised educational reset product flow | Continuity default is preserve; reset-with-consequence UX may follow |
| Full authorised Evidence catalogue live (quiz, mock, mission assessment, official exam) | Reserved pathways remain silent |
| Dual Twin / separated Knowledge vs Mastery stores | Conceptual distinction mandatory; physical separation optional later |
| Revision / Diagnostic / Adaptive Mode lifecycle | Future evolution; Mode activation required for mission focus redirection |
| Numerical Evidence decay half-lives | Named rules only when specialised architecture authorises them |
| Educational Intelligence redesign | Out of scope |
| Admin-governed curriculum edition remap tables | Objective topic-code remap ships in EIP-005; richer edition maps may follow |

### 7.3 What Version 2 may extend

| Extension | Intent |
|-----------|--------|
| **Continuity productisation** | Preserve Study Progress and educational history across plan archive/delete/rebuild by default |
| **Expanded Evidence sources** | Quiz, mock, mission assessment, official exam results under Evidence Authority |
| **Clearer Knowledge vs Mastery persistence** | Separate stores/stages without changing constitutional meanings |
| **Revision Mode lifecycle** | Disclosed mode switch; revision Missions; retain first-pass history |
| **Curriculum migration tooling** | Explicit unit remaps for V1↔V2 and syllabus editions |
| **Specialised Readiness logic** | Single student-facing definition under Registry FEL-004 |
| **Observation retention policies** | Privacy-aligned, educationally named soft-signal retention |
| **Decision Journal completeness** | Accept/Dismiss as preference history with reconstructable Why |

Version 2 extensions amend specialised architecture and Registry behaviour as needed; they must not contradict the Constitution without Article X amendment.

---

## 8. Cross References

| Document | Role |
|----------|------|
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational state meanings (Article IV); Evidence (Article V); continuity belief (II §1.8) |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-001–EL-012 operational behaviour |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Owner / Authority / Permitted Writers |
| `EDUCATIONAL_EVIDENCE_MODEL.md` | What Evidence is; Activity ≠ Evidence ≠ Inference ≠ Knowledge |
| `EDUCATIONAL_EVIDENCE_AUTHORITY.md` | Version 1 authorised Evidence gate |
| `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | Guidance narration; claim types |
| `EDUCATIONAL_CONTINUITY_STANDARD.md` | Operational continuity / deletion / migration contract (EIP-005) |
| `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | Programme sequencing toward Version 1 readiness |

---

## Closing

This Architecture is the lifecycle reference for Educational Integrity work that touches state succession, deletion, and continuity.

If implementation would erase rightful learner educational history because a Study Plan container disappeared, the implementation is educationally unlawful under this Architecture — even if the database cascade is convenient.

EIP-005 implements §5 Educational Continuity for ordinary Study Plan deletion and objective topic-code curriculum remapping. Architecture Review remains the gate before EIP-006.
