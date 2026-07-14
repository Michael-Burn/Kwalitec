# ============================================================================
# ENG-004
# ENGINEERING DEPENDENCY RULES
# ============================================================================

**Document ID:** ENG-004

**Title:** Engineering Dependency Rules

**Owner:** Architecture Office

**Status:** Version 1.0

**Classification:** Engineering Standard

---

# Revision History

| Version | Date | Author | Notes |
|----------|------|--------|-------|
| 1.0 | Initial | Architecture Office | First Engineering Dependency Standard |

---

# Related Documents

Constitutional

- Product Blueprint
- Digital Twin Constitution
- ENG-001 Engineering Handbook

Reference Standards

- ENG-002 Engineering Patterns
- ENG-003 Engineering Anti-Patterns

Supporting Standards

- ENG-005 Engineering Naming Standard
- ENG-006 Engineering Logging Standard
- ENG-007 Engineering Testing Standard
- ENG-008 Engineering Review Checklist

---

# Purpose

This document defines the dependency rules governing all engineering work within Kwalitec.

Dependencies determine how components collaborate.

Poor dependency management gradually destroys architecture.

Correct dependency management enables long-term maintainability, replaceability and independent evolution.

These rules are mandatory unless an Architecture Decision Record explicitly authorises an exception.

---

# ============================================================================
# PART I
# Dependency Philosophy
# ============================================================================

# Chapter 1

## Guiding Principle

Dependencies express architectural relationships.

Every dependency should communicate a legitimate ownership relationship.

Dependencies should never exist merely because they are convenient.

The direction of dependencies determines the direction of architectural influence.

---

# Chapter 2

## Engineering Objectives

Dependency management exists to achieve the following objectives.

- preserve architectural boundaries
- minimise coupling
- maximise cohesion
- enable testing
- improve replaceability
- simplify maintenance
- support independent evolution

Every dependency should improve one or more of these objectives.

---

# Chapter 3

## Stable Dependency Rule

Less stable components may depend upon more stable components.

More stable components should not depend upon less stable components.

Within Kwalitec:

```text
Engineering Standards

↑

Domain

↑

Application

↑

Presentation
```

Engineering knowledge influences implementation.

Implementation should not redefine engineering knowledge.

---

# Chapter 4

## Dependency Direction

Architectural dependencies should always point toward greater abstraction.

Preferred direction:

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Concrete implementations should remain replaceable.

Protocols should define collaboration boundaries.

---

# Chapter 5

## Explicit Dependencies

Dependencies should always be visible.

Hidden dependencies reduce understandability.

Every significant collaborator should appear in:

- constructor parameters
- dependency injection configuration
- explicit factory construction

Avoid implicit dependency discovery.

---

# Chapter 6

## Dependency Ownership

Every dependency should have a clearly identifiable owner.

Ownership answers:

- Who requested this collaboration?
- Why does it exist?
- Which component controls the interaction?

Dependencies without obvious ownership should be reconsidered.

---

# Chapter 7

## Dependency Lifetime

Dependencies should live no longer than necessary.

Prefer:

- immutable collaborators
- constructor injection
- scoped lifetime management

Avoid:

- global mutable dependencies
- shared hidden state
- long-lived singleton behaviour unless architecturally justified

---

# Chapter 8

## Architectural Independence

Business behaviour should remain independent of implementation technology.

Examples:

Educational reasoning should not depend upon Flask.

Domain rules should not depend upon SQLAlchemy.

Application workflows should not depend upon HTML rendering.

Architecture should make technology replaceable.

---

# Chapter 9

## Dependency Review Questions

Every new dependency should answer the following questions.

- Is this dependency necessary?
- Does it respect architectural layering?
- Does ownership remain clear?
- Can the dependency be replaced?
- Does it improve maintainability?
- Does it introduce coupling that could be avoided?

If these questions cannot be answered positively, the dependency should be reconsidered.

---

# Closing Statement — Part I

Architectural quality depends upon disciplined dependency management.

Dependencies should be introduced deliberately, reviewed carefully and maintained consistently throughout the lifetime of the software.

Every dependency should strengthen the architecture rather than weaken it.

---

**END OF PART I**

---

# ============================================================================
# PART II
# Layer Dependency Matrix
# ============================================================================

Part II defines the architectural dependency rules between the major layers of the Kwalitec platform.

These rules are mandatory.

Violations require explicit approval through an Architecture Decision Record (ADR).

---

# Chapter 10

## Architectural Layers

Kwalitec consists of four primary engineering layers.

```text
Presentation

↓

Application

↓

Domain

↓

Infrastructure
```

Each layer owns a distinct responsibility.

Dependencies exist to support those responsibilities—not to bypass them.

---

# Chapter 11

## Layer Responsibility Summary

| Layer | Primary Responsibility |
|--------|------------------------|
| Presentation | User interaction and external communication |
| Application | Workflow orchestration |
| Domain | Business and educational reasoning |
| Infrastructure | Technical implementation and persistence |

Responsibilities should remain exclusive.

No layer should duplicate another layer's purpose.

---

# Chapter 12

## Permitted Layer Dependencies

The following matrix defines permitted architectural dependencies.

| Consumer | Presentation | Application | Domain | Infrastructure |
|----------|:------------:|:-----------:|:------:|:--------------:|
| Presentation | ✓ | ✓ | ✗ | ✗ |
| Application | ✗ | ✓ | ✓ | ✓ |
| Domain | ✗ | ✗ | ✓ | ✗ |
| Infrastructure | ✗ | ✗ | ✓* | ✓ |

*Infrastructure may depend upon Domain contracts and models required to satisfy persistence or implementation responsibilities.

Infrastructure must not influence Domain behaviour.

---

# Chapter 13

## Prohibited Layer Dependencies

The following dependencies are prohibited.

### Domain → Presentation

The Domain must never know:

- HTTP
- Flask
- Templates
- Browser behaviour
- View models

---

### Domain → Application

Business rules must not depend upon workflow orchestration.

Application coordinates.

Domain reasons.

---

### Domain → Infrastructure

Domain behaviour must remain independent of:

- databases
- repositories
- messaging systems
- file systems
- framework technology

---

### Presentation → Infrastructure

Presentation should communicate through the Application Layer.

Direct persistence bypasses orchestration.

---

### Presentation → Domain

Presentation should not execute business behaviour directly.

All workflows should enter through the Application Layer.

---

# Chapter 14

## Dependency Matrix Interpretation

A permitted dependency does not imply that every component should collaborate directly.

Dependencies should be introduced only when they satisfy a legitimate architectural requirement.

Engineers should always prefer the smallest dependency graph capable of satisfying the current capability.

---

# Chapter 15

## Dependency Direction Examples

### Correct

```text
Presentation

↓

Application

↓

Strategy

↓

Domain
```

---

### Correct

```text
Coordinator

↓

Repository Protocol

↓

Repository Implementation
```

---

### Incorrect

```text
Strategy

↓

Repository
```

Reason:

Educational reasoning should not retrieve persistence directly.

The Coordinator owns orchestration.

---

### Incorrect

```text
Domain

↓

Flask
```

Reason:

Business behaviour becomes coupled to implementation technology.

---

### Incorrect

```text
Presentation

↓

SQLAlchemy
```

Reason:

Persistence bypasses the Application Layer.

---

# Chapter 16

## Cross-Layer Communication

Communication between layers should occur through well-defined interfaces.

Preferred mechanisms include:

- Protocols
- Immutable domain objects
- Value Objects
- Result Objects

Avoid exposing implementation-specific types across architectural boundaries.

---

# Chapter 17

## Layer Independence

Each layer should remain independently understandable.

Replacing one layer should require minimal change to neighbouring layers.

Examples include:

- replacing Flask
- replacing SQLAlchemy
- replacing PostgreSQL
- replacing UI technology

Business behaviour should remain unchanged during these replacements.

---

# Chapter 18

## Layer Review Checklist

During Architecture Review verify:

✓ Dependencies follow the approved direction.

✓ No prohibited imports exist.

✓ Layer responsibilities remain distinct.

✓ Framework technology remains isolated.

✓ Business behaviour remains independent.

✓ Dependency graph remains understandable.

Any violation should be resolved before approval.

---

# Closing Statement — Part II

Layered architecture succeeds only when dependency rules remain disciplined.

Every dependency crossing a layer boundary should strengthen architectural clarity rather than weaken it.

These rules provide the structural foundation upon which all future engineering capabilities are built.

---

**END OF PART II**

---

# ============================================================================
# PART III
# Component Dependency Rules
# ============================================================================

Part III establishes dependency rules for the major engineering components used throughout Kwalitec.

Where Part II governs architectural layers, this part governs collaboration between engineering patterns.

These rules are mandatory.

---

# Chapter 19

## Component Responsibility

Every engineering component exists to fulfil one clearly defined responsibility.

Dependencies should reinforce that responsibility rather than expand it.

Whenever a component begins depending upon collaborators outside its responsibility, architectural review should determine whether ownership has drifted.

---

# Chapter 20

## Coordinator Dependencies

### Permitted

A Coordinator may depend upon:

- Strategies
- Repositories
- Providers
- Composers
- Builders
- Result Objects
- Protocols
- Domain Models

---

### Prohibited

A Coordinator shall not depend directly upon:

- Flask request objects
- HTML templates
- SQLAlchemy sessions
- ORM entities
- Browser-specific logic

Presentation concerns belong to Presentation.

Infrastructure concerns belong to Infrastructure.

---

### Dependency Philosophy

The Coordinator owns orchestration.

It should know *who* performs work.

It should not know *how* collaborators implement their responsibilities.

---

# Chapter 21

## Strategy Dependencies

### Permitted

Strategies may depend upon:

- Domain Models
- Value Objects
- Policies
- Specifications
- Immutable inputs

---

### Prohibited

Strategies shall not depend upon:

- Repositories
- Providers
- Coordinators
- Flask
- SQLAlchemy
- File systems
- External APIs
- Messaging systems

---

### Dependency Philosophy

Strategies should be executable entirely in memory.

Given the same immutable inputs, a Strategy should always produce the same output.

---

# Chapter 22

## Repository Dependencies

### Permitted

Repositories may depend upon:

- persistence frameworks
- infrastructure adapters
- storage engines
- serialization utilities
- domain contracts

---

### Prohibited

Repositories shall not depend upon:

- Strategies
- Educational Intelligence
- Coordinators
- Presentation
- Recommendation engines

---

### Dependency Philosophy

Repositories translate between persistence and domain objects.

They remain behaviour-neutral.

---

# Chapter 23

## Provider Dependencies

### Permitted

Providers may depend upon:

- Repositories
- Repository Protocols
- Domain Models

---

### Prohibited

Providers shall not depend upon:

- Strategies
- Educational Intelligence
- Presentation
- Composers

---

### Dependency Philosophy

Providers retrieve.

They never modify.

They never interpret.

---

# Chapter 24

## Composer Dependencies

### Permitted

Composers may depend upon:

- immutable aggregates
- Value Objects
- Strategy outputs
- Builder outputs

---

### Prohibited

Composers shall not depend upon:

- Repositories
- Providers
- Flask
- SQLAlchemy
- Recommendation engines

---

### Dependency Philosophy

Composers assemble.

They never coordinate.

They never reason.

---

# Chapter 25

## Builder Dependencies

### Permitted

Builders may depend upon:

- Domain Models
- Value Objects
- Configuration Objects

---

### Prohibited

Builders shall not depend upon:

- Repositories
- Coordinators
- Strategies
- Providers

---

### Dependency Philosophy

Builders improve construction.

Construction should remain separate from behaviour.

---

# Chapter 26

## Factory Dependencies

### Permitted

Factories may depend upon:

- Protocol registrations
- Construction logic
- Configuration

---

### Prohibited

Factories shall not depend upon:

- educational reasoning
- persistence implementation details
- Presentation components

---

### Dependency Philosophy

Factories create implementations.

They do not own system behaviour.

---

# Chapter 27

## Value Object Dependencies

### Permitted

Value Objects may depend upon:

- primitive values
- other Value Objects

---

### Prohibited

Value Objects shall not depend upon:

- Repositories
- Strategies
- Coordinators
- Frameworks
- Infrastructure

---

### Dependency Philosophy

Value Objects should remain among the most stable engineering artefacts in the system.

---

# Chapter 28

## Protocol Dependencies

Protocols occupy the highest level of abstraction.

Protocols should depend upon nothing beyond stable language constructs.

Protocols should never depend upon implementations.

Implementations should depend upon Protocols.

---

# Chapter 29

## Component Dependency Matrix

| Consumer | Coordinator | Strategy | Repository | Provider | Composer | Builder | Factory | Protocol |
|-----------|:----------:|:--------:|:----------:|:--------:|:---------:|:-------:|:-------:|:--------:|
| Coordinator | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | ✓ |
| Strategy | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Repository | ✗ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✓ |
| Provider | ✗ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | ✓ |
| Composer | ✗ | ✓ | ✗ | ✗ | ✓ | ✓ | ✗ | ✓ |
| Builder | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✗ | ✓ |
| Factory | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ |

This matrix represents preferred architectural collaboration.

Deviations require explicit architectural justification.

---

# Chapter 30

## Component Review Checklist

During Architecture Review verify:

✓ Every dependency supports the component's responsibility.

✓ Dependencies remain directed toward appropriate abstractions.

✓ No prohibited collaborators exist.

✓ Educational reasoning remains isolated.

✓ Persistence remains isolated.

✓ Construction remains isolated.

✓ Assembly remains isolated.

✓ Workflow remains isolated.

When ownership and dependency direction align, architectural cohesion naturally follows.

---

# Closing Statement — Part III

Component dependencies define the operational structure of Kwalitec.

Correct dependency direction preserves ownership, simplifies maintenance and allows independent evolution of every engineering component.

These rules should guide both implementation and Architecture Review.

---

**END OF PART III**

---

# ============================================================================
# PART IV
# Protocol & Dependency Injection Rules
# ============================================================================

Part IV defines how dependencies are introduced, managed and satisfied throughout the Kwalitec platform.

Dependency Injection and Protocols work together to preserve architectural independence.

Protocols define collaboration.

Dependency Injection provides implementations.

The two concepts should never be separated.

---

# Chapter 31

## Protocol Philosophy

Protocols define architectural contracts.

A Protocol specifies:

- required behaviour
- collaboration expectations
- semantic meaning

A Protocol intentionally avoids:

- implementation
- framework knowledge
- persistence
- workflow

Protocols establish the stable boundary between collaborating components.

---

# Chapter 32

## Protocol Ownership

Every Protocol shall have exactly one architectural owner.

Ownership includes responsibility for:

- contract stability
- documentation
- version compatibility
- architectural intent

Implementations satisfy the Protocol.

They do not redefine it.

---

# Chapter 33

## Dependency Injection Philosophy

Dependency Injection exists to separate construction from behaviour.

Construction should occur once.

Business behaviour should occur many times.

These responsibilities should remain independent.

---

## Objectives

Dependency Injection improves:

- replaceability
- testability
- architectural clarity
- explicit dependencies
- implementation flexibility

---

# Chapter 34

## Constructor Injection

Constructor Injection is the preferred dependency injection mechanism throughout Kwalitec.

Example:

```text
Coordinator

↓

receives

↓

Strategy
Repository
Provider
Composer
```

Dependencies should be complete when construction finishes.

Objects should never require additional hidden collaborators before becoming operational.

---

## Prohibited Forms

Avoid:

- property injection
- setter injection
- runtime dependency lookup
- service locator
- hidden singleton retrieval

These techniques obscure architectural relationships.

---

# Chapter 35

## Composition Root

Dependency construction should occur in one clearly identifiable location.

Examples include:

- application factory
- composition module
- dependency bootstrap
- startup configuration

Business components should not construct collaborators.

---

## Benefits

A Composition Root provides:

- visible dependency graphs
- simpler testing
- deterministic construction
- improved architectural review

---

# Chapter 36

## Lifetime Management

Dependencies should have explicit lifetimes.

Preferred lifetimes include:

### Singleton

Only when architectural identity genuinely requires one shared instance.

Examples:

- immutable configuration
- application-wide registries

---

### Scoped

Preferred for application workflows.

Examples:

- Coordinators
- application services

---

### Transient

Preferred for stateless collaborators.

Examples:

- Builders
- Strategies
- Composers
- Specifications

Lifetime should reflect responsibility.

---

# Chapter 37

## Protocol Versioning

Protocols should evolve conservatively.

Minor implementation improvements should not require Protocol changes.

Protocol modification should occur only when:

- behavioural contracts evolve
- architectural responsibilities change
- collaboration semantics change

Breaking Protocol changes require Architecture Review.

---

# Chapter 38

## Testing with Protocols

Tests should depend upon Protocols wherever practical.

Preferred testing approaches include:

- fake implementations
- in-memory repositories
- deterministic providers
- lightweight test doubles

Tests should avoid unnecessary framework dependencies.

---

# Chapter 39

## Dependency Injection Review Checklist

During Architecture Review verify:

✓ Constructor Injection used.

✓ Collaborators explicit.

✓ Protocols define contracts.

✓ Implementations remain replaceable.

✓ No Service Locator.

✓ No hidden runtime lookup.

✓ Lifetime appropriate.

✓ Construction separated from behaviour.

---

# Chapter 40

## Dependency Injection Examples

### Preferred

```text
Application Startup

↓

Construct Repository

↓

Construct Provider

↓

Construct Strategy

↓

Construct Composer

↓

Construct Coordinator

↓

Execute Workflow
```

Construction occurs once.

Workflow executes repeatedly.

---

### Discouraged

```text
Coordinator

↓

Repository = ServiceLocator.get()

↓

Strategy = GlobalContainer.resolve()

↓

Provider = Registry.lookup()
```

This obscures architectural relationships and complicates testing.

---

# Closing Statement — Part IV

Protocols preserve architectural stability.

Dependency Injection preserves implementation flexibility.

Together they enable Kwalitec to evolve while maintaining explicit ownership, replaceable implementations and clear dependency relationships.

---

**END OF PART IV**

---

# ============================================================================
# PART V
# Architectural Exceptions & Enforcement
# ============================================================================

Part V defines how dependency rules are enforced, when exceptions may be granted and how architectural compliance is maintained throughout the lifetime of Kwalitec.

Dependency rules exist to preserve architectural integrity.

Exceptions exist only to support deliberate architectural evolution.

---

# Chapter 41

## Architectural Enforcement

Every engineering contribution shall be evaluated against the dependency rules established within this document.

Dependency validation should occur during:

- Engineering Design
- Implementation
- Architecture Review
- Release Review
- Major Refactoring

Dependency validation is a continuous engineering activity.

---

# Chapter 42

## Acceptable Exceptions

Exceptions to dependency rules are intentionally rare.

An exception may be approved only when all of the following conditions are satisfied:

- a legitimate architectural need exists
- no simpler alternative exists
- the exception improves long-term maintainability
- the exception is documented
- Architecture Office approval has been obtained

Convenience is never sufficient justification.

---

## Exception Approval

Every approved exception shall reference an Architecture Decision Record (ADR).

The ADR should describe:

- rationale
- affected components
- architectural impact
- expected duration
- review schedule

Undocumented exceptions are prohibited.

---

# Chapter 43

## Temporary Architectural Debt

Occasionally a capability may require temporary architectural compromise.

When this occurs:

- the compromise shall be documented
- the owner shall be identified
- a resolution strategy shall exist
- review shall occur during subsequent planning

Temporary debt should remain visible until resolved.

---

# Chapter 44

## Dependency Audits

The Architecture Office should periodically review dependency relationships across the codebase.

Typical audit objectives include:

- prohibited imports
- circular dependencies
- framework leakage
- protocol violations
- hidden collaborators
- dependency growth
- architectural consistency

Audit findings should inform future engineering priorities.

---

# Chapter 45

## Engineering Review Workflow

Dependency compliance should be evaluated using the following sequence.

```text
Implementation

↓

Static Review

↓

Architecture Review

↓

Dependency Validation

↓

Merge Approval

↓

Release Approval
```

Dependency violations identified during review should normally be corrected before merge.

---

# Chapter 46

## Architectural Drift

Architectural drift occurs when implementation gradually diverges from approved architectural principles.

Common causes include:

- repeated shortcuts
- unclear ownership
- hidden dependencies
- duplicated behaviour
- inconsistent implementation

Small instances of drift should be corrected promptly.

Architectural drift becomes increasingly expensive when ignored.

---

# Chapter 47

## Continuous Governance

Architecture governance is an ongoing engineering responsibility.

Its objectives include:

- preserving architectural integrity
- supporting safe evolution
- maintaining engineering consistency
- reducing unnecessary complexity

Governance should enable engineering rather than obstruct it.

---

# Chapter 48

## Dependency Compliance Matrix

| Requirement | Required |
|-------------|:--------:|
| Layer direction respected | ✓ |
| Protocols honoured | ✓ |
| Constructor Injection used | ✓ |
| Explicit collaborators | ✓ |
| No circular dependencies | ✓ |
| No framework leakage | ✓ |
| Replaceable implementations | ✓ |
| Clear ownership | ✓ |

Every Architecture Review should evaluate this matrix.

---

# Chapter 49

## Relationship to Other Standards

This document defines dependency rules only.

Additional engineering guidance is provided by:

- ENG-001 Engineering Handbook
- ENG-002 Engineering Patterns
- ENG-003 Engineering Anti-Patterns
- ENG-005 Engineering Naming Standard
- ENG-006 Engineering Logging Standard
- ENG-007 Engineering Testing Standard
- ENG-008 Engineering Review Checklist

These documents should be interpreted together.

---

# Chapter 50

## Long-Term Evolution

Dependency rules should evolve cautiously.

Stable dependency structures contribute significantly to software longevity.

Future revisions should favour clarification rather than frequent structural change.

Material changes should be approved through the Architecture Decision Record process.

---

# Closing Statement

Dependencies determine the structural integrity of every software system.

When dependencies remain disciplined:

- ownership remains clear
- components remain replaceable
- testing remains straightforward
- architecture remains understandable

The Engineering Dependency Rules therefore exist not to restrict engineering, but to preserve the long-term evolvability of Kwalitec.

---

# End of Document

**Document ID:** ENG-004

**Title:** Engineering Dependency Rules

**Version:** 1.0

**Status:** APPROVED FOR ENGINEERING STANDARD

**Classification:** Engineering Standard

---
