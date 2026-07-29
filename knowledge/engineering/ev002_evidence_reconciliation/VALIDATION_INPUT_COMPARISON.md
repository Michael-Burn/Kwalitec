# Validation Input Comparison

**Programme:** EV-002  
**Question:** Did validation evaluate the same curriculum?

---

## Answer

**No.** Validation evaluated different subjects, different PDF bytes, and different CIP graphs — on different databases / processes.

---

## Inputs at Validate click

| Input | EV-001 CS1V | FV-001B CS1F |
|---|---|---|
| Workspace | `ws-cs1v` | `ws-cs1f` |
| Version label | `2026.1` | `2026.1` |
| Package id (published) | N/A at validate; later package `1` | Never published |
| Authority (publication) | None yet → later CS1V package | None |
| CMP PDF | 5 chapters; **1** `Learning objective:` per chapter | 6 chapters; **2** `Learning objective:` per chapter |
| Syllabus PDF | 5 sections / 10 numbered items | 6 sections / 12 numbered items |
| CIP topic+subtopic count | 21 | 24 |
| CIP learning_objectives | 5 (all on CMP) | 12 (all on CMP) |
| Syllabus CIP LO warning | Present (`missing_learning_objective`, severity warning, report passed) | Present (same pattern on doc 7) |
| Pre-validate UI topic cue | ~23 | ~26 |
| Post-validate UI topic cue | 23 (stable into preview ready) | Collapsed to **2** with failed validation |

---

## Prepared structure

| | EV-001 | FV-001B |
|---|---|---|
| After successful validate | Structure consumed by preview (23 UI nodes); later package `topic_count=21`, `objective_count=5` | Validate failed; foundation `parsed_structure_json` remains **null**; stage stays `create_subject` |
| Blueprint / Management gate | Cleared (validation_passed → approve → publish) | Not cleared (`validation_passed` never true) |

---

## Shared vs different

**Shared pattern:** Syllabus documents lack CIP learning_objective entities → CIP warning `missing_learning_objective` while CMP carries LOs. On EV-001 this warning is **non-blocking** and validation still passes.

**Different:** Absolute curriculum graphs, PDF hashes, subject identity, DB, and — decisively — the **runtime code image** applying Management / Structure Preparation gates (see [`ENVIRONMENT_COMPARISON.md`](ENVIRONMENT_COMPARISON.md)).

---

## Conclusion

Validation did **not** evaluate the same curriculum instance. Even the “same shape” warning on syllabus LOs does not explain EV pass vs FV fail by itself; environment + process code image do.
