# Kwalitec Product Blueprint

**Version:** 1.1  
**Status:** Active  
**Effective:** July 2026  
**Authority:** Product strategy (subordinate to Vision 2030 on philosophy)

---

## Purpose

This document defines **how** Kwalitec operates as a product: audiences, educational model, Digital Twin role, roadmap, and product promise.

**Philosophy, north star, and never-build rules** are owned exclusively by:

[`knowledge/product/vision/PRODUCT_VISION_2030.md`](knowledge/product/vision/PRODUCT_VISION_2030.md)

Do not restate Vision philosophy here. Link to it.

Document hierarchy: [`knowledge/GOVERNANCE.md`](knowledge/GOVERNANCE.md).

**Canonical path:** repository root `PRODUCT_BLUEPRINT.md`.  
Do not create a second copy under `knowledge/`.

---

## Governing references

| Authority | Path | Use when |
|---|---|---|
| Product Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Why; north star; Final Test |
| Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational lawfulness |
| Product Language Guide | `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` | Learner-facing terminology |
| Architecture | `ARCHITECTURE.md`, `docs/architecture/SYSTEM_ARCHITECTURE.md` | Runtime structure |

---

## Vision alignment (summary only)

Kwalitec exists to help students become professionals by answering, every day:

1. What to study  
2. Why it matters  
3. Whether they understand it  
4. What they should do next  

**North star** (Vision): materially higher exam pass probability for consistent users.  
**Daily product expression**: the highest-value next action the student should take.

Full text: Vision 2030.

---

## Company purpose (not domain “Mission”)

Kwalitec maximises a student's probability of passing professional examinations in the shortest **sustainable** time.

We achieve this by:

- understanding the official curriculum;
- modelling the student's educational state;
- reasoning over evidence;
- providing explainable recommendations.

**Terminology:** In product and engineering prose, “Mission” may mean the Educational OS study commitment. In learner UI, use **Session** / **Today's Session** (Product Language Guide). This Blueprint’s “purpose” section is not the domain Mission entity.

---

## The problem we solve

Professional examination students frequently experience:

- repeated failures;
- inefficient study;
- poor revision timing;
- uncertainty about readiness;
- information overload;
- lack of personalised guidance.

Most students do not fail because they never study.

They fail because they repeatedly make suboptimal study decisions.

Kwalitec exists to improve those decisions — consistent with Vision 2030 (structure, consistency, feedback, guidance, confidence).

---

## Target users

**Primary:** Students preparing for professional qualification examinations, including:

- IFoA
- SOA
- CAA
- CAS
- other professional bodies in future

**Secondary:** Training providers and employers supporting professional qualification programmes.

---

## Product operating principles

These implement Vision 2030 in product decisions. They do not replace Vision.

### 1. Educational outcomes before engagement

Success is measured by learning outcomes and pass probability — not screen time, vanity DAU, or gamification metrics.

### 2. Evidence before opinion

Recommendations arise from curriculum, learning evidence, Digital Twin, and educational reasoning — never arbitrary heuristics or opaque AI.

### 3. Explainability

Every recommendation must answer **why**, in educationally defensible language (Vision AI philosophy).

### 4. Sustainable progress

Maximise effective learning while reducing burnout — not maximise study hours.

### 5. Professional quality

Reliability, accuracy, transparency, and consistency — students trust Kwalitec with their professional future.

---

## What Kwalitec is

- an educational intelligence platform;
- an evidence-driven study companion;
- a personalised decision-support system;
- a Digital Twin of the student's educational journey;
- the product surface of the Educational Operating System (EOS).

## What Kwalitec is not

- a generic note-taking application;
- a flashcard app;
- a question bank;
- a habit tracker;
- a gamification platform;
- a social network.

Those capabilities may exist within Kwalitec, but they are not the product's identity.

**Never-build list:** Vision 2030 (authoritative).

---

## The educational model

The platform is built upon four pillars.

| Pillar | Meaning |
|---|---|
| **Curriculum** | Understand the syllabus (official structure is primary truth). |
| **Student** | Understand the learner (educational state, not demographics alone). |
| **Evidence** | Understand what has actually happened. |
| **Decisions** | Recommend what should happen next. |

### Decision framework

Every recommendation should maximise expected educational value.

The Decision Engine considers curriculum weighting, knowledge, memory, behaviour, performance, available study time, and examination date.

Its output is the highest-value next action — the daily expression of the Vision north star.

### Digital Twin

The Digital Twin is the educational model of the student.

It evolves through evidence rather than assumptions.

Future educational capabilities should improve the Digital Twin rather than bypass it.

**Do not modify Twin or EducationalStateService in governance-only programmes** — see post-consolidation execution directive.

### Educational State (product meaning)

Educational State is the unified learning truth presented to experience surfaces.

Engineering requirement (Vision): **One Educational State** — no parallel educational truths for the same student moment.

Runtime detail: `docs/architecture/SYSTEM_ARCHITECTURE.md`.

### One Runtime (product meaning)

Learners have one navigation and one canonical student experience (`/student/*`, `/session/*` under sole runtime).

Legacy shells may redirect; they must not teach a second educational story.

---

## Success metrics

Aligned with Vision 2030. Product tracks:

| Metric | Notes |
|---|---|
| Exam pass rate | Ultimate outcome (north star) |
| Predicted readiness accuracy | Calibration of readiness claims |
| Study consistency | Behavioural substrate of learning |
| Session / Mission completion | Domain Mission; UI Session |
| Revision adherence | Intelligent revision behaviour |
| Recommendation acceptance | Trust in guidance |
| Retention | Continued use through exam cycle |
| Educational satisfaction | Qualitative trust and clarity |
| Confidence (where evidenced) | Gradual confidence building — not vanity |

Activity metrics (raw time, click counts, videos watched) are **not** success metrics.

Analytics architecture (design): `knowledge/product/analytics/PRODUCT_ANALYTICS_ARCHITECTURE.md`.

---

## Product roadmap

### Version 1 (Internal Alpha — RC2 baseline)

Shipped for invite-only Internal Alpha:

- Curriculum Architecture (Epic 1) — V1 flat + V2 hierarchical curricula
- Educational Intelligence domain stack (Epic 2) — Twin / Evidence / Readiness / Decision / Recommendation packages (Stage A product coexistence remains where documented)
- Student Learning + Revision workspaces
- Founder Command Centre (operations, not educational authority)
- Brand infrastructure and Internal Alpha identity
- Architecture consolidation — Education Operating System as canonical runtime

Version 1 does **not** include public registration, Exam Ready lifecycle as a marketed guarantee, or a claim that Twin-first authority is fully cut over on every legacy path.

### Version 2 / later epics (deferred)

**Epic 2 product cutover / Epic 3** — Adaptive Educational Guidance on Twin-first authority:

- Explainable recommendations as sole product path
- Dynamic study planning refinements
- Revision optimisation beyond Version 1 Revision Workspace
- Twin persistence and Evidence journal product loops

**Epic 4** — Professional Learning Ecosystem:

- Multiple examination providers
- Institutional support
- Advanced analytics (beyond private-beta instrumentation)

### Historical epic labels

Original Epic 2–4 headings remain as long-term strategy language. Prefer the Version 1 / Version 2 framing above when judging whether a capability is live.

---

## Product promise

We do not promise to guarantee examination success.

We promise to help students make better educational decisions.

Over time, consistently better decisions should lead to consistently better outcomes — the Vision north star.

---

## Closing

Kwalitec is being built for students pursuing some of the most demanding professional qualifications in the world.

Every design decision should honour that responsibility and pass the Vision Final Test:

> Does this help students become better professionals?

---

**Version:** 1.1  
**Status:** Active  

Review at the conclusion of every major release. Update only through deliberate product strategy discussions. Philosophy changes require Vision 2030 amendment first.
