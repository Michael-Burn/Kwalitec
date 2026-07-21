# Kwalitec Anti-Patterns

**Status:** Permanent Cursor governance  
**Authority:** Binding for all implementation work

When in doubt, check this list before writing code. Each item exists because it has caused or would cause architectural drift.

---

## Educational authority

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **Duplicate Educational Pipeline logic** | Creates divergent educational outcomes | Call `EducationalPipeline` or the relevant domain engine |
| **Compute mastery outside Educational Pipeline** | Bypasses evidence-first reasoning | Delegate to `domain.progress_evaluation` via pipeline |
| **Create educational recommendations outside Pipeline** | Breaks single recommendation authority | Route through `application.pipeline` → `domain.recommendation` |
| **Bypass Student Twin** | Fragments learner state | Read/write twin through authorised ports and UoW |
| **Duplicate business rules** | Rules drift across layers | One rule, one domain module |
| **Create new domain concepts without architectural justification** | Bloats the educational model | Propose ADR or extend existing aggregates |

---

## Layer violations

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **Place Flask outside adapters** | Couples HTTP to business logic | `src/adapters/flask/` or legacy `app/` blueprints only |
| **Place SQLAlchemy outside infrastructure** | Couples persistence to domain | `src/infrastructure/persistence/` only |
| **Place HTML outside presentation/adapters** | Scatters rendering | Templates in `adapters.flask.rendering/templates/` or `app/templates/`; view models in `presentation/` |
| **Introduce framework dependencies into Domain** | Breaks testability and portability | Keep domain pure Python |
| **Introduce persistence into Application** | Breaks dependency inversion | Use ports; inject repositories at composition root |
| **Introduce presentation logic into Domain** | Mixes authority with display | Project in presentation layer |

---

## Design violations

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **Hardcode design tokens** | Breaks theming and consistency | `presentation.design_system` tokens or CSS variables |
| **Hardcode colours or spacing** | Same | `colour()`, `space()`, `--brand-*`, `--student-space-*` |
| **Multiple competing CTAs** | Violates single-focus UX | One primary action per screen |
| **Gamification chrome** | Violates calm professional feel | Purposeful, explainable UI only |

---

## Engineering violations

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **God routes or god services** | Untestable, unmaintainable | Small modules per concern |
| **Swallow exceptions** | Hides failures | Log and fail explicitly |
| **Return `None` where `Result` exists** | Ambiguous error handling | Use explicit result types |
| **Drive-by refactors** | Scope creep, review noise | Change only what the milestone requires |
| **Black-box AI in core learning paths** | Breaks explainability | AI enrichment ports only, after decisions |

---

## Curriculum and legacy

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **Duplicate topic ordering logic** | V1/V2 ordering diverges | `CurriculumService` traversal helpers |
| **Treat engine dataclasses as ORM models** | Confuses in-memory truth with persistence | Separate engine types from SQLAlchemy models |
| **Silently break flat (V1) curricula** | Regression for existing users | Test V1 and V2 traversal |
| **Bypass `StartupService` safety** | Risky production bootstrap | Idempotent migrate + admin paths |

---

## Abstraction discipline

| Anti-pattern | Why forbidden | Instead |
|---|---|---|
| **Prefer composition over new abstractions** | Over-abstraction obscures flow | Compose existing engines, services, and ports |
| **New abstraction for one call site** | Premature generalisation | Inline until a second use case appears |
| **Leaky ports** | Infrastructure details in application | Narrow port interfaces |

---

## Quick decision tree

```
Is this an educational decision?
  YES → domain engine, orchestrated by pipeline
  NO  → is it HTTP?        → adapters
        is it persistence? → infrastructure
        is it rendering?   → presentation
        is it wiring?      → application / composition root
```
