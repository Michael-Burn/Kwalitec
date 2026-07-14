# ============================================================================
# AUTOMATION FRAMEWORK
# ============================================================================

**Document ID:** FSI-004  
**Title:** Automation Framework (Version 1)  
**Owner:** Architecture Office  
**Status:** Version 1.0 Implemented  
**Classification:** Platform Engineering  
**Programme:** Founder System Integration

---

## Purpose

The Automation Framework provides **deterministic, manually triggered**
execution of registered automation workflows.

Version 1 is intentionally generic. Founder workflows are the first registered
consumers. Future Educational Intelligence, Digital Twin, and Product workflows
reuse the same registry, executor, and service surface.

### In scope

- Workflow protocol (`AutomationTask`)
- Registry (register / lookup / metadata)
- Executor (validate → execute → measure → result)
- Service (run by workflow id)
- Explicit validation and immutable results
- Registration of Internal Alpha Live Workflow

### Out of scope (Version 1)

- Scheduling / cron
- Celery or other queues
- Background jobs
- Filesystem watchers
- Notifications
- AI / LLM invocation inside the framework
- Changes to Internal Alpha Workflow internals

---

## Architecture

```text
AutomationService
        │
        ▼
AutomationRegistry  ─── look up AutomationTask by id
        │
        ▼
AutomationExecutor
        │
        ├── validate context (framework)
        ├── validate context (workflow)
        ├── execute(workflow, context)
        ├── measure duration
        └── return AutomationResult
```

Package layout:

```text
app/automation/
├── models/          # AutomationContext, AutomationResult, payload
├── dto/             # WorkflowMetadata, validation cargo / errors
├── registry/        # AutomationRegistry + default bootstrap
├── workflows/       # AutomationTask protocol + Founder adapter
├── executors/       # AutomationExecutor
├── validators/      # Context + result validators
├── services/        # AutomationService (public entry)
└── tests/           # Mocked workflow unit tests
```

This is a **platform subsystem** (`app/automation/`), not a Founder package.

---

## Workflow Protocol

Every automation workflow implements `AutomationTask`:

| Member | Role |
|--------|------|
| `id` | Stable unique identifier |
| `name` | Human-readable name |
| `description` | Short purpose statement |
| `validate(context)` | Return `ValidationReport` |
| `execute(context)` | Return `WorkflowExecutionPayload` |

No other public interface is required or permitted by the framework contract.

`execute` returns a `WorkflowExecutionPayload` (outputs, warnings, errors, and
optional explicit status). The executor wraps timing into `AutomationResult`.

---

## Registry

`AutomationRegistry` responsibilities:

- Register workflows
- Look up workflows by id
- Prevent duplicate registrations (`DuplicateWorkflowError`)
- Expose immutable `WorkflowMetadata`

The registry **does not execute** workflows.

`build_default_registry()` registers Version 1 platform workflows, including
the Founder Internal Alpha adapter.

---

## Execution Model

`AutomationExecutor`:

1. Resolve context (default: empty parameters).
2. Framework-validate context structure.
3. Call `workflow.validate(context)`.
4. On validation failure → `AutomationResult` with `FAILED` (no execute).
5. Call `workflow.execute(context)` and capture duration.
6. On exception → `FAILED` with the exception message.
7. Derive or accept status → return complete `AutomationResult`.

`AutomationService` is the public coordinator:

```python
from app.automation import AutomationContext, AutomationService

result = AutomationService().run(
    "founder.internal_alpha.workflow",
    AutomationContext.from_mapping({"week": "week_001"}),
)
assert result.status.value in {"SUCCESS", "FAILED", "PARTIAL_SUCCESS"}
```

### AutomationResult fields

| Field | Meaning |
|-------|---------|
| `workflow_id` | Executed workflow id |
| `status` | `SUCCESS` \| `FAILED` \| `PARTIAL_SUCCESS` |
| `started_at` / `completed_at` | Clock timestamps |
| `duration_ms` | Measured wall duration |
| `warnings` / `errors` | Strings gathered from validation/execution |
| `outputs` | Immutable mapping of workflow outputs |

---

## Extending the Framework

1. Implement `AutomationTask` (id, name, description, validate, execute).
2. Register the instance on an `AutomationRegistry` (or extend
   `build_default_registry()` for platform defaults).
3. Trigger via `AutomationService.run(workflow_id, context)`.

Rules:

- Keep domain logic inside the workflow implementation, not the executor.
- Prefer injecting collaborators into the workflow for testability.
- Do not add scheduling, queues, or watchers to the framework core.

---

## Founder Integration

Registered automation id:

```text
founder.internal_alpha.workflow
```

Adapter: `InternalAlphaAutomationWorkflow` in
`app/automation/workflows/founder_internal_alpha.py`.

It wraps `InternalAlphaWorkflowService.run()` **without modifying** the FSI-003
workflow. Optional context parameters:

| Parameter | Type | Meaning |
|-----------|------|---------|
| `week` | `str` | Week folder label (e.g. `week_001`) |
| `generated_at` | `datetime` | Optional timestamp override |

Stage outcomes from `WorkflowResult` are mapped into `outputs` and framework
status (`SUCCESS` / `PARTIAL_SUCCESS` / `FAILED`).

---

## Future Scheduling

Version 1 remains **manually triggered**. Future programmes may add:

- Schedulers / cron triggers that call `AutomationService.run`
- Background / queued execution adapters
- Filesystem watchers that enqueue a manual-equivalent run
- Notification hooks on `AutomationResult`

Those belong **outside** the core framework. The registry, executor, result
model, and workflow protocol should stay scheduling-agnostic.

---

## Related Paths

| Path | Role |
|------|------|
| `app/automation/` | Automation Framework package |
| `app/founder/internal_alpha_workflow/` | FSI-003 Internal Alpha Live Workflow |
| `knowledge/founder/FSI-003_INTERNAL_ALPHA_LIVE_WORKFLOW.md` | Founder workflow capability |
| `knowledge/engineering/patterns/ENG-002_ENGINEERING_PATTERNS.md` | Coordinator pattern |
