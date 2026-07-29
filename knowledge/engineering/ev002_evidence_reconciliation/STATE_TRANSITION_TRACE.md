# State Transition Trace

**Programme:** EV-002  
**Flags traced:** `validation_passed` → `preview_ready` / preview readiness → `preview_approved` → `published` → Ready catalogue.

---

## EV-001 (CS1V) — observed transitions

| Step | Evidence | Resulting state |
|---|---|---|
| Create | Workspace Subject / Active | Draft workspace |
| Upload + process | Docs Ready; preview cue `not_ready · 23 topics`; validation `not_started` | Structure present, not gated |
| Validate | UI `Validation completed successfully · passed` | **`validation_passed = true`** |
| Preview | `Preview ready · ready_for_review · 23 topics` | **Preview Ready** |
| Approve | Success flash; `Preview ready · approved · 23 topics` | **`preview_approved`** |
| Publish | Success flash; `Status: Published · Version 2026.1`; package row | **`published`** |
| Ready | Subjects hub Ready · Current Version · Published date | **Ready** |

DB end state (`/tmp/ev001_verify.sqlite3`): `publication_state=published`, active package id 1.

---

## FV-001B Final (CS1F) — observed transitions

| Step | Evidence | Resulting state |
|---|---|---|
| Create | Workspace Subject / Active | Draft workspace |
| Upload + process | Docs Ready; preview cue `not_ready · 26 topics`; validation `in_progress` | Structure present, not gated |
| Validate | Flash blocking findings; UI `Validation needs attention · in_progress` | **`validation_passed` remains false** |
| Preview | Flash “built successfully — 2 topics”; card `not_ready · 2 topics`; version text `preview_ready` | **No authoritative Preview Ready** |
| Approve | Publish-refusal flash; no approved confirmation | **`preview_approved` false** |
| Publish | Same refusal; checklist advances 4→5 of 8 without publish | **`published` false** |
| Ready | Subjects `2026.1 · Content Sources` | **Ready never reached** |

DB end state (`instance/kwalitec.sqlite3`): `publication_state=draft`, `stage=create_subject`, `parsed_structure_json` null, **no** published package.

---

## First divergence

| Flag / transition | EV-001 | FV-001B | First diverge? |
|---|---|---|---|
| Documents Ready | Yes | Yes | No |
| Structure extracted (CIP) | Yes | Yes | No |
| **`validation_passed`** | **True** | **False** | **YES — first** |
| Preview Ready (`ready_for_review`) | True | False (`not_ready`) | Consequent |
| `preview_approved` | True | False | Consequent |
| `published` | True | False | Consequent |
| Ready catalogue | True | False | Consequent |

---

## Cascade

```text
validation_passed = false
        ↓
preview cannot become ready_for_review (PI-002R semantics) / stays not_ready
        ↓
approve refused (requires validation / readiness)
        ↓
publish refused (requires approval + version gates)
        ↓
Ready never materialises
```

The contradictory FV preview flash and Approve→Publish copy are **presentation defects on a failed path**, not evidence that hidden state actually reached Ready.
