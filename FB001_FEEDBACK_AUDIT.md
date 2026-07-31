# FB-001 — Student Feedback End-to-End Audit

**Programme:** FB-001 · Student Feedback End-to-End Audit  
**Date:** 2026-07-30  
**Scope:** Evidence-only investigation (no code changes, no SQL execution, no fabricated rows)  
**Method:** Static trace of student UI → routes → services → ORM tables → Founder Console readers

---

## Executive Summary

The student feedback pipeline does **not** fail at validation, commit, or the success flash. For the primary student “Feedback” entry points (**Report issue** / **Send beta feedback**), submission persists successfully into `private_beta_feedback`, and the UI correctly shows a success notification after commit.

The failure is a **store / console surface mismatch**:

| Student channel | Writes to | Appears in Founder Console |
|---|---|---|
| Report issue / Send beta feedback | `private_beta_feedback` | **Private Beta** (`/console/beta`) — **not** Support Feedback |
| Report a problem / Suggest improvement | `alpha_feedback_submissions` | **Platform** (`/console/alpha-observability`) — **not** Support Feedback |
| Full Product Check-in / Share feedback | `research_feedback_submissions` | **Support → Feedback** (`/console/feedback`) |

Founder Console **Support / Feedback** (`founder_dashboard.feedback`) is labelled “Feedback” in the page chrome and “Support” in primary nav, but its inbox is **Product Check-in only** (`ResearchFeedbackSubmission` via `FounderResearchService`). It never queries private-beta or alpha feedback tables.

**Exact failure point:** after a successful student write to `private_beta_feedback` (or `alpha_feedback_submissions`), the Founder read path at `/console/feedback` queries a different table. The pipelines diverge at **Founder Console data source selection**, not at student submission.

---

## Pipeline Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│ STUDENT UI                                                               │
│                                                                          │
│  Footer “Report issue” ──┐                                               │
│  Help “Send beta feedback”├──► POST /alpha/feedback/beta                 │
│                           │    PrivateBetaFeedbackService.submit         │
│                           └──► TABLE: private_beta_feedback              │
│                                    │                                     │
│                                    ▼                                     │
│                           Founder: /console/beta  (Private Beta)         │
│                           ✗ NOT /console/feedback                        │
│                                                                          │
│  Help “Report a problem” ─┐                                              │
│  Help “Suggest…”          ├──► POST /alpha/feedback/report-problem|…     │
│                           │    AlphaFeedbackService.submit               │
│                           └──► TABLE: alpha_feedback_submissions         │
│                                    │                                     │
│                                    ▼                                     │
│                           Founder: /console/alpha-observability          │
│                           ✗ NOT /console/feedback                        │
│                                                                          │
│  Help “Full Product Check-in” ─┐                                         │
│  Settings “Share feedback”     ├──► POST /research/checkin               │
│  Post-session invitation       │    ResearchFeedbackService.submit_checkin│
│                                └──► TABLE: research_feedback_submissions │
│                                         │                                │
│                                         ▼                                │
│                                Founder: /console/feedback  (Support)     │
└──────────────────────────────────────────────────────────────────────────┘

DIVERGENCE (primary incident path):
  Student write ──OK──► private_beta_feedback
  Founder Feedback read ──────────► research_feedback_submissions  (empty for that event)
```

---

## Frontend Findings

### Primary “Feedback feature” entry (most likely incident path)

| Item | Evidence |
|---|---|
| Page | `app/templates/alpha/feedback_beta.html` — title “Send beta feedback” |
| Entry points | Student footer **Report issue** (`layouts/eos_student.html` → `alpha.feedback_beta`); Help **Send beta feedback** (`alpha/help.html`) |
| Endpoint | `POST /alpha/feedback/beta` (`alpha.feedback_beta`) |
| HTTP method | `GET` (form) / `POST` (submit) |
| Auth | `@login_required` |
| Payload | WTForms `PrivateBetaFeedbackForm`: CSRF (`hidden_tag`), `category`, `message`, hidden `mission_id`, `current_screen`, `subject_code`, `browser`, `device`, `path` |
| Client extras | Inline JS fills browser/device/path/current_screen from `navigator` / `document.title` |
| Success UX | Server `flash(..., "success")` then redirect home (or safe local `next`); rendered via `partials/flash_messages.html` as `student-success` |
| Success copy | `"Thank you — your feedback helps private beta validation."` |

### Parallel student channels (same Help “Quick actions”)

| UI label | Route | Template | Success copy |
|---|---|---|---|
| Report a problem | `POST /alpha/feedback/report-problem` | `feedback_report_problem.html` | `"Thank you — your feedback helps Internal Alpha."` |
| Suggest an improvement | `POST /alpha/feedback/suggest` | `feedback_suggest.html` | same Internal Alpha thank-you |
| Full Product Check-in | `POST /research/checkin` | `research/checkin.html` | Redirect to `/research/thank-you` (thank-you page, not the beta flash) |
| Settings Share feedback | `GET /settings/share-feedback` → redirect to Product Check-in | — | Check-in thank-you path |

Mission post-session also offers mission-helpful / explanation-clear alpha forms and an optional Product Check-in invitation (`mission/session_recorded.html`).

### Frontend conclusion

There is **no single unified Feedback feature**. The most visible chrome link (**Report issue** in the footer) is the **private-beta** form, not Product Check-in. A founder looking at Support Feedback will miss that submission even when the student saw a legitimate success message.

---

## Backend Findings

### Path A — Private beta (footer Report issue)

| Layer | Detail |
|---|---|
| Controller | `app/alpha/routes.py` → `feedback_beta` |
| Form validation | `PrivateBetaFeedbackForm.validate_on_submit()` (category + message required) |
| Service | `PrivateBetaFeedbackService.submit` (`app/services/private_beta/feedback_service.py`) |
| Validation in service | Category ∈ `FEEDBACK_CATEGORIES`; non-empty message (truncated to 1000); optional mission must be owned by user |
| Severity | Auto via `classify_feedback_severity` — not student-supplied |
| Persistence | `db.session.add` + `commit`; on exception → rollback, `ok=False`, warning flash |
| Success return | **Conditional** on `result.ok` after commit — **not** unconditional |
| Telemetry | `PresentationTelemetryService.record(EVENT_FEEDBACK_SUBMITTED, resource_type="private_beta_feedback", …)` after success |
| Swallowed exceptions | Commit failures are caught, logged, and surfaced as warning flash — student would **not** see success in that case |

### Path B — Alpha lightweight feedback

| Layer | Detail |
|---|---|
| Controller | `_handle_feedback` in `app/alpha/routes.py` |
| Service | `AlphaFeedbackService.submit` |
| Persistence | `alpha_feedback_submissions` |
| Success | Same pattern: flash only if `result.ok` after commit |

### Path C — Product Check-in (only path that feeds Support Feedback)

| Layer | Detail |
|---|---|
| Controller | `app/research/routes.py` → `checkin` |
| Service | `ResearchFeedbackService.submit_checkin` |
| Persistence | `research_feedback_submissions` (+ `research_contributions`) |
| Failure UX | `ValueError` → danger flash, re-render form (no thank-you) |
| Success UX | Redirect to thank-you page (no flash required) |

### Backend conclusion

Student submission backends for beta/alpha feedback are coherent: validate → commit → success flash. There is **no evidence** that success is returned without a successful commit on those paths.

---

## Database Findings

Audit is schema/code evidence only (no live DB queries per investigation constraints).

### Store 1 — `private_beta_feedback` (PB-001)

Model: `PrivateBetaFeedback` (`app/models/private_beta.py`)

| Field | Notes |
|---|---|
| PK | `id` |
| Student | `user_id` → `users.id` |
| Category | `category` (bug, suggestion, confusing_screen, missing_feature, incorrect_recommendation, general) |
| Subject | `subject_code` (optional string — **not** FK to subjects) |
| Status | `status` default `"new"` |
| Severity | `severity` (auto) |
| Message | `message` (required) |
| Timestamps | `created_at` |
| Attachments | **None** — no attachment column/relation |
| Mission | optional `mission_id` |
| Soft delete | **None** |

### Store 2 — `alpha_feedback_submissions` (ALPHA-001)

Model: `AlphaFeedbackSubmission`

| Field | Notes |
|---|---|
| PK | `id` |
| Student | `user_id` |
| Kind | mission_helpful / explanation_clear / report_problem / suggest_improvement |
| Status | default `"new"` |
| Timestamps | `created_at` |
| Attachments | **None** |
| Soft delete | **None** |

### Store 3 — `research_feedback_submissions` (RIP-001) — Support inbox SoT

Model: `ResearchFeedbackSubmission`

| Field | Notes |
|---|---|
| PK | `id` |
| Student | `user_id` |
| Structured ratings | experience, feature_helped_most, friction, confidence, return_intent |
| Free text | optional `free_text` + `classification` |
| Status | `workflow_status` default `"new"` |
| Timestamps | `submitted_at` |
| Relations | contribution, status_transitions, founder_notes, finding_links |
| Soft delete | **None** |

### If no row in Support inbox

For a student who used **Report issue** / **Send beta feedback**:

1. A row **should** exist in `private_beta_feedback` (if commit succeeded — matching the success flash).
2. A row **will not** exist in `research_feedback_submissions` for that event.
3. Therefore Support Feedback correctly shows nothing for that event — it is looking at the wrong store.

---

## Founder Console Findings

### Support → Feedback (`GET/POST /console/feedback`)

| Concern | Finding |
|---|---|
| Route | `founder_dashboard.feedback` → `handle_feedback_request` |
| Template | `founder_dashboard/feedback.html` — subtitle: “Product Check-in inbox” |
| Nav label | Primary nav: **Support**; page H1: **Feedback** |
| Auth | `@founder_required` |
| Repository / service | `FounderResearchService.list_inbox` / `build_dashboard_context` |
| Query source | **Only** `ResearchFeedbackSubmission` |
| Filters | version, badge, feature, severity (via linked findings), status (`workflow_status`), classification, date range, submission_source, keyword, student email |
| Soft delete filter | N/A — no soft-delete column |
| Tenant filter | N/A — single-tenant user scoping by optional student email |
| Pagination | `page` query param → `inbox_page` |
| Sorting | `submitted_at` descending |
| Includes private beta? | **No** |
| Includes alpha feedback? | **No** |

Conclusion: the record is **not filtered out** of Support Feedback — it was **never loaded**. Empty inbox for a beta submission is expected with default (empty) filters.

### Where the student record *does* surface

| Student store | Founder surface | Path |
|---|---|---|
| `private_beta_feedback` | Private Beta dashboard | `/console/beta` via `FounderBetaDashboardService` → `PrivateBetaFeedbackService.recent(limit=12)` |
| `alpha_feedback_submissions` | Platform Intelligence | `/console/alpha-observability` via `AlphaFeedbackService.recent(limit=40)` |
| `research_feedback_submissions` | Support Feedback | `/console/feedback` |

Private Beta is secondary nav under Settings grouping (`COMMAND_CENTRE_SECONDARY_NAV`), not the primary **Support** item. Easy to miss when operators open “Feedback”.

---

## Root Cause

**Siloed feedback stores with a misleading Console label.**

1. The dominant student “send feedback” chrome (**Report issue**) writes to **PB-001** (`private_beta_feedback`).
2. Founder Console primary **Support / Feedback** reads only **RIP-001** Product Check-ins (`research_feedback_submissions`).
3. There is **no bridge, sync, or union query** between these stores.
4. The student success message is truthful (commit succeeded). The founder observation “nothing in Feedback” is also truthful for the Support inbox — different product surfaces, same English word “feedback”.

**First divergence point:** Founder Console read path (`FounderResearchService` → `ResearchFeedbackSubmission`) after a successful write to a non-research table.

Not root causes (ruled out by code):

- Unconditional success without commit (success flash requires `result.ok` post-commit)
- Soft-delete hiding rows (no soft-delete fields)
- Default status filters hiding new beta rows (Support never queries that table)
- Permission denial on Support (would block the page, not selectively hide beta rows)

---

## Recommended Fix

Evidence-only programme — recommendations only:

1. **Operator immediate workaround:** Check `/console/beta` (Private Beta → Latest feedback) for footer/Help beta submissions; check `/console/alpha-observability` for Report a problem / Suggest improvement.
2. **Product clarity (low risk):** Rename Support page copy / nav to “Product Check-in” (or “Check-in inbox”) so it does not imply all student feedback.
3. **Student clarity:** Align footer **Report issue** labelling with the store it writes (e.g. “Send beta feedback”) or route the primary chrome entry to the same store the Support inbox reads — product decision required.
4. **Unified Support inbox (medium):** Project private-beta + alpha submissions into `/console/feedback` (or a single Support inbox DTO) with source badges — without merging educational reflection systems.
5. **Do not** silently dual-write without an explicit product rule; keep RIP / PB / ALPHA boundaries unless a consolidation programme owns the merge.

---

## Risk Assessment

| Risk | Level | Notes |
|---|---|---|
| Lost student trust if founders ignore beta reports | **High** | Success UI implies the team will see it; Support inbox does not |
| Operational miss of critical bugs | **High** | Critical severity lives on private-beta rows (`severity=critical`) visible on `/console/beta`, not Support |
| False “submission broken” engineering chase | **Medium** | Symptom looks like a write failure; write path is healthy |
| Premature store merge | **Medium** | RIP workflow (status transitions, findings, badges) differs from PB-001 / ALPHA-001 models |
| Curriculum / Twin / educational state impact | **None** | All three feedback stores explicitly avoid educational mutation |

---

## Step cross-check (investigation checklist)

| Step | Result |
|---|---|
| 1 Trace request | Primary: `POST /alpha/feedback/beta`, login-required form POST, category+message payload, 302 + success flash |
| 2 Backend processing | `feedback_beta` → `PrivateBetaFeedbackService.submit`; validation real; success only after commit |
| 3 Database | Intended table `private_beta_feedback`; Support table `research_feedback_submissions` remains empty for this event |
| 4 Founder Console | Loads Product Check-ins only; filters/pagination irrelevant for cross-store miss |
| 5 Pipeline compare | Diverges at Founder data source after successful student write |
| 6 UI success | Flash is conditional and accurate — not a false success bug |
| 7 Data model | Three complete-but-separate entities; no shared Founder Feedback relation |

---

## Architecture Compliance (audit note)

- Application code was **not modified**.
- Curriculum V1/V2 traversal: **N/A**.
- Migration impact: **None**.
- Layering observed: blueprints → services → models as designed; the defect is product-surface fragmentation, not a layering violation.

---

## Evidence Index

| Artefact | Path |
|---|---|
| Student beta route | `app/alpha/routes.py` (`feedback_beta`, `_handle_feedback`) |
| Footer entry | `app/templates/layouts/eos_student.html` |
| Help quick actions | `app/templates/alpha/help.html` |
| Beta form UI | `app/templates/alpha/feedback_beta.html` |
| PB service | `app/services/private_beta/feedback_service.py` |
| Alpha service | `app/services/alpha_feedback_service.py` |
| Check-in route | `app/research/routes.py` |
| Check-in service | `app/services/research_feedback_service.py` |
| Models | `app/models/private_beta.py`, `alpha_infrastructure.py`, `research_feedback.py` |
| Founder Feedback handler | `app/founder/dashboard/feedback_handlers.py` |
| Founder inbox service | `app/services/founder_research_service.py` |
| Private Beta console | `app/founder/dashboard/services/beta_dashboard_service.py`, `routes.py` (`/beta`) |
| Alpha observability | `app/founder/dashboard/routes.py` (`alpha_observability`) |
| Console nav | `app/founder/dashboard/nav.py` |
| PB operator docs | `knowledge/engineering/pb001_private_beta_validation/README.md` |
