# PI-001B — Educational Engine Foundation

## Summary

PI-001B introduces a deterministic derivation layer that turns a **published curriculum package** into student-learning artefacts without replacing the live JSON runtime yet.

Current compatibility path remains:

```text
Bundled JSON → CurriculumRepository → CurriculumService / StudyPlanService / PlanningService
```

New additive path is:

```text
PublishedCurriculumAuthority
    → EducationalEngineFoundationService
    → EducationalArtefactDeriver
    → Derived artefacts:
         - Curriculum graph
         - Study plan template
         - Mission templates
         - Journey structure
         - Progress model
```

## Layering

| Layer | Package | Responsibility |
|---|---|---|
| Domain | `app/domain/educational_engine_foundation/` | Pure deterministic derivation rules |
| Application | `app/application/educational_engine_foundation/` | Published-package access + snapshot emission |
| Existing foundation | `app/application/curriculum_studio_foundation/` | Publish-only authority and package production |
| Existing student runtime | `app/services/` | Remains authoritative until cutover evidence exists |

## Design decisions

1. **Published curriculum stays the SSOT**  
   PI-001B derives artefacts only from `PublishedCurriculumPackage.package_json`.

2. **No duplicate authored curriculum**  
   Study plans, missions, journey, and progress structures are generated from the published hierarchy and prerequisite edges.

3. **Backward compatibility first**  
   Existing student behaviour is untouched. No cutover of `CurriculumService`, study plan wizard, mission generation, or readiness denominator happens in this milestone.

4. **Published package fidelity is improved**  
   PI-001A publication now preserves:
   - prerequisite edges
   - normalized metadata
   - ordered section/topic/objective structure
   - entry attributes needed by ingestion

5. **Deterministic ordering law**  
   Topic order is the published curriculum order unless prerequisite edges require a later topic to move behind its dependencies.

## Derived artefacts

### Curriculum graph

- Topic nodes derive from published topics
- `REQUIRES` edges derive from published prerequisite edges
- Uses existing `CurriculumGraph` foundation for deterministic topological ordering

### Study plan template

- One ordered topic template per curriculum topic
- Includes recommended minutes and prerequisite references

### Mission templates

- At least one mission template per topic
- Bound to the topic and its objectives
- No actuarial-only “Core Reading” assumptions are introduced here

### Journey structure

- Section → Topic → Objective hierarchy from the published curriculum

### Progress model

- Trackable section/topic/objective ids
- Topic-to-objective membership
- Topic prerequisite references

## Migration strategy

### Phase 1 — additive derivation

- Publish richer package structure
- Derive educational artefacts from published packages
- Prove CS1 equivalence against current JSON ordering/hierarchy

### Phase 2 — runtime authority bridge

- Introduce a runtime authority that can prefer published packages for founder-onboarded subjects
- Keep bundled JSON as fallback for existing subjects

### Phase 3 — safe service cutovers

- Study plan discovery/version support
- Curriculum import/binding
- Mission generation
- Journey projection
- Readiness denominator scoping

Each cutover must be evidence-backed and reversible until equivalence is demonstrated.
