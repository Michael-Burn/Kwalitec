# UX-003 — Premium Settings Redesign Report

**Programme:** Premium Product Experience  
**Status:** Complete  
**Date:** 2026-07-29  
**Scope:** Redesign the canonical Student Settings surface (`/student/profile`) into a compact, high-density configuration hub. Nested product Settings tabs (`/settings/preferences`, `/settings/data`, …) remain reachable via card actions; their internal layouts were not rewritten in this milestone.  
**Related:** UX-004 (IA audit — review-only; KPI relocation remains a later phase)

---

## Summary

Settings previously stacked oversized single-column cards (examination hero, preference summary, goal bars, statistics panel, account summary, primary CTA). UX-003 replaces that stack with a Linear/Stripe-style hub: a compact six-cell KPI overview, a responsive two-column configuration layout, and grouped **Profile · Learning · Notifications · Account · Security** sections built from compact information cards and interactive rows (dropdown, appearance selector, action buttons). Decorative goal progress bars were removed to raise density. Application learning engines and schema were untouched.

---

## Design rationale

| Principle | Application |
|-----------|-------------|
| Configuration first | Groups answer “how does Kwalitec behave for me?”; KPIs are a quiet overview with a **View progress → History** escape hatch (UX-004 Phase 1 alignment without full KPI removal yet). |
| Density over decoration | Large padded cards → compact KPI cells and info cards (icon, title, value, description, action). |
| Interactive where real | Daily study goal posts to existing `settings.update_preferences`; appearance uses the shared switcher; reminder/notification states deep-link rather than fake non-persisted toggles. |
| Premium without noise | No new animations; existing brand tokens (`student.css` / brand blue); uppercase group labels; quiet borders. |
| Hierarchy | Group titles are small caps; primary values are the loudest text; actions are text/button links, not full-width CTAs. |

---

## Before vs after

| Aspect | Before | After |
|--------|--------|-------|
| Layout | Single-column stack of `student-card` blocks | KPI strip + two-column `settings-columns` (≥800px) |
| Examination | Hero card with large title | KPI cell + Profile info card with **Manage → Choose Exam** |
| Statistics | Large “Progress summary” meta-row | Six-cell compact KPI grid |
| Preferences | Read-only definition list | Learning panel: goal dropdown + Save, Adjust links, appearance selector |
| Account | Static meta-row + full-width “Open account settings” | Compact cards linking to Profile / Data / Check-in |
| Goals | Progress-bar articles when present | Removed (non-editable analytics — matches UX-004 Phase 3 intent) |
| Width | Reading width (`44rem`) | Workspace width for the Settings hub |
| Page copy | “Examination, preferences, goals, and account.” | “Configure how Kwalitec works for you.” |

---

## Components changed

| Component | Role |
|-----------|------|
| `settings-hub` | Page root |
| `settings-kpi` / `settings-kpi-grid` / `settings-kpi-item` | Compact overview metrics |
| `settings-columns` / `settings-column` | Responsive two-column IA |
| `settings-group` / `settings-group-title` | Section chrome |
| `settings-panel` / `settings-row` | Interactive preference rows |
| `settings-info-card` | Compact card (icon · title · value · description · action) |
| `settings-select` / `settings-appearance` | Controls |
| Shared `appearance_switcher` | Embedded in Learning (browser-persisted) |
| Icon set (`clock`, `sessions`, `topics`, `streak`, `bell`, `shield`, `mail`, `exam`, `chevron-right`) | KPI / card glyphs via `partials/icons.html` |

### KPI grid (after)

1. Study Time  
2. Sessions  
3. Topics Mastered  
4. Current Streak  
5. Average Daily Study (streak-window only; otherwise `—`)  
6. Current Examination  

---

## Screens affected

| Screen | Route | Change |
|--------|-------|--------|
| **Student Settings (canonical)** | `GET /student/profile` | Full redesign |
| Product Settings → Preferences | `GET/POST /settings/preferences` | Unchanged UI; daily goal Save from hub POSTs here |
| Product Settings → Profile / Data / Account Status / Check-in | `/settings/*` | Unchanged; linked from hub cards |
| Choose Exam | `study_plan.index` | Linked from Examination **Manage** |
| History | `student.history` | Linked from Overview **View progress** |
| Founder Console Settings | `/founder/.../settings` | Out of scope |

---

## Responsive behaviour

| Breakpoint | Behaviour |
|------------|-----------|
| &lt; 480px | Info-card action wraps under body; KPI value slightly smaller |
| ≥ 480px default | Two-column KPI grid |
| ≥ 640px | Three-column KPI grid |
| ≥ 800px | Two-column settings groups (Profile/Learning \| Notifications/Account/Security) |
| ≥ 960px | Six-column KPI strip (one cell per metric) |
| Settings hub | `student-main--workspace` so columns use shell width |

Touch targets: row buttons and appearance options retain usable padding; no hover-only critical actions.

---

## Accessibility review

| Check | Result |
|-------|--------|
| Landmarks / headings | `aria-label` on hub; `h2` group titles; `h3` card titles |
| KPI list | `role="list"` / `listitem` on KPI cells |
| Appearance | Existing `role="group"` + per-button `aria-label` / `aria-pressed` |
| Daily goal | `<label for="daily_goal_hours">` + named `<select>` |
| Notification status | `role="status"` with accessible label on account notifications state |
| Focus | `:focus-visible` rings on links, select, appearance options |
| Motion | No new animations; existing `prefers-reduced-motion` rules preserved |
| Colour | Status chips use border + text, not colour alone |
| Disabled future control | Password & sessions uses `aria-disabled` muted “Soon” (not a fake button) |

---

## Performance impact

| Concern | Assessment |
|---------|------------|
| Payload | Template HTML smaller (fewer large cards / no goal loop). CSS added once to `student.css` (~4 KB uncompressed). |
| Icons | Inline SVG via existing macro — no new network requests. |
| JS | No new scripts; appearance still uses `theme.js`. |
| Server | Presentation-only average/streak labels in `profile_vm`; no extra service/DB calls. |
| Runtime | Negligible. |

---

## Relation to UX-004

UX-004 recommends removing learning KPIs from Settings entirely. UX-003 ships a **compact** KPI overview (mission requirement) plus History deep-link, and stops presenting goals as decorative progress. Full KPI subtraction (UX-004 Phase 1) remains a follow-up once product accepts History as the sole stats home.

---

## Architecture compliance

| Concern | Assessment |
|---------|------------|
| Layering | Templates + presentation view-model labels only; no blueprint business math; preferences Save reuses existing settings route |
| Curriculum V1/V2 | N/A — no traversal or import changes |
| Examination identity | Still resolved via `_authoritative_examination_label` (B2 preserved) |
| Sole runtime | `/settings/` → profile redirect unchanged; hub remains canonical Settings |

---

## Migration impact

**None.** No Alembic or schema changes.

---

## Technical debt

| Debt | Note |
|------|------|
| Dual Settings shells | Hub deep-links nested `/settings/*`; Phase 4 consolidation (UX-004) still open |
| Reminder toggle not in-place | Reminder state is Twin-projected; hub uses Manage / Turn on|off → Preferences rather than inventing persistence |
| Average Daily Study | Honest only inside current streak window; blank otherwise — needs study-day evidence for a lifetime daily average |
| Password & sessions | Placeholder “Soon” card until security controls ship |
| Product Settings tabs | Still use older panel density; not restyled in UX-003 |

---

## Known limitations

- Nested product Settings pages were not redesigned.  
- No true boolean toggle persistence for reminders/notifications on this page.  
- KPIs remain on Settings pending UX-004 Phase 1 product decision.  
- Founder Console Settings out of scope.

---

## Student Impact Assessment

N/A for full EP/P template — UX-003 is a Premium Product Experience presentation programme. Student-facing effect: faster scanning of account/learning configuration, less scroll, clearer paths to change exam, appearance, data, and preferences without changing learning algorithms.

---

## Estimated KSI contribution

**ΔKSI = 0** (presentation / IA density; no validated K1–K8 evidence package in this milestone).

---

## CRI domains improved

| Domain | Effect |
|--------|--------|
| CR5 Product polish / trust surface | Provisional — Settings reads as a configuration centre rather than a card dump |
| Other CR1–CR9 | None claimed |

**Estimated CRI delta:** provisional **+1** on polish only; not validated; board not updated.

---

## Evidence collected

- `tests/presentation/student/test_templates.py` — hub groups, KPI labels, interactive controls  
- `tests/presentation/student/test_view_models.py` — streak / average daily / session labels  
- Manual structure review against Linear/Stripe density patterns  

---

## Files created

- `knowledge/product/ux003_settings_redesign/UX003_SETTINGS_REDESIGN_REPORT.md`

## Files modified

- `app/templates/student/profile.html` — Settings hub redesign  
- `app/static/css/student/student.css` — Settings hub styles  
- `app/templates/partials/icons.html` — KPI/card icons  
- `app/presentation/student/view_models.py` — KPI/setting labels + page description  
- `app/presentation/student/educational_view_models.py` — page description  
- `app/presentation/student/views.py` — page description  
- `tests/presentation/student/test_templates.py` — hub assertions  
- `tests/presentation/student/test_view_models.py` — label coverage  

## Tests executed

```bash
python3 -m pytest tests/presentation/student/test_templates.py \
  tests/presentation/student/test_view_models.py \
  tests/presentation/student/test_routes.py::test_profile_shows_examination -q
```

**Outcome:** 84 passed.

## Commit

- Not requested / not created for this milestone
