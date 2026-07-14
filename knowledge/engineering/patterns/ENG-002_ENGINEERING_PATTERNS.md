# ============================================================================
# ENG-002
# ENGINEERING PATTERNS
# ============================================================================

**Document ID:** ENG-002

**Title:** Engineering Patterns

**Owner:** Architecture Office

**Status:** Version 1.0

**Classification:** Engineering Reference Standard

---

# Revision History

| Version | Date | Author | Notes |
|----------|------|--------|-------|
| 1.0 | Initial | Architecture Office | First Engineering Pattern Catalogue |

---

# Related Documents

Constitutional

- ENG-001 Engineering Handbook
- Product Blueprint
- Digital Twin Constitution

Supporting Standards

- ENG-003 Anti-Patterns
- ENG-004 Dependency Rules
- ENG-005 Naming Standard
- ENG-006 Logging Standard
- ENG-007 Testing Standard
- ENG-008 Review Checklist

---

# Purpose

This document defines the canonical engineering patterns used throughout Kwalitec.

Patterns describe proven engineering structures that may be reused across multiple capabilities.

Patterns exist to improve consistency.

Patterns should reduce architectural decision-making during implementation.

Patterns should never replace engineering judgement.

---

# Pattern Template

Every pattern in this document follows the same structure.

- Purpose
- Intent
- Responsibilities
- Non-Responsibilities
- Lifecycle
- Dependency Rules
- Collaboration
- Known Kwalitec Examples
- Common Mistakes
- Review Checklist

---

# ============================================================================
# Pattern 001
# Coordinator Pattern
# ============================================================================

## Purpose

Coordinate collaborators required to complete one application workflow.

---

## Intent

The Coordinator exists to orchestrate work.

It owns sequencing.

It owns workflow.

It owns operational coordination.

It deliberately owns no educational reasoning.

---

## Responsibilities

A Coordinator may:

- validate application inputs
- coordinate collaborators
- invoke strategies
- invoke repositories
- invoke providers
- invoke composers
- coordinate transactions
- coordinate workflow
- produce application results
- perform operational logging

---

## Non-Responsibilities

A Coordinator shall never:

- perform educational reasoning
- interpret educational evidence
- persist data directly
- compose Digital Twins
- calculate recommendations
- render HTML
- perform HTTP routing
- construct dependencies internally

---

## Lifecycle

```text
Receive Request

↓

Validate

↓

Coordinate Collaborators

↓

Collect Results

↓

Return Application Result
```

---

## Dependency Rules

Coordinator depends upon:

- Protocols
- Interfaces
- Domain contracts

Coordinator never depends directly upon:

- Flask
- SQLAlchemy models
- Templates
- Browser code

---

## Collaboration

Typical collaborators include:

- Strategy
- Repository
- Provider
- Composer
- Builder

The Coordinator never replaces collaborator responsibilities.

---

## Known Kwalitec Examples

- TwinUpdateCoordinator
- EducationalLearningLoop
- Future WeeklyReviewCoordinator

---

## Common Mistakes

❌ Performing educational reasoning.

❌ Constructing collaborators internally.

❌ Owning persistence.

❌ Becoming a "God Object."

❌ Returning framework objects.

---

## Review Checklist

Before approving a Coordinator verify:

- Single responsibility maintained.
- Workflow only.
- No educational policy.
- No persistence ownership.
- Dependencies injected.
- Logging operational only.

---

# ============================================================================
# Pattern 002
# Strategy Pattern
# ============================================================================

## Purpose

Encapsulate one area of educational or business reasoning.

---

## Intent

Strategies own decisions.

They do not own workflow.

---

## Responsibilities

Strategies may:

- analyse domain information
- evaluate policy
- apply educational rules
- produce domain outputs
- explain reasoning

---

## Non-Responsibilities

Strategies shall never:

- orchestrate workflows
- persist state
- invoke repositories
- invoke Flask
- assemble complete objects
- coordinate unrelated strategies

---

## Lifecycle

```text
Receive Domain Input

↓

Apply Domain Rules

↓

Produce Domain Output
```

---

## Dependency Rules

Strategies depend only upon:

- domain models
- value objects
- policies
- immutable inputs

---

## Known Kwalitec Examples

- KnowledgeUpdateStrategy

Future

- BehaviourUpdateStrategy
- PerformanceUpdateStrategy
- GoalUpdateStrategy

---

## Common Mistakes

❌ Repository access.

❌ HTTP access.

❌ Dashboard logic.

❌ Workflow coordination.

❌ Educational side effects outside owned domain.

---

## Review Checklist

Verify:

- reasoning isolated
- deterministic behaviour
- explainable output
- immutable inputs
- no orchestration
- no persistence

---

**END OF PART I**

---

# ============================================================================
# Pattern 003
# Repository Pattern
# ============================================================================

## Purpose

Provide the canonical persistence boundary between the Domain/Application Layers and Infrastructure.

The Repository Pattern exists to isolate persistence concerns from business behaviour.

---

## Intent

Repositories own persistence.

They translate between durable storage and domain objects.

Repositories do not make engineering or educational decisions.

---

## Responsibilities

A Repository may:

- persist aggregates
- retrieve aggregates
- replace immutable successors
- remove persisted entities
- query durable storage
- translate persistence concerns

---

## Non-Responsibilities

A Repository shall never:

- perform educational reasoning
- orchestrate workflows
- coordinate application services
- render presentation models
- perform HTTP operations
- calculate recommendations

---

## Lifecycle

```text
Receive Request

↓

Persist / Retrieve

↓

Return Domain Object
```

---

## Dependency Rules

Repositories depend upon:

- persistence technology
- infrastructure adapters
- storage engines

Repositories should expose domain-oriented contracts.

Consumers should never depend upon storage implementation.

---

## Collaboration

Typical collaborators:

- Coordinator
- Infrastructure
- Provider

Repositories should never invoke Strategies.

---

## Known Kwalitec Examples

- TwinRepository
- InMemoryTwinRepository

Future

- WeeklyReviewRepository
- EducationalFindingRepository

---

## Common Mistakes

❌ Performing orchestration

❌ Educational reasoning

❌ Returning ORM entities beyond infrastructure boundaries

❌ Business validation

❌ Hidden transactions

---

## Review Checklist

Verify:

- persistence only
- infrastructure isolated
- no domain reasoning
- contracts remain stable
- implementation replaceable

---

# ============================================================================
# Pattern 004
# Provider Pattern
# ============================================================================

## Purpose

Provide controlled retrieval of domain information without exposing persistence implementation.

---

## Intent

Providers retrieve.

They do not persist.

They do not reason.

They do not orchestrate.

---

## Responsibilities

Providers may:

- retrieve current aggregates
- retrieve historical aggregates
- retrieve projections
- validate retrieval success

---

## Non-Responsibilities

Providers shall never:

- update persisted state
- interpret educational evidence
- coordinate workflows
- assemble aggregates
- own caching policy unless explicitly assigned

---

## Lifecycle

```text
Receive Retrieval Request

↓

Retrieve Information

↓

Return Requested Object
```

---

## Dependency Rules

Providers depend upon:

- repositories
- retrieval contracts

Consumers depend upon Provider abstractions rather than storage implementations.

---

## Collaboration

Typical collaborators:

- Coordinator
- Repository
- Educational Intelligence

---

## Known Kwalitec Examples

- TwinProvider

Future

- WeeklyReviewProvider

---

## Common Mistakes

❌ Persistence ownership

❌ Educational reasoning

❌ Returning implementation-specific objects

❌ Hidden write operations

---

## Review Checklist

Verify:

- retrieval only
- no mutation
- abstraction preserved
- deterministic behaviour

---

# ============================================================================
# Pattern 005
# Composer Pattern
# ============================================================================

## Purpose

Assemble immutable aggregates from validated component outputs.

---

## Intent

A Composer owns structural assembly.

It never interprets meaning.

---

## Responsibilities

A Composer may:

- assemble immutable aggregates
- validate structural completeness
- replace supplied components
- preserve unchanged components

---

## Non-Responsibilities

A Composer shall never:

- perform educational reasoning
- orchestrate workflows
- retrieve persistence
- invoke repositories
- evaluate policies

---

## Lifecycle

```text
Receive Existing Aggregate

↓

Receive Component Outputs

↓

Assemble Successor Aggregate

↓

Return Immutable Aggregate
```

---

## Dependency Rules

Composers depend upon:

- immutable domain objects
- value objects
- validated outputs

They should not depend upon infrastructure.

---

## Collaboration

Typical collaborators:

- Coordinator
- Strategies

The Coordinator owns sequencing.

The Composer owns assembly.

---

## Known Kwalitec Examples

- TwinComposer

Future

- WeeklyReviewComposer

---

## Common Mistakes

❌ Educational reasoning

❌ Persistence

❌ Workflow ownership

❌ Mutable aggregate construction

❌ Side effects

---

## Review Checklist

Verify:

- assembly only
- immutable output
- no orchestration
- no persistence
- structural completeness

---

# Pattern Relationships

The following patterns frequently collaborate.

```text
Coordinator
      │
      ├─────────────┐
      │             │
      ▼             ▼
 Strategy       Repository
      │             │
      ▼             ▼
   Composer     Provider
```

Each pattern owns exactly one responsibility.

Engineering quality depends upon preserving these ownership boundaries.

---

**END OF PART II**

---

# ============================================================================
# Pattern 006
# Builder Pattern
# ============================================================================

## Purpose

Construct complex domain objects through a controlled and readable construction process.

Builders separate object construction from object behaviour.

---

## Intent

Builders exist to improve clarity whenever object construction becomes sufficiently complex that direct constructors reduce readability.

Builders own construction.

They do not own business behaviour.

---

## Responsibilities

A Builder may:

- collect construction inputs
- validate construction completeness
- create immutable objects
- provide sensible construction defaults where appropriate

---

## Non-Responsibilities

A Builder shall never:

- perform educational reasoning
- persist constructed objects
- coordinate workflows
- invoke repositories
- perform HTTP operations

---

## Lifecycle

```text
Receive Construction Inputs

↓

Validate Required Inputs

↓

Construct Immutable Object

↓

Return Completed Object
```

---

## Dependency Rules

Builders depend upon:

- domain contracts
- immutable value objects

Builders should not depend upon infrastructure.

---

## Known Kwalitec Examples

Future

- WeeklyReviewBuilder
- FounderDashboardBuilder

---

## Common Mistakes

❌ Business reasoning

❌ Hidden persistence

❌ Mutable partially-built objects escaping the Builder

---

## Review Checklist

Verify:

- construction only
- immutable output
- no orchestration
- no persistence

---

# ============================================================================
# Pattern 007
# Factory Pattern
# ============================================================================

## Purpose

Create families of related implementations while hiding construction details.

Factories simplify implementation selection.

---

## Intent

Factories choose implementations.

Factories do not own workflow.

---

## Responsibilities

Factories may:

- instantiate implementations
- encapsulate construction logic
- select implementation variants
- centralise object creation

---

## Non-Responsibilities

Factories shall never:

- perform educational reasoning
- coordinate application workflows
- persist information
- expose implementation selection to consumers

---

## Lifecycle

```text
Receive Construction Request

↓

Determine Implementation

↓

Construct Object

↓

Return Implementation
```

---

## Dependency Rules

Factories depend upon implementation registrations.

Consumers depend only upon factory contracts.

---

## Known Kwalitec Examples

Future

- LearningLoopFactory
- RecommendationFactory

---

## Common Mistakes

❌ Business logic inside factories

❌ Workflow ownership

❌ Returning framework-specific objects

---

## Review Checklist

Verify:

- construction only
- implementation selection isolated
- dependencies hidden

---

# ============================================================================
# Pattern 008
# Result Pattern
# ============================================================================

## Purpose

Represent the outcome of an engineering operation explicitly.

Result objects communicate success, failure and supporting information without relying upon exceptions for normal operational flow.

---

## Intent

Result objects improve readability and explicitness.

---

## Responsibilities

Result objects may contain:

- success indicator
- returned value
- failure information
- operational metadata

---

## Non-Responsibilities

Result objects shall never:

- perform behaviour
- own persistence
- contain workflow logic

---

## Lifecycle

```text
Operation Executes

↓

Result Created

↓

Returned To Caller
```

---

## Dependency Rules

Result objects should remain immutable.

---

## Known Kwalitec Examples

- TwinUpdateResult

Future

- WeeklyReviewResult

---

## Common Mistakes

❌ Mutable result state

❌ Hidden side effects

❌ Business logic inside results

---

## Review Checklist

Verify:

- immutable
- explicit success/failure
- behaviour-free

---

# ============================================================================
# Pattern 009
# Value Object Pattern
# ============================================================================

## Purpose

Represent immutable concepts defined entirely by their value rather than identity.

---

## Intent

Value Objects improve correctness, readability and domain modelling.

---

## Responsibilities

Value Objects may:

- encapsulate validation
- guarantee invariants
- expose immutable behaviour
- simplify equality

---

## Non-Responsibilities

Value Objects shall never:

- own persistence
- depend upon repositories
- perform orchestration
- expose mutable state

---

## Lifecycle

```text
Construction

↓

Validation

↓

Immutable Use

↓

Discard
```

---

## Dependency Rules

Value Objects should depend only upon primitive values and other Value Objects.

---

## Known Kwalitec Examples

Examples include identifiers, evidence references and immutable domain descriptors.

Future architectural evolution may introduce additional specialised Value Objects.

---

## Common Mistakes

❌ Mutable properties

❌ Identity semantics

❌ Infrastructure dependencies

---

## Review Checklist

Verify:

- immutable
- value equality
- encapsulated validation
- behaviour appropriate to represented concept

---

# Pattern Relationships

```text
Coordinator
      │
      ▼
 Strategy
      │
      ▼
 Result
      │
      ▼
 Composer
      ▲
      │
 Builder

Factory
   │
   ▼
Builder

Value Objects
     │
     └────────────► Used Throughout
```

Each pattern has one primary responsibility.

Patterns should collaborate.

Patterns should never absorb one another's responsibilities.

---

**END OF PART III**

---

# ============================================================================
# Pattern 010
# Protocol Pattern
# ============================================================================

## Purpose

Define stable behavioural contracts between collaborating components while allowing multiple interchangeable implementations.

Protocols establish architectural boundaries without prescribing implementation.

---

## Intent

Protocols separate dependency from implementation.

Consumers depend upon the contract.

Implementations satisfy the contract.

---

## Responsibilities

Protocols may:

- define required operations
- define behavioural expectations
- establish collaboration contracts
- enable dependency injection
- improve testability

---

## Non-Responsibilities

Protocols shall never:

- contain implementation
- contain business rules
- own persistence
- perform orchestration
- depend upon framework technology

---

## Lifecycle

```text
Architecture Defines Contract

↓

Implementation Satisfies Contract

↓

Consumers Depend Upon Contract
```

---

## Dependency Rules

Protocols belong at the architectural boundary between collaborators.

Implementations depend upon protocols.

Consumers depend upon protocols.

Protocols should never depend upon implementations.

---

## Collaboration

Typical collaborators include:

- Coordinators
- Strategies
- Repositories
- Providers
- Composers

Protocols make these collaborations replaceable.

---

## Known Kwalitec Examples

- TwinComposerProtocol
- TwinRepositoryProtocol
- TwinProviderProtocol
- TwinUpdateStrategyProtocol

---

## Common Mistakes

❌ Adding implementation.

❌ Depending upon concrete classes.

❌ Mixing infrastructure concerns into contracts.

❌ Expanding protocols beyond one responsibility.

---

## Review Checklist

Verify:

- contract only
- implementation-free
- stable abstraction
- single responsibility
- supports dependency injection

---

# ============================================================================
# Pattern 011
# Specification Pattern
# ============================================================================

## Purpose

Represent reusable business rules as composable objects that evaluate whether defined criteria are satisfied.

Specifications promote reusable decision logic.

---

## Intent

Specifications answer questions.

They do not perform actions.

---

## Responsibilities

Specifications may:

- evaluate domain conditions
- combine business rules
- compose logical expressions
- expose pass/fail outcomes

---

## Non-Responsibilities

Specifications shall never:

- persist information
- coordinate workflows
- modify aggregates
- perform educational reasoning outside their defined scope

---

## Lifecycle

```text
Receive Domain Object

↓

Evaluate Rule

↓

Return Boolean Result
```

---

## Dependency Rules

Specifications depend upon:

- domain models
- value objects
- immutable state

Specifications should remain free from infrastructure.

---

## Known Kwalitec Examples

Future candidates include:

- RecommendationEligibilitySpecification
- MissionAvailabilitySpecification
- RevisionReadinessSpecification

---

## Common Mistakes

❌ Hidden side effects.

❌ Repository access.

❌ Workflow ownership.

❌ State mutation.

---

## Review Checklist

Verify:

- read-only evaluation
- deterministic outcome
- reusable rule
- no side effects

---

# ============================================================================
# Pattern 012
# Policy Pattern
# ============================================================================

## Purpose

Capture long-lived organisational or educational rules governing system behaviour.

Policies define what the organisation has decided.

Strategies determine how those policies are applied.

---

## Intent

Policies represent organisational decisions rather than implementation techniques.

Policies should remain stable.

---

## Responsibilities

Policies may define:

- engineering rules
- educational rules
- organisational rules
- operational constraints

---

## Non-Responsibilities

Policies shall never:

- coordinate workflows
- persist information
- implement infrastructure
- replace strategies

---

## Lifecycle

```text
Organisation Defines Policy

↓

Policy Referenced

↓

Strategy Applies Policy
```

---

## Dependency Rules

Policies should be independent of implementation technology.

Strategies may depend upon policies.

Policies should not depend upon strategies.

---

## Known Kwalitec Examples

Examples include:

- Educational sufficiency rules
- Engineering constitutional principles
- Internal Alpha operational policies

---

## Common Mistakes

❌ Embedding implementation details.

❌ Frequent policy changes.

❌ Mixing organisational and technical concerns.

---

## Review Checklist

Verify:

- policy clearly expressed
- implementation independent
- organisational ownership explicit
- strategy remains separate

---

# ============================================================================
# Pattern Interaction Principles
# ============================================================================

The engineering patterns described throughout this document are intentionally complementary.

No pattern exists in isolation.

Correct engineering emerges from disciplined collaboration between patterns while preserving ownership boundaries.

General interaction guidelines include:

- Coordinators orchestrate.
- Strategies reason.
- Repositories persist.
- Providers retrieve.
- Composers assemble.
- Builders construct.
- Factories create implementations.
- Results communicate outcomes.
- Value Objects represent immutable concepts.
- Protocols define contracts.
- Specifications evaluate conditions.
- Policies establish organisational intent.

Patterns should collaborate.

Patterns should never absorb responsibilities belonging to another pattern.

---

**END OF PART IV**

---

# ============================================================================
# Pattern Selection Guide
# ============================================================================

The purpose of this section is to assist engineers in selecting the appropriate engineering pattern for a given responsibility.

Correct pattern selection reduces architectural drift and improves implementation consistency.

When multiple patterns appear applicable, engineers should first identify the single responsibility of the capability before selecting the corresponding pattern.

---

# Responsibility → Pattern Matrix

| Responsibility | Preferred Pattern |
|---------------|-------------------|
| Coordinate a workflow | Coordinator |
| Apply educational or business reasoning | Strategy |
| Persist aggregates | Repository |
| Retrieve aggregates | Provider |
| Assemble immutable aggregates | Composer |
| Construct complex objects | Builder |
| Select implementation | Factory |
| Return operation outcome | Result |
| Represent immutable concept | Value Object |
| Define behavioural contract | Protocol |
| Evaluate reusable rule | Specification |
| Express organisational rule | Policy |

---

# Pattern Selection Decision Tree

```text
Is the responsibility coordinating collaborators?

        │
       YES
        │
        ▼
Coordinator

        │
       NO
        │
        ▼

Is the responsibility making decisions?

        │
       YES
        │
        ▼
Strategy

        │
       NO
        │
        ▼

Is the responsibility persisting information?

        │
       YES
        │
        ▼
Repository

        │
       NO
        │
        ▼

Is the responsibility retrieving information?

        │
       YES
        │
        ▼
Provider

        │
       NO
        │
        ▼

Is the responsibility assembling an immutable aggregate?

        │
       YES
        │
        ▼
Composer

        │
       NO
        │
        ▼

Is the responsibility constructing a complex object?

        │
       YES
        │
        ▼
Builder

        │
       NO
        │
        ▼

Is the responsibility selecting an implementation?

        │
       YES
        │
        ▼
Factory

        │
       NO
        │
        ▼

Is the responsibility communicating an operation outcome?

        │
       YES
        │
        ▼
Result

        │
       NO
        │
        ▼

Is the responsibility representing an immutable concept?

        │
       YES
        │
        ▼
Value Object

        │
       NO
        │
        ▼

Is the responsibility defining a behavioural contract?

        │
       YES
        │
        ▼
Protocol

        │
       NO
        │
        ▼

Is the responsibility evaluating a reusable rule?

        │
       YES
        │
        ▼
Specification

        │
       NO
        │
        ▼

Is the responsibility expressing organisational policy?

        │
       YES
        │
        ▼
Policy
```

---

# Pattern Collaboration Matrix

| Pattern | Coordinates | Reasons | Persists | Retrieves | Assembles | Constructs |
|----------|------------|----------|-----------|------------|------------|------------|
| Coordinator | ✓ | — | — | — | — | — |
| Strategy | — | ✓ | — | — | — | — |
| Repository | — | — | ✓ | — | — | — |
| Provider | — | — | — | ✓ | — | — |
| Composer | — | — | — | — | ✓ | — |
| Builder | — | — | — | — | — | ✓ |
| Factory | Creates | — | — | — | — | Creates |
| Result | Reports | — | — | — | — | — |
| Value Object | Represents | — | — | — | — | — |
| Protocol | Defines | — | — | — | — | — |
| Specification | Evaluates | ✓ | — | — | — | — |
| Policy | Governs | ✓ | — | — | — | — |

No pattern should assume responsibilities assigned to another pattern.

---

# Pattern Review Questions

During Architecture Review, each implementation should be evaluated using the following questions.

## Coordinator

Does it coordinate rather than reason?

---

## Strategy

Does it reason rather than orchestrate?

---

## Repository

Does it persist rather than decide?

---

## Provider

Does it retrieve rather than mutate?

---

## Composer

Does it assemble rather than interpret?

---

## Builder

Does it construct rather than coordinate?

---

## Factory

Does it create rather than reason?

---

## Result

Does it communicate outcome without behaviour?

---

## Value Object

Is it immutable and identity-free?

---

## Protocol

Does it define behaviour without implementation?

---

## Specification

Does it evaluate rules without side effects?

---

## Policy

Does it define organisational intent independently of implementation?

---

# Pattern Evolution

Engineering patterns are expected to evolve more frequently than constitutional engineering doctrine.

New patterns may be introduced when recurring engineering structures demonstrate long-term value.

Existing patterns may be refined when implementation experience reveals superior engineering approaches.

Pattern evolution should preserve backwards architectural consistency whenever practical.

---

# Cross-Reference Matrix

| Pattern | Related Patterns |
|----------|------------------|
| Coordinator | Strategy, Repository, Provider, Composer |
| Strategy | Specification, Policy, Result |
| Repository | Provider, Protocol |
| Provider | Repository, Protocol |
| Composer | Builder, Result |
| Builder | Factory, Value Object |
| Factory | Builder, Protocol |
| Result | Coordinator, Strategy |
| Value Object | Builder, Specification |
| Protocol | All implementation patterns |
| Specification | Strategy, Policy |
| Policy | Strategy, Specification |

---

# Closing Statement

Engineering patterns provide the shared engineering vocabulary of Kwalitec.

They improve implementation consistency, simplify architectural reviews and reduce unnecessary design variation.

Patterns are not intended to constrain engineering creativity.

They exist to ensure that creativity strengthens rather than fragments the architecture.

Future engineering patterns should remain consistent with the constitutional principles established in ENG-001.

---

# End of Document

**Document ID:** ENG-002

**Title:** Engineering Patterns

**Version:** 1.0

**Status:** APPROVED FOR ENGINEERING REFERENCE

**Classification:** Engineering Reference Standard

---
