# Persistent Context Spec

**Programme:** DX-004C  
**Status:** Binding for workspace identity header  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-004B `OBJECT_MODEL.md`, DX-003 Terminology  

---

## 1. Purpose

The Founder must never lose track of **which Subject** they are executing. Persistent context is the identity anchor for the entire workspace session.

---

## 2. Always visible fields

| Field | Required | Example | Visual role |
|---|---|---|---|
| **Subject code** | Yes when available | CS1 | Quiet leading identity |
| **Subject name** | Yes | Probability | Dominant title |
| **Version label** | Yes when available | 2026.1 | Quiet secondary |
| **Current stage** | Yes | Validate | Quiet secondary; matches stage strip |

Example rendering:

```
CS1
Probability
Version 2026.1 · Current stage: Validate
```

Or single block:

```
CS1 · Probability
Version 2026.1 · Current stage: Validate
```

---

## 3. Invariants

| Rule | Detail |
|---|---|
| **Never changes role** | Header is always identity + stage — not a KPI strip, not a nav hub |
| **Object permanence** | Name and code match Subjects catalogue and Home Current Work (DX-004B) |
| **No aliases** | Do not retitle “Workspace: Probability Draft Pipeline” |
| **Stage sync** | Current stage in header equals stage strip active step |
| **Version sync** | Version matches the workspace version under edit |

If Home, Subjects, and Workspace disagree on name/stage for the same id, that is a defect.

---

## 4. Forbidden in persistent context

- Participant counts, Alpha health, platform pulse  
- Multiple CTAs  
- “Welcome back” / tutorial copy  
- Progress percentage / wheels  
- Workspace UUID as primary display (belongs in L3)  
- Owner essays (owner may appear in L3 if multi-operator)  

---

## 5. DTO fields (workspace header)

| Field | Source | Notes |
|---|---|---|
| `subject_id` | Workspace | Stable |
| `subject_code` | Subject | Display |
| `subject_name` / `subject_title` | Subject | Display primary |
| `version_label` | Workspace version | Display |
| `current_stage` | Workflow | Founder stage label |
| `publication_status` | Derived | Optional quiet; prefer stage |

Technical ids (`workspace_id`) → L3 only.

---

## 6. Sticky behaviour

| Viewport | Behaviour |
|---|---|
| Desktop | Prefer sticky persistent context so identity remains while scrolling L1 |
| Narrow | Persistent context at top; may scroll; stage + Primary stay early in focus order |

Sticky must not obscure the Primary.

---

## 7. After stage change

On advance/retreat:

1. Update `Current stage` text immediately.  
2. Update stage strip active marker.  
3. Replace Primary label.  
4. Do **not** remount a different page chrome that feels like a new product.

---

## 8. Success test

Cover the L1 content. From the header alone, the Founder must answer:

1. Which subject?  
2. Which version?  
3. Which stage?
