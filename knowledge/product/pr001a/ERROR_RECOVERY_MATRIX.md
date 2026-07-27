# Error Recovery Matrix

**Programme:** PR-001A  

Maps founder-facing failure modes → operator recovery. Implementation: `recover_flash` + validation guidance catalog.

---

## Matrix

| Failure mode | Typical exception / signal | User-visible guidance | Recovery procedure |
|---|---|---|---|
| Upload failure (empty refs) | Form / upload flash | Couldn't upload sources; CMP/syllabus required | Assign version; provide CMP and/or syllabus reference; retry upload |
| Upload / port failure | `PortUnavailable` | Studio service temporarily unavailable | Refresh; retry; escalate if persistent |
| Parsing / ingestion failure | `ingestion_error` findings | Blocking ingestion problem + what to do | Correct references/structure; re-upload; validate |
| Validation failure (sources) | `missing_cmp` / `missing_syllabus` | Findings panel + validate flash | Upload sources; validate again |
| Validation failure (no version) | `ValidationError` requires version | Assign version then try again | Assign version label; retry validate |
| Validation failure (blocking) | `ValidationError` failed/blocked | Review findings; fix CMP/syllabus | Clear findings; re-validate |
| Publication failure | `PublicationError` | Couldn't publish; need version/approval | Complete checklist; assign version; approve; publish |
| Duplicate subject | `SubjectAlreadyExists` | Code already exists; choose different code or open workspace | New code or open existing workspace |
| Duplicate / conflicting version | `VersionError` already exists | Conflicting labels break history | Choose new version label; retry |
| Workspace missing | `WorkspaceNotFound` / LookupError | Workspace could not be found | Return to Studio; open listed workspace |
| Workflow gate blocked | `WorkflowGateBlocked` | Complete current stage checklist | Satisfy stage gates; advance again |
| Preview before validate | `PreviewError` | Validate first | Validate; then preview |
| Approve incomplete | `PublicationError` | Assign version; complete preview | Fix prerequisites; approve |

## Design rules

1. Founders never see stack traces.
2. Recovery always ends with a concrete next action and “try again”.
3. Why-it-matters language ties to student safety or publication integrity.
4. Escalation is only for persistent infrastructure unavailability — not for clearing validation gates.

## Evidence

Automated coverage: `tests/certification/test_pr001a_founder_operations.py` (`TestOperationalErrorRecovery`).
