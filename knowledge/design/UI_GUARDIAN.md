# ==========================================================
# KWALITEC UI GUARDIAN
#
# Version: 1.0
#
# Purpose
#
# This document governs every UI/UX implementation in Kwalitec.
#
# It enforces compliance with:
#
# • BRAND_GUIDELINES.md
# • UI_UX_IMPLEMENTATION_STANDARD.md
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



#############################################################
# IMPLEMENTATION WORKFLOW
#############################################################

Before writing code Cursor MUST

1.

Read

knowledge/design/BRAND_GUIDELINES.md

2.

Read

knowledge/design/UI_UX_IMPLEMENTATION_STANDARD.md

3.

Inspect existing reusable components.

4.

Reuse components whenever possible.

5.

Only create new components when no suitable component exists.

6.

Verify that the proposed implementation follows the design
system.

Only then may implementation begin.



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

Correct hierarchy

Correct weights

Correct spacing

Reject

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

□ Typography compliant

□ Colours compliant

□ Responsive

□ Accessible

□ Reusable components used

□ No duplicate components

□ Loading states implemented

□ Empty states implemented

□ Error states implemented

□ Animations implemented

□ Performance acceptable

□ Visual hierarchy clear

□ Consistent spacing

□ Consistent shadows

□ Consistent radii

□ Consistent icons

□ Semantic HTML

□ Keyboard navigation

□ Dark mode verified

□ Mobile verified



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

UI Standard passes.

UI Guardian passes.

Accessibility passes.

Responsive checks pass.

Performance passes.

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
