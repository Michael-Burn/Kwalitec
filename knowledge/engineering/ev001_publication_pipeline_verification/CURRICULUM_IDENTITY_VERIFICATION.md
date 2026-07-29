# Curriculum Identity Verification

**Programme:** EV-001  
**Question:** Was exactly one curriculum identity used from Upload through Ready / package materialisation?

---

## Identity chain (authoritative)

| Layer | Identifier |
|---|---|
| Subject code | `CS1V` |
| Studio workspace | `ws-cs1v` |
| Foundation subject id | `1` |
| Foundation version id | `1` |
| Version label | `2026.1` |
| Published package id | `1` |
| Package → version_id | `1` (same as Foundation version) |
| Package foundation_version_id (payload) | `1` |

Evidence: `_evidence/engineering_analysis.json` → `identity.same_identity_chain`.

---

## Stage consumption of the same instance

| Stage | Identity consumed | Evidence |
|---|---|---|
| Upload | `ws-cs1v` documents kind=cmp / syllabus | Active Foundation documents id 1–2 bound to workspace |
| Structure preparation | CIP entities for those document ids | 28 CIP entities; topics/subtopics=21; objectives=5 |
| Validation | Same workspace + version `2026.1` | UI validation pass; workspace URL remained `/workspaces/ws-cs1v` |
| Preview | Same structure hierarchy | Preview 23 topics; package structure topic_count=21 (+ subjects/title nodes visible as topics) |
| Approval | Same workspace facts → preview_approved | Preview line became `approved` without identity change |
| Publication | Same Foundation version published | `publication_state=published`; package version_id=1 |
| Ready | Same package projected to Subjects hub | Ready · Current Version 2026.1 |
| Student catalogue (data) | Same package via PublishedCurriculumAuthority | Active package CS1V / 2026.1 |

---

## Duplicate representation check

| Risk | Result |
|---|---|
| Synthetic Ingestion stub as publication authority | Not observed — reference uploads follow PI-002R (CIP owns extraction) |
| Second Foundation version for CS1V | None — single version row |
| Second active published package | None — single active package |
| Subjects hub Ready for a different subject code | N/A — CS1V only published in this verification DB |

---

## Structure consistency summary

| Metric | CIP entities | Package structure | Preview UI |
|---|---|---|---|
| Topics / subtopics | 21 | topic_count=21 | 23 nodes (includes subject/title nodes in hierarchy) |
| Learning objectives | 5 | objective_count=5 | Present in structure panels / package |
| Sections / subjects | 2 | section_count=2 | Present |

The Founder-visible hierarchy and the published package structure derive from the same CIP extraction for `ws-cs1v` documents — not from a separate stub curriculum.

---

## Conclusion

**Pass.** One curriculum identity (`CS1V` / `ws-cs1v` / version `2026.1` / Foundation version id `1`) flowed through Validation → Preview → Approval → Publication → Ready package.
