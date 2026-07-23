# Accessibility (WCAG) Audit Notes — PR-001

Scope: production readiness audit of existing shells. No Student Experience or Console redesign.

## Baseline already present

- Student shell: skip link, `role="main"`, live region, labelled cards
- Console shell: skip link, banner/nav landmarks, reduced-motion CSS in founder dashboard styles
- Global `prefers-reduced-motion` rules in `app/static/css/app.css`
- Focus-visible styles on links

## PR-001 additions

- Legacy app shell (`layouts/base.html`): skip link → `#main-content`, `role="main"`, focus target
- Skip-link CSS for keyboard users

## Remaining gaps (blockers only if shipping UI-heavy changes)

| Area | Gap | Severity |
|---|---|---|
| CSP `unsafe-inline` | Limits future nonce-based hardening; not a WCAG fail | Medium (security) |
| Some wizard confirms | Inline `onsubmit` handlers | Low |
| Chart.js pages | Ensure canvas has text alternative where charts convey meaning | Medium |
| Colour tokens | Spot-check gold-on-navy contrast for small text | Medium |

## Gate rule

No production release of UI-impacting changes unless:

- Keyboard path reaches primary actions
- Landmarks present on changed shells
- Visible focus retained
- Reduced motion respected for new animation
