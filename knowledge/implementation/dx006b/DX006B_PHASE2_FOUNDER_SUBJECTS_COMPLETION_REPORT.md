# DX-006B Phase 2 — Founder Subjects Completion Report

**Programme:** DX-006B — Founder & Student Surface Migration  
**Phase:** 2 — Founder Subjects  
**Authority:** DX-004B Catalogue First  
**Status:** Implementation complete — awaiting independent review  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01`  
**Design freeze tag:** `v2.0.0-design-freeze`  
**Foundation Gate:** CERTIFIED  
**Phase 1:** CERTIFIED (per programme authority for this phase)

---

## Executive Summary

Legacy Founder Subjects hub (`hub.html` tutorial / dual Create–Open cards / workspace list mashup) was **replaced** with the DX-004B catalogue-first architecture: one H1 **Subjects**, L1 Search + Status/Sort filters via shared macros, L0 professional table/list catalogue, and exactly one Primary **Create Subject**. Legacy Review / Publishing / Versions / Quality hub pages redirect to Subjects filter presets. Curriculum Studio is demoted to a workspace execution index (no KPI strip, no competing Create Subject catalogue). Presentation only — publication logic, models, and permissions unchanged.

**Recommendation: GO WITH CONDITIONS** — ready for independent Phase 2 review. Do not start Phase 3 until certified.

---

## Architecture Implemented

| Layer | Implementation |
|---|---|
| **L0** | Subject catalogue — `ds_subject_catalogue` table (desktop) / stacked list (narrow) |
| **L1** | Search (`ds_search_input`) + Status + Sort (`ds_select`) in `ds_toolbar` |
| **L2** | Quiet row metadata: stage, updated, publication status (+ optional code) |
| **L3** | Console shell nav only — no in-page hub tabs / breadcrumbs on Subjects |
| **Primary** | Exactly one: **Create Subject** (header when populated; empty-region when empty; form submit when `?create=1`) |

One question answered: **Which subject do I want to work on?**

Open → Workspace immediately (row link). Create → create form → subject + workspace → Workspace.

---

## Legacy Removed

Deleted / redirected (not CSS-hidden):

- `hub.html` Subjects / Review / Publishing / Versions / Quality landing mashup  
- Curriculum workflow 7-step tutorial essay  
- Dual Primary cards (Create Subject + Open Workspace)  
- “Open Curriculum Studio” CTA on Subjects  
- Hub KPI / readiness decoration on Subjects path  
- Studio dashboard KPI metric cards (Published / Drafts / Pending…)  
- Studio Create Subject / Open Workspace peer forms (catalogue belongs on Subjects)  
- Secondary nav entries for Review Queue / Publishing / Versions / Quality as peer catalogues  
- Settings links to hub pages → Subjects filter presets  

---

## Shared Components Used

| Component | Source |
|---|---|
| Page header + Primary strip | `ds_page_header` / `ds_primary_action_strip` |
| Search | `ds_search_input` (SearchInput / SearchBar contract) |
| Status / Sort | `ds_select` |
| Toolbar | `ds_toolbar` |
| Catalogue table/list | `ds_subject_catalogue` (`DataTable` / `DataList` pattern) |
| Badge (status) | `ds_badge` |
| Empty operational | `ds_empty_operational` |
| Button | `ds_button` |

No page-specific primitives. Rejected KPI components unused.

---

## Foundation Imports

- Template: `{% from "design_system/macros.html" import … %}` only.  
- CSS: `design_system.css` already linked after `tokens.css` in `console_base.html`.  
- Python service is founder-local DTO projection; UI via Jinja macros.  
- **No** imports from `presentation.design_system.components.*` on the Subjects path.

---

## Files Modified

- `app/presentation/curriculum_studio/routes.py`  
- `app/templates/curriculum_studio/dashboard.html`  
- `app/templates/design_system/macros.html`  
- `app/static/css/design_system.css`  
- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/templates/founder_dashboard/settings.html`  
- `tests/presentation/curriculum_studio/test_navigation.py`  
- `tests/presentation/curriculum_studio/test_product_language.py`  
- `tests/presentation/workflows/test_workflow_founder_nav.py`  
- `tests/presentation/workflows/test_workflow_founder_studio.py`  
- `knowledge/implementation/dx006b/PHASE_TRACKER.md`  

## Files Created

- `app/founder/dashboard/dto/founder_subjects.py`  
- `app/founder/dashboard/services/founder_subjects_service.py`  
- `app/templates/curriculum_studio/subjects.html`  
- `tests/test_dx006b_founder_subjects.py`  
- `knowledge/implementation/dx006b/DX006B_PHASE2_FOUNDER_SUBJECTS_COMPLETION_REPORT.md`  

## Files Deleted

- `app/templates/curriculum_studio/hub.html`

---

## Behaviour Changes

| Change | Notes |
|---|---|
| Subjects body | Catalogue-first DTO replaces hub tutorial + dual forms |
| Search / filter / sort | Query params `q`, `status`, `sort`; URL presets supported |
| Create Subject | Primary → `?create=1` form; POST creates subject **and** opens workspace → Workspace |
| Legacy hubs | Routes retained; redirect to Subjects filters (routing preserved) |
| Studio index | Workspace list only; Create lives on Subjects |
| Unchanged | Permissions (`founder_required`), DB models, publication/validation services, API contracts |

---

## Accessibility Result

**PASS**

- Exactly one H1 (`Subjects`)  
- Search labelled; Status/Sort labelled selects  
- Catalogue rows are links with focus-visible styles  
- Status communicated as text (badge + label)  
- Empty / zero-result: Reason + Next Action  
- Touch targets via DS button min-height  

---

## Responsive Result

**PASS**

- Header Primary stacks full-width &lt;768px  
- Toolbar stacks; search/filters full width  
- Table → stacked list on narrow viewports  
- One Primary retained  

---

## Guardian Result

| Rule | Status |
|---|---|
| G-1 One Primary | PASS |
| G-2 One H1 | PASS |
| G-3 Token only (page body) | PASS |
| G-4 No hard-coded colours (page) | PASS |
| G-5 No duplicate spacing scale | PASS |
| G-6 No KPI | PASS |
| G-7 No decorative cards | PASS (table/list) |
| G-8 L0–L3 hierarchy | PASS |
| G-9 No decorative icons | PASS |
| G-10 No duplicate nav on page | PASS |
| G-11 Catalogue only | PASS |
| G-12 Rejected unused | PASS |

**Guardian: PASS**

---

## Regression Result

```text
PYTHONPATH=src:app python3 -m pytest \
  tests/test_dx006b_founder_subjects.py \
  tests/test_dx006b_founder_home.py \
  tests/presentation/curriculum_studio/test_navigation.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/presentation/workflows/test_workflow_founder_nav.py \
  tests/presentation/workflows/test_workflow_founder_studio.py \
  tests/education_os/presentation/design_system/test_foundation_gate.py \
  -q
→ 136 passed; 1 pre-existing unrelated failure
  (test_preview_next_action_mentions_version — copy drift outside Phase 2)
```

---

## Architectural Fidelity Score

```text
Surface: Founder Subjects
Phase: 2
Authority: DX-004B
Reviewer: Implementation agent (provisional)
Date: 2026-07-29
Release Candidate: RC-2026.07.29-01

Matches DX Architecture:   29 / 30
Shared Components:         20 / 20
Token Compliance:          14 / 15
Guardian Compliance:       15 / 15
Accessibility:             9 / 10
Performance:              10 / 10
─────────────────────────────────
TOTAL:                     97 / 100

Hard caps triggered?  No
Verdict:  PASS (≥95)
```

Minor deductions: Apply remains an explicit secondary submit (not pure live-filter); shell CSS still mixed legacy outside page body.

---

## Premium Score

### Mandatory checks

| Check | Result |
|---|---|
| One Primary action | PASS |
| KPI policy respected | PASS |
| Cards only for justified grouping | PASS (none on catalogue) |
| Empty state = Reason + Next Action only | PASS |
| Lucide only; Inter only | PASS |
| Semantic colour only; Gold not UI chrome | PASS |
| No implementation leakage in primary UI | PASS |
| Motion ≤250ms and purposeful | PASS |

### Dimensions

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | Visual Hierarchy | 9 | Catalogue dominates; tools quiet above |
| 2 | Typography | 9 | Page 24 / section 18 / body 16 / support 14 |
| 3 | Spacing | 9 | DS space scale on page body |
| 4 | Information Density | 10 | No KPI / tutorial chrome |
| 5 | Professional Tone | 9 | Operational vocabulary only |
| 6 | Minimalism | 10 | Search → filters → rows → Create |
| 7 | Accessibility | 9 | Labels, focus, one H1 |
| 8 | Consistency | 9 | Shared macros / foundation |
| 9 | Task Focus | 10 | Find or create only |
| 10 | Premium Feel | 9 | Calm table; no theatre |

**All dimensions ≥9:** YES  
**Surface extra (Phase 2 Catalogue only; object permanence):** PASS  

**Premium: CERTIFIED (provisional — confirm in independent review)**

---

## Known Issues

1. Live dogfood 3-second Founder validation pending independent reviewer.  
2. Workspace `created_at` not on snapshot DTO — “Recently created” sort uses activity stamp fallback.  
3. More (…) row menu deferred (Archive / Rename / History) — Alpha Open-only rows; DX-004B allows More as secondary.  
4. Pre-existing `test_preview_next_action_mentions_version` failure unrelated to Subjects.  
5. Curriculum Studio empty state offers Create Subject once (links to Subjects create) — intentional boundary hand-off, not a second Subjects catalogue.

---

## Technical Debt Introduced

**None** intended for Subjects path. Hub route redirects are compatibility shims until callers fully migrate to Subjects URLs.

---

## Migration Impact

**None** — no Alembic / schema changes.

---

## Architecture Compliance

- Presentation-only Subjects migration; curriculum V1/V2 untouched.  
- Layering: route → FounderSubjectsService → Studio/Authority read models → macros.  
- No educational algorithm changes.

---

## Recommendation

### GO WITH CONDITIONS

1. Independent Founder validation walkthrough against DX-004B (3-second test).  
2. Confirm Premium / Fidelity scores with a second reviewer.  
3. Mark Phase 2 **CERTIFIED** in `PHASE_TRACKER.md` only after that review.  
4. **Do not begin Phase 3 (Founder Workspace)** until Phase 2 is certified.

---

## Commit

Changes prepared only — **await explicit approval before commit**.

---

*Release Candidate: RC-2026.07.29-01*
