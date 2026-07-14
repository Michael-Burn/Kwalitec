# ============================================================================
# ENG-003
# ENGINEERING ANTI-PATTERNS
# ============================================================================

**Document ID:** ENG-003

**Title:** Engineering Anti-Patterns

**Owner:** Architecture Office

**Status:** Version 1.0

**Classification:** Engineering Reference Standard

---

# Revision History

| Version | Date | Author | Notes |
|----------|------|--------|-------|
| 1.0 | Initial | Architecture Office | First Engineering Anti-Pattern Catalogue |

---

# Related Documents

Constitutional

- Product Blueprint
- Digital Twin Constitution
- ENG-001 Engineering Handbook

Supporting Standards

- ENG-002 Engineering Patterns
- ENG-004 Engineering Dependency Rules
- ENG-005 Engineering Naming Standard
- ENG-006 Engineering Logging Standard
- ENG-007 Engineering Testing Standard
- ENG-008 Engineering Review Checklist

---

# Purpose

This document catalogues engineering structures that Kwalitec intentionally rejects.

Anti-patterns are not simply "bad code."

They represent recurring architectural mistakes that weaken ownership, reduce maintainability, increase coupling or compromise educational integrity.

Every anti-pattern described herein has a corresponding preferred engineering pattern documented in ENG-002.

---

# Using This Document

Architecture Reviews should consult this document whenever implementation appears to violate established engineering doctrine.

Engineering teams should use this catalogue during implementation to recognise architectural drift before it reaches review.

This document is intended to complement ENG-002 rather than replace it.

---

# ============================================================================
# Anti-Pattern AP-001
# Fat Coordinator
# ============================================================================

## Summary

A Coordinator gradually accumulates responsibilities that belong to collaborating components until it becomes the centre of both workflow and business behaviour.

---

## Symptoms

Typical symptoms include:

- educational reasoning inside the Coordinator
- direct persistence logic
- object construction
- recommendation generation
- large conditional blocks
- rapidly increasing file size
- knowledge of multiple unrelated domains

---

## Why It Is Harmful

The Coordinator Pattern exists to orchestrate.

When it begins reasoning, persisting, assembling and validating simultaneously, it becomes difficult to understand, difficult to test and difficult to evolve.

The architecture loses clear ownership boundaries.

Future capabilities become increasingly expensive to implement.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 8 (Capability Engineering)
- ENG-001 Chapter 17 (Architecture Review Philosophy)
- ENG-002 Coordinator Pattern

---

## Correct Pattern

Move responsibilities to their proper owners.

Workflow remains inside the Coordinator.

Educational decisions belong to Strategies.

Persistence belongs to Repositories.

Assembly belongs to Composers.

Construction belongs to Builders.

---

## Detection

Indicators include:

- rapidly increasing Coordinator complexity
- collaborators becoming passive
- duplicated orchestration logic
- repeated domain calculations
- frequent architecture review comments

---

## Refactoring Strategy

1. Identify responsibilities.
2. Separate orchestration from reasoning.
3. Extract Strategies.
4. Extract Composers.
5. Extract Builders where appropriate.
6. Reduce Coordinator to workflow only.

---

## Review Questions

- Does this Coordinator make educational decisions?
- Does it perform persistence?
- Does it assemble aggregates?
- Could responsibilities be delegated?
- Would removing orchestration leave meaningful behaviour behind?

If the answer is yes, the Coordinator has likely become oversized.

---

# ============================================================================
# Anti-Pattern AP-002
# Smart Repository
# ============================================================================

## Summary

A Repository begins performing business or educational reasoning instead of remaining a persistence boundary.

---

## Symptoms

Examples include:

- calculating recommendations
- validating educational rules
- interpreting evidence
- selecting learning strategies
- computing readiness
- modifying domain behaviour during persistence

---

## Why It Is Harmful

Repositories exist to isolate persistence.

When they begin making decisions, persistence becomes tightly coupled to business policy.

Replacing storage technology becomes more difficult.

Testing becomes significantly more complicated.

Business logic becomes hidden inside infrastructure.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 7 (Layered Architecture)
- ENG-001 Chapter 9 (Dependency Doctrine)
- ENG-002 Repository Pattern

---

## Correct Pattern

Repositories persist.

Strategies reason.

Coordinators orchestrate.

Repositories should remain behaviour-neutral.

---

## Detection

Indicators include:

- Repository imports Strategy classes
- Repository evaluates educational rules
- Repository returns calculated recommendations
- Repository mutates domain behaviour

---

## Refactoring Strategy

1. Remove business logic.
2. Extract reasoning into Strategies.
3. Keep Repository contracts stable.
4. Preserve persistence ownership.

---

## Review Questions

- Is persistence the only responsibility?
- Would changing storage affect business behaviour?
- Does the Repository interpret educational meaning?

If not, architectural drift has occurred.

---

# Closing Statement — Part I

The first responsibility of Architecture Review is protecting ownership.

The Fat Coordinator and Smart Repository are the two most common architectural failures observed in layered systems.

Preventing them preserves engineering clarity throughout the lifetime of the product.

---

**END OF PART I**

---

# ============================================================================
# Anti-Pattern AP-003
# Leaky Strategy
# ============================================================================

## Summary

A Strategy extends beyond domain reasoning and begins orchestrating workflows, accessing infrastructure or managing persistence.

---

## Symptoms

Typical symptoms include:

- invoking repositories
- coordinating multiple collaborators
- constructing application services
- initiating HTTP requests
- performing logging beyond operational reasoning
- managing transactions

---

## Why It Is Harmful

Strategies exist to encapsulate domain reasoning.

When a Strategy begins orchestrating application behaviour it becomes tightly coupled to infrastructure and loses determinism.

Testing becomes more difficult.

Reasoning becomes less reusable.

Architectural ownership becomes unclear.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 7 (Layered Architecture)
- ENG-001 Chapter 8 (Ownership Doctrine)
- ENG-002 Strategy Pattern

---

## Correct Pattern

Strategies should:

- receive immutable inputs
- apply domain rules
- return immutable outputs

Workflow belongs to Coordinators.

Persistence belongs to Repositories.

Assembly belongs to Composers.

---

## Detection

Indicators include:

- repository dependencies
- provider dependencies
- transaction management
- orchestration logic
- framework imports
- mutable shared state

---

## Refactoring Strategy

1. Remove orchestration.
2. Inject all required inputs.
3. Return reasoning results only.
4. Move workflow into the Coordinator.
5. Move persistence into the Repository.

---

## Review Questions

- Does the Strategy coordinate anything?
- Does it retrieve or persist information?
- Does it depend upon infrastructure?
- Can the Strategy be executed entirely in memory?

If the final answer is no, the Strategy has leaked beyond its responsibility.

---

# ============================================================================
# Anti-Pattern AP-004
# Mutable Digital Twin
# ============================================================================

## Summary

An implementation directly modifies an existing Digital Twin instead of producing an immutable successor.

---

## Symptoms

Typical symptoms include:

- in-place mutation
- partial updates
- shared mutable state
- modifying nested structures
- side effects across references
- historical state disappearing

---

## Why It Is Harmful

The Digital Twin Constitution establishes immutable succession.

Mutating a Twin destroys historical traceability.

It makes debugging difficult.

It invalidates reasoning based upon historical evolution.

It weakens explainability.

---

## Constitutional Violation

Violates:

- Digital Twin Constitution
- ENG-001 Chapter 10 (Immutability Doctrine)
- ENG-002 Composer Pattern

---

## Correct Pattern

Current Twin

↓

Strategy Outputs

↓

Composer

↓

Successor Twin

↓

Repository Persistence

Existing Twins remain unchanged.

---

## Detection

Indicators include:

- mutable collections exposed publicly
- setters on Twin state
- in-place updates
- repository overwrite of existing object
- shared references between generations

---

## Refactoring Strategy

1. Remove mutable setters.
2. Introduce immutable construction.
3. Use Composer for successor assembly.
4. Preserve historical Twins.
5. Persist successors explicitly.

---

## Review Questions

- Does a previous Twin change after update?
- Can historical Twins be reconstructed?
- Are successor Twins newly created?
- Is history preserved?

Any negative answer indicates constitutional drift.

---

# ============================================================================
# Anti-Pattern AP-005
# Evidence Interpretation Outside Strategy
# ============================================================================

## Summary

Educational evidence is interpreted by components that do not own educational reasoning.

---

## Symptoms

Examples include:

- Coordinator interpreting assessment scores
- Repository inferring mastery
- Provider calculating readiness
- Composer evaluating educational meaning
- Presentation deciding learning state

---

## Why It Is Harmful

Educational interpretation is among the most important intellectual responsibilities in Kwalitec.

Duplicating or relocating that reasoning creates inconsistent educational behaviour.

Future policy changes become difficult.

Trust decreases.

---

## Constitutional Violation

Violates:

- Digital Twin Constitution
- Educational Intelligence Architecture
- ENG-001 Educational Integrity
- ENG-002 Strategy Pattern

---

## Correct Pattern

Educational observations flow through Strategies.

Other components transport educational information without interpreting it.

---

## Detection

Indicators include:

- conditional logic based on educational evidence
- recommendation calculations outside Strategies
- mastery inference outside Strategies
- educational terminology inside infrastructure

---

## Refactoring Strategy

1. Remove educational interpretation.
2. Pass observations unchanged.
3. Delegate reasoning to Strategy.
4. Preserve observational integrity.

---

## Review Questions

- Who interpreted the educational evidence?
- Is that component a Strategy?
- Could educational policy change without modifying this component?

If not, responsibility has leaked.

---

# Closing Statement — Part II

Strategies preserve educational integrity by owning educational reasoning exclusively.

Digital Twins preserve explainability by remaining immutable.

Observational evidence preserves trust by remaining uninterpreted until evaluated by the appropriate Strategy.

Together these principles form the core of Kwalitec's educational architecture.

---

**END OF PART II**

---

# ============================================================================
# Anti-Pattern AP-006
# Presentation Business Logic
# ============================================================================

## Summary

Presentation components begin performing business or educational reasoning instead of limiting themselves to interaction and presentation responsibilities.

---

## Symptoms

Typical symptoms include:

- educational calculations inside routes
- recommendation generation in controllers
- business rule evaluation in templates
- direct manipulation of domain objects
- persistence logic inside views
- complex conditional decision trees

---

## Why It Is Harmful

Presentation is responsible for communication.

Business behaviour belongs elsewhere.

When presentation owns business decisions:

- interfaces become difficult to maintain
- behaviour becomes duplicated
- testing becomes tightly coupled to the user interface
- changing interfaces risks changing business behaviour

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 7 (Layered Architecture)
- ENG-001 Chapter 8 (Ownership Doctrine)
- ENG-002 Coordinator Pattern
- ENG-002 Strategy Pattern

---

## Correct Pattern

Presentation should:

- receive requests
- validate input
- invoke application workflows
- render responses

Presentation should never determine educational outcomes.

---

## Detection

Indicators include:

- recommendation logic inside routes
- educational terminology inside templates
- domain calculations in controllers
- direct repository access
- duplicated business rules across pages

---

## Refactoring Strategy

1. Extract business behaviour.
2. Introduce Application coordination.
3. Move reasoning into Strategies.
4. Reduce Presentation to interaction responsibilities.

---

## Review Questions

- Can the interface change without changing business behaviour?
- Does Presentation calculate educational outcomes?
- Does Presentation know domain rules?

If not, ownership has leaked into the Presentation Layer.

---

# ============================================================================
# Anti-Pattern AP-007
# God Service
# ============================================================================

## Summary

A service gradually accumulates unrelated responsibilities until it becomes responsible for a substantial portion of the application.

---

## Symptoms

Typical symptoms include:

- hundreds of lines of unrelated logic
- numerous collaborators
- multiple business domains
- persistence ownership
- workflow ownership
- educational reasoning
- object construction

---

## Why It Is Harmful

Large services become difficult to understand.

Every change increases implementation risk.

Testing becomes increasingly expensive.

Refactoring becomes progressively more difficult.

Architecture gradually collapses into a single implementation centre.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 8 (Ownership Doctrine)
- ENG-001 Chapter 13 (Capability Doctrine)

---

## Correct Pattern

Split responsibilities according to ownership.

Introduce:

- Coordinators
- Strategies
- Builders
- Composers
- Repositories

Each should own one responsibility.

---

## Detection

Indicators include:

- continually growing class size
- increasing constructor dependencies
- unrelated methods
- changing for multiple independent reasons

---

## Refactoring Strategy

1. Identify cohesive responsibilities.
2. Extract components.
3. Introduce explicit ownership.
4. Preserve behaviour through tests.
5. Reduce service scope incrementally.

---

## Review Questions

- Why does this service change?
- How many independent responsibilities exist?
- Can responsibilities evolve independently?

If multiple independent answers exist, decomposition is required.

---

# ============================================================================
# Anti-Pattern AP-008
# Service Locator Dependency
# ============================================================================

## Summary

Components retrieve dependencies from a shared registry or global container instead of receiving them explicitly through construction.

---

## Symptoms

Examples include:

- global dependency container
- hidden service lookup
- runtime dependency discovery
- static dependency retrieval
- implicit collaborators

---

## Why It Is Harmful

Hidden dependencies obscure architecture.

Testing becomes harder.

Consumers appear independent while secretly depending upon external state.

Dependency graphs become difficult to understand.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 9 (Dependency Doctrine)
- ENG-001 Chapter 23 (Dependency Injection)
- ENG-002 Protocol Pattern

---

## Correct Pattern

Dependencies should be supplied explicitly.

Construction should reveal every collaborator required by the component.

---

## Detection

Indicators include:

- global container access
- static service retrieval
- dependency lookup inside methods
- hidden runtime configuration

---

## Refactoring Strategy

1. Replace service lookup with constructor injection.
2. Depend upon protocols.
3. Remove hidden dependencies.
4. Make collaborators explicit.

---

## Review Questions

- Are dependencies visible from the constructor?
- Could the component be instantiated without a global container?
- Does the dependency graph remain explicit?

If not, hidden dependency coupling exists.

---

# Closing Statement — Part III

Presentation exists to communicate.

Services exist to fulfil clearly defined responsibilities.

Dependencies should remain explicit rather than hidden.

Maintaining these boundaries preserves the layered architecture established throughout Kwalitec.

---

**END OF PART III**

---

# ============================================================================
# Anti-Pattern AP-009
# Circular Dependencies
# ============================================================================

## Summary

Two or more components depend upon each other directly or indirectly, preventing independent evolution and introducing architectural coupling.

---

## Symptoms

Typical symptoms include:

- Component A imports Component B while Component B imports Component A.
- Application depends upon Presentation.
- Domain depends upon Infrastructure.
- Strategies depending upon Coordinators.
- Repositories depending upon Services.

---

## Why It Is Harmful

Circular dependencies destroy layering.

Responsibilities become intertwined.

Components become difficult to test independently.

Refactoring becomes progressively more expensive.

Architectural boundaries become impossible to enforce.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 7 (Layered Architecture)
- ENG-001 Chapter 9 (Dependency Doctrine)
- ENG-002 Protocol Pattern

---

## Correct Pattern

Dependencies should always move in one direction.

When bidirectional collaboration appears necessary:

- introduce a Protocol
- introduce an Application Coordinator
- split responsibilities
- move shared behaviour into a common abstraction

---

## Detection

Indicators include:

- cyclic import graphs
- dependency inversion violations
- duplicated abstractions
- construction deadlocks

---

## Refactoring Strategy

1. Identify the dependency cycle.
2. Determine ownership.
3. Introduce abstraction where appropriate.
4. Break the cycle.
5. Re-run architectural dependency validation.

---

## Review Questions

- Does either component depend upon the other?
- Can either component be tested independently?
- Is dependency direction obvious?

Any cycle should be considered an architectural defect.

---

# ============================================================================
# Anti-Pattern AP-010
# Framework Leakage
# ============================================================================

## Summary

Framework-specific concepts spread beyond their architectural boundary and become embedded in business or educational logic.

---

## Symptoms

Examples include:

- Flask objects inside Domain
- ORM entities inside Strategies
- HTTP requests inside Repositories
- Template rendering inside Application
- Database sessions inside educational reasoning

---

## Why It Is Harmful

Frameworks evolve.

Business rules should not.

Framework leakage tightly couples engineering decisions to implementation technology.

Migration becomes difficult.

Testing becomes unnecessarily complex.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 7 (Layered Architecture)
- ENG-001 Chapter 9 (Dependency Doctrine)
- ENG-002 Protocol Pattern

---

## Correct Pattern

Framework technology should terminate at the appropriate architectural boundary.

Presentation owns web frameworks.

Infrastructure owns persistence frameworks.

Domain owns business behaviour.

---

## Detection

Indicators include:

- Flask imports outside Presentation
- SQLAlchemy models used directly by Domain
- infrastructure exceptions exposed publicly
- framework decorators within domain logic

---

## Refactoring Strategy

1. Isolate framework concerns.
2. Introduce Protocols.
3. Translate framework models into domain objects.
4. Restore architectural boundaries.

---

## Review Questions

- Could the framework be replaced without changing business behaviour?
- Does Domain know implementation technology?
- Are framework objects crossing architectural boundaries?

If yes, leakage has occurred.

---

# ============================================================================
# Anti-Pattern AP-011
# Primitive Obsession
# ============================================================================

## Summary

Domain concepts are represented by primitive values rather than meaningful domain objects.

---

## Symptoms

Examples include:

- raw strings representing identities
- integers representing complex state
- repeated validation logic
- duplicated formatting rules
- numerous related primitive parameters

---

## Why It Is Harmful

Primitive values communicate little meaning.

Validation becomes duplicated.

Invariants become difficult to enforce.

Engineering intent becomes unclear.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 10 (Immutability Doctrine)
- ENG-002 Value Object Pattern

---

## Correct Pattern

Encapsulate meaningful concepts within immutable Value Objects.

Value Objects preserve:

- validation
- invariants
- semantics
- readability

---

## Detection

Indicators include:

- repeated validation code
- repeated identifier parsing
- identical primitive parameter lists
- duplicated formatting logic

---

## Refactoring Strategy

1. Identify recurring primitives.
2. Introduce Value Objects.
3. Centralise validation.
4. Replace primitive parameters incrementally.

---

## Review Questions

- Is this primitive representing a domain concept?
- Is validation duplicated?
- Would a Value Object improve clarity?

If yes, Primitive Obsession may exist.

---

# Closing Statement — Part IV

Healthy architecture depends upon clear dependency direction, disciplined framework isolation and expressive domain modelling.

Preventing these anti-patterns protects Kwalitec from gradual architectural erosion while preserving long-term maintainability.

---

**END OF PART IV**

---

# ============================================================================
# Anti-Pattern AP-012
# Hidden Educational Reasoning
# ============================================================================

## Summary

Educational conclusions are produced outside explicitly designated educational reasoning components.

The implementation appears operational while silently making educational decisions.

---

## Symptoms

Examples include:

- recommendation scoring outside Educational Intelligence
- mastery calculations inside infrastructure
- readiness decisions inside application services
- dashboard components interpreting learning evidence
- persistence layer deriving educational conclusions

---

## Why It Is Harmful

Educational reasoning is one of Kwalitec's principal intellectual assets.

When reasoning becomes distributed:

- behaviour becomes inconsistent
- educational policy becomes difficult to evolve
- explainability decreases
- trust is weakened

---

## Constitutional Violation

Violates:

- Digital Twin Constitution
- Product Blueprint
- ENG-001 Chapter 4 (Educational Integrity)
- ENG-002 Strategy Pattern

---

## Correct Pattern

Educational observations may flow through multiple architectural layers.

Educational interpretation belongs exclusively to designated educational Strategies and Educational Intelligence components.

---

## Detection

Indicators include:

- educational terminology outside educational domains
- duplicated recommendation logic
- readiness calculations outside Strategy implementations
- conflicting educational outcomes

---

## Refactoring Strategy

1. Locate distributed educational logic.
2. Consolidate educational reasoning.
3. Preserve observational information.
4. Route interpretation through approved educational Strategies.
5. Remove duplicated educational decisions.

---

## Review Questions

- Which component reached the educational conclusion?
- Does that component own educational reasoning?
- Can educational policy evolve independently?

If not, educational reasoning has leaked.

---

# ============================================================================
# Anti-Pattern AP-013
# Premature Generalisation
# ============================================================================

## Summary

Implementation introduces abstractions for anticipated future requirements rather than demonstrated engineering needs.

---

## Symptoms

Typical symptoms include:

- unused extension points
- multiple implementations with one consumer
- generic frameworks solving hypothetical problems
- highly configurable components without current use
- abstraction layers without demonstrated benefit

---

## Why It Is Harmful

Premature abstraction increases complexity.

Future requirements rarely match speculation exactly.

Simple implementations are easier to evolve than unnecessary frameworks.

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 18 (Engineering Decision Making)

---

## Correct Pattern

Engineer for current architectural needs.

Generalise only after recurring implementation patterns emerge.

Abstractions should be justified by evidence.

---

## Detection

Indicators include:

- interfaces with one implementation and no foreseeable alternative
- configuration without consumers
- extensive unused extension hooks
- generic terminology replacing concrete domain language

---

## Refactoring Strategy

1. Remove speculative abstractions.
2. Simplify implementation.
3. Introduce abstraction only after recurring need.
4. Preserve architectural clarity.

---

## Review Questions

- What current requirement justifies this abstraction?
- Has this pattern already occurred more than once?
- Does the abstraction reduce current complexity?

If not, simplification should be preferred.

---

# ============================================================================
# Anti-Pattern AP-014
# Side-Effect Specification
# ============================================================================

## Summary

A Specification modifies application state while evaluating business rules.

---

## Symptoms

Examples include:

- database updates during evaluation
- logging business events
- modifying aggregates
- triggering workflows
- sending notifications

---

## Why It Is Harmful

Specifications exist to evaluate conditions.

Side effects make evaluation unpredictable.

Testing becomes more difficult.

Specifications lose composability.

---

## Constitutional Violation

Violates:

- ENG-002 Specification Pattern

---

## Correct Pattern

Specifications evaluate.

They do not mutate.

Actions resulting from satisfied Specifications belong elsewhere.

---

## Detection

Indicators include:

- repository calls
- mutations
- event publication
- state changes
- hidden persistence

---

## Refactoring Strategy

1. Remove side effects.
2. Return evaluation only.
3. Allow callers to decide subsequent actions.

---

## Review Questions

- Does evaluation change state?
- Could the Specification be executed repeatedly without changing behaviour?
- Is the result deterministic?

If not, side effects exist.

---

# ============================================================================
# Anti-Pattern AP-015
# Contract Drift
# ============================================================================

## Summary

Implementations gradually diverge from the Protocols or documented contracts they are intended to satisfy.

---

## Symptoms

Examples include:

- undocumented method behaviour
- optional parameters replacing explicit contracts
- inconsistent return semantics
- implementation-specific assumptions
- breaking changes without contract revision

---

## Why It Is Harmful

Protocols define architectural stability.

When implementations drift:

- substitution becomes unreliable
- testing assumptions fail
- engineering confidence decreases
- architectural consistency erodes

---

## Constitutional Violation

Violates:

- ENG-001 Chapter 9 (Dependency Doctrine)
- ENG-002 Protocol Pattern

---

## Correct Pattern

Protocols remain the authoritative behavioural contract.

Implementations evolve while preserving contractual compatibility.

Material contract changes require explicit architectural review.

---

## Detection

Indicators include:

- protocol methods ignored
- inconsistent implementations
- undocumented behavioural differences
- growing implementation-specific knowledge

---

## Refactoring Strategy

1. Compare implementation against protocol.
2. Restore contractual behaviour.
3. Update documentation where necessary.
4. Review architectural impact before changing contracts.

---

## Review Questions

- Does every implementation satisfy the documented contract?
- Would consumers observe behavioural differences?
- Has the protocol remained authoritative?

If not, contract drift has occurred.

---

# ============================================================================
# Architecture Review Matrix
# ============================================================================

During Architecture Review, every capability should be evaluated against this catalogue.

| Anti-Pattern | Primary Review Question |
|--------------|-------------------------|
| Fat Coordinator | Is workflow separated from reasoning? |
| Smart Repository | Does persistence remain behaviour-neutral? |
| Leaky Strategy | Is reasoning isolated from orchestration? |
| Mutable Digital Twin | Are successor Twins immutable? |
| Evidence Interpretation Outside Strategy | Who interpreted the educational evidence? |
| Presentation Business Logic | Does Presentation own interaction only? |
| God Service | Does every component have one responsibility? |
| Service Locator Dependency | Are dependencies explicit? |
| Circular Dependencies | Is dependency direction acyclic? |
| Framework Leakage | Are frameworks contained within their architectural layer? |
| Primitive Obsession | Should this concept be a Value Object? |
| Hidden Educational Reasoning | Does educational interpretation occur only in approved components? |
| Premature Generalisation | Is this abstraction justified today? |
| Side-Effect Specification | Does evaluation remain side-effect free? |
| Contract Drift | Does implementation still honour the Protocol? |

This matrix should be consulted during every Architecture Review.

---

# Relationship to ENG-002

Engineering Patterns describe the preferred architectural structures.

Engineering Anti-Patterns describe the recurring architectural failures those structures are intended to prevent.

Together they form complementary references:

- **ENG-002** answers: *What should we build?*
- **ENG-003** answers: *What must we avoid?*

Both documents should be consulted during implementation and Architecture Review.

---

# Closing Statement

Architectural quality is preserved not only by encouraging good patterns but also by recognising and eliminating recurring mistakes.

The anti-patterns documented herein represent structural risks that threaten ownership, clarity, educational integrity and long-term maintainability.

By identifying them early, Kwalitec protects its architecture from gradual erosion and preserves its ability to evolve safely over many years.

---

# End of Document

**Document ID:** ENG-003

**Title:** Engineering Anti-Patterns

**Version:** 1.0

**Status:** APPROVED FOR ENGINEERING REFERENCE

**Classification:** Engineering Reference Standard

---
