# PX-002B — Screen Standardization Report

Screen-by-screen record of what PX-002B changed, and the explicit "no change
needed" verdict where a screen already met the standard after PX-002A.

Legend: 🔧 changed in this programme · ✅ reviewed, already compliant · —
out of scope (Runtime A / educational logic).

## Navigation chrome

| Screen / component | Before | After | Status |
|---|---|---|---|
| Sidebar (`partials/sidebar.html`) | 13+ inline SVG icon definitions duplicated with `topnav.html` | All icons rendered via the shared `icon()` macro (`partials/icons.html`) | 🔧 |
| Top nav (`partials/topnav.html`) | Inline SVG for the sidebar-toggle icon; bespoke icon+label appearance switcher markup | `icon()` macro for the toggle icon; shared `appearance_switcher()` macro | 🔧 |
| Settings sidebar nav (`settings/index.html`) | 6 inline SVG icons duplicated from the same icon set | All icons via `icon()` macro | 🔧 |
| Settings → Data section icons (download/upload) | 3 inline SVGs | All via `icon()` macro | 🔧 |

## Appearance control

| Location | Before | After | Status |
|---|---|---|---|
| Top nav | Icon + label buttons, `aria-labelledby` to shared caption, no per-button `aria-label` | Same visual treatment via shared macro; each button now has its own `aria-label` | 🔧 |
| Settings → Preferences | Text-only buttons + separate `<select>` fallback (different visual language from top nav) | Icon + label buttons (matching top nav) + `<select>` fallback, via shared macro | 🔧 |
| Settings → Internal Alpha | Text-only buttons (different visual language from top nav) | Icon + label buttons (matching top nav), via shared macro | 🔧 |

## Student surfaces (Journey / Revision / History)

| Screen | Before | After | Status |
|---|---|---|---|
| Journey — true empty state (no study plan / snapshot unavailable) | Bare `student-card` with one flat sentence, no CTA | `.student-empty` pattern (title + description) + "Go to Home" primary action | 🔧 |
| Journey — populated state | One current topic, completed/upcoming timelines, single primary CTA | Reviewed — already one primary heading, one CTA, no change needed | ✅ |
| Revision — true empty state | Bare `student-card`, one flat sentence, no CTA | `.student-empty` pattern + "Go to Home" primary action | 🔧 |
| Revision — "no revision focus yet" (has plan, nothing to revise) | Already had CTA + service-provided message | Reviewed — already compliant | ✅ |
| History — true empty state | Bare `student-card`, one flat sentence, no CTA | `.student-empty` pattern + "Go to Home" primary action | 🔧 |
| History — "no sessions yet" sub-empty | Single muted sentence, no encouragement | `.student-empty` title + description pattern | 🔧 |
| Home — empty state | Already used `.student-empty` pattern | Reviewed — this is the reference pattern the other three screens were brought up to | ✅ |

## Study Plan

| Screen | Before | After | Status |
|---|---|---|---|
| Roadmap card — per-topic time estimate | `{{ (minutes/60)\|round(1) }}h` — false decimal precision, "Est. Hours" label | `{{ minutes\|format_minutes }}` — "1 hour 30 min" phrasing shared with every other duration on the product, "Estimated time" label | 🔧 |
| Roadmap card — syllabus weighting, status badges, mastery % | Reviewed | Already consistent card layout, one badge per state, no change needed | ✅ |

## Mission / Study Session

| Screen | Before | After | Status |
|---|---|---|---|
| Study Session Feedback (`session_recorded.html`) | Three full-width buttons of equal visual weight; anomalous `mx-4 mb-4` on the third | One primary + one secondary full-width button; third action demoted to a plain text link | 🔧 |
| Practice Outcome Capture (`session_practice_outcome.html`) | One primary + two secondary equal-weight buttons | Reviewed — already compliant with button hierarchy rules | ✅ |
| Mission hero metrics (`mission/index.html`, `mission/session.html`) | Flex row of metric cards, no mobile breakpoint | Stacks vertically below 576px | 🔧 |
| Mission hero — "why this matters" explanation panel | Reviewed | Already one message, one visual treatment | ✅ |

## Help & Support

| Screen | Before | After | Status |
|---|---|---|---|
| Help search — no-results message | `hidden` toggled with no AT notification | `role="status" aria-live="polite"` added | 🔧 |
| Help — popular topics, quick actions, diagnostics disclosure | Reviewed (already restructured in PX-002A T2-8) | Already guidance-first; no change needed | ✅ |

## Out of scope for this programme

- Runtime A surfaces, recommendation/readiness computation, and any
  governance-controlled screens — untouched, per constraint.
- Founder/console dashboards and `education_os` adapter-rendered pages were
  not part of this student-facing premium pass and were left untouched.
