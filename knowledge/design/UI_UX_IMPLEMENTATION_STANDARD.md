# ============================================================
# KWALITEC UI/UX IMPLEMENTATION STANDARD
# Version: UX-001
# Status: MANDATORY
#
# This document complements BRAND_GUIDELINES.md.
#
# BRAND_GUIDELINES.md defines the visual identity.
#
# This document defines how that identity is implemented
# inside the Kwalitec application.
#
# Every screen, component and interaction must comply.
# ============================================================



################################################################
# 1. DESIGN PHILOSOPHY
################################################################

Kwalitec is a premium professional education platform.

The interface should feel effortless.

Students should never admire the interface.

They should admire how easy learning feels.

Every design decision must support:

• Clarity
• Confidence
• Focus
• Speed
• Trust
• Professionalism

Never design to impress.

Design to disappear.

Good UI removes friction.

Great UI becomes invisible.



################################################################
# 2. DESIGN BENCHMARKS
################################################################

Every implementation should be judged against the quality
standards of:

• Apple
• Linear
• Notion

DO NOT COPY.

Instead emulate their principles.

Apple teaches restraint.

Linear teaches efficiency.

Notion teaches organisation.

Kwalitec combines all three while maintaining its own identity.



################################################################
# 3. BRAND COMPLIANCE
################################################################

This document NEVER overrides the official Brand Guidelines.

Always use:

Primary Blue
#3B4FB8

Primary Dark
#0D1B2A

Deep Navy
#0A1628

Midnight
#020D24

Gold
#E8B02B

Never substitute brand colours.

Never invent new branding colours.

Gold is reserved for:

• Achievement
• Logo
• Awards
• Premium indicators
• Certificates
• Completion celebrations

Gold is NOT a UI colour.

Never use gold for:

Primary buttons

Navigation

Links

Input focus

charts

Primary actions

Primary UI actions always use Brand Blue.



################################################################
# 4. DESIGN PRINCIPLES
################################################################

When uncertain choose the simpler solution.

Whitespace is a feature.

Consistency beats originality.

Remove before adding.

Interfaces should breathe.

Visual hierarchy should be immediately obvious.

Every page should answer:

What is important?

What should I do next?

What has changed?

If those answers are unclear,

the page fails review.



################################################################
# 5. LAYOUT
################################################################

Use an 8-point spacing grid.

Allowed spacing:

4

8

12

16

24

32

48

64

96

128

Never invent spacing values.

Never compress layouts to fit more content.

Use whitespace generously.



################################################################
# 6. TYPOGRAPHY
################################################################

Use Inter everywhere.

Never introduce additional fonts.

Hierarchy

Page title

40px

Section title

28px

Card title

20px

Body

16px

Caption

14px

One font.

One system.

One hierarchy.



################################################################
# 7. ICONOGRAPHY
################################################################

Use Lucide Icons exclusively.

Never mix icon libraries.

Use:

20px

24px

32px

Maintain consistent stroke width.

Icons support content.

They never replace labels.



################################################################
# 8. COMPONENT DESIGN
################################################################

Every component belongs to one system.

Buttons

Cards

Inputs

Dialogs

Badges

Tables

Charts

Navigation

No screen should introduce custom styles.

Reuse existing components.



################################################################
# 9. BUTTONS
################################################################

Primary

Brand Blue

White text

Hover

Darken slightly

Lift 2px

Pressed

Scale 98%

Disabled

Reduced opacity

No shadow changes.

Transition

200ms ease-out



Secondary

White background

Grey border

Primary Dark text



Ghost

Transparent

Blue text

Subtle hover fill



Never create button variants without approval.



################################################################
# 10. CARDS
################################################################

Cards are the primary information container.

Rules

16px radius

Large internal padding

Minimal borders

Soft shadows

No gradients

No decorative backgrounds

Cards separate concepts.

They do not decorate pages.



################################################################
# 11. INPUTS
################################################################

Rounded

12px radius

Clear labels

Helper text below

Errors below

Blue focus ring

Never rely on placeholders as labels.

Validation should appear immediately.

Never after form submission.



################################################################
# 12. TABLES
################################################################

Sticky headers

Comfortable row height

Hover highlight

Minimal borders

No zebra striping

Actions right aligned.

Never overload tables.



################################################################
# 13. CHARTS
################################################################

Charts communicate insight.

Never decoration.

Default colour

Brand Blue

Supporting colours

Neutral greys

Success

Warning

Danger

Only where meaningful.

Avoid rainbow palettes.

Avoid unnecessary legends.



################################################################
# 14. MOTION
################################################################

Motion communicates state.

Never entertainment.

Hover

150ms

Page transition

250ms

Modal

200ms

Sidebar

220ms

Tooltip

120ms

Chart entrance

600ms

Use ease-out.

Never bounce.

Never shake.

Never spin unless loading.



################################################################
# 15. LOADING
################################################################

Never display empty screens.

Always preserve layout.

Use skeleton loaders.

Avoid spinners where possible.

Loading should feel stable.



################################################################
# 16. EMPTY STATES
################################################################

Every empty page includes

Illustration

Clear explanation

Primary action

Example

"No study sessions yet."

Button

Start Session

Never show blank white space.



################################################################
# 17. ERROR STATES
################################################################

Errors should help.

Never blame users.

Explain:

What happened.

Why.

How to recover.

Avoid technical language.



################################################################
# 18. ACCESSIBILITY
################################################################

Minimum WCAG AA.

Keyboard accessible.

Visible focus states.

ARIA labels.

Large hit targets.

High contrast.

Never use colour alone.

Accessibility is mandatory.



################################################################
# 19. RESPONSIVENESS
################################################################

Desktop first.

Tablet second.

Mobile third.

Do not simply shrink layouts.

Recompose them.

Navigation may collapse.

Information hierarchy must remain identical.



################################################################
# 20. PERFORMANCE
################################################################

UI quality includes speed.

Targets

60fps animations

Minimal layout shift

Lazy loading

Optimised SVG assets

No blocking animations

Fast interfaces feel premium.



################################################################
# 21. MICROINTERACTIONS
################################################################

Every interaction should acknowledge the user.

Buttons depress.

Cards elevate slightly.

Notifications fade.

Dialogs scale gently.

Success feels rewarding.

Failure feels informative.

Never overanimate.



################################################################
# 22. DASHBOARD PRINCIPLES
################################################################

Dashboards should feel calm.

Never overwhelm.

Maximum four KPI cards per row.

Charts require whitespace.

Related information grouped together.

The eye should naturally flow

Top

↓

Left

↓

Right

↓

Bottom

without confusion.



################################################################
# 23. PREMIUM QUALITY CHECK
################################################################

Before every commit ask:

Would this screen feel comfortable
next to Apple?

Would this interaction feel natural
inside Linear?

Would this information organisation
make sense inside Notion?

If the answer is "no",

redesign.



################################################################
# 24. CURSOR IMPLEMENTATION RULES
################################################################

Before implementing any UI:

1.
Check BRAND_GUIDELINES.md.

2.
Reuse existing components.

3.
Maintain design token consistency.

4.
Avoid introducing new colours.

5.
Avoid introducing new spacing values.

6.
Avoid introducing new typography.

7.
Ensure responsive behaviour.

8.
Ensure accessibility.

9.
Ensure loading states.

10.
Ensure empty states.

11.
Ensure error handling.

12.
Review against this document.



################################################################
# 25. GOLDEN RULE
################################################################

Kwalitec is not trying to look modern.

It is trying to look timeless.

Every release should move the product

towards simplicity,

towards consistency,

towards confidence.

If removing an element improves clarity,

remove it.

Premium software is rarely created by
adding more.

It is created by refining what remains.
