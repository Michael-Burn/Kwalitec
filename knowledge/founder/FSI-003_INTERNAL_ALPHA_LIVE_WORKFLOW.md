# FSI-003 — Internal Alpha Live Workflow

**Document ID:** FSI-003  
**Title:** Internal Alpha Live Workflow  
**Owner:** Founder Operating System  
**Status:** Version 1.0 Implemented  
**Classification:** Founder Infrastructure  
**Programme:** Founder System Integration

---

## Purpose

Integrate the existing Internal Alpha Pipeline with the live repository week
layout so the Founder performs **one manual action**:

> Drop tester `.txt` files into the appropriate week folder.

Everything else runs automatically through the Founder Operating System when
the workflow is triggered.

This capability is **integration only**:

- No AI
- No Dashboard modifications
- No Recommendation Engine modifications
- No Operational State redesign
- No scheduling, filesystem watchers, background jobs, notifications, or email

Version 1 automation remains **manually triggered**.

---

## Workflow

```text
WeekDiscoveryService
        │
        ▼
InternalAlphaPipelineService          (FOS-003)
        │
        ▼
FounderOperationalStateService        (FOS-005, alpha injected from pipeline)
        │
        ▼
FounderRecommendationService          (FOS-006)
        │
        ▼
FounderWeeklyBriefingService          (FOS-007, in-memory)
        │
        ▼
WorkflowOutputManager                 (distribute managed exports)
```

### Execution Order

1. Detect week folder (`week_NNN`, latest unless specified).
2. Locate `raw_feedback/`.
3. Process all `.txt` files via the existing Internal Alpha Pipeline.
4. Generate processed outputs under `processed/`.
5. Refresh Founder Operational State (pipeline summary → Internal Alpha DTO).
6. Generate Recommendation Set.
7. Generate Founder Weekly Brief (in memory first).
8. Write outputs into their respective folders.

No additional orchestration exists outside this workflow.

---

## Folder Structure

Production layout:

```text
research/internal_alpha/
├── week_template/          # scaffold only (ignored by discovery)
└── week_001/
    ├── raw_feedback/       # Founder input — tester .txt files
    ├── processed/          # FOS-003 pipeline exports
    ├── findings/           # category findings + WEEK_SUMMARY
    ├── decisions/          # proposed_actions + recommendations
    ├── weekly_review/      # FOUNDER_WEEKLY_REPORT.*
    ├── release/            # release_readiness.md
    └── archive/            # manifest + archived key artefacts
```

Every week follows the same convention. Missing **output** directories are
created automatically. Unrelated files in those folders are never deleted or
overwritten.

---

## Packages

| Package | Role |
|---------|------|
| `app/founder/internal_alpha_workflow/` | FSI-003 coordinator + discovery + exports |
| `app/founder/internal_alpha/` | FOS-003 pipeline (unchanged public API) |
| `app/founder/operational_state/` | FOS-005 snapshot (DTO inject only) |
| `app/founder/recommendations/` | FOS-006 recommendations (unchanged) |
| `app/founder/briefing/` | FOS-007 briefing (unchanged) |

### Public API

| Type | Responsibility |
|------|----------------|
| `WeekDiscoveryService` | Locate weeks, pick latest, validate structure |
| `WeekReference` | Immutable week path DTO |
| `InternalAlphaWorkflowService` | Coordinator only |
| `WorkflowResult` | Immutable stage outcome |
| `WorkflowOutputManager` | Ensure folders + managed exports |

---

## Output Placement

| Folder | Managed artefacts |
|--------|-------------------|
| `processed/` | Pipeline JSON/Markdown (FOS-003) |
| `findings/` | `WEEK_SUMMARY.md`, category `.md` copies |
| `decisions/` | `proposed_actions.md`, `recommendations.json`, `recommendations.md` |
| `weekly_review/` | `FOUNDER_WEEKLY_REPORT.md`, `founder_weekly_report.json` |
| `release/` | `release_readiness.md` |
| `archive/` | `workflow_manifest.json`, archived summary / recommendations / brief |

Only config-managed filenames are written.

---

## Failure Behaviour

Failures are isolated and never silently continued.

| Failure | Behaviour |
|---------|-----------|
| Week missing / invalid | Stop immediately; explicit error |
| Missing / empty `raw_feedback/` | Stop; no pipeline |
| Pipeline failure | Stop workflow; report explicit error; no downstream stages |
| Operational State failure | Stop downstream generation; preserve pipeline `processed/` outputs |
| Recommendation failure | Stop brief + export; preserve pipeline outputs |
| Brief generation failure | Stop export; preserve pipeline outputs; no advisory folder writes |
| Export failure | Preserve pipeline outputs; report `export_failed` |

Downstream folder distribution runs **only after** pipeline, state,
recommendations, and briefing all succeed (partial export prevention).

---

## Recovery

1. Inspect `WorkflowResult.errors` / `.warnings`.
2. Fix the failing stage input (e.g. add `.txt` files, repair providers).
3. Re-run `InternalAlphaWorkflowService.run(week="week_NNN")`.
4. Pipeline and managed exports are idempotent for managed filenames; human
   notes in week folders remain untouched.

---

## Manual Trigger (Version 1)

```python
from app.founder.internal_alpha_workflow import InternalAlphaWorkflowService

result = InternalAlphaWorkflowService().run()  # latest week
# or
result = InternalAlphaWorkflowService().run(week="week_001")
assert result.success
```

For tests / isolated runs, inject `internal_alpha_root` plus static Knowledge /
Capability providers.

---

## Future Automation

Out of scope for FSI-003 (do not implement here):

- Schedulers / cron
- Filesystem watchers
- Background jobs
- Notifications / email
- Dashboard wiring of workflow status
- Default live Internal Alpha provider inside Operational State defaults
  (parity with FSI-001 Knowledge / Capability bridges)

---

## Related Paths

| Path | Role |
|------|------|
| `app/founder/internal_alpha_workflow/` | Live workflow package |
| `research/internal_alpha/` | Week folders |
| `knowledge/founder/FOS-003_INTERNAL_ALPHA_PIPELINE.md` | Pipeline capability |
| `knowledge/founder/FOS-005_OPERATIONAL_STATE.md` | Operational State |
| `knowledge/founder/FOS-006_RECOMMENDATION_ENGINE.md` | Recommendations |
| `knowledge/founder/FOS-007_FOUNDER_WEEKLY_BRIEFING.md` | Weekly Brief |
