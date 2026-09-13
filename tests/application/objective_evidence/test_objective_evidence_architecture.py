"""Objective Evidence Architecture Phase 1-2 tests.

Covers CanonicalObjectiveId resolution, authored objective_id threading to
ScoreablePracticeItem, Assessment Evidence write path, untagged silence, and
structural isolation from Twin / Spacing / Policy V1 / Decision Engine.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    ProgressModelSnapshot,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import score_practice_response
from app.application.objective_evidence.canonical_objective_id import (
    CanonicalObjectiveId,
)
from app.application.objective_evidence.recorder import (
    ObjectiveAssessmentEvidenceRecorder,
)
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
    get_objective_assessment_evidence_store,
    reset_objective_assessment_evidence_store,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.services.curriculum_engine_service import CurriculumEngineService

LIVE_ROOT = Path("app/curriculum/data/educational_packages")

# Enumerated tagged sample: 36 packages / 72 item ids
# (26 original foundation + 8 topic 1.1 + 4 topic 2.3 + 12 topic 1.2
#  + 12 remaining topic 2.1 items for LO01/LO02/LO05/LO06
#  + 10 topic 2.2 items).
TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("2.1.4-poisson-process-cs1004.json", "cs1004-2.1d-ar-01", "CS1-B-T01-LO04"),
    ("2.1.4-poisson-process-cs1004.json", "cs1004-2.1d-cp-01", "CS1-B-T01-LO04"),
    ("2.1.3-prob-quantiles-cs1004.json", "cs1004-2.1c-ar-01", "CS1-B-T01-LO03"),
    ("2.1.3-prob-quantiles-cs1004.json", "cs1004-2.1c-cp-01", "CS1-B-T01-LO03"),
    ("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-ar-01", "CS1-B-T01-LO03"),
    ("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-cp-01", "CS1-B-T01-LO03"),
    ("4.1.1-response-explanatory-cs1003.json", "cs1003-4.1.1-ar-01", "CS1-D-T01-LO01"),
    ("4.1.1-response-explanatory-cs1003.json", "cs1003-4.1.1-cp-01", "CS1-D-T01-LO01"),
    ("4.1.1-response-explanatory-cs1013.json", "cs1013-4.1.1-ar-01", "CS1-D-T01-LO01"),
    ("4.1.1-response-explanatory-cs1013.json", "cs1013-4.1.1-cp-01", "CS1-D-T01-LO01"),
    ("cp-4.1.1-linear-regression-cs1016.json", "cs1016-4.1.1-ar-01", "CS1-D-T01-LO01"),
    ("cp-4.1.1-linear-regression-cs1016.json", "cs1016-4.1.1-cp-01", "CS1-D-T01-LO01"),
    ("4.1.4-software-inference-cs1003.json", "cs1003-4.1.4-ar-01", "CS1-D-T01-LO04"),
    ("4.1.4-software-inference-cs1003.json", "cs1003-4.1.4-cp-01", "CS1-D-T01-LO04"),
    ("4.1.4-software-fit-cs1013.json", "cs1013-4.1.4-ar-01", "CS1-D-T01-LO04"),
    ("4.1.4-software-fit-cs1013.json", "cs1013-4.1.4-cp-01", "CS1-D-T01-LO04"),
    ("4.2.7-model-choice-cs1003.json", "cs1003-4.2.7-ar-01", "CS1-D-T02-LO07"),
    ("4.2.7-model-choice-cs1003.json", "cs1003-4.2.7-cp-01", "CS1-D-T02-LO07"),
    ("4.2.7-model-choice-cs1014.json", "cs1014-4.2.7-ar-01", "CS1-D-T02-LO07"),
    ("4.2.7-model-choice-cs1014.json", "cs1014-4.2.7-cp-01", "CS1-D-T02-LO07"),
    ("3.1.1-method-of-moments-cs1010.json", "cs1010-3.1.1-ar-01", "CS1-C-T01-LO01"),
    ("3.1.1-method-of-moments-cs1010.json", "cs1010-3.1.1-cp-01", "CS1-C-T01-LO01"),
    ("cp-3.1.1-estimators-cs1016.json", "cs1016-3.1.1-ar-01", "CS1-C-T01-LO01"),
    ("cp-3.1.1-estimators-cs1016.json", "cs1016-3.1.1-cp-01", "CS1-C-T01-LO01"),
    ("cr-1.1.1-aims-analysis-cs1017.json", "cs1017-1.1.1-ar-01", "CS1-A-T01-LO01"),
    ("cr-1.1.1-aims-analysis-cs1017.json", "cs1017-1.1.1-cp-01", "CS1-A-T01-LO01"),
    ("cr-1.1.2-stages-tools-cs1017.json", "cs1017-1.1.2-ar-01", "CS1-A-T01-LO02"),
    ("cr-1.1.2-stages-tools-cs1017.json", "cs1017-1.1.2-cp-01", "CS1-A-T01-LO02"),
    ("cr-1.1.3-data-sources-cs1017.json", "cs1017-1.1.3-ar-01", "CS1-A-T01-LO03"),
    ("cr-1.1.3-data-sources-cs1017.json", "cs1017-1.1.3-cp-01", "CS1-A-T01-LO03"),
    ("cr-1.1.4-reproducible-cs1017.json", "cs1017-1.1.4-ar-01", "CS1-A-T01-LO04"),
    ("cr-1.1.4-reproducible-cs1017.json", "cs1017-1.1.4-cp-01", "CS1-A-T01-LO04"),
    ("1.1-purpose-function-ep001.json", "ep001-1.1-ar-01", "CS1-A-T01-LO01"),
    ("1.1-purpose-function-ep001.json", "ep001-1.1-cp-01", "CS1-A-T01-LO02"),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "cs1006-2.3.1-ar-01",
        "CS1-B-T03-LO01",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "cs1006-2.3.1-cp-01",
        "CS1-B-T03-LO01",
    ),
    (
        "2.3.2-mean-variance-conditioning-cs1006.json",
        "cs1006-2.3.2-ar-01",
        "CS1-B-T03-LO02",
    ),
    (
        "2.3.2-mean-variance-conditioning-cs1006.json",
        "cs1006-2.3.2-cp-01",
        "CS1-B-T03-LO02",
    ),
    ("1.2.1-eda-summaries-ep001.json", "ep001-1.2a-ar-01", "CS1-A-T02-LO01"),
    ("1.2.1-eda-summaries-ep001.json", "ep001-1.2a-cp-01", "CS1-A-T02-LO01"),
    ("cr-1.2.1-eda-summaries-cs1017.json", "cs1017-1.2.1-ar-01", "CS1-A-T02-LO01"),
    ("cr-1.2.1-eda-summaries-cs1017.json", "cs1017-1.2.1-cp-01", "CS1-A-T02-LO01"),
    ("1.2.2-eda-association-ep001.json", "ep001-1.2b-ar-01", "CS1-A-T02-LO02"),
    ("1.2.2-eda-association-ep001.json", "ep001-1.2b-cp-01", "CS1-A-T02-LO02"),
    ("cr-1.2.2-correlation-cs1017.json", "cs1017-1.2.2-ar-01", "CS1-A-T02-LO02"),
    ("cr-1.2.2-correlation-cs1017.json", "cs1017-1.2.2-cp-01", "CS1-A-T02-LO02"),
    ("1.2.3-pca-cs1002.json", "cs1002-1.2c-ar-01", "CS1-A-T02-LO03"),
    ("1.2.3-pca-cs1002.json", "cs1002-1.2c-cp-01", "CS1-A-T02-LO03"),
    ("cr-1.2.3-pca-cs1017.json", "cs1017-1.2.3-ar-01", "CS1-A-T02-LO03"),
    ("cr-1.2.3-pca-cs1017.json", "cs1017-1.2.3-cp-01", "CS1-A-T02-LO03"),
    ("2.1.1-discrete-cs1002.json", "cs1002-2.1a-ar-01", "CS1-B-T01-LO01"),
    ("2.1.1-discrete-cs1002.json", "cs1002-2.1a-cp-01", "CS1-B-T01-LO01"),
    ("cr-2.1.1-discrete-cs1017.json", "cs1017-2.1.1-ar-01", "CS1-B-T01-LO01"),
    ("cr-2.1.1-discrete-cs1017.json", "cs1017-2.1.1-cp-01", "CS1-B-T01-LO01"),
    ("2.1.2-continuous-cs1002.json", "cs1002-2.1b-ar-01", "CS1-B-T01-LO02"),
    ("2.1.2-continuous-cs1002.json", "cs1002-2.1b-cp-01", "CS1-B-T01-LO02"),
    ("cr-2.1.2-continuous-cs1017.json", "cs1017-2.1.2-ar-01", "CS1-B-T01-LO02"),
    ("cr-2.1.2-continuous-cs1017.json", "cs1017-2.1.2-cp-01", "CS1-B-T01-LO02"),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "cs1004-2.1e-ar-01",
        "CS1-B-T01-LO05",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "cs1004-2.1e-cp-01",
        "CS1-B-T01-LO05",
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "cs1004-2.1f-ar-01",
        "CS1-B-T01-LO06",
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "cs1004-2.1f-cp-01",
        "CS1-B-T01-LO06",
    ),
    (
        "2.2.1-marginal-conditional-cs1005.json",
        "cs1005-2.2.1-ar-01",
        "CS1-B-T02-LO01",
    ),
    (
        "2.2.1-marginal-conditional-cs1005.json",
        "cs1005-2.2.1-cp-01",
        "CS1-B-T02-LO01",
    ),
    (
        "cp-2.2.1-marginal-conditional-cs1016.json",
        "cs1016-2.2.1-ar-01",
        "CS1-B-T02-LO01",
    ),
    (
        "cp-2.2.1-marginal-conditional-cs1016.json",
        "cs1016-2.2.1-cp-01",
        "CS1-B-T02-LO01",
    ),
    (
        "2.2.2-independence-cs1005.json",
        "cs1005-2.2.2-ar-01",
        "CS1-B-T02-LO02",
    ),
    (
        "2.2.2-independence-cs1005.json",
        "cs1005-2.2.2-cp-01",
        "CS1-B-T02-LO02",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "cs1005-2.2.3-ar-01",
        "CS1-B-T02-LO03",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "cs1005-2.2.3-cp-01",
        "CS1-B-T02-LO03",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "cs1005-2.2.4-ar-01",
        "CS1-B-T02-LO04",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "cs1005-2.2.4-cp-01",
        "CS1-B-T02-LO04",
    ),
)

# Frozen 26-item foundation before topic 1.1 completion (must remain unchanged).
FOUNDATION_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = TAGGED_ITEMS[:26]

# Frozen 34-item foundation before topic 2.3 completion (26 original + topic 1.1).
FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    TAGGED_ITEMS[:34]
)

# Frozen 38-item foundation before topic 1.2 completion
# (26 original + topic 1.1 + topic 2.3).
FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    TAGGED_ITEMS[:38]
)

# Topic 1.1 (CS1-A-T01) complete slice: all 10 live knowledge checks.
TOPIC_1_1_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("cr-1.1.1-aims-analysis-cs1017.json", "cs1017-1.1.1-ar-01", "CS1-A-T01-LO01"),
    ("cr-1.1.1-aims-analysis-cs1017.json", "cs1017-1.1.1-cp-01", "CS1-A-T01-LO01"),
    ("cr-1.1.2-stages-tools-cs1017.json", "cs1017-1.1.2-ar-01", "CS1-A-T01-LO02"),
    ("cr-1.1.2-stages-tools-cs1017.json", "cs1017-1.1.2-cp-01", "CS1-A-T01-LO02"),
    ("cr-1.1.3-data-sources-cs1017.json", "cs1017-1.1.3-ar-01", "CS1-A-T01-LO03"),
    ("cr-1.1.3-data-sources-cs1017.json", "cs1017-1.1.3-cp-01", "CS1-A-T01-LO03"),
    ("cr-1.1.4-reproducible-cs1017.json", "cs1017-1.1.4-ar-01", "CS1-A-T01-LO04"),
    ("cr-1.1.4-reproducible-cs1017.json", "cs1017-1.1.4-cp-01", "CS1-A-T01-LO04"),
    ("1.1-purpose-function-ep001.json", "ep001-1.1-ar-01", "CS1-A-T01-LO01"),
    ("1.1-purpose-function-ep001.json", "ep001-1.1-cp-01", "CS1-A-T01-LO02"),
)

# Topic 2.3 (CS1-B-T03) complete slice: all 4 live knowledge checks.
TOPIC_2_3_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "cs1006-2.3.1-ar-01",
        "CS1-B-T03-LO01",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "cs1006-2.3.1-cp-01",
        "CS1-B-T03-LO01",
    ),
    (
        "2.3.2-mean-variance-conditioning-cs1006.json",
        "cs1006-2.3.2-ar-01",
        "CS1-B-T03-LO02",
    ),
    (
        "2.3.2-mean-variance-conditioning-cs1006.json",
        "cs1006-2.3.2-cp-01",
        "CS1-B-T03-LO02",
    ),
)

# Topic 1.2 (CS1-A-T02) complete slice: all 12 live knowledge checks.
TOPIC_1_2_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("1.2.1-eda-summaries-ep001.json", "ep001-1.2a-ar-01", "CS1-A-T02-LO01"),
    ("1.2.1-eda-summaries-ep001.json", "ep001-1.2a-cp-01", "CS1-A-T02-LO01"),
    ("cr-1.2.1-eda-summaries-cs1017.json", "cs1017-1.2.1-ar-01", "CS1-A-T02-LO01"),
    ("cr-1.2.1-eda-summaries-cs1017.json", "cs1017-1.2.1-cp-01", "CS1-A-T02-LO01"),
    ("1.2.2-eda-association-ep001.json", "ep001-1.2b-ar-01", "CS1-A-T02-LO02"),
    ("1.2.2-eda-association-ep001.json", "ep001-1.2b-cp-01", "CS1-A-T02-LO02"),
    ("cr-1.2.2-correlation-cs1017.json", "cs1017-1.2.2-ar-01", "CS1-A-T02-LO02"),
    ("cr-1.2.2-correlation-cs1017.json", "cs1017-1.2.2-cp-01", "CS1-A-T02-LO02"),
    ("1.2.3-pca-cs1002.json", "cs1002-1.2c-ar-01", "CS1-A-T02-LO03"),
    ("1.2.3-pca-cs1002.json", "cs1002-1.2c-cp-01", "CS1-A-T02-LO03"),
    ("cr-1.2.3-pca-cs1017.json", "cs1017-1.2.3-ar-01", "CS1-A-T02-LO03"),
    ("cr-1.2.3-pca-cs1017.json", "cs1017-1.2.3-cp-01", "CS1-A-T02-LO03"),
)

# Frozen 50-item foundation before topic 2.1 remaining-tag completion
# (26 original + topic 1.1 + topic 2.3 + topic 1.2).
FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    TAGGED_ITEMS[:50]
)

# Frozen 62-item foundation before topic 2.2 completion
# (50 through topic 1.2 + 12 remaining topic 2.1 items).
FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    TAGGED_ITEMS[:62]
)

# Topic 2.1 (CS1-B-T01) complete slice: all 18 live knowledge checks.
TOPIC_2_1_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    ("2.1.1-discrete-cs1002.json", "cs1002-2.1a-ar-01", "CS1-B-T01-LO01"),
    ("2.1.1-discrete-cs1002.json", "cs1002-2.1a-cp-01", "CS1-B-T01-LO01"),
    ("cr-2.1.1-discrete-cs1017.json", "cs1017-2.1.1-ar-01", "CS1-B-T01-LO01"),
    ("cr-2.1.1-discrete-cs1017.json", "cs1017-2.1.1-cp-01", "CS1-B-T01-LO01"),
    ("2.1.2-continuous-cs1002.json", "cs1002-2.1b-ar-01", "CS1-B-T01-LO02"),
    ("2.1.2-continuous-cs1002.json", "cs1002-2.1b-cp-01", "CS1-B-T01-LO02"),
    ("cr-2.1.2-continuous-cs1017.json", "cs1017-2.1.2-ar-01", "CS1-B-T01-LO02"),
    ("cr-2.1.2-continuous-cs1017.json", "cs1017-2.1.2-cp-01", "CS1-B-T01-LO02"),
    ("2.1.3-prob-quantiles-cs1004.json", "cs1004-2.1c-ar-01", "CS1-B-T01-LO03"),
    ("2.1.3-prob-quantiles-cs1004.json", "cs1004-2.1c-cp-01", "CS1-B-T01-LO03"),
    ("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-ar-01", "CS1-B-T01-LO03"),
    ("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-cp-01", "CS1-B-T01-LO03"),
    ("2.1.4-poisson-process-cs1004.json", "cs1004-2.1d-ar-01", "CS1-B-T01-LO04"),
    ("2.1.4-poisson-process-cs1004.json", "cs1004-2.1d-cp-01", "CS1-B-T01-LO04"),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "cs1004-2.1e-ar-01",
        "CS1-B-T01-LO05",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "cs1004-2.1e-cp-01",
        "CS1-B-T01-LO05",
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "cs1004-2.1f-ar-01",
        "CS1-B-T01-LO06",
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "cs1004-2.1f-cp-01",
        "CS1-B-T01-LO06",
    ),
)

# Topic 2.2 (CS1-B-T02) complete slice: all 10 live knowledge checks.
TOPIC_2_2_TAGGED_ITEMS: tuple[tuple[str, str, str], ...] = (
    (
        "2.2.1-marginal-conditional-cs1005.json",
        "cs1005-2.2.1-ar-01",
        "CS1-B-T02-LO01",
    ),
    (
        "2.2.1-marginal-conditional-cs1005.json",
        "cs1005-2.2.1-cp-01",
        "CS1-B-T02-LO01",
    ),
    (
        "cp-2.2.1-marginal-conditional-cs1016.json",
        "cs1016-2.2.1-ar-01",
        "CS1-B-T02-LO01",
    ),
    (
        "cp-2.2.1-marginal-conditional-cs1016.json",
        "cs1016-2.2.1-cp-01",
        "CS1-B-T02-LO01",
    ),
    (
        "2.2.2-independence-cs1005.json",
        "cs1005-2.2.2-ar-01",
        "CS1-B-T02-LO02",
    ),
    (
        "2.2.2-independence-cs1005.json",
        "cs1005-2.2.2-cp-01",
        "CS1-B-T02-LO02",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "cs1005-2.2.3-ar-01",
        "CS1-B-T02-LO03",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "cs1005-2.2.3-cp-01",
        "CS1-B-T02-LO03",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "cs1005-2.2.4-ar-01",
        "CS1-B-T02-LO04",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "cs1005-2.2.4-cp-01",
        "CS1-B-T02-LO04",
    ),
)

SAMPLE_OBJECTIVES: tuple[tuple[str, str], ...] = (
    ("CS1-B-T01-LO01", "2.1.1"),
    ("CS1-B-T01-LO02", "2.1.2"),
    ("CS1-B-T01-LO03", "2.1.3"),
    ("CS1-B-T01-LO04", "2.1.4"),
    ("CS1-B-T01-LO05", "2.1.5"),
    ("CS1-B-T01-LO06", "2.1.6"),
    ("CS1-D-T01-LO01", "4.1.1"),
    ("CS1-D-T01-LO04", "4.1.4"),
    ("CS1-D-T02-LO07", "4.2.7"),
    ("CS1-C-T01-LO01", "3.1.1"),
    ("CS1-A-T01-LO01", "1.1.1"),
    ("CS1-A-T01-LO02", "1.1.2"),
    ("CS1-A-T01-LO03", "1.1.3"),
    ("CS1-A-T01-LO04", "1.1.4"),
    ("CS1-B-T03-LO01", "2.3.1"),
    ("CS1-B-T03-LO02", "2.3.2"),
    ("CS1-A-T02-LO01", "1.2.1"),
    ("CS1-A-T02-LO02", "1.2.2"),
    ("CS1-A-T02-LO03", "1.2.3"),
    ("CS1-B-T02-LO01", "2.2.1"),
    ("CS1-B-T02-LO02", "2.2.2"),
    ("CS1-B-T02-LO03", "2.2.3"),
    ("CS1-B-T02-LO04", "2.2.4"),
)

# One AR item per diversity axis (package family / campaign / LO).
E2E_DIVERSITY: tuple[tuple[str, str, str], ...] = (
    ("2.1.4-poisson-process-cs1004.json", "cs1004-2.1d-ar-01", "CS1-B-T01-LO04"),
    ("cp-2.1.3-prob-quantiles-cs1016.json", "cs1016-2.1.3-ar-01", "CS1-B-T01-LO03"),
    ("4.1.1-response-explanatory-cs1003.json", "cs1003-4.1.1-ar-01", "CS1-D-T01-LO01"),
    ("4.2.7-model-choice-cs1014.json", "cs1014-4.2.7-ar-01", "CS1-D-T02-LO07"),
    ("cr-1.1.1-aims-analysis-cs1017.json", "cs1017-1.1.1-ar-01", "CS1-A-T01-LO01"),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "cs1006-2.3.1-ar-01",
        "CS1-B-T03-LO01",
    ),
)


def _package_from_v2(curriculum) -> dict:
    sections: list[dict] = []
    topics: list[dict] = []
    objectives: list[dict] = []
    for section in sorted(curriculum.sections, key=lambda s: s.display_order):
        sections.append(
            {
                "section_id": section.id,
                "code": section.code,
                "title": section.title,
                "number": section.code,
                "order_index": section.display_order,
            }
        )
        for topic in sorted(section.topics, key=lambda t: t.display_order):
            topics.append(
                {
                    "topic_id": topic.id,
                    "code": topic.code,
                    "title": topic.title,
                    "section_ref": section.id,
                    "number": topic.code,
                    "order_index": topic.display_order,
                    "estimated_minutes": topic.estimated_minutes,
                    "difficulty": topic.difficulty,
                    "prerequisite_ids": [],
                }
            )
            for objective in sorted(
                topic.learning_objectives, key=lambda item: item.display_order
            ):
                objectives.append(
                    {
                        "objective_id": objective.id,
                        "code": objective.code,
                        "text": objective.description,
                        "topic_ref": topic.id,
                        "number": objective.code,
                        "order_index": objective.display_order,
                        "estimated_minutes": objective.estimated_minutes,
                        "learning_type": objective.learning_type,
                        "cognitive_level": objective.cognitive_level,
                    }
                )
    return {
        "subject_code": curriculum.exam_code,
        "version_label": curriculum.version,
        "structure": {
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": [],
            "metadata": tuple(curriculum.metadata.items()),
        },
    }


class _SnapshotFoundation:
    def __init__(self, snapshot: EducationalArtefactSnapshot) -> None:
        self._snapshot = snapshot

    def derive_active(self, subject_code: str):
        return self._snapshot


@pytest.fixture
def cs1_objective_resolver() -> CanonicalObjectiveId:
    curriculum = CurriculumEngineService().load_auto("ifoa", "cs1", "2026")
    snapshot = EducationalEngineFoundationService().derive_from_package(
        _package_from_v2(curriculum)
    )
    return CanonicalObjectiveId(foundation=_SnapshotFoundation(snapshot))


@pytest.fixture(autouse=True)
def _reset_package_and_evidence_caches() -> None:
    reset_educational_package_cache()
    reset_objective_assessment_evidence_store()
    yield
    reset_educational_package_cache()
    reset_objective_assessment_evidence_store()


def test_sample_objectives_resolve_including_topic_focus_lo(
    cs1_objective_resolver: CanonicalObjectiveId,
) -> None:
    """Each sample LO resolves by id, by code, and via package topic_focus_lo."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs_by_focus: dict[str, object] = {}
    for pack in loader.all_approved():
        focus = (pack.topic_focus_lo or "").strip()
        if focus and focus not in packs_by_focus:
            packs_by_focus[focus] = pack

    for objective_id, code in SAMPLE_OBJECTIVES:
        assert (
            cs1_objective_resolver.resolve_from_objective_id(
                objective_id, subject_code="CS1"
            )
            == objective_id
        )
        assert (
            cs1_objective_resolver.resolve_from_code(code, subject_code="CS1")
            == objective_id
        )
        assert (
            cs1_objective_resolver.resolve(code, subject_code="CS1") == objective_id
        )
        # Never collapse LO identity into the parent topic id.
        resolved = cs1_objective_resolver.resolve(code, subject_code="CS1")
        assert resolved is not None
        assert "-LO" in resolved
        parent_topic_guess = resolved.rsplit("-LO", 1)[0]
        assert resolved != parent_topic_guess

        pack = packs_by_focus.get(code)
        assert pack is not None, f"no package with topic_focus_lo={code}"
        assert pack.topic_focus_lo == code
        assert (
            cs1_objective_resolver.resolve_from_topic_focus_lo(
                pack.topic_focus_lo, subject_code="CS1"
            )
            == objective_id
        )


def test_canonical_objective_id_rejects_topic_collapse() -> None:
    """Topic codes / published topic ids must not resolve as objectives."""
    snapshot = EducationalArtefactSnapshot(
        curriculum_identity="ifoa:cs1:2026",
        subject_code="CS1",
        version_label="2026",
        topics=(
            {
                "topic_id": "CS1-B-T01",
                "code": "2.1",
                "title": "Distributions",
            },
        ),
        objectives=(
            {
                "objective_id": "CS1-B-T01-LO04",
                "code": "2.1.4",
                "number": "2.1.4",
                "topic_id": "CS1-B-T01",
                "text": "Poisson process",
            },
        ),
        progress_model=ProgressModelSnapshot(
            curriculum_identity="ifoa:cs1:2026",
            topic_ids=("CS1-B-T01",),
            topics=({"topic_id": "CS1-B-T01", "topic_code": "2.1"},),
        ),
    )
    helper = CanonicalObjectiveId(foundation=_SnapshotFoundation(snapshot))
    assert helper.resolve("2.1.4", subject_code="CS1") == "CS1-B-T01-LO04"
    assert helper.resolve("CS1-B-T01-LO04", subject_code="CS1") == "CS1-B-T01-LO04"
    assert helper.resolve("2.1", subject_code="CS1") is None
    assert helper.resolve("CS1-B-T01", subject_code="CS1") is None
    assert helper.resolve("node-x", subject_code="CS1") is None
    assert helper.resolve("42", subject_code="CS1") is None


def test_all_tagged_items_carry_objective_id_on_scoreable() -> None:
    """All enumerated tagged items land on ScoreablePracticeItem.objective_ids."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    seen: set[str] = set()

    for fname, item_id, expected_oid in TAGGED_ITEMS:
        pack = packs[fname]
        substance = substance_from_package(
            pack,
            curriculum_identity=f"CS1:{pack.package_id}",
            topic_id=pack.topic_code,
        )
        practice = [
            a for a in substance.activities if a.stage is EducationalStage.PRACTICE
        ]
        match = None
        for spec in practice:
            assert spec.scoreable is not None
            if spec.scoreable.item_id == item_id:
                match = spec.scoreable
                break
        assert match is not None, f"missing practice item {item_id} in {fname}"
        assert match.objective_ids == (expected_oid,)
        seen.add(item_id)

    assert len(seen) == len(TAGGED_ITEMS)


def test_catalogue_has_no_objective_id_outside_tagged_sample() -> None:
    """No knowledge check outside the enumerated sample carries objective_id."""
    allowed = {item_id for _, item_id, _ in TAGGED_ITEMS}
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    offenders: list[str] = []
    for pack in loader.all_approved():
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            if not oid:
                continue
            if check.item_id not in allowed:
                offenders.append(f"{pack.package_id}:{check.item_id}:{oid}")
    assert offenders == []


def test_topic_1_1_all_items_carry_correct_objective_id() -> None:
    """Topic 1.1 has 10 tagged items; each of its 4 LOs has at least one."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    expected = {item_id: oid for _, item_id, oid in TOPIC_1_1_TAGGED_ITEMS}
    assert len(expected) == 10

    seen_oids: set[str] = set()
    for fname, item_id, expected_oid in TOPIC_1_1_TAGGED_ITEMS:
        pack = packs[fname]
        assert pack.topic_code == "1.1"
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid
        seen_oids.add(expected_oid)

    assert seen_oids == {
        "CS1-A-T01-LO01",
        "CS1-A-T01-LO02",
        "CS1-A-T01-LO03",
        "CS1-A-T01-LO04",
    }

    # Every knowledge check on every live topic 1.1 package is tagged.
    topic_1_1_packs = [p for p in loader.all_approved() if p.topic_code == "1.1"]
    assert topic_1_1_packs
    for pack in topic_1_1_packs:
        assert pack.knowledge_checks, f"{pack.package_id} has no knowledge checks"
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            assert oid, f"untagged {pack.package_id}:{check.item_id}"
            assert check.item_id in expected
            assert oid == expected[check.item_id]


def test_foundation_tagged_sample_unaffected_by_topic_1_1_completion() -> None:
    """The original 26-item foundation mappings are unchanged after the addition."""
    assert len(FOUNDATION_TAGGED_ITEMS) == 26
    foundation_ids = {item_id for _, item_id, _ in FOUNDATION_TAGGED_ITEMS}
    assert len(foundation_ids) == 26

    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    for fname, item_id, expected_oid in FOUNDATION_TAGGED_ITEMS:
        pack = packs[fname]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing foundation item {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid

    # New topic 1.1 completion items are outside the frozen foundation set.
    new_ids = {
        item_id
        for _, item_id, _ in TOPIC_1_1_TAGGED_ITEMS
        if item_id not in foundation_ids
    }
    assert new_ids == {
        "cs1017-1.1.2-ar-01",
        "cs1017-1.1.2-cp-01",
        "cs1017-1.1.3-ar-01",
        "cs1017-1.1.3-cp-01",
        "cs1017-1.1.4-ar-01",
        "cs1017-1.1.4-cp-01",
        "ep001-1.1-ar-01",
        "ep001-1.1-cp-01",
    }
    assert len(FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS) == 34
    assert set(FOUNDATION_TAGGED_ITEMS).issubset(
        set(FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS)
    )
    assert set(FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))


def test_topic_2_3_all_items_carry_correct_objective_id() -> None:
    """Topic 2.3 has 4 tagged items; each of its 2 LOs has at least one."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    expected = {item_id: oid for _, item_id, oid in TOPIC_2_3_TAGGED_ITEMS}
    assert len(expected) == 4

    seen_oids: set[str] = set()
    for fname, item_id, expected_oid in TOPIC_2_3_TAGGED_ITEMS:
        pack = packs[fname]
        assert pack.topic_code == "2.3"
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid
        seen_oids.add(expected_oid)

    assert seen_oids == {
        "CS1-B-T03-LO01",
        "CS1-B-T03-LO02",
    }

    # Every knowledge check on every live topic 2.3 package is tagged.
    topic_2_3_packs = [p for p in loader.all_approved() if p.topic_code == "2.3"]
    assert topic_2_3_packs
    for pack in topic_2_3_packs:
        assert pack.knowledge_checks, f"{pack.package_id} has no knowledge checks"
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            assert oid, f"untagged {pack.package_id}:{check.item_id}"
            assert check.item_id in expected
            assert oid == expected[check.item_id]


def test_foundation_tagged_sample_unaffected_by_topic_2_3_completion() -> None:
    """The prior 34-item foundation mappings are unchanged after topic 2.3."""
    assert len(FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS) == 34
    prior_ids = {
        item_id for _, item_id, _ in FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS
    }
    assert len(prior_ids) == 34

    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    for fname, item_id, expected_oid in FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS:
        pack = packs[fname]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing prior foundation item {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid

    # Topic 2.3 completion items are entirely outside the frozen prior set.
    new_ids = {
        item_id
        for _, item_id, _ in TOPIC_2_3_TAGGED_ITEMS
        if item_id not in prior_ids
    }
    assert new_ids == {
        "cs1006-2.3.1-ar-01",
        "cs1006-2.3.1-cp-01",
        "cs1006-2.3.2-ar-01",
        "cs1006-2.3.2-cp-01",
    }
    assert len(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS) == 38
    assert set(FOUNDATION_THROUGH_TOPIC_1_1_TAGGED_ITEMS).issubset(
        set(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS)
    )
    assert set(TOPIC_2_3_TAGGED_ITEMS).issubset(
        set(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS)
    )
    assert set(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))


def test_topic_1_2_all_items_carry_correct_objective_id() -> None:
    """Topic 1.2 has 12 tagged items; each of its 3 LOs has at least one."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    expected = {item_id: oid for _, item_id, oid in TOPIC_1_2_TAGGED_ITEMS}
    assert len(expected) == 12

    seen_oids: set[str] = set()
    for fname, item_id, expected_oid in TOPIC_1_2_TAGGED_ITEMS:
        pack = packs[fname]
        assert pack.topic_code == "1.2"
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid
        seen_oids.add(expected_oid)

    assert seen_oids == {
        "CS1-A-T02-LO01",
        "CS1-A-T02-LO02",
        "CS1-A-T02-LO03",
    }

    # Every knowledge check on every live topic 1.2 package is tagged.
    topic_1_2_packs = [p for p in loader.all_approved() if p.topic_code == "1.2"]
    assert topic_1_2_packs
    for pack in topic_1_2_packs:
        assert pack.knowledge_checks, f"{pack.package_id} has no knowledge checks"
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            assert oid, f"untagged {pack.package_id}:{check.item_id}"
            assert check.item_id in expected
            assert oid == expected[check.item_id]


def test_foundation_tagged_sample_unaffected_by_topic_1_2_completion() -> None:
    """The prior 38-item foundation mappings are unchanged after topic 1.2."""
    assert len(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS) == 38
    prior_ids = {
        item_id for _, item_id, _ in FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS
    }
    assert len(prior_ids) == 38

    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    for fname, item_id, expected_oid in FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS:
        pack = packs[fname]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing prior foundation item {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid

    new_ids = {
        item_id
        for _, item_id, _ in TOPIC_1_2_TAGGED_ITEMS
        if item_id not in prior_ids
    }
    assert new_ids == {
        "ep001-1.2a-ar-01",
        "ep001-1.2a-cp-01",
        "cs1017-1.2.1-ar-01",
        "cs1017-1.2.1-cp-01",
        "ep001-1.2b-ar-01",
        "ep001-1.2b-cp-01",
        "cs1017-1.2.2-ar-01",
        "cs1017-1.2.2-cp-01",
        "cs1002-1.2c-ar-01",
        "cs1002-1.2c-cp-01",
        "cs1017-1.2.3-ar-01",
        "cs1017-1.2.3-cp-01",
    }
    assert len(TAGGED_ITEMS) == 72
    assert set(FOUNDATION_THROUGH_TOPIC_2_3_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(TOPIC_1_2_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(TOPIC_2_1_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))


def test_topic_2_1_all_items_carry_correct_objective_id() -> None:
    """Topic 2.1 has 18 tagged items; each of its 6 LOs has at least one."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    expected = {item_id: oid for _, item_id, oid in TOPIC_2_1_TAGGED_ITEMS}
    assert len(expected) == 18

    seen_oids: set[str] = set()
    for fname, item_id, expected_oid in TOPIC_2_1_TAGGED_ITEMS:
        pack = packs[fname]
        assert pack.topic_code == "2.1"
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid
        seen_oids.add(expected_oid)

    assert seen_oids == {
        "CS1-B-T01-LO01",
        "CS1-B-T01-LO02",
        "CS1-B-T01-LO03",
        "CS1-B-T01-LO04",
        "CS1-B-T01-LO05",
        "CS1-B-T01-LO06",
    }

    topic_2_1_packs = [p for p in loader.all_approved() if p.topic_code == "2.1"]
    assert topic_2_1_packs
    for pack in topic_2_1_packs:
        assert pack.knowledge_checks, f"{pack.package_id} has no knowledge checks"
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            assert oid, f"untagged {pack.package_id}:{check.item_id}"
            assert check.item_id in expected
            assert oid == expected[check.item_id]


def test_foundation_tagged_sample_unaffected_by_topic_2_1_completion() -> None:
    """The prior 50-item foundation mappings are unchanged after topic 2.1."""
    assert len(FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS) == 50
    prior_ids = {
        item_id for _, item_id, _ in FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS
    }
    assert len(prior_ids) == 50

    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    for fname, item_id, expected_oid in FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS:
        pack = packs[fname]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing prior foundation item {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid

    new_ids = {
        item_id
        for _, item_id, _ in TOPIC_2_1_TAGGED_ITEMS
        if item_id not in prior_ids
    }
    assert new_ids == {
        "cs1002-2.1a-ar-01",
        "cs1002-2.1a-cp-01",
        "cs1017-2.1.1-ar-01",
        "cs1017-2.1.1-cp-01",
        "cs1002-2.1b-ar-01",
        "cs1002-2.1b-cp-01",
        "cs1017-2.1.2-ar-01",
        "cs1017-2.1.2-cp-01",
        "cs1004-2.1e-ar-01",
        "cs1004-2.1e-cp-01",
        "cs1004-2.1f-ar-01",
        "cs1004-2.1f-cp-01",
    }
    assert len(TAGGED_ITEMS) == 72
    assert set(FOUNDATION_THROUGH_TOPIC_1_2_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(TOPIC_2_1_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))


def test_topic_2_2_all_items_carry_correct_objective_id() -> None:
    """Topic 2.2 has 10 tagged items; each of its 4 LOs has at least one."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    expected = {item_id: oid for _, item_id, oid in TOPIC_2_2_TAGGED_ITEMS}
    assert len(expected) == 10

    seen_oids: set[str] = set()
    for fname, item_id, expected_oid in TOPIC_2_2_TAGGED_ITEMS:
        pack = packs[fname]
        assert pack.topic_code == "2.2"
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid
        seen_oids.add(expected_oid)

    assert seen_oids == {
        "CS1-B-T02-LO01",
        "CS1-B-T02-LO02",
        "CS1-B-T02-LO03",
        "CS1-B-T02-LO04",
    }

    topic_2_2_packs = [p for p in loader.all_approved() if p.topic_code == "2.2"]
    assert topic_2_2_packs
    for pack in topic_2_2_packs:
        assert pack.knowledge_checks, f"{pack.package_id} has no knowledge checks"
        for check in pack.knowledge_checks:
            oid = (check.objective_id or "").strip()
            assert oid, f"untagged {pack.package_id}:{check.item_id}"
            assert check.item_id in expected
            assert oid == expected[check.item_id]


def test_foundation_tagged_sample_unaffected_by_topic_2_2_completion() -> None:
    """The prior 62-item foundation mappings are unchanged after topic 2.2."""
    assert len(FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS) == 62
    prior_ids = {
        item_id for _, item_id, _ in FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS
    }
    assert len(prior_ids) == 62

    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    for fname, item_id, expected_oid in FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS:
        pack = packs[fname]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing prior foundation item {item_id} in {fname}"
        assert (match.objective_id or "").strip() == expected_oid

    new_ids = {
        item_id
        for _, item_id, _ in TOPIC_2_2_TAGGED_ITEMS
        if item_id not in prior_ids
    }
    assert new_ids == {
        "cs1005-2.2.1-ar-01",
        "cs1005-2.2.1-cp-01",
        "cs1016-2.2.1-ar-01",
        "cs1016-2.2.1-cp-01",
        "cs1005-2.2.2-ar-01",
        "cs1005-2.2.2-cp-01",
        "cs1005-2.2.3-ar-01",
        "cs1005-2.2.3-cp-01",
        "cs1005-2.2.4-ar-01",
        "cs1005-2.2.4-cp-01",
    }
    assert len(TAGGED_ITEMS) == 72
    assert set(FOUNDATION_THROUGH_TOPIC_2_1_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))
    assert set(TOPIC_2_2_TAGGED_ITEMS).issubset(set(TAGGED_ITEMS))


def _advance_to_item(
    engine: PackageActivityEngine,
    *,
    student_id: str,
    session_id: str,
    item_id: str,
) -> dict:
    current = engine.get_current_activity_opaque(student_id, session_id=session_id)
    guard = 0
    while current is not None and guard < 20:
        guard += 1
        # Sequence item scoreable is internal; use store.
        key = PackageActivityEngine._key(student_id, session_id)
        seq = engine._store.get(PackageActivityEngine.NS_SEQUENCE, key) or {}
        activities = list(seq.get("activities") or ())
        index = int(seq.get("index") or 1)
        item = dict(activities[index - 1]) if activities else {}
        raw_scoreable = item.get("scoreable") or {}
        scoreable_id = str(raw_scoreable.get("item_id") or "")
        if (
            current.get("stage") == EducationalStage.PRACTICE.value
            and scoreable_id == item_id
        ):
            return current
        engine.submit_response_opaque(
            student_id,
            session_id=session_id,
            activity_id=current["activity_id"],
            response="noted",
        )
        current = engine.advance_activity_opaque(student_id, session_id=session_id)
    raise AssertionError(f"did not reach practice item {item_id}")


def _correct_response_for_item(pack, item_id: str) -> str:
    for check in pack.knowledge_checks:
        if check.item_id != item_id:
            continue
        if (check.response_type or "").lower() in {"mcq", "multiple_choice"}:
            return check.correct_choice_id
        if (check.response_type or "").lower() in {"numeric", "number"}:
            return check.accepted_keywords[0] if check.accepted_keywords else "0"
        # short_structured: use a keyword if present
        if check.accepted_keywords:
            return " ".join(check.accepted_keywords[:2])
        return "explain link"
    raise AssertionError(f"item {item_id} not in package")


@pytest.mark.parametrize(
    ("fname", "item_id", "expected_oid"),
    E2E_DIVERSITY,
    ids=[row[1] for row in E2E_DIVERSITY],
)
def test_e2e_assessment_evidence_for_diversity_axes(
    fname: str, item_id: str, expected_oid: str
) -> None:
    """Load → sit → submit writes durable Assessment Evidence with real LO id."""
    store = ObjectiveAssessmentEvidenceStore()
    recorder = ObjectiveAssessmentEvidenceRecorder(store=store)
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    pack = packs[fname]

    substance = substance_from_package(
        pack,
        curriculum_identity=f"CS1:{pack.package_id}",
        topic_id=pack.topic_code,
    )
    session_store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=session_store)
    engine = PackageActivityEngine(
        store=session_store,
        persistence=persistence,
        objective_evidence_recorder=recorder,
    )
    student_id = f"stu-{item_id}"
    session_id = f"sess-{item_id}"
    engine.provision_sequence(student_id, session_id=session_id, substance=substance)

    activity = _advance_to_item(
        engine, student_id=student_id, session_id=session_id, item_id=item_id
    )
    response = _correct_response_for_item(pack, item_id)
    before = store.count()
    result = engine.submit_response_opaque(
        student_id,
        session_id=session_id,
        activity_id=activity["activity_id"],
        response=response,
    )
    assert result.get("scored_correct") is True
    assert store.count() == before + 1

    rows = store.list_for_objective(expected_oid)
    assert len(rows) == 1
    row = rows[0]
    assert row.objective_id == expected_oid
    assert row.item_id == item_id
    assert row.student_id == student_id
    assert row.session_id == session_id
    assert row.package_id == pack.package_id
    assert row.scored_correct is True
    assert row.source == "package_activity_engine"


def test_untagged_item_produces_zero_assessment_evidence() -> None:
    """Any untagged catalogue item leaves Assessment Evidence empty."""
    # Pick a live package that is not in the tagged sample set.
    tagged_files = {fname for fname, _, _ in TAGGED_ITEMS}
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    untagged = None
    for pack in loader.all_approved():
        if Path(pack.source_path).name in tagged_files:
            continue
        if not pack.knowledge_checks:
            continue
        if any((c.objective_id or "").strip() for c in pack.knowledge_checks):
            continue
        untagged = pack
        break
    assert untagged is not None

    store = ObjectiveAssessmentEvidenceStore()
    recorder = ObjectiveAssessmentEvidenceRecorder(store=store)
    substance = substance_from_package(
        untagged,
        curriculum_identity=f"CS1:{untagged.package_id}",
        topic_id=untagged.topic_code,
    )
    session_store = SessionDocumentStore()
    engine = PackageActivityEngine(
        store=session_store,
        persistence=LearningSessionPersistenceAdapter(store=session_store),
        objective_evidence_recorder=recorder,
    )
    engine.provision_sequence(
        "stu-untagged",
        session_id="sess-untagged",
        substance=substance,
    )

    current = engine.get_current_activity_opaque(
        "stu-untagged",
        session_id="sess-untagged",
    )
    guard = 0
    while current is not None and guard < 20:
        guard += 1
        engine.submit_response_opaque(
            "stu-untagged",
            session_id="sess-untagged",
            activity_id=current["activity_id"],
            response="noted explain link",
        )
        if current.get("stage") == EducationalStage.PRACTICE.value:
            # Continue through remaining practice too.
            pass
        current = engine.advance_activity_opaque(
            "stu-untagged", session_id="sess-untagged"
        )

    assert store.count() == 0
    assert get_objective_assessment_evidence_store().count() == 0


def test_recorder_ignores_synthetic_package_lo_ids() -> None:
    """Synthetic activity ids like '{package}:lo' must not create evidence."""
    from app.application.learning_session.scoreable_practice import (
        AnswerKey,
        PracticeResponseType,
        PracticeScoreResult,
        ScoreablePracticeItem,
    )

    store = ObjectiveAssessmentEvidenceStore()
    recorder = ObjectiveAssessmentEvidenceRecorder(store=store)
    scoreable = ScoreablePracticeItem(
        item_id="synthetic-item",
        prompt="x",
        response_type=PracticeResponseType.MCQ,
        answer_key=AnswerKey(accepted=("a",), correct_choice_id="a"),
        explanation="",
        model_answer="",
        objective_ids=("CS1-EP001-PKG-2.1-POISSON-PROCESS:lo",),
    )
    score = PracticeScoreResult(
        scored=True,
        correct=True,
        item_id="synthetic-item",
        response_type="mcq",
    )
    assert (
        recorder.record_if_tagged(
            student_id="s",
            session_id="sess",
            package_id="pkg",
            scoreable=scoreable,
            score=score,
        )
        is None
    )
    assert store.count() == 0


def test_objective_evidence_path_isolated_from_decision_systems() -> None:
    """Structural import check: new path is unread by Twin / Spacing / Policy / DE."""
    forbidden_consumers = (
        Path("app/application/student_twin"),
        Path("app/application/spacing_scheduler"),
        Path("app/domain/spacing_scheduler"),
        Path("app/infrastructure/adapters/spacing_scheduler"),
        Path("app/application/adaptive_decision"),
    )
    banned_import_needles = (
        "app.application.objective_evidence",
        "objective_evidence.canonical_objective_id",
        "objective_evidence.recorder",
        "objective_evidence.store",
        "objective_evidence.records",
    )

    offenders: list[str] = []
    for root in forbidden_consumers:
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names: list[str] = []
                if isinstance(node, ast.Import):
                    names = [alias.name for alias in node.names]
                elif isinstance(node, ast.ImportFrom) and node.module:
                    names = [node.module]
                for name in names:
                    if any(b in name for b in banned_import_needles):
                        offenders.append(f"{path}: import {name}")
            source = path.read_text(encoding="utf-8")
            if "ObjectiveAssessmentEvidenceRecorder" in source:
                offenders.append(f"{path}: references recorder")
            if "AssessmentEvidenceRecord" in source:
                offenders.append(f"{path}: references AssessmentEvidenceRecord")
            if "CanonicalObjectiveId" in source:
                offenders.append(f"{path}: references CanonicalObjectiveId")

    # New package must not import Twin / Spacing / Policy / Decision Engine.
    oe_root = Path("app/application/objective_evidence")
    banned_from_oe = (
        "app.application.student_twin",
        "app.application.spacing_scheduler",
        "app.domain.spacing_scheduler",
        "app.infrastructure.adapters.spacing_scheduler",
        "app.application.adaptive_decision",
    )
    for path in oe_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if any(name == b or name.startswith(b + ".") for b in banned_from_oe):
                    offenders.append(f"{path}: imports {name}")

    # PackageActivityEngine may import the recorder for writes only; confirm
    # it does not import Twin / Spacing / Policy decision modules.
    engine_path = Path(
        "app/infrastructure/adapters/learning_session/package_activity_engine.py"
    )
    engine_tree = ast.parse(engine_path.read_text(encoding="utf-8"))
    engine_imports: list[str] = []
    for node in ast.walk(engine_tree):
        if isinstance(node, ast.Import):
            engine_imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            engine_imports.append(node.module)
    for name in engine_imports:
        if any(
            b in name
            for b in (
                "student_twin",
                "spacing_scheduler",
                "adaptive_decision",
                "policy_v1",
            )
        ):
            offenders.append(f"{engine_path}: import {name}")
    assert "app.application.objective_evidence.recorder" in engine_imports

    assert offenders == []


def test_find_package_topic_focus_lo_runtime_path() -> None:
    """Loader surfaces topic_focus_lo so package → code → objective_id works."""
    pack = find_package_by_id("CS1-EP001-PKG-2.1-POISSON-PROCESS")
    assert pack is not None
    assert pack.topic_focus_lo == "2.1.4"
    for check in pack.knowledge_checks:
        if check.item_id in {"cs1004-2.1d-ar-01", "cs1004-2.1d-cp-01"}:
            assert check.objective_id == "CS1-B-T01-LO04"


def test_score_practice_roundtrip_preserves_objective_ids() -> None:
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    pack = packs["2.1.4-poisson-process-cs1004.json"]
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:test",
        topic_id=pack.topic_code,
    )
    practice = [
        a for a in substance.activities if a.stage is EducationalStage.PRACTICE
    ]
    scoreable = practice[0].scoreable
    assert scoreable is not None
    assert scoreable.objective_ids == ("CS1-B-T01-LO04",)
    opaque = scoreable.to_opaque()
    restored = type(scoreable).from_opaque(opaque)
    assert restored is not None
    assert restored.objective_ids == ("CS1-B-T01-LO04",)
    choice = pack.knowledge_checks[0].correct_choice_id
    result = score_practice_response(restored, choice)
    assert result.scored_correct is True
