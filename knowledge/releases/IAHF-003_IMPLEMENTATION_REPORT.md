# IAHF-003 — Founder Command Centre Implementation Report

**Programme:** Product Operations Programme (POP)  
**Sprint:** POP Sprint 1  
**Milestone:** IAHF-003  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Commit:** `6018ab3` — `feat(founder): implement Founder Command Centre (IAHF-003)`  

---

## Summary

IAHF-003 establishes a **single Founder operational home**: the **Founder Command Centre** under `/founder`, organised per [`POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md`](../architecture/POP-002_FOUNDER_INFORMATION_ARCHITECTURE.md) and governed by [`DESIGN_PRINCIPLES.md`](../architecture/DESIGN_PRINCIPLES.md) (especially DP-001 One Source of Truth, DP-002 One Entry Point, DP-003 Workflow Before Data, DP-004 Educational Integrity, DP-008 Trust).

The previous dual-home model (`/founder` FOS executive dashboard vs undiscoverable `/research/founder` live Research Command Centre) is collapsed:

- Sidebar **Founder** opens Command Centre **Overview** (sole home).
- Live Product Check-in inbox, findings, and related ops live as Command Centre sections.
- Legacy `/research/founder*` URLs redirect into the Command Centre tree.
- Overview and Internal Alpha metrics use **live** Product Check-in / research data — not the unwired static FOS Internal Alpha provider.
- FOS Knowledge / Capability / engineering content remains under **Operations**, with honest labelling for the unwired offline week pipeline.
- Student Product Check-in (`/research/checkin`), educational evidence, Twin, curriculum, missions, and recommendations are unchanged.

---

## Files Modified

### Created

- `app/founder/dashboard/nav.py`
- `app/founder/dashboard/feedback_handlers.py`
- `app/founder/dashboard/dto/command_centre.py`
- `app/founder/dashboard/services/command_centre_service.py`
- `app/founder/dashboard/templates/founder_dashboard/_nav.html`
- `app/founder/dashboard/templates/founder_dashboard/overview.html`
- `app/founder/dashboard/templates/founder_dashboard/attention.html`
- `app/founder/dashboard/templates/founder_dashboard/feedback.html`
- `app/founder/dashboard/templates/founder_dashboard/findings.html`
- `app/founder/dashboard/templates/founder_dashboard/finding_detail.html`
- `app/founder/dashboard/templates/founder_dashboard/research.html`
- `app/founder/dashboard/templates/founder_dashboard/internal_alpha.html`
- `app/founder/dashboard/templates/founder_dashboard/participants.html`
- `app/founder/dashboard/templates/founder_dashboard/operations.html`
- `app/founder/dashboard/templates/founder_dashboard/releases.html`
- `app/founder/dashboard/templates/founder_dashboard/settings.html`
- `app/founder/dashboard/templates/founder_dashboard/review.html`
- `tests/test_iahf003_founder_command_centre.py`
- `knowledge/releases/IAHF-003_IMPLEMENTATION_REPORT.md` (this file)

### Modified

- `app/founder/dashboard/__init__.py`
- `app/founder/dashboard/routes.py`
- `app/founder/dashboard/services/__init__.py`
- `app/founder/dashboard/services/dashboard_service.py`
- `app/founder/dashboard/dto/internal_alpha.py`
- `app/founder/dashboard/static/css/founder_dashboard.css`
- `app/research/routes.py`
- `app/templates/partials/sidebar.html`
- `tests/test_founder_dashboard.py`
- `tests/test_rip003_founder_command_centre.py`
- `tests/test_rip004_research_insight_engine.py`

### Retained (heritage / unused as home)

- `app/founder/dashboard/templates/founder_dashboard/index.html` — prior FOS home template; Operations section supersedes it for HTTP.
- `app/templates/research/founder_dashboard.html` — heritage template; Feedback section uses the Command Centre copy.

---

## Architectural Decisions

| Decision | Rationale | Design Principles |
|---|---|---|
| One sidebar entry → Overview | Eliminate competing Founder homes | DP-002 |
| Live Product Check-in DB as Alpha SoT | End silent static zeros on the navigable home | DP-001, DP-008 |
| Secondary nav inside Command Centre | Two-click reach to all POP-002 sections | DP-003, DP-006 |
| Feedback absorbs Research Command Centre | Preserve live inbox without a second product | DP-001, DP-002 |
| Operations hosts FOS strengths | Keep Knowledge/Capability/recs without pretending they are daily triage | DP-003, DP-006 |
| Offline week pipeline labelled unavailable | Honest emptiness when `source_version=unwired` | DP-008 |
| Legacy `/research/founder*` redirects | Backwards-compatible bookmarks; not marketed as homes | DP-002 |
| Share Feedback active only on student check-in routes | Stop stealing active state from Founder sections | DP-007 |
| Observational only — no Twin/evidence writes | Educational boundary | DP-004 |
| Overview skips live FS Operational State under `TESTING` | Deterministic, fast tests without inventing metrics | DP-008 (test honesty) |

---

## Route Changes

### New routes (Founder Command Centre)

| Method | Path | Endpoint | Role |
|---|---|---|---|
| GET | `/founder`, `/founder/` | `founder_dashboard.index` | **Overview** (sole home) |
| GET | `/founder/attention` | `founder_dashboard.attention` | Attention triage |
| GET/POST | `/founder/feedback` | `founder_dashboard.feedback` | Feedback inbox (live SoT) |
| GET/POST | `/founder/feedback/review/<id>` | `founder_dashboard.review_submission` | Optional review form |
| GET | `/founder/findings` | `founder_dashboard.findings` | Findings list |
| GET/POST | `/founder/findings/<id>` | `founder_dashboard.finding_detail` | Finding detail |
| GET | `/founder/research` | `founder_dashboard.research` | Research insights |
| GET | `/founder/internal-alpha` | `founder_dashboard.internal_alpha` | Alpha programme health |
| GET | `/founder/participants` | `founder_dashboard.participants` | Participants |
| POST | `/founder/participants/award-founders-circle/<user_id>` | `founder_dashboard.award_founders_circle` | Award badge |
| GET | `/founder/operations` | `founder_dashboard.operations` | System / FOS ops |
| GET | `/founder/releases` | `founder_dashboard.releases` | Releases |
| GET | `/founder/settings` | `founder_dashboard.settings` | Settings bridge |

### Deprecated routes (compat redirects)

| Method | Path | Disposition |
|---|---|---|
| GET/POST | `/research/founder` | 302/307 → `/founder/feedback` |
| GET/POST | `/research/founder/finding/<id>` | 302/307 → `/founder/findings/<id>` |
| GET/POST | `/research/founder/review/<id>` | 302/307 → `/founder/feedback/review/<id>` |
| POST | `/research/founder/award-founders-circle/<user_id>` | 307 → `/founder/participants/award-founders-circle/<user_id>` |

### Unchanged (student)

| Path | Role |
|---|---|
| `/research/checkin` | Student Product Check-in |
| `/research/thank-you` | Post check-in |
| `/research/dismiss` | Skip check-in |
| `/settings/share-feedback` | Alias → check-in |

---

## Data Sources

Every Overview metric and its authority:

| Displayed metric | Source | Live? |
|---|---|---|
| Check-ins today | `ResearchFeedbackSubmission` filtered to calendar day (server local) | Yes |
| Participants active today | Distinct `user_id` among today's submissions | Yes |
| Outstanding reviews | Submissions with `workflow_status == "new"` via `FounderResearchService.get_internal_alpha_summary` | Yes |
| Open High/Critical findings | `ResearchProductFinding` open statuses ∩ High/Critical | Yes |
| Needs action | Outstanding reviews + open high-severity findings | Yes (derived) |
| Alpha health label | Derived from live summary + `is_internal_alpha_enabled()` | Yes |
| System health % / label | FOS Operational State engineering signals (skipped under pytest `TESTING`) | Yes in production |
| Active participants / completed check-ins / participation / avg experience / return intent | `FounderResearchService.get_internal_alpha_summary` | Yes |
| Check-ins last 7 days | Submission count since `today - 6 days` | Yes |
| Recent feedback rows | Newest submissions + `User.email` | Yes |
| Attention queue | New / clarification-requested submissions + open high findings | Yes |
| Research top trend / friction | Insight engine + product health aggregates | Yes when check-ins exist; otherwise honest empty |
| Capabilities completed/active | Operational State capability counts | Yes in production |
| App / Alpha version / build | `APP_VERSION`, `INTERNAL_ALPHA_VERSION`, `KWALITEC_BUILD_NUMBER` / status service | Config/live |
| Alerts (outstanding threshold, high findings, Alpha off, inbox truncated, stale under-review) | Live counts + rules in `CommandCentreService` | Yes |
| Internal Alpha section programme metrics | Same live summary as Overview | Yes |
| Internal Alpha “Offline week processing” | Explicit unavailable copy — not static zeros | Honest empty |
| Operations offline week panel | `pipeline_available` from `source_versions.internal_alpha != "unwired"` | Honest empty when unwired |

**Never fabricated:** Overview does not display FOS `StaticInternalAlphaSource` zeros as Product Check-in counts.

---

## Tests Executed

### Automated

```text
python3 -m pytest tests/test_iahf003_founder_command_centre.py tests/test_founder_dashboard.py -q
# 15 passed

python3 -m pytest \
  tests/test_rip003_founder_command_centre.py \
  tests/test_rip004_research_insight_engine.py \
  tests/test_rip002_contributor_recognition.py \
  tests/test_rip001_daily_checkin.py \
  app/founder/dashboard/tests/ -q
# 91 passed

python3 -m pytest tests/test_auth.py -q
# 21 passed

python3 -m ruff check \
  app/founder/dashboard/nav.py \
  app/founder/dashboard/routes.py \
  app/founder/dashboard/feedback_handlers.py \
  app/founder/dashboard/services/command_centre_service.py \
  app/founder/dashboard/services/__init__.py \
  app/founder/dashboard/dto/command_centre.py \
  app/research/routes.py \
  tests/test_iahf003_founder_command_centre.py
# All checks passed
```

### Coverage exercised

- Founder Overview rendering and live check-in counts  
- Section route founder-gating (403 for students)  
- Legacy `/research/founder` → `/founder/feedback` redirect  
- Feedback inbox / workflow / finding detail / review  
- Share Feedback active-state isolation from Founder pages  
- Auth login regression  
- FOS dashboard service/provider unit tests  

### Manual verification

Not run in this environment (no interactive browser session). Recommended smoke after deploy:

1. Founder login → sidebar Founder → Overview  
2. Submit Product Check-in as student → Founder Overview / Feedback show live count  
3. Confirm `/research/founder` redirects  
4. Confirm student Dashboard / Study Session unchanged  

---

## Known Limitations

- **Founder post-login landing** remains the student Dashboard (POP-002 deferred policy).  
- **Feedback pagination** beyond the existing 50-item inbox cap is not expanded (IAHF-004).  
- **Overview soft refresh** not implemented — full page reload; timestamp shown.  
- **Operations live FS scan** can be expensive outside tests; Overview skips it under `TESTING` only.  
- **Branding / Alpha chrome** (IAHF-005–007) not in scope.  
- **Educational Workflow Review** not in scope.  
- Heritage research templates under `app/templates/research/` retained but are no longer the Founder HTTP home.  
- Capability titles in Operations remain incomplete (pre-existing FOS presentation gap / IAHF-008).  

---

## Acceptance Criteria

| Criterion | Status |
|---|---|
| Founder has one operational home | ✓ Overview at `/founder` |
| Duplicate Founder dashboards no longer compete | ✓ Research home redirects; FOS content under Operations |
| Founder metrics originate from live operational data | ✓ Product Check-in / research DB + honest empties |
| Navigation reflects POP-002 | ✓ Secondary nav hierarchy + single sidebar entry |
| Student functionality remains unaffected | ✓ Check-in routes and student nav unchanged |
| No educational data modified | ✓ Observational Founder ops only |
| No regressions introduced | ✓ Targeted automated suites green |

---

## Document Control

| Field | Value |
|---|---|
| Owner | Product Operations Programme (POP) |
| Classification | Implementation / release report |
| Architecture authority | POP-002, DESIGN_PRINCIPLES |
| Next | Remaining IAHF backlog items (pagination, brand chrome, post-login preference) as scheduled |
