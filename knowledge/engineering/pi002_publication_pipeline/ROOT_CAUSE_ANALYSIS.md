# Root Cause Analysis

**Programme:** PI-002  
**Method:** Work backwards from failed Ready; require evidence for each hop

---

## 1. Dependency graph

```text
                    ┌─────────────────────────┐
                    │ Official CMP / Syllabus │
                    │ upload (PDFs Ready)     │
                    └───────────┬─────────────┘
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   CIP extraction        Management assets      Ingestion job
   (real topics)         (opaque refs)          (SYNTHETIC stub
          │                     │                topic-e-1)
          │                     │                     │
          ▼                     ▼                     ▼
   Structure panel       Management package     Ingestion validation
   Preview fallback      + blueprints           FAILED (missing_objectives)
          │                     │                     │
          │                     ▼                     │
          │              Management validate          │
          │              can PASS                     │
          │                     │                     │
          └─────────────┬───────┴─────────────────────┘
                        ▼
            Studio validate_curriculum
            requires Ingestion AND Management
                        │
                        ▼
            validation_passed = False   ← FIRST FAILED TRANSITION
                        │
          ┌─────────────┼─────────────┐
          ▼             ▼             ▼
     Preview         Approve       Checklist
     not_ready       refused       incomplete
          │             │             │
          └─────────────┴──────┬──────┘
                               ▼
                            Publish
                            refused
                               │
                               ▼
                     Foundation bridge skipped
                               │
                               ▼
                     Subject Catalogue Ready
                     never reached
```

---

## 2. Earliest incorrect state transition

### Definition

The first point where expected Studio publication state diverges from actual:

| Field | Expected after Validate (documents Ready + extraction complete) | Actual |
|---|---|---|
| `WorkspacePublicationFacts.validation_passed` | `True` | `False` |

### Causal mechanism

1. Upload calls `upload_sources(..., start_ingestion=True)` with references only.  
2. `CurriculumIngestionAdapter` fabricates a one-topic stub document when `entries` are absent.  
3. Ingestion engine marks the job validation as failed (`missing_objectives`, etc.).  
4. Studio AND-gates that failed report with Management validation.  
5. Even when Management passes, Studio refuses to set `validation_passed`.  
6. Founder-visible CIP structure is **not** fed into the Ingestion job that validation consults.

This is an **orchestration / input wiring** defect, not a deliberate safety refusal of bad curriculum content. Safety gates are functioning; they are being fed non-representative stub content beside the real extraction path.

---

## 3. Why this is primary (not symptoms)

| Candidate | Why not primary |
|---|---|
| Preview `not_ready` with topics | Correctly derives from `validation_passed=False` |
| Approve publish-flavoured flash | Downstream of missing validation + flash mapping bug |
| Publish refusal | Correct checklist safety after missing facts |
| Ready / catalogue | Terminal consequence |
| Empty findings / 0 errors | Amplifies confusion; does not cause the fact to stay false |
| Management EMPTY_PACKAGE (when assets missing) | Alternate failure mode; **not** required to explain FV re-run flash text. Reproduced path with assets present still fails via Ingestion |

---

## 4. Propagation through the pipeline

### Validation
- Combined gate fails → `validation_passed` stays false  
- Flash claims blocking findings; mapper drops `issues[]` → 0 errors  

### Preview
- CIP nodes allow `build_for_review` success  
- Readiness stays `not_ready` without `validation_passed`  

### Approval
- Hard-requires `validation_passed` → `PublicationError`  
- Flash mapper emits Publish copy  

### Publication
- Checklist missing `validation_passed` and `preview_approved` → refuse  

### Ready
- Bridge never runs → no active Foundation package → catalogue non-Ready  

---

## 5. Secondary root causes (clearly defined set)

These must be fixed for an honest Founder journey, but they are **not** the first transition failure:

1. **Report projection bug:** `_map_report` does not read `issues`.  
2. **Flash taxonomy bug:** Approve/validation PublicationError mapping uses Publish verbs.  
3. **Preview success criterion bug:** success ignores readiness semantics.  
4. **Dual structure authority:** CIP vs Ingestion stub vs Management package without a single SSOT for validation inputs.  
5. **Lifecycle label misuse:** Management mid-states mapped to Studio checklist “READY”.  

---

## 6. Evidence summary

| Claim | Evidence |
|---|---|
| FV journey fails at validate with exact Studio ValidationError flash | `complete.json` C2_validate |
| Production adapters reproduce flash + 0 errors + in_progress | 2026-07-29 reproduction with `CurriculumIngestionAdapter` + `CurriculumManagementAdapter` |
| Ingestion stub lacks objectives | Ingestion report `missing_objectives` on `topic-e-1` |
| Management can pass while Studio fails | Same reproduction |
| Approve/Publish messages match mapping rules | `operator_guidance.py` + C4/C5 |

---

## 7. Statement of root cause

**Single primary root cause:**  
Studio validation AND-gates a Curriculum Ingestion job that was started from reference-only uploads and therefore validates **synthetic stub content**, while the Founder’s real extracted curriculum lives on the CIP/Foundation path. That gate never flips `validation_passed` to true.

**Defined secondary causes:** report mapping, flash taxonomy, preview success semantics, and multi-authority structure projections — all amplify or follow the primary failure.
