# CS1 Begin Learning Investigation

**Date:** 2026-07-30  
**Scope:** Evidence-only — no application code changes  
**Subject under investigation:** `CS1` (Actuarial Statistics)  
**Reported symptom:** Begin Learning surfaces  
`Published Curriculum must include sections, topics and objectives.`  
**Canonical exception text (code):**  
`published curriculum must include sections, topics, and objectives`  
**Evidence DB:** `sqlite:////Users/kwalitec/Developer/kwalitec/instance/kwalitec.sqlite3`  
**Git HEAD at investigation:** `ee1101d`

---

## Verdict (executive)

Against the local development database that Student Runtime uses when `DATABASE_URL` is unset:

1. Begin Learning loads **Published Curriculum Package id=1** (`CS1` / `2026.1`, active).
2. That package **already contains** hierarchy: **5 sections · 15 topics · 73 objectives**.
3. `EducationalArtefactDeriver.derive(...)` **succeeds** (`CS1:2026.1`).
4. Therefore the reported message is **not reproduced** against this local active package.

The message is raised **only** when `package["structure"]` has an empty/missing `sections`, `topics`, or `objectives` **list**. It is not raised by empty metadata counts alone, and it is not raised by the legacy JSON ORM `curricula` table.

If the operator is still seeing the message, the failure is environmental (different host/DB, stale process, or a package state that is not this local row) — not a present local hierarchy omission on package id=1.

---

## Message origin

| Item | Value |
|---|---|
| Exact string | `published curriculum must include sections, topics, and objectives` |
| Module | `app/domain/educational_engine_foundation/derivation.py` |
| Class | `EducationalArtefactDeriver.derive` |
| Condition | `not raw_sections or not raw_topics or not raw_objectives` after reading `package["structure"]` |
| Call chain (Begin Learning) | `study_plan.review_post` → `FounderStudentEnrolmentBridge.enrol` → `EducationalRuntimeEngineService.enrol_student` → `EducationalEngineFoundationService.derive_from_package` → `EducationalArtefactDeriver.derive` |

```153:156:app/domain/educational_engine_foundation/derivation.py
        if not raw_sections or not raw_topics or not raw_objectives:
            raise EducationalDerivationError(
                "published curriculum must include sections, topics, and objectives"
            )
```

**Surfacing note:** `EducationalDerivationError` subclasses `ValueError`. The enrolment bridge only wraps `PublishedCurriculumUnavailable` into `BridgeEnrolmentBlocked` (flashed as warning). An empty-structure derive failure therefore propagates as an **unhandled exception** (HTTP 500 / debugger page text), which FV-002 dogfood scripts also scanned for in page body + flashes.

---

## Evidence checklist (requested items)

### 1. Which Published Curriculum record is being loaded

Student Runtime loads the **active** `PublishedCurriculumPackage` for subject code `CS1` via `PublishedCurriculumAuthority.get_active("CS1")`.

| Field | Value |
|---|---|
| Table | `published_curriculum_packages` |
| Selection | `subject_code='CS1' AND is_active=True` ordered by `published_at DESC` |
| Row loaded | **id=1** |
| Subject | `CS1` |
| Version label | `2026.1` |
| Active | `true` |
| Published by | `rr001` |
| Published at | `2026-07-29 22:21:01.531710` (row upserted by later RR-001 publishes; payload is current) |
| Structure source | `certified_snapshot` |
| Curriculum identity after derive | `CS1:2026.1` |

Only one published package exists in this DB (any subject). There is no alternate active CS1 row to confuse Runtime.

### 2. Published Curriculum ID

**`published_curriculum_packages.id = 1`**

### 3. Curriculum ID

Runtime C does **not** use the legacy ORM `curricula.id` for Begin Learning. Relevant identifiers:

| Identity | Value | Role |
|---|---|---|
| Published package id | **1** | Student-consumable SSOT row |
| Foundation version id (`version_id` / `foundation_version_id`) | **5** | Studio Foundation curriculum version materialised into the package |
| Foundation subject PK (`studio_foundation_subjects.id`) | **5** | Parent of version 5 |
| Workspace | `ws-cs1` | Studio workspace bound to CS1 |
| Legacy ORM `curricula.id` for `IFoA CS1` v2026 | **1** | JSON Runtime A import — **not** consulted by Runtime C enrol/derive |

### 4. Publication version

**`version_label = 2026.1`** (Foundation version id **5**, stage `publish`, publication_state `published`).

### 5. Certification status

From `package_json.certification` (and matching workspace columns):

| Field | Value |
|---|---|
| `authority` | `certified_snapshot` |
| `status` | `CERTIFIED_WITH_WARNINGS` |
| `snapshot_id` | `snap-ae1eaf5e82aabf58` |
| `chain_id` | `ei-chain-ws-cs1` |
| Workspace `certification_status` | `CERTIFIED_WITH_WARNINGS` |
| EI certification decision | `cert-941329e077dca20b` · outcome `CERTIFIED_WITH_WARNINGS` · quality **95.79** |

`PublishedCurriculumAuthority._runtime_accepts` accepts this package (`authority=certified_snapshot` and/or status `certified_with_warnings`).

### 6–8. Hierarchy counts in the published package

| Artefact | Count in `package.structure` |
|---|---:|
| Sections | **5** |
| Topics | **15** |
| Learning objectives | **73** |

Metadata mirrors lists: `section_count=5`, `topic_count=15`, `objective_count=73`.

Sample shape (flat lists required by deriver — not nested V2 JSON):

- sections: `{section_id, code, title, number, order_index, ...}`
- topics: `{topic_id, title, section_ref, ...}`
- objectives: `{objective_id, text, topic_ref, ...}`

### 9. Whether counts match the certified curriculum

**Yes — for the certified Gen7 snapshot projection used at publish.**

Active non-rejected nodes on `snap-ae1eaf5e82aabf58`:

| Node kind | Count | Maps to package field |
|---|---:|---|
| `chapter` | 5 | sections (via Founder Preview `_SECTION_KINDS` including `chapter`) |
| `concept` | 15 | topics (via `_TOPIC_KINDS` including `concept`) |
| `learning_objective` | 73 | objectives |

Metrics JSON on the same snapshot reports `chapters=5`, `sections=0`, `topics=15`, `objectives=73`. The metrics label “sections” means kind=`section` only; publish projection correctly treats **chapters as sections**, so package sections=5 matches educational chapters=5.

**Does not match** legacy ORM `IFoA CS1` v2026 (`curricula.id=1`): 5 / 14 / 72. That table is a different SSOT (bundled JSON import) and is irrelevant to Runtime C Begin Learning.

### 10. SQLAlchemy relationships used

**Published package model has no ORM relationships.**

```230:265:app/models/curriculum_studio_foundation.py
class PublishedCurriculumPackage(db.Model):
    ...
    id: int = db.Column(db.Integer, primary_key=True)
    subject_code: str = db.Column(db.String(64), nullable=False, index=True)
    version_id: int = db.Column(db.Integer, nullable=False, unique=True)
    version_label: str = db.Column(db.String(64), nullable=False)
    package_json: str = db.Column(db.Text, nullable=False)
    is_active: bool = db.Column(db.Boolean, nullable=False, default=True, index=True)
```

`PublishedCurriculumPackage.__mapper__.relationships` → **empty**.

Related models / FKs involved in the wider flow:

| Model | Relationships / FKs |
|---|---|
| `StudioFoundationSubject` | `versions` → `StudioFoundationVersion` |
| `StudioFoundationVersion` | `subject` → subject; `documents` → `StudioFoundationDocument` |
| `StudioFoundationDocument` | `version` → version |
| `RuntimeEnrolment` | FK `published_package_id` → `published_curriculum_packages.id` (no `relationship()` declared) |
| `StudioWorkspaceProjection` | Standalone projection row (`workspace_id=ws-cs1`); no FK to published packages |

Authority does **not** join Foundation versions via relationship. It reads the published row, `json.loads(package_json)`, and returns a DTO.

Publication **writes** structure from `StudioFoundationVersion.parsed_structure_json` (and documents via `version.documents` relationship) inside `CurriculumStudioFoundationService.publish_curriculum`.

### 11. Student Runtime query

Authority query (what Begin Learning / Runtime C uses):

```python
PublishedCurriculumPackage.query.filter_by(
    subject_code=code,  # "CS1"
    is_active=True,
).order_by(PublishedCurriculumPackage.published_at.desc()).first()
```

Source: `PublishedCurriculumAuthority.get_active` in  
`app/application/curriculum_studio_foundation/authority.py`.

Enrol path then:

```python
package = self._authority.get_active(code)
snapshot = self._artefacts.derive_from_package(package.package)
```

Source: `EducationalRuntimeEngineService.enrol_student` in  
`app/application/educational_runtime_engine/service.py`.

HTTP entry: `POST /study-plan/review` → `FounderStudentEnrolmentBridge.enrol` when bridge selects Runtime C.

### 12. Publication query / materialisation

Foundation publish (no SELECT of published row for structure — structure comes from the version):

```python
version = StudioFoundationVersion.query...  # _require_version(version_id)
structure = json.loads(version.parsed_structure_json)
package = {
    "subject_code": version.subject.subject_code,  # relationship: version.subject
    "version_label": version.version_label,
    "foundation_version_id": version.id,
    "structure": structure,
    "documents": [... for d in version.documents ...],  # relationship
    "certification": {...},
}
# upsert PublishedCurriculumPackage by (subject_code, version_label)
```

Before that, `PublicationBridgeService._ensure_structure` rebuilds `parsed_structure_json` from `StructurePreparationService.structure_dict(workspace_id)` (certified dual-read preferred).

### 13. Root-cause determination

| Hypothesis | Against local active CS1 package id=1 | Notes |
|---|---|---|
| Publication omitted hierarchy | **Rejected** | Structure lists are 5 / 15 / 73; derive OK |
| Runtime loads wrong publication | **Rejected** | Only one published row; `get_active("CS1")` returns id=1 with matching certification |
| Validation checks wrong object | **Rejected** | Deriver validates the same `package` dict loaded from `package_json` (not ORM `curricula`, not workspace `structure_json` id-lists) |
| **Another root cause** | **Conditional** | See below |

#### What actually raises the message

The deriver requires **flat non-empty lists**:

```python
structure = package.get("structure") or {}
raw_sections = tuple(structure.get("sections") or ())
raw_topics = tuple(structure.get("topics") or ())
raw_objectives = tuple(structure.get("objectives") or ())
```

Reproduced negative controls (same exception text):

| Payload shape | Result |
|---|---|
| `sections/topics/objectives` all `[]` | **FAIL** — exact message |
| Nested V2-only (`sections[].topics[].learning_objectives`) with empty top-level topics/objectives | **FAIL** — exact message |
| Workspace-style id lists only (`section_ids` / `topic_ids` / `objective_ids`) | **FAIL** — exact message |

#### Historical context (when this message was a live Begin Learning blocker)

- FV-002 dogfood scripts explicitly treated this string as Begin Learning failure (`D-BEGIN`).
- PL-001A / RR-001 documented publication integrity defects where republish/`validate_curriculum` could overwrite certified `parsed_structure_json` (C1/C2). RR-001 cut over the active package to certified **5 / 15 / 73** with `certification.authority=certified_snapshot`.
- Local package `published_by=rr001` and certification block match that cutover.

#### Current local conclusion

For **this** DB, Begin Learning’s derive gate would **pass**. The reported symptom is therefore **not explained by missing hierarchy on the active CS1 published package**.

If the message is observed on another host (e.g. production after a publish that materialised empty or wrong-shaped `structure`), the failure mode is: **published `package_json.structure` lacked flat sections/topics/objectives lists** at enrol time — not a wrong Runtime query, and not validation of the legacy `curricula` ORM row.

Production was not queried in this investigation (`DATABASE_URL` unset locally; no Render CLI credentials in session). RC-001 notes student Ready catalogue starts empty until Founder publishes on the deployed DB.

---

## Path diagram

```text
Student UI: Begin Learning (POST /study-plan/review)
  → FounderStudentEnrolmentBridge.enrol (Runtime C)
    → EducationalRuntimeEngineService.enrol_student
      → PublishedCurriculumAuthority.get_active("CS1")
           SELECT published_curriculum_packages
           WHERE subject_code='CS1' AND is_active=1
           ORDER BY published_at DESC
      → EducationalEngineFoundationService.derive_from_package(package_dict)
           → EducationalArtefactDeriver.derive
                reads package["structure"]["sections"|"topics"|"objectives"]
                raises EducationalDerivationError if any list empty
```

Publication path (Founder):

```text
PublicationBridgeService.publish_to_catalogue(ws-cs1)
  → StructurePreparationService.structure_dict (certified snapshot dual-read)
  → StudioFoundationVersion.parsed_structure_json = structure_dict
  → CurriculumStudioFoundationService.publish_curriculum(version_id=5)
       upserts published_curriculum_packages (id=1)
```

---

## Reproduce commands (read-only)

```bash
# Inspect active CS1 package + derive
python - <<'PY'
from app import create_app
from app.application.curriculum_studio_foundation.authority import PublishedCurriculumAuthority
from app.domain.educational_engine_foundation.derivation import EducationalArtefactDeriver

app = create_app()
with app.app_context():
    snap = PublishedCurriculumAuthority().get_active("CS1")
    assert snap is not None
    st = snap.package.get("structure") or {}
    print(snap.package_id, snap.version_label, snap.package.get("certification"))
    print(len(st.get("sections") or []), len(st.get("topics") or []), len(st.get("objectives") or []))
    b = EducationalArtefactDeriver().derive(snap.package)
    print("DERIVE OK", b.curriculum_identity, len(b.sections), len(b.topics), len(b.objectives))
PY
```

Observed result during this investigation:

```text
1 2026.1 {'authority': 'certified_snapshot', ... 'status': 'CERTIFIED_WITH_WARNINGS'}
5 15 73
DERIVE OK CS1:2026.1 5 15 73
```

---

## Application code

**Not modified.** No fixes implemented.

---

## Recommended next proof steps (still no code changes)

1. Capture the exact host/DB where Begin Learning fails (`DATABASE_URL` / Render service) and dump `published_curriculum_packages` for `CS1` the same way as above.
2. If production package `structure` lists are empty or id-list shaped, treat as **publication materialisation** defect on that environment (republish with certified dual-read), not a Runtime query bug.
3. If production has no published row, Begin Learning should not reach this deriver message via Ready catalogue — investigate catalogue/routing instead.
