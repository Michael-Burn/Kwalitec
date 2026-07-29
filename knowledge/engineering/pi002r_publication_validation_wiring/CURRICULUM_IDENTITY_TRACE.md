# Curriculum Identity Trace

**Programme:** PI-002R  
**Phase:** 2 — Validation Wiring / Identity

---

## Identity keys

For a Founder workspace, the following identifiers must remain aligned:

| Key | Owner | Flows through |
|---|---|---|
| `workspace_id` | Studio registry | All Studio services |
| `subject_code` | Management subject + Studio workspace | Upload, validate, publish, catalogue |
| `version_id` | Management version (mirrored on workspace) | Validate, preview, approve, publish |
| `version_label` | Management / Studio | Catalogue display |
| Structure ids (`section_ids`, `topic_ids`, `objective_ids`) | CIP / Foundation → StructurePreparation | Validate, Preview, Ready bridge |

---

## Trace (happy path)

```text
upload CMP/Syllabus
  → workspace.facts.cmp_uploaded / official_syllabus_uploaded
  → Management add_asset_ref(version_id, kind, reference)
  → CIP extraction (async) produces entities for workspace documents
  → NO stub Ingestion job registered

validate
  → StructurePreparation loads CIP/Foundation → workspace structure ids
  → Management validate_version(version_id)
  → workspace.facts.validation_passed = True
  → identity: workspace_id + version_id + structure ids

preview
  → hierarchy nodes derived from same structure ids
  → readiness ready_for_review iff validation_passed
  → identity: same workspace_id + structure node ids

approve
  → requires validation_passed
  → Management approve(version_id)
  → workspace.facts.preview_approved = True
  → identity: same version_id

publish
  → Management publish(version_id)
  → Foundation bridge on same subject_code / version_label / structure
  → workspace status = published
  → identity: same version_id → Foundation package

Ready / Subject Catalogue
  → active Foundation package for subject_code
  → no new curriculum invented
```

---

## Test evidence

`tests/application/curriculum_studio/test_pi002r_validation_wiring.py::test_curriculum_identity_flows_validate_preview_approve_publish`

Asserts:
- `version_id` stable across validate → approve → publish  
- Preview hierarchy contains validation structure ids  
- `validation_passed` and `preview_approved` remain true through publish  

---

## Defect definition

Any stage that introduces a different topic set, version, or synthetic stub as the gate input is a PI-002R defect.
