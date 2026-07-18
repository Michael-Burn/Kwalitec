# Version 2 Design Manifesto

**Document ID:** V2-DESIGN-MANIFESTO  
**Status:** Foundational  
**Authority:** Foundational  
**Audience:** Every engineer, product contributor, and AI agent working on Version 2  
**Nature:** Philosophical foundation — not a technical specification  

**Read this first.** Then read architecture, ADRs, and package docs.

---

## Purpose

This manifesto states the design philosophy of Kwalitec Version 2.

It is not an API contract.  
It is not a schema.  
It is not a roadmap.

It is the shared educational and engineering conscience for all Version 2 work.

---

## Core Principles

### 1. Educational outcomes over engagement

We optimise understanding, retention, and exam readiness.  
We do not optimise screen time, streaks, or empty activity volume.

### 2. Evidence over assumption

Educational state changes only when observable evidence arrives.  
Assumptions are not learner truth.

### 3. Deterministic educational decisions

Given identical educational inputs, core engines produce identical conclusions.  
Surprise belongs in learning content — not in platform authority.

### 4. Explainability over opacity

Every recommendation must be explainable.  
Every recommendation must reference evidence.  
Opaque scores are not educational authority.

### 5. Curriculum is independent from pedagogy

The syllabus is official structural truth.  
Teaching strategy lives in Instructional Blueprints.  
Neither may silently rewrite the other.

### 6. Pedagogy is independent from learner state

Blueprints describe how to teach.  
The Digital Twin describes what evidence says about the learner.  
The Twin does not teach; blueprints do not invent mastery.

### 7. AI assists learning — AI does not determine educational truth

AI may explain, coach, and enrich.  
AI must not own learner-state mutations, syllabus order, or unverifiable mastery claims.

### 8. One responsibility per bounded context

Every Version 2 context owns exactly one educational responsibility.  
God services and cross-domain theatres are forbidden.

### 9. Framework independence

Educational cores must not depend on Flask, SQLAlchemy, UI, or request globals.  
Adapters may; educational law may not.

### 10. Long-term maintainability

Prefer clear boundaries, immutable history, and small reversible decisions.  
Convenience that corrupts educational honesty is not progress.

### 11. Learning quality over application usage

The platform succeeds when students understand more and pass more —  
not when they spend more time inside the product.

---

## Digital Twin Stance

The Student Digital Twin is the evidence-based model of learner educational state.

- Philosophy: [`DIGITAL_TWIN_PHILOSOPHY.md`](DIGITAL_TWIN_PHILOSOPHY.md)
- Constitution: [`../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md`](../../docs/architecture/DIGITAL_TWIN_CONSTITUTION.md)
- Architecture: [`STUDENT_DIGITAL_TWIN.md`](STUDENT_DIGITAL_TWIN.md)

---

## How to Use This Document

1. Read this manifesto.
2. Read [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md).
3. Read relevant ADRs under [`ARCHITECTURE_DECISIONS/`](ARCHITECTURE_DECISIONS/).
4. Implement only within the owning bounded context.
5. If a change contradicts this manifesto, stop and seek architectural review.

---

## Authority

**Authority class:** Foundational  

This manifesto does not replace the Educational Constitution or the Digital Twin Constitution.  
It orients Version 2 design so those higher laws are easier to obey.
