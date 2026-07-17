# Kwalitec Design Principles

**Programme:** Architecture Governance  
**Milestone:** ARCH-001  
**Status:** Governing — product design philosophy  
**Nature:** Architecture only — technology-agnostic; no application specification  
**Date:** 2026-07-17  

---

## 1. Purpose

This document states the enduring design principles that govern Kwalitec product decisions.

It is the first document to consult before proposing a new feature, architectural change, or significant interface redesign. Every future capability should be evaluable against these principles without reading application code, choosing a framework, or knowing the current stack.

These principles are intended to remain valid if Kwalitec is rewritten in another technology five years from now.

This document **governs** specialised architecture programmes and blueprints. It does **not** replace them.

---

## 2. Philosophy

Kwalitec exists to help candidates for demanding professional examinations study with clarity, honesty, and continuity.

Its central product promise is:

> **Reduce decisions. Increase learning.**

Students should spend less time asking what to study and more time studying the right thing. Founders and operators should spend less time reconciling dashboards and more time acting on trustworthy operational signals.

Kwalitec is therefore designed as:

- an educational coach grounded in official syllabus structure;
- a decision-support system driven by observable learning evidence;
- an operator console for product health that never invents educational truth.

Kwalitec is not a generic planner, engagement engine, or opaque tutor. Visual polish, novelty, and automation are subordinate to educational integrity and user trust.

---

## 3. Design Principles

### DP-001 — One Source of Truth

Every piece of operational or educational information must have one authoritative source.

Do not duplicate the same fact across competing stores, dashboards, or metric definitions. When two surfaces answer the same question, they must share the same authority — or one of them must stop claiming to answer it.

Conflicting metrics are a design failure, not a presentation preference.

---

### DP-002 — One Entry Point

Each user persona should have one primary home.

Examples:

| Persona | Primary home |
|---|---|
| Student | Student Dashboard |
| Founder / operator | Founder Command Centre |

Navigation must not force users to choose between equivalent “homes.” Secondary destinations may exist for deep work, but the primary entry point must be unambiguous.

---

### DP-003 — Workflow Before Data

Users complete workflows. They do not navigate database tables.

Navigation, labels, and page hierarchy should reflect tasks and decisions — “What should I study?”, “What needs action?” — rather than internal entities, programme codes, or storage shapes.

If a screen only makes sense after knowing the schema, the design has leaked implementation into the product.

---

### DP-004 — Educational Integrity

Operational tools must never alter educational evidence.

Learning evidence must remain trustworthy. Educational progress, mastery estimates, readiness judgements, and related educational state may change only through authorised educational workflows.

Founder, research, analytics, and administrative surfaces may observe educational systems. They must not rewrite educational truth for convenience, demonstration, or operational completeness.

---

### DP-005 — Explainability

Every recommendation, progress value, readiness estimate, and material metric should be explainable.

Users should be able to understand why Kwalitec reached a conclusion — in plain language, from identifiable inputs, not from opaque scores or unexplained automation.

If a result cannot be explained, it is not ready to be shown as guidance.

---

### DP-006 — Progressive Disclosure

Show users only what they need for the current task.

The first screen of a workflow should answer the most important question first. Advanced detail, secondary metrics, and expert controls may remain available without crowding the primary path.

Density is not richness. Clarity is.

---

### DP-007 — Consistency

Every page should answer:

1. Where am I?  
2. What am I looking at?  
3. What should I do next?

Navigation patterns, terminology, hierarchy, and layout behaviour should remain consistent across the product. The same concept must not wear different names on different screens. The same action must not live behind different rituals without cause.

---

### DP-008 — Trust

Kwalitec should never knowingly display stale, contradictory, or misleading information.

Trust is more important than visual polish. Prefer honest emptiness, explicit unavailability, or restrained language over fabricated zeros, confident theatre, or metrics that look live when they are not.

When honesty and optimisation conflict, choose honesty.

---

### DP-009 — Evidence Before Opinion

Educational recommendations and claims about learning should rest on observable evidence wherever possible.

Prefer measured learning signals, authorised educational evidence, and curriculum structure over assumptions, engagement heuristics, or ungrounded narrative.

Inference may interpret evidence. Inference must not invent evidence. Absence of evidence is not proof of mastery, readiness, or weakness stated as fact.

---

### DP-010 — Human-Centred Intelligence

Artificial intelligence and automated reasoning should help students and founders make better decisions.

They should augment judgement, not replace it. Intelligence may advise; it must not silently commandeer the user’s authorised path or obscure accountability for the recommendation.

The human remains the decision-maker. The system remains the explainable adviser.

---

### DP-011 — Curriculum Primacy

Official syllabus structure is the educational spine of the product.

Planning, progress narration, missions, recommendations, and readiness judgements must remain accountable to that spine. Features may personalise *how* and *when* a student works through the syllabus; they must not quietly substitute a private taxonomy for the examining body’s curriculum.

---

### DP-012 — Deterministic Educational Cores

Core educational judgements that shape the student’s journey must be reproducible from the same educational inputs.

Given the same curriculum, evidence, plan constraints, and authorised state, the platform should reach the same material conclusions. Randomness, opaque generative substitution, and non-reproducible “magic” are forbidden in those cores.

Assistive intelligence may exist around the edges. The educational centre must remain accountable and repeatable.

---

### DP-013 — Continuity of Learning History

Educational history belongs to the learner.

Disposable planning containers may change. Rightful study progress, attempts, authorised evidence posture, and lawful estimates must not be silently erased, invented, or reset without clear educational justification.

Continuity preserves trust across plan changes, migrations, and product evolution.

---

## 4. Applying the Principles

Use these principles as constraints, not slogans.

| Situation | Apply especially |
|---|---|
| New dashboard or home surface | DP-001, DP-002, DP-006, DP-007 |
| New student journey or daily loop | DP-003, DP-004, DP-009, DP-011 |
| New recommendation or readiness signal | DP-005, DP-009, DP-010, DP-012 |
| Founder / research / ops tooling | DP-001, DP-002, DP-003, DP-004, DP-008 |
| Metric, copy, or empty-state design | DP-008, DP-007 |
| Plan lifecycle or migration | DP-004, DP-013 |
| Cross-cutting product bets | All principles; Product Blueprint alignment |

When principles appear to conflict, prefer this order of deference:

1. Educational integrity and lawful evidence (DP-004, DP-009)  
2. Trust and honesty (DP-008)  
3. Curriculum accountability and determinism (DP-011, DP-012)  
4. Clarity of entry, workflow, and disclosure (DP-002, DP-003, DP-006, DP-007)  
5. Assistive intelligence (DP-010)  

No principle authorises violating the Educational Constitution.

---

## 5. Relationship to Other Architecture Documents

This document is the **governing product-design philosophy**. Specialised documents remain authoritative within their domains. They must comply with these principles; these principles do not rewrite their detailed rules.

| Document / programme | Role | Relationship to Design Principles |
|---|---|---|
| **Product Blueprint** | Long-term vision, mission, and strategic product direction | Strategy. Design Principles operationalise how blueprint intent is judged in concrete product and UX decisions. |
| **Educational Constitution** | Highest educational authority — meaning, truth, ownership, integrity | Educational law. Design Principles amplify constitutional obligations into product-wide design constraints; they never override the Constitution. |
| **Educational Workflow Review (EWR)** | Review and authority over how educational journeys are structured | Workflow law for learning journeys. Design Principles require workflow-first navigation and a single authoritative path per educational event. |
| **Product Operations Programme (POP)** | Operator workflows, Internal Alpha operations, founder operating surfaces | Operational programme. Design Principles govern POP information architecture: one truth, one entry, workflows over entities, educational boundary. |
| **Founder Information Architecture** | Founder Command Centre structure and navigation | Applied IA. Must instantiate DP-001–DP-003, DP-004, DP-006–DP-008 for the founder persona. |
| **Curriculum Intelligence Programme** | Official syllabus as source of educational structure | Curriculum authority. Design Principles require curriculum primacy and forbid silent substitution of unofficial taxonomies. |
| **Research Intelligence Programme** | Product-experience research loop | Observational programme. Bound by educational integrity: research may observe product experience; it must not write educational evidence or twin state. |
| **Student Digital Twin documentation** | Model of the learner’s educational state | Inference layer. Bound by evidence-before-opinion, explainability, determinism, and continuity. |
| **Release protocols** | What may ship and under what freeze / validation rules | Release governance. Design Principles inform whether a candidate preserves trust, integrity, and clarity — they do not replace release checklists. |

**Summary:** Design Principles sit above programme blueprints as shared philosophy. Constitutions, evidence authorities, workflow reviews, and programme specifications remain the detailed law of their domains.

---

## 6. Decision-Making Framework

Before accepting a proposal, answer the following. A single “No” is a warning. Multiple “No” answers mean the design should be reconsidered.

1. **Truth** — Does this introduce a second source of truth for the same fact or metric?  
2. **Entry** — Does each affected persona still have one clear primary home?  
3. **Workflow** — Does navigation reflect a user task, or an internal data shape?  
4. **Integrity** — Does this preserve educational integrity? Can non-educational tools still write educational evidence?  
5. **Explainability** — Are recommendations and material metrics more explainable, or less?  
6. **Load** — Does this increase or reduce cognitive load for the primary task?  
7. **Trust** — Would a careful user still trust what they see if they knew how it was produced?  
8. **Evidence** — Are claims grounded in observable evidence (or honestly labelled as estimates / unavailable)?  
9. **Judgement** — Does intelligence assist the user’s decision, or quietly replace it?  
10. **Curriculum** — Does the design remain accountable to official syllabus structure?  
11. **Reproducibility** — Would the same educational inputs produce the same core judgement?  
12. **Continuity** — Does learner educational history survive plan and product change without silent invention or erasure?  
13. **Blueprint** — Does the proposal align with the Product Blueprint and Educational Constitution?

### Pass rule

Proceed when the design strengthens truth, clarity, integrity, and trust without inventing educational certainty.

### Stop rule

Stop or redesign when the proposal:

- creates competing homes or competing metrics;
- hides implementation as product language;
- writes educational state outside authorised educational workflows;
- cannot explain its conclusions;
- trades honesty for polish;
- or conflicts with the Educational Constitution or Product Blueprint.

---

## Authority

**Owner:** Architecture Governance  
**Classification:** Governing product-design philosophy  
**Supersedes:** None — this document is foundational  

Future ADRs, programme blueprints, information architectures, and significant UI redesigns should cite compliance with these principles (by DP identifier) where material.
