# FH-001 — Founder Feedback Hub Implementation Report

**Programme:** FH-001 · Founder Feedback Hub / Unified Feedback Inbox  
**Date:** 2026-07-30  
**Predecessor:** FB-001 (Student Feedback End-to-End Audit)  
**Scope:** Read-only Founder aggregation layer across existing feedback Sources of Truth  
**Out of scope:** Schema merges, migrations, dual-writes, student submission changes, specialist dashboard removal

---

## Executive Summary

FB-001 established that student feedback persists correctly; Founders could not see all of it from one place because Console surfaces were fragmented (`/console/beta`, `/console/alpha-observability`, `/console/feedback`).

FH-001 delivers a **unified Founder Feedback Hub** at `/console/feedback`. The Hub is a **read-only aggregation layer**: it loads Private Beta, Alpha, and Product Check-in rows through source adapters, normalizes them into one DTO, sorts newest-first, filters, and paginates. Opening a row redirects to the specialist page. No tables were merged, no data was migrated, and student submission flows are unchanged.

Product Check-in triage (RIP-003 editing surface) remains available at `/console/feedback/checkins`. Specialist dashboards at `/console/beta` and `/console/alpha-observability` are preserved.

**Verdict: SUCCESS** — all FH-001 success criteria met.

---

## Architecture

```
Student write paths (unchanged)
  ├── private_beta_feedback          → PrivateBetaAdapter
  ├── alpha_feedback_submissions     → AlphaAdapter
  └── research_feedback_submissions  → ResearchAdapter
              │
              ▼
     FounderFeedbackHubService
              │
              ▼
     FounderFeedbackItem (DTO)
              │
              ▼
     /console/feedback  (Hub UI — read-only)
              │
              ├── Open → /console/beta?feedback_id=…
              ├── Open → /console/alpha-observability?feedback_id=…
              └── Open → /console/feedback/checkins?submission=…
```

| Invariant | Status |
|---|---|
| No database changes | ✓ |
| No Alembic migration | ✓ |
| No dual-write | ✓ |
| No record duplication | ✓ (composite Hub ids `source:native_id`) |
| Existing student APIs unchanged | ✓ |
| Specialist pages preserved | ✓ |
| Hub never edits | ✓ (GET-only) |

Future sources require only another `FeedbackSourceAdapter` registered in `DEFAULT_ADAPTERS`.

---

## Hub Service

**Package:** `app/services/founder_feedback_hub/`

| Module | Role |
|---|---|
| `dto.py` | `FounderFeedbackItem`, `HubFilters`, `HubPage`, source constants |
| `adapters.py` | `PrivateBetaAdapter`, `AlphaAdapter`, `ResearchAdapter` |
| `service.py` | `FounderFeedbackHubService.list_items()` |
| `__init__.py` | Public exports |

**Responsibilities**

1. Load each Source of Truth via its adapter (`joinedload(user)` — no N+1 on student email).
2. Normalize to `FounderFeedbackItem` (never ORM entities).
3. Apply filters (source, severity, status, subject, date range, student, keyword).
4. Sort descending by `created_at`.
5. Paginate (`DEFAULT_PER_PAGE=25`, max 100).

---

## DTO Design

`FounderFeedbackItem` fields:

| Field | Private Beta | Alpha | Product Check-in |
|---|---|---|---|
| `id` | `private_beta:{id}` | `alpha:{id}` | `research:{id}` |
| `source` / `source_label` | PRIVATE BETA | ALPHA | PRODUCT CHECK-IN |
| `student` / `student_email` | User email | User email | User email |
| `subject` | `subject_code` | `NULL` | `NULL` |
| `category` | category | kind | classification or friction |
| `severity` | severity | `NULL` | `NULL` |
| `status` | status | status | workflow_status |
| `message` | message | message | free_text |
| `summary` | preview | preview / kind | preview / feature·friction |
| `created_at` | created_at | created_at | submitted_at |
| `updated_at` | `NULL` | `NULL` | `NULL` |
| `link_to_original` | beta URL | alpha URL | checkins URL |
| `origin_colour` | blue | purple | green |
| `metadata` | screen, device, … | rating, surface, … | ratings, source, … |

Missing fields are **NULL**, never fabricated.

---

## UI Changes

| Route | Role |
|---|---|
| `GET /console/feedback` | **Feedback Hub** (new landing) |
| `GET/POST /console/feedback/checkins` | Product Check-in specialist inbox (moved) |
| `GET /console/beta` | Private Beta dashboard (preserved; highlight `#feedback-{id}`) |
| `GET /console/alpha-observability` | Alpha observability (preserved; highlight row) |
| `GET/POST /console/feedback/review/<id>` | Review form (redirects to checkins) |

**Hub row columns:** Source badge · Category · Severity · Student · Subject · Created · Status · Preview · Open

**Filters:** All / Private Beta / Alpha / Product Check-in · Severity · Status · Subject · Date range · Student · Keyword

**Nav:** Console primary item relabelled **Feedback** → Hub. Specialist shortcuts on the Hub chrome link to Beta, Alpha, and Product Check-in.

**Legacy:** `/research/founder` redirects to `/console/feedback/checkins` (editing surface).

---

## Evidence

| Check | Evidence |
|---|---|
| Private Beta appears in Hub | `tests/test_fh001_founder_feedback_hub.py` |
| Alpha appears in Hub | same |
| Research appears in Hub | same |
| Source / severity / status filters | same |
| Keyword search | same |
| Newest-first sort | same |
| Pagination | same |
| Open routes to specialists | same + HTTP assertions |
| No duplicate Hub ids | `test_aggregates_all_three_sources` |
| Hub is GET-only | `test_hub_is_read_only_get` (405 on POST) |
| Specialist pages still work | `test_specialist_pages_still_work` |
| RIP-003 / RIP-004 checkins | updated to `/console/feedback/checkins` |

Commands:

```bash
python3 -m pytest tests/test_fh001_founder_feedback_hub.py -q
python3 -m pytest tests/test_rip003_founder_command_centre.py::TestCommandCentreHttp \
  tests/test_rip004_research_insight_engine.py::TestInsightEngineHttp -q
python3 -m ruff check app/services/founder_feedback_hub app/founder/dashboard/feedback_handlers.py
```

Result: **14/14 FH-001 tests passed**; RIP-003/RIP-004 HTTP suites green after path update.

---

## Performance

- Per-source queries use `joinedload(User)` — student email without N+1.
- SQL date / severity / status / subject / student filters pushed down where columns exist.
- Soft per-source fetch cap: 2000 rows (Alpha/Beta Founder volumes are far lower).
- Merge → sort → slice pagination in service (correct newest-first across sources).
- Hub does not hydrate related review/finding graphs (those stay on the checkins specialist page).

---

## Regression Tests

| Suite | Outcome |
|---|---|
| `tests/test_fh001_founder_feedback_hub.py` | 14 passed |
| RIP-003 Command Centre HTTP | passed (paths → checkins) |
| RIP-004 Insight Engine HTTP | passed (paths → checkins) |
| Specialist Beta / Alpha pages | preserved (smoke via Hub specialist test) |

---

## Backward Compatibility

| Surface | Status |
|---|---|
| `/console/beta` | Unchanged (optional `feedback_id` highlight) |
| `/console/alpha-observability` | Unchanged (optional `feedback_id` highlight) |
| `/console/feedback` | Now Hub (still founder-gated; Feedback menu entry) |
| Product Check-in inbox | `/console/feedback/checkins` |
| Student submission endpoints | Untouched |
| Storage models / tables | Untouched |

---

## Files Created

- `app/services/founder_feedback_hub/__init__.py`
- `app/services/founder_feedback_hub/dto.py`
- `app/services/founder_feedback_hub/adapters.py`
- `app/services/founder_feedback_hub/service.py`
- `app/founder/dashboard/templates/founder_dashboard/feedback_hub.html`
- `tests/test_fh001_founder_feedback_hub.py`
- `FH001_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/founder/dashboard/routes.py`
- `app/founder/dashboard/feedback_handlers.py`
- `app/founder/dashboard/nav.py`
- `app/founder/dashboard/templates/founder_dashboard/feedback.html`
- `app/founder/dashboard/templates/founder_dashboard/findings.html`
- `app/founder/dashboard/templates/founder_dashboard/beta.html`
- `app/founder/dashboard/templates/founder_dashboard/alpha_observability.html`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/research/routes.py`
- `tests/test_rip003_founder_command_centre.py`
- `tests/test_rip004_research_insight_engine.py`
- `tests/test_iahf003_founder_command_centre.py`
- `tests/test_founder_dashboard.py`

## Migration Impact

**None.** No Alembic revisions. No schema changes.

## Architecture Compliance

- Layering preserved: blueprint → service → models.
- Curriculum V1/V2: N/A (Founder Console only).
- Student submission services and tables remain Sources of Truth; Hub is projection-only.

## Technical Debt

- Cross-source pagination merges capped result sets in memory (acceptable for current Founder volumes; SQL `UNION ALL` could replace later if needed).
- Alpha/Research have no native severity/subject — Hub correctly returns empty for those filters on those sources rather than inventing values.
- Private Beta / Alpha “detail” pages remain list dashboards with highlight, not full single-record editors (Hub never becomes the editor).

## Known Limitations

- Hub does not replace RIP-003 workflow actions — those stay on Product Check-in.
- Insight engine panels live on `/console/feedback/checkins`, not the Hub landing page.
- Older Private Beta rows beyond the Beta dashboard’s “latest 12” list may not appear highlighted on `/console/beta` even though the Open link lands there.

## Final Verdict

**FH-001 complete.** Every student feedback source is visible from one central Feedback Hub without changing storage architecture, student flows, or specialist dashboards.
