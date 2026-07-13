# Kwalitec v0.9.1

## CM1 Learning Objective Storage Hotfix

Version:

v0.9.1

Status:

Production (Internal Alpha)

---

## Overview

Version 0.9.1 unblocks official CM1 Learning Objective import by storing full syllabus wording, and publishes Release Protocol Version 2.0 as the canonical release procedure.

---

## Highlights

### Learning Objective description storage

`learning_objectives.description` is widened from `VARCHAR(500)` to unbounded `TEXT`.

Official IFoA Learning Objective text (notably CM1) can exceed 500 characters when stored with syllabus prefixes. Existing CS1 / CB2 rows are preserved.

### Release Protocol 2.0

`docs/process/RELEASE_PROTOCOL.md` is replaced with the operational V2.0 playbook covering classification, database and curriculum gates, educational data compatibility, deployment fingerprints, Internal Alpha rules, risk, and rollback.

---

## Operator notes

- Classification: Hotfix + Migration Release + Internal Alpha Release
- Educational data compatibility: **Compatible** (additive column widen; no Internal Alpha reset required)
- After deploy, confirm Alembic head `202607130002` and that CM1 import stores full LO text
- Re-import curricula if a prior CM1 import failed or truncated descriptions

---

Thank you to everyone contributing to Kwalitec.
