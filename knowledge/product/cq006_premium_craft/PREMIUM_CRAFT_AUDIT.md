# CQ-006 — Premium Craft Audit

**Programme:** CQ-006 — Premium Craft  
**Date:** 2026-07-28  
**Scope:** Founder-facing Version 1 surfaces (Home → Session → Quick Check → History/Journey → Auth entry)  
**Constraint:** Identify unfinished craft only — no redesign, no new capability

---

## Method

Code-level review of templates and CSS for Home, Session, Adaptive Assessment / Quick Check, History, Journey, Auth, shared tokens/partials. Findings cite existing class hooks and stylesheet boundaries.

**Overall maturity:** Low–Emerging. Tokens, calm shells, and primary-button motion exist, but templates often outpace CSS, and shared component styles live in the wrong stylesheet for the EOS shell.

---

## Critical

| ID | Surface | Evidence | Issue |
|---|---|---|---|
| A01 | Home / first session | `welcome_modal.html` + `app.css` welcome rules; `student/base.html` blocks `app.css` | Welcome modal backdrop/card/outline button unstyled on EOS |
| A02 | Session Overview / QC | `session-btn-secondary` in `assessment.css` only; overview/QC load `quick_check.css` / `session.css` | Secondary CTAs render as browser-default |
| A03 | Home readiness | `ctx-learn-more*` styled only in `app.css` | “Why this estimate?” disclosure looks like raw `<details>` |

---

## Major

| ID | Surface | Evidence | Issue |
|---|---|---|---|
| A04 | Home hero | `.student-hero-purpose { margin: 0 }`; no `.student-session-next` rules | Why / Next / benefit stack with collapsed rhythm |
| A05 | Home commitment | Commitment / defer / coach-trust classes unused in CSS | Defer radios and trust lists look like raw HTML |
| A06 | Home shell | `student/base.html` page_header + hero `h2` | Double title hierarchy (“Today”/“Home” + mission title) |
| A07 | Journey | `.student-card--current`, `.student-journey-map` unstyled | Current topic has no “you are here” emphasis |
| A08 | Auth flashes | Success class `.student-success` without student CSS on auth | Login success flash unstyled (auth uses `app.css`) |

---

## Medium

| ID | Surface | Evidence | Issue |
|---|---|---|---|
| A09 | Home | Standalone “Study Sensei” muted line + “Today’s Mission” eyebrow | Narrator hierarchy unclear |
| A10 | Home Journey feedback | Eyebrow and `h2` both “Your Journey” | Duplicate copy |
| A11 | History | Secondary buttons inline without gap; narrative list unstyled | Awkward wrap / flat list |
| A12 | Eyebrows | 4+ eyebrow class variants (0.72–0.8rem) | Inconsistent caption scale |
| A13 | Secondary panels | `opacity: 0.92` on subordinate block | Feels faded/disabled |
| A14 | Session | Inline `session-eyebrow` inside body text; unstyled support / reflection framing | Label and callout polish gaps |
| A15 | Nav | `data-nav-pending` with no CSS | No optimistic navigation feedback |
| A16 | JS | `enhancePrimaryCta` demotes to Bootstrap `btn-outline-secondary` | Second primary looks non-EOS |

---

## Low (noted; selective fix)

| ID | Issue |
|---|---|
| A17 | Logo max-height 2.75rem vs 2.5rem across shells |
| A18 | Primary hover lift −1px vs −2px |
| A19 | Complete vs Summary bridge copy drift |
| A20 | Broken `<meta>` typo on student assessment base |
| A21 | Appearance switcher on auth only |

---

## Patterns

1. **Stylesheet silos** — EOS omits `app.css`; QC omits `assessment.css`; templates still depend on those classes.  
2. **Template ahead of CSS** — Home commitment / next / coach hooks never styled.  
3. **Button class proliferation** — `student-btn-*`, `session-btn-*`, Bootstrap `btn-*` without shared motion.  
4. **Empty-state dual systems** — centred `app.css` vs left dashed EOS; macros underused.

---

## Out of scope (explicit)

- Redesign of layout or visual language  
- Recommendation / Twin / readiness algorithms  
- New educational capability or Version 2 surfaces  
- CR9 commercial envelope  

---

**End of Premium Craft Audit**
