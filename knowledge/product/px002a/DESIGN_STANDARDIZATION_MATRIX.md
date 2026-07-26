# PX-002A — Design Standardization Matrix

**Programme:** PX-002A — Trust & Friction Resolution
**Purpose:** Screen-by-screen before/after record of every visible change made under this programme, so a reviewer can verify scope discipline (no visual redesign, no unrequested polish) against `knowledge/product/px001/SCREEN_BY_SCREEN_REVIEW.md`.

Every row is a **behaviour/copy/structure** change, not a colour, spacing, or typography restyle, unless explicitly noted (T2-7's colour token fix is the one exception, and it corrects an off-brand deviation rather than introducing a new style).

---

| Screen | Before | After | Backlog item |
|---|---|---|---|
| Student Home (`student/home.html`) | Nav label "Dashboard"; Coach panel always repeats Mission card's Why/Why now/Next/Benefit; reflection preview rendered as styled buttons with `role="status"`; empty state used rejected synonym "study session" | Nav label "Home"; Coach panel shows commitment status or a pointer when the Mission card already carries the explanation, full list only when Mission card doesn't; reflection preview is plain, correctly-semantic text; empty state copy compliant with approved terminology | T1-1, T1-3 (a11y), T2-8 |
| Student History (`student/history.html`, nav) | Nav label "Analytics" (canonical), colliding conceptually with legacy Analytics | Nav label "History" | T1-1 |
| Sidebar (`partials/sidebar.html`) | "Dashboard" / "Analytics" pills in the canonical tree | "Home" / "History" pills | T1-1 |
| Reflection card (`session/components/reflection_card.html`) | No explanation of purpose or downstream use | One sentence of value framing at the point of use | T1-3 |
| Session Overview / Mission-adjacent duration copy | Independently-built duration strings, no shared rounding rule | All routed through `app/presentation/formatting.py` | T1-2 |
| Study Plan detail (`study_plan/view.html`) | "Learning Outcomes: Not available yet" repeated on 14 topic cards; native `confirm()` for archive/delete; CTA "Dashboard" | One top-level roadmap note; styled confirmation modal for archive/delete; CTA "Home" | T2-6, T2-4, T1-1 |
| Study Plan list (`study_plan/list.html`) | Native `confirm()` for archive/delete | Styled confirmation modal | T2-4 |
| Settings (`settings/index.html`) | Build date, environment, build number, commit hash, and raw user ID visible by default; Internal Alpha status block showed build number/app version inline; native `confirm()` for Restore from Backup | All of the above moved behind a "Diagnostic information" `<details>` disclosure (two instances — General/Internal Alpha); Restore from Backup uses the styled confirmation modal | T2-1, T2-4 |
| Help & Support (`alpha/help.html`) | Release-info table + four feedback buttons; no search, topics, or FAQ | Search box filtering "Popular topics" (accordion via existing `learn_more` macro); release info demoted to a "Diagnostic information" disclosure | T2-2 |
| Analytics (`analytics/index.html`) | Six KPI tiles in one row; warning-triangle icon on zero-history "Areas for improvement" | KPI tiles in rows of four or fewer; neutral icon + single encouraging message for a zero-history week | T2-3 |
| Dashboard (legacy) Time Status (`dashboard/index.html`) | `remaining_hours` and surplus/deficit shown to two decimals (e.g. "199.98") | Rounded to whole numbers | T2-6 |
| Error pages (`errors/404.html`, `403.html`, `500.html`) | Reference ID in an off-palette pink/magenta colour, no guidance | Muted/neutral token colour; one sentence of guidance on what to do with the reference ID | T2-7 |
| Sign-in (`auth/login.html`) | Duplicate "Kwalitec" headline beneath the lockup; "Kwalitec coordinator" mentioned twice | Duplicate headline removed; "Kwalitec coordinator" stated once | T2-5 |
| Mission-related CTAs (`mission/session_recorded.html`, `research/thank_you.html`, `alpha/onboarding.html`) | "Return to Dashboard" / "Continue to Dashboard" | "Return Home" / "Continue to Home" | T1-1 |
| Global chrome (`layouts/base.html`) | No shared confirmation-dialog markup | `partials/confirm_modal.html` included once, backing every destructive-action confirmation site-wide | T2-4 |

---

## Explicitly out of scope for this pass (visual-only or unconfirmed)

- **Icon sourcing** (inline SVG duplication) — a structural/maintainability concern, not a rendered visual inconsistency today. Deferred (T2-10).
- **Legacy Learning Workspace home** (`dashboard/index.html`) still says "Dashboard" and was not restyled or relabelled — production does not serve it (`SOLE_RUNTIME=1`), and this programme's brief is to resolve *confirmed* friction, not redesign a screen scheduled for retirement.
- **General typography, spacing, colour palette** — `CONSISTENCY_AUDIT.md` §2 already found `tokens.css` compliant with `UI_UX_IMPLEMENTATION_STANDARD.md` across 8-point spacing, type scale, brand colours, card radii, input radii, motion timing, and skeleton loading. None of that was touched, per this programme's explicit "do NOT redesign for appearance" instruction.
- **Appearance/theme switcher duplication** (button-group + `<select>` on Preferences; separate button-group on Internal Alpha) — identified but not actioned; see `CONSISTENCY_DECISIONS.md` Decision 6.
