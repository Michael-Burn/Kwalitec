# Validation Investigation

**Programme:** PI-002  
**Stage:** Validation

---

## 1. What validation requires

Studio `ValidationService.validate_curriculum` (`app/application/curriculum_studio/validation_service.py`):

1. **Structure preparation** via `StructurePreparationService.prepare_for_validation`
   - Load CIP entities and/or Foundation parsed structure
   - Sync `section_ids` / `topic_ids` / `objective_ids` onto workspace
   - Assign default blueprints on Management version (`founder-default`)
2. **Ingestion gate** (when an ingestion job is registered on the workspace)
   - `CurriculumIngestionPort.get_validation_report(job_id)`
   - Pass if `passed` true, or readiness in `{passed,ready,ok}`, or empty issues list
3. **Management gate** (default `run_management_gate=True`)
   - Requires `workspace.version_id`
   - `CurriculumManagementPort.validate_version(version_id)`
   - Management `ValidationPolicy` requires:
     - Non-empty curriculum package
     - Syllabus asset (blocking if missing)
     - Blueprint assignments (error/blocking if missing)
     - CMP / learning-objectives warnings when absent
4. **Combined pass:** `ingestion_passed AND management_passed`
5. On success: set `validation_passed=True` and `blueprint_assigned=True`
6. On failure: set `validation_passed=False` (only on Studio `ValidationError` path) and raise

---

## 2. What validation actually receives (Founder happy path)

| Input | Source | Actual content |
|---|---|---|
| Official CMP / Syllabus files | Document storage + SQL metadata | Real PDFs; UI shows Ready after CIP processing |
| CIP entities | `CipCurriculumEntity` linked to foundation docs | Real modules/topics from extraction |
| Management assets | `upload_sources` → `add_asset_ref` | Opaque references (`cmp`, `syllabus`) on package |
| Ingestion job | `upload_sources(..., start_ingestion=True)` | **Synthetic** documents: adapter invents a single topic entry when sources have no `entries` |
| Ingestion validation report | Ingestion engine | Fails: `missing_objectives` (blocking) on stub topic; often also metadata warnings |

Reproduction (production adapters):

```text
ingestion report.passed = False
issues = [
  missing_objectives (blocking) — "Topic topic-e-1 has no learning objectives",
  missing_metadata (warning) — "Missing required metadata key: subject_code",
]
Management validate = PASS (assets + blueprints present after prepare)
Studio combined = FAIL
Exception = ValidationError("Validation failed for …: 0 error(s)")
```

---

## 3. Why validation reports blocking findings

`recover_flash` maps Studio `ValidationError` containing `"failed"` / `"blocked"` to:

> We couldn't complete validation because blocking findings remain… Review the Validation findings below…

That path is taken when `validate_curriculum` raises:

```python
raise ValidationError(
    f"Validation failed for {workspace_id}: {snap.error_count} error(s)"
)
```

In the reproduced failure, `snap.error_count` is **0**.

---

## 4. Why validation simultaneously reports zero errors

### 4.1 Report schema mismatch (`_map_report`)

Studio mapper:

```python
report.get("errors") or report.get("blocking_issues") or ()
```

Ingestion / Management opaque snapshots expose findings under:

```text
issues: [{code, message, severity, is_blocking, ...}]
```

They do **not** populate `errors` or `blocking_issues`.

Therefore `_map_report`:

- Adds **no** error findings
- Sees `passed=False` + non-empty report → readiness `in_progress`
- UI / intelligence overlay: **0 validation errors**
- Findings panel: empty (no mapped blocking rows)

### 4.2 Management latest validation not projected

`CurriculumManagementAdapter.latest_validation` reads `version_summary["latest_validation"]`, but `VersionSnapshot` does not include that field → typically `None`. Summarise therefore depends on ingestion report (mis-mapped) or structure heuristics.

### 4.3 Structure heuristic can claim PASSED

If no mappable report, summarise may treat presence of `section_ids`/`topic_ids` as `PASSED` even when `validation_passed` fact is false. With a mis-mapped failed ingestion report, readiness becomes `in_progress` instead — matching FV-001B Re-run cards.

---

## 5. Consistency check

| Dimension | Consistent? | Observation |
|---|---|---|
| State (`validation_passed` fact) | Correctly false | Gate did not pass |
| Messaging (flash) | Misleading | Claims “blocking findings below” with nothing below |
| Data (findings list) | Incomplete | Real issues exist under `issues` but are not mapped |
| Orchestration | Incorrect for Founder path | AND-gates stub Ingestion against CIP-derived Management success |

**Conclusion:** State (fact false) is honest. Messaging, findings projection, and orchestration are inconsistent with each other and with Founder-visible extraction success.

---

## 6. Transition conditions

| From | To | Condition |
|---|---|---|
| facts.validation_passed=False | True | Ingestion pass (if job) **and** Management pass |
| Management `uploaded` | `validated` | Management validation report.passed |
| Management `validated` | `blueprint_assigned` | Assignments present during/after validate |

**First failed Studio transition:** `validation_passed` never becomes True on the Founder upload→validate path when Ingestion was started with reference-only sources.

---

## 7. Downstream consumers of validation_passed

- `PreviewSummary.create` readiness (`ready_for_review` requires `validation_passed`)
- `PreviewService.approve` / `PublicationService.approve` hard require the fact
- Publication checklist item `validation_passed`
- `ready_to_publish` derivation

---

## 8. Evidence

- FV-001B Re-run `_evidence/complete.json` → `C2_validate` flash (exact Studio ValidationError copy)
- Status card: `Validation needs attention · in_progress`
- Overlay: `0 validation errors`
- Checklist often `5 of 8` (cmp, syllabus, version, blueprint from prepare, not validation/preview/rollback)
- Code paths cited above; adapter reproduction 2026-07-29
