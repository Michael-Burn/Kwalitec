# Student Experience Design System

**Document ID:** V2-017B-B-DESIGN-SYSTEM  
**Milestone:** V2-017B-B — Student Experience UI  
**Status:** Authoritative presentation design reference  
**Authority:** Presentation / UX — not educational law  
**Implements:** `app/static/css/student.css`, `templates/student/`

---

## 1. Purpose

Define a calm, professional, trustworthy visual language for the Version 2 Student Experience.

Every screen answers:

> What should I do next?

Every recommendation answers:

> Why?

This document does **not** define educational algorithms. Those live in Student Experience application services and upstream ports.

---

## 2. Product feel

| Intent | Meaning |
|--------|---------|
| Calm | Large whitespace, one focus, quiet chrome |
| Professional | Inter everywhere; weight and size create hierarchy |
| Trustworthy | Explainable copy, accessible contrast, stable layout |
| Purposeful | One primary action per screen |

### Avoid

- Gamification (streaks, confetti, empty badges)
- Information overload
- Internal architecture terms (Digital Twin, Adaptive Decision, Learning Orchestrator)
- Multiple competing CTAs

---

## 3. Typography

Governed by `knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md` (UX-001) and Brand Guidelines.

| Role | Family | Weight | Size |
|------|--------|--------|------|
| Page title | Inter | 600 | 40px |
| Section title | Inter | 600 | 28px |
| Card title | Inter | 600 | 20px |
| Body / UI | Inter | 400–500 | 16px |
| Caption / eyebrows | Inter | 500–600 | 14px |

Never introduce additional fonts. Hierarchy comes from size and weight only.

Line length: content column max `44rem`.

---

## 4. Spacing

CSS tokens:

| Token | Value |
|-------|-------|
| `--student-space-1` | 0.25rem |
| `--student-space-2` | 0.5rem |
| `--student-space-3` | 0.75rem |
| `--student-space-4` | 1rem |
| `--student-space-5` | 1.5rem |
| `--student-space-6` | 2rem |
| `--student-space-7` | 3rem |
| `--student-space-8` | 4rem |

Prefer vertical rhythm over dense grids. Home uses a short summary row, then one primary recommendation stack.

---

## 5. Colour semantics

Built on `brand.css` and governed by UX-001 / UI Guardian:

| Semantic | Source |
|----------|--------|
| Primary action | `--brand-blue` |
| Primary hover | `--brand-blue-dark` |
| Text | `--text-primary` |
| Muted text | `--text-secondary` |
| Surfaces | `--surface` / `--surface-alt` |
| Borders | `--divider` |
| Success / warning / danger | brand status tokens (warning is amber — **not** brand gold) |

Gold (`#E8B02B`) is reserved for logo, achievement, awards, and completion — never for CTAs, charts, warnings, or decorative washes.

---

## 6. Cards

`.student-card` is the default content container:

- Soft border, 16px radius (`--student-radius`)
- Generous padding (`1.5rem`)
- Eyebrow + title + body pattern
- Recommendation / primary revision cards get a subtle blue border emphasis

Cards are allowed because they contain interaction or focused educational content — not decorative chrome.

---

## 7. Buttons

| Type | Class | Use |
|------|-------|-----|
| Primary | `.student-btn-primary` + `data-student-cta="primary"` | The single next action |
| Secondary | Bootstrap outline / text links | Navigation and alternatives |

Rules:

1. Exactly one primary CTA per surface when an action exists.
2. Primary CTA answers “what next”.
3. Disabled / unavailable states explain calmly — never invent a fake action.

---

## 8. Navigation

Canonical surfaces (owned by Experience):

1. Home  
2. Journey  
3. Revision  
4. History  
5. Profile  

Presentation:

- Sticky top bar with brand + horizontal nav
- Active item uses `aria-current="page"` and `.is-active`
- Mobile: wrap; no hamburger required for five items

---

## 9. Badges

Use sparingly for educational meaning only (e.g. revision priority labels).

Do **not** use badges for streaks, XP, or empty engagement trophies.

---

## 10. Progress indicators

`.student-progress` / `.student-progress-bar`:

- Horizontal bar with `role="progressbar"`
- `aria-valuenow` / `min` / `max` required
- Values come from Experience snapshots — UI only formats

---

## 11. Timeline

Journey completed / upcoming topics use `.student-timeline`:

- Marker + title + optional prerequisite note
- Completed markers filled; upcoming outlined
- Never expose graph/node/edge terminology

---

## 12. Responsive behaviour

| Breakpoint | Behaviour |
|------------|-----------|
| < 480px | Single column; full-width primary CTA |
| ≥ 480px | Meta rows two-column; CTA auto-width |
| ≥ 640px | Home / history stats two-column |

Touch targets: primary buttons ≥ ~44px height via padding.

---

## 13. Accessibility

- Skip link to `#student-main`
- Focus rings via `--student-focus`
- Colour is not the sole signal (labels + text accompany readiness / priority)
- Prefer `prefers-reduced-motion: reduce` (disable progress transitions)
- Semantic landmarks: `banner`, `navigation`, `main`, `contentinfo`
- Forms use Flask-WTF CSRF

Contrast: text/background follow brand light/dark themes.

---

## 14. Dark mode strategy

- Rely on `[data-theme="dark"]` tokens from `brand.css` / `theme.js`
- Student surfaces remount on shared semantic variables — no separate dark palette inventing new brand colours
- Top bar uses translucent surface + blur for continuity

---

## 15. Component inventory

| Component | Template | Contents |
|-----------|----------|----------|
| Recommendation Card | `recommendation_card.html` | Recommendation, benefit, time, reason, CTA |
| Readiness Card | `readiness_card.html` | Current readiness, trend, confidence |
| Journey Card | `journey_card.html` | Current topic, progress, next topic |
| Progress Card | `progress_card.html` | Overall progress + estimate |
| Explanation Card | `explanation_card.html` | Educational reasoning |
| History Card | `history_card.html` | Session summary, duration, outcome |
| Countdown Card | `countdown_card.html` | Exam countdown |
| Navigation | `navigation.html` | Surface links |

---

## 16. Architecture reminder

```text
Templates / routes
        │
        ▼
Student Experience application services
        │
        ▼
Ports → Twin / Adaptive Decision / Mission / Journey / Orchestrator
```

Presentation may format labels and navigate.  
Presentation must not compute readiness, recommendations, missions, or journeys.
