# Subject Comparison

**Programme:** EV-002  
**Sources:** EV-001 `engineering_analysis.json` / `lifecycle.json`; FV-001B Final `phases.json`; SQLite probes of `/tmp/ev001_verify.sqlite3` and `instance/kwalitec.sqlite3`.

---

## Identity matrix

| Attribute | EV-001 | FV-001B (Final) | Same? |
|---|---|---|---|
| Subject code | `CS1V` | `CS1F` | **No** |
| Title | CS1V — Actuarial Statistics (EV-001 Verification) | CS1F — Actuarial Statistics (FV-001B Final) | **No** |
| Workspace id | `ws-cs1v` | `ws-cs1f` | **No** |
| Foundation subject id | `1` (sole subject in EV DB) | `4` (after CS1R/CS1S/CS1U) | **No** |
| Version label | `2026.1` | `2026.1` | Yes (label only) |
| Foundation version id | `1` | `4` | **No** |
| Lifecycle after walk | `publication_state=published`, `stage=publish` | `publication_state=draft`, `stage=create_subject` | **No** |
| Active published package | id `1`, CS1V / 2026.1 | **None** | **No** |
| Authority package | Active `PublishedPackageSnapshot` for CS1V | No active package for CS1F | **No** |
| Blueprint assignment (end state) | Publication completed (implies gates cleared) | Never validated → blueprints not publication-ready | **No** |
| Curriculum identity chain | Single chain CS1V → ws-cs1v → version 1 → package 1 | Single chain CS1F → ws-cs1f → version 4; **no package** | Different instances |

---

## Document / CIP summary

| Metric | EV-001 (CS1V) | FV-001B (CS1F) |
|---|---|---|
| CMP bytes / sha256 prefix | 1844 / `b7b33a78a7635089` | 2059 / `84e1748ee96fb2e0` |
| Syllabus bytes / sha256 prefix | 1731 / `68b4204d62b21513` | 1597 / `44a0164c287af316` |
| Active doc ids | 1 (cmp), 2 (syllabus) | 6 (cmp), 7 (syllabus) |
| CIP topics+subtopics | 21 | 24 (12 topic + 12 subtopic) |
| CIP learning_objectives | 5 | 12 |
| CIP subjects | 2 | 2 |
| CIP syllabus `missing_learning_objective` | warning on doc 2; report `passed=1` | warning on doc 7; report `passed=1` |

---

## Conclusion

Subjects are **different curriculum instances** with **different PDF bytes** and **different end lifecycles**. Shared version *label* `2026.1` is coincidental naming, not shared identity.
