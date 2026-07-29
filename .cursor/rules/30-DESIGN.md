# Design and UX Rules

**Status:** Permanent Cursor governance  
**Canonical references:**

| Document | Role |
|---|---|
| **BI-000** — [`knowledge/design/BRAND_GUIDELINES.md`](../../knowledge/design/BRAND_GUIDELINES.md) | Brand manual: logo, palette, voice |
| **DX-006A** — [`knowledge/design/dx006a_design_system/`](../../knowledge/design/dx006a_design_system/) | Design System foundation (tokens, catalogue, Guardian G-1…G-12) |
| **DX-006B** — [`knowledge/implementation/dx006b/`](../../knowledge/implementation/dx006b/) | Founder & Student surface migration law (fidelity ≥95%, phase order, Guard) |
| **DX-001** — [`knowledge/design/dx001_design_system/`](../../knowledge/design/dx001_design_system/) | Design language authority |
| [`knowledge/design/UI_GUARDIAN.md`](../../knowledge/design/UI_GUARDIAN.md) | UI compliance guardian |
| [`knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md`](../../knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md) | Legacy UX-001 — **superseded on conflict** by DX-001 / DX-006A |
| [`knowledge/version2/DESIGN_SYSTEM.md`](../../knowledge/version2/DESIGN_SYSTEM.md) | V2 student experience visual language |
| [`src/presentation/design_system/`](../../src/presentation/design_system/) | V3 framework-independent design system (remap to DX-006A in Phase 1) |

---

## Principles

Premium minimalist design. The interface should feel **calm, professional, and trustworthy** — never gamified, never overwhelming.

> Design to disappear. Students should admire how easy learning feels, not the chrome.

Every screen answers: **What should I do next?**  
Every recommendation answers: **Why?**

Pages compose components. Components compose tokens. Tokens define the visual language.

---

## Design System (single source of UI truth)

**Law:** `knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md` + `COMPONENT_CATALOGUE.md`.

Runtime sources (must stay semantically aligned):

- **CSS:** `app/static/css/tokens.css`
- **Python:** `presentation.design_system` (`design_tokens`, colours, spacing, typography, radius, elevation, motion, layout)
- **Hierarchy:** L0 Tokens → L1 Primitives → L2 Layout → L3 Operational → Pages (DX-006B)
- **Page migration:** Follow `knowledge/implementation/dx006b/` — Replace never layer; certify each phase before the next; Fidelity ≥95%

### Hard rules

- **No hard-coded colours.** Use semantic tokens / CSS variables.
- **No hard-coded spacing.** Product UI: **4, 8, 16, 24, 32, 48, 64** only.
- **No additional fonts.** Inter only. Hierarchy from DX-001 roles.
- **Gold (`#E8B02B`)** is reserved for logo, achievement, and completion — never for CTAs, warnings, or charts.
- **One Primary · One H1** per page (Guardian G-1, G-2).
- **No KPI theatre · No decorative cards** (G-6, G-7).
- **Rejected catalogue components** must not ship in new/migrated UI (G-12).

---

## Typography (DX-001 / DX-006A)

| Role | Size | Weight |
|---|---:|---|
| Display (rare) | 32px | 600 |
| Page heading (one H1) | 24px | 600 |
| Section heading | 18px | 600 |
| Body | 16px | 400 |
| Supporting | 14px | 400 |
| Caption | 12px | 500 |

Content column max width: `44rem` (`container.narrow`). Legacy UX-001 40/28/20 scale is not a redesign target.

---

## Spacing

| Token | Value |
|---|---|
| `space-1` | 4px |
| `space-2` | 8px |
| `space-3` | 16px |
| `space-4` | 24px |
| `space-5` | 32px |
| `space-6` | 48px |
| `space-7` | 64px |

Prefer vertical rhythm and whitespace over dense grids. Do not use 12 / 96 / 128 for new product UI.

---

## Component hierarchy

1. **One primary action per screen** — single CTA with Primary variant.
2. **L3 operational components** for Mission, Stage, Context, Queues, Findings, Feedback.
3. **Cards** only when DX-001 grouping justification holds — not decorative chrome.
4. **Secondary actions** use outline / ghost / text only.
5. **No competing CTAs.** No information overload.

---

## Colour tokens

| Semantic | Token |
|---|---|
| Primary action | `--primary` / Brand Primary Blue |
| Primary hover | `--primary-hover` |
| Text | `--text-primary` |
| Muted text | `--text-secondary` / `--text-muted` |
| Surfaces | `--surface` / `--background` |
| Borders | `--border` / `--border-subtle` |
| Status | success / warning / danger tokens |

Dark and light modes derive from the same semantic roles — never duplicate raw hex values per theme in components.

---

## Dark mode and light mode

- Semantic tokens adapt; components do not branch on theme with inline colours.
- Test contrast in both modes using `presentation.design_system.contrast` helpers.
- Dark canvases use Brand midnight / deep navy from BI-000.

---

## Motion

- Use motion tokens from the design system (≤250ms).
- Motion supports focus and feedback — not decoration.
- Respect `prefers-reduced-motion`.

---

## Navigation

- Clear wayfinding; shell owns navigation.
- Avoid exposing internal architecture terms in user-facing copy.
- Founder/operator surfaces may use denser navigation; student surfaces stay single-focus.
- No duplicate in-page nav trees (Guardian G-10).

---

## Responsive behaviour

- Breakpoints: mobile &lt;768 · tablet 768–1023 · desktop ≥1024.
- One component definition; responsive behaviour — see `RESPONSIVE_STANDARD.md`.
- Touch targets meet `shell.touch-target-min`.

---

## Accessibility

- WCAG AA — `ACCESSIBILITY_STANDARD.md`.
- Semantic HTML; ARIA when required; keyboard navigable; visible focus.
- Form errors associated with fields.

---

## Layer placement

| Concern | Layer |
|---|---|
| Design tokens and component contracts | `presentation.design_system` + CSS tokens |
| Catalogue / Guardian law | `knowledge/design/dx006a_design_system/` |
| View models and mappers | `presentation.*` |
| HTML templates | `app/templates/` (and adapters as applicable) |
| HTTP and static asset serving | Adapters |

Presentation must not contain educational decision logic.
