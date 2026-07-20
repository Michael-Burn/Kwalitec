"""Unit tests for educational foundation enumerations."""

from __future__ import annotations

import pytest

from domain.education.foundation import (
    ConfidenceLevel,
    DependencyKind,
    DiagnosisType,
    EvidenceType,
    LearningDimension,
    ReflectionType,
    RepresentationKind,
    TeachingIntentionType,
    TeachingStrategyType,
    TransferLevel,
    UnderstandingLevel,
)


def test_understanding_level_ladder() -> None:
    assert list(UnderstandingLevel) == [
        UnderstandingLevel.RECOGNITION,
        UnderstandingLevel.EXPLANATION,
        UnderstandingLevel.APPLICATION,
        UnderstandingLevel.ANALYSIS,
        UnderstandingLevel.TEACHING_OTHERS,
    ]


def test_learning_dimensions_match_learning_model() -> None:
    assert {d.value for d in LearningDimension} == {
        "understanding",
        "application",
        "connection",
        "retention",
        "transfer",
    }


def test_teaching_intention_primary_catalogue_present() -> None:
    required = {
        TeachingIntentionType.REPAIR_MISCONCEPTION,
        TeachingIntentionType.BUILD_INTUITION,
        TeachingIntentionType.STRENGTHEN_PREREQUISITE,
        TeachingIntentionType.IMPROVE_TRANSFER,
        TeachingIntentionType.INCREASE_PROCEDURAL_FLUENCY,
        TeachingIntentionType.CONSOLIDATE_UNDERSTANDING,
        TeachingIntentionType.RECOVER_CONFIDENCE,
        TeachingIntentionType.PREPARE_FOR_EXAMINATION,
    }
    assert required <= set(TeachingIntentionType)


def test_teaching_strategy_catalogue_size() -> None:
    assert len(TeachingStrategyType) == 20
    assert TeachingStrategyType.MISCONCEPTION_CONFRONTATION.value == (
        "misconception_confrontation"
    )


def test_diagnosis_types_match_deficiency_catalogue() -> None:
    assert len(DiagnosisType) == 12
    assert DiagnosisType.MISCONCEPTION in DiagnosisType
    assert DiagnosisType.PREREQUISITE_GAP in DiagnosisType


def test_transfer_level_excludes_mastery_claims() -> None:
    assert TransferLevel.NONE.value == "none"
    assert TransferLevel.NEAR.value == "near"
    assert TransferLevel.FAR.value == "far"


def test_confidence_level_includes_unknown() -> None:
    assert ConfidenceLevel.UNKNOWN in ConfidenceLevel
    assert ConfidenceLevel.HIGH.value == "high"


def test_evidence_and_reflection_types_are_educational() -> None:
    assert EvidenceType.PERFORMANCE in EvidenceType
    assert EvidenceType.REFLECTION in EvidenceType
    assert ReflectionType.POST_EPISODE in ReflectionType
    assert ReflectionType.CONFUSION_MAP in ReflectionType


def test_supporting_representation_and_dependency_kinds() -> None:
    assert RepresentationKind.SYMBOLIC in RepresentationKind
    assert RepresentationKind.TIMELINE in RepresentationKind
    assert DependencyKind.REQUIRED_PREREQUISITE in DependencyKind
    assert DependencyKind.REMEDIATION in DependencyKind


@pytest.mark.parametrize(
    ("enum_cls", "raw"),
    [
        (UnderstandingLevel, "not_a_level"),
        (LearningDimension, "engagement"),
        (TransferLevel, "mastered"),
    ],
)
def test_invalid_enum_values_rejected(enum_cls: type, raw: str) -> None:
    with pytest.raises(ValueError):
        enum_cls(raw)
