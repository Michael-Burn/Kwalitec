# Curriculum Studio

**Document ID:** V2-016B-CURRICULUM-STUDIO  
**Milestone:** V2-016B — Curriculum Studio Application Services  
**Status:** Authoritative domain + application specification  
**Authority:** Architectural — source of truth for Founder operational integration  
**Nature:** Framework-independent Founder orchestration / projection layer  

**Packages:**
- `app/domain/curriculum_studio/`
- `app/application/curriculum_studio/`

**Depends on:** optional injected ports only (Curriculum Management, Curriculum Ingestion, Education Platform). Does **not** import or modify those packages.

**Related:** [`CURRICULUM_MANAGEMENT.md`](CURRICULUM_MANAGEMENT.md) · [`CURRICULUM_INGESTION.md`](CURRICULUM_INGESTION.md) · [`EDUCATION_PLATFORM.md`](EDUCATION_PLATFORM.md) · [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md) · [`VERSION2_ROADMAP.md`](VERSION2_ROADMAP.md) · [`V2_ARCHITECTURE_DESIGN_REVIEW.md`](V2_ARCHITECTURE_DESIGN_REVIEW.md)

---

## 1. Purpose

Curriculum Studio is the **operational interface** through which a Founder creates, validates, reviews, approves, publishes, versions, and archives curricula.

The Founder is managing **educational products**, not files.

Every workflow answers:

> **Is this curriculum ready to publish?**

Curriculum Studio does **not**:

- Implement Flask routes, HTML, CSS, or JavaScript
- Persist to a database
- Parse PDFs
- Own Curriculum Management publication policies
- Own Curriculum Ingestion extraction / normalisation
- Own Education Platform student learning generation
- Embed Adaptive Decision or Twin mathematics

```text
Founder (future UI)
        │
        ▼
Curriculum Studio (this package)
        │
        ├── ports → Curriculum Management   (subjects, versions, publish, approve, gate preview)
        ├── ports → Curriculum Ingestion    (ingest, normalise, structural validation)
        └── ports → Education Platform      (health + optional student-surface display)
```

**Posture (V2-016B):** Studio is a **thin orchestration and projection layer**. Publication, version lifecycle, and validation policies remain owned by upstream bounded contexts.

---

## 2. Application Services

```text
app/application/curriculum_studio/
    subject_service.py                 # Create / list subjects via Management
    workspace_service.py               # Open workspace; upload sources; assign blueprint
    validation_service.py              # Present Ingestion + Management validation
    preview_service.py                 # Management gate preview + optional EP surface
    publication_service.py             # Approve / publish / archive via Management
    version_history_service.py         # Version history / archive / rollback via Management
    diff_service.py                    # Pure structural diff (Ingestion structures)
    publication_checklist_service.py   # Computed readiness projection
    dashboard_service.py               # Founder dashboard projection
    workflow_service.py                # Studio-owned Founder stage navigation
    curriculum_studio_service.py       # Public facade
    ports/                             # Expanded Protocols (no BC imports)
    dto/                               # Immutable snapshots only
```

| Service | Responsibility | Owns authority? |
|---------|----------------|-----------------|
| `SubjectService` | Create / get / list subjects | No — Management |
| `WorkspaceService` | Founder workspace session; source upload orchestration | Workspace session only |
| `ValidationService` | Map validation reports; sync `validation_passed` fact | No — Ingestion + Management |
| `PreviewService` | Display gate preview; optional student-surface | No — Management (+ EP display) |
| `PublicationService` | Orchestrate approve / publish / archive | No — Management |
| `VersionHistoryService` | Assign / history / archive / rollback | No — Management |
| `DiffService` | Compare normalised structures | Pure projection |
| `PublicationChecklistService` | Compute checklist from facts | Projection only |
| `DashboardService` | Aggregate Founder dashboard | Projection only |
| `WorkflowService` | Six-stage Founder navigation + gates | Yes — Studio UX stages |

Facade: `CurriculumStudioService` wires ports into all specialised services.

---

## 3. Use-case Catalogue

| Use-case | Entry | Authority | Port |
|----------|-------|-----------|------|
| Create Subject | `subjects.create_subject` / facade | Management | `CurriculumManagementPort.create_subject` |
| Open Workspace | `workspaces.open_workspace` | **Studio** session | — |
| Upload Curriculum Sources | `workspaces.upload_sources` | Management refs + Ingestion job | Management + Ingestion |
| Validate Curriculum | `validation.validate_curriculum` | Ingestion structure + Management gate | Ingestion + Management |
| Generate Preview | `preview.preview` | Management gate preview | Management (+ EP surface) |
| Review Validation | `validation.summarise` | Projection | Ingestion / Management read |
| Approve Curriculum | `publication.approve` / `preview.approve` | Management | Management |
| Publish Curriculum | `publication.publish` | Management | Management |
| Archive Version | `versions.archive_version` / `publication.archive` | Management | Management |
| Rollback Version | `versions.rollback_version` | Management | Management |
| View Version History | `versions.history` | Management | Management |
| Compare Versions | `diff.compare_ingestion_jobs` / `compare` | Studio pure + Ingestion data | Ingestion |
| Publication Readiness | `checklist.checklist` | Studio projection | Management state tokens |
| Founder Dashboard | `dashboard.dashboard` | Studio projection | Management + local workspaces |

Mutating use-cases **require** an available Management port (`PortUnavailable` otherwise).

---

## 4. Authority Matrix

| Capability | Owner BC | Studio service | Port family |
|------------|----------|----------------|-------------|
| Subject create/list | Management | `SubjectService` | `create_subject`, `list_subjects`, `get_subject_summary` |
| Version create/list | Management | `VersionHistoryService` | `create_version`, `list_versions` |
| Asset references | Management | `WorkspaceService` | `add_asset_ref`, `list_assets` |
| Ingest / normalise | Ingestion | `WorkspaceService` / `ValidationService` | `start_ingestion`, `normalised_structure` |
| Structural validation | Ingestion | `ValidationService` | `get_validation_report` |
| Publication-gate validation | Management | `ValidationService` | `validate_version`, `latest_validation` |
| Blueprint assignment | Management | `WorkspaceService` | `assign_blueprint` |
| Founder gate preview | Management | `PreviewService` | `preview_version` |
| Student-surface preview | Education Platform | `PreviewService` (display only) | `student_surface` |
| Approval | Management | `PublicationService` | `approve`, `reject` |
| Publish / Archive | Management | `PublicationService` | `publish`, `archive`, `publication_state` |
| Rollback | Management | `VersionHistoryService` | `rollback_version` |
| Checklist readiness | **Studio projection** | `PublicationChecklistService` | facts synced from ports |
| Workflow stages | **Studio** | `WorkflowService` | — |
| Diff | **Studio pure** | `DiffService` | Ingestion structures |
| Dashboard | **Studio projection** | `DashboardService` | Management lists + workspaces |

### Preview clarification

- **Founder publication-gate preview** → Curriculum Management (`PREVIEW_READY`).
- **Optional student-surface** → Education Platform (display / diagnostics only; never publishes).
- Studio never invents hierarchy as authority; it maps port payloads into DTOs.

---

## 5. Founder Workflow Mapping

```text
Stage 1  Subject          → SubjectService / WorkspaceService
Stage 2  Content Sources  → WorkspaceService.upload_sources
Stage 3  Validation       → ValidationService.validate_curriculum
Stage 4  Preview          → PreviewService.preview / approve
Stage 5  Approval         → PublicationService.approve
Stage 6  Publication      → PublicationService.publish
```

| Stage | Question | Gate facts (Studio checklist) |
|-------|----------|-------------------------------|
| Subject | Which educational product? | — |
| Content Sources | CMP + syllabus refs present? | `cmp_uploaded`, `official_syllabus_uploaded` |
| Validation | Structure + gate checks pass? | `validation_passed` |
| Preview | Student-visible curriculum acceptable? | `preview_approved` |
| Approval | Founder approved? | Management approval via port |
| Publication | Ready to publish? | All checklist facts + Management `publish` |

Stages (`WorkflowStage`) and advance gates remain Studio-owned UX.  
Publication truth is always `CurriculumManagementPort.publication_state(version_id)`.

---

## 6. Dashboard model

`DashboardSnapshot` is a **projection only** (no persistence):

- Published Curricula
- Draft Curricula
- Pending Validation
- Pending Approval
- Recent Publications
- Recent Activity
- Publication Readiness

Built by `DashboardService` from in-memory workspaces, activity log, and checklist projections.

---

## 7. Domain foundation (V2-016A retained)

**Package:** `app/domain/curriculum_studio/`

- `StudioWorkflow` / `WorkflowStage` — Founder stage machine
- `PublicationChecklist` — computed from `WorkspacePublicationFacts`
- `ValidationSummary`, `PreviewSummary`, `PublicationSummary`
- `VersionHistory` / `VersionRecord` — local UX mirror only (not authority)
- `CurriculumDiff` — structural comparison

Checklist items are **never manually toggled**. Facts are written after successful port responses.

---

## 8. Architecture principles

1. **Products, not files** — workspaces represent educational product releases.
2. **Readiness first** — every path converges on “ready to publish?”
3. **Computed checklist** — never manual toggles.
4. **Ports only** — no imports of Management / Ingestion / Platform packages.
5. **Immutable DTOs** — never expose domain entities to UI.
6. **No second publication authority** — Management owns publish / archive / approve.
7. **No second version authority** — Management owns version lifecycle.
8. **Framework independence** — no Flask / SQLAlchemy / UI / persistence.

---

## 9. Success criteria (V2-016B)

| Criterion | Status |
|-----------|--------|
| Founder use-cases implemented | ✓ |
| Authority boundaries preserved | ✓ |
| Studio remains projection / orchestration | ✓ |
| Immutable DTO contracts | ✓ |
| Framework independent | ✓ |
| Ready for UI integration | ✓ |

---

## 10. Explicit non-goals

- Flask routes / blueprints
- HTML templates / CSS / JavaScript
- Database persistence / Alembic
- Modifications to Curriculum Management, Curriculum Ingestion, Education Platform, Student Digital Twin, Adaptive Decision Engine, or Learning Orchestrator
- Duplicating publication state, version lifecycle, validation logic, or preview generation as Studio authority
