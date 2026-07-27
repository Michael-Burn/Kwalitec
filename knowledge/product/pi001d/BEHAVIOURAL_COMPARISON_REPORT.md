# PI-001D — Behavioural Comparison Report

**Programme:** PI-001D — Educational Platform Certification  
**Status:** Complete  
**Date:** 2026-07-27  

---

## Summary

This report documents where Runtime A and Runtime C behave equivalently, and where they intentionally differ.

The key certification rule is:

> Equivalent educational behaviour is required where Runtime C claims to replace educational truth.  
> Intentional differences are acceptable where Runtime C is explicitly coexistence-gated and not yet the production runtime.

---

## Equivalent behaviours

The following behaviours were certified as equivalent or sufficiently aligned:

| Behaviour | Runtime A | Runtime C | Status |
|---|---|---|---|
| Subject curriculum structure | Bundled JSON V2 curriculum | Published-package derivation | Equivalent |
| Topic ordering | Canonical engine order | Derived topological/published order | Equivalent |
| Section/topic/objective coverage | Existing curriculum tree | Derived artefact tree | Equivalent |
| Student journey starts at first topic | Study-plan progression starts from curriculum order | Plan instance starts from derived first topic | Equivalent |
| Mission generated per active learning topic | Daily learning mission from planner | Daily mission from template | Equivalent at current scope |
| Topic completion advances progress | Progress/lifecycle updates after completion | Event-sourced progress advances after completion | Equivalent at current scope |
| Syllabus completion ends learning traversal | No more learning topics remain | No more learning missions allowed | Equivalent |

---

## Intentional differences

### 1. Runtime ownership model

- **Runtime A:** production runtime for bundled subjects
- **Runtime C:** additive coexistence runtime for published subjects

This is intentional. PI-001D explicitly forbids cutover.

### 2. Progress persistence model

- **Runtime A:** mutable rows such as `TopicProgress`
- **Runtime C:** append-only educational events, with progress derived from the event stream

This is an intentional architectural difference, not a certification defect.

### 3. Study-plan shape

- **Runtime A:** exam-date-aware `StudyPlan` plus `WeekPlan` schedule
- **Runtime C:** deterministic topic-sequenced `RuntimeStudyPlanInstance`

Runtime C currently certifies educational traversal, not calendar planning parity.

### 4. Mission sophistication

- **Runtime A:** richer planning and mission logic, including broader lifecycle behaviour
- **Runtime C:** one deterministic mission template per current topic

This is acceptable for PI-001D because the milestone certifies end-to-end learning-cycle viability, not full planner replacement.

### 5. Readiness outputs

- **Runtime A:** full readiness intelligence calculation
- **Runtime C:** readiness inputs only

This is an intentional boundary. Runtime C currently feeds readiness-capable downstream systems but does not replace them.

### 6. Estimated Knowledge outputs

- **Runtime A:** broader learner-state ecosystem
- **Runtime C:** EK input DTOs with `has_estimated_knowledge=False` unless real evidence exists

This is safer than overclaiming mastery.

### 7. Production route integration

- **Runtime A:** reachable through live student flows
- **Runtime C:** application-service level and coexistence policy driven

This difference is intentional and required for safe certification before cutover.

---

## Behavioural non-defects

The following outcomes should **not** be treated as failures in PI-001D:

1. Runtime C lacking weekly plan rows
2. Runtime C refusing post-syllabus learning mission generation
3. Runtime C exposing readiness/EK inputs instead of final intelligence outputs
4. Runtime A and Runtime C using different persistence schemas
5. Runtime A remaining the default runtime for existing subjects

---

## Behavioural risks still open

1. **Student-facing cutover path not yet certified**  
   Runtime C works at service level, but live route-level discovery and navigation for founder-published subjects is not yet proven.

2. **Advanced planning parity not yet proven**  
   Runtime C has not yet demonstrated parity with Runtime A’s broader planning logic.

3. **Downstream readiness/recommendation integration not yet cut over**  
   Runtime C produces inputs, but the live student intelligence stack still depends on Runtime A-era services.

---

## Verdict

**Behavioural comparison verdict: PASS WITH DOCUMENTED DIFFERENCES.**

Runtime C behaves equivalently to Runtime A on the certified educational core:

- curriculum coverage
- ordered traversal
- mission-driven topic progression
- progress derivation
- syllabus completion

The remaining differences are intentional, documented, and compatible with PI-001D’s no-cutover constraint.
