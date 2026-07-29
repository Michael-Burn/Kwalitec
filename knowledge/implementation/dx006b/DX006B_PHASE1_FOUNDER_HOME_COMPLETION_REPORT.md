# DX-006B Phase 1 — Founder Home Completion Report

**Programme:** DX-006B — Founder & Student Surface Migration  
**Phase:** 1 — Founder Home  
**Authority:** DX-004A Founder Operating System  
**Status:** Implementation complete — awaiting independent review  
**Date:** 2026-07-29  
**Release Candidate:** `RC-2026.07.29-01`  
**Design freeze tag:** `v2.0.0-design-freeze`  
**Foundation Gate:** CERTIFIED  

---

## Executive Summary

Legacy Founder Console Home (`overview.html` KPI / Quick Actions / Platform Summary chrome) was **replaced** with the DX-004A architecture: L0 Current Work + one Primary, L1 Publication Queue, L2 Recent Publications, and L3 shell navigation (≤6). The page composes only `presentation.design_system.foundation` contracts via `design_system/macros.html`, loads `design_system.css` after `tokens.css`, and no longer surfaces vanity metrics on Home.

**Recommendation: GO WITH CONDITIONS** — ready for independent Phase 1 review. Do not start Phase 2 until certified.

---

## Architecture Implemented

| Layer | Implementation |
|---|---|
| **L0** | `ds_current_work` — subject, stage, one Primary (Resume / Validate / Approve / Publish / Create Subject) |
| **Primary Action Strip** | Shared `ds_primary_action_strip` inside Current Work / empty state |
| **L1** | `ds_publication_queue` — attention-only rows (Ready → Approval → Validation → Incomplete) |
| **L2** | `ds_recent_publications` — ≤5 active published packages; section omitted when empty |
| **L3** | Console sidebar: Home · Subjects · Curriculum Studio · Students · Support · Settings |

One question answered: **What should I work on next?**

---

## Legacy Removed

From Home path (deleted, not CSS-hidden):

- Operational pulse essay / version eyebrow  
- Attention Required KPI grid  
- Platform Summary KPI cards  
- Quick Actions multi-CTA strip  
- Operational detail card mosaic (support / attention / Vision)  
- Competing “Review attention queue” Primary  
- Unused legacy `index.html` Founder Overview template  
- Home-only KPI grid CSS (`.console-attention-grid`, `.console-summary-grid`, `.console-detail-grid`, `.console-quick-actions`)

---

## Components Used

| Component | Source |
|---|---|
| Current Work | `ds_current_work` |
| Primary Action Strip | `ds_primary_action_strip` (via Current Work / empty) |
| Publication Queue | `ds_publication_queue` + `ds_queue_list` |
| Recent Publications | `ds_recent_publications` |
| Empty Operational State | `ds_empty_operational` |
| Button (ghost “View all”) | `ds_button` |
| Page / container classes | `ds-page`, `ds-container--content` |

No page-specific primitives. Rejected KPI components unused.

---

## Foundation Imports

- Python (service contracts only as needed): Home DTO is founder-local; UI via Jinja macros.  
- Template: `{% from "design_system/macros.html" import … %}` only.  
- CSS: `design_system.css` linked in `console_base.html` after `tokens.css`.  
- **No** imports from `presentation.design_system.components.*` or `layout.*` on the Home path.

---

## Files Modified

- `app/founder/dashboard/templates/founder_dashboard/overview.html`  
- `app/founder/dashboard/routes.py`  
- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/static/css/founder_dashboard.css`  
- `app/founder/dashboard/templates/founder_dashboard/settings.html`  
- `app/founder/dashboard/templates/founder_dashboard/operational_health.html`  
- `app/founder/dashboard/templates/founder_dashboard/evidence_gates.html`  
- `app/founder/dashboard/templates/founder_dashboard/founder_intelligence.html`  
- `app/templates/layouts/console_base.html`  
- `app/templates/design_system/macros.html`  
- `app/static/css/design_system.css`  
- `app/templates/curriculum_studio/hub.html`  
- `app/presentation/curriculum_studio/view_models.py`  
- `app/presentation/product_language.py`  
- `app/brand_identity.py`  
- `knowledge/design/dx003_decision_content/TERMINOLOGY_DICTIONARY.md`  
- Multiple regression tests under `tests/`  

## Files Created

- `app/founder/dashboard/dto/founder_home.py`  
- `app/founder/dashboard/services/founder_home_service.py`  
- `tests/test_dx006b_founder_home.py`  
- `knowledge/implementation/dx006b/DX006B_PHASE1_FOUNDER_HOME_COMPLETION_REPORT.md`  

## Files Deleted

- `app/founder/dashboard/templates/founder_dashboard/index.html` (unreferenced legacy Overview)

---

## Behavioural changes (explicit)

| Change | Notes |
|---|---|
| Home content model | Publication-centred DTO replaces `CommandCentreOverview` on `/console/` |
| Primary CTA | Publication Resume/Validate/Approve/Publish or Create Subject — not Attention Center |
| Primary nav | ≤6 items; Review/Publishing/Versions/Quality demoted to Settings + secondary |
| Active section | Nested ops map to `settings` for shell highlight |
| Labels | Overview / Console Home → **Home** |
| Unchanged | Routes, permissions (`founder_required`), services for Attention/Support/Ops, DB models, publication rules, API contracts |

`CommandCentreService.build_overview` retained for Attention / Participants / Operations consumers.

---

## Accessibility Result

**PASS**

- One H1 (`Home`)  
- Landmarks: `main` (shell) + page `article` with `aria-labelledby`  
- Primary has accessible name = label  
- Queue/recent rows are focusable links with focus-visible styles from DS  
- Status communicated as text labels (not colour alone)  
- Touch targets via DS button min-height tokens  

---

## Responsive Result

**PASS**

- Single column preserved  
- DS CSS stacks Primary full-width &lt;768px  
- Content container narrow/content width  

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
| G-7 No decorative cards | PASS |
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
  tests/test_dx006b_founder_home.py \
  tests/test_founder_dashboard.py \
  tests/test_console_001_kwalitec_console.py \
  tests/test_iahf003_founder_command_centre.py \
  tests/presentation/curriculum_studio/test_navigation.py \
  tests/presentation/workflows/test_workflow_founder_nav.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/presentation/curriculum_studio/test_view_models.py \
  tests/operational/test_alpha_smoke_founder.py \
  tests/presentation/workflows/test_workflow_consistency.py \
  tests/test_v1sp001c_operational_health.py::TestRegression \
  tests/test_px002_product_experience.py::TestFounderNavigation \
  tests/education_os/presentation/design_system/test_foundation_gate.py \
  -q
→ PASS (Phase 1 relevant suite; pre-existing unrelated failures elsewhere not introduced by this phase)
```

Support / Operations remain reachable via Support nav and Settings nesting.

---

## Architectural Fidelity Score

```text
Surface: Founder Home
Phase: 1
Authority: DX-004A
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

Minor deductions: Console shell/footer still carry legacy “attention today” wording; shell CSS remains mixed legacy (page body is DS/token compliant).

---

## Premium Score

### Mandatory checks

| Check | Result |
|---|---|
| One Primary action | PASS |
| KPI policy respected | PASS |
| Cards only for justified grouping | PASS |
| Empty state = Reason + Next Action only | PASS |
| Lucide only; Inter only | PASS |
| Semantic colour only; Gold not UI chrome | PASS |
| No implementation leakage in primary UI | PASS |
| Motion ≤250ms and purposeful | PASS |

### Dimensions

| # | Dimension | Score | Rationale |
|---:|---|---:|---|
| 1 | Visual Hierarchy | 9 | L0 dominates; queue/recent supporting |
| 2 | Typography | 9 | Page 24 / section 18 / body 16 / support 14 via tokens |
| 3 | Spacing | 9 | DS space scale on page body |
| 4 | Information Density | 10 | KPI/chrome removed |
| 5 | Professional Tone | 9 | Operational vocabulary only |
| 6 | Minimalism | 10 | Three sections max + shell |
| 7 | Accessibility | 9 | Landmarks, focus, one H1 |
| 8 | Consistency | 9 | Shared macros / foundation |
| 9 | Task Focus | 10 | Publication Continue only |
| 10 | Premium Feel | 9 | Calm list layout; no theatre |

**All dimensions ≥9:** YES  
**Surface extra (Phase 1 Current Work; no Platform Summary):** PASS  

**Premium: CERTIFIED (provisional — confirm in independent review)**

---

## Known Issues

1. Console footer still says “What needs attention today?” — shell residual; not Home body.  
2. Studio hub peers remain as routes (Settings links) until Phase 2/3 fully retires them as catalogues.  
3. Live dogfood 3-second Founder validation pending independent reviewer.  
4. `CommandCentreOverview` DTO retained for non-Home Console pages (intentional).

---

## Technical Debt Introduced

**None** intended for Home path. Temporary dual existence of legacy ops DTOs outside Home is pre-existing, not new Home debt.

---

## Migration Impact

**None** — no Alembic / schema changes.

---

## Architecture Compliance

- Presentation-only Home migration; curriculum V1/V2 untouched.  
- Layering preserved: route → FounderHomeService → Studio/Authority read models → macros.  
- No educational algorithm changes.

---

## Recommendation

### GO WITH CONDITIONS

1. Independent Founder validation walkthrough against DX-004A.  
2. Confirm Premium / Fidelity scores with a second reviewer.  
3. Mark Phase 1 **CERTIFIED** in `PHASE_TRACKER.md` only after that review.  
4. **Do not begin Phase 2 (Founder Subjects)** until Phase 1 is certified.

---

## Commit

Changes prepared only — **await explicit approval before commit**.

---

*Release Candidate: RC-2026.07.29-01*
