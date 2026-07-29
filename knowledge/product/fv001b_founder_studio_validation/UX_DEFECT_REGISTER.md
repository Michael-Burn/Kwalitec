# FV-001B — UX Defect Register

**Date:** 2026-07-28  
**Severity:** Critical = blocks publish/Ready · Major = confidence/path severely hurt · Minor = polish  
**Source:** Visible Founder Studio walkthrough only

---

## Critical

| ID | Defect | Evidence | Acceptance impact |
|---|---|---|---|
| C1 | Cannot complete publish of verified curriculum | Publish flash refuses; Studio **Published 0** | Publish ✗ · Ready ✗ |
| C2 | Preview reports 0 nodes / not_ready after “built successfully” | Workspace preview panel + success flash | Review ✗ · Trust ✗ |
| C3 | Validation state contradictions | Flash: could not complete validation; NEXT STEP: validation looks ready; panel: 0 validation errors | Extraction understanding ✗ |
| C4 | Official CMP / Syllabus documents appear in swapped slots | `official_syllabus.pdf` under CMP; `official_cmp.pdf` under Syllabus | Upload trust ✗ |
| C5 | No Founder-usable extraction review/correction surface | Review Queue hub empty of structure; 0 nodes | Review ✗ |

---

## Major

| ID | Defect | Evidence |
|---|---|---|
| M1 | Console Home does not lead with curriculum next action | Platform Health 0%, check-ins, Platform Intelligence |
| M2 | Open Workspace errors instead of opening existing workspace | Flash about single workspace / “dashboard” |
| M3 | Subject catalogue lacks Ready / Draft / Coming Soon confidence model | Stage crumbs only (`Content Sources`, `Validation`) |
| M4 | Engineering tabs on primary authoring UI | PIPELINE, KNOWLEDGE GRAPH, EVIDENCE EXPLORER, ENTITY DETAILS |
| M5 | Hub pages largely duplicate Studio empty shells | Review Queue / Publishing / Versions / Quality |
| M6 | `UPLOADED BY 1` exposes internal user id | Document cards |
| M7 | Checklist stuck at 3 of 8 without recoverable path to Ready | Workspace checklist panel |
| M8 | Pipeline claims graph relations while preview has 0 nodes | `graph_rebuilt · 32 relations` vs `0 nodes` |

---

## Minor

| ID | Defect | Evidence |
|---|---|---|
| m1 | Sign-in copy is student-study oriented | “Know exactly what to study next” |
| m2 | Activity feed uses snake_case event keys | `sources_uploaded:`, `subject_created:` |
| m3 | Duplicate stacked flash banners | Same message twice in capture |
| m4 | Mojibake in mapped topic titles | `Chapter 3 â Regression` |
| m5 | Create Subject Title not marked required | Only Subject code * |
| m6 | Document labels “Document 1/2/3/4” in pipeline | Not CMP/Syllabus names |

---

## Defects that are *not* defects (correct behaviour)

| Observation | Why kept |
|---|---|
| Publish blocked without approval/version | Protects students — good safety UX |
| Invite-only login (no self-register) | Explicit Internal Alpha policy |
| Subject not marked Ready when incomplete | Honest catalogue behaviour |

---

## Counts

- Critical: **5**
- Major: **8**
- Minor: **6**
