# Validation Guide

**Programme:** PR-001A  
**Goal:** Understand and clear Curriculum Studio validation findings  

---

## What validation does

Validation checks that the workspace has enough correct curriculum material to preview and publish safely. It combines:

- **Source presence** (CMP / official syllabus references)
- **Ingestion** structural checks (when an ingestion job exists)
- **Management** publication-gate validation (when a version is assigned)

## Finding format

Every finding shown in Studio includes:

| Part | Meaning |
|---|---|
| **Issue** | What is wrong |
| **Why it matters** | Impact on students / publication safety |
| **What to do** | Concrete recovery action |

## Common findings

### Missing CMP (`missing_cmp`)

- **Issue:** CMP source is not present.
- **Why:** Without CMP the Studio cannot derive sections, topics, or learning objectives.
- **Do:** Assign a version, enter a CMP reference, upload sources, validate again.

### Missing syllabus (`missing_syllabus`)

- **Issue:** Official syllabus source is not present.
- **Why:** Publication must stay grounded in authorised syllabus order.
- **Do:** Enter syllabus reference, upload, validate again.

### Ingestion error (`ingestion_error`)

- **Issue:** Parsing or structural failure from ingestion.
- **Why:** Extracted curriculum would be unsafe to publish.
- **Do:** Correct references/source structure, re-upload, validate again.

### Ingestion warning (`ingestion_warning`)

- **Issue:** Non-blocking warning from ingestion.
- **Why:** May hide gaps students feel later.
- **Do:** Review detail; fix if material; re-validate before preview.

## Operator rules

1. **Blocking findings must be cleared** before preview/publish.
2. Warnings may be accepted only when you understand the student impact.
3. Always re-run **Validate Curriculum** after changing sources.
4. If validation says a version is required, assign a version label first.

## Flash messages

Failed validation posts return a warning flash that:

- states the failure,
- explains why it matters,
- tells you to review findings and try again.

Stack traces are never shown in the Console.
