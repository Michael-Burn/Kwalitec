# Engine Components

**Programme:** X — Workstream 2 — Constitutional Execution Architecture  
**Milestone:** MS001 — Constitutional Execution Engine Model  
**Classification:** Closed catalogue of recognised constitutional execution engine components  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **recognised constitutional execution engine components** (CEE-01…CEE-07).

It is subordinate to:

1. [`../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`](../educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md)
2. [`CONSTITUTIONAL_EXECUTION_ENGINE_MODEL.md`](CONSTITUTIONAL_EXECUTION_ENGINE_MODEL.md)
3. [`ENGINE_OBJECTIVES.md`](ENGINE_OBJECTIVES.md)
4. Programme VI corpora under [`../educational/`](../educational/)
5. Programme VII corpora under [`../orchestration/`](../orchestration/)
6. Programme VIII corpora under [`../runtime/`](../runtime/)
7. Programme IX corpora under [`../conformance/`](../conformance/), [`../verification/`](../verification/), [`../compliance/`](../compliance/), [`../certification/`](../certification/), and [`../evolution/`](../evolution/)
8. Programme X / WS1 corpora under [`../execution/`](../execution/)
9. EIP corpora (Evidence, Continuity, Explainability, State Authority Matrix, Knowledge & Mastery)

> **Only published execution engine components may perform constitutional execution against a completed execution context.  
> Unpublished “implied engine steps” are constitutionally defective.**

**Catalogue disambiguation:** CEE-01…CEE-07 here are *constitutional execution engine components*. They are not WS1 CECX / CECR / CECC catalogues, Programme VII educational / orchestration engines, Programme VIII runtime contracts (RC-xx), evidence categories (EC-xx), evidence validation categories (EV-xx), or Programme IX conformance / verification / compliance / certification / evolution types.

---

## 1. Purpose

Execution without a closed engine catalogue invents law by proximity: whichever services, queues, or “ambient” product steps happen to run become the tutor’s “proof the system marked the script.”

This catalogue names the only lawful constitutional execution engine components a run may apply — and binds each component to constitutional purpose, inputs, outputs, and permitted / prohibited responsibilities.

---

## 2. Catalogue Overview

| ID | Component | Constitutional purpose (short) | Primary inputs | Primary outputs |
|----|-----------|--------------------------------|----------------|-----------------|
| **CEE-01** | Rule Dispatcher | Select and order published constitutional rules for the completed context | Completed context + published rule identities | Dispatch plan (rules to execute; not new law) |
| **CEE-02** | Rule Executor | Apply published constitutional rules exactly as published | Dispatch plan + completed context | Rule-application traces / interim results |
| **CEE-03** | Constraint Evaluator | Evaluate hard constitutional constraints preserved in the context | Completed constraints + interim results | Constraint-evaluation records |
| **CEE-04** | Outcome Collector | Assemble reconstructable execution outcomes | Rule traces + constraint records | Execution outcome set |
| **CEE-05** | Execution State Manager | Maintain speakable execution-state transitions for the run | Component progress signals | Execution-state record (not educational / governance state) |
| **CEE-06** | Exception Coordinator | Coordinate lawful stops, refusals, and boundary violations | Exception signals + published boundaries | Exception disposition (stop / escalate / record) |
| **CEE-07** | Execution Publisher | Publish execution outcomes for downstream decision architecture | Outcome set + state / exception records | Published execution outcomes (not seals or amendments) |

Material constitutional execution must map to one or more of these components as published law requires. Cross-cutting situations may bind multiple CEE components; none may invent a component outside this catalogue.

**Relation to WS1:** CECX / CECR / CECC prepare, resolve, and complete context. CEE consumes only completed context; it never redefines preparation catalogues.

**Relation to Programme VIII / IX catalogues:** Those catalogues remain defined solely by Programmes VIII / IX. CEE may *execute published rules that reference* their identities; it does not replace, re-run, or reclassify them.

**Relation to educational quality:** No CEE component judges whether learning was good, whether a tip was wise, or whether the student is ready. Execution ≠ quality. Execution outcome ≠ compliance or certification.

---

## 3. CEE-01 — Rule Dispatcher

### Constitutional purpose

Identify, select, and lawfully order the **published constitutional rules** that the completed execution context makes available for this execution — so the engine knows *which rules to apply* and *in what published order* without inventing rules or soft-amending specifications.

### Constitutional inputs

- Completed resolved execution context (WS1 / MS003 fulfilment confirmed).
- Named published rule identities / specification clauses assembled under CECX / CECR for the execution identity.
- Published scope, assumptions, and constraints relevant to dispatch.
- Published CEEO-01 / CEEO-05 expectations.

### Constitutional outputs

- Dispatch plan: ordered set of published rule identities to execute (references only).
- Explicit exclusion of unpublished customs from the dispatch plan.
- Honest refuse when required published rules cannot be identified without invention.

### Permitted responsibilities

- Select published rules named in the completed context.
- Order rules according to published composition / precedence already stated in constitutional corpora.
- Record which rules were selected and which were out of scope under the completed context.
- Refuse dispatch when the context is incomplete or rules are unpublished.

### Prohibited responsibilities

- Invent unpublished rules or “implied house rules.”
- Soft-amend specification text to make dispatch convenient.
- Reorder rules contrary to published precedence to force a preferred outcome.
- Dispatch Programme IX judgement production (compliance, certification, verification) as if it were engine rule authorship.
- Begin dispatch against an incomplete execution context.

---

## 4. CEE-02 — Rule Executor

### Constitutional purpose

**Apply** the dispatched published constitutional rules against the completed execution context **exactly as published** — so constitutional execution occurs without independent reinterpretation, specification amendment, or governance determination.

### Constitutional inputs

- Dispatch plan from CEE-01.
- Completed execution context (authority, EIP references, specifications, governance artefacts as information, identity, scope, assumptions, constraints).
- Published CEEO-01 / CEEO-02 / CEEO-05 expectations.

### Constitutional outputs

- Rule-application traces: which rule identities were applied, against which context elements, with what reconstructable interim results.
- Honest stop / hand-off to CEE-06 when a rule cannot be applied without invention or amendment.
- Explicit non-claim: application is not compliance determination, certification, or EIP replacement.

### Permitted responsibilities

- Apply published rules as cited.
- Record reconstructable application traces for each material rule.
- Honour EIP principles referenced in the completed context without rewriting them.
- Compose with CEE-03 when a rule application requires constraint evaluation.

### Prohibited responsibilities

- Independently interpret constitutional law into new meaning.
- Replace Educational Interpretation Principles mid-execution.
- Amend constitutional specifications under “clarification” pretext.
- Determine conformance, verification, compliance, certification, or evolution dispositions.
- Mint recommendations, invent educational state, or rewrite Programme VI / VII warrants.
- Treat Twin / Adaptive / analytics narratives as rule outcomes.

---

## 5. CEE-03 — Constraint Evaluator

### Constitutional purpose

**Evaluate** the hard constitutional constraints preserved in the completed execution context (and any constraints published for the engine itself) — so boundaries remain intact, speakable, and enforceable during execution.

### Constitutional inputs

- Explicit constraint set from the completed context (CECX-07 and related).
- Published engine boundaries ([`ENGINE_BOUNDARIES.md`](ENGINE_BOUNDARIES.md)).
- Interim rule-application traces from CEE-02 (as needed for constraint checking).
- Published CEEO-05 expectations.

### Constitutional outputs

- Constraint-evaluation records: which constraints were evaluated, whether they held, and what boundary-preserving action followed.
- Signals to CEE-06 when a constraint would be violated by continued execution.
- Explicit confirmation that constraints were not waived.

### Permitted responsibilities

- Evaluate published hard stops (no amendment, no EIP replacement, no compliance determination, no certification, no authority substitution, no stack freeze, and concern-specific published constraints).
- Record held / would-be-violated statuses reconstructably.
- Trigger lawful stop or escalation when continued execution would breach a constraint.

### Prohibited responsibilities

- Soft-waive constraints for demos, deadlines, or preferred outcomes.
- Invent emergency exemptions that mint amendment power.
- Rewrite constraints to match a preferred implementation result.
- Treat constraint evaluation as a Programme IX compliance determination.
- Silence material constraints that published law requires to be explicit.

---

## 6. CEE-04 — Outcome Collector

### Constitutional purpose

**Assemble** reconstructable **execution outcomes** from rule-application traces and constraint-evaluation records — so downstream decision architecture receives honest execution results without mistaking them for governance seals or constitutional amendments.

### Constitutional inputs

- Rule-application traces (CEE-02).
- Constraint-evaluation records (CEE-03).
- Execution-state and exception records as available (CEE-05 / CEE-06).
- Published CEEO-03 / CEEO-04 expectations.

### Constitutional outputs

- Execution outcome set: reconstructable results of lawful constitutional execution for the execution identity.
- Explicit classification of outcomes as *execution outcomes* (not compliance, certification, or law change).
- Honest incomplete / refused outcome set when collection cannot proceed without invention.

### Permitted responsibilities

- Collect and structure outcomes from published component traces.
- Preserve linkage from each outcome to rule identities, constraint records, and completed-context identity.
- Distinguish successful application, lawful refuse, and exception-stopped outcomes.
- Prepare outcomes for publication under CEE-07.

### Prohibited responsibilities

- Upgrade outcomes into conformance findings, verification findings, compliance determinations, or certifications.
- Erase inconvenient traces to simplify the outcome set.
- Invent outcomes not grounded in CEE-02 / CEEO-03 records.
- Present educational quality, mastery, or readiness scores as constitutional execution outcomes.
- Soft-amend specifications by encoding new law inside “outcome notes.”

---

## 7. CEE-05 — Execution State Manager

### Constitutional purpose

Maintain a **speakable execution-state record** for the constitutional run — transitions among recognised engine progress points — so audit and explanation can say *where execution stood*, without inventing educational state or governance dispositions.

### Constitutional inputs

- Progress signals from CEE-01…CEE-04 and CEE-06 / CEE-07.
- Completed-context execution identity (CECX-05).
- Published CEEO-02 / CEEO-03 / CEEO-04 expectations.

### Constitutional outputs

- Execution-state record: ordered transitions (for example dispatched → executing → constraints evaluated → outcomes collected → published / refused / exception-stopped).
- Binding of state transitions to reconstructable component events.
- Explicit non-claim: execution state is not educational state (EIP-001) and not a Programme IX disposition.

### Permitted responsibilities

- Record lawful engine progress transitions.
- Preserve continuity of state history for the execution identity (EIP-005).
- Make state transitions available to explainability contracts (CEEEQ-04).
- Halt further progress when CEE-06 requires stop / escalate.

### Prohibited responsibilities

- Invent educational state, mastery state, or student journey state under engine pretext.
- Encode compliance / certification / verification dispositions as “execution state.”
- Silently mutate or erase prior lawful state history.
- Use stack process state, CI job state, or UI wizard steps as constitutional execution state without mapping to this component’s record.
- Treat state transition itself as constitutional amendment.

---

## 8. CEE-06 — Exception Coordinator

### Constitutional purpose

**Coordinate lawful exceptions** — incomplete context, unpublished rules, constraint violations, non-determinism defects, and related hard stops — so execution refuses or escalates honestly without minting new law, waiving boundaries, or fabricating outcomes.

### Constitutional inputs

- Exception signals from CEE-01…CEE-05 (and prerequisite WS1 completion failures when surfaced).
- Published boundaries ([`ENGINE_BOUNDARIES.md`](ENGINE_BOUNDARIES.md)) and completed-context constraints.
- Published CEEO-01 / CEEO-05 expectations.

### Constitutional outputs

- Exception disposition: stop / escalate / record (as published law permits).
- Reconstructable exception record naming cause, component, and preserved boundaries.
- Hand-off to CEE-04 / CEE-07 for honest incomplete or refused publication where lawful.

### Permitted responsibilities

- Stop execution when completed context is absent or defective.
- Stop or escalate when unpublished rules would be required.
- Stop or escalate when continued execution would violate constraints.
- Record exceptions reconstructably for explainability and audit.
- Prefer honest refuse over improvisation.

### Prohibited responsibilities

- Soft-waive exceptions for delivery urgency.
- Mint constitutional amendments, EIP replacements, or governance dispositions as “exception resolutions.”
- Swallow exceptions silently so outcomes appear complete.
- Convert exceptions into certifications or compliance passes.
- Invent unpublished exception categories that expand engine authority.

---

## 9. CEE-07 — Execution Publisher

### Constitutional purpose

**Publish** the collected execution outcomes (and associated state / exception records) so **downstream decision architecture** may lawfully consume them — without presenting publication as certification, compliance, stack freeze, or constitutional amendment.

### Constitutional inputs

- Execution outcome set (CEE-04).
- Execution-state record (CEE-05).
- Exception dispositions / records (CEE-06) when material.
- Published CEEO-03 / CEEO-04 / CEEO-05 expectations.

### Constitutional outputs

- Published execution outcomes bound to execution identity and completed-context identity.
- Explicit audience-honest publication markers (available for downstream consumption; not a seal of conformity).
- Reconstructable publication record for audit and explainability.

### Permitted responsibilities

- Publish reconstructable outcomes to lawful downstream consumers.
- Preserve linkage to rules executed, constraints evaluated, state transitions, and boundaries intact.
- Publish honest refuse / incomplete dispositions when execution did not complete.
- Remain implementation-neutral in publication meaning (no stack privilege).

### Prohibited responsibilities

- Present publication as certification, compliance determination, verification finding, or conformance seal.
- Amend constitutional specifications by publishing “corrected” law.
- Replace EIP under publication pretext.
- Freeze Runtime A / Twin / Adaptive / CI as constitutional authority because outcomes were published there.
- Erase publication history contrary to continuity (EIP-005).
- Publish outcomes for incomplete contexts as if preparation had completed.

---

## 10. Composition Rules

1. **Closed catalogue.** Only CEE-01…CEE-07 may perform constitutional execution engine responsibilities.
2. **Completed context before dispatch.** CEE-01 must not dispatch against incomplete WS1 preparation.
3. **Dispatch before execute.** CEE-02 applies only rules selected under CEE-01.
4. **Constraints are not optional.** Material runs evaluate constraints under CEE-03; waivers are unlawful.
5. **Outcomes are collected, not invented.** CEE-04 assembles from traces; it does not fabricate results.
6. **State is engine progress only.** CEE-05 never becomes educational or governance state.
7. **Exceptions preserve boundaries.** CEE-06 stops or escalates; it never amends law.
8. **Publication is not legislation.** CEE-07 publishes execution outcomes; it never certifies or amends.
9. **Consistency across components.** Contradictions among CEE-01…CEE-07 yield refuse / exception disposition (CEEO-01 / CEEO-05).
10. **Cross-cutting binding.** Multiple components may bind together; none may invent an off-catalogue component.

---

## 11. Status

APPROVED — governing for constitutional execution engine components (documentation only).
