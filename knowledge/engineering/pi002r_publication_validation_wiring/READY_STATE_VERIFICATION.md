# Ready State Verification

**Programme:** PI-002R  
**Phase:** 7 — Ready State

---

## Ready definition

Ready is **not** an independent Studio computation.

```text
validated → previewed → approved → published → Foundation package active
                                                      ↓
                                              Subject Catalogue Ready
```

---

## Wiring

| Step | Fact / state | Authority |
|---|---|---|
| Validated | `workspace.facts.validation_passed` | Management validate + structure prep |
| Preview Ready | Preview readiness `ready_for_review` | Same structure + validation_passed |
| Approved | `workspace.facts.preview_approved` | Management approve |
| Published | Management `publication_state=published` + workspace `PUBLISHED` | Management publish |
| Ready | Active Foundation `PublishedCurriculumPackage` | `PublicationBridgeService` |
| Catalogue | Discovery / Subjects hub columns | Foundation package projection |

---

## Guarantees

1. No duplicate Ready calculator in Studio checklist beyond publication facts  
2. Catalogue does not invent curriculum — reflects published package  
3. Bridge uses `StructurePreparationService.structure_dict` when Foundation parse is empty  
4. Unit paths without Foundation documents still allow Management publish (bridge skipped with warning) — production Founder path has Foundation documents from upload  

---

## Engineering verification required (next)

Before FV-001B re-run, manually or via script confirm one subject:

| Transition | Evidence |
|---|---|
| Draft | Workspace created, documents uploaded |
| Validated | `validation_passed`, findings consistent |
| Preview Ready | Preview flash success + `ready_for_review` |
| Approved | Approve success flash + `preview_approved` |
| Published | Publish success + Management published |
| Ready | Subjects hub Ready + Student Catalogue discovers subject |

---

## Out of scope hardening (not blockers)

- Persist StudioRegistry across processes  
- Lifecycle label cleanup (Management mid-states labelled READY)  
- Publish ordering polish for rollback-before-assert
