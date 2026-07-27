# Validation UX Review

**Programme:** PR-001A  
**Date:** 2026-07-27  
**Status:** Pass with operator-guidance improvements  

---

## Review criteria

Every founder-facing validation message must:

1. Explain the **issue**
2. Explain **why it matters**
3. Provide a clear **recovery action**

## Surfaces reviewed

| Surface | Location | Result |
|---|---|---|
| Validation finding catalog | `app/application/curriculum_studio/validation_guidance.py` | Pass — issue/why/recovery per code |
| Summarise missing sources | `ValidationService.summarise` via `guided_finding` | Pass |
| Ingestion mapped findings | `_map_report` + `enrich_finding` | Pass — defaults applied |
| Workspace findings panel | `workspace.html` Validation findings | Pass — shows issue, why, what to do |
| Validation flash warnings | `FLASH_WARNING["validate"]` + `recover_flash` | Pass — three-part copy |
| Form field errors | `CreateSubjectForm` / `AssignVersionForm` | Pass — issue/why/recovery in DataRequired messages |

## Catalog coverage

| Code | Issue | Why | Recovery |
|---|---|---|---|
| `missing_cmp` | Yes | Yes | Yes |
| `missing_syllabus` | Yes | Yes | Yes |
| `ingestion_error` | Yes | Yes | Yes |
| `ingestion_warning` | Yes | Yes | Yes |
| unknown codes | Message kept | Default why | Default recovery |

## Gaps closed in PR-001A

- Findings previously showed short technical phrases only (`CMP source not present`).
- Workspace UI did not surface finding why/recovery.
- Validation failures flashed a generic “review and try again” without tying to findings.

## Residual limitations

- Ingestion ports may return terse upstream messages; enrichment supplies why/recovery when upstream omits them.
- Student-facing surfaces are out of scope (founder Console only).

## Verdict

**Pass** for founder validation UX under PR-001A acceptance criteria.
