# Kwalitec Technical Debt Register

**Version:** v0.4.0

**Last Updated:** July 2026

**Status:** Active

---

# Purpose

This document records **intentional technical debt** within the Kwalitec codebase.

Technical debt differs from defects.

A defect is unintended incorrect behaviour.

Technical debt is an intentional engineering compromise accepted because the cost of immediate resolution exceeds the short-term value.

Every item recorded here should have:

- a clear description;
- business justification;
- engineering impact;
- priority;
- proposed resolution;
- target Epic or release.

This register shall be reviewed at the conclusion of every Epic.

---

# Priority Definitions

| Priority | Meaning |
|-----------|---------|
| Critical | Must be resolved before major production expansion. |
| High | Should be resolved within the next 1–2 Epics. |
| Medium | Improves maintainability but does not affect correctness. |
| Low | Desirable improvements with minimal operational impact. |

---

# Current Technical Debt

## TD-001 — SQLAlchemy 2.x Deprecations

**Priority:** High

**Category:** Framework Upgrade

### Description

Several services and tests still use legacy SQLAlchemy APIs.

Examples include:

- `Query.get()`
- legacy engine access patterns

### Impact

No immediate functional impact.

Future SQLAlchemy releases may remove compatibility.

### Justification

Deferred to avoid interrupting Curriculum Architecture work.

### Recommendation

Upgrade all code to SQLAlchemy 2.x APIs.

### Target

Maintenance Sprint after Epic 2.

---

## TD-002 — Large Route Modules

**Priority:** Medium

**Category:** Maintainability

### Description

Some blueprint route modules remain significantly larger than preferred.

Examples include:

- Study Plan routes

### Impact

Reduced readability.

More difficult code reviews.

### Recommendation

Split large route modules into feature-focused modules.

### Target

Future Architecture Improvement.

---

## TD-003 — Service Decomposition

**Priority:** Medium

**Category:** Architecture

### Description

Several services continue to grow as additional educational capabilities are introduced.

### Impact

Reduced cohesion over time.

### Recommendation

Continue decomposing services into narrowly focused domain services.

### Target

Epic 3+

---

## TD-004 — Remaining Lint Warnings

**Priority:** Medium

**Category:** Code Quality

### Description

A number of existing lint warnings remain outside the scope of Epic 1.

Examples include:

- formatting
- line length
- historical warnings

### Impact

No functional impact.

### Recommendation

Resolve incrementally during maintenance.

### Target

Ongoing.

---

## TD-005 — SQLAlchemy Warning Cleanup

**Priority:** High

**Category:** Framework Compatibility

### Description

Several SQLAlchemy warnings remain during test execution.

### Impact

Potential future compatibility issues.

### Recommendation

Remove deprecated patterns.

### Target

Maintenance Sprint.

---

## TD-006 — Architecture Guardian Findings

**Priority:** Medium

**Category:** Architecture

### Description

Architecture Guardian continues to report pre-existing issues including:

- large files
- business logic in routes
- dependency cycles

No new issues were introduced during Epic 1.

### Recommendation

Treat findings as architectural improvement work rather than release blockers.

### Target

Epic 3.

---

## TD-007 — Performance Optimisation

**Priority:** Low

**Category:** Performance

### Description

Curriculum queries currently prioritise correctness and clarity over optimisation.

### Impact

Negligible for current scale.

### Recommendation

Profile before optimising.

Introduce eager loading only where justified.

### Target

When supporting significantly larger curriculum libraries.

---

# Deferred Design Decisions

The following ideas were intentionally deferred because they do not yet provide sufficient educational value.

---

## Topic Progress at Learning Objective Level

**Status:** Deferred

Reason:

Topic-level progress provides the right balance between educational fidelity and usability.

---

## Graph-based Curriculum Relationships

**Status:** Deferred

Reason:

The canonical hierarchy is sufficient for current Educational Intelligence.

Prerequisite graphs may be introduced later without replacing the hierarchy.

---

## Section-weighted Recommendation Engine

**Status:** Deferred

Reason:

Depends on completion of Educational Intelligence.

Target:

Epic 2.

---

## Behaviour Analytics

**Status:** Deferred

Reason:

Requires Behaviour Engine.

Target:

Epic 2.

---

## Memory Scheduling

**Status:** Deferred

Reason:

Requires Memory Engine.

Target:

Epic 2.

---

# Debt Accepted During Epic 1

None.

All architectural compromises introduced during implementation were resolved before Epic completion.

---

# Review Process

At the completion of every Epic:

- Review each debt item.
- Update priority.
- Close resolved items.
- Add newly accepted debt.
- Remove completed entries.

No technical debt should remain undocumented.

---

# Summary

| Priority | Count |
|----------|------:|
| Critical | 0 |
| High | 3 |
| Medium | 4 |
| Low | 1 |

---

# Overall Assessment

The remaining technical debt is **manageable, intentional, and well understood**.

None of the current items prevent progression to Epic 2 or deployment of v0.4.0.

The architecture remains stable and maintainable.

Future work should prioritise Educational Intelligence while addressing framework modernisation during scheduled maintenance.

---

**Status:** Approved

**Next Review:** End of Epic 2
