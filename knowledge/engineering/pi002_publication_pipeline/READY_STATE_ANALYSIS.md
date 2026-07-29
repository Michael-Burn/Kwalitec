# Ready State Analysis

**Programme:** PI-002  
**Question:** Exactly how does a Subject become Ready — and why does it not?

---

## 1. Ready is a multi-layer predicate

“Ready” in Founder / student language is **not** a single enum. It requires all of the following.

### A. Studio publication checklist

All facts true:

- `cmp_uploaded`
- `official_syllabus_uploaded`
- `validation_passed`
- `blueprint_assigned`
- `preview_approved`
- `version_assigned`
- `rollback_snapshot_created`

⇒ `ready_to_publish == True`

### B. Management authority

- Version state `published`
- Lawful path through validate → blueprint → preview_ready → approved → published

### C. Foundation student package

- Foundation version exists for subject
- Parsed structure present (sections/topics)
- Foundation publication state advanced through review → published
- Active `PublishedCurriculumPackage` row

### D. Subject Catalogue projection

`SubjectCatalogueService._from_published`:

- Active package ⇒ availability `ready` (even if enrolment still gated)
- Support status may further allow plan creation

### E. Founder Subjects hub display

Studio subjects hub joins published packages for Ready / Current Version / Published Date columns (`routes.py` subjects listing).

---

## 2. Required artefacts

| Artefact | System |
|---|---|
| Official CMP + Syllabus documents | Document metadata + storage |
| Extracted structure (CIP/Foundation) | CIP entities / Foundation `parsed_structure_json` |
| Management curriculum package + assets | CurriculumCatalogue package |
| Blueprint assignments | Management assignments |
| Validation + approval records | Management reports / approvals |
| Studio workspace facts | StudioRegistry |
| PublishedCurriculumPackage | Foundation DB |
| Catalogue offer / discovery | Platform integration discovery |

### Required version

- Studio `version_label` + `version_id` linked to Management version
- Foundation version label aligned for bridge resolution

---

## 3. Why Ready is never reached

Working backwards:

```text
Catalogue Ready
  ← needs active Foundation package
    ← needs PublicationBridge after Management publish
      ← needs PublicationService.publish
        ← needs ready_to_publish checklist
          ← needs preview_approved
            ← needs PublicationService.approve
              ← needs validation_passed
                ← FAILS HERE (see Validation Investigation)
```

**Root blockage:** `validation_passed` never becomes true on the Founder upload→validate path when the stub Ingestion job fails while CIP extraction succeeded.

Without that fact:

- Preview stays `not_ready` for approval gating semantics
- Approve refuses
- Publish checklist incomplete
- Bridge never runs
- Subjects hub never shows Ready / published date
- Students never discover the new subject as Ready

---

## 4. False “Ready” signals to avoid

| Signal | Means Ready? |
|---|---|
| Document processing stage Ready | No — only sources ready |
| Structure topics listed | No — extraction only |
| Management state `preview_ready` | No — not published |
| Checklist lifecycle label READY for mid-states | **Misleading** — see consistency audit |
| Preview success flash | No — build ≠ review-ready ≠ published |

---

## 5. Evidence

- FV-001B Re-run Phase 9: subjects not Ready; student surface lacks new Ready subject
- LB-R4
- Code: `subject_catalogue.py`, `publication_bridge.py`, `publication_checklist.py`
