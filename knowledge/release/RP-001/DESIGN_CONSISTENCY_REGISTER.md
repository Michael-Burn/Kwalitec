# RP-001.4 — Design Consistency Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.4 — Premium Experience Certification  
**Date:** 2026-07-28  
**Status:** Certified register · **Verified post-RR-001.2 (2026-07-28)**  
**Companion:** `PREMIUM_EXPERIENCE_AUDIT.md`  
**Remediation:** `knowledge/release/RR-001/RR001_2_COMPLETION_REPORT.md`

---

## Purpose

Record whether Alpha presents **one design language** across shells, components, hierarchy, educational emphasis, brand, and interaction patterns.

---

## Consistency dimensions

### DC-01 — Design language (tokens & type)

| Aspect | Finding | Status |
|--------|---------|--------|
| Shared tokens | `tokens.css` + `brand.css` loaded on auth, EOS student, session | **Consistent** |
| Typeface | Self-hosted Inter via `fonts.css` across shells | **Consistent** |
| Spacing grid | 8-point tokens; student/session alias them | **Consistent** on EOS |
| Colour hierarchy | Navy chrome, blue primary, muted text, gold reserved | **Consistent** on EOS/auth brand panel |
| Hardcoded / Bootstrap defaults | Workspace pages (Help/Onboarding/Settings/Wizard) now use EOS header/panel/button primitives (RR-001.2); residual Bootstrap utilities remain inside panels | **Mostly consistent** (post-RR-001.2) |
| Duplicate token aliases | `--color-*` legacy aliases coexist with semantic tokens — workable but noisy | **Acceptable residual** |

**Verdict:** **Conditional → Improved (RR-001.2)** — one token source; workspace student pages now share EOS primitives; residual Bootstrap utilities inside panels remain acceptable Alpha debt.

---

### DC-02 — Component usage

| Component family | EOS student / session | V1 / Bootstrap pages | Status |
|------------------|----------------------|----------------------|--------|
| Page header | `student-page-header` / `session-page-header` | Help / Onboarding / Settings / Wizard now use `student-page-header` (RR-001.2) | **Aligned** |
| Cards / panels | `student-panel`, `student-card`, `session-card` | Settings/Help/Onboarding/Wizard use `student-panel` (RR-001.2) | **Aligned** |
| Primary button | `student-btn-primary` / `session-btn-primary` | Workspace CTAs use `student-btn-primary` / `student-btn-secondary` | **Aligned** |
| Empty state | `student-empty` | `educational_empty` macro now emits `student-empty` (XR-17) | **Aligned** |
| Skeleton | `skeleton.html` macros | Rarely used outside session overview | **Under-used** |
| Flash / toast | Bootstrap `alert` | Same | **Consistent** (generic) |
| Icons | Inline Lucide-weight SVG; `partials/icons.html` in settings | Mixed | **Mostly consistent stroke language** |
| Modals | `confirm_modal` on EOS | Welcome modal shared | **Partial** |
| Appearance | Public switcher on auth; Settings preferences on app | Split placement | **Acceptable** |

**Verdict:** **Conditional → Improved (RR-001.2)** — student-facing workspace pages share EOS component family; Bootstrap remains for grid/forms only.

---

### DC-03 — Visual hierarchy

| Surface group | Hierarchy quality | Notes |
|---------------|-------------------|-------|
| Login | Strong | Brand left, action right |
| Session | Strong | One objective, one CTA |
| Journal / Timeline | Strong | Timeline → entry → provenance |
| Home hero | Strong locally | Eyebrow → title → why → CTA |
| Home full page | Improved (RR-001.2) | Hero primary; MI disclosed; secondary subordinate; tertiary disclosed |
| Settings / Help | Medium | Section titles; card grids |
| Wizard | Strong within flow | Step indicator + question |

**Verdict:** **Conditional** — hierarchy rules exist; Home full composition and dual chrome break them.

---

### DC-04 — Educational emphasis

| Pattern | Where strong | Where weak |
|---------|--------------|------------|
| Why / Why now / Next / Benefit labels | Home MES, MI, Coach | Help/onboarding use product vocabulary |
| Evidence + uncertainty | MI, Journal provenance, Timeline certainty | Settings/Help non-educational |
| One focus per moment | Session shell | Home multi-panel |
| No gamification chrome | Student/session CSS briefs | Holds across Alpha student path |

**Verdict:** **Conditional** — educational emphasis is clear on learning cores; diluted by chrome density and product surfaces.

---

### DC-05 — Brand presentation

| Element | Status | Evidence |
|---------|--------|----------|
| Logo lockup rules | **Consistent** | `brand.css` `.brand-logo*`; used in auth, student, session |
| Wordmark discipline | **Consistent** | Login avoids repeating product name under logo |
| Topbar navy | **Consistent** | Student + session |
| Footer line | **Split** | Student: “Reduce decisions…”; Session: “One objective…”; Auth: `app_footer` |
| Alpha identity badge | **Present** | Login; Internal Alpha settings |
| Gold usage | **Mostly disciplined** | Achievement/identity accents; login feature icons use soft gold |

**Verdict:** **Pass with residuals** — brand mark is coherent; footer microcopy and dual chrome dilute “one product room.”

---

### DC-06 — Interaction patterns

| Pattern | Consistency | Notes |
|---------|-------------|-------|
| Primary action | One CTA emphasis on Session; Home usually one primary | Good on cores |
| Progressive disclosure | `<details>` for defer, MI explain, readiness learn-more, diagnostics | Recurring pattern — good |
| Commitment / defer | Home-specific | Clear when present |
| Navigation active state | EOS `aria-current` | Good |
| Form validation | WTForms + alert/form-text | Adequate |
| Destructive / confirm | Confirm modal on EOS | Not universal |
| Fake affordances | Reflection preview remidiated (RR-001.1) | Residual: option chips look choice-like |
| Shell transition | EOS ↔ auth error pages; EOS content ↔ V1 card pages | Friction |

**Verdict:** **Conditional**.

---

## Shell map (Alpha student path)

| Shell | Typical surfaces | Design feel |
|-------|------------------|-------------|
| `auth_base` | Login, errors | Brand marketing + form |
| `eos_student` | Home, History, Journal, Timeline, Journey, Revision, Profile | Reading calm, navy topbar |
| `session` | Overview → activity → reflection → summary | Focus room |
| `layouts/base` → EOS under sole runtime | Onboarding, Help, Settings, Study Plan wizard | **EOS chrome + EOS content primitives** (RR-001.2); residual Bootstrap utilities only |

Primary fracture from RP-001.4 (EOS chrome + V1 card language) is **remidiated for Alpha student-facing workspace pages** (XR-01). Remaining dual-chrome risk is Low residual utility styling, not a second component language.

---

## Consistency scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Design language | Conditional → Stronger | Tokens shared; workspace primitives aligned (RR-001.2) |
| Component usage | Conditional → Pass (student path) | EOS panels/headers/buttons on workspace pages |
| Visual hierarchy | Conditional → Stronger | Home density remidiated (XR-02) |
| Educational emphasis | Conditional | Strong on ILE surfaces; Home quieter |
| Brand presentation | Pass | Lockup + navy chrome |
| Interaction patterns | Conditional → Stronger | Disclosure + compact mobile nav |

**Overall design consistency (post-RR-001.2 verification): Conditional Pass → trending Pass on student Alpha path** — dual component language no longer the primary fracture; cohort validation (XR-20) still required for unconditional premium Pass.

---

## Required before unconditional Pass

1. ~~Unify page header, panel/card, button, and empty-state primitives on student-facing V1 content pages~~ **Done (RR-001.2)** — residual utility cleanup optional.  
2. ~~Reduce Home to one primary educational composition~~ **Done (RR-001.2)** — MI/tertiary disclosed; secondary subordinate.  
3. ~~Adopt one empty + one success pattern on student routes~~ **Done (RR-001.2)** for empty + success; skeleton adoption remains sparse (XR-06).  
4. ~~Mobile: compact navigation that does not wrap into a second visual band~~ **Done (RR-001.2)**.  
5. **Still required:** Internal Alpha cohort UX validation (XR-20) before claiming student-proven premium quality.
