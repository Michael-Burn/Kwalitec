# ==========================================================
# KWALITEC UI GUARDIAN
#
# Version: 2.0 (DX-006A)
#
# Purpose
#
# This document governs every UI/UX implementation in Kwalitec.
#
# It enforces compliance with:
#
# • BRAND_GUIDELINES.md
# • DX-006A Design System foundation
#   knowledge/design/dx006a_design_system/
# • DX-001 … DX-005 surface authorities (as applicable)
# • UI_UX_IMPLEMENTATION_STANDARD.md (legacy; superseded on
#   conflict by DX-001 / DX-006A for redesigns)
#
# Detail checklist: dx006a_design_system/GUARDIAN_RULES.md
#
# Cursor MUST consult this document before implementing,
# modifying, or reviewing any user-facing interface.
#
# UI quality is a release blocker.
# ==========================================================



#############################################################
# PRIMARY DIRECTIVE
#############################################################

Every user interface must feel like it belongs to the same
product.

No screen should reveal which developer built it.

Users should experience one coherent design language.

Pages compose components.
Components compose tokens.
Tokens define the visual language.
No page invents its own primitives.



#############################################################
# IMPLEMENTATION WORKFLOW
#############################################################

Before writing code Cursor MUST

1.

Read

knowledge/design/BRAND_GUIDELINES.md

2.

Read

knowledge/design/dx006a_design_system/DESIGN_SYSTEM_ARCHITECTURE.md

knowledge/design/dx006a_design_system/DESIGN_TOKEN_SPEC.md

knowledge/design/dx006a_design_system/COMPONENT_CATALOGUE.md

knowledge/design/dx006a_design_system/GUARDIAN_RULES.md

3.

Read the surface authority when touching Founder or Student OS

DX-004A / DX-004B / DX-004C / DX-005A / DX-005B / DX-005C

4.

Inspect existing reusable components in the catalogue (L1–L3).

5.

Reuse catalogue components whenever possible.

6.

Only create new components when no suitable component exists —
and document Purpose / When / When NOT per COMPONENT_STANDARDS.md.

7.

Verify G-1 … G-12 (below) and the design system.

Only then may implementation begin.



#############################################################
# DX-006A ENFORCEMENT (G-1 … G-12)
#############################################################

Every UI change MUST PASS:

G-1  Exactly one Primary button / CTA per page
     (primary task viewport).

G-2  Exactly one H1 per page.

G-3  Token usage only — colour, space, type, radius,
     elevation, motion from DESIGN_TOKEN_SPEC.md.

G-4  No hard-coded colours in components or pages
     (token definition files excepted).

G-5  No duplicate spacing scales in new work
     (product UI: 4, 8, 16, 24, 32, 48, 64 only).

G-6  No dashboard KPI patterns
     (StatisticTile, vanity counts, ProgressRing chrome).

G-7  No decorative cards
     (cards only with DX-001 grouping justification).

G-8  L0–L3 hierarchy respected
     (pages compose catalogue components; components
     compose tokens; no page-invented primitives).

G-9  No decorative icons (Lucide; functional; named).

G-10 No duplicate navigation
     (shell owns nav; OS surface boundaries hold).

G-11 Catalogue only for shared components
     (orphans and Rejected list banned in new UI).

G-12 No Rejected foundation components
     (see COMPONENT_CATALOGUE.md § Rejected).

Full detail: knowledge/design/dx006a_design_system/GUARDIAN_RULES.md



#############################################################
# NEVER IMPLEMENT
#############################################################

Cursor MUST NEVER

Invent colours.

Invent spacing values.

Invent typography.

Invent button styles.

Invent shadows.

Invent border radii.

Invent animations.

Invent icons.

Invent layouts.

Invent component behaviour.

Ship more than one Primary CTA per page.

Ship more than one H1 per page.

Ship KPI / StatisticTile / vanity ProgressRing chrome.

Ship decorative Card wrappers.

Use Rejected catalogue components in new or migrated UI.

Use Gold as button, link, nav, or focus colour.

Invent responsive rules.

Invent accessibility behaviour.

Everything must originate from the Design System.



#############################################################
# COLOUR VALIDATION
#############################################################

Verify

✓ Brand Blue

✓ Primary Dark

✓ Deep Navy

✓ Midnight

✓ Gold

✓ White

✓ Approved semantic colours

Reject

Random blues

Random greys

Random shadows

Random gradients

Random accent colours

Never replace brand colours.



#############################################################
# TYPOGRAPHY VALIDATION
#############################################################

Verify

Inter

DX-001 / DX-006A hierarchy

Display 32 (rare) · Page 24 · Section 18 · Body 16 ·
Supporting 14 · Caption 12

Correct weights

Correct spacing

Reject

Legacy UX-001 defaults as redesign targets
(page 40 / section 28 / card 20)

Random font sizes

Mixed font families

Decorative fonts

Excessive bold text

Typography should create hierarchy through consistency.



#############################################################
# COMPONENT VALIDATION
#############################################################

Buttons

Cards

Inputs

Navigation

Dialogs

Tables

Badges

Charts

Tooltips

Dropdowns

Accordions

Tabs

Alerts

Every component must already exist inside the component system.

If a component must be created

ensure

API consistency

Styling consistency

Naming consistency

Behaviour consistency.



#############################################################
# PAGE VALIDATION
#############################################################

Every page must answer

What is this page?

What is the most important action?

Where should the eye go first?

What should happen next?

If these questions cannot be answered in under five seconds

the page fails.



#############################################################
# WHITESPACE VALIDATION
#############################################################

Whitespace is intentional.

Never compress layouts.

Never reduce spacing simply to fit more information.

Prefer

Less content

Better hierarchy

Cleaner layout



#############################################################
# VISUAL HIERARCHY
#############################################################

Each page should have

Primary focus

Secondary focus

Supporting information

Avoid

Equal emphasis everywhere.

Too many colours.

Too many cards.

Too many buttons.

Too many icons.

Too many charts.

Reduce visual noise.



#############################################################
# BUTTON VALIDATION
#############################################################

Primary actions

Brand Blue

One dominant CTA

Secondary actions

Outlined

Ghost actions

Minimal

Avoid

Multiple primary buttons.

Competing actions.

Inconsistent sizes.



#############################################################
# FORM VALIDATION
#############################################################

Labels visible.

Errors below fields.

Focus state visible.

Keyboard accessible.

Validation immediate.

Placeholder never replaces label.

Autocomplete supported where appropriate.



#############################################################
# TABLE VALIDATION
#############################################################

Minimal borders.

Comfortable spacing.

Sticky headers.

Responsive behaviour.

Action alignment.

Sorting consistency.

Loading consistency.



#############################################################
# DASHBOARD VALIDATION
#############################################################

Dashboard must feel calm.

Reject

Visual clutter.

Tiny charts.

Too many KPIs.

Competing colours.

Large paragraphs.

Aim for

Clear hierarchy.

Scannable information.

Obvious next actions.



#############################################################
# ANIMATION VALIDATION
#############################################################

Animation exists only when it communicates.

Accept

Hover

Fade

Slide

Scale

Reject

Bounce

Flash

Shake

Spin

Elastic

Long transitions

Motion should never attract attention.



#############################################################
# RESPONSIVE VALIDATION
#############################################################

Desktop

Tablet

Mobile

must all be reviewed.

Do not shrink layouts.

Recompose layouts.

Navigation adapts.

Cards stack naturally.

Tables remain usable.



#############################################################
# ACCESSIBILITY VALIDATION
#############################################################

Keyboard navigation.

Visible focus.

ARIA labels.

WCAG AA contrast.

Large touch targets.

Semantic HTML.

Accessibility failures block release.



#############################################################
# PERFORMANCE VALIDATION
#############################################################

Avoid

Layout shift

Heavy animation

Oversized images

Blocking rendering

Duplicate libraries

Large icon packs

Premium software feels fast.



#############################################################
# EMPTY STATE VALIDATION
#############################################################

Every feature requires

Loading

Empty

Success

Failure

Permission denied

Offline (where applicable)

No feature is complete without all states.



#############################################################
# MICROCOPY VALIDATION
#############################################################

Language should be

Professional.

Concise.

Helpful.

Calm.

Avoid

Developer terminology.

Blame.

Sarcasm.

Exclamation marks.

Technical stack traces.

The interface should always sound confident.



#############################################################
# DESIGN REVIEW CHECKLIST
#############################################################

Before approving implementation verify

□ Brand compliant

□ DX-006A G-1 … G-12 PASS

□ Typography compliant (DX-001 scale)

□ Colours compliant (semantic tokens only)

□ Responsive (DX-006A RESPONSIVE_STANDARD)

□ Accessible (DX-006A ACCESSIBILITY_STANDARD / WCAG AA)

□ Catalogue components used (L1–L3)

□ No Rejected components

□ No duplicate components

□ Loading states implemented

□ Empty states implemented (Reason + Next Action)

□ Error states implemented

□ Animations purposeful (≤250ms; reduced-motion)

□ Performance acceptable

□ Visual hierarchy clear

□ Consistent spacing (DX-001 4–64)

□ Consistent elevation (prefer border)

□ Consistent radii

□ Consistent icons (Lucide; non-decorative)

□ Semantic HTML

□ Keyboard navigation

□ Dark mode verified

□ Mobile verified

□ One Primary · One H1



#############################################################
# SELF REVIEW
#############################################################

Before every commit Cursor MUST ask

Would Apple remove anything?

Would Linear simplify anything?

Would Notion make this easier to scan?

If yes

implement the simpler solution.



#############################################################
# RELEASE RULE
#############################################################

UI implementation is NOT COMPLETE until

Brand Guidelines pass.

DX-006A Design System (tokens + catalogue) passes.

UI Guardian passes (including G-1 … G-12).

Accessibility passes (WCAG AA).

Responsive checks pass.

Performance passes.

Surface authority (DX-004 / DX-005) respected when applicable.

Only then may the feature be committed.



#############################################################
# FINAL PRINCIPLE
#############################################################

The objective is not to build beautiful screens.

The objective is to build software that disappears behind
the learner's experience.

When users stop noticing the interface and focus entirely on
learning,

the design has succeeded.
