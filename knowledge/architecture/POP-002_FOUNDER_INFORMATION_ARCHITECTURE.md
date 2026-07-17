# POP-002 — Founder Information Architecture

**Programme:** Product Operations Programme (POP)  
**Milestone:** POP-002  
**Status:** Architecture & UX Design — complete; authoritative blueprint for POP Sprint 1  
**Date:** 2026-07-17  
**Nature:** Architecture and product design only — **no application code changes**  
**Supersedes (navigation intent):** Dual Founder entry model documented in POP-001  
**Companion investigation:** [`knowledge/investigations/POP-001_FOUNDER_DASHBOARD_AND_BRAND_AUDIT.md`](../investigations/POP-001_FOUNDER_DASHBOARD_AND_BRAND_AUDIT.md)

---

## Executive Summary

If Kwalitec Version 1 were being designed today, the Founder would open **one place**: the **Founder Command Centre**.

That surface is not a second product and not a parallel “research app.” It is the operator console for Internal Alpha — organised around **daily operational questions**, fed by **one live operational source of truth**, reachable from **one sidebar entry**, with every operational area at most **two clicks** away.

### Overall philosophy

| Law | Statement |
|---|---|
| **One door** | There is a single Founder entry point. The Founder never chooses between dashboards. |
| **One truth** | Founder metrics for product feedback, participation, and review workflow come from live operational data (database-backed Product Check-ins and related research records). Filesystem pipelines may support offline processing; they must not silently present empty “operational” numbers. |
| **Workflows over entities** | Navigation is named for jobs (“What needs action?”, “Is Alpha healthy?”), not for tables or historical programme codes (FOS vs RIP). |
| **Answer first** | The homepage answers the Founder’s most important questions within ~10 seconds; deeper sections exist for work, not for dumping every metric. |
| **Two-click reach** | From the Command Centre shell, any operational area is ≤2 clicks. |
| **Honest emptiness** | Missing or unwired data is labelled as unavailable — never shown as zero without context. |
| **Educational boundary** | Founder Command Centre observes **product operations** and **system readiness**. It does not rewrite Educational Intelligence, readiness maths, or student learning authority (aligned with RIP hard boundary). |

This document is the **authoritative Information Architecture specification** for Founder operations. Implementation belongs to later POP / Internal Alpha Hotfix milestones; this milestone defines *what* to build, not *how* to code it.

---

## Current Architecture

> **Historical baseline (POP-001 / pre–IAHF-003).** This section records the dual-home Founder topology that POP-002 was designed to replace. For live Version1-RC2 routes and naming, see **Document Control → Implementation status** and `knowledge/releases/IAHF-003_IMPLEMENTATION_REPORT.md`.

Grounded in the live application as audited in POP-001 and reconfirmed for POP-002 (routes, sidebar, FOS package, Research Command Centre).

### Surface inventory

| Surface | URL | Audience gate | Primary data | In sidebar? |
|---|---|---|---|---|
| Founder Operating System (FOS-004) Dashboard | `/founder` | `@founder_required` | Operational State (Knowledge + Capability live; Internal Alpha **static empty** on HTTP) | Yes — labelled **Founder** |
| Research Command Centre (RIP-003) | `/research/founder` | `@founder_required` | Live `research_feedback_*` models | **No** |
| Product Finding detail | `/research/founder/finding/<id>` | Founder | Live findings | No (in-page only) |
| Feedback review form | `/research/founder/review/<id>` | Founder | Live review marks | No |
| Award Founder’s Circle | `POST /research/founder/award-founders-circle/<user_id>` | Founder | Badges | No |
| Product Check-in (student) | `/research/checkin` | Any authenticated user | Writes live submissions | Yes — **Share Feedback** |
| Settings → Internal Alpha Status | `/settings` | Any authenticated user | Alpha version / enablement | Yes — Settings |
| Student Dashboard / Analytics / Missions | various | Students (Founders also land here) | Learning data | Yes — Main / Analysis |

Post-login destination for **all** users (including Founders) is the **student** Dashboard (`dashboard.index`). There is no Founder home after authentication.

### Strengths

1. **Clear Founder authorisation** — `ADMIN_EMAIL` ∪ `FOUNDER_EMAILS` via `@founder_required`; students receive 403 on Founder routes.
2. **Research Command Centre is operationally rich** — inbox, workflow lifecycle, marks, notes, Product Findings, insights, participation metrics, all from live SQLAlchemy data.
3. **FOS package is well-layered** — providers → Operational State → Dashboard DTOs; Knowledge and Capability archives are live via FSI integrations.
4. **Hard educational boundary is documented** (RIP) — Research Intelligence must not write educational evidence or twin state.
5. **Student check-in capture works** — submissions commit immediately; live Founder reads succeed after reload on `/research/founder`.

### Weaknesses

1. **Two Founder “homes” with different truths** — `/founder` and `/research/founder` both read as executive dashboards; only one shows Product Check-ins.
2. **Navigable surface is the wrong one for daily ops** — Sidebar “Founder” opens FOS; live feedback ops are undiscoverable without memorising a URL.
3. **Internal Alpha panel on FOS is unwired for HTTP** — empty static source presents `feedback_count=0` as if operational.
4. **Dual feedback artefacts** — Filesystem FOS-003 week `.txt` pipeline vs database Product Check-ins; naming (“Internal Alpha”, “feedback”) collides.
5. **Sidebar active-state collision** — `request.endpoint.startswith('research.')` highlights **Share Feedback** even when the Founder is on the Research Command Centre.
6. **No Founder-specific shell** — Founders share student Main/Analysis nav; Command Centre work competes with Study Plan / Study Session chrome.
7. **Homepage overload on Research Centre** — summary + yesterday + product health + insights + inbox + findings on one scroll; no triage-first hierarchy.
8. **Incomplete presentation** — e.g. newest contributions computed but not rendered; capability titles emptied in FOS mapping; inbox hard-capped at 50.

### Pain points (Founder experience)

| Question the Founder asks | Current answer |
|---|---|
| Which dashboard do I use? | Ambiguous — two exist. |
| Where is today’s check-in? | Only on `/research/founder` after reload — not linked. |
| Why does Founder show zero feedback? | FOS Internal Alpha provider is empty — looks like a sync bug. |
| What needs my attention first? | Buried in a dense Research page; outstanding reviews exist but aren’t a first-class destination. |
| Did I land in the right product role? | Login always drops into student Dashboard. |
| Is Internal Alpha healthy? | Split across Research metrics, Settings status, and empty FOS panel. |

---

## Founder Workflow Analysis

### Workflows currently supported

| ID | Workflow | Where today | Data | Overlap |
|---|---|---|---|---|
| W1 | Review Product Check-in inbox | `/research/founder` | Live DB | — |
| W2 | Filter / search submissions | `/research/founder` | Live DB | — |
| W3 | Open feedback detail | `/research/founder?submission=` | Live DB | Overlaps W8 |
| W4 | Mark Helpful / Insightful | Command Centre actions + `/research/founder/review/<id>` | Live DB | **Duplicated paths** |
| W5 | Advance feedback workflow status | Command Centre transitions | Live DB | — |
| W6 | Add internal Founder note | Command Centre | Live DB | — |
| W7 | Create / manage Product Findings | Command Centre + finding detail | Live DB | — |
| W8 | Award contributor badges / Founder’s Circle | Command Centre | Live DB | — |
| W9 | Monitor Internal Alpha participation & health | Research summary tiles | Live DB | **Overlaps W12** (conceptually) |
| W10 | View product health heuristics | Research Product Health | Live DB | — |
| W11 | View Research Insights (RIP-004) | Research Insights section | Live DB | — |
| W12 | View Internal Alpha week / categories | FOS Internal Alpha panel | **Static empty / filesystem** | **Conflicts with W9** |
| W13 | View engineering / architecture health signals | FOS Engineering | Operational State | — |
| W14 | Browse Knowledge artefact counts | FOS Knowledge | Live Knowledge Engine | — |
| W15 | Browse Capability inventory | FOS Capabilities | Live Capability Archive | Incomplete titles |
| W16 | Read top Founder recommendations | FOS Recommendations | Recommendation Engine from state | — |
| W17 | View Weekly Brief metadata | FOS Weekly Brief | Brief service | — |
| W18 | Check Internal Alpha product/build status | Settings → Internal Alpha | Status service | Ambient identity gap (POP-001) |
| W19 | Submit Product Check-in | `/research/checkin` | Writes DB | **Student workflow** — not Founder ops |
| W20 | View own learning Analytics | `/analytics` | Student analytics | **Student workflow** |

### Overlap conclusions

1. **W9 vs W12** — Same Founder question (“How is Internal Alpha doing?”), two incompatible answers. **Must collapse to one live source.**
2. **W4** — Review marks available both inline and on a separate review page; keep one primary interaction path (inline) and treat the standalone page as optional or merge.
3. **W19** — Student intake must remain separate from Founder ops; nav label “Share Feedback” must never be the Founder’s path to research operations.
4. **FOS executive metrics (W13–W17)** are valuable but secondary to daily feedback triage during Internal Alpha; they belong under **Operations**, not as the sole “Founder” home.

### Workflows the Founder needs but lack a coherent home

| Need | Status |
|---|---|
| “What happened today?” strip | Partially — yesterday panel excludes today; newest list not rendered |
| Attention queue (outstanding reviews first) | Metric exists; not a dedicated workflow surface |
| Participant roster / who needs a nudge | Only aggregates + filters — no Participants section |
| Release / build health at a glance | Scattered (footer version, Settings Alpha, FOS release label) |
| Post-login Founder landing | Missing — always student Dashboard |
| Single Command Centre nav tree | Missing |

---

## Founder Navigation Audit

### Current navigation map

```text
Login
  └─► Student Dashboard (/)                          [all users]

Authenticated sidebar
  Main
    ├─ Dashboard          → student home
    ├─ Study Plan         → student
    └─ Study Session      → student
  Analysis
    └─ Analytics          → student learning analytics
  System
    ├─ Founder            → /founder  (FOS only)           [Founder emails]
    ├─ Settings           → /settings (+ Internal Alpha status)
    └─ Share Feedback     → /research/checkin              [student intake]
         ✗ does NOT link to Research Command Centre

Undiscoverable (URL / in-page only)
  /research/founder                    Research Command Centre (LIVE ops)
  /research/founder/finding/<id>       Finding detail
  /research/founder/review/<id>        Standalone review
  POST …/award-founders-circle/<id>    Badge award

Dead ends / traps
  • Sidebar “Founder” never reaches live check-ins
  • Active nav highlights “Share Feedback” on /research/founder*
  • FOS Internal Alpha metrics look like live ops but are empty
  • No breadcrumb from Research back to FOS (or vice versa)
  • No Founder submenu — flat single link
```

### Issues catalogue

| Type | Detail |
|---|---|
| Duplicated dashboards | `/founder` and `/research/founder` both act as Founder homes |
| Duplicated routes (conceptual) | Two “Internal Alpha” metric stories |
| Dead end | FOS Internal Alpha panel with no path to live inbox |
| Missing nav | Research Command Centre, Findings, Participants |
| Inconsistent nav | “Founder” vs “Research Command Centre” naming; “Share Feedback” vs “Product Check-in” |
| Wrong active state | `research.*` → Share Feedback |
| Missing post-login IA | Founders start in student product |

---

## Proposed Information Architecture

### Naming

| Term | Meaning |
|---|---|
| **Founder Command Centre** | The single Founder product area (entry + shell + homepage). |
| **Overview** | Command Centre homepage — answers daily questions; not a second dashboard. |
| **Section** | First-level area under the Command Centre (≤1 click from Overview chrome). |
| **Operational source of truth** | Live application data for Product Check-ins, reviews, findings, badges, and derived summaries. |

Historical labels **FOS Dashboard** and **Research Command Centre** become implementation heritage, not user-facing product names.

### Complete hierarchy

```text
Founder Command Centre                         ← ONE entry (sidebar: “Founder”)
│
├── Overview                                   ← Homepage after Founder entry / preferred post-login
│
├── Attention                                  ← Triage queue: outstanding & urgent work
│
├── Feedback                                   ← Full research inbox + submission workflow
│   ├── Submission detail                      ← Same IA node; deep link
│   └── Review actions                         ← Inline primary; no parallel “second app”
│
├── Findings                                   ← Product Findings list + create
│   └── Finding detail                         ← Status, links, target release
│
├── Research                                   ← Insights, product health, trends (read/decide)
│
├── Internal Alpha                             ← Programme health (participation, week, status)
│
├── Participants                               ← Students in Alpha: activity, badges, awards
│
├── Operations                                 ← System & engineering readiness
│   ├── System Health                          ← Engineering / architecture signals
│   ├── Knowledge                              ← Knowledge Engine counts / index health
│   ├── Capabilities                           ← Capability Archive inventory
│   ├── Recommendations                        ← Founder Recommendation Engine outputs
│   └── Weekly Brief                           ← Brief metadata / latest brief
│
├── Releases                                   ← Release labels, comparisons, findings by target
│
└── Settings                                   ← Founder-relevant ops settings
    └── (deep-link) Product Settings           ← Shared Settings / Internal Alpha status
```

### Reserved future modules (nav slots, not built)

These do **not** appear in Version 1 Internal Alpha chrome until real, but the hierarchy reserves space under clear parents:

| Future module | Parent | Notes |
|---|---|---|
| Educational Analytics (Founder view) | Operations → or new **Learning Ops** sibling | Observe only; never override student EI authority |
| Curriculum Intelligence | Learning Ops | Syllabus / V1–V2 traversal health |
| Student Digital Twin Analytics | Learning Ops | Aggregate, anonymised where required |
| Recommendation Engine Monitoring | Operations | Distinct from Founder Recommendation Engine (FOS-006) |
| AI Insights | Research or Learning Ops | Explicitly gated; not in core deterministic path |
| Experiment Tracking | Releases | Feature flags / experiments |
| Founder Notifications | Overview + Attention | Alert delivery; not a separate “dashboard” |
| Release Management (richer) | Releases | Expand from comparison tiles |

### Hierarchy design rationale

1. **Overview first** — mirrors PTP-004 “answer the most important question first,” applied to Founder ops.
2. **Attention before Feedback** — Founders usually need *what to do*, then the full inbox.
3. **Findings separate from Feedback** — Findings are decision artefacts; submissions are evidence.
4. **Research vs Internal Alpha** — Research = patterns & product experience; Internal Alpha = programme pulse (participation, week, enablement).
5. **Operations groups FOS strengths** — Knowledge, Capabilities, Recommendations, Briefs stay valuable without pretending to be the daily feedback console.
6. **Releases early enough** — Internal Alpha ships often; release context must be visible without hunting Settings.

---

## Dashboard Modules

For each first-level section:

### Overview

| Field | Specification |
|---|---|
| **Purpose** | Orient the Founder in ≤10 seconds; surface alerts and next actions. |
| **Primary audience** | Founder / admin operators |
| **Key metrics** | Check-ins today; outstanding reviews; Active participants; Alpha health status; System health status; Open high-severity findings |
| **Primary actions** | Open Attention; Open newest feedback; Open Internal Alpha; Open Operations if unhealthy |
| **Dependencies** | Live feedback summaries; finding counts; Operational State health; Alpha status |
| **Update frequency** | Every page load (live). Optional soft refresh later — not required for IA. |

### Attention

| Field | Specification |
|---|---|
| **Purpose** | Single triage list of work requiring Founder action. |
| **Primary audience** | Founder |
| **Key metrics** | Count by urgency: New reviews, Clarification requested, High-severity findings, Stale under-review items |
| **Primary actions** | Open item → Feedback or Finding detail; transition status; mark helpful/insightful |
| **Dependencies** | Feedback workflow statuses; finding severities; age heuristics |
| **Update frequency** | Live per request |

### Feedback

| Field | Specification |
|---|---|
| **Purpose** | Complete Product Check-in inbox and submission lifecycle. |
| **Primary audience** | Founder |
| **Key metrics** | Filtered result count; status distribution; source (study session vs settings) |
| **Primary actions** | Filter/search; open detail; marks; transitions; notes; link to finding |
| **Dependencies** | `ResearchFeedbackSubmission` and related review/transition/note models |
| **Update frequency** | Live; pagination required beyond current 50-item ceiling (implementation later) |

### Findings

| Field | Specification |
|---|---|
| **Purpose** | Manage Product Findings as roadmap-facing decision objects. |
| **Primary audience** | Founder |
| **Key metrics** | Open by severity; by status; by target release |
| **Primary actions** | Create finding; transition status; set target release; open linked feedback |
| **Dependencies** | Product Finding models + linked submissions |
| **Update frequency** | Live |

### Research

| Field | Specification |
|---|---|
| **Purpose** | Understand product experience patterns without performing inbox triage. |
| **Primary audience** | Founder |
| **Key metrics** | Product health heuristics; insight trends; participation trends; release comparison |
| **Primary actions** | Change time window; drill to Feedback with pre-filled filters; open Findings |
| **Dependencies** | Research Insight Engine; Product Health aggregations |
| **Update frequency** | Live (windowed). Labels must state window and timezone policy. |

### Internal Alpha

| Field | Specification |
|---|---|
| **Purpose** | Answer “Is Internal Alpha healthy?” with one coherent programme view. |
| **Primary audience** | Founder |
| **Key metrics** | Active participants; completed check-ins; participation rate; avg experience; return intent; confidence; outstanding vs implemented; Product Shapers; current Alpha version/build/enablement |
| **Primary actions** | Jump to Participants; Jump to Feedback; Open Settings Alpha detail |
| **Dependencies** | Live check-in aggregates **as source of truth**; Settings Alpha status for build identity. Filesystem week pipeline may appear as a clearly labelled **secondary** “Offline week processing” panel only if still used — never as silent zeros. |
| **Update frequency** | Live for DB metrics; status as configured |

### Participants

| Field | Specification |
|---|---|
| **Purpose** | See who is in the Alpha loop and recognise contributors. |
| **Primary audience** | Founder |
| **Key metrics** | Participant list; last check-in; badge set; contribution counts |
| **Primary actions** | Filter by badge/activity; award Founder’s Circle; open student’s feedback |
| **Dependencies** | Submissions; contributor badges; recognition service |
| **Update frequency** | Live |

### Operations

| Field | Specification |
|---|---|
| **Purpose** | Answer “Is the system operating correctly?” using FOS operational subsystems. |
| **Primary audience** | Founder / technical operator |
| **Key metrics** | Engineering & architecture health; capability completed/active; knowledge counts; recommendation status; weekly brief freshness |
| **Primary actions** | Inspect capability list; open recommendations; open weekly brief |
| **Dependencies** | Operational State; Knowledge Engine; Capability Archive; Recommendation Engine; Weekly Briefing |
| **Update frequency** | Live per request from Operational State providers |

### Releases

| Field | Specification |
|---|---|
| **Purpose** | Tie feedback and findings to release identity and change over time. |
| **Primary audience** | Founder |
| **Key metrics** | Current app / Alpha version labels; findings by target release; release comparison insights |
| **Primary actions** | Set comparison releases; open findings for a release |
| **Dependencies** | Version/config surfaces; insight release comparison; finding target_release |
| **Update frequency** | Live / on config change |

### Settings (Founder)

| Field | Specification |
|---|---|
| **Purpose** | Operator configuration and Alpha identity detail without leaving Founder IA. |
| **Primary audience** | Founder |
| **Key metrics** | Alpha enablement, version, build labels (via existing status) |
| **Primary actions** | Deep-link to product Settings Internal Alpha section; future Founder notification prefs |
| **Dependencies** | Settings / Internal Alpha status services |
| **Update frequency** | On visit |

---

## Founder Homepage Specification

### Role

The **Overview** is the Founder homepage. It is the only page that should feel like “the dashboard.” All other sections are workspaces.

### Recommended layout (top → bottom)

```text
┌─────────────────────────────────────────────────────────────────┐
│ Founder Command Centre · Internal Alpha · v{app} · {build}      │
│ Last refreshed: {timestamp} · Timezone: {policy}                │
├─────────────────────────────────────────────────────────────────┤
│ A. Top summary cards (one row)                                  │
│    [Today] [Needs action] [Alpha health] [System health]        │
├─────────────────────────────────────────────────────────────────┤
│ B. Operational alerts                                           │
│    Critical / High only — empty state: “No alerts”              │
├─────────────────────────────────────────────────────────────────┤
│ C. Two-column work strip                                        │
│    Left: Recent feedback (newest)     Right: Attention queue    │
├─────────────────────────────────────────────────────────────────┤
│ D. Programme pulse                                              │
│    Recent Product Check-ins summary · Participation snapshot    │
├─────────────────────────────────────────────────────────────────┤
│ E. Research snapshot (compact)                                  │
│    Top trend · Top friction · Link: Research                    │
├─────────────────────────────────────────────────────────────────┤
│ F. Operations snapshot (compact)                                │
│    System health · Capabilities · Link: Operations              │
├─────────────────────────────────────────────────────────────────┤
│ G. Deployment / build information                               │
│    App version · Internal Alpha version · Release label         │
└─────────────────────────────────────────────────────────────────┘
```

### Top summary cards

| Card | Answers | Primary click-through |
|---|---|---|
| **Today** | What happened today? Check-ins today; participants active today | Feedback (today filter) |
| **Needs action** | Outstanding reviews + open high-severity findings | Attention |
| **Alpha health** | Participation / return intent / experience at a glance | Internal Alpha |
| **System health** | Engineering/architecture signal | Operations → System Health |

### Operational alerts

Show only actionable conditions, for example:

- Outstanding reviews above threshold or aging > N days  
- High/Critical finding opened or stalled  
- Alpha enablement off unexpectedly  
- Operational State validation failures / unhealthy signals  
- Inbox truncated (“Showing 50 of M — open Feedback”)

Do **not** alert on healthy zeros without context.

### Recommended operational widgets

| Widget | Content | Avoid |
|---|---|---|
| Recent feedback | Newest submissions (id, student, feature, status, time) | Full filter chrome |
| Attention queue | Top N actionable items | Entire inbox |
| Product Check-ins pulse | Today + 7-day participation | Replacing Internal Alpha section |
| Research snapshot | 2–3 insight highlights | Full RIP-004 layout |
| System health | One status + one sentence | Full capability table |
| Deployment / build | Versions aligned with Settings | Conflicting version numbers |

### Explicit non-goals for Overview

- Not a second Research Insights page  
- Not a capability archive browser  
- Not student learning analytics  
- Not a place to show filesystem pipeline zeros as “feedback received”

### Post-login recommendation

For users with Founder privileges, **default landing after login should be Founder Overview** (or offer a persistent preference). Ordinary students continue to land on the student Dashboard. This is an IA rule for Sprint 1 planning; implementation is deferred.

---

## Founder Navigation Map

### Current → Proposed

```text
CURRENT                                              PROPOSED
=======                                              ========

Sidebar: Founder ──► /founder (FOS)                  Sidebar: Founder ──► Command Centre Overview
                         │                                              │
                         ├─ empty Internal Alpha                        ├─ Attention
                         ├─ Knowledge / Capabilities                    ├─ Feedback  ←── live inbox (today’s /research/founder)
                         └─ Recommendations / Brief                     ├─ Findings
                                                                        ├─ Research
URL-only: /research/founder (LIVE)  ──merge──►                          ├─ Internal Alpha
          /research/founder/finding/* ──retain under Findings           ├─ Participants
          /research/founder/review/*  ──fold into Feedback               ├─ Operations (FOS strengths)
                                                                         ├─ Releases
Sidebar: Share Feedback → student check-in                               └─ Settings
         (unchanged for students)                                       
                                                                         Share Feedback remains STUDENT intake
                                                                         (never the Founder ops entry)
```

### Proposed sidebar rules (Founder-visible)

When `show_founder_nav` is true:

1. **One** top-level item: **Founder** → Overview.  
2. Inside the Command Centre: persistent secondary nav (sidebar subsection or in-page nav) listing the hierarchy above — **same order everywhere**.  
3. Student Main/Analysis items may remain for Founders who also study, but must not be required to reach ops.  
4. **Share Feedback** stays the student Product Check-in entry; it must not activate when browsing Founder sections.  
5. Breadcrumbs: `Founder / {Section} / {Entity}` (e.g. `Founder / Findings / Login friction`).

### Two-click budget

| Destination | Path |
|---|---|
| Overview | Sidebar Founder (1) |
| Any section | Founder → Section link (2) |
| Submission detail | Founder → Feedback → item (2 from section; 3 from cold sidebar — acceptable for entity) |
| Finding detail | Founder → Findings → item |

Entity detail may take a third click; **sections** must remain within two.

---

## Navigation Principles

1. **One dashboard only** — Overview is the sole Founder home. No peer “second dashboard” URLs in chrome.  
2. **Single source of truth** — Product Check-in metrics and inbox read live operational data. Secondary offline pipelines are labelled secondary or hidden until wired.  
3. **No duplicated operational pages** — Do not maintain parallel FOS vs Research homes that answer the same question differently.  
4. **Consistent breadcrumb hierarchy** — Always `Founder / Section [/ Item]`.  
5. **Predictable sidebar ordering** — Fixed order as in the hierarchy (Overview → Attention → Feedback → Findings → Research → Internal Alpha → Participants → Operations → Releases → Settings).  
6. **Active state honesty** — Only the current Founder section highlights; student “Share Feedback” never steals active state from Founder routes.  
7. **Founder chrome ≠ student chrome** — Founder sections may use a denser operational layout, but shared design tokens and brand identity (per POP-001 brand follow-ups).  
8. **Deep links welcome; entry points singular** — Old URLs may redirect into the new tree; they must not remain marketed as alternate homes.  
9. **Workflow names in nav** — Prefer Attention, Feedback, Internal Alpha over programme IDs (RIP-003, FOS-004) in UI copy.  
10. **Empty states are instructional** — Tell the Founder whether data is missing, filtered out, or unwired.

---

## Operational Principles

Governing principles for Founder operations (product rules):

1. **Command Centre is authoritative** for Founder ops visibility.  
2. **Live data wins** for Internal Alpha product feedback.  
3. **Triage before analysis** — Attention and Feedback outrank Insights on the daily path.  
4. **Evidence → Finding → Release** — Submissions inform Findings; Findings carry target releases.  
5. **Deterministic aggregation** — No opaque AI in the core Founder path (insights remain pure aggregation unless a future module is explicitly introduced).  
6. **Educational non-interference** — Founder ops must not write educational evidence, mastery, readiness, or twin educational state.  
7. **Explainable metrics** — Every heuristic (e.g. “most confusing feature”) has a stated definition.  
8. **Timezone honesty** — Day buckets declare policy (UTC or `APP_TIMEZONE`).  
9. **Refresh contract** — Version 1 may require full page reload; Overview should say so until soft refresh exists.  
10. **Security** — Founder routes remain founder-gated; no leakage of other users’ resources beyond Alpha ops scope.  
11. **Idempotent honesty** — Re-opening Overview never invents activity; it reflects current operational state.  
12. **Scalable slots** — New modules attach under existing parents; they do not create a second Founder entry.

---

## Future Scalability

The IA is a **stable spine** with **extension points**:

```text
Founder Command Centre
├── Overview ......................... + Notifications widget (future)
├── Attention ........................ + SLA / notification rules
├── Feedback / Findings / Research ... + Experiment annotations
├── Internal Alpha ................... + cohort / week management UI
├── Participants ..................... + Digital Twin ops (read-only aggregates)
├── Operations ....................... + Recommendation monitoring, Curriculum Intelligence
│   └── (future) Learning Ops ........ Educational Analytics, Twin Analytics, AI Insights*
└── Releases ......................... + Experiment Tracking, Release Management
```

\*AI Insights only behind an explicit product decision; not part of deterministic educational cores.

**Rule:** New capability documentation (FOS/RIP/EI/etc.) may add **sections or widgets**, not new top-level Founder products competing with the Command Centre.

---

## Migration Recommendations

No implementation in POP-002. Guidance for POP Sprint 1+ (including IAHF items from POP-001):

### Pages to retain (evolve in place)

| Current | Becomes |
|---|---|
| Research inbox + detail + actions | **Feedback** section |
| Product Findings + finding detail | **Findings** section |
| Research Insights + Product Health | **Research** section |
| FOS Knowledge / Capabilities / Recommendations / Brief / Engineering health | **Operations** subsections |
| Settings Internal Alpha status | Linked from **Internal Alpha** + **Settings** |
| Student Product Check-in | Unchanged student intake |

### Pages to merge

| Merge | Into |
|---|---|
| `/founder` (FOS home) + `/research/founder` (Research home) | **Founder Command Centre Overview** + section tree |
| Standalone `/research/founder/review/<id>` (if redundant) | Inline Feedback actions |

### Pages to deprecate (as Founder *entry points*)

| Deprecate as home | Disposition |
|---|---|
| FOS Dashboard as sole “Founder” meaning | Replaced by Overview; FOS content lives under Operations |
| Research Command Centre as secret second home | Absorbed; URL redirects into Command Centre |
| Presenting Static Internal Alpha zeros as ops | Remove or relabel as offline pipeline |

### Pages to rename (user-facing)

| From | To |
|---|---|
| Founder Dashboard / Founder Operating System (eyebrow) | **Founder Command Centre** |
| Research Command Centre (as peer product) | **Feedback** / **Research** sections under Command Centre |
| Share Feedback (Founder confusion risk) | Keep for students; never use as Founder ops label |

### Pages / areas to introduce

| New | Role |
|---|---|
| Overview | Homepage |
| Attention | Triage |
| Participants | Roster & recognition |
| Releases | Release-oriented ops |
| Founder secondary nav | Two-click IA |
| Founder post-login landing (policy) | Role-appropriate home |

### Suggested URL evolution (design intent only)

Exact paths are an implementation choice for later milestones. Conceptual target:

```text
/founder                       → Overview
/founder/attention             → Attention
/founder/feedback              → Feedback (+ ?submission=)
/founder/findings              → Findings
/founder/findings/<id>         → Finding detail
/founder/research              → Research
/founder/internal-alpha        → Internal Alpha
/founder/participants          → Participants
/founder/operations            → Operations
/founder/releases              → Releases
/founder/settings              → Settings bridge

/research/founder              → permanent redirect into /founder/...  (compat)
/research/checkin              → remains student check-in
```

Compatibility redirects preserve bookmarks while enforcing **one door**.

### Alignment with POP-001 hotfixes

| Hotfix | IA implication |
|---|---|
| IAHF-001 Nav to Research | Superseded by single Command Centre nav — do not merely add a second sidebar peer long-term |
| IAHF-002 Wire or clarify FOS Alpha | Overview / Internal Alpha must use live SoT or honest labels |
| IAHF-003 Sync / today / newest | Overview + Feedback widgets |
| IAHF-004 Pagination | Feedback section |
| IAHF-005–007 Brand / Alpha chrome | Command Centre header + ambient Alpha badge |
| IAHF-008 FOS presentation | Operations subsections |
| IAHF-011 Operator runbook | Point to this IA as authoritative map |

---

## Acceptance Criteria

A new developer can rely on this document alone to answer:

| Question | Answered herein? |
|---|---|
| How many Founder entry points should exist? | Yes — one |
| What is the operational source of truth? | Yes — live Product Check-in / research data |
| What is the section hierarchy? | Yes — complete tree |
| What does the Founder see first? | Yes — Overview specification |
| How do current URLs evolve? | Yes — retain / merge / deprecate / rename / introduce |
| How do we extend for future modules? | Yes — reserved parents + scalability rules |
| What must never happen again? | Yes — dual homes, silent empty metrics, student intake as Founder ops nav |

**Pass condition:** This file is the blueprint for implementing POP Sprint 1 and establishing a single, coherent Founder Command Centre.

---

## Success Criteria

> If Kwalitec Version 1 were being designed today, what would the Founder experience look like?

**Answer:** One **Founder Command Centre**. The Founder signs in, lands on **Overview**, sees what happened today, what needs action, whether Internal Alpha and the system are healthy, and reaches Feedback, Findings, Research, Participants, Operations, or Releases in at most two clicks — all reading the same live operational truth.

---

## Document Control

| Field | Value |
|---|---|
| Owner | Product Operations Programme (POP) |
| Classification | Architecture specification |
| Code changes in this milestone | **None** |
| Next | POP Sprint 1 implementation against this IA (with POP-001 IAHF backlog) |

### Implementation status (as-built — Version1-RC2)

This document remains the **authoritative IA specification**. Target navigation was implemented primarily by **IAHF-003** (Founder Command Centre) with follow-on V1SP work:

| Spec intent | Live as of RC2 |
|---|---|
| One Founder door (`/founder`) | **Met** — sidebar → Overview |
| Live Product Check-in SoT | **Met** — Command Centre services |
| Legacy `/research/founder*` redirects | **Met** |
| Primary nav including Operational Health + Vision Journal | **Met** (V1SP-001C / V1SP-001D) — label is **Operational Health** (not “Operational Insights”) |
| Feedback as triage inbox | **Mostly met** (V1SP-001B declutter; density refinements in V1SP-001E) |
| Founder post-login landing on Overview | **Not met** — all users still land on student Dashboard (accepted Alpha deferral) |

Treat **§ Current Architecture** and **Appendix A** below as the **pre–IAHF-003** audit baseline (POP-001 era). Do not brief operators from those sections as live topology — use `knowledge/releases/IAHF-003_IMPLEMENTATION_REPORT.md` and V1SP Founder reports for as-built routes.

---

## Appendix A — Pre–IAHF-003 Founder route inventory (historical)

| Method | Path | Role (at POP-002 design time) |
|---|---|---|
| GET | `/founder` | FOS Dashboard |
| GET/POST | `/research/founder` | Research Command Centre |
| GET/POST | `/research/founder/finding/<id>` | Finding detail |
| GET/POST | `/research/founder/review/<id>` | Review form |
| POST | `/research/founder/award-founders-circle/<user_id>` | Award badge |
| GET/POST | `/research/checkin` | Student Product Check-in |
| GET | `/research/thank-you` | Post check-in |
| GET | `/research/dismiss` | Skip check-in |

## Appendix B — Principle traceability

| Design principle (milestone) | Where satisfied |
|---|---|
| ONE Founder entry point | Navigation Principles §1; Proposed hierarchy |
| ONE operational source of truth | Operational Principles §2; Internal Alpha module |
| Workflows over entities | Hierarchy; Workflow Analysis |
| ≤2 clicks | Navigation Map; two-click budget |
