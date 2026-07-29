# PI-002R — Executive Summary

**Programme:** PI-002R — Publication Validation Wiring  
**Status:** Complete  
**Predecessor:** PI-002 — Publication Pipeline Root Cause Investigation  
**Date:** 2026-07-29

---

## Verdict

**Resolved.** Founder Studio publication now evaluates one authoritative curriculum representation through Validate → Preview → Approve → Publish → Ready.

The primary PI-002 defect — AND-gating a synthetic Curriculum Ingestion stub against CIP-extracted curriculum — is corrected without bypassing validation, approval, or publication safety.

---

## What changed

| Area | Change |
|---|---|
| Validation authority | Management ValidationPolicy + Structure Preparation (CIP/Foundation) is the Founder publication gate |
| Stub ingestion | Reference-only uploads no longer start Ingestion jobs; non-authoritative stub jobs are ignored if present |
| Findings projection | `_map_report` consumes `issues[]`; failed reports surface as `failed` readiness |
| Preview | Hierarchy prefers prepared structure (same as validation); success flash requires `ready_for_review` + `validation_passed` |
| Approval flash | Approve failures use Approve copy, not Publish verbs |
| Management latest | Adapter returns full validation snapshot including issues |

---

## Authority chain (now)

```text
Official Documents
    ↓
CIP Extraction
    ↓
Structure Preparation
    ↓
Management Validation  ← publication-gate authority
    ↓
Preview (same structure)
    ↓
Approval (preview_approved)
    ↓
Publication (Management + Foundation bridge)
    ↓
Ready (Subject Catalogue)
```

---

## Exit criteria

| Criterion | Status |
|---|---|
| Exactly one authoritative curriculum representation | ✓ |
| Validation / Preview / Approval / Publication / Ready consume it | ✓ |
| No synthetic placeholder curriculum in Founder publication gate | ✓ |
| Publication safety gates intact | ✓ |
| End-to-end integration tests pass | ✓ |

---

## Next step (do not skip)

Run an **internal engineering verification** that a subject transitions:

Draft → Validated → Preview Ready → Approved → Published → Ready

Only after that succeeds should **FV-001B** be re-run.

**Do not proceed directly to FV-001B.**
