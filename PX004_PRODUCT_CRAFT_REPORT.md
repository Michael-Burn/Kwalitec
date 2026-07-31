# PX-004 — Product Craft Report

**Programme:** Product Experience Programme PX-004 — Premium Craft & Release Polish  
**Date:** 2026-07-31  
**Authority:** UX-001 · PX-001 · PX-002 · PX-003 · RC-002 · PRODUCT_EXPERIENCE_GUIDELINES.md  
**Verdict:** PASS — ready for G1 Founder Validation

---

### Principle

Every pixel must earn its place. No new capabilities — polish, consistency, interaction quality, and confidence only.

### Pages reviewed

| Surface | Pages |
|---------|-------|
| Founder | Login, Home, Subjects, Curriculum Studio (index + workspace), Feedback hub, Product Check-in, Students, Settings, Logout |
| Student | Login, Home, Session Overview / Activity / Reflection / Summary / Complete, History, Revision, Journey, Profile/Settings, Logout |
| Shared | Flash stack, empty states, design-system buttons/badges/disclosures |

### Craft improvements

| Area | Change |
|------|--------|
| Notifications | Unified `.ds-flash` token styling for Student EOS and Founder Console |
| Buttons | Complete hover / active / disabled / busy states on `ds-btn` and `console-btn` |
| Badges | Neutral tone + token-based origin badges (no hard-coded hex) |
| Empty states | History duplicate sentence removed; title/body typography hierarchy fixed |
| Headings | Profile single Settings `h1`; Journey unique aria ids |
| Copy | Softened engineering flashes; student reflections and session start tones aligned |
| Forms | Feedback hub console buttons; calmer placeholders; version validation copy |
| Motion | Flash enter animation; reduced-motion gates; removed unused `will-change` |
| Responsive | Mobile topbar: hide Switch Experience (footer remains); tighter meta spacing |

### Premium checklist

| Item | Status |
|------|--------|
| Icons | Intact (existing DS / student icon set) |
| Spacing | DS scale reinforced; founder origin badges on tokens |
| Microcopy | Softened; decision + next step |
| Alignment | Profile / History / Journey heading fixes |
| Empty states | Guide-only; no duplicate body |
| Loading | `aria-busy` cursor affordance on buttons |
| Notifications | Shared craft + dismiss |
| Tables / lists | Console buttons; list-row hover |
| Cards | No new cards; passive content left quiet |
| Forms | Focus ring fix on disclosures; validation language |
| Buttons | Predictable hierarchy on Feedback / Students |
| Dialogs / dropdowns | Existing nav / disclosure behaviour retained |
| Navigation | Labels calmed (Settings Advanced links) |
| Consistency | One flash language; one button system on polished Founder pages |

### Remaining polish debt

1. Legacy Founder pages (Vision Journal, Beta, Findings) still mix Bootstrap `btn` with Console chrome.
2. Feedback Check-in action row still uses Bootstrap outline variants (workflow-required actions).
3. No full-page POST loading indicator (intentionally not added).
4. Gate-blocked flash still includes checklist marks in one string (shortened; on-page panel remains source of truth).

### No feature additions

Presentation, CSS, flash copy, and test expectation alignment only. No Runtime C, SCI, recommendation, or curriculum changes.
