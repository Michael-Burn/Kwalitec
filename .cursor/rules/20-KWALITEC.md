# Kwalitec Product Knowledge

**Status:** Permanent Cursor governance  
**Canonical detail:** [`PROJECT_CONTEXT.md`](../../PROJECT_CONTEXT.md), [`docs/ARCHITECTURE_OVERVIEW.md`](../../docs/ARCHITECTURE_OVERVIEW.md), [`knowledge/version2/education/`](../../knowledge/version2/education/)

This document maps product concepts to architectural layers so agents know **what** each concept is and **where** it belongs.

---

## Mission

> **Reduce decisions. Increase learning.**

Kwalitec is an adaptive learning platform for demanding professional examinations. It answers *what to study next* deterministically from performance history, available time, and exam deadlines — not from opaque AI.

| Layer | Role |
|---|---|
| **Domain** | Educational meaning of missions, plans, and recommendations |
| **Application** | Use-case orchestration that assembles outputs for surfaces |
| **Presentation** | Copy and layout that communicates the next action |
| **Adapters** | HTTP routes that deliver pages and accept evidence |

---

## Core concepts

### Student Twin

**Canonical educational model of the learner.**

- **Package:** `domain.education.digital_twin` (`EducationalDigitalTwin`; alias `StudentTwin` in application code)
- **Layer:** Domain (model) · Application (ports for load/save) · Infrastructure (persistence via `twin_repository`)
- **Responsibility:** Holds provisional educational state — evidence-linked judgements, not presentation facts. All educational engines read twin context through authorised paths.
- **Rule:** Never bypass the twin. Never duplicate twin state in adapters or templates.

### Evidence

**Observable learning facts.**

- **Package:** `domain.education.evidence`
- **Layer:** Domain (specifications, records) · Application (`evidence_capture`, `evidence_update`) · Infrastructure (`evidence_repository`)
- **Responsibility:** Captures what happened (attempts, session outcomes, reflections). Evidence flows inward; speculation does not flow back as authority.

### Reflection

**Post-session learner self-report.**

- **Package:** `presentation.reflection`, `adapters.flask.reflection`
- **Layer:** Presentation (forms, view models) · Application (evidence capture) · Adapters (HTTP POST)
- **Responsibility:** Collects declarative reflection input and forwards it as evidence. Does not diagnose or recommend.

### Educational Pipeline

**End-to-end orchestrator of educational outputs.**

- **Package:** `application.pipeline` (`EducationalPipeline`)
- **Layer:** Application only
- **Responsibility:** Sequences stages — analyse evidence → mission → plan → progress → **recommendations** → explanation → student experience → optional AI enrichment. Delegates all decisions to domain engines.
- **Rule:** **Recommendations originate only here** (via `domain.recommendation.RecommendationGenerator`). No blueprint, service, or template may invent recommendations.

### Dashboard

**Student home — "what should I do next?"**

- **Package:** `presentation.dashboard`, `application.read_models.dashboard`, `adapters.flask.dashboard`
- **Layer:** Presentation + Application read models + Adapters
- **Responsibility:** Projects pipeline outputs into a calm, single-focus home. Displays; never authors educational decisions.

### Learning Session

**Active study episode.**

- **Package:** `presentation.study_session`, `application.session_runtime`, `application.evidence_capture`
- **Layer:** Application (runtime, outcome capture) · Presentation (workspace UI) · Adapters (`adapters.flask.session`)
- **Responsibility:** Runs a session, captures `LearningSessionOutcome`, feeds evidence back to the twin. Does not compute mastery independently.

### Study Strategy

**Teaching approach selection for a learning episode.**

- **Package:** `domain.education.teaching_strategy`
- **Layer:** Domain
- **Responsibility:** Deterministic strategy selection from diagnosis, priority, and intention. Owned entirely by the Educational Core — not by UI or analytics.

### Availability

**Declared weekly study capacity.**

- **Package:** `domain.onboarding` (`WeeklyAvailabilityPayload`)
- **Layer:** Domain (validation) · Application (`onboarding_service`) · Infrastructure (persistence)
- **Responsibility:** Stores weekday/weekend minutes and preferred session length. Feeds study planning; does not override pipeline recommendations directly.

### Confidence

**Self-reported confidence band at onboarding.**

- **Package:** `domain.onboarding` (`ConfidencePayload`, `ConfidenceBand`)
- **Layer:** Domain (declaration) · Application (onboarding orchestration)
- **Responsibility:** Captures learner self-assessment as initial evidence. Declaration only — not a mastery score.

### Exam History

**Prior sitting outcomes declared at onboarding.**

- **Package:** `domain.onboarding` (exam history step payloads)
- **Layer:** Domain · Application (`onboarding_service`)
- **Responsibility:** Seeds initial context for planning. Does not replace progress evaluation from live evidence.

### Onboarding

**First-run setup wizard.**

- **Package:** `domain.onboarding`, `application.onboarding`, `presentation.onboarding`, `adapters.flask.onboarding`
- **Layer:** Domain (step payloads, validation) · Application (orchestration, twin initialization) · Presentation (step UI) · Adapters (HTTP)
- **Responsibility:** Collects exam target, history, availability, and confidence; emits `StudentTwinInitializationRequest`. Initializes the twin via ports — does not run the full pipeline until evidence exists.

---

## Layer ownership summary

| Concept | Domain | Application | Infrastructure | Adapters | Presentation |
|---|---|---|---|---|---|
| Student Twin | ✓ model | ✓ ports | ✓ persist | — | — |
| Evidence | ✓ | ✓ capture/update | ✓ persist | — | — |
| Reflection | — | ✓ capture | — | ✓ HTTP | ✓ UI |
| Educational Pipeline | — | ✓ orchestrate | — | — | — |
| Recommendations | ✓ generate | ✓ sequence | — | — | ✓ display |
| Dashboard | — | ✓ read models | — | ✓ HTTP | ✓ UI |
| Learning Session | — | ✓ runtime | — | ✓ HTTP | ✓ UI |
| Study Strategy | ✓ | — | — | — | — |
| Availability | ✓ | ✓ onboarding | ✓ persist | ✓ HTTP | ✓ UI |
| Confidence | ✓ | ✓ onboarding | — | ✓ HTTP | ✓ UI |
| Exam History | ✓ | ✓ onboarding | — | ✓ HTTP | ✓ UI |
| Onboarding | ✓ | ✓ | ✓ persist | ✓ HTTP | ✓ UI |

---

## Recommendation authority (non-negotiable)

```
Evidence → Domain engines → Educational Pipeline → Read models → Presentation → Adapters
                ↑                      ↑
         RecommendationGenerator   orchestrates only
```

- `domain.recommendation` **generates** `RecommendationSpecification`.
- `application.pipeline.EducationalPipeline` **orchestrates** the stage.
- `infrastructure.ai` may **enrich wording** of already-decided recommendations.
- `domain.student_experience` may **present** completed outputs.
- **Nothing else** may create, rewrite, or prioritise educational recommendations.
