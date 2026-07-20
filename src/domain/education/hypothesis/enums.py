"""Educational Hypothesis domain enumerations.

Architecture Source
    EDUCATIONAL_HYPOTHESIS_MODEL.md
Concept
    Hypothesis Status / Kind / Plausibility / Strength / Scope / Revision
"""

from __future__ import annotations

from enum import StrEnum


class HypothesisStatus(StrEnum):
    """Lifecycle status of an EducationalHypothesis aggregate.

    Hypotheses are provisional explanations, never facts. DISCARDED retires
    explanatory trust; REVISED records lawful correction. Hypotheses never
    select teaching strategy, priority, or intention.
    """

    ACTIVE = "active"
    REVISED = "revised"
    SUSPENDED = "suspended"
    DISCARDED = "discarded"


class HypothesisKind(StrEnum):
    """Catalogue of educational explanation families.

    These name *why* a diagnosed difficulty is believed to exist. They are
    not deficiency labels (diagnosis) and not instructional moves (strategy).
    """

    PREREQUISITE_DEFICIENCY = "prerequisite_deficiency"
    REPRESENTATION_MISMATCH = "representation_mismatch"
    WEAK_ABSTRACTION = "weak_abstraction"
    SURFACE_MEMORISATION = "surface_memorisation"
    PROCEDURAL_FIXATION = "procedural_fixation"
    TRANSFER_LIMITATION = "transfer_limitation"
    CONFIDENCE_CALIBRATION_ISSUE = "confidence_calibration_issue"


class PlausibilityLevel(StrEnum):
    """Confidence posture of an educational hypothesis.

    Aligns with Educational Hypothesis Model §6. Plausibility is provisional
    and never freezes a hypothesis against contradictory evidence.
    """

    TENTATIVE = "tentative"
    WORKING = "working"
    STRONG = "strong"
    SUSPENDED = "suspended"


class ExplanatoryStrengthLevel(StrEnum):
    """How strongly the explanation accounts for supporting observations."""

    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    COMPELLING = "compelling"


class HypothesisScopeKind(StrEnum):
    """Grain of educational scope for a hypothesis explanation."""

    CONCEPT = "concept"
    LEARNING_OBJECTIVE = "learning_objective"
    LEARNING_EPISODE = "learning_episode"
    LEARNING_DIMENSION = "learning_dimension"
    CROSS_CONCEPT = "cross_concept"
    PREREQUISITE_CHAIN = "prerequisite_chain"
    SESSION_WINDOW = "session_window"


class RevisionForm(StrEnum):
    """Lawful forms of hypothesis revision (Hypothesis Model §7)."""

    NARROWING = "narrowing"
    BROADENING = "broadening"
    SHIFT = "shift"
    LAYERING = "layering"
