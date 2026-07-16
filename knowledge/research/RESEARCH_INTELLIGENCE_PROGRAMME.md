# Research Intelligence Programme Blueprint

**Capability ID:** RIP-000  
**Programme:** Research Intelligence Programme  
**Programme ID:** RIP-000  
**Title:** Research Intelligence Programme Blueprint  
**Priority:** P0  
**Status:** APPROVED — awaiting Architecture Review before capability design  
**Version:** 1.0  
**Date:** 2026-07-16  
**Nature:** Governance only — documentation; no application code  
**Classification:** Product research programme — independent of Educational Intelligence, Digital Twin, Educational Constitution, Learning Experience, and Product Trust  

---

## Authority

This Blueprint is the master roadmap for **Research Intelligence** — the programme that transforms Internal Alpha from a manual feedback process into a structured research platform that continuously captures, organises, analyses, and preserves student experience of the product.

It is **completely independent** from:

1. Educational Intelligence  
2. Digital Twin  
3. Educational Constitution (`KWALITEC_EDUCATIONAL_CONSTITUTION.md`)  
4. Learning Experience Programme  
5. Product Trust Programme  

This Programme exists to understand the **PRODUCT**.  
It does **not** exist to understand the learner as an educational subject.

This document:

- defines **programme vision, principles, capability roadmap, research lifecycle, conceptual research objects, and success criteria**;
- does **not** design implementation, schemas, dashboards, forms, models, migrations, analytics algorithms, AI, badges, or scoring systems;
- does **not** amend educational meaning, evidence rules, or learning-loop behaviour;
- does **not** modify application code.

**Research Intelligence consumes the product experience.  
It must never change educational meaning.**

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)  
2. [Programme Vision](#2-programme-vision)  
3. [Programme Principles](#3-programme-principles)  
4. [Programme Scope](#4-programme-scope)  
5. [Capability Roadmap](#5-capability-roadmap)  
6. [Research Lifecycle](#6-research-lifecycle)  
7. [Research Objects](#7-research-objects)  
8. [Research Philosophy](#8-research-philosophy)  
9. [Founder Intelligence Vision](#9-founder-intelligence-vision)  
10. [Future Evolution](#10-future-evolution)  
11. [Architecture Relationships](#11-architecture-relationships)  
12. [Success Criteria](#12-success-criteria)  
13. [Out of Scope](#13-out-of-scope)  
14. [Known Limitations](#14-known-limitations)  
15. [Cross References](#15-cross-references)  

---

## 1. Executive Summary

Internal Alpha today relies primarily on manual text feedback: students write free-form notes; the Founder Operating System processes week folders through a filesystem pipeline (`FOS-003`). That model can capture issues, but it does not give students a continuous, low-friction way to contribute product observations inside Kwalitec, and it does not give the Founder a living picture of how the product feels day to day.

The Research Intelligence Programme replaces that manual posture with an integrated research experience. Students should feel they are helping improve the product — not completing surveys. Every meaningful study session becomes an optional opportunity for Kwalitec to learn about its own product experience.

Research Intelligence continuously answers:

- How are students experiencing Kwalitec today?  
- Why?  
- What changed?  
- What should the Founder improve next?

The Programme is sequenced as five capabilities (RIP-001 through RIP-005), from Daily Check-in through Version 2 Community Research. This Blueprint governs that sequence. It does not implement any of it.

**Hard boundary:** Research Intelligence observes product experience. Educational Intelligence observes learning. The two remain independent forever.

---

## 2. Programme Vision

Every meaningful study session becomes an opportunity for Kwalitec to learn about its own product experience.

Students study for exams. Research Intelligence does not interrupt that purpose. It sits beside study as a short, optional, structured reflection on the product — clarity, friction, delight, confusion, trust in the interface, reliability of workflows — never as a measure of mastery, readiness, or educational state.

Over time, structured contributions accumulate into Founder-visible trends, insights, and product findings. The Founder makes conscious decisions: act, defer, or reject. Future releases close the loop when students can see that their contribution mattered.

**End state:** Kwalitec runs a continuous product-research loop inside the product itself — lightweight for students, decisive for the Founder, and strictly separated from educational cores.

---

## 3. Programme Principles

Every capability in this Programme obeys the following principles.

### Research Principle 1 — Reflection, not administration

Feedback should feel like reflection, not administration.

The student experience must feel like a brief moment of honesty about the product after studying — not a compliance form, not a survey battery, not homework about homework.

### Research Principle 2 — Structure over free-text

Structured feedback should be preferred over long free-text.

Most answers should be single-click or similarly constrained. Free-text remains available as an optional enrichment path, never as the default tax for being helpful.

### Research Principle 3 — Why is always visible

Students should always understand why feedback is requested.

Every prompt states its purpose in plain language: improving the product, not judging the student’s learning.

### Research Principle 4 — Recognition for meaning, not verbosity

Recognition should reward meaningful contribution, not verbosity.

Consistency, constructive participation, quality, and community contribution matter. Longest comments, spam volume, and empty repetition must not be rewarded.

### Research Principle 5 — Every item is acted on or consciously rejected

Every feedback item should either:

- influence a product decision, or  
- be consciously rejected.

Silence after contribution is a research failure. Rejection is allowed; invisibility is not.

### Research Principle 6 — Product observation, not learning observation

Research Intelligence observes product experience.  
Educational Intelligence observes learning.

The two must remain independent. Research signals must never write Educational Evidence, Estimated Knowledge, Estimated Mastery, Study Progress, readiness, mission authority, or any Digital Twin educational state. Educational surfaces must never silently reclassify Research contributions as proof of understanding.

---

## 4. Programme Scope

### 4.1 In programme

| Area | Meaning |
|------|---------|
| Daily Check-in experience | Optional, post-study structured product reflection |
| Contributor recognition | Philosophy and later capability for meaningful contribution |
| Founder Intelligence Dashboard | Vision for founder-facing product research visibility |
| Insight Engine | Organisation of observations into trends and findings |
| Version 2 Community Research Platform | Longer-horizon community research surface |
| Conceptual research objects | Shared vocabulary for later design (not schemas) |
| Lifecycle and relationships | How research sits beside study without changing education |

### 4.2 Explicit non-goals (this Blueprint)

No application code. No dashboards. No forms. No models. No migrations. No analytics implementation. No AI. No educational redesign. No contributor implementation. No badges. No scoring. Blueprint only.

### 4.3 Independence declaration

This Programme does not reopen, amend, or subordinate itself to Educational Integrity, Learning Experience, Product Trust, Educational Intelligence, or Digital Twin authorities. Those programmes govern learning meaning, learning loop, and product trust. Research Intelligence governs product-experience research only.

---

## 5. Capability Roadmap

Implementation sequence. Later capabilities may depend on earlier ones; this Blueprint describes **purpose only**. Do not treat these descriptions as UI, schema, or algorithm designs.

---

### RIP-001 — Daily Check-in Experience

**Purpose**  
Give students an optional, approximately 30-second structured check-in after studying so product experience can be captured continuously inside Kwalitec.

**Problem addressed**  
Internal Alpha depends on manual free-text dumps outside the product rhythm. Valuable observations are irregular, hard to compare, and feel like admin work.

**Expected outcome**  
Students can contribute structured product observations without interrupting study. Free-text remains optional. Unlimited submissions remain possible when students choose to contribute more than once.

**Does not**  
Change educational feedback (e.g. LXP Study Session Feedback), invent surveys that block missions, or write educational state.

---

### RIP-002 — Contributor Recognition

**Purpose**  
Recognise students who consistently and constructively help improve the product.

**Problem addressed**  
Without recognition, contribution feels unpaid labour. With the wrong recognition, spam and verbosity are incentivised.

**Expected outcome**  
A recognition philosophy realised later as product behaviour that rewards consistency, constructive participation, quality, and community contribution — never comment length or submission volume alone.

**Does not**  
Implement badges, leaderboards, or scoring in this Blueprint. Recognition design belongs to RIP-002 capability work after Architecture Review of this Programme.

---

### RIP-003 — Founder Intelligence Dashboard

**Purpose**  
Give the Founder a durable view of how students are experiencing the product — satisfaction, friction, loved and confusing areas, contribution health, and release comparison context.

**Problem addressed**  
Founder visibility today depends on processed week artefacts and operational summaries. Continuous in-product research needs a Founder-facing intelligence surface of its own.

**Expected outcome**  
A clear long-term vision for Founder Intelligence (see §9). Implementation remains out of scope for this Blueprint.

**Does not**  
Redesign the Founder Operating System Operational State, Weekly Briefing, or Internal Alpha Pipeline in this document. RIP may later complement those systems; it does not silently replace educational or operational meanings they already own.

---

### RIP-004 — Insight Engine

**Purpose**  
Organise structured responses into product observations, trends, insights, and product findings that can support conscious Founder decisions.

**Problem addressed**  
Raw check-ins alone do not answer “what changed?” or “what should improve next?” without organisation.

**Expected outcome**  
A governed path from Feedback Responses → Insights / Trends / Product Findings → Founder Decisions — without inventing AI summarisation or opaque scoring in this Blueprint.

**Does not**  
Design analytics algorithms, classifiers, or LLM pipelines here.

---

### RIP-005 — Version 2 Community Research Platform

**Purpose**  
Evolve Research Intelligence from individual daily check-ins into a Version 2 community research platform that preserves history, supports release-candidate comparison, and scales contribution beyond early Internal Alpha.

**Problem addressed**  
Version 1 Research Intelligence is continuous but still founder-centred. Version 2 needs community-scale research without becoming educational social media or survey spam.

**Expected outcome**  
A declared evolution path (see §10) that preserves Principles 1–6 and the educational independence boundary.

**Does not**  
Specify Version 2 UX, moderation systems, or community governance mechanics in this Blueprint beyond purpose and constraints.

---

### Dependency sketch (non-blocking narrative)

```
RIP-001 Daily Check-in
        ↓
RIP-002 Contributor Recognition  (needs something worth recognising)
        ↓
RIP-003 Founder Intelligence Dashboard  (needs incoming research signal)
        ↓
RIP-004 Insight Engine  (needs volume + structure to organise)
        ↓
RIP-005 Version 2 Community Research Platform
```

Exact engineering dependencies are deferred to Architecture Review and individual capability briefs.

---

## 6. Research Lifecycle

The complete Research Intelligence lifecycle:

```
Student studies
        ↓
Optional Daily Check-in
        ↓
Structured responses
        ↓
Product observations
        ↓
Founder Dashboard
        ↓
Product decisions
        ↓
Future release
        ↓
Student sees improvements
```

### Lifecycle notes

| Stage | Intent |
|-------|--------|
| Student studies | Primary job remains learning; research never owns this step |
| Optional Daily Check-in | Invitation, not interruption; skippable |
| Structured responses | Prefer clicks; optional free-text |
| Product observations | Research objects accumulate as product experience signal |
| Founder Dashboard | Founder sees experience health and change |
| Product decisions | Act, defer, or consciously reject (Principle 5) |
| Future release | Changes land in the product students use |
| Student sees improvements | Closes the human loop — contribution was not theatre |

Research Lifecycle must not merge with the Learning Experience educational chain (Activity → Observation → Evidence → State → Guidance). Those are different pipes.

---

## 7. Research Objects

Conceptual research objects only. These define shared vocabulary for later design.  
**Do not treat this section as a database schema.**

| Object | Conceptual meaning |
|--------|--------------------|
| **Research Session** | One optional research moment attached to (or near) a study context — the container for a check-in attempt |
| **Feedback Submission** | A completed contribution package within a Research Session |
| **Feedback Question** | A defined prompt used to elicit structured product experience |
| **Feedback Response** | An answer to a Feedback Question (structured primary; free-text optional) |
| **Contribution** | The durable unit of recognised student help toward product improvement |
| **Badge** | A recognition artefact for meaningful contribution patterns (philosophy in RIP-002; not implemented here) |
| **Insight** | An interpreted product-experience signal derived from one or more responses |
| **Trend** | Directional change in product experience over time or across releases |
| **Product Finding** | A concrete, reviewable claim about the product that can enter decision-making |
| **Founder Decision** | A conscious act / defer / reject outcome tied to Findings or Insights |
| **Feature Area** | A product surface or capability region under research (e.g. missions, planning, analytics UI) |
| **Issue Category** | Taxonomy label for kinds of product friction or praise |
| **Severity** | Relative urgency of a product issue for Founder attention |
| **Version** | Product version context for comparing experience over time |
| **Release Candidate** | A candidate build or release slice against which research may be compared |

### Object independence rule

Research objects must not be aliases for Educational Evidence, Educational State, Digital Twin fields, or Learning Experience closure artefacts. Naming collisions with “feedback”, “session”, or “observation” in educational docs are linguistic only — meanings remain separate.

---

## 8. Research Philosophy

### 8.1 Feedback philosophy (student experience)

| Constraint | Rule |
|------------|------|
| Maximum duration | Approximately **30 seconds** |
| Answer style | Most answers require a **single click** (or equivalent one-tap choice) |
| Free-text | Always **optional** |
| Volume | **Unlimited** feedback submissions remain possible |
| Study integrity | Feedback must **never interrupt studying** |

Students should feel they are helping improve the product rather than completing surveys.

### 8.2 Contributor philosophy (recognition)

Recognition should reward:

- **consistency** — returning contribution over time  
- **constructive participation** — useful, actionable product signal  
- **quality** — clarity and relevance over length  
- **community contribution** — helping the product for others, not self-display  

Avoid encouraging spam. Do not reward longest comments. Do not treat unlimited submissions as a scoreboard.

### 8.3 Decision philosophy (Founder duty)

Every Feedback Submission that becomes a Product Finding deserves a Founder Decision path: influence a change, or be consciously rejected with enough trace that the research system does not pretend the item vanished.

---

## 9. Founder Intelligence Vision

Long-term Founder Intelligence should make product experience legible without inventing analytics algorithms in this Blueprint.

Illustrative vision areas (examples, not metrics specs):

| Vision area | Question answered |
|-------------|-------------------|
| Overall satisfaction | How do students feel about the product lately? |
| Would open tomorrow | Is the product worth returning to tomorrow? |
| Most loved feature | What do students value most? |
| Most confusing feature | Where does the product create friction? |
| Fastest growing issue | What is getting worse quickly? |
| Resolved issues | What previously reported pain is gone? |
| Contribution trends | Is research participation healthy? |
| Feedback history | What have we heard over time? |
| Release comparisons | Did experience improve after a release? |
| Student retention | Are contributing students staying with the product? |

Founder Intelligence for Research must remain product-experience intelligence. It must not become a shadow Educational Intelligence dashboard.

---

## 10. Future Evolution

| Horizon | Intent |
|---------|--------|
| Near-term (RIP-001–004) | In-product optional check-in → recognition philosophy → Founder visibility → insight organisation |
| Version 2 (RIP-005) | Community Research Platform: preserved history, release-candidate research, broader contribution without survey culture |
| Ongoing | Continuous answer to “How are students experiencing Kwalitec today / why / what changed / what next?” |

Evolution constraints:

- Principles 1–6 remain binding.  
- Educational independence remains binding.  
- Manual Internal Alpha text pipelines may continue as a complementary Founder Operating System path until consciously superseded; this Blueprint does not mandate their deletion.  
- No AI requirement is introduced by this Programme. Opaque generative interpretation of student research is not a Version 1 research goal.

---

## 11. Architecture Relationships

### 11.1 Relationship matrix

| Programme / authority | Relationship |
|----------------------|--------------|
| **Educational Integrity Programme** | Independent. EIP governs educational meaning, evidence, and state. RIP must not write or reinterpret educational state. |
| **Learning Experience Programme** | Adjacent but separate. LXP owns the study → practice → educational feedback loop. RIP may invite optional product check-in near study moments but must not replace or mutate LXP educational closure (including LXP-004 Study Session Feedback). |
| **Product Trust Programme** | Complementary consumer. PTP improves clarity, consistency, transparency, and reliability. RIP may later *observe* whether trust work improved experience; RIP does not redefine PTP principles or reopen PTP capabilities. |
| **Version 1 Release Programme** | Release context. RIP may use Version / Release Candidate as research dimensions. RIP does not itself certify educational or engineering release gates. |
| **Educational Intelligence** | Strict separation. Educational Intelligence observes learning. Research Intelligence observes product experience. |
| **Digital Twin** | Strict separation. RIP must not become a twin writer or twin narrative channel. |
| **Educational Constitution** | Non-amending. RIP does not change constitutional educational meaning. |
| **Founder Operating System (FOS / FSI)** | Complementary. Existing Internal Alpha pipeline and Founder Operational State remain Founder infrastructure. RIP defines an in-product research programme that may later feed Founder visibility; it does not silently absorb FOS ownership in this Blueprint. |

### 11.2 Consumption rule

```
Product (study workflows, UI, releases)
        ↓  consumed as experience context
Research Intelligence
        ↓  produces product findings / decisions
Future product improvements
```

Research Intelligence **consumes** the product.  
It must **never change educational meaning**.

### 11.3 Layering note (for later Architecture Review)

When capabilities are designed, Research Intelligence HTTP/services/models (if any) must follow Kwalitec layering:

```
Templates/JS → Blueprints → Services → Models → DB
```

and must not place research math in routes or educational curriculum engines. This Blueprint does not create those layers yet.

### 11.4 Curriculum V1/V2

Research Intelligence does not alter curriculum loaders, traversal, or V1/V2 coexistence. Curriculum compatibility impact of this Blueprint: **N/A** (documentation only; no engine touch).

---

## 12. Success Criteria

The Programme Blueprint succeeds when Architecture Review can confirm:

| ID | Criterion |
|----|-----------|
| S-1 | Vision and principles are explicit and binding for RIP-001–RIP-005 |
| S-2 | Capability roadmap purposes are clear without implementation design |
| S-3 | Research Lifecycle is complete and distinct from the educational learning loop |
| S-4 | Conceptual Research Objects are defined without schemas |
| S-5 | Feedback and Contributor philosophies constrain future UX incentives |
| S-6 | Founder Intelligence vision is declared without analytics algorithms |
| S-7 | Independence from Educational Intelligence, Digital Twin, Constitution, LXP, and PTP is unambiguous |
| S-8 | Out of scope forbids code, dashboards, forms, models, migrations, AI, badges, and scoring in this milestone |

Programme delivery success (later) will be judged per capability — not by this Blueprint alone.

---

## 13. Out of Scope

This milestone and this Blueprint exclude:

- Application code changes  
- Dashboards (implementation)  
- Forms / check-in UI  
- ORM models  
- Migrations  
- Analytics implementation  
- AI / LLM interpretation  
- Educational redesign  
- Contributor implementation  
- Badges / scoring systems  
- Database schemas  
- Algorithm design for insights or recognition  

**Blueprint only.**

---

## 14. Known Limitations

| Limitation | Implication |
|------------|-------------|
| Manual Internal Alpha still exists | RIP does not yet replace `raw_feedback/` week processing; dual paths may coexist until a later decision |
| No capability designs yet | RIP-001–RIP-005 require separate briefs after Architecture Review |
| No instrumentation yet | Vision areas in §9 are aspirational labels, not measurable KPI definitions |
| Recognition not implemented | Philosophy only; spam-resistance must be engineered in RIP-002 |
| Insight Engine unspecified | Organisation of observations is purposeful but not algorithmic here |
| Version 2 is horizon only | RIP-005 is roadmap intent, not a near-term build plan |
| Founder OS overlap unresolved in detail | How RIP dashboards relate to FOS Operational State / Weekly Briefing needs Architecture Review |

---

## 15. Cross References

| Document | Role relative to RIP |
|----------|----------------------|
| `knowledge/founder/FOS-003_INTERNAL_ALPHA_PIPELINE.md` | Current manual Internal Alpha processing baseline |
| `knowledge/founder/FSI-003_INTERNAL_ALPHA_LIVE_WORKFLOW.md` | Live week-folder workflow for text feedback |
| `knowledge/product/LEARNING_EXPERIENCE_PROGRAMME.md` | Educational daily loop — separate from research check-in |
| `knowledge/product/LXP-004_STUDY_SESSION_FEEDBACK.md` | Educational session narration — not product research |
| `knowledge/product/PRODUCT_TRUST_PROGRAMME.md` | Product trust programme — may be observed by RIP; not owned by RIP |
| `knowledge/educational/EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | Educational integrity — independent authority |
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational meaning — must not be changed by RIP |
| `PROJECT_CONTEXT.md` / `ARCHITECTURE.md` | Product and structural context |

---

## Governance

- **Owner:** Research Intelligence Programme (RIP-000)  
- **Change control:** Amendments to principles, independence boundaries, or roadmap require explicit Programme update and Architecture Review  
- **Implementation gate:** No RIP capability may implement application behaviour until this Blueprint has passed Architecture Review and the specific capability brief is approved  
- **Educational safety gate:** Any proposed RIP behaviour that would write educational state or redefine educational meaning is automatically out of programme scope  

---

*End of Research Intelligence Programme Blueprint (RIP-000).*
