"""Foundational educational enumerations.

Vocabulary aligns with Version 2 educational architecture:
Understanding Model, Learning Model, Teaching Intention Model, Teaching
Strategy Catalogue, Educational Diagnosis Model, Application and Transfer
Model, and Educational Evidence doctrine.
"""

from __future__ import annotations

from enum import StrEnum


class UnderstandingLevel(StrEnum):
    """Progressive ladder of understanding (Understanding Model §8)."""

    RECOGNITION = "recognition"
    EXPLANATION = "explanation"
    APPLICATION = "application"
    ANALYSIS = "analysis"
    TEACHING_OTHERS = "teaching_others"


class LearningDimension(StrEnum):
    """Five dimensions of learning (Learning Model §4)."""

    UNDERSTANDING = "understanding"
    APPLICATION = "application"
    CONNECTION = "connection"
    RETENTION = "retention"
    TRANSFER = "transfer"


class TeachingIntentionType(StrEnum):
    """Named educational change sought by the next episode.

    Primary catalogue plus specialised lawful intentions from the Teaching
    Intention Model.
    """

    REPAIR_MISCONCEPTION = "repair_misconception"
    BUILD_INTUITION = "build_intuition"
    STRENGTHEN_PREREQUISITE = "strengthen_prerequisite"
    IMPROVE_TRANSFER = "improve_transfer"
    INCREASE_PROCEDURAL_FLUENCY = "increase_procedural_fluency"
    CONSOLIDATE_UNDERSTANDING = "consolidate_understanding"
    RECOVER_CONFIDENCE = "recover_confidence"
    PREPARE_FOR_EXAMINATION = "prepare_for_examination"
    IMPROVE_RETENTION = "improve_retention"
    CALIBRATE_CONFIDENCE_DOWNWARD = "calibrate_confidence_downward"
    CONNECT_FRAGMENTED_KNOWLEDGE = "connect_fragmented_knowledge"
    STRENGTHEN_APPLICATION = "strengthen_application"
    COMPLETE_MISSING_FACETS = "complete_missing_facets"


class TeachingStrategyType(StrEnum):
    """Named instructional strategies (Teaching Strategy Catalogue)."""

    DIRECT_EXPLANATION = "direct_explanation"
    ANALOGY = "analogy"
    WORKED_EXAMPLE = "worked_example"
    GUIDED_DISCOVERY = "guided_discovery"
    SOCRATIC_QUESTIONING = "socratic_questioning"
    RETRIEVAL_FIRST = "retrieval_first"
    RETRIEVAL_AFTER_INSTRUCTION = "retrieval_after_instruction"
    CONCEPT_COMPARISON = "concept_comparison"
    COUNTEREXAMPLE = "counterexample"
    MISCONCEPTION_CONFRONTATION = "misconception_confrontation"
    PROGRESSIVE_SCAFFOLDING = "progressive_scaffolding"
    FADED_GUIDANCE = "faded_guidance"
    DELIBERATE_PRACTICE = "deliberate_practice"
    INTERLEAVING = "interleaving"
    SPACED_REINFORCEMENT = "spaced_reinforcement"
    DUAL_REPRESENTATION = "dual_representation"
    CONCEPT_MAPPING = "concept_mapping"
    ERROR_LED_TEACHING = "error_led_teaching"
    THINK_ALOUD_MODELLING = "think_aloud_modelling"
    EXAM_SIMULATION = "exam_simulation"


class DiagnosisType(StrEnum):
    """Educational deficiency categories (Educational Diagnosis Model §8)."""

    CONCEPTUAL_MISUNDERSTANDING = "conceptual_misunderstanding"
    PROCEDURAL_WEAKNESS = "procedural_weakness"
    WEAK_RETENTION = "weak_retention"
    KNOWLEDGE_FRAGMENTATION = "knowledge_fragmentation"
    PREREQUISITE_GAP = "prerequisite_gap"
    MISCONCEPTION = "misconception"
    LOW_CONFIDENCE = "low_confidence"
    FALSE_CONFIDENCE = "false_confidence"
    EXAM_TECHNIQUE_WEAKNESS = "exam_technique_weakness"
    APPLICATION_WEAKNESS = "application_weakness"
    TRANSFER_WEAKNESS = "transfer_weakness"
    INCOMPLETE_UNDERSTANDING = "incomplete_understanding"


class EvidenceType(StrEnum):
    """Educational evidence kinds at the foundation grain.

    These classify *what was observed educationally*, not product event
    channel names. They remain distinct from inference, scores, and claims.
    """

    PERFORMANCE = "performance"
    EXPLANATION = "explanation"
    CLASSIFICATION = "classification"
    DIAGNOSTIC_PROBE = "diagnostic_probe"
    TRANSFER_PROBE = "transfer_probe"
    RETENTION_PROBE = "retention_probe"
    REFLECTION = "reflection"
    SELF_REPORT = "self_report"
    TIMED_PERFORMANCE = "timed_performance"
    ERROR_PATTERN = "error_pattern"
    WORKED_REASONING = "worked_reasoning"
    BOUNDARY_JUDGEMENT = "boundary_judgement"


class ReflectionType(StrEnum):
    """Structured reflection kinds that produce soft educational evidence."""

    POST_EPISODE = "post_episode"
    DIFFICULTY = "difficulty"
    CONFIDENCE = "confidence"
    CONFUSION_MAP = "confusion_map"
    STRATEGY_APPRAISAL = "strategy_appraisal"
    EXAM_READINESS = "exam_readiness"
    UNCERTAINTY = "uncertainty"


class ConfidenceLevel(StrEnum):
    """Qualitative confidence / certainty band for educational claims."""

    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
    UNKNOWN = "unknown"


class TransferLevel(StrEnum):
    """Transfer distance relative to practised surface forms.

    ``NONE`` denotes clone / identical surface competence — not transfer.
    """

    NONE = "none"
    NEAR = "near"
    FAR = "far"


class RepresentationKind(StrEnum):
    """Educational representation categories (Representation Model §4).

    Supporting vocabulary for ``RepresentationReference``.
    """

    SYMBOLIC = "symbolic"
    VERBAL = "verbal"
    VISUAL = "visual"
    GRAPHICAL = "graphical"
    TABULAR = "tabular"
    WORKED_EXAMPLE = "worked_example"
    ANALOGY = "analogy"
    SIMULATION = "simulation"
    COUNTEREXAMPLE = "counterexample"
    TIMELINE = "timeline"


class DependencyKind(StrEnum):
    """Educational dependency kinds (Knowledge Dependency Model §4).

    Supporting vocabulary for ``DependencyReference``.
    """

    REQUIRED_PREREQUISITE = "required_prerequisite"
    HELPFUL_PREREQUISITE = "helpful_prerequisite"
    PARALLEL = "parallel"
    EXTENSION = "extension"
    REMEDIATION = "remediation"
