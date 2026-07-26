# Educational Validation Framework (EVF)

**Programme:** Programme V — Educational Validation Framework  
**Status:** Active — permanent educational release governance  
**Classification:** Educational quality authority  
**Effective:** July 2026  
**Scope:** Documentation and governance only (no Runtime A integration in this milestone)

---

## Purpose

The Educational Validation Framework answers one question for every Kwalitec release:

> **Has Kwalitec demonstrated sufficient educational quality to justify releasing this version to students?**

EVF is the **official educational release approval process** from Version 1.0 onward.  
No educational feature is complete until it satisfies the Educational Release Gate.

**Version 1.0 target:** at least **80% educational trust**.

---

## What EVF is — and is not

| EVF is | EVF is not |
|---|---|
| Educational quality validation | Software architecture review |
| Release authority for educational trust | A replacement for Blind Review |
| Consumer of Blind Review and other evidence | A Runtime A decision engine |
| Explainable, evidence-driven governance | Opinion-only product preference |
| Independent of recommendation generation | A modifier of educational decisions |

EVF **evaluates** educational behaviour. It never **generates** or **mutates** Study Plans, Missions, Recovery Plans, recommendations, or Twin state.

---

## Relationship to sibling authorities

| Authority | Path | Question it answers |
|---|---|---|
| Educational Constitution (EGI-001) | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | What is educationally lawful? |
| Educational Governance Review (EGI-003) | `knowledge/educational/EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | Does this implementation tell the educational truth? |
| Blind Review subsystem | `knowledge/product/ep004_private_beta/reviewer_framework/` | How do independent student personas experience the product? |
| **Educational Validation Framework (EVF)** | `knowledge/educational_validation/` | **Is educational quality sufficient to release?** |
| Engineering / Architecture release | `knowledge/RELEASE_PLAYBOOK.md`, Architecture Constitution | Is it safe and structurally correct to ship? |

**Order of educational gates (conceptual):**

1. **Law** — Educational Constitution compliance  
2. **Integrity** — Educational Governance Review (EGI-003)  
3. **Quality** — Educational Validation Framework (this programme)  
4. **Ship** — Release Playbook / Protocol (engineering + educational gates cleared)

Blind Review remains a **mature research subsystem**. EVF consumes its outputs; it does not redefine its protocol, personas, or execution rules.

---

## Four validation layers

| Layer | Name | Primary artefact |
|---:|---|---|
| 1 | Educational Capability Validation | `CAPABILITY_VALIDATION_GUIDE.md` |
| 2 | Blind Comparative Review | `BLIND_COMPARATIVE_REVIEW.md` |
| 3 | Educational Quality Assessment | `EDUCATIONAL_DIMENSIONS.md` |
| 4 | Educational Release Gate | `EDUCATIONAL_RELEASE_GATE.md` |

---

## Document map

| Document | Role |
|---|---|
| [`EDUCATIONAL_VALIDATION_CONSTITUTION.md`](EDUCATIONAL_VALIDATION_CONSTITUTION.md) | Constitutional principles of educational validation |
| [`EDUCATIONAL_RELEASE_STANDARD.md`](EDUCATIONAL_RELEASE_STANDARD.md) | Version release bar (V1.0 and onward) |
| [`EDUCATIONAL_RELEASE_GATE.md`](EDUCATIONAL_RELEASE_GATE.md) | Official gate procedure and outcomes |
| [`CAPABILITY_VALIDATION_GUIDE.md`](CAPABILITY_VALIDATION_GUIDE.md) | Layer 1 — independent capability reviews |
| [`BLIND_COMPARATIVE_REVIEW.md`](BLIND_COMPARATIVE_REVIEW.md) | Layer 2 — blind comparison protocol |
| [`EDUCATIONAL_DIMENSIONS.md`](EDUCATIONAL_DIMENSIONS.md) | Layer 3 — permanent quality dimensions |
| [`EDUCATIONAL_BENCHMARKS.md`](EDUCATIONAL_BENCHMARKS.md) | Benchmark strategies and registration |
| [`VERSION_APPROVAL_WORKFLOW.md`](VERSION_APPROVAL_WORKFLOW.md) | End-to-end approval workflow |
| [`RELEASE_DECISION_TEMPLATE.md`](RELEASE_DECISION_TEMPLATE.md) | Official Version Approval Report template |
| [`REVIEWER_GUIDELINES.md`](REVIEWER_GUIDELINES.md) | How validators and comparative reviewers operate |

### Evidence folders

| Folder | Contents |
|---|---|
| [`capability_reviews/`](capability_reviews/) | Per-capability validation reports |
| [`benchmark_reviews/`](benchmark_reviews/) | Benchmark comparison records |
| [`reports/`](reports/) | Cross-cutting validation reports and working papers |
| [`release_reports/`](release_reports/) | Official Version Approval Reports (release artefacts) |

---

## Version 1 educational capabilities

Each capability is independently reviewable:

| ID | Capability | Student-facing trust focus |
|---|---|---|
| EC-01 | Master Planner | Study Plans |
| EC-02 | Daily Coach | Daily Missions / tonight’s study |
| EC-03 | Learning Coach | Educational explanations and coaching guidance |
| EC-04 | Recovery Coach | Recovery Plans after missed or failed study |
| EC-05 | Revision Coach | Revision Strategy |
| EC-06 | Exam Coach | Readiness Assessment / exam preparation |

---

## Hard constraints (Programme V)

- Do **not** integrate EVF into Runtime A in this framework milestone.
- Do **not** modify Blind Review protocol, personas, or execution rules.
- Do **not** use EVF to change recommendation generation.
- Do **not** approve a release on engineering success alone.
- Do **not** treat Blind Review meta-analysis as a silent bypass of the Release Gate.

---

## Quick start (release operators)

1. Read the [Educational Validation Constitution](EDUCATIONAL_VALIDATION_CONSTITUTION.md).  
2. Confirm the version against the [Educational Release Standard](EDUCATIONAL_RELEASE_STANDARD.md).  
3. Execute Layers 1–3 per the guides above (or reuse current evidence where still valid).  
4. Run the [Educational Release Gate](EDUCATIONAL_RELEASE_GATE.md).  
5. File the official report using [`RELEASE_DECISION_TEMPLATE.md`](RELEASE_DECISION_TEMPLATE.md) under `release_reports/`.

---

## Related programmes

| Programme | Relationship |
|---|---|
| EP-004 Blind Review | Evidence source for student experience and comparative preference |
| Educational Governance Initiative (EGI) | Prerequisite integrity / educational truth authority |
| EP-003 Educational Effectiveness | Historical effectiveness Go/No-Go; superseded for *release authority* by EVF |
| GA / Release Protocol | Operational and engineering ship criteria; complementary to EVF |
