# Object Model

**Programme:** DX-004B  
**Status:** Binding for Subject object permanence  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-002, DX-003 Terminology Dictionary  

---

## 1. Purpose

Define the **Subject** as a stable product object so it is recognised identically across every Founder surface. Recognition fails when the same curriculum is presented as different shapes, names, or status languages on Catalogue vs Workspace vs Publish.

---

## 2. Canonical object: Subject

| Attribute | Definition |
|---|---|
| **Noun** | **Subject** |
| **Meaning** | Official curriculum offering under operator control |
| **Forbidden nouns** | Course, Module (as top-level), Exam product, Curriculum (as catalogue row label) |
| **Identity** | Stable id + human **Subject name**; optional **subject code** (quiet) |
| **Lifecycle owner** | Subjects catalogue (discovery) + Workspace (execution) |

Student catalogue also uses **Subject** for Ready offerings — same noun, different shell (Student). Operator Subjects may include non-Ready work; student catalogue shows Ready only.

---

## 3. Object permanence contract

A Subject **must** present the same:

| Dimension | Rule |
|---|---|
| **Name** | Identical string across Catalogue, Workspace header, Review, Publish, History |
| **Code** | If shown, same code; never invent display aliases per surface |
| **Status vocabulary** | Shared dictionary (below); no surface-specific synonyms |
| **Row / header shape** | Name dominant; stage/status secondary; no reinvented card heroes |
| **Open target** | Always the subject’s operational workspace (not a per-surface mini-home) |

```
Catalogue row  ──Open──►  Workspace (same Subject)
                           │
                           ├── Review stage (same Subject)
                           ├── Publish stage (same Subject)
                           └── History / versions (same Subject)
```

Never:

- Redesign Subject as a “hub card” on one page and a “pipeline chip” on another without shared identity fields  
- Rename to “Workspace” in the catalogue (workspace is the execution container; subject is the offering)  
- Show different titles for the same id  

---

## 4. Related objects (do not conflate)

| Object | Role | Relationship to Subject |
|---|---|---|
| **Workspace** | Operational execution container for a subject’s pipeline | Opened from Subject; not a second catalogue entry |
| **Document** | Syllabus / CMP source | Belongs to workspace; not a catalogue row |
| **Publication** | Release event / outcome | Status on Subject becomes Ready for students |
| **Version** | Immutable snapshot of published curriculum | Reachable via More / History — not a parallel catalogue of Subjects |
| **Finding** | Blocking or advisory issue | Workspace / Review concern — not catalogue KPI |

Catalogue rows are **Subjects**, not workspaces-as-products. If one subject has one active workspace in Alpha, the row still represents the Subject; Open enters that workspace.

---

## 5. Status dictionary (operator catalogue)

Align DX-003 status system. Quiet text; semantic colour only when needed.

| Catalogue status | Meaning | Actionable? |
|---|---|---|
| **In progress** | Active pipeline work; not Ready | Open → continue |
| **Ready to publish** | Gates cleared; publish next | Open → Publish stage |
| **Published** / student **Ready** | Released; students may see Ready | Open → maintain / version |
| **Archived** | Hidden from default browse | Filter; restore via More |
| **Documents** / stage name | Prefer current **stage** as progress when more precise | Open → stage |

Prefer **stage name** (Documents, Structure, Validation, Approval, Publish) as the “where is it?” column when it is more precise than a coarse status. Do not show both a verbose essay and a duplicate badge.

**Student-facing availability** uses **Ready** / **Coming Soon** only on student surfaces — not as operator catalogue decoration essays.

---

## 6. Identity fields (catalogue DTO)

Minimal projection for L0/L2:

| Field | Required | Notes |
|---|---|---|
| `subject_id` | Yes | Stable |
| `name` | Yes | Display primary |
| `code` | Optional | Quiet secondary |
| `stage` | Yes | Current pipeline stage |
| `publication_status` | Yes | In progress / Ready to publish / Published / Archived |
| `updated_at` | Yes | Drives default sort + Updated column |
| `created_at` | Yes | Sort: Recently created |
| `published_at` | Optional | Sort: Recently published |
| `owner` | Optional | Multi-operator only |
| `workspace_href` | Yes | Open target |

No KPI aggregates on the Subject object for catalogue display.

---

## 7. Cross-surface rendering rules

| Surface | Subject presentation |
|---|---|
| **Subjects (catalogue)** | Row: name + stage + updated + status |
| **Home (DX-004A)** | Current Work / queue: same name + stage |
| **Workspace** | Header: same name (+ code); stage in pipeline chrome |
| **Review / Publish** | Same name in context header |
| **History** | Same name as object of record |

If Home and Subjects disagree on name or stage for the same id, that is a defect — not a design variant.

---

## 8. Create Subject

Creating a Subject:

1. Establishes the catalogue object (system of record)  
2. Establishes (or links) the operational workspace  
3. Lands the Founder in the workspace — not on a summary interstitial  

Create is the only Primary on Subjects because origin of every curriculum object is this catalogue.

---

## 9. Success test (permanence)

Show a Founder the same Subject on Catalogue and Workspace (and Home Current Work). They must say it is the **same** object without reconciling different titles or status languages.
