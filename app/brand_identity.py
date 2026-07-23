"""Canonical product brand identity labels and logo asset path (IAHF-004B / PX-001).

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
# CONSOLE-001 — Founder Command Centre becomes Kwalitec Console.
KWALITEC_CONSOLE_LABEL = "Kwalitec Console"
CONSOLE_HOME_LABEL = "Console Home"
FOUNDER_COMMAND_CENTRE_LABEL = KWALITEC_CONSOLE_LABEL  # alias for legacy imports
LEARNING_WORKSPACE_LABEL = "Learning Workspace"
REVISION_WORKSPACE_LABEL = "Revision Workspace"
STUDENT_DASHBOARD_LABEL = "Student Dashboard"

# Brand positioning (PX-001) — supporting descriptor and value line.
PRODUCT_NAME = "Kwalitec"
PRODUCT_DESCRIPTOR = "Education Operating System"
PRODUCT_VALUE_PROPOSITION = "Know exactly what to study next."

# Single source of truth for the displayed Kwalitec logo.
# Path is relative to Flask ``static/`` (served via versioned_static).
# Derived from the Final Approved master PNG (navy keyed for natural layout).
# Do not recreate this mark with SVG/CSS/Canvas — replace from the master only.
APPROVED_LOGO_STATIC_PATH = "assets/branding/approved-kwalitec-logo.png"
APPROVED_LOGO_ALT = "Kwalitec"
# Transparent display lockup pixel size (aspect preserved; do not stretch).
APPROVED_LOGO_NATIVE_WIDTH = 1418
APPROVED_LOGO_NATIVE_HEIGHT = 372
# In-repo archive of the Final Approved master (opaque canvas, unaltered).
APPROVED_LOGO_MASTER_STATIC_PATH = (
    "assets/branding/original/Final-Approved-Kwalitec-Logo.png"
)
APPROVED_LOGO_MASTER_NATIVE_WIDTH = 1774
APPROVED_LOGO_MASTER_NATIVE_HEIGHT = 887
