# Design and UX Rules

**Status:** Permanent Cursor governance  
**Canonical references:**

| Document | Role |
|---|---|
| **BI-000** — [`knowledge/design/BRAND_GUIDELINES.md`](../../knowledge/design/BRAND_GUIDELINES.md) | Brand manual: logo, palette, voice |
| [`knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md`](../../knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md) | UX-001 mandatory implementation standard |
| [`knowledge/version2/DESIGN_SYSTEM.md`](../../knowledge/version2/DESIGN_SYSTEM.md) | V2 student experience visual language |
| [`src/presentation/design_system/`](../../src/presentation/design_system/) | V3 framework-independent design system (tokens + components) |
| [`knowledge/design/UI_GUARDIAN.md`](../../knowledge/design/UI_GUARDIAN.md) | UI compliance guardian |

---

## Principles

Premium minimalist design. The interface should feel **calm, professional, and trustworthy** — never gamified, never overwhelming.

> Design to disappear. Students should admire how easy learning feels, not the chrome.

Every screen answers: **What should I do next?**  
Every recommendation answers: **Why?**

---

## Design System (single source of UI truth)

Use `presentation.design_system` for V3 surfaces:

- **Tokens:** `design_tokens`, `colours`, `spacing`, `typography`, `radius`, `elevation`, `motion`
- **Components:** `Button`, `Card`, `MissionCard`, `RecommendationCard`, `PageHeader`, etc.
- **Layout:** `layout` (breakpoints, grids, containers)
- **Contrast:** `contrast` helpers for accessibility validation

Legacy V1/V2 surfaces use CSS tokens in `app/static/css/` (`brand.css`, `student.css`).

### Hard rules

- **No hard-coded colours.** Use `colour()`, `SEMANTIC_COLOURS`, or CSS variables (`--brand-blue`, `--text-primary`, …).
- **No hard-coded spacing.** Use `space()`, `SPACING` tokens, or `--student-space-*` CSS variables.
- **No additional fonts.** Inter only. Hierarchy from size and weight.
- **Gold (`#E8B02B`)** is reserved for logo, achievement, and completion — never for CTAs, warnings, or charts.

---

## Typography

| Role | Weight | Size (reference) |
|---|---|---|
| Page title | 600 | 40px |
| Section title | 600 | 28px |
| Card title | 600 | 20px |
| Body / UI | 400–500 | 16px |
| Caption / eyebrows | 500–600 | 14px |

Content column max width: `44rem`. See UX-001 for full scale.

---

## Spacing

Use design tokens exclusively:

| Token | Value |
|---|---|
| `space-1` | 0.25rem |
| `space-2` | 0.5rem |
| `space-3` | 0.75rem |
| `space-4` | 1rem |
| `space-5` | 1.5rem |
| `space-6` | 2rem |
| `space-7` | 3rem |
| `space-8` | 4rem |

Prefer vertical rhythm and whitespace over dense grids.

---

## Component hierarchy

1. **One primary action per screen** — single CTA with `data-student-cta="primary"` or `primary_button()`.
2. **Eyebrow → title → body** pattern inside cards.
3. **Cards** (`.student-card` / `Card`) contain focused content — not decorative chrome.
4. **Secondary actions** use outline buttons or text links only.
5. **No competing CTAs.** No information overload.

---

## Colour tokens

| Semantic | Token |
|---|---|
| Primary action | `--brand-blue` / `BrandColour.PRIMARY` |
| Primary hover | `--brand-blue-dark` |
| Text | `--text-primary` |
| Muted text | `--text-secondary` |
| Surfaces | `--surface` / `--surface-alt` |
| Borders | `--divider` |
| Status | brand success / warning / danger tokens |

Dark and light modes derive from the same semantic tokens — never duplicate raw hex values per theme.

---

## Dark mode and light mode

- Semantic tokens adapt; components do not branch on theme with inline colours.
- Test contrast in both modes using `presentation.design_system.contrast` helpers.
- Dark canvases use `--brand-midnight` / `--brand-deep-navy` from BI-000.

---

## Motion

- Use `motion()` / `MOTION` tokens from the design system.
- Motion supports focus and feedback — not decoration.
- Respect `prefers-reduced-motion` for accessibility.

---

## Navigation

- Clear wayfinding: student surfaces use minimal chrome.
- Avoid exposing internal architecture terms (Digital Twin, Pipeline, Orchestrator) in user-facing copy.
- Founder/operator surfaces may use denser navigation; student surfaces stay single-focus.

---

## Responsive behaviour

- Breakpoints and grids: `presentation.design_system.layout` (`BREAKPOINTS`, `MOBILE_GRID`, `TABLET_GRID`, `DESKTOP_GRID`).
- Mobile-first layout; content reflows without horizontal scroll.
- Touch targets meet accessibility minimums.

---

## Accessibility

- WCAG contrast requirements enforced via design system contrast helpers.
- Semantic HTML in templates; ARIA labels on forms and interactive regions.
- Keyboard navigable controls; visible focus states.
- Form errors associated with fields.

---

## Layer placement

| Concern | Layer |
|---|---|
| Design tokens and component contracts | `presentation.design_system` |
| View models and mappers | `presentation.*` |
| HTML templates | `adapters.flask.rendering/templates/` and legacy `app/templates/` |
| HTTP and static asset serving | Adapters |

Presentation must not contain educational decision logic.
