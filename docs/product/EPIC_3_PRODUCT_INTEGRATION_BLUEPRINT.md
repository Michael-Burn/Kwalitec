# Epic 3 — Product Integration & Experience Blueprint

**Epic:** Epic 3 — Product Integration & Experience  
**Status:** Kickoff — Blueprint only  
**Predecessor:** Epic 2 — Educational Intelligence (v0.5.0 domain release)  
**Target product:** Kwalitec Version 1.0  
**Governing ADRs:** ADR-001 (Curriculum Hierarchy), ADR-002 (Educational Intelligence Architecture)  
**Upstream gates:** Epic 2 Completion Review, Architecture Guardian Review (Epic 2) — APPROVED WITH CONDITIONS  

**This document is a product blueprint.** It does not authorize implementation, architecture redesign, migrations, or tests.

---

# Purpose

Epic 3 transforms the completed Educational Intelligence Platform (v0.5.0) into the production student experience that will become Kwalitec Version 1.0.

Educational Intelligence is complete.

Epic 3 integrates it into the product.

---

# 1. Executive Summary

## Platform → Product

Epic 2 delivered a **platform**: a framework-independent Educational Intelligence stack that can, from Learning Evidence and Twin state, answer *what the highest-value next action should be* — with Decision as sole selection authority, explainability by construction, and Curriculum V1/V2 safety.

That stack lives in domain packages. It is not yet the student experience.

Epic 3 delivers the **product**: the same intelligence, wired through thin orchestration into readiness, recommendation, mission, progress, and daily study surfaces — so that what students see is Twin-first Educational Intelligence, not Stage A legacy heuristics.

```
Platform (v0.5.0)
  Evidence → Twin → Readiness → Decision → Recommendation → Mission
         ↓
Product Integration (Epic 3)
  Orchestration · Persistence · Cutover · Experience · Trust
         ↓
Version 1.0
  Students receive one calm, explainable, complete study day
```

## Why Epic 3 exists

v0.5.0 ships **named Stage A dual truth**: live surfaces still consume `ReadinessService`, `RecommendationService`, and `PlanningService` / ORM missions while Twin-first engines exist only in `app/domain/`. Claiming Twin-first student behaviour today would be false.

Epic 3 exists to:

1. Eliminate that dual truth through honest Stage B → Stage C cutover (no hybrid averages).  
2. Persist Twin, Evidence, and Decision Journal so intelligence survives sessions.  
3. Present a premium, trustworthy Version 1.0 experience where every visible control works.  
4. Validate with real students that the product reduces decision load and increases learning confidence.

Epic 3 must **not** redesign Educational Intelligence (ADR-002). It integrates what Epic 2 already proved.

---

# 2. Objectives

## Primary goals

### Integrate Educational Intelligence

Wire thin service-layer orchestration so product surfaces consume Twin-first Readiness, Decision, Recommendation packaging, and Mission Intelligence — without moving educational math into routes or inventing a second intelligence architecture.

### Eliminate Stage A dual truth

Freeze deepening of legacy readiness / recommendation / mission-generation heuristics as Twin-first truth. Progress through named dual-truth adapters (Stage B) to single product educational authority (Stage C). Never average legacy percentages with Twin / Decision factors.

### Premium UX from Version 1.0

Version 1.0 ships as a coherent premium student product: calm daily guidance, explainable recommendations, attributable missions, and progress that reflects evidence — not a dashboard of unfinished experiments.

### Trust before features

Prefer fewer complete surfaces over many half-wired ones. Warrant honesty, cold-start posture, and Decision attribution outrank feature count.

### Student-first validation

Judge Epic 3 success by whether students understand what to do next, trust why, and can sustain study — not by domain package completeness alone (already achieved in Epic 2).

---

# 3. Product Principles

These principles bind Epic 3 product decisions. They extend the Engineering Charter and ADR-002 into student-facing behaviour.

### Premium is incremental

Premium is earned by disciplined cutover and finish quality, not by a visual redesign that outruns intelligence wiring. Ship polish on surfaces that already tell the educational truth.

### Trust before features

If a feature cannot be explained from Curriculum → Evidence → Twin → Readiness → Decision → Recommendation → Mission, it does not ship as educational guidance.

### Invisible Intelligence

Students experience a clear next action and a calm day. They should not need to understand Twin domains, warrant tags, or pipeline order. Intelligence stays behind the experience unless they ask *why*.

### No dead buttons

Every control a student can see must complete a real action or navigate to a finished destination. Disabled theatre, placeholder CTAs, and “coming soon” behind active chrome are forbidden on Version 1.0 surfaces.

### Educational honesty

Cold-start, thin warrant, and unknown postures remain visible in product language. Never invent Mid/High preparedness theatre under sparse evidence.

### Progressive disclosure

Default view: one recommendation, today’s mission, enough context to act. Detail, lineage, and deeper analytics expand on demand — not as competing first-viewport noise.

### Every visible feature is complete

Version 1.0 scope is defined by what students may touch. Unfinished capability is deferred, hidden, or honestly labelled outside the interactive path — never half-exposed.

### Explainability everywhere

Recommendations and mission tasks answer *why* with chain-supported reason codes and attributions. Opaque “recommended for you” copy is rejected.

### Calm over complexity

Reduce decisions. Increase learning. Prefer one clear path over multi-panel urgency, streak theatre, and competing calls to action.

### Student confidence over feature count

Success is a student who trusts the next step — not a feature matrix that impresses evaluators.

### Research-backed operational behaviour

Spacing, retrieval, burnout pacing, session length, habit formation, metacognition, and cognitive load inform *how* the product operates sessions and messaging — without replacing evidence-driven Twin personalisation or Decision selection authority.

---

# 4. Integration Strategy

Epic 3 replaces **product authority**, not Epic 2 domain design.

Educational Intelligence remains:

```
Learning Evidence
      ↓
Twin Update Pipeline (K → M → B → P)
      ↓
Digital Twin snapshot
      ↓
Readiness Aggregation
      ↓
Decision Engine          ← sole next-action selection
      ↓
Recommendation packaging ← projection only
      ↓
Mission Intelligence     ← execution / projection only
```

## What product cutover replaces

| Legacy product peer | Twin-first authority after cutover | Integration rule |
|---|---|---|
| `ReadinessService` (overall % / coverage composites as preparedness truth) | Domain Readiness Aggregation projections | Freeze heuristic deepening; Stage B adapters; Stage C product authority; no hybrid % + Twin averages |
| `RecommendationService.generate_recommendations` | Decision → Recommendation packaging | Decision selects; packaging narrates; legacy ceases to be next-action authority |
| `MissionService` / optimizer mission generation | Decision → Mission Intelligence composition | Mission executes Decision; does not re-rank or invent filler under leftover capacity |
| `PlanningService` (as daily next-action / mission authority) | Remains multi-day WeekPlan / exam-date planning owner where appropriate; loses dual claim on Twin-first daily selection | Planning ≠ Decision; cutover targets mission/next-action dual authority, not deletion of exam-date planning |
| Learning Evidence (product loops) | Append-only Evidence as sole Twin write input | Accept/dismiss, completion, failure → Evidence → Strategies — never mastery or readiness writes from UI handlers |
| Twin persistence | Durable Twin snapshots + load path for orchestration | Adapters outside domain packages; domain stays framework-free |
| Decision orchestration | Thin services: `CurriculumContext` builder, pipeline factory, Decision → Recommendation → Mission path, Decision Journal recording | Orchestration before live consumers; no educational selection in routes |

## Explicit non-goals of integration

- Redesigning Evidence → Twin → Readiness → Decision → Recommendation → Mission.  
- Moving selection into Recommendation, Mission, Planning, or LLM-owned services.  
- Merging legacy and Twin scores into a temporary “hybrid truth.”  
- Treating structural Twin postures as finished calibrated pass-probability scores without warrant discipline.  
- Deleting legacy services on day one before Stage B/C adapters exist (progressive cutover, not big-bang rewrite).

---

# 5. Capability Streams

Epic 3 organises work into five capability streams. Streams may proceed with controlled parallelism, but **Integration and Learning Evidence foundations precede Premium Experience claims**.

## A — Integration

**Responsibility:** Make Educational Intelligence the product’s educational authority.

- Thin orchestration adapters (Evidence → Pipeline → Twin; Decision → Recommendation → Mission).  
- `CurriculumContext` construction via Curriculum helpers only (V1/V2 safe).  
- Stage B named dual-truth adapters → Stage C single product authority.  
- Freeze legacy heuristic deepening as Twin-first truth.  
- Preserve Decision sole selection authority and write/read firewall at every boundary.

## B — Learning Evidence

**Responsibility:** Close the live learning loop so Twin state reflects real study.

- Twin persistence so snapshots survive sessions.  
- Decision Journal persistence (accept / dismiss / defer as preference evidence).  
- Mission persistence convergence (`domain.Mission` → product mission path without type conflation).  
- Completion / failure → Behaviour Learning Evidence loops.  
- Ensure UI outcomes become Evidence, not direct Twin or readiness mutation.

## C — Premium Experience

**Responsibility:** Present Version 1.0 as a calm, coherent, premium student product.

- Dashboard and Today’s Mission as Twin-first surfaces.  
- Warrant-bound recommendation and explanation copy.  
- Progressive disclosure; no dead buttons; complete interactive paths only.  
- Focus, consistency, performance, and accessibility as product quality bars — not afterthoughts.  
- Premium polish applied to finished educational truth, not to unfinished experiments.

## D — Product Trust

**Responsibility:** Earn and protect student trust in guidance.

- Educational honesty (cold-start / thin warrant).  
- Explainability chain visible where students need it.  
- Scope discipline: Included / Deferred / Hidden / Coming Soon.  
- No preparedness theatre; no black-box recommendations.  
- Communications honesty: do not market Stage A or partial cutover as Twin-first Version 1.0.

## E — Student Validation

**Responsibility:** Prove the product works for learners, not only for architecture reviews.

- Student-first journeys through recommendation → mission → study → evidence.  
- Qualitative and outcome-oriented validation against Version 1.0 success criteria.  
- Feedback loops that inform messaging and UX — without reopening educational selection architecture.  
- Confirm “reduce decisions, increase learning” in practice.

---

# 6. Version 1.0 Scope

**Rule:** Students never interact with unfinished functionality.

## Included

- Twin-first daily recommendation (Decision-packaged, explainable).  
- Today’s Mission attributable to Decision (no re-ranking theatre).  
- Learning Evidence capture for study outcomes that matter to the Twin loop.  
- Durable Twin / journal persistence required for truthful multi-day guidance.  
- Dashboard focused on next action, today’s work, and honest progress signals.  
- Curriculum-safe behaviour for V1 and V2 syllabuses.  
- Auth, ownership scoping, and existing security posture preserved.  
- Calm premium UX on the included interactive surface.

## Deferred

- Calibrated Confidence-as-risk narratives (requires Confidence ownership enrichment — Epic 3+).  
- Belief-bag / scoring enrichment beyond structural Twin postures (Readiness / Performance / Behaviour / Decision optimisation math).  
- LLM-owned educational selection (rejected by ADR-002).  
- Broad analytics theatre unrelated to next-action trust.  
- Feature expansion that does not improve pass probability, decision quality, student modelling, or explainability.

## Hidden

- Incomplete admin / diagnostic domain tooling not ready for students.  
- Dual-authority debug views during Stage B (engineering-only).  
- Experimental enrichment UI that would expose unfinished Confidence or scoring claims.

## Coming Soon

- Capabilities acknowledged to students only as non-interactive messaging (if at all), never as clickable unfinished chrome.  
- Post–1.0 enrichments (deeper calibrated readiness, richer metacognitive coaching) communicated without implying they are live.

If a capability is not Included, it must be Deferred, Hidden, or Coming Soon — and must not appear as a working control.

---

# 7. Product Experience Vision

### Dashboard

One composition oriented to *what to do next*. Brand and calm hierarchy first; not a multi-widget command centre. Primary content: today’s recommendation, path into mission, honest status — not competing panels of unfinished insight.

### Today's Mission

A single day’s attributable work derived from Decision via Mission Intelligence. Tasks explain their educational warrant. No filler tasks invented to fill leftover capacity. Completion feeds Evidence.

### Recommendation

One clear next action (or an honest cold-start posture). Packaged from Decision — title, explanation affordances, warrant posture. Students should not choose among conflicting heuristic lists that disagree with Decision.

### Explainability

*Why this?* answers use chain-supported reason codes and attributions. Detail is progressive: short default rationale; deeper lineage on demand. Never strip warrant to make guidance look more confident than evidence allows.

### Progress

Progress reflects evidence-backed Twin / readiness projections appropriate to Version 1.0 honesty — not vanity streaks or legacy percentages presented as Twin truth during dual authority.

### Focus

The product removes the daily “what should I study?” burden. First viewport avoids schedule dumps, promo clusters, and secondary marketing of unfinished features.

### Consistency

Same educational vocabulary across dashboard, recommendation, mission, and progress. Domain.Mission and models.Mission must not confuse students with divergent “today” stories after cutover.

### Performance

Version 1.0 feels responsive on the daily path (open → recommend → mission → study). Orchestration must not make the calm experience feel heavy; perceived latency is a trust issue.

### Accessibility

Premium includes accessible structure, readable contrast, keyboard paths, and clear focus states on the student journey. Accessibility is part of completeness, not a later polish pass on broken chrome.

---

# 8. Educational Research

Validated educational research gradually informs **operational behaviour** — how Kwalitec paces, frames, and structures study sessions — without replacing evidence-driven personalisation or Decision selection.

| Research theme | Product role in Epic 3 / Version 1.0 | Boundary |
|---|---|---|
| **Spacing** | Session and revisit framing that respects Memory-aware scheduling posture | Does not invent a second spaced-repetition authority outside Twin / Adaptive paths already owned |
| **Retrieval** | Prefer active retrieval-shaped mission work where Decision selects it | Does not force retrieval theatre when warrant is thin |
| **Burnout** | Workload pacing and unsustainable-intensity honesty in messaging and mission sizing | Does not override Decision with wellness heuristics that invent educational state |
| **Session length** | Feasible session design consistent with Behaviour / feasibility signals | Does not pad missions to look productive |
| **Habit formation** | Calm daily ritual: open → next action → complete → return tomorrow | Does not gamify with empty streak authority |
| **Metacognition** | Explainability that helps students understand *why* and reflect lightly | Does not require students to operate Twin domains manually |
| **Cognitive load** | Progressive disclosure; one job per section; reduce competing decisions | Does not dump full explainability chains into the first viewport |

**Binding rule:** Research informs product operations and UX. Learning Evidence and the Twin remain the personalisation authority. Decision remains the next-action authority. Research never justifies hybrid legacy averages or LLM selection.

---

# 9. Student Journey

The Version 1.0 day should feel like this:

```
Morning
   ↓
Open Kwalitec
   ↓
Recommendation          ← Decision packaged; explainable; warrant-honest
   ↓
Mission                 ← Today’s attributable tasks
   ↓
Study                   ← Student does the work
   ↓
Evidence                ← Completion / outcomes recorded as Learning Evidence
   ↓
Twin                    ← Pipeline evolves educational state
   ↓
Tomorrow                ← Next open continues from updated Twin — not from Stage A heuristics
```

Each arrow is a product obligation for Epic 3. Broken arrows (study that does not become Evidence; Evidence that does not update Twin; Twin that does not drive tomorrow’s recommendation) are integration failures, not UX polish issues.

---

# 10. Version 1.0 Success Criteria

### Educational

- Student-facing next action is Decision-authored and chain-explainable.  
- Cold-start / thin warrant postures remain honest in product language.  
- Curriculum V1 and V2 remain loadable and traversable through canonical helpers.  
- Completion and preference events become Learning Evidence, not direct mastery/readiness writes.

### Engineering

- Stage A dual truth eliminated on Version 1.0 student paths (Stage C product authority).  
- Thin orchestration exists; domain packages remain framework-independent.  
- Twin / Decision Journal / Evidence loops persist durably.  
- No hybrid legacy + Twin educational formulas.  
- ADR-002 chain not redesigned; CI discipline (pytest + ruff) held for implementation milestones when they begin.

### Product

- No dead buttons on Version 1.0 interactive surfaces.  
- Included / Deferred / Hidden / Coming Soon discipline enforced.  
- Dashboard + recommendation + mission form one calm daily composition.  
- Explainability available without cognitive overload.

### Student

- Students can answer: *What should I do today, and why?*  
- Decision load for “what next?” is materially reduced.  
- Trust is preserved when evidence is thin (honesty > false confidence).  
- Journey Morning → Tomorrow works across sessions.

### Business

- Version 1.0 can be positioned as a trustworthy Educational Intelligence product experience — not merely a curriculum tracker with a parallel unused domain stack.  
- Marketing claims match Stage C reality.  
- Foundation ready for post–1.0 enrichment inside existing owners (Confidence, calibrated scoring) without architectural rewrites.

---

# 11. Risks

| Risk class | Risk | Mitigation posture |
|---|---|---|
| **Integration** | Dual authority remains while marketing claims Twin-first | Name Stage A/B honestly; Stage C gate before Version 1.0 claims |
| **Integration** | Orchestration missing while UI binds early | Orchestration and persistence before live Twin-first consumers |
| **Integration** | `domain.Mission` vs `models.Mission` conflation | Explicit adapters and naming discipline at cutover |
| **UX** | Presentation strips warrant or invents Mid/High theatre | Bind copy to warrant / reason codes; progressive disclosure |
| **UX** | Premium visual work ahead of educational truth | Premium is incremental; polish finished paths only |
| **Legacy** | Deepening `ReadinessService` / `RecommendationService` / planning mission heuristics during cutover | Freeze as Twin-first truth; adapters only |
| **Legacy** | Hybrid averages as “temporary” packaging | Forbidden (ADR-002 / Epic 2 binding conditions) |
| **Product trust** | Dead buttons, Coming Soon as active chrome, unfinished analytics | Version 1.0 scope rule; no unfinished interactive functionality |
| **Product trust** | Premature Confidence-as-risk narratives | Defer until Confidence ownership enrichment |
| **Technical debt** | Skipping Stage B and forcing big-bang deletion of legacy peers | Progressive cutover; debt register E2-PI / E2-PE / E2-PX items as roadmap, not ignore list |
| **Technical debt** | Reopening Educational Intelligence redesign under product pressure | ADR-002 Epic 3 Implications bind: integrate, do not redesign |

---

# 12. High-Level Roadmap

Capability streams map to Epic 3 capabilities **3.2–3.6**. Capability **3.1** is this blueprint / kickoff (documentation only). No implementation detail below.

| Capability | Stream | Intent (summary) |
|---|---|---|
| **3.2** | A — Integration | Orchestration and Stage B→C cutover so Twin-first engines become product educational authority without redesigning Epic 2 |
| **3.3** | B — Learning Evidence | Persist Twin / journals and close Evidence loops so study outcomes evolve tomorrow’s intelligence |
| **3.4** | C — Premium Experience | Ship the calm Version 1.0 student surfaces on finished Twin-first paths |
| **3.5** | D — Product Trust | Enforce honesty, explainability, and scope discipline so students can trust what they see |
| **3.6** | E — Student Validation | Validate the Morning → Tomorrow journey with students against Version 1.0 success criteria |

**Sequencing principle:** 3.2 and 3.3 establish truth and memory; 3.4 presents that truth; 3.5 guards trust throughout; 3.6 confirms the product works for learners. Experience work must not outrun Integration and Evidence.

---

# 13. Recommendations

How Epic 3 should be executed:

1. **Treat this blueprint as product law for Version 1.0 scope** — integrate Educational Intelligence; do not reopen ADR-002’s chain.  
2. **Start with orchestration and persistence** before Twin-first UI claims (Architecture Guardian binding conditions).  
3. **Freeze legacy heuristic deepening** immediately; cut over through Stage B adapters to Stage C authority without hybrid truth.  
4. **Preserve Decision as sole selection authority**; Recommendation packages; Mission executes.  
5. **Preserve write/read firewall**; all student outcomes that change educational state become Learning Evidence.  
6. **Ship premium only on complete paths**; enforce no dead buttons and Included / Deferred / Hidden / Coming Soon.  
7. **Bind warrant and explainability** before calling recommendations “explainable” in product copy.  
8. **Use research to shape calm operations**, not to replace Twin personalisation or Decision.  
9. **Validate with students** before declaring Version 1.0 success.  
10. **Keep curriculum V1/V2 and security posture intact** at every wiring boundary.  
11. **Execute capability-by-capability** (3.2→3.6) with Analysis → Architecture → Implementation → Review discipline when implementation milestones open — this blueprint authorizes none of those yet.  
12. **STOP after planning artefacts until an implementation milestone explicitly begins.**

---

# References

| Document | Role |
|---|---|
| [`docs/architecture/ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](../architecture/ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md) | Educational Intelligence decision; Epic 3 implications |
| [`docs/architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](../architecture/EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md) | Canonical EI architecture |
| [`docs/reviews/EPIC_2_COMPLETION_REVIEW.md`](../reviews/EPIC_2_COMPLETION_REVIEW.md) | Epic 2 domain sign-off |
| [`docs/reviews/ARCHITECTURE_GUARDIAN_REVIEW_EPIC_2.md`](../reviews/ARCHITECTURE_GUARDIAN_REVIEW_EPIC_2.md) | Architecture readiness for Epic 3 |
| [`docs/TECHNICAL_DEBT_REGISTER.md`](../TECHNICAL_DEBT_REGISTER.md) | E2-PI / E2-PE / E2-PX residual roadmap |
| [`docs/ENGINEERING_CHARTER.md`](../ENGINEERING_CHARTER.md) | Trust and educational outcomes principles |
| [`CHANGELOG.md`](../../CHANGELOG.md) | v0.5.0 Educational Intelligence Platform release |
| [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md) | Product thesis: reduce decisions, increase learning |

---

*End of Epic 3 — Product Integration & Experience Blueprint.*

**STOP.** No implementation. No architecture redesign. No tests.
