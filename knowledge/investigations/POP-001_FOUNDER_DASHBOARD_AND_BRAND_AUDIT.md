# POP-001 — Founder Dashboard & Brand Consistency Investigation

**Programme:** Product Operations Programme (POP)  
**Milestone:** POP-001  
**Status:** Investigation complete — no code changes  
**Date:** 2026-07-17  
**Scope:** Version 1 Internal Alpha operational assessment  
**Nature:** Read-only audit (application code untouched)

---

## Executive Summary

Version 1 Internal Alpha is **functionally usable for students**, but **Founder operational visibility is fragmented and partially unwired**. Two separate “Founder Dashboard” surfaces exist with different data backends, and the surface founders are most likely to open from the sidebar does **not** show live Product Check-in data.

| Surface | URL | Data source | Sidebar link |
|---|---|---|---|
| Founder Operating System (FOS-004) | `/founder` | Filesystem Knowledge/Capability + **static empty Internal Alpha** | Yes (“Founder”) |
| Research Command Centre (RIP-003) | `/research/founder` | Live SQLAlchemy Product Check-ins | **No** |

Observed operational symptoms (stale / incomplete Founder metrics, feedback not “synchronising”) are explained primarily by this **dual-system disconnect**, not by HTTP caching. Product Check-ins commit immediately to the database and appear on the Research Command Centre after a full page reload; they never flow into the FOS dashboard’s Internal Alpha panel.

Brand and Internal Alpha identity are **inconsistent and incomplete**: there are **zero tracked image logo assets**, no favicon/PWA/OG icons, text-only branding in chrome, and Internal Alpha labelling appears on login (conditionally) and Settings — not as a persistent badge on navbar, student dashboard, FOS dashboard, or footer.

**Overall verdict:** Continue Internal Alpha student testing, but **resolve Critical Founder visibility hotfixes before treating Founder operations as reliable**. Brand/identity hotfixes can follow in the same sprint without blocking study loops.

---

## Findings

### Critical

| ID | Finding |
|---|---|
| C-1 | **Dual Founder dashboards with no shared feedback pipeline.** FOS `/founder` Internal Alpha metrics default to an empty static source (`feedback_count=0`). Live Product Check-ins live only in `research_feedback_submissions` and surface on `/research/founder`. |
| C-2 | **Research Command Centre is not navigable from the app chrome.** Sidebar “Founder” → FOS only. Founders must know `/research/founder` to see check-ins. |
| C-3 | **FOS Internal Alpha provider is unwired for HTTP.** `InternalAlphaProvider` always wraps `StaticInternalAlphaSource` (empty). Knowledge and Capability are live (FSI-001); Internal Alpha is not live on page load. FSI-003 workflow injects alpha only into a one-shot CLI/workflow run — not into subsequent `/founder` GETs. |
| C-4 | **Filesystem Internal Alpha week repo is empty of feedback.** `research/internal_alpha/week_001/` has no `raw_feedback` content (only `.DS_Store`). Even the offline pipeline has nothing to process. |

### High

| ID | Finding |
|---|---|
| H-1 | **No logo image assets in the repository.** `app/static/images/` contains only `.gitkeep`. `git ls-files` finds **0** `.png`/`.svg`/`.ico`/`.webp`/`.jpg` assets. |
| H-2 | **No favicon, Apple touch icon, PWA manifest, or Open Graph / social preview images.** Layouts omit `rel="icon"`, `apple-touch-icon`, `manifest`, `og:image`, `twitter:image`. |
| H-3 | **Internal Alpha identity is not consistently visible.** Login shows an Internal Alpha note only when `KWALITEC_EI_INTERNAL_ALPHA` is enabled. Footer shows `Kwalitec v{{ app_version }}` with no Alpha badge. Student Dashboard and FOS dashboard have no Alpha badge. Settings has an Internal Alpha section (discoverable, not ambient). |
| H-4 | **Two logo treatments compete.** Landing/login uses an inline SVG layers icon + wordmark (`.landing-logo`). Authenticated shell uses text-only `.sidebar-brand` (“Kwalitec”) with no icon. Topnav shows email, not brand. |
| H-5 | **“What changed since yesterday” excludes today’s submissions by design.** After a new check-in today, founders can see updated totals but a “since yesterday” panel that still looks stale — amplifying the synchronisation perception bug. |
| H-6 | **`newest_contributions` is computed but never rendered** in `research/founder_dashboard.html`, so the most recent feedback list is not on the home summary. |

### Medium

| ID | Finding |
|---|---|
| M-1 | **Inbox / findings capped at 50 with no pagination UI.** Older submissions silently drop off the inbox list. |
| M-2 | **Summary metrics load all submissions into memory** (`ResearchFeedbackSubmission.query.all()`) for averages/counts — correct for small Internal Alpha, fragile as volume grows; not cached, but expensive. |
| M-3 | **Date boundary mixing:** submissions store UTC-naive timestamps; “yesterday” buckets use `date.today()` (server local) with naive midnight bounds — day boundaries can shift near UTC midnight. |
| M-4 | **Combined `student` + `badge` filters each `join(User)`** in `_apply_inbox_filters` — risk of incorrect SQL / duplicate joins when both filters are set. |
| M-5 | **“Most confusing feature” heuristic is weak.** It counts `feature_helped_most` when classification is Confusing **or** any friction is present — often conflates loved features with friction. |
| M-6 | **FOS capability table mapping drops titles/status.** `_map_capabilities` sets `title=""`, `status=""`, `version=""`, `completion_date=""` — UI shows IDs only. Recent Internal Alpha week rows hardcode `feedback_count=0` / `duplicate_count=0`. |
| M-7 | **No auto-refresh / polling on either Founder surface.** Freshness requires full page reload (expected for server-rendered apps, but undocumented for operators). |
| M-8 | **Register page does not exist.** Public registration is intentionally disabled; brand audit “Register” maps to login’s invite-only copy only. |
| M-9 | **Typography uses system UI stack** (`Segoe UI`, Helvetica Neue, system-ui) — acceptable for app chrome, but there is no distinctive brand typeface or logo mark. |
| M-10 | **Visual language split:** student surfaces use `.command-card`; FOS dashboard uses `.founder-metric-card` / `.founder-panel-card` (separate CSS package). Research Command Centre reuses `.command-card` (closer to student UI). |

### Low

| ID | Finding |
|---|---|
| L-1 | FOS dashboard JS only filters the capability table client-side; no other interactivity. |
| L-2 | Landing illustration is abstract CSS shapes (`.shape-*`), not product imagery. |
| L-3 | Error pages (403/404/500) inherit layouts but were not given dedicated brand marks. |
| L-4 | Wizard CSS (`wizard.css`) is feature-specific but token-aligned — minor polish only. |
| L-5 | `INTERNAL_ALPHA_VERSION = "4.3"` in settings status is separate from `APP_VERSION` (`1.0.0`) — intentional (PTP-005), but easy to misread as product version drift. |
| L-6 | Sidebar labels “Share Feedback” for Product Check-in — accurate enough, but “Research” / “Check-in” naming varies across templates. |

---

## Root Cause Analysis

### RCA-1 — FOS Founder Dashboard shows empty / stale Internal Alpha feedback

| Field | Detail |
|---|---|
| **Description** | `/founder` Internal Alpha panel shows empty week, `feedback_count=0`, no categories, even when students submit Product Check-ins. |
| **Root Cause** | Architectural split: FOS-003 Internal Alpha Pipeline is filesystem `.txt` based and never reads `research_feedback_submissions`. HTTP Operational State uses `InternalAlphaProvider(StaticInternalAlphaSource())` → empty DTO (`source_version="unwired"`). FSI-003 injects pipeline output only during workflow execution; the dashboard’s `OperationalStateProvider` does not persist or reload that injection. |
| **Files Involved** | `app/founder/operational_state/providers/internal_alpha.py`; `app/founder/operational_state/services/operational_state_service.py`; `app/founder/dashboard/services/dashboard_service.py`; `app/founder/dashboard/providers/operational_state.py`; `app/founder/internal_alpha_workflow/services/workflow_service.py`; `app/templates` path via `founder_dashboard/index.html` |
| **Components Involved** | `InternalAlphaProvider`, `StaticInternalAlphaSource`, `FounderOperationalStateService`, `FounderDashboardService`, FSI-003 workflow |
| **Recommended Solution** | Choose one product rule: (A) Wire a live Internal Alpha source for HTTP from DB check-ins and/or last pipeline summary; and/or (B) Deep-link FOS → Research Command Centre and stop presenting check-in metrics on FOS until wired. Prefer clear labelling either way. |
| **Estimated Complexity** | Medium (wiring + acceptance tests); Low if nav/labelling-only interim |

### RCA-2 — Founders cannot discover live Product Check-in data

| Field | Detail |
|---|---|
| **Description** | Product Check-ins appear to “not sync” because the linked Founder page does not show them. |
| **Root Cause** | Sidebar only links `founder_dashboard.index`. Research Command Centre (`research.founder_command_centre`) has no nav entry. |
| **Files Involved** | `app/templates/partials/sidebar.html`; `app/research/routes.py`; `app/founder/dashboard/routes.py` |
| **Components Involved** | Sidebar nav, `show_founder_nav`, research blueprint |
| **Recommended Solution** | Add Founder-only nav item(s): “Research Command Centre” and/or nest under Founder. Optionally land `/founder` with cross-links. |
| **Estimated Complexity** | Low |

### RCA-3 — Feedback metrics feel stale after submission

| Field | Detail |
|---|---|
| **Description** | After submitting a check-in, some Founder panels do not reflect “just now”. |
| **Root Cause** | (1) Looking at wrong dashboard (RCA-1/2). (2) No auto-refresh — must reload. (3) “What changed since yesterday” intentionally ignores *today*. (4) `newest_contributions` not rendered. Inbox itself is ordered by `submitted_at DESC` and **does** include new rows after reload. |
| **Files Involved** | `app/services/founder_research_service.py` (`get_changes_since_yesterday`, `get_internal_alpha_summary`); `app/templates/research/founder_dashboard.html`; `app/services/research_feedback_service.py` (`submit_checkin` commits) |
| **Components Involved** | Research Command Centre metrics, inbox query |
| **Recommended Solution** | Relabel panel to “Yesterday vs prior day”; add “Today so far” strip; render newest contributions; document manual refresh. Optional later: soft poll / HTMX fragment. |
| **Estimated Complexity** | Low–Medium |

### RCA-4 — Missing brand logo system

| Field | Detail |
|---|---|
| **Description** | Approved Kwalitec branding cannot be applied consistently because no logo/favicon asset pack exists in-repo. |
| **Root Cause** | Static images directory is a placeholder; brand is text + ad-hoc inline SVG on login only. |
| **Files Involved** | `app/static/images/.gitkeep`; `app/templates/auth/login.html`; `app/templates/partials/sidebar.html`; `app/templates/layouts/base.html`; `app/templates/layouts/auth_base.html`; `app/static/css/app.css` (`.landing-logo`, `.sidebar-brand`) |
| **Components Involved** | Auth landing, app shell, design tokens |
| **Recommended Solution** | Introduce a single brand asset pack (SVG primary + PNG favicons + OG) and one partial for logo mark; replace inline SVG and text-only chrome. |
| **Estimated Complexity** | Medium (asset + template sweep) |

### RCA-5 — Internal Alpha identity not ambient

| Field | Detail |
|---|---|
| **Description** | Users/operators may not realise they are on an Internal Alpha build. |
| **Root Cause** | Alpha copy is gated (`is_internal_alpha_enabled`) on login; Settings status is buried; footer/version line has no Alpha marker. EI flag and product Alpha are also easy to conflate. |
| **Files Involved** | `app/templates/auth/login.html`; `app/templates/layouts/base.html`; `app/templates/layouts/auth_base.html`; `app/templates/settings/index.html`; `app/application/config/internal_alpha.py`; `app/services/internal_alpha_status_service.py` |
| **Components Involved** | Login onboarding note, footer, settings Internal Alpha section |
| **Recommended Solution** | Persistent “Internal Alpha” badge in sidebar brand and/or footer on all authenticated layouts; show on login regardless of EI flag if product is in Internal Alpha programme; keep Settings detail as deeper status. |
| **Estimated Complexity** | Low |

### RCA-6 — Inbox filter edge cases / incomplete lists

| Field | Detail |
|---|---|
| **Description** | Filters may fail or truncate; founders may think data is missing. |
| **Root Cause** | Hard `limit=50` without pagination; dual `User` joins when badge+student combine. |
| **Files Involved** | `app/services/founder_research_service.py` (`list_inbox`, `_apply_inbox_filters`) |
| **Components Involved** | Research inbox |
| **Recommended Solution** | Add pagination or “showing N of M”; refactor joins to a single User join / aliased joins; add tests for combined filters. |
| **Estimated Complexity** | Medium |

### RCA-7 — FOS presentation incompleteness (capabilities / weeks)

| Field | Detail |
|---|---|
| **Description** | FOS capability and recent-week sections look incomplete even when Operational State has data. |
| **Root Cause** | Dashboard DTO mapping intentionally empties capability metadata fields; recent week summaries hardcode zero counts. |
| **Files Involved** | `app/founder/dashboard/services/dashboard_service.py` (`_map_capabilities`, `_map_internal_alpha`) |
| **Components Involved** | FounderDashboardService presentation layer |
| **Recommended Solution** | Map real capability titles/status from Capability Archive DTO; pass per-week counts when Internal Alpha is live. |
| **Estimated Complexity** | Low–Medium |

### RCA-8 — Branding / meta asset vacuum (favicon, PWA, OG)

| Field | Detail |
|---|---|
| **Description** | Browser tab, bookmarks, and link previews show generic defaults. |
| **Root Cause** | No assets and no `<link>` / meta tags in layouts. |
| **Files Involved** | `app/templates/layouts/base.html`; `app/templates/layouts/auth_base.html`; `app/static/` |
| **Components Involved** | Document head |
| **Recommended Solution** | Add favicon set + optional `site.webmanifest` + OG image; reference from both layouts. |
| **Estimated Complexity** | Low once assets exist |

---

## Founder Dashboard Audit (Detail)

### A. Surface map

#### A.1 Founder Operating System — `/founder`

- **Blueprint:** `founder_dashboard` (`app/founder/dashboard/`)
- **Access:** `@founder_required` (ADMIN_EMAIL ∪ FOUNDER_EMAILS)
- **Service:** `FounderDashboardService.build_page()` on each GET
- **Refresh:** Full page reload only; JS = capability table text filter
- **Caching:** None observed (no fragment cache, no service memoisation, no Flask view cache)

**Sections displayed:**

| Section | Source | Update behaviour |
|---|---|---|
| Operational Snapshot | Live `FounderOperationalState` + recommendations/brief | Recomputed each request |
| Engineering Health % | Derived from `state.engineering` signals (100 or 0) | Each request |
| Architecture Health % | Same signal as engineering (presentation only) | Each request |
| Capabilities completed/active | Live Capability Archive via Operational State | Each request |
| Top Recommendations | `FounderRecommendationService` from current state | Each request |
| Weekly Brief metadata | In-memory brief from providers | Each request (unavailable if deps fail) |
| Internal Alpha week / feedback / duplicates | **Static empty Internal Alpha DTO by default** | Always empty on HTTP unless injected elsewhere (not persisted) |
| Knowledge counts | Live Knowledge Engine | Each request |
| Activity lists | Capability IDs + alpha week labels from state | Incomplete titles |

#### A.2 Research Command Centre — `/research/founder`

- **Blueprint:** `research` (`app/research/routes.py`)
- **Access:** `@founder_required`
- **Service:** `FounderResearchService.build_dashboard_context(...)`
- **Refresh:** Full page reload; filter forms GET/POST redirect
- **Caching:** None; multiple `query.all()` aggregations per request

**Feedback**

| Question | Answer |
|---|---|
| Newly submitted feedback immediately visible? | **Yes on this page after reload** — `submit_checkin` commits; inbox orders by `submitted_at DESC`. Not visible on `/founder`. |
| Feedback counts accurate? | Summary counts from all rows are consistent with DB for small N. “Outstanding reviews” = `workflow_status == "new"` only. |
| Queries correct? | Inbox filters generally correct; badge+student double-join risk; severity filter joins findings (submissions without findings excluded). |
| Filters functioning? | Yes for single filters; combined badge+student needs verification/fix. |
| Stale data? | No server cache. Perceived staleness from wrong dashboard, yesterday panel, or no reload. |
| Timestamps correct? | Stored as UTC-naive `datetime.now(UTC).replace(tzinfo=None)`; day buckets use local `date.today()`. |

**Product Check-ins**

| Concern | Status |
|---|---|
| Retrieval | `list_inbox` — newest first, limit 50 |
| Ordering | `submitted_at DESC` |
| Pagination | **None** (hard limit) |
| Timestamps | `submitted_at` on model |
| Statistics | Summary + product health + insight engine |
| Aggregation | In-Python over full table for summary/health |

**Research Check-ins**

There is **no separate Research Check-in entity**. Product Check-in (`ResearchFeedbackSubmission`) *is* the research intake (RIP-001). “Research Insights” (RIP-004) aggregates the same submissions. Filesystem FOS-003 “feedback” is a **different** artefact (`.txt` weeks), not the student form.

**Founder metrics (Research Command Centre)**

| Metric | Data source | Query / calculation | Refresh |
|---|---|---|---|
| Active Participants | Distinct `user_id` on submissions | Set length over `query.all()` | Per request |
| Completed Check-ins | Submission count | `len(submissions)` | Per request |
| Participation Rate | Participants ÷ distinct mission users | `_active_student_count()` | Per request |
| Avg Product Experience | Map ratings → 1–5 | Mean of mapped scores | Per request |
| Would Open Tomorrow % | Return intent in {Definitely, Probably} | % of completed | Per request |
| Avg Confidence | Map confidence → 1–5 | Mean | Per request |
| Outstanding Reviews | `workflow_status == "new"` | Count | Per request |
| Implemented Feedback | status ∈ {implemented, released, verified} | Count | Per request |
| Product Shapers | `ResearchContributorBadge` | `.filter_by(badge_slug=...).count()` | Per request |
| Changes since yesterday | Submissions on yesterday vs prior day | Naive local-day windows | Per request; **excludes today** |
| Product Health fields | Counters over all submissions | Heuristics (see M-5) | Per request |
| Insight Engine | `ResearchInsightService.generate_insights` | Time-windowed | Per request |

---

## Dashboard Refresh Lifecycle

```text
Student submits Product Check-in
        │
        ▼
ResearchFeedbackService.submit_checkin
  → INSERT research_feedback_submissions + research_contributions
  → db.session.commit()
        │
        ├──► /research/founder  (after browser reload)
        │      FounderResearchService.build_dashboard_context
        │      → live SQLAlchemy reads (no cache)
        │
        └──► /founder  (FOS)
               FounderDashboardService.build_page
               → OperationalStateProvider.get_state()
               → InternalAlphaProvider → Static empty DTO
               → Product Check-in NEVER appears
```

| Mechanism | Present? |
|---|---|
| Automatic update / polling | No |
| Manual refresh required | Yes (browser reload) |
| Application-level caching | No |
| Template fragment caching | No |
| Statistics computed dynamically | Yes (each request) |
| Stale ORM objects reused across requests | No (new queries per request) |
| Client-side stale state | FOS capability filter only (local DOM) |

---

## Brand Consistency Audit (Page-by-Page)

| Page | Template | Logo | Palette / type | Notes |
|---|---|---|---|---|
| Landing / Login | `auth/login.html` + `auth_base.html` | Inline SVG + “Kwalitec” (`.landing-logo`) | Design tokens + landing-specific CSS | Strongest brand treatment; Alpha note conditional |
| Register | — | N/A | N/A | **No public register route** |
| Student Dashboard | `dashboard/index.html` | Sidebar text wordmark only | `.command-card`, tokens | No Alpha badge |
| Founder OS Dashboard | `founder_dashboard/index.html` | Sidebar text | Separate `founder_dashboard.css` | No Alpha badge; different card language |
| Research Command Centre | `research/founder_dashboard.html` | Sidebar text | `.command-card` (student-aligned) | Not in nav |
| Settings | `settings/index.html` | Sidebar text | Settings nav pattern | Internal Alpha **section** exists |
| Missions / Study Session | `mission/*.html` | Sidebar text | Mission hero cards | Token-aligned |
| Feedback / Check-in | `research/checkin.html` | Sidebar text | Reuses mission-hero patterns | Clear product-research copy |
| Analytics | `analytics/index.html` | Sidebar text | Standard shell | — |
| Study Plan / Wizard | `study_plan/*` + `wizard.css` | Sidebar / wizard chrome | Token-aligned wizard | — |
| Calibration | `calibration/alpha.html` | Shell | — | “Alpha” = calibration capability, not brand badge |
| Navigation | `partials/sidebar.html`, `topnav.html` | Text brand in sidebar; topnav = email | — | No logo image; no Alpha chip |
| Footer | `layouts/base.html`, `auth_base.html` | Version string only | — | `Kwalitec v{{ app_version }}` — no Alpha |
| Errors | `errors/*.html` | Inherit layout | — | Minimal |

**Inconsistencies recorded**

1. Login icon mark vs authenticated text-only brand.  
2. FOS card styling vs student/research `.command-card`.  
3. Alpha identity only on login (flagged) + Settings — missing ambient chrome.  
4. No shared logo component/partial.  
5. Abstract landing shapes instead of product/brand imagery.  
6. System font stack only — no brand typeface.

---

## Internal Alpha Identity

| Location | Present? | Form |
|---|---|---|
| Landing / Login | Conditional | “New to the Internal Alpha?” when `internal_alpha_enabled` |
| Navbar / Topnav | No | — |
| Sidebar | No | Tagline only (`PRODUCT_TAGLINE`) |
| Student Dashboard | No | — |
| Founder OS Dashboard | Section title “Internal Alpha” for **metrics**, not product badge | Easy to confuse with brand identity |
| Research Command Centre | “Internal Alpha Summary” metrics heading | Operational, not chrome badge |
| Footer | No | Version only |
| Settings → Internal Alpha | Yes | Version 4.3, build, enablement, curriculum/plan/twin labels |

**Ideal placement (recommendation only — not implemented)**

1. Persistent badge beside sidebar wordmark: `Internal Alpha`.  
2. Footer: `Kwalitec v1.0.0 · Internal Alpha`.  
3. Login: always show programme note during Internal Alpha (decouple from EI env flag if product Alpha ≠ EI flag).  

**Templates/components that would require updates (future)**

- `partials/sidebar.html`  
- `layouts/base.html` / `layouts/auth_base.html`  
- `auth/login.html` (flag coupling)  
- Optionally `founder_dashboard/index.html` header eyebrow  

---

## Logo Audit — Asset Inventory

| Asset | Path | Status | Referenced by |
|---|---|---|---|
| *(none)* | `app/static/images/.gitkeep` | Placeholder only | — |
| Inline SVG mark | Embedded in `auth/login.html` | Not a file asset; layers/book icon | Login landing only |
| Wordmark text | “Kwalitec” | Ubiquitous text | Sidebar, titles, footers |

| Category | Count |
|---|---|
| Tracked PNG/SVG/ICO/WebP/JPG | **0** |
| Duplicate logo files | N/A |
| Unused logo files | N/A |
| Hardcoded image `url_for('static', filename='images/...')` | **None found** |

**Conclusion:** There is no logo asset system to reconcile — branding currently depends on typography and one inline SVG.

---

## Branding Asset Audit (Favicon / PWA / Social)

| Asset type | Implemented? | Notes |
|---|---|---|
| Favicon | No | No `rel="icon"` |
| App icon | No | — |
| Apple touch icon | No | — |
| PWA icons / manifest | No | No `manifest.json` / `.webmanifest` |
| Open Graph image | No | No `og:image` |
| Social / Twitter preview | No | No `twitter:image` |

**Consistent branding system?** No — meta/brand assets are absent. Colour/typography tokens in `app.css` are the only coherent design system layer.

---

## UI Consistency Review

**Strengths**

- Shared semantic CSS variables (light/dark) in `app/static/css/app.css`.  
- Student shell (sidebar + topnav + command cards) is largely consistent across Dashboard, Mission, Analytics, Settings, Research check-in.  
- Bootstrap 5 + custom tokens rather than one-off colour hardcoding in most places.

**Divergences**

| Area | Divergence |
|---|---|
| Login / public | Full-bleed split landing; unique logo treatment; public appearance switcher |
| FOS Dashboard | Own CSS/JS package; metric cards; uppercase section titles |
| Research Command Centre | Dense operational UI; many metric tiles; filters — visually heavier |
| Wizard | Dedicated `wizard.css` (token-aligned) |
| Empty states | Shared partial exists; usage uneven |

**Spacing / radius / buttons**

- Global `--radius`, spacing scale, `.btn-primary` hierarchy generally shared.  
- Research choice radios use outline secondary pills — slightly different interaction pattern from wizard pills but acceptable.

---

## Technical Review

### Templates

| Path | Role |
|---|---|
| `app/founder/dashboard/templates/founder_dashboard/index.html` | FOS Founder Dashboard |
| `app/templates/research/founder_dashboard.html` | Research Command Centre |
| `app/templates/research/checkin.html` | Product Check-in |
| `app/templates/research/thank_you.html` | Post check-in |
| `app/templates/research/founder_review.html` | Review marks |
| `app/templates/research/finding_detail.html` | Product finding |
| `app/templates/layouts/base.html` | Authenticated shell |
| `app/templates/layouts/auth_base.html` | Public shell |
| `app/templates/partials/sidebar.html` | Nav / brand |
| `app/templates/partials/topnav.html` | Top chrome |
| `app/templates/auth/login.html` | Landing + login |
| `app/templates/dashboard/index.html` | Student dashboard |
| `app/templates/settings/index.html` | Settings + Alpha status |
| `app/templates/mission/*`, `study_plan/*`, `analytics/*`, `errors/*`, `calibration/*` | Remaining UX |

### Blueprints

| Blueprint | Prefix | Relevance |
|---|---|---|
| `founder_dashboard` | `/founder` | FOS executive UI |
| `research` | `/research` | Check-in + Command Centre |
| `auth` | (auth) | Login only |
| `dashboard`, `mission`, `study_plan`, `analytics`, `settings`, `calibration` | various | Student surfaces |

### Services / components

| Module | Role |
|---|---|
| `FounderDashboardService` | FOS DTO aggregation |
| `FounderOperationalStateService` | Snapshot coordinator |
| `InternalAlphaProvider` / `StaticInternalAlphaSource` | Unwired HTTP alpha |
| `InternalAlphaWorkflowService` | CLI/manual week pipeline + inject |
| `FounderResearchService` | Command Centre |
| `ResearchFeedbackService` | Check-in persistence |
| `ResearchInsightService` | RIP-004 insights |
| `ContributorRecognitionService` | Badges |
| `InternalAlphaStatusService` | Settings Alpha status |
| `ProductCommunicationService` | Honest copy helpers |

### Static assets

| Path | Role |
|---|---|
| `app/static/css/app.css` | Design system |
| `app/static/css/wizard.css` | Wizard |
| `app/static/js/app.js`, `theme.js`, `mission.js`, `study_session.js` | App behaviour |
| `app/founder/dashboard/static/css/founder_dashboard.css` | FOS styles |
| `app/founder/dashboard/static/js/founder_dashboard.js` | Capability filter |
| `app/static/images/` | **Empty** |

### Database models (research)

- `ResearchFeedbackSubmission`  
- `ResearchContribution`  
- `ResearchContributorBadge`  
- `ResearchFeedbackReview`  
- `ResearchFeedbackStatusTransition`  
- `ResearchFounderNote`  
- `ResearchProductFinding` (+ links, status transitions)  

### Key queries

- `ResearchFeedbackSubmission.query.all()` — summary & product health  
- Inbox: `order_by(submitted_at.desc()).limit(50)` + filters  
- Day windows: naive `datetime.combine(day, min)` ranges  
- Distinct mission users for participation denominator  

---

## Recommended Internal Alpha Hotfix Backlog

### IAHF-001 — Founder Navigation to Research Command Centre

**Priority:** Critical  
**Complexity:** Low  
**Dependencies:** None  

**Acceptance Criteria:**

- Founder-only sidebar (or Founder submenu) links to `/research/founder`.  
- “Founder” FOS entry remains available and clearly labelled (e.g. “Founder OS” vs “Research”).  
- Ordinary students never see these links.

---

### IAHF-002 — Clarify or Wire FOS Internal Alpha Metrics

**Priority:** Critical  
**Complexity:** Medium  
**Dependencies:** Product decision (wire DB vs filesystem vs both)

**Acceptance Criteria:**

- `/founder` must not silently show `0` feedback when live check-ins exist **or** must explicitly label metrics as “filesystem pipeline only / unwired”.  
- If wired: HTTP Operational State Internal Alpha reflects an agreed live source; tests cover non-zero path.  
- Cross-link to Research Command Centre when check-in data is the source of truth.

---

### IAHF-003 — Founder Dashboard Synchronisation (Research Centre)

**Priority:** Critical  
**Complexity:** Medium  
**Dependencies:** IAHF-001 (discoverability)

**Acceptance Criteria:**

- Founder metrics update correctly after check-in + reload.  
- Feedback appears at top of inbox after reload.  
- “Today so far” (or equivalent) exists alongside yesterday deltas.  
- Newest contributions visible on the Command Centre home.  
- Dashboard statistics remain consistent with DB counts for fixture scenarios.

---

### IAHF-004 — Inbox Completeness (Pagination / Limits)

**Priority:** High  
**Complexity:** Medium  
**Dependencies:** None  

**Acceptance Criteria:**

- Founders can access submissions beyond the first 50.  
- UI shows total matching count when truncated.  
- Combined badge + student filters return correct results (tests).

---

### IAHF-005 — Internal Alpha Chrome Badge

**Priority:** High  
**Complexity:** Low  
**Dependencies:** None (copy decision only)

**Acceptance Criteria:**

- Authenticated shell shows Internal Alpha identity in sidebar and/or footer.  
- Login communicates Internal Alpha without depending solely on EI feature flag (unless product decides they are the same).  
- Student Dashboard first viewport includes a discreet Alpha indicator.

---

### IAHF-006 — Brand Logo Asset Pack + Consistent Mark

**Priority:** High  
**Complexity:** Medium  
**Dependencies:** Approved logo files from brand owner  

**Acceptance Criteria:**

- Canonical SVG (+ PNG fallbacks) committed under `app/static/images/`.  
- Login, sidebar, and footer use the same mark via one partial.  
- Inline one-off SVG removed or aligned to canonical mark.  
- Sizes documented (e.g. sidebar 24px, landing 36px).

---

### IAHF-007 — Favicon / Touch / OG Meta Pack

**Priority:** High  
**Complexity:** Low–Medium  
**Dependencies:** IAHF-006 assets  

**Acceptance Criteria:**

- Favicon appears in browser tabs (auth + app layouts).  
- Apple touch icon present.  
- Basic `og:image` (and optional Twitter card) for shared links.  
- Optional web manifest for installability (nice-to-have for Alpha).

---

### IAHF-008 — FOS Capability / Week Presentation Completeness

**Priority:** Medium  
**Complexity:** Low–Medium  
**Dependencies:** IAHF-002 if alpha week counts required  

**Acceptance Criteria:**

- Capability rows show title/status when archive provides them.  
- Recent week summaries do not hardcode zero when data exists.  
- Empty states remain honest when data is unavailable.

---

### IAHF-009 — Timestamp / Day-Boundary Hardening

**Priority:** Medium  
**Complexity:** Medium  
**Dependencies:** None  

**Acceptance Criteria:**

- “Yesterday / today” buckets use a documented timezone policy (prefer UTC or explicit `APP_TIMEZONE`).  
- Tests cover near-midnight submissions.  
- UI labels state the timezone basis.

---

### IAHF-010 — Product Health Heuristic Honesty

**Priority:** Medium  
**Complexity:** Low  
**Dependencies:** None  

**Acceptance Criteria:**

- “Most confusing feature” uses a defensible definition (e.g. classification Confusing and/or friction≠Nothing on friction field — not loved-feature conflation).  
- Labels/tooltips explain the heuristic.

---

### IAHF-011 — Founder Operator Runbook (Docs-only)

**Priority:** Medium  
**Complexity:** Low  
**Dependencies:** IAHF-001–003 decisions  

**Acceptance Criteria:**

- Short operator doc: which URL shows live check-ins; how FOS filesystem weeks work; refresh = reload; when to run FSI-003 workflow.  
- Linked from `knowledge/founder/` or POP docs.

---

### IAHF-012 — Visual Harmonisation Pass (FOS ↔ Student Shell)

**Priority:** Low  
**Complexity:** Medium  
**Dependencies:** IAHF-006 preferred  

**Acceptance Criteria:**

- FOS dashboard reuses shared section/metric patterns where practical.  
- No requirement for charts/animation.  
- Dark/light themes remain token-driven.

---

## Overall Operational Readiness

| Dimension | Ready? | Notes |
|---|---|---|
| Student study loop | **Yes** | Dashboard / missions / plans operational for Internal Alpha |
| Product Check-in capture | **Yes** | Persists correctly to DB |
| Founder live feedback ops | **Partial / No** | Works only if Founder knows `/research/founder` and reloads |
| Founder OS executive metrics | **Partial** | Knowledge/Capability live; Internal Alpha feedback **not** live on HTTP |
| Brand / Alpha identity | **No** | Missing assets + inconsistent Alpha signalling |
| Continue student Alpha? | **Yes, with caution** | Do not block studying |
| Treat Founder ops as stable? | **Not yet** | Resolve IAHF-001–003 first |

**Recommendation:** Proceed with Internal Alpha participant study activity, but treat **POP Sprint 1 Critical hotfixes (IAHF-001–003)** as prerequisites for trustworthy Founder operations. Brand pack + Alpha chrome (IAHF-005–007) should ship in the same sprint to protect participant confidence and professionalism.

---

## Success Criteria Checklist

| Criterion | Met? |
|---|---|
| Complete understanding of Founder Dashboard behaviour | Yes (both surfaces documented) |
| Complete inventory of branding inconsistencies | Yes |
| Complete inventory of logo assets | Yes (empty set) |
| Complete understanding of Internal Alpha identity | Yes |
| Prioritised Internal Alpha Hotfix backlog | Yes (IAHF-001–012) |
| Zero code changes | Yes — investigation document only |

---

## Investigation Method Notes

- Read-only inspection of blueprints, services, models, templates, static assets, and founder knowledge docs (FOS-003/004, FSI-002/003).  
- Confirmed **0** tracked image assets via `git ls-files`.  
- Confirmed `InternalAlphaProvider` defaults to empty static source; Knowledge/Capability use live query providers.  
- No application code, UI, assets, packages, or commits were modified for this milestone beyond adding this investigation document under `knowledge/investigations/`.
