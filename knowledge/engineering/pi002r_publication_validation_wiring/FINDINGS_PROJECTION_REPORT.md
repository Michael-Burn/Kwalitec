# Findings Projection Report

**Programme:** PI-002R  
**Phase:** 3 — Findings Projection

---

## Problem (from PI-002)

Validation failed with flash “blocking findings remain” while the Validation panel showed **0 errors**, because `_map_report` ignored the opaque `issues[]` array used by Ingestion / Management snapshots.

Failed reports with `passed=False` and empty mapped errors were classified as `in_progress`.

---

## Fixes

### `_map_report`
- Consumes `issues`, `errors`, and `blocking_issues`
- Maps `severity` / `is_blocking` into Studio `ValidationFinding`
- Warnings from `issues` with non-blocking severity go to warnings
- Explicit `passed=False` or `blocks_publication` → readiness `failed`

### `summarise`
- Prefers Management `latest_validation` (now returns full snapshot with `issues`)
- Only projects authoritative Ingestion reports

### Management adapter
- `latest_validation` calls `facade.validation.latest()` instead of reading a missing VersionSnapshot field

### Flash taxonomy
- Approve `PublicationError` paths use Approve copy (validation / preview gates)
- Publish verbs reserved for publish fallback

### Preview messaging
- Route flash success only when `ready_for_review`/`approved` **and** `validation_passed`
- Otherwise: topics loaded, validation still required

---

## Consistency rules

| Condition | Findings | Readiness | Flash |
|---|---|---|---|
| Management/Ingestion pass | 0 blocking | `passed` | Validation success |
| Blocking issues present | ≥1 error | `failed` | Blocking findings remain |
| `passed=False`, no mapped issues | 0 errors, `failed` readiness | `failed` | Blocking findings / validate warning |
| Preview without validation | nodes may load | `not_ready` | Warning, not success |

---

## Tests

- `test_map_report_consumes_issues_array`
- `test_map_report_explicit_fail_without_issues_is_failed`
- `test_approve_flash_does_not_use_publish_verbs`
- `test_friendly_preview_never_claims_ready_when_not_ready`
