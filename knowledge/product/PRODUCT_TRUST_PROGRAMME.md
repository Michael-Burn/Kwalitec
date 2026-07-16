# Product Trust Programme

**Capability ID:** PTP-000  
**Programme:** Product Trust Programme  
**Programme ID:** PTP-000  
**Title:** Product Trust Programme Blueprint  
**Priority:** P0  
**Status:** APPROVED — awaiting Architecture Review before capability implementation  
**Version:** 1.0  
**Date:** 2026-07-15  
**Nature:** Governance only — documentation; no application code  
**Classification:** Product programme — subordinate to Educational Constitution and Educational Logic Registry; complementary to Educational Integrity Programme and Learning Experience Programme  

---

## Authority

This Blueprint is the master roadmap for **product trust** work leading into Version 1 polish and Blind Internal Alpha Review Version 3.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001) — highest educational authority  
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002) — operational educational behaviour  
3. Educational Integrity Programme outcomes (EIP) — educational meaning, evidence, and state already governed  
4. Learning Experience Programme outcomes (LXP) — daily learning loop already productised  

**Product evidence (not architecture):**

- `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` — student judgement that remaining hesitation is product maturity and trust, not missing educational integrity or a broken learning loop  

This document:

- defines **programme vision, principles, capability roadmap, and success criteria** for Product Trust;
- does **not** redesign Educational Constitution, Educational Logic Registry, Evidence Authority, Digital Twin, Educational Intelligence, Learning Mode, recommendation algorithms, readiness algorithms, question banks, Adaptive Learning, or Revision Mode;
- does **not** implement application code;
- does **not** reopen closed EIP or LXP Sprint 1 educational purposes.

**The Product Trust Programme governs PTP capability design and implementation.  
Implementation never invents trust behaviour that contradicts higher educational authorities.**

---

## Table of Contents

1. [Programme Vision](#1-programme-vision)  
2. [Why This Programme Exists](#2-why-this-programme-exists)  
3. [Programme Purpose](#3-programme-purpose)  
4. [Programme Principles](#4-programme-principles)  
5. [Capability Roadmap](#5-capability-roadmap)  
6. [Dependency Graph](#6-dependency-graph)  
7. [Success Criteria](#7-success-criteria)  
8. [Relationship to Existing Programmes](#8-relationship-to-existing-programmes)  
9. [Out of Scope](#9-out-of-scope)  
10. [Governance](#10-governance)  
11. [Cross References](#11-cross-references)  

---

## 1. Programme Vision

Educational meaning is already governed.  
The daily learning loop is already complete.

What remains between Kwalitec and a student’s full reliance is not another educational model and not another learning-loop step. It is whether the product feels **clear, consistent, predictable, transparent, and reliable** enough to be the primary study companion for an expensive professional exam.

The Product Trust Programme exists so that Blind Internal Alpha Review Version 3 can conclude:

> “I trust Kwalitec enough to depend on it throughout my exam preparation.”

Every capability in this Programme removes one concrete reason a serious student still hesitates after Educational Integrity and Learning Experience Sprint 1 are complete.

---

## 2. Why This Programme Exists

### 2.1 Prior programme status

| Programme | Status | What it closed |
|-----------|--------|----------------|
| Educational Integrity Programme (EIP) | **COMPLETE** | Educational state ownership, evidence authority, explainability, continuity, Version 1 educational state refinement |
| Learning Experience Programme Sprint 1 (LXP) | **COMPLETE** | Study Session → Practice Outcome Capture → Study Session Feedback daily loop |

### 2.2 Blind Internal Alpha Review v2 outcome

Review v2 scored the product **57 / 100** (up from **34 / 100**). Educational Trust rose. The daily loop is now a real coach sequence. Analytics can populate through normal use. Feedback refuses to overclaim.

The reviewer’s residual judgment is product trust, not educational emptiness:

- Hollow-subject trap — unsupported examinations produce beautiful empty plans with no warning  
- Two “how did it go?” paths — Practice Outcome Capture and Reflect on Your Learning coexist  
- Self-reported practice is unverified but read as objective — honesty about limits is incomplete  
- Multiple coverage percentages on the Dashboard — coherent enough not to look broken, still too many stories  
- Version / terminology / microcopy polish — small signals that undermine a trust brand  

### 2.3 The remaining problem class

```
Educational Integrity     →  meaning is lawful
Learning Experience       →  daily loop works and closes honestly
Product Trust (this)      →  maturity, clarity, consistency, transparency, reliability
```

EIP prevented unlawful claims.  
LXP made the learning day real.  
PTP removes the remaining reasons a student still withholds full dependence.

---

## 3. Programme Purpose

The Product Trust Programme exists to remove every remaining reason a student hesitates to trust Kwalitec as their **primary study companion**.

Focus areas:

| Focus | Student meaning |
|-------|-----------------|
| **Clarity** | One obvious path; numbers that mean one thing |
| **Consistency** | Same examination, same behaviour; same terms everywhere |
| **Predictability** | Supported vs unsupported is known before investment of time |
| **Transparency** | Limits of evidence and product capability are stated, never hidden |
| **Product reliability** | Version, wording, and small surfaces do not contradict the trust pitch |

This Programme does not invent new educational philosophy. It does not reopen the understanding spine. It makes the already-honest product **dependable to live with**.

---

## 4. Programme Principles

Every capability in this Programme obeys the following principles.

### P-1 — Never create false confidence

The product must not imply support, certainty, readiness, or completeness that the product cannot deliver. A supported-looking unsupported plan is a trust violation.

### P-2 — Never hide product limitations

Known limits — including which examinations are fully supported, and what practice evidence can and cannot prove — must be visible at the moment they matter, not buried in footnotes after harm.

### P-3 — Always explain unsupported behaviour

If a behaviour cannot be offered, or can only be offered partially, the product explains *what* is unsupported and *what the student should do instead*. Silence that produces hollow shells is forbidden.

### P-4 — Every workflow has one obvious path

For each student job (especially “record how practice went” and “complete today’s study”), there is one primary path. Parallel legacy paths that invite double entry or ambiguity are Programme debt until reconciled.

### P-5 — Every dashboard number must tell one coherent story

Coverage, progress, and related metrics may use distinct technical meanings internally, but the student-facing Dashboard must present one understandable narrative — not a cluster of unexplained sibling percentages.

### P-6 — Every supported examination behaves consistently

Within the supported set, examination experience must be predictable. Outside the supported set, the product must refuse, gate, or clearly label — never silently degrade into an empty shell that looks finished.

### P-7 — Release polish builds educational trust

Version strings, terminology, and microcopy are not cosmetics when the brand promise is trust. Inconsistency at the surface undoes integrity earned at the core.

---

## 5. Capability Roadmap

Implementation sequence for Version 1 Product Trust. Later capabilities may benefit from earlier closures; blocking dependencies are stated per capability.

---

### Capability 1 — PTP-001 Supported Subject Integrity

**Purpose**  
Prevent unsupported examinations from creating misleading study plans.

**Product trust problem addressed**  
Blind Review v2 “hollow-subject trap”: a student can build a full plan for a paper that yields no real curriculum, with no warning.

**In scope**  
- Definition of Version 1 supported examinations (product surface, not new curriculum engines)  
- Gating, clear labelling, or refusal paths before hollow-plan creation  
- Student-facing explanation when a selection is unsupported or limited  

**Expected outcome**  
A student cannot invest onboarding and planning time in an unsupported examination without knowing. Supported examinations remain the only path to a complete Version 1 planning experience.

**Blind Review v2 mapping**  
Remaining Release Blocker 1 (mandatory before general release).

**Dependency**  
None within this Programme. Prerequisite: EIP and LXP Sprint 1 remain complete and governing for educational claims.

---

### Capability 2 — PTP-002 Single Daily Workflow

**Purpose**  
Remove duplicated study-completion and reflection paths.

**Status**  
Implemented — awaiting Architecture Review (`PTP-002_SINGLE_SOURCE_OF_TRUTH.md`).

**Product trust problem addressed**  
Practice Outcome Capture coexists with the older “Reflect on Your Learning” review (confidence + mistakes), creating ambiguity and possible double entry.

**In scope**  
- One obvious “record how it went / close the day” path  
- Reconciliation or retirement of parallel completion/reflection surfaces  
- Preservation of LXP Sprint 1 educational closure honesty (no reinvention of evidence rules)  

**Expected outcome**  
After finishing a Study Session, the student meets one clear next step. There is no competing “how did it go?” ritual that confuses what data was recorded.

**Blind Review v2 mapping**  
Remaining Release Blocker 2 (mandatory before general release).

**Dependency**  
Should follow or respect PTP-001 supported-subject clarity where workflow messaging mentions examination support. Does not reopen LXP educational purpose — it consolidates the product path around the already-approved loop.

---

### Capability 3 — PTP-003 Evidence Transparency / Honest Product Communication

**Purpose**  
Explain the limits of self-reported practice honestly; label every estimated,
unavailable, and empty educational claim so students do not invent certainty.

**Status**  
Implemented — awaiting Architecture Review (`PRODUCT_COMMUNICATION_STANDARD.md`).

**Product trust problem addressed**  
Practice counts are unverified but can be read as objective; self-reported-only evidence caps trust in Estimated Knowledge / readiness unless the product states that ceiling openly. Empty analytics and unexplained estimate badges create residual hesitation.

**In scope**  
- Student-facing disclosure of self-report limits on relevant surfaces (feedback, analytics, readiness-adjacent narration)  
- Clear separation of what was recorded vs what can be concluded  
- No claim that unverified self-report equals observed in-app performance  

**Expected outcome**  
A serious student knows that Kwalitec’s understanding picture depends on the faithfulness of practice they log, unless and until stronger evidence sources exist. Transparency is mandatory; inventing verification content is out of scope for this Programme.

**Blind Review v2 mapping**  
Remaining Release Blocker 3 (strongly recommended for Version 1 trust).

**Dependency**  
Builds on EIP evidence authority and LXP feedback honesty. Does **not** redesign Evidence Authority, question banks, or Adaptive Learning. Does **not** invent in-app practice content as a PTP deliverable.

---

### Capability 4 — PTP-004 Dashboard Clarity / Information Architecture

**Purpose**  
Simplify educational metrics into one understandable narrative ordered around student decisions.

**Status**  
Implemented — awaiting Architecture Review (`PTP-004_INFORMATION_ARCHITECTURE.md`).

**Product trust problem addressed**  
Two-to-three related coverage percentages (“Syllabus coverage”, “Curriculum Coverage”, “Weighted Coverage”) remain without a student-facing explanation of difference — no longer contradictory, still more numbers than needed. Dashboard overload and competing educational messages obscure what to study next.

**In scope**  
- Student-facing Dashboard information architecture (not a visual redesign)  
- Decision hierarchy: Today's Study Session → Progress → Estimated Knowledge → Attention → Secondary  
- One authoritative syllabus-coverage / progress story for Version 1  
- Removal of competing coverage percentages and non-actionable duplicates  

**Expected outcome**  
Within ~10 seconds a student can answer: what to study, whether they are on track, and whether anything needs attention. Internal technical distinctions may remain for engineering; they must not compete for student attention.

**Blind Review v2 mapping**  
Remaining Release Blocker 4.

**Dependency**  
Benefits from PTP-003 so that metric honesty and evidence limits do not conflict. Does not redesign readiness or recommendation algorithms. Preserves Educational Constitution, Logic Registry, LXP, Evidence Authority, and Product Communication Standard.

---

### Capability 5 — PTP-005 Release Polish

**Purpose**  
Version consistency, terminology, microcopy, and small trust signals.

**Product trust problem addressed**  
Settings vs footer version disagreement; repetitive disclaimer fatigue; terminology drift that undermines a trust brand.

**In scope**  
- Single coherent Version 1 version presentation  
- Terminology alignment across Mission, Dashboard, Settings, and footers  
- Microcopy trim / unification that preserves educational truth without disclaimer overload  
- Other small, documented trust signals required for Version 1 polish  

**Expected outcome**  
Surface polish stops inventing doubt. Educational honesty remains; repetitive lecture tone is reduced where lawful under Constitution messaging rules.

**Blind Review v2 mapping**  
Remaining Release Blocker 5.

**Dependency**  
Best executed after PTP-001–PTP-004 define supported subjects, single workflow, evidence speech, and dashboard narrative — so polish does not cement wording around paths that will change.

---

## 6. Dependency Graph

```
PTP-001 Supported Subject Integrity
              ↓
PTP-002 Single Daily Workflow
              ↓
PTP-003 Evidence Transparency
              ↓
PTP-004 Dashboard Clarity
              ↓
PTP-005 Release Polish
```

### Dependency rules

1. **PTP-001 first** — unsupported examinations must not continue to mint misleading plans while other trust work proceeds as if the product is globally safe.  
2. **PTP-002 next** — one daily closure path before further speech and metric polish.  
3. **PTP-003 before / with metric narration** — evidence limits must be stated before dashboard story claims can be fully trusted.  
4. **PTP-004 after evidence speech is designed** — coverage narrative must not invent certainty the evidence model denies.  
5. **PTP-005 last** — polish locks terminology around the reconciled product, not around duplicate workflows or unsupported shells.

Parallel design exploration is allowed; completion claims and release-blocker closure follow this order unless Architecture Review explicitly authorises reordering with documented risk.

---

## 7. Success Criteria

### 7.1 Programme success

The Programme succeeds when **Blind Internal Alpha Review Version 3** would conclude:

> “I trust Kwalitec enough to depend on it throughout my exam preparation.”

That sentence is the student-facing north star. Supporting signals:

| Signal | Threshold |
|--------|-----------|
| Hollow-subject trap | Unsupported examinations cannot create misleading “complete” plans without clear gate or label |
| Daily workflow | One obvious study-completion / practice-capture path; no competing reflection ritual |
| Evidence honesty | Self-report limits are visible where Estimated Knowledge / readiness adjacent claims appear |
| Dashboard | Coverage / progress reads as one coherent story to a non-engineer |
| Release polish | Version, terminology, and primary microcopy do not contradict each other |
| Blind Review v3 | Product trust verdict supports dependence as primary study companion for supported examinations |

### 7.2 What success is not

Success is **not**:

- In-app question banks or ActEd replacement content  
- Verified remote proctoring of practice performance  
- Redesign of Educational Intelligence, Digital Twin, Adaptive Learning, or Revision Mode  
- Claiming readiness oracle behaviour beyond what lawful evidence can support  

Version 1 Product Trust success is **dependence on an honest, consistent, supported planner and practice tracker** — not a promise the educational cores do not authorise.

---

## 8. Relationship to Existing Programmes

### 8.1 Educational Integrity Programme (EIP)

| EIP | Product Trust |
|-----|---------------|
| Governs **educational meaning**, ownership, evidence lawfulness, explainability | Governs **product maturity** around that meaning |
| COMPLETE | Starts after EIP COMPLETE |
| Prevents false educational claims | Prevents false **product** confidence (support, workflow, polish, metric presentation) |

PTP must not weaken EIP outcomes. Transparency about self-report (PTP-003) must remain constitutionally lawful under existing Evidence Authority — it discloses limits; it does not invent new evidence ranks.

### 8.2 Learning Experience Programme (LXP)

| LXP | Product Trust |
|-----|---------------|
| Built the Study Session → Practice Outcome → Feedback **loop** | Makes that loop the **only** obvious daily path and polishes trust around it |
| Sprint 1 COMPLETE | PTP-002 consolidates product paths; PTP-003/005 reinforce honest speech |

PTP must not redesign LXP educational closure. It reconciles product duplication and clarifies presentation.

### 8.3 Release roadmap

| Release concern | PTP role |
|-----------------|----------|
| Version 1 conditional GO (Blind Review v2) | PTP-001 and PTP-002 are mandatory release blockers; PTP-003–PTP-005 strongly recommended |
| Marketing / positioning | Must remain “adaptive study planner and honest practice tracker” for supported subjects — not readiness oracle |
| Blind Internal Alpha Review v3 | Primary external success test for this Programme |
| Engineering stabilisation / RC validation | May consume PTP outcomes; PTP does not replace release engineering certification |

### 8.4 Authority stack (product trust layer)

```
Educational Constitution / Logic Registry
        ↓
Educational Integrity Programme (COMPLETE)
        ↓
Learning Experience Programme Sprint 1 (COMPLETE)
        ↓
Product Trust Programme (THIS BLUEPRINT)
        ↓
PTP-001 … PTP-005 capability briefs
        ↓
Application implementation (future; not this document)
```

---

## 9. Out of Scope

This Programme intentionally does **not** redesign or open:

- Educational Constitution  
- Educational Logic Registry  
- Evidence Authority  
- Digital Twin  
- Educational Intelligence  
- Learning Mode (authority model)  
- Recommendation algorithms  
- Readiness algorithms  
- Question banks / in-app study content  
- Adaptive Learning product surfaces  
- Revision Mode  

Work that requires the above must be scoped as a different programme or constitutional amendment — not smuggled into PTP polish.

---

## 10. Governance

### 10.1 Document nature

This Blueprint is **documentation only**. PTP-000 creates no application change.

### 10.2 Capability briefs

Each of PTP-001–PTP-005 requires its own design / architecture brief before implementation, approved under Architecture Review.

### 10.3 Educational non-regression

Any PTP implementation must preserve:

- Educational state ownership  
- Evidence authority rules  
- Explainability honesty (including LXP feedback structure)  
- Learning Mode mission authority  

### 10.4 Exit

The Programme exits when:

1. PTP-001–PTP-005 are designed, implemented, and regression-protected as agreed in their briefs; and  
2. Blind Review Version 3 (or equivalent Architecture-approved trust evaluation) supports the success sentence in §7.1; and  
3. Residual product trust debt, if any, is intentional, owned, and documented.

---

## 11. Cross References

| Document | Relationship |
|----------|--------------|
| `BLIND_INTERNAL_ALPHA_REVIEW_V2.md` | Diagnostic product evidence for PTP problem set |
| `knowledge/educational/EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | Prior programme — educational meaning COMPLETE |
| `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md` | Prior programme — daily loop COMPLETE (Sprint 1) |
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Higher educational authority |
| `knowledge/educational/EDUCATIONAL_LOGIC_REGISTRY.md` | Higher operational educational authority |
| `knowledge/educational/EDUCATIONAL_EVIDENCE_AUTHORITY.md` | Evidence limits PTP-003 must disclose, not rewrite |
| `knowledge/release/VERSION1_RELEASE_CANDIDATE.md` | Release context for polish and gating |
| `knowledge/release/RELEASE_CANDIDATE_VALIDATION_PLAN.md` | Validation context; PTP does not replace it |

---

**End of Product Trust Programme Blueprint (PTP-000).**  
**Stop. Return for Architecture Review.**
