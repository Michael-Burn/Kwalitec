# FV-001B Re-run — Terminology Audit

**Method:** Capture visible body text across login → Studio → workspace → Subjects → student orientation. Flag Educational Intelligence / internal architecture terms in the **primary** Founder workflow.

**Forbidden / sensitive terms scanned:** SCI, Runtime, Twin, Educational Decision, Educational Intelligence, Experience Model, Learner Lifecycle, Inference, CKG, Digital Twin, Preferred Authority, Knowledge Graph, Entity Details.

**Result:** `phases.json` → `term_hits: []` on the primary blind walk.

---

## Primary workflow language (good)

| Surface | Observed language |
|---|---|
| Sidebar | CURRICULUM AUTHORITY, Subjects, Curriculum Studio, Review Queue, Publishing, Versions, Quality |
| Studio | validate, preview, approve, publish |
| Uploads | Official CMP, Official Syllabus, Curriculum Master Pack |
| Actions | Validate Curriculum, Build Preview, Approve Curriculum, Publish Verified Curriculum |
| Catalogue | Ready after publish (explained in copy) |

---

## Problematic or opaque terms (visible)

| Term / pattern | Where | Severity | Notes |
|---|---|---|---|
| `entities · relationships` | Curriculum Structure tab | Minor | Internal graph wording in Founder review |
| `Uploaded by 38` | Document metadata | Minor | Numeric user id, not a person name |
| `sources_uploaded`, `workspace_opened` | Studio recent activity | Minor | Event keys, not Founder prose |
| `in_progress`, `not_ready`, `preview_ready` | Status chips / version suffix | Major (clarity) | Machine states shown raw beside human copy |
| `Platform Intelligence` | Console Home quick actions | Minor | Outside core Studio path |
| Topic labels containing prior subject codes (e.g. CS1R inside CS1U structure) | Structure tab | Major (trust) | Extracted titles reflect PDF text; confuses subject identity |

---

## Contradictory phrases (terminology of state)

These are wording failures even when individual words are Founder-friendly:

1. “We've built the preview **successfully**” vs “Preview needs attention · **not_ready**”
2. “**blocking findings** remain” vs “**0 validation errors**” / “Extracted curriculum **ready**”
3. Click **Approve Curriculum** → flash about **publish** failure

---

## Verdict

Primary chrome largely avoids Educational Intelligence jargon — **pass** for the EI-terminology acceptance criterion.

State language and action-attribution copy still **fail** Founder trust.
