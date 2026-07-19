"""Canonical product brand identity labels and logo asset path (IAHF-004B).

Presentation-only constants for chrome, badges, page identity, and the
single approved logo asset. Does not affect educational logic, Twin, or
recommendations.
"""

from __future__ import annotations

# Ambient Internal Alpha programme identity (authenticated + public chrome).
INTERNAL_ALPHA_LABEL = "Internal Alpha"
FOUNDING_COHORT_LABEL = "Founding Cohort"
INTERNAL_ALPHA_BUILD_LABEL = "RC2"

# Official product-area names (user-facing).
FOUNDER_COMMAND_CENTRE_LABEL = "Founder Command Centre"
LEARNING_WORKSPACE_LABEL = "Learning Workspace"
REVISION_WORKSPACE_LABEL = "Revision Workspace"
STUDENT_DASHBOARD_LABEL = "Student Dashboard"

# Single source of truth for the displayed Kwalitec logo.
# Path is relative to Flask ``static/`` (served via versioned_static).
# Do not recreate this mark with SVG/CSS/Canvas — replace this PNG only.
APPROVED_LOGO_STATIC_PATH = "assets/branding/approved-kwalitec-logo.png"
APPROVED_LOGO_ALT = "Kwalitec"
# Native pixel size of the approved master PNG (do not stretch beyond this).
APPROVED_LOGO_NATIVE_WIDTH = 1881
APPROVED_LOGO_NATIVE_HEIGHT = 836
