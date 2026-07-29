# Publication State Machine

**Programme:** PI-002  
**Scope:** Curriculum Studio Founder publication pipeline + Curriculum Management authority states

---

## 1. Two layered machines

Publication readiness is expressed in **two** coordinated state spaces:

| Layer | Owner | Persistence | Role |
|---|---|---|---|
| **Studio workflow stages** | Curriculum Studio (`StudioWorkflow`) | In-memory `StudioRegistry` | Founder navigation / stage chrome |
| **Management publication states** | Curriculum Management (`PublicationState`) | In-memory `CurriculumCatalogue` | Authoritative version lifecycle |
| **Studio publication facts** | `WorkspacePublicationFacts` | In-memory registry | Checklist inputs (computed, not toggled) |
| **Foundation publication** | Curriculum Studio Foundation | SQLAlchemy | Student Subject Catalogue Ready package |

Studio never owns publication authority. Management `publish` / `approve` are authoritative; Foundation materialises student-facing Ready.

---

## 2. Studio workflow stages

Source: `app/domain/curriculum_studio/workflow_stage.py`, `studio_workflow.py`

| State | Entry | Exit | Owner | Dependents |
|---|---|---|---|---|
| `subject` | Workspace created | Advance / jump | Studio workflow | Subject registration |
| `content_sources` | Advance from subject | Advance after sources | Studio workflow | Document upload, checklist CMP/syllabus facts |
| `validation` | Advance / jump | Advance after validate | Studio workflow | ValidationService, StructurePreparation |
| `preview` | Advance / jump | Advance after preview review | Studio workflow | PreviewService |
| `approval` | Advance / jump | Advance after approve | Studio workflow | PublicationService.approve |
| `publication` | Advance / jump | Terminal for workflow | Studio workflow | PublicationService.publish |

**Transition law:** `LAWFUL_WORKFLOW_TRANSITIONS` allows ADVANCE/RETREAT/RESET/jumps. Application gates (facts/checklist) are **not** enforced by the domain transition map — jumps are lawful; readiness is enforced in services.

**StageOutcome vocabulary:** `ready` / `blocked` / `in_progress` / `complete` / `skipped` (evaluation labels; not persisted workflow states).

---

## 3. Curriculum Management publication states

Source: `app/domain/curriculum_management/publication_state.py`

Forward pipeline:

```text
draft → uploaded → validated → blueprint_assigned → preview_ready → approved → published
                                                                                 ↓
                                                                             archived
```

| State | Entry conditions | Exit conditions | Owner | Dependent systems |
|---|---|---|---|---|
| `draft` | Version created | First asset upload → `mark_uploaded` | Management VersionService | AssetService |
| `uploaded` | ≥1 asset on package | Validation pass → `mark_validated` | AssetService / ValidationService | ValidationPolicy |
| `validated` | Validation passed from `uploaded` | Blueprint assign → `mark_blueprint_assigned` | ValidationService | BlueprintAssignmentService |
| `blueprint_assigned` | Assignment recorded while validated (or auto-advance on validate if assignments exist) | Preview → `mark_preview_ready` | BlueprintAssignmentService | PreviewService |
| `preview_ready` | Preview built from `blueprint_assigned` | Approve → `mark_approved` | PreviewService | ApprovalService |
| `approved` | Approval decision | Publish → `mark_published` | ApprovalService | PublicationService |
| `published` | Publish | Archive → `mark_archived` | PublicationService | Studio mirror, Foundation bridge |
| `archived` | Archive from published | Terminal | PublicationService | History / rollback UX |

Illegal transitions raise Management policy/domain errors. Studio catches and surfaces Founder flashes.

---

## 4. Workspace publication facts (checklist inputs)

Source: `app/domain/curriculum_studio/publication_checklist.py`

Facts are **inputs**. Checklist items are **computed**.

| Fact | Meaning | Typically set by |
|---|---|---|
| `cmp_uploaded` | Official CMP present | Document upload / `upload_sources` |
| `official_syllabus_uploaded` | Official Syllabus present | Document upload / `upload_sources` |
| `validation_passed` | Studio validation gate passed | `ValidationService.validate_curriculum` |
| `blueprint_assigned` | Blueprints recorded / prepared | `StructurePreparationService` / validate success |
| `preview_approved` | Founder approved preview | `PublicationService.approve` / `PreviewService.approve` |
| `version_assigned` | Version label linked | `VersionHistoryService.assign_version` |
| `rollback_snapshot_created` | Rollback snapshot exists | `PublicationService._ensure_rollback_snapshot` on publish |

Derived:

| Item | Condition |
|---|---|
| `ready_to_publish` | **All** prerequisite facts true |

---

## 5. Studio workspace status

Source: `CurriculumWorkspace.WorkspaceStatus`

| State | Meaning |
|---|---|
| `active` | Working draft |
| `published` | Studio projection after Management publish |
| `archived` | Archived |
| `abandoned` | Abandoned |

---

## 6. Preview readiness (display)

Source: `PreviewReadiness` in `preview_summary.py`

| State | Derived when |
|---|---|
| `not_ready` | No hierarchy **or** `validation_passed` false |
| `ready_for_review` | Nodes present **and** `validation_passed` |
| `approved` | `preview_approved` fact true |
| `rejected` | Explicit reject |

---

## 7. Validation readiness (display)

Source: `ValidationReadiness` in `validation_summary.py`

| State | Meaning |
|---|---|
| `not_started` | No report / no structure |
| `in_progress` | Report present but not mapped as passed/failed cleanly |
| `passed` | Ready for publication gate |
| `failed` | Blocking findings |
| `blocked` | Blocked posture |

---

## 8. Foundation / Subject Catalogue Ready

Source: `publication_bridge.py`, `subject_catalogue.py`, Foundation lifecycle

| Required | Meaning |
|---|---|
| Management version `published` | Authority publish succeeded |
| Foundation version approved + published package | `PublicationBridgeService.publish_to_catalogue` |
| Active `PublishedCurriculumPackage` | Catalogue `availability = ready` |

Student Ready ≠ Management `preview_ready`. Checklist service incorrectly maps several Management mid-states to lifecycle label `READY` for Studio projection — see consistency audit.

---

## 9. Expected Founder path ↔ state changes

```text
Create Subject
  → Studio subject exists; workflow subject
Upload CMP + Syllabus
  → facts cmp/syllabus; Management assets → uploaded; Foundation docs; CIP extraction
Extraction complete (CIP Ready)
  → structure visible; Management still may be uploaded only
Validate
  → Management uploaded→validated→blueprint_assigned (when assignments exist)
  → Studio fact validation_passed=True, blueprint_assigned=True
Preview
  → Management blueprint_assigned→preview_ready
  → PreviewReadiness ready_for_review
Approve
  → Management preview_ready→approved
  → fact preview_approved=True
Publish
  → rollback fact; Management approved→published
  → Foundation Ready package; catalogue Ready
```

---

## 10. Verified transition points (investigation)

| Transition | Expected | Observed in FV-001B Re-run / reproduction |
|---|---|---|
| Documents → Ready (CIP/Foundation) | Yes | Yes |
| Extraction → structure topics | Yes | Yes |
| Validate → `validation_passed=True` | Yes | **No** (first failure) |
| Preview → `ready_for_review` | Yes | No (stuck `not_ready`) |
| Approve → `preview_approved=True` | Yes | No |
| Publish → Management `published` | Yes | No |
| Catalogue → Ready | Yes | No |
