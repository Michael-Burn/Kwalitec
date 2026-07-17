# V1SP-001E — Information Architecture & Dashboard Simplification

**Programme:** Version 1 Stabilisation Programme (V1SP)  
**Milestone:** V1SP-001E  
**Status:** Implementation complete  
**Date:** 2026-07-17  
**Commit:** `0663f61` — `feat(ui): simplify information architecture and dashboard density (V1SP-001E)`  

---

## Summary

V1SP-001E reduces cognitive load across Kwalitec by simplifying page headers, consolidating duplicate workflow actions, and moving long instructional copy behind a consistent contextual help pattern (`ⓘ` tip + expandable Learn more).

Educational workflows, navigation destinations, and business logic are unchanged. Clarity improved; no redesign.

---

## Simplification Audit

| Surface | KEEP | MOVE TO HELP | REMOVE / DEMOTE |
|---|---|---|---|
| Student Dashboard | Session topic, progress %, Estimated Knowledge, next step | Honesty footnotes, recommendation explainability, revision intro depth | Duplicate recommendation “Start Study Session” button; repeated Create Plan CTAs in secondary empties |
| Study Session | Topic, metrics, success checklist, primary Start/Resume | Mode essays, claim blocks, activity disclaimer | Permanent multi-paragraph “why” wall |
| Analytics | Charts, KPIs | Per-chart honesty paragraphs → help tips | Permanent prose under every chart |
| Study Plan list/view | Plan cards, roadmap | — | Competing equal-weight action buttons on view; `display-6` header |
| Settings / Check-in | Section actions | Longer intros shortened | Multi-sentence permanent headers |
| Welcome modal | Primary Start Study Session | — | Two of three instructional paragraphs |
| Founder Overview | Metrics, alerts, queues | — | Verbose refresh metadata; generic Vision empties |
| Vision Journal | Search, entries, New entry primary | Long strategic-memory essay | Dual primary buttons in header row |
| Internal Alpha | Live metrics | Offline filesystem pipeline essay | Permanent operator paragraph |

No educational guidance was deleted — it remains available via help tip, Learn more, or existing honesty constants.

---

## Duplicate Actions Removed

| Location | Removed / demoted | Retained primary |
|---|---|---|
| Student Dashboard recommendation card | `btn-primary` launching `mission.missions` (often labelled Start Study Session / Continue Studying) | Today's Study Session CTA (`data-ptp004-cta="primary"`) |
| Dashboard secondary empties | Extra Create Study Plan buttons in Exam / Progress cards when onboarding card already owns that action | Onboarding “Create Study Plan” when no plan exists |
| Study Plan view | Equal-weight Edit / Set Active / Archive / Delete / All Plans / Dashboard buttons | **Edit** primary; Set Active secondary; Archive/Delete/All Plans/Dashboard tertiary |
| Vision Journal | New entry competing with Timeline as equal small primaries | **New entry** as page primary; Timeline secondary |

Workflow destinations unchanged — only presentation hierarchy.

---

## Progressive Disclosure

New shared partial: `app/templates/partials/contextual_help.html`

| Macro | Pattern | Accessibility |
|---|---|---|
| `help_tip(text, label)` | ⓘ button with `title` + visually hidden text | Keyboard focusable; `aria-label`; focus outline preserved |
| `learn_more(summary)` | Native `<details>` / `<summary>` | Expandable without JS; summary focusable |

Styles: `.ctx-help*`, `.ctx-learn-more*` in `app/static/css/app.css`.

---

## Dashboard Changes

### Student Dashboard

- One-line header description.
- Session card shows **Next step** first; rationale under Learn more.
- Recommendation explainability collapsed; no second primary CTA.
- Honesty / basis notes moved to help tips (strings retained for PTP-003).
- Empty states shortened and action-oriented.

### Founder Command Centre

- Overview description reduced to operational pulse metadata.
- Vision snapshot empty state points to New entry.
- Feedback / Internal Alpha / Vision Journal headers shortened.
- Offline pipeline detail behind Learn more.
- Vision Journal: single primary **New entry**; meaningful empty states.

---

## Microcopy Improvements

| Before | After |
|---|---|
| Long multi-clause page descriptions | One sentence |
| Review Today's Study Session | Review Session |
| Open Today's Study Session | Open Session |
| Study Session History | Session History |
| Edit Plan / All Study Plans / Back to Dashboard | Edit / All Plans / Dashboard |
| Dense Analytics honesty under each chart | Chart title + ⓘ tip |
| Welcome three-paragraph body | One sentence |

Preserved tested primary labels: **Start Study Session**, **Resume Study Session**, **Create Study Plan**.

---

## Accessibility

- Help triggers are `<button type="button">` with `aria-label` and visually hidden tip text.
- Focus-visible outline on help triggers and Learn more summaries.
- Learn more uses native disclosure (no custom JS modal).
- Colour contrast and brand tokens unchanged.
- Screen-reader honesty strings remain in the DOM via tip / details content.

---

## Tests

Automated:

```bash
python -m pytest tests/test_v1sp001e_information_architecture.py \
  tests/test_ptp004_information_architecture.py \
  tests/test_ptp003_honest_product_communication.py \
  tests/test_first_time_experience.py \
  tests/test_iahf004b_brand_experience.py \
  tests/test_lxp002_study_session_experience.py -q
```

Coverage includes help partial presence, duplicate CTA removal, honesty string retention, Founder header simplification, Study Plan header hierarchy, and runtime single primary CTA.

Manual review surfaces: Student Dashboard, Study Session, Analytics, Study Plan, Settings, Product Check-in, Founder Overview / Feedback / Vision Journal / Internal Alpha, Login chrome (unchanged nav).

---

## Known Limitations

- Legacy Founder `index.html` / dense Operations heritage layout not redesigned (out of scope; Overview remains the live home).
- Feedback inbox still carries Research-era summary blocks (density reduced at header only; deeper Feedback IA is deferred).
- Native `title` tooltips are limited on touch devices; Learn more remains the primary long-form path.
- Welcome modal still offers Start Study Session (intentional first-run path; not a Dashboard duplicate once dismissed).

---

## Architecture Compliance

- Layering preserved: templates/CSS only; no educational maths, Twin, Decision, or curriculum engine changes.
- Navigation endpoints unchanged (PTP-004 / IAHF-004B).
- Curriculum V1/V2 traversal unaffected.
- Migration impact: **None**.

---

## Files Created

- `app/templates/partials/contextual_help.html`
- `tests/test_v1sp001e_information_architecture.py`
- `knowledge/releases/V1SP-001E_INFORMATION_ARCHITECTURE_SIMPLIFICATION.md`

## Files Modified

- `app/static/css/app.css`
- `app/templates/dashboard/index.html`
- `app/templates/mission/index.html`
- `app/templates/analytics/index.html`
- `app/templates/study_plan/list.html`
- `app/templates/study_plan/view.html`
- `app/templates/settings/index.html`
- `app/templates/research/checkin.html`
- `app/templates/partials/welcome_modal.html`
- `app/founder/dashboard/templates/founder_dashboard/overview.html`
- `app/founder/dashboard/templates/founder_dashboard/feedback.html`
- `app/founder/dashboard/templates/founder_dashboard/vision_journal.html`
- `app/founder/dashboard/templates/founder_dashboard/internal_alpha.html`
- `tests/test_first_time_experience.py`

---

## Technical Debt

None introduced beyond documented Known Limitations. Optional follow-up: further Feedback inbox density reduction without changing review workflows.

---

*End of V1SP-001E Information Architecture Simplification report.*
