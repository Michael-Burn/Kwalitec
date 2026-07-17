# V1SP-001D — Founder Vision Journal

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001D  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Commit:** `7f3610a` — `feat(founder): add Founder Vision Journal for strategic product memory (V1SP-001D)`  

---

## Summary

V1SP-001D delivers the **Founder Vision Journal** — the structured strategic memory of Kwalitec and the official birthplace of future product capabilities.

The Founder Command Centre already answered *what is happening* and *what needs attention*. The Journal adds *where the product is going*: calm, searchable, Founder-only capture of ideas before they become architecture or implementation.

It is not a diary, chat surface, or free-form notebook. Each entry is a structured decision object with lifecycle, version targeting, relationships, promotion placeholders, and exportable history.

---

## Journal Model

`VisionEntry` (`app/models/vision_journal.py`) stores:

| Field | Purpose |
|---|---|
| Title | Short name of the idea |
| Description | Full statement of the capability |
| Reason | Why it matters now |
| Potential Value | Critical / High / Medium / Low / Exploratory |
| Expected Impact | What changes for Founder or student |
| Target Version | Version 1.x / 2 / 3 / Future / Unknown |
| Category | Fixed V1 taxonomy (configurable later) |
| Status | Lifecycle workflow (see below) |
| Tags | Multi-tag CSV (searchable) |
| Author | Founder user id |
| Future Milestone | Optional milestone link |
| Created / Updated | Audit timestamps |
| Deleted at | Soft-delete marker |

Supporting tables:

- `vision_entry_status_transitions` — append-only status history  
- `vision_entry_relations` — optional `depends_on` / `related_to` links  
- `vision_entry_promotions` — architecture placeholders (traceability only)

### Categories

Educational Intelligence, Student Experience, Founder Experience, Analytics, Student Digital Twin, Assessment, Revision, Infrastructure, Security, Performance, Brand, Research, Operations, Other.

### Status workflow

```
Vision → Research → Validated → Planned → In Development → Implemented
                 ↘ Rejected / Archived
```

Status changes never overwrite history; each transition appends a row.

### Version targets

Version 1.x, Version 2, Version 3, Future, Unknown — Version 2 is not hard-coded as the only destination.

---

## Search

`VisionJournalService.search` supports combined criteria:

- Free-text query across title, description, category, status, target version, tags  
- Filters: category, status, target version, tag, author  
- Sort: Newest, Oldest, Recently Updated, Target Version, Status, Category, Highest Potential Value  

Designed for hundreds of entries (indexed columns + in-process sort for ranked value). Soft-deleted entries are excluded by default.

---

## Relationships

Entries may optionally link with:

- **depends on** — e.g. Learning Confidence Engine depends on Learning Object Model  
- **related to** — e.g. Revision Workspace related to Revision Analytics  

Links are displayed on the entry detail page. **No dependency validation** is performed (out of scope).

---

## Dashboard

Founder Overview includes four compact Vision widgets:

1. Recent Vision Entries  
2. Ideas Awaiting Validation (`vision` / `research`)  
3. Ideas Planned for Next Version (`planned` / `validated` × Version 1.x / 2)  
4. Recently Promoted Ideas (placeholder refs)

Primary Command Centre navigation now:

Overview · Operational Health · Feedback · Research · **Vision Journal** · Releases · Settings  

Secondary operational destinations (Attention, Findings, Internal Alpha, Participants) remain reachable from Overview / Operational Health.

---

## Export

`/founder/vision/export/<fmt>` supports:

| Format | MIME | Use |
|---|---|---|
| Markdown | `text/markdown` | Human-readable strategic backup |
| JSON | `application/json` | Structured interchange |
| CSV | `text/csv` | Spreadsheet review |

Exports honour the current search/filter query string.

---

## Promotion

**Promote to Development** creates a `VisionEntryPromotion` placeholder (e.g. `ARCH-PLACEHOLDER-<id>-<slug>`). It does **not** create tickets or implementation work. Optionally advances status to `in_development` for traceability.

---

## Permissions

All Vision Journal routes use `@founder_required`. Students receive 403. No multi-user editing. Soft-delete and archive require confirmation; permanent hard-delete is not offered in V1.

---

## Tests

```bash
python3 -m pytest tests/test_v1sp001d_vision_journal.py -v
python3 -m pytest tests/test_iahf003_founder_command_centre.py -v
python3 -m ruff check app/models/vision_journal.py app/services/vision_journal_service.py \
  app/founder/dashboard/vision_*.py app/founder/dashboard/nav.py \
  app/founder/dashboard/routes.py app/founder/dashboard/services/command_centre_service.py \
  app/founder/dashboard/dto/command_centre.py tests/test_v1sp001d_vision_journal.py
```

Covered:

- Create / edit / archive / soft-delete  
- Status history preservation  
- Search, filters, sorting, tags  
- Relationships  
- Promotion placeholder  
- Export (MD / JSON / CSV)  
- Overview widgets  
- Founder-only access  
- Student workflow isolation  
- IAHF-003 Command Centre regression  

---

## Known Limitations

Intentional Version 1 boundaries (out of scope):

- No AI summarisation or idea scoring  
- No automatic roadmap generation  
- No collaborative editing, voting, comments, or notifications  
- No Kanban board  
- Categories are constant tuples (not admin-configurable UI yet)  
- No dependency graph validation  
- Soft-delete only (no hard purge UI)  

---

## Migration Impact

Alembic revision `202607170002_create_vision_journal_tables` adds four Founder-only tables. No educational schema changes. Curriculum V1/V2 traversal unaffected.

---

## Architecture Compliance

- HTTP in `founder_dashboard` blueprint; logic in `VisionJournalService`  
- Models under `app/models/`; no educational evidence writes  
- Founder-only gate preserved  
- Student dashboards / missions / study plans untouched  

---

## Files Created

- `app/models/vision_journal.py`  
- `app/services/vision_journal_service.py`  
- `app/founder/dashboard/vision_forms.py`  
- `app/founder/dashboard/vision_handlers.py`  
- `app/founder/dashboard/templates/founder_dashboard/vision_journal.html`  
- `app/founder/dashboard/templates/founder_dashboard/vision_entry_form.html`  
- `app/founder/dashboard/templates/founder_dashboard/vision_entry_detail.html`  
- `app/founder/dashboard/templates/founder_dashboard/vision_timeline.html`  
- `migrations/versions/202607170002_create_vision_journal_tables.py`  
- `tests/test_v1sp001d_vision_journal.py`  
- `knowledge/releases/V1SP-001D_FOUNDER_VISION_JOURNAL.md`  

## Files Modified

- `app/__init__.py`  
- `app/models/__init__.py`  
- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/dto/command_centre.py`  
- `app/founder/dashboard/services/command_centre_service.py`  
- `app/founder/dashboard/templates/founder_dashboard/overview.html`  
- `app/founder/dashboard/static/css/founder_dashboard.css`  
