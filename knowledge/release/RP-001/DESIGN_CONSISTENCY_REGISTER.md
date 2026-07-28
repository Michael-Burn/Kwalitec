# RP-001.4 — Design Consistency Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.4 — Premium Experience Certification  
**Date:** 2026-07-28  
**Status:** Certified register (documentation only)  
**Companion:** `PREMIUM_EXPERIENCE_AUDIT.md`

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
| Hardcoded / Bootstrap defaults | V1 content often uses Bootstrap utility classes and `.card` defaults | **Inconsistent** vs EOS panels |
| Duplicate token aliases | `--color-*` legacy aliases coexist with semantic tokens — workable but noisy | **Acceptable residual** |

**Verdict:** **Conditional** — one token source exists; application is uneven.

---

### DC-02 — Component usage

| Component family | EOS student / session | V1 / Bootstrap pages | Status |
|------------------|----------------------|----------------------|--------|
| Page header | `student-page-header` / `session-page-header` | `section-header` | **Divergent** |
| Cards / panels | `student-panel`, `student-card`, `session-card` | Bootstrap `.card` | **Divergent** |
| Primary button | `student-btn-primary` / `session-btn-primary` | `btn btn-primary` | **Divergent styling path** |
| Empty state | `student-empty` | `educational_empty` macro | **Divergent** |
| Skeleton | `skeleton.html` macros | Rarely used outside session overview | **Under-used** |
| Flash / toast | Bootstrap `alert` | Same | **Consistent** (generic) |
| Icons | Inline Lucide-weight SVG; `partials/icons.html` in settings | Mixed | **Mostly consistent stroke language** |
| Modals | `confirm_modal` on EOS | Welcome modal shared | **Partial** |
| Appearance | Public switcher on auth; Settings preferences on app | Split placement | **Acceptable** |

**Verdict:** **Inconsistent** across EOS vs V1 content patterns.

---

### DC-03 — Visual hierarchy

| Surface group | Hierarchy quality | Notes |
|---------------|-------------------|-------|
| Login | Strong | Brand left, action right |
| Session | Strong | One objective, one CTA |
| Journal / Timeline | Strong | Timeline → entry → provenance |
| Home hero | Strong locally | Eyebrow → title → why → CTA |
| Home full page | Weakened | Secondary + tertiary compete with hero |
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
| `layouts/base` → EOS under sole runtime | Onboarding, Help, Settings, Study Plan wizard | **EOS chrome + V1 content language** |

This last row is the primary **design consistency fracture** for Alpha (maps to JR-02 / R-02 / XR-01).

---

## Consistency scorecard

| Dimension | Score | Notes |
|-----------|-------|-------|
| Design language | Conditional | Tokens shared; Bootstrap/V1 diverge |
| Component usage | Fail (cross-system) | Two component families in one product |
| Visual hierarchy | Conditional | Cores strong; Home density |
| Educational emphasis | Conditional | Strong on ILE surfaces |
| Brand presentation | Pass | Lockup + navy chrome |
| Interaction patterns | Conditional | Disclosure good; shell switches |

**Overall design consistency: Conditional Pass** — not one visual system end-to-end; coherent enough for Alpha if dual chrome remains disclosed.

---

## Required before unconditional Pass

1. Unify page header, panel/card, button, and empty-state primitives on student-facing V1 content pages **or** fully migrate those pages to EOS components.  
2. Reduce Home to one primary educational composition (hero ± one intelligence panel).  
3. Adopt one empty + one loading + one success pattern on all student routes.  
4. Mobile: compact navigation that does not wrap into a second visual band.
