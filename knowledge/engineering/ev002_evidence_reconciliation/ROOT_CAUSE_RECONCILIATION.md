# Root Cause Reconciliation

**Programme:** EV-002  
**Selected case:** **D — Environment mismatch**

---

## Case selection

Exactly one case is selected:

| Case | Selected? | Reason |
|---|---|---|
| A — EV-001 invalid / unrealistic path | No | EV used visible Studio actions; package created by Publish; no seeded publication facts |
| B — FV-001B invalid / stale UI | No | CS1F remains `draft` with no package; Ready never exists to be “hidden” |
| C — Regression between identical executions | No | Executions were not identical environments; cannot attribute delta to a single shared runtime regressing |
| **D — Environment mismatch** | **Yes** | Different process code image, database, port, and curriculum inputs |
| E — Previously unidentified defect (primary) | No | Primary conflict dissolves under D; residual UX defects are known/PI-002-class, not the reconciling cause |

---

## Precise differing assumption

**Assumption (false):** “EV-001 VERIFIED and FV-001B Final NO-GO describe the same post–PI-002R system executing the same curriculum publication path.”

**Reality:**

1. **Runtime process / loaded code differed.**  
   FV-001B Final hit Flask on `:5130` started `2026-07-28T22:04:44Z` with debug/reload off. Disk edits to validation/preview/routes landed ~`22:27Z` and were imported by EV-001’s fresh `:5141` process (~`22:34Z`), not by the already-running `:5130` process still serving at FV Final (`22:47Z`).

2. **Databases differed.**  
   EV-001: fresh `/tmp/ev001_verify.sqlite3`.  
   FV-001B: default `instance/kwalitec.sqlite3` with prior CS1R/S/U workspaces.

3. **Curriculum inputs differed.**  
   CS1V vs CS1F PDF hashes and CIP graphs (see [`SUBJECT_COMPARISON.md`](SUBJECT_COMPARISON.md)).

---

## How both programmes can be “correct”

| Programme | What it correctly observed |
|---|---|
| EV-001 | On a clean DB + post-edit process, Studio path reaches Ready for CS1V |
| FV-001B Final | On stale process + instance DB + CS1F fixtures, Validate fails and Ready is never reached; UI contradictions appear |

No programme needs to be discarded; the **shared-system assumption** does.

---

## First divergence mechanism

```text
Upload Ready (both)
        ↓
Validate Curriculum
        ├── EV (:5141, post-PI-002R image, clean DB, CS1V) → validation_passed
        └── FV (:5130, pre-edit image, instance DB, CS1F) → validation blocked
```

Downstream FV failures follow directly from missing `validation_passed`.

Supporting symptom check: FV Approve flash uses Publish refusal wording and Preview shows success-with-`not_ready` — behaviours PI-002R explicitly targeted — consistent with FV not running the post-edit code image.

---

## Why not Case E as the verdict

Unidentified *new* defects are not required to explain the mutual exclusivity. Environment mismatch is sufficient and evidenced. Residual product issues (stale NEXT STEP, syllabus CIP LO warning messaging, Choose Exam `_format_release`) remain for remediation programmes but are out of scope as EV-002’s reconciling case.
