"""Phase-0 prototype — choice-aware feedback via misconception_tag.

Proves allowlisted items get choice-specific mistake copy, correctness
matching is unchanged, correct-answer path is untouched, and the selected
misconception_tag is captured on the score / evidence log path.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.choice_aware_feedback_prototype import (
    PROTOTYPE_CHOICE_FEEDBACK,
    PROTOTYPE_ITEM_IDS,
    assemble_choice_aware_mistake,
)
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import (
    PracticeResponseType,
    ScoreablePracticeItem,
    _match_mcq,
    score_practice_response,
)
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.session.services.study_session_service import (
    _practice_feedback_parts,
)
from tests.presentation.session.test_session_redesign import _base_page, _render

LIVE_PACKAGE_ROOT = Path("app/curriculum/data/educational_packages")

# Original four pilot items (must remain byte-identical in feedback map).
_ORIGINAL_PILOT_PACKAGES: tuple[tuple[str, str], ...] = (
    ("3.1.3-efficiency-bias-consistency-mse-cs1010", "cs1010-3.1.3-cp-01"),
    ("4.2.1-exponential-family-cs1014", "cs1014-4.2.1-ar-01"),
    ("cr-2.1.2-continuous-cs1017", "cs1017-2.1.2-cp-01"),
    ("revision-estimators-cs1010", "cs1010-ck-r1-cp-01"),
)

# Editorially reviewed expansion (2026-09-09).
_EXPANSION_PACKAGES: tuple[tuple[str, str], ...] = (
    ("5.1.1-bayes-theorem-cs1003", "cs1003-5.1.1-ar-01"),
    ("5.1.1-bayes-theorem-cs1003", "cs1003-5.1.1-cp-01"),
    ("5.1.1-bayes-theorem-cs1015", "cs1015-5.1.1-ar-01"),
    ("5.1.1-bayes-theorem-cs1015", "cs1015-5.1.1-cp-01"),
    ("revision-bayesian-cs1015", "cs1015-co-r1-ar-01"),
    ("revision-bayesian-cs1015", "cs1015-co-r1-cp-01"),
    ("3.1.3-efficiency-bias-consistency-mse-cs1010", "cs1010-3.1.3-ar-01"),
    ("3.1.4-comparison-mse-cs1010", "cs1010-3.1.4-ar-01"),
    ("3.1.4-comparison-mse-cs1010", "cs1010-3.1.4-cp-01"),
    ("4.2.1-exponential-family-cs1014", "cs1014-4.2.1-cp-01"),
)

# CAF Wave 1 — editorially reviewed (2026-09-10).
_CAF_WAVE1_PACKAGES: tuple[tuple[str, str], ...] = (
    ("revision-estimators-cs1010", "cs1010-ck-r1-ar-01"),
    ("cr-2.1.2-continuous-cs1017", "cs1017-2.1.2-ar-01"),
    ("5.1.2-prior-posterior-cs1003", "cs1003-5.1.2-ar-01"),
    ("5.1.2-prior-posterior-cs1003", "cs1003-5.1.2-cp-01"),
    ("5.1.2-prior-posterior-cs1015", "cs1015-5.1.2-ar-01"),
    ("5.1.2-prior-posterior-cs1015", "cs1015-5.1.2-cp-01"),
    ("5.1.3-posterior-simple-cs1003", "cs1003-5.1.3-ar-01"),
    ("5.1.3-posterior-simple-cs1003", "cs1003-5.1.3-cp-01"),
    ("5.1.3-posterior-simple-cs1015", "cs1015-5.1.3-ar-01"),
    ("5.1.3-posterior-simple-cs1015", "cs1015-5.1.3-cp-01"),
)

# Coordinated NUM Wave 2 / CAF credibility AR items (2026-09-10).
_CREDIBILITY_WAVE_PACKAGES: tuple[tuple[str, str], ...] = (
    ("5.1.7-bayesian-credibility-cs1003", "cs1003-5.1.7-ar-01"),
    ("5.1.7-bayesian-credibility-cs1015", "cs1015-5.1.7-ar-01"),
    ("5.1.8-empirical-bayes-cs1003", "cs1003-5.1.8-ar-01"),
    ("5.1.8-empirical-bayes-cs1015", "cs1015-5.1.8-ar-01"),
)

_EXISTING_FOURTEEN_PACKAGES: tuple[tuple[str, str], ...] = (
    *_ORIGINAL_PILOT_PACKAGES,
    *_EXPANSION_PACKAGES,
)

_PRIOR_TWENTY_FOUR_PACKAGES: tuple[tuple[str, str], ...] = (
    *_EXISTING_FOURTEEN_PACKAGES,
    *_CAF_WAVE1_PACKAGES,
)

_PRIOR_TWENTY_EIGHT_PACKAGES: tuple[tuple[str, str], ...] = (
    *_PRIOR_TWENTY_FOUR_PACKAGES,
    *_CREDIBILITY_WAVE_PACKAGES,
)

# CAF Wave 3 — editorially reviewed (2026-09-10). Conflicting CPs excluded.
_CAF_WAVE3_PACKAGES: tuple[tuple[str, str], ...] = (
    ("5.1.4-loss-estimators-cs1003", "cs1003-5.1.4-ar-01"),
    ("5.1.4-loss-estimators-cs1015", "cs1015-5.1.4-ar-01"),
    ("5.1.5-credible-intervals-cs1003", "cs1003-5.1.5-ar-01"),
    ("5.1.5-credible-intervals-cs1003", "cs1003-5.1.5-cp-01"),
    ("5.1.5-credible-intervals-cs1015", "cs1015-5.1.5-ar-01"),
    ("5.1.5-credible-intervals-cs1015", "cs1015-5.1.5-cp-01"),
    ("5.1.6-credibility-premium-cs1003", "cs1003-5.1.6-ar-01"),
    ("5.1.6-credibility-premium-cs1015", "cs1015-5.1.6-ar-01"),
    ("5.1.9-bayes-vs-eb-cs1003", "cs1003-5.1.9-ar-01"),
    ("5.1.9-bayes-vs-eb-cs1003", "cs1003-5.1.9-cp-01"),
    ("5.1.9-bayes-vs-eb-cs1015", "cs1015-5.1.9-ar-01"),
    ("5.1.9-bayes-vs-eb-cs1015", "cs1015-5.1.9-cp-01"),
    ("cp-5.1.1-bayes-theorem-cs1016", "cs1016-5.1.1-ar-01"),
    ("revision-midspine-cs1003", "cs1003-cd-r3-ar-01"),
    ("revision-midspine-cs1003", "cs1003-cd-r3-cp-01"),
    ("3.1.1-method-of-moments-cs1010", "cs1010-3.1.1-ar-01"),
    ("3.1.2-maximum-likelihood-cs1010", "cs1010-3.1.2-ar-01"),
    ("3.1.5-asymptotic-mle-cs1010", "cs1010-3.1.5-ar-01"),
    ("3.1.5-asymptotic-mle-cs1010", "cs1010-3.1.5-cp-01"),
    ("3.1.6-bootstrap-estimator-cs1010", "cs1010-3.1.6-ar-01"),
    ("cp-3.1.1-estimators-cs1016", "cs1016-3.1.1-ar-01"),
    ("4.2.1-exponential-family-cs1003", "cs1003-4.2.1-ar-01"),
    ("4.2.1-exponential-family-cs1003", "cs1003-4.2.1-cp-01"),
    ("4.2.2-mean-variance-cs1003", "cs1003-4.2.2-ar-01"),
    ("4.2.2-mean-variance-cs1003", "cs1003-4.2.2-cp-01"),
    ("4.2.2-mean-variance-cs1014", "cs1014-4.2.2-ar-01"),
    ("4.2.2-mean-variance-cs1014", "cs1014-4.2.2-cp-01"),
    ("4.2.3-link-canonical-cs1003", "cs1003-4.2.3-ar-01"),
    ("4.2.3-link-canonical-cs1003", "cs1003-4.2.3-cp-01"),
    ("4.2.3-link-canonical-cs1014", "cs1014-4.2.3-ar-01"),
    ("4.2.3-link-canonical-cs1014", "cs1014-4.2.3-cp-01"),
)

_PRIOR_FIFTY_NINE_PACKAGES: tuple[tuple[str, str], ...] = (
    *_PRIOR_TWENTY_EIGHT_PACKAGES,
    *_CAF_WAVE3_PACKAGES,
)

# CAF Wave 4 — editorially reviewed (2026-09-10). Conflicting CPs excluded.
_CAF_WAVE4_PACKAGES: tuple[tuple[str, str], ...] = (
    ("4.2.4-factors-interactions-cs1003", "cs1003-4.2.4-ar-01"),
    ("4.2.4-factors-interactions-cs1003", "cs1003-4.2.4-cp-01"),
    ("4.2.4-factors-interactions-cs1014", "cs1014-4.2.4-cp-01"),
    ("4.2.4-factors-interactions-cs1014", "cs1014-4.2.4-ar-01"),
    ("4.2.5-linear-predictor-cs1003", "cs1003-4.2.5-ar-01"),
    ("4.2.5-linear-predictor-cs1014", "cs1014-4.2.5-ar-01"),
    ("4.2.6-deviance-estimation-cs1003", "cs1003-4.2.6-ar-01"),
    ("4.2.6-deviance-estimation-cs1014", "cs1014-4.2.6-ar-01"),
    ("4.2.6-deviance-estimation-cs1003", "cs1003-4.2.6-cp-01"),
    ("4.2.6-deviance-estimation-cs1014", "cs1014-4.2.6-cp-01"),
    ("4.2.7-model-choice-cs1003", "cs1003-4.2.7-ar-01"),
    ("4.2.7-model-choice-cs1014", "cs1014-4.2.7-ar-01"),
    ("4.2.7-model-choice-cs1003", "cs1003-4.2.7-cp-01"),
    ("4.2.7-model-choice-cs1014", "cs1014-4.2.7-cp-01"),
    ("4.2.8-residuals-cs1003", "cs1003-4.2.8-ar-01"),
    ("4.2.8-residuals-cs1014", "cs1014-4.2.8-ar-01"),
    ("4.2.9-goodness-tests-cs1003", "cs1003-4.2.9-ar-01"),
    ("4.2.9-goodness-tests-cs1014", "cs1014-4.2.9-ar-01"),
    ("4.2.9-goodness-tests-cs1003", "cs1003-4.2.9-cp-01"),
    ("4.2.9-goodness-tests-cs1014", "cs1014-4.2.9-cp-01"),
    ("4.2.10-fit-interpret-cs1003", "cs1003-4.2.10-ar-01"),
    ("4.2.10-fit-interpret-cs1014", "cs1014-4.2.10-ar-01"),
    ("revision-glm-cs1014", "cs1014-cx-r1-ar-01"),
    ("revision-glm-cs1014", "cs1014-cx-r1-cp-01"),
    ("revision-regression-glm-cs1003", "cs1003-cd-r2-ar-01"),
    ("revision-regression-glm-cs1003", "cs1003-cd-r2-cp-01"),
    ("2.1.1-discrete-cs1002", "cs1002-2.1a-ar-01"),
    ("2.1.1-discrete-cs1002", "cs1002-2.1a-cp-01"),
    ("2.1.2-continuous-cs1002", "cs1002-2.1b-ar-01"),
    ("2.1.2-continuous-cs1002", "cs1002-2.1b-cp-01"),
    ("2.1.3-prob-quantiles-cs1004", "cs1004-2.1c-ar-01"),
    ("2.1.4-poisson-process-cs1004", "cs1004-2.1d-ar-01"),
    ("2.1.4-poisson-process-cs1004", "cs1004-2.1d-cp-01"),
    ("2.1.5-inverse-transform-cs1004", "cs1004-2.1e-ar-01"),
    ("2.1.5-inverse-transform-cs1004", "cs1004-2.1e-cp-01"),
    ("2.1.6-software-generation-cs1004", "cs1004-2.1f-ar-01"),
    ("2.1.6-software-generation-cs1004", "cs1004-2.1f-cp-01"),
    ("cp-2.1.3-prob-quantiles-cs1016", "cs1016-2.1.3-ar-01"),
    ("cr-2.1.1-discrete-cs1017", "cs1017-2.1.1-ar-01"),
    ("cr-2.1.1-discrete-cs1017", "cs1017-2.1.1-cp-01"),
    ("revision-distributions-generation-cs1004", "cs1004-cgr1-ar-01"),
)

_PRIOR_ONE_HUNDRED_PACKAGES: tuple[tuple[str, str], ...] = (
    *_PRIOR_FIFTY_NINE_PACKAGES,
    *_CAF_WAVE4_PACKAGES,
)

# CAF Wave 5 — editorially reviewed (2026-09-10). No conflicting CPs.
_CAF_WAVE5_PACKAGES: tuple[tuple[str, str], ...] = (
    ("2.2.1-marginal-conditional-cs1005", "cs1005-2.2.1-ar-01"),
    ("2.2.2-independence-cs1005", "cs1005-2.2.2-ar-01"),
    ("2.2.2-independence-cs1005", "cs1005-2.2.2-cp-01"),
    ("2.2.3-cov-corr-expectation-cs1005", "cs1005-2.2.3-ar-01"),
    ("2.2.4-linear-combinations-cs1005", "cs1005-2.2.4-ar-01"),
    ("2.3.1-conditional-expectation-cs1006", "cs1006-2.3.1-ar-01"),
    ("2.3.2-mean-variance-conditioning-cs1006", "cs1006-2.3.2-ar-01"),
    ("cp-2.2.1-marginal-conditional-cs1016", "cs1016-2.2.1-ar-01"),
    ("revision-joint-distributions-cs1005", "cs1005-ce-r1-ar-01"),
    ("revision-joint-distributions-cs1005", "cs1005-ce-r1-cp-01"),
    ("revision-conditional-expectations-cs1006", "cs1006-cz-r1-ar-01"),
    ("revision-conditional-expectations-cs1006", "cs1006-cz-r1-cp-01"),
    ("3.2.1-confidence-interval-parameter-cs1011", "cs1011-3.2.1-ar-01"),
    ("3.2.1-confidence-interval-parameter-cs1011", "cs1011-3.2.1-cp-01"),
    ("3.2.2-prediction-interval-cs1011", "cs1011-3.2.2-ar-01"),
    ("3.2.2-prediction-interval-cs1011", "cs1011-3.2.2-cp-01"),
    ("3.2.3-ci-given-sampling-distribution-cs1011", "cs1011-3.2.3-ar-01"),
    ("3.2.3-ci-given-sampling-distribution-cs1011", "cs1011-3.2.3-cp-01"),
    ("3.2.4-ci-normal-mean-variance-cs1011", "cs1011-3.2.4-ar-01"),
    ("3.2.4-ci-normal-mean-variance-cs1011", "cs1011-3.2.4-cp-01"),
    ("3.2.5-ci-binomial-poisson-cs1011", "cs1011-3.2.5-ar-01"),
    ("3.2.5-ci-binomial-poisson-cs1011", "cs1011-3.2.5-cp-01"),
    ("3.2.6-ci-two-sample-cs1011", "cs1011-3.2.6-ar-01"),
    ("3.2.6-ci-two-sample-cs1011", "cs1011-3.2.6-cp-01"),
    ("3.2.7-ci-paired-means-cs1011", "cs1011-3.2.7-ar-01"),
    ("3.2.7-ci-paired-means-cs1011", "cs1011-3.2.7-cp-01"),
    ("3.2.8-bootstrap-confidence-interval-cs1011", "cs1011-3.2.8-ar-01"),
    ("3.2.8-bootstrap-confidence-interval-cs1011", "cs1011-3.2.8-cp-01"),
    ("3.3.1-hypothesis-concepts-cs1012", "cs1012-3.3.1-ar-01"),
    ("3.3.1-hypothesis-concepts-cs1012", "cs1012-3.3.1-cp-01"),
    ("3.3.2-basic-tests-cs1012", "cs1012-3.3.2-ar-01"),
    ("3.3.2-basic-tests-cs1012", "cs1012-3.3.2-cp-01"),
    ("3.3.3-permutation-tests-cs1012", "cs1012-3.3.3-ar-01"),
    ("3.3.3-permutation-tests-cs1012", "cs1012-3.3.3-cp-01"),
    ("3.3.4-chi-square-gof-cs1012", "cs1012-3.3.4-ar-01"),
    ("3.3.4-chi-square-gof-cs1012", "cs1012-3.3.4-cp-01"),
    ("3.3.5-contingency-independence-cs1012", "cs1012-3.3.5-ar-01"),
    ("3.3.5-contingency-independence-cs1012", "cs1012-3.3.5-cp-01"),
    ("cp-3.2.1-ci-sample-cs1016", "cs1016-3.2.1-ar-01"),
    ("cp-3.2.1-ci-sample-cs1016", "cs1016-3.2.1-cp-01"),
    ("cp-3.3.1-hypothesis-testing-cs1016", "cs1016-3.3.1-ar-01"),
    ("cp-3.3.1-hypothesis-testing-cs1016", "cs1016-3.3.1-cp-01"),
)

_PROTOTYPE_PACKAGES: tuple[tuple[str, str], ...] = (
    *_PRIOR_ONE_HUNDRED_PACKAGES,
    *_CAF_WAVE5_PACKAGES,
)

_CAF_WAVE3_CONFLICT_NUMERIC_CPS: frozenset[str] = frozenset(
    {
        "cs1016-5.1.1-cp-01",
        "cs1003-5.1.4-cp-01",
        "cs1015-5.1.4-cp-01",
        "cs1010-3.1.6-cp-01",
    }
)

_CAF_WAVE4_CONFLICT_NUMERIC_CPS: frozenset[str] = frozenset(
    {
        "cs1003-4.2.5-cp-01",
        "cs1003-4.2.8-cp-01",
    }
)

_ORIGINAL_PILOT_FEEDBACK: dict[tuple[str, str], str] = {
    (
        "cs1010-3.1.3-cp-01",
        "b",
    ): (
        "That choice treats unbiasedness as an MSE guarantee. "
        "MSE(A)=4/n while MSE(B)=1/n²+1/n≈1/n for large n, so the biased "
        "estimator can win on MSE. Unbiasedness is not optimality."
    ),
    (
        "cs1010-3.1.3-cp-01",
        "c",
    ): (
        "That choice drops Var(B) from the MSE and keeps only bias². "
        "MSE is variance plus squared bias, so MSE(B)=1/n²+1/n, not 1/n² alone."
    ),
    (
        "cs1010-3.1.3-cp-01",
        "d",
    ): (
        "That choice equates consistency with Bias=0 for every finite n. "
        "Consistency is large-sample concentration in probability; a biased "
        "estimator can still be consistent and can still beat an unbiased one "
        "on MSE."
    ),
    (
        "cs1014-4.2.1-ar-01",
        "b",
    ): (
        "That choice collapses GLM into renamed OLS. A GLM needs a named "
        "exponential-family response (and a link); package naming alone does "
        "not define the model class."
    ),
    (
        "cs1014-4.2.1-ar-01",
        "c",
    ): (
        "That choice treats Normal as the only GLM response. Poisson and "
        "binomial are standard exponential-family GLM members; Normal with "
        "identity link is a special case inside the family list, not the "
        "whole definition."
    ),
    (
        "cs1014-4.2.1-ar-01",
        "d",
    ): (
        "That choice treats any exp() in a density as exponential-family "
        "membership. Family membership is a specific exponential-family "
        "structure for named responses, not the mere presence of an "
        "exponential symbol."
    ),
    (
        "cs1017-2.1.2-cp-01",
        "b",
    ): (
        "That choice misuses the CLT to force Normal waiting times. The CLT "
        "is about sample means for large n, not a licence to ignore strictly "
        "positive, memoryless waiting-time support—which points first to "
        "exponential."
    ),
    (
        "cs1017-2.1.2-cp-01",
        "c",
    ): (
        "That choice forces a Beta model because times are 'between zero and "
        "one.' Waiting times here are unbounded positive durations under "
        "constant hazard; Beta support on (0,1) does not match that story."
    ),
    (
        "cs1017-2.1.2-cp-01",
        "d",
    ): (
        "That choice wrongly bans lognormal for every waiting-time problem "
        "and ties memorylessness to discrete data. Memoryless continuous "
        "waiting under constant hazard selects exponential first; lognormal "
        "is a different positive-support model, not ruled out by a "
        "discrete-data claim."
    ),
    (
        "cs1010-ck-r1-cp-01",
        "b",
    ): (
        "That choice adds Bias(T) without squaring. MSE is variance plus "
        "squared bias, so the bias term must be Bias(T)²."
    ),
    (
        "cs1010-ck-r1-cp-01",
        "c",
    ): (
        "That choice keeps only Bias(T)² and drops variance. An estimator's "
        "MSE always includes both Var(T) and Bias(T)²."
    ),
    (
        "cs1010-ck-r1-cp-01",
        "d",
    ): (
        "That choice sets MSE equal to variance for every estimator. That "
        "holds only when bias is zero; in general MSE = Var(T) + Bias(T)²."
    ),
}

# Frozen byte-identical copy for all 14 items live before CAF Wave 1.
_EXISTING_FOURTEEN_FEEDBACK: dict[tuple[str, str], str] = {
    **_ORIGINAL_PILOT_FEEDBACK,
    (
        "cs1003-5.1.1-ar-01",
        "b",
    ): (
        "That choice discards the prior once data arrive. Bayes forms the "
        "posterior from prior times likelihood (then normalises); the prior "
        "is not dropped after observing data."
    ),
    (
        "cs1003-5.1.1-ar-01",
        "c",
    ): (
        "That choice keeps only the prior and parks likelihood in "
        "frequentist tests. Bayes updates by multiplying prior by "
        "likelihood, then normalising."
    ),
    (
        "cs1003-5.1.1-ar-01",
        "d",
    ): (
        "That choice equates P(A given B) with P(B given A) and skips the "
        "prior-likelihood product. Those conditionals are not the same; "
        "Bayes combines prior and likelihood into a normalised posterior."
    ),
    (
        "cs1003-5.1.1-cp-01",
        "b",
    ): (
        "That choice treats positive tests and disease status as "
        "interchangeable labels. P(disease given positive) is not equal to "
        "P(positive given disease); Bayes combines base rate with "
        "likelihood."
    ),
    (
        "cs1003-5.1.1-cp-01",
        "c",
    ): (
        "That choice claims a known base rate makes the two conditionals "
        "equal. Knowing prevalence does not equate them; Bayes still "
        "multiplies prior by likelihood and normalises."
    ),
    (
        "cs1003-5.1.1-cp-01",
        "d",
    ): (
        "That choice replaces the prior with the likelihood alone and "
        "claims that equates the conditionals. Bayes keeps the prior, "
        "multiplies by likelihood, and normalises; that does not make the "
        "two conditionals equal."
    ),
    (
        "cs1015-5.1.1-ar-01",
        "b",
    ): (
        "That choice treats conditioning as symmetric and sets P(A given B) "
        "equal to P(B given A). Those conditionals are not equal; Bayes "
        "uses prior, likelihood, and evidence together."
    ),
    (
        "cs1015-5.1.1-ar-01",
        "c",
    ): (
        "That choice sets the posterior equal to the likelihood and drops "
        "the base rate. Bayes needs P(A) and the normalising evidence "
        "P(B), not likelihood alone."
    ),
    (
        "cs1015-5.1.1-ar-01",
        "d",
    ): (
        "That choice updates from the prior alone. A conditional update "
        "needs prior, likelihood, and evidence, not the prior by itself."
    ),
    (
        "cs1015-5.1.1-cp-01",
        "b",
    ): (
        "That choice sets P(fraud given flag) equal to P(flag given fraud), "
        "which is 0.90. The likelihood is not the posterior; with prior "
        "0.02, Bayes gives about 0.269 after normalising by P(flag) = 0.067."
    ),
    (
        "cs1015-5.1.1-cp-01",
        "c",
    ): (
        "That choice leaves the posterior at the prior 0.02 after a flag. "
        "Data update the prior through likelihood and evidence; the prior "
        "alone is not P(fraud given flag)."
    ),
    (
        "cs1015-5.1.1-cp-01",
        "d",
    ): (
        "That choice takes P(flag given genuine) = 0.05 as the posterior. "
        "That false-flag rate is not P(fraud given flag); Bayes multiplies "
        "prior by likelihood and divides by P(flag) = 0.067."
    ),
    (
        "cs1015-co-r1-ar-01",
        "b",
    ): (
        "That choice adds prior and likelihood and writes likelihood of "
        "theta given y. Bayes multiplies likelihood of y given theta by "
        "prior of theta; it does not add them."
    ),
    (
        "cs1015-co-r1-ar-01",
        "c",
    ): (
        "That choice drops the prior and skips normalisation. The posterior "
        "is proportional to likelihood times prior, then normalised over "
        "theta."
    ),
    (
        "cs1015-co-r1-ar-01",
        "d",
    ): (
        "That choice reverses the conditional roles, using prior of y and "
        "likelihood of theta. Posterior of theta given y uses likelihood "
        "of y given theta times prior of theta."
    ),
    (
        "cs1015-co-r1-cp-01",
        "b",
    ): (
        "That choice gives a frequentist coverage reading to a credible "
        "interval. A 95% credible interval is a posterior probability "
        "statement given the model, prior, and data, not repeated-sample "
        "coverage of a fixed theta."
    ),
    (
        "cs1015-co-r1-cp-01",
        "c",
    ): (
        "That choice treats the interval as a prediction band for future "
        "observations. The credible interval is about the parameter theta, "
        "not about where future data will fall."
    ),
    (
        "cs1015-co-r1-cp-01",
        "d",
    ): (
        "That choice claims the probability does not depend on prior or "
        "likelihood. A credible interval is defined from the posterior, "
        "which depends on both."
    ),
    (
        "cs1010-3.1.3-ar-01",
        "b",
    ): (
        "That choice sets bias equal to variance, MSE equal to absolute "
        "bias, and consistency equal to finite-n unbiasedness. Bias is the "
        "expected value of theta-hat minus theta; MSE is variance plus "
        "squared bias; consistency is large-sample concentration in "
        "probability."
    ),
    (
        "cs1010-3.1.3-ar-01",
        "c",
    ): (
        "That choice writes MSE as variance minus squared bias. MSE is "
        "variance plus squared bias; a larger bias cannot cut MSE by that "
        "subtraction."
    ),
    (
        "cs1010-3.1.3-ar-01",
        "d",
    ): (
        "That choice treats efficiency and consistency as synonyms for "
        "unbiasedness. Unbiasedness does not imply either; efficiency "
        "compares variance or MSE, and consistency is convergence in "
        "probability."
    ),
    (
        "cs1010-3.1.4-ar-01",
        "b",
    ): (
        "That choice stops at unbiasedness and skips MSE. Prefer the "
        "smaller MSE; a biased estimator can win when variance reduction "
        "outweighs squared bias."
    ),
    (
        "cs1010-3.1.4-ar-01",
        "c",
    ): (
        "That choice prefers larger bias as if it always cuts variance "
        "enough to cut MSE. Larger bias does not automatically improve "
        "MSE; compare variance plus squared bias."
    ),
    (
        "cs1010-3.1.4-ar-01",
        "d",
    ): (
        "That choice replaces MSE comparison with an asymptotic Normality "
        "check. Asymptotic Normality is a different criterion; comparison "
        "here is by MSE."
    ),
    (
        "cs1010-3.1.4-cp-01",
        "b",
    ): (
        "That choice drops squared bias from MSE of theta-hat-2 and treats "
        "the comparison as optional because theta-hat-1 is unbiased. MSE "
        "of theta-hat-2 is 0.25/n plus 0.5/n equals 0.75/n; compare full "
        "MSEs, and unbiasedness does not waive that."
    ),
    (
        "cs1010-3.1.4-cp-01",
        "c",
    ): (
        "That choice computes MSE of theta-hat-2 as 0.75/n correctly but "
        "still prefers the unbiased estimator. Smaller MSE wins; "
        "theta-hat-2 beats theta-hat-1 even though it is biased."
    ),
    (
        "cs1010-3.1.4-cp-01",
        "d",
    ): (
        "That choice squares 0.5 over root n as 0.25 over root n instead of "
        "0.25/n. Correctly, bias squared is 0.25/n so MSE of theta-hat-2 "
        "is 0.75/n, which is less than 2/n; prefer theta-hat-2."
    ),
    (
        "cs1014-4.2.1-cp-01",
        "b",
    ): (
        "That choice collapses GLM into renamed OLS. A GLM needs a named "
        "exponential-family response (and a link); package naming alone "
        "does not define the model class."
    ),
    (
        "cs1014-4.2.1-cp-01",
        "c",
    ): (
        "That choice treats Normal as the only exponential-family GLM "
        "response. Poisson and binomial are standard members; Normal is "
        "one case inside the family list, not the whole definition."
    ),
    (
        "cs1014-4.2.1-cp-01",
        "d",
    ): (
        "That choice treats any exp() in a Poisson pmf as the family "
        "definition. Family membership needs the exponential-family "
        "structure tied to the response, not the mere presence of an "
        "exponential symbol."
    ),
}


# Frozen byte-identical copy for CAF Wave 1 items (prior to credibility wave).
_CAF_WAVE1_FEEDBACK: dict[tuple[str, str], str] = {
    (
        "cs1010-ck-r1-ar-01",
        "b",
    ): (
        "That choice treats method of moments and maximum likelihood as "
        "always identical. The methods use different estimating principles "
        "and need not agree, even when they coincide in some models."
    ),
    (
        "cs1010-ck-r1-ar-01",
        "c",
    ): (
        "That choice assigns maximising the observed-sample probability to "
        "method of moments. That is the MLE principle; method of moments "
        "equates sample and model moments."
    ),
    (
        "cs1010-ck-r1-ar-01",
        "d",
    ): (
        "That choice limits maximum likelihood to the first population "
        "moment. MLE maximises the observed-data likelihood; matching the "
        "first moment alone is a moments step, not the MLE definition."
    ),
    (
        "cs1017-2.1.2-ar-01",
        "b",
    ): (
        "That choice makes Normal the default for any positive quantity. "
        "Symmetric all-real support does not match strictly positive "
        "waiting-time support; family choice follows support and shape story."
    ),
    (
        "cs1017-2.1.2-ar-01",
        "c",
    ): (
        "That choice treats Exponential and Normal as interchangeable because "
        "each has one numeric parameter. Parameter count does not equate "
        "families; memoryless waiting under constant hazard points to "
        "exponential, not Normal."
    ),
    (
        "cs1017-2.1.2-ar-01",
        "d",
    ): (
        "That choice requires a z-score transform before any continuous "
        "family applies. Continuous families model raw support directly; "
        "positive memoryless waiting under constant hazard selects "
        "exponential first."
    ),
    (
        "cs1003-5.1.2-ar-01",
        "b",
    ): (
        "That choice treats naming a conjugate pair as finishing the "
        "numerical posterior. Conjugate closure keeps the posterior in the "
        "same family; you still obtain posterior parameters from prior plus "
        "data."
    ),
    (
        "cs1003-5.1.2-ar-01",
        "c",
    ): (
        "That choice collapses prior and posterior into one object and "
        "equates conjugate with the MLE. Prior is belief before data; "
        "posterior is after; conjugate means family closure under updating, "
        "not MLE equality."
    ),
    (
        "cs1003-5.1.2-ar-01",
        "d",
    ): (
        "That choice calls any zero-to-one prior conjugate and treats closure "
        "as optional. Conjugate means the prior family stays closed under "
        "updating so the posterior remains in that family."
    ),
    (
        "cs1003-5.1.2-cp-01",
        "b",
    ): (
        "That choice treats the prior as the last observed sample. The prior "
        "is belief about theta before data; conjugate updating combines that "
        "prior with the likelihood, not a copied sample."
    ),
    (
        "cs1003-5.1.2-cp-01",
        "c",
    ): (
        "That choice treats naming Beta-Binomial as finishing the numerical "
        "posterior. Conjugate naming structures the update; you still "
        "calculate posterior parameters from prior plus data."
    ),
    (
        "cs1003-5.1.2-cp-01",
        "d",
    ): (
        "That choice makes prior and posterior identical once data arrive and "
        "equates conjugate with the MLE. Posterior updates the prior; "
        "conjugate means family closure, not MLE equality."
    ),
    (
        "cs1015-5.1.2-ar-01",
        "b",
    ): (
        "That choice treats naming a conjugate pair as finishing the "
        "numerical posterior. Conjugate closure keeps the posterior in the "
        "same family; you still obtain posterior parameters from prior plus "
        "data."
    ),
    (
        "cs1015-5.1.2-ar-01",
        "c",
    ): (
        "That choice collapses prior and posterior into one object and "
        "equates conjugate with the MLE. Prior is belief before data; "
        "posterior is after; conjugate means family closure under updating, "
        "not MLE equality."
    ),
    (
        "cs1015-5.1.2-ar-01",
        "d",
    ): (
        "That choice calls any zero-to-one prior conjugate and treats closure "
        "as optional. Conjugate means the prior family stays closed under "
        "updating so the posterior remains in that family."
    ),
    (
        "cs1015-5.1.2-cp-01",
        "b",
    ): (
        "That choice treats naming Beta-Binomial as finishing the numerical "
        "posterior. Conjugate naming structures the update; you still "
        "calculate posterior parameters from prior plus data."
    ),
    (
        "cs1015-5.1.2-cp-01",
        "c",
    ): (
        "That choice sets the prior equal to the sample mean and leaves the "
        "posterior unchanged under conjugate updating. Conjugate updating "
        "revises parameters with the data; prior and posterior are distinct "
        "stages."
    ),
    (
        "cs1015-5.1.2-cp-01",
        "d",
    ): (
        "That choice keeps prior and likelihood as objects that never "
        "combine. Bayes forms the posterior from prior times likelihood, then "
        "normalises; conjugate pairs still combine."
    ),
    (
        "cs1003-5.1.3-ar-01",
        "b",
    ): (
        "That choice treats having the posterior as finishing the "
        "squared-error point estimator. The posterior is the updated "
        "distribution; a loss-based point estimate is a further summary under "
        "a chosen loss."
    ),
    (
        "cs1003-5.1.3-ar-01",
        "c",
    ): (
        "That choice sets the simple posterior equal to the prior alone. "
        "Posterior comes from prior and likelihood together; likelihood is "
        "not reserved for frequentist intervals."
    ),
    (
        "cs1003-5.1.3-ar-01",
        "d",
    ): (
        "That choice replaces the posterior distribution with a credible "
        "interval as the only output. Intervals are summaries of the "
        "posterior; the primary object is the full posterior distribution."
    ),
    (
        "cs1003-5.1.3-cp-01",
        "b",
    ): (
        "That choice treats Bayesian as a slogan and skips the posterior once "
        "Beta(2,2) is named. With Binomial n=10 and x=3, the conjugate update "
        "is Beta(5,9); Bayesian work needs that posterior distribution."
    ),
    (
        "cs1003-5.1.3-cp-01",
        "c",
    ): (
        "That choice leaves the posterior at Beta(2,2) as if n=10 were too "
        "small to update. Successes and failures revise the shapes: Beta(2+3, "
        "2+7) = Beta(5,9)."
    ),
    (
        "cs1003-5.1.3-cp-01",
        "d",
    ): (
        "That choice treats having Beta(5,9) as finishing the squared-error "
        "point estimator. Beta(5,9) is the posterior distribution; a "
        "loss-based point estimate is a further step."
    ),
    (
        "cs1015-5.1.3-ar-01",
        "b",
    ): (
        "That choice treats having the posterior as finishing the "
        "squared-error point estimator. The posterior is the updated "
        "distribution; a loss-based point estimate is a further summary under "
        "a chosen loss."
    ),
    (
        "cs1015-5.1.3-ar-01",
        "c",
    ): (
        "That choice sets the simple posterior equal to the prior alone. "
        "Posterior comes from prior and likelihood together; likelihood is "
        "not reserved for frequentist intervals."
    ),
    (
        "cs1015-5.1.3-ar-01",
        "d",
    ): (
        "That choice replaces the posterior distribution with a credible "
        "interval as the only output. Intervals are summaries of the "
        "posterior; the primary object is the full posterior distribution."
    ),
    (
        "cs1015-5.1.3-cp-01",
        "b",
    ): (
        "That choice leaves the posterior at Beta(2,2) as if n=10 were too "
        "small to update. Successes and failures revise the shapes: Beta(2+3, "
        "2+7) = Beta(5,9)."
    ),
    (
        "cs1015-5.1.3-cp-01",
        "c",
    ): (
        "That choice treats the sample proportion three-tenths as the "
        "posterior distribution. The conjugate posterior is Beta(5,9); that "
        "ratio is a point summary, not the full posterior."
    ),
    (
        "cs1015-5.1.3-cp-01",
        "d",
    ): (
        "That choice treats having Beta(5,9) as finishing the squared-error "
        "point estimator. Beta(5,9) is the posterior distribution; a "
        "loss-based point estimate is a further step."
    ),
}

_PRIOR_TWENTY_FOUR_FEEDBACK: dict[tuple[str, str], str] = {
    **_EXISTING_FOURTEEN_FEEDBACK,
    **_CAF_WAVE1_FEEDBACK,
}

# Approved copy for the four credibility-wave AR items.
_CREDIBILITY_WAVE_FEEDBACK: dict[tuple[str, str], str] = {
    (
        "cs1003-5.1.7-ar-01",
        "b",
    ): (
        "That choice treats the blend formula as Bayesian credibility by "
        "itself. Bayesian credibility needs a prior or structural story that "
        "warrants mu and Z, then the premium."
    ),
    (
        "cs1003-5.1.7-ar-01",
        "c",
    ): (
        "That choice collapses Bayesian credibility into finishing Empirical "
        "Bayes. A shared numeric premium does not make the approaches the "
        "same; Bayes treats structurals as known from the prior, EB estimates "
        "them from data."
    ),
    (
        "cs1003-5.1.7-ar-01",
        "d",
    ): (
        "That choice forces full credibility and parks the prior in Empirical "
        "Bayes alone. In simple Bayesian credibility the prior structure "
        "supplies mu and Z; Z need not be 1."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "b",
    ): (
        "That choice treats a shared numeric premium as finishing Empirical "
        "Bayes. Bayesian credibility and Empirical Bayes differ in how "
        "structural parameters are obtained, even when both produce a "
        "premium."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "c",
    ): (
        "That choice reserves mu and Z for Empirical Bayes alone. In simple "
        "Bayesian credibility the prior or structural distribution supplies "
        "mu and Z theoretically."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "d",
    ): (
        "That choice drops the credibility premium form. In simple cases the "
        "premium object is Z times X-bar plus one minus Z times mu, with Z "
        "and mu from the prior structure."
    ),
    (
        "cs1003-5.1.8-ar-01",
        "b",
    ): (
        "That choice equates Empirical Bayes with a fully specified Bayesian "
        "prior. EB estimates structurals from collective data; full Bayes "
        "treats them as given by the prior."
    ),
    (
        "cs1003-5.1.8-ar-01",
        "c",
    ): (
        "That choice reduces Empirical Bayes to a single-claim Bayes update. "
        "EB uses collective experience to estimate structurals before forming "
        "the credibility premium."
    ),
    (
        "cs1003-5.1.8-ar-01",
        "d",
    ): (
        "That choice forces Z equal to one whenever data appear. EB still "
        "forms Z-hat as n over n plus k-hat, and the blend Z-hat times X-bar "
        "plus one minus Z-hat times mu-hat; full credibility is not "
        "automatic."
    ),
    (
        "cs1015-5.1.8-ar-01",
        "b",
    ): (
        "That choice equates Empirical Bayes with a fully specified Bayesian "
        "prior. EB estimates structurals from collective data; full Bayes "
        "treats them as given by the prior."
    ),
    (
        "cs1015-5.1.8-ar-01",
        "c",
    ): (
        "That choice reduces Empirical Bayes to a single-claim Bayes update. "
        "EB uses collective experience to estimate structurals before forming "
        "the credibility premium."
    ),
    (
        "cs1015-5.1.8-ar-01",
        "d",
    ): (
        "That choice forces Z equal to one whenever data appear. EB still "
        "forms Z-hat as n over n plus k-hat, and the blend Z-hat times X-bar "
        "plus one minus Z-hat times mu-hat; full credibility is not "
        "automatic."
    ),
}


_PRIOR_TWENTY_EIGHT_FEEDBACK: dict[tuple[str, str], str] = {
    **_PRIOR_TWENTY_FOUR_FEEDBACK,
    **_CREDIBILITY_WAVE_FEEDBACK,
}

_CAF_WAVE3_FEEDBACK: dict[tuple[str, str], str] = {
    (
        "cs1003-5.1.4-ar-01",
        "b",
    ): (
        "That choice treats the loss-based point estimator as the same object as a credible interval. "
        "A point estimator is a single posterior summary under a loss; a credible interval is a posterior probability set for theta."
    ),
    (
        "cs1003-5.1.4-ar-01",
        "c",
    ): (
        "That choice swaps the loss pairings. "
        "Squared-error loss justifies the posterior mean; absolute-error loss justifies the posterior median."
    ),
    (
        "cs1003-5.1.4-ar-01",
        "d",
    ): (
        "That choice forces every loss-based Bayes estimator to equal the MLE. "
        "The Bayes point estimate is a posterior summary under a chosen loss, not automatically the maximum-likelihood value."
    ),
    (
        "cs1015-5.1.4-ar-01",
        "b",
    ): (
        "That choice treats the loss-based point estimator as the same object as a credible interval. "
        "A point estimator is a single posterior summary under a loss; a credible interval is a posterior probability set for theta."
    ),
    (
        "cs1015-5.1.4-ar-01",
        "c",
    ): (
        "That choice swaps the loss pairings. "
        "Squared-error loss justifies the posterior mean; absolute-error loss justifies the posterior median."
    ),
    (
        "cs1015-5.1.4-ar-01",
        "d",
    ): (
        "That choice forces every loss-based Bayes estimator to equal the MLE. "
        "The Bayes point estimate is a posterior summary under a chosen loss, not automatically the maximum-likelihood value."
    ),
    (
        "cs1003-5.1.5-ar-01",
        "b",
    ): (
        "That choice copies the frequentist repeated-sampling coverage slogan onto the credible interval. "
        "A credible interval is a posterior probability statement that the parameter lies in the interval."
    ),
    (
        "cs1003-5.1.5-ar-01",
        "c",
    ): (
        "That choice reads the interval as covering 95% of the sample observations. "
        "The claim is about the parameter under the posterior, not about sample coverage."
    ),
    (
        "cs1003-5.1.5-ar-01",
        "d",
    ): (
        "That choice equates a 95% credible interval with the posterior mean equalling 0.95. "
        "The 95% is a posterior probability for an interval containing the parameter, not a value of the mean."
    ),
    (
        "cs1003-5.1.5-cp-01",
        "b",
    ): (
        "That choice accepts identical probability readings for credible and confidence intervals. "
        "Credible intervals are posterior probability statements about the parameter; confidence intervals have a different frequentist coverage reading."
    ),
    (
        "cs1003-5.1.5-cp-01",
        "c",
    ): (
        "That choice refuses credible intervals entirely because only frequentist coverage language is allowed. "
        "Bayesian posterior probability statements about the parameter are a valid distinct reading."
    ),
    (
        "cs1003-5.1.5-cp-01",
        "d",
    ): (
        "That choice treats the difference as notation only once an interval is computed. "
        "Posterior probability for the parameter and frequentist coverage over repeated samples remain different claims."
    ),
    (
        "cs1015-5.1.5-ar-01",
        "b",
    ): (
        "That choice gives only the frequentist repeated-sampling coverage reading. "
        "A credible interval is a posterior probability statement about theta given the observed data."
    ),
    (
        "cs1015-5.1.5-ar-01",
        "c",
    ): (
        "That choice builds credible intervals from the prior alone. "
        "The interval comes from the posterior, which already combines prior and likelihood."
    ),
    (
        "cs1015-5.1.5-ar-01",
        "d",
    ): (
        "That choice treats credible and confidence as interchangeable adjectives with the same reading. "
        "The objects answer different probability questions and must not be collapsed."
    ),
    (
        "cs1015-5.1.5-cp-01",
        "b",
    ): (
        "That choice collapses the interval to the single point (0.10, 0.10). "
        "The posterior is Normal with positive sd 0.02, so an equal-tailed 95% interval has positive width about (0.0608, 0.1392)."
    ),
    (
        "cs1015-5.1.5-cp-01",
        "c",
    ): (
        "That choice uses plus or minus one posterior standard deviation as if that were always the 95% equal-tailed rule. "
        "For this Normal posterior, 95% equal-tailed uses about 1.96 sd, giving roughly (0.0608, 0.1392), not (0.08, 0.12)."
    ),
    (
        "cs1015-5.1.5-cp-01",
        "d",
    ): (
        "That choice substitutes the frequentist repeated-sampling coverage slogan. "
        "A credible interval is a posterior probability statement about theta given the data."
    ),
    (
        "cs1003-5.1.6-ar-01",
        "b",
    ): (
        "That choice always forces full credibility Z = 1. "
        "Z depends on how much individual experience is available relative to collateral information; it need not be 1."
    ),
    (
        "cs1003-5.1.6-ar-01",
        "c",
    ): (
        "That choice puts Z on the collateral mean and (1-Z) on individual experience. "
        "In the standard blend, Z weights the individual mean X-bar and (1-Z) weights the collateral mean mu."
    ),
    (
        "cs1003-5.1.6-ar-01",
        "d",
    ): (
        "That choice sets the premium to mu alone. "
        "Credibility blends individual experience with collateral information unless Z is actually 0."
    ),
    (
        "cs1015-5.1.6-ar-01",
        "b",
    ): (
        "That choice always forces full credibility Z = 1. "
        "Z depends on how much individual experience is available relative to collateral information; it need not be 1."
    ),
    (
        "cs1015-5.1.6-ar-01",
        "c",
    ): (
        "That choice puts Z on the collateral mean and (1-Z) on individual experience. "
        "In the standard blend, Z weights the individual mean X-bar and (1-Z) weights the collateral mean mu."
    ),
    (
        "cs1015-5.1.6-ar-01",
        "d",
    ): (
        "That choice sets the premium to mu alone. "
        "Credibility blends individual experience with collateral information unless Z is actually 0."
    ),
    (
        "cs1003-5.1.9-ar-01",
        "b",
    ): (
        "That choice treats fully Bayesian credibility and Empirical Bayes as identical methods that must agree on premiums. "
        "They differ in how structural parameters enter, and premiums can differ."
    ),
    (
        "cs1003-5.1.9-ar-01",
        "c",
    ): (
        "That choice reverses the roles. "
        "Fully Bayesian specifies structural or prior parameters in a prior model; Empirical Bayes estimates those structurals from collective data."
    ),
    (
        "cs1003-5.1.9-ar-01",
        "d",
    ): (
        "That choice blames only software rounding for premium differences. "
        "The methods make different structural assumptions, so premiums need not agree even with identical arithmetic precision."
    ),
    (
        "cs1003-5.1.9-cp-01",
        "b",
    ): (
        "That choice calls the methods identical because both can return a credibility premium. "
        "Sharing a premium formula shape does not erase the different structural-input assumptions."
    ),
    (
        "cs1003-5.1.9-cp-01",
        "c",
    ): (
        "That choice treats stating the contrast as finishing every posterior, interval, and premium calculation. "
        "Naming how structurals enter is not a substitute for those later steps."
    ),
    (
        "cs1003-5.1.9-cp-01",
        "d",
    ): (
        "That choice reverses who specifies structure. "
        "Fully Bayesian specifies structurals in a prior model; Empirical Bayes estimates them from collective data."
    ),
    (
        "cs1015-5.1.9-ar-01",
        "b",
    ): (
        "That choice treats Bayesian and Empirical Bayes as the same method with different names. "
        "They differ in how structural knowledge enters, so premiums need not always agree."
    ),
    (
        "cs1015-5.1.9-ar-01",
        "c",
    ): (
        "That choice attributes premium differences only to software packages. "
        "Assumptions about structural parameters differ; that alone can change the premium."
    ),
    (
        "cs1015-5.1.9-ar-01",
        "d",
    ): (
        "That choice reverses the roles. "
        "Fully Bayesian uses specified prior structure; Empirical Bayes estimates structurals from collective data."
    ),
    (
        "cs1015-5.1.9-cp-01",
        "b",
    ): (
        "That choice collapses Bayesian and Empirical Bayes into one method. "
        "They differ in whether structurals are specified in a prior or estimated from collective data."
    ),
    (
        "cs1015-5.1.9-cp-01",
        "c",
    ): (
        "That choice treats the contrast as finishing every prior, posterior, loss, and premium calculation. "
        "Contrasting assumptions does not replace those separate calculations."
    ),
    (
        "cs1015-5.1.9-cp-01",
        "d",
    ): (
        "That choice reverses who specifies structure. "
        "Bayesian specifies structurals in a prior model; Empirical Bayes estimates them from collective data."
    ),
    (
        "cs1016-5.1.1-ar-01",
        "b",
    ): (
        "That choice treats conditioning as symmetric and sets P(A given B) equal to P(B given A). "
        "Those conditionals are not equal; Bayes uses prior, likelihood, and evidence together."
    ),
    (
        "cs1016-5.1.1-ar-01",
        "c",
    ): (
        "That choice sets the posterior equal to the likelihood and drops the base rate. "
        "Bayes needs P(A) and the normalising evidence P(B), not likelihood alone."
    ),
    (
        "cs1016-5.1.1-ar-01",
        "d",
    ): (
        "That choice updates from the prior alone. "
        "A conditional update needs prior, likelihood, and evidence, not the prior by itself."
    ),
    (
        "cs1003-cd-r3-ar-01",
        "b",
    ): (
        "That choice says Empirical Bayes never uses a prior. "
        "Empirical Bayes still uses a prior structure; it estimates some hyperparameters from data rather than giving them full hyperpriors."
    ),
    (
        "cs1003-cd-r3-ar-01",
        "c",
    ): (
        "That choice defines fully Bayesian inference as estimating every prior parameter by maximum likelihood from the same data. "
        "That plug-in pattern is Empirical Bayes; full Bayes puts distributions on the hyperparameters."
    ),
    (
        "cs1003-cd-r3-ar-01",
        "d",
    ): (
        "That choice claims identical posterior uncertainty under both approaches. "
        "Plugging in estimated hyperparameters typically understates uncertainty relative to a full Bayesian hyperprior treatment."
    ),
    (
        "cs1003-cd-r3-cp-01",
        "b",
    ): (
        "That choice updates to Beta(alpha+n, beta+x). "
        "Conjugacy adds the success count x to alpha and the failure count n-x to beta, giving Beta(alpha+x, beta+n-x)."
    ),
    (
        "cs1003-cd-r3-cp-01",
        "c",
    ): (
        "That choice keeps a Binomial posterior in n and theta. "
        "With a Beta prior and binomial likelihood, the posterior stays Beta, not Binomial."
    ),
    (
        "cs1003-cd-r3-cp-01",
        "d",
    ): (
        "That choice adds x to both Beta shapes. "
        "Failures n-x must update beta; adding successes twice omits the failure contribution."
    ),
    (
        "cs1010-3.1.1-ar-01",
        "b",
    ): (
        "That choice calls any closed-form estimator a method-of-moments estimator. "
        "MoM specifically equates sample moments to population moments and solves for the parameter."
    ),
    (
        "cs1010-3.1.1-ar-01",
        "c",
    ): (
        "That choice maximises the likelihood and calls that method of moments. "
        "Maximising the likelihood is MLE; MoM matches moments instead."
    ),
    (
        "cs1010-3.1.1-ar-01",
        "d",
    ): (
        "That choice takes an interval midpoint as the MoM estimator. "
        "MoM constructs a point estimator by matching moments, not by building an interval."
    ),
    (
        "cs1010-3.1.2-ar-01",
        "b",
    ): (
        "That choice defines maximum likelihood as equating the first sample and population moments. "
        "That is a moments step; MLE maximises the likelihood (or log-likelihood)."
    ),
    (
        "cs1010-3.1.2-ar-01",
        "c",
    ): (
        "That choice treats existence of a MoM estimator as finishing the MLE by definition. "
        "The constructions differ even when numerical answers sometimes coincide."
    ),
    (
        "cs1010-3.1.2-ar-01",
        "d",
    ): (
        "That choice defines MLE as minimising MSE among unbiased estimators. "
        "That is an optimality criterion, not the MLE definition."
    ),
    (
        "cs1010-3.1.5-ar-01",
        "b",
    ): (
        "That choice says large-sample MLEs are exactly MoM estimators, so no distributional result is needed. "
        "Asymptotic MLE theory gives an approximate Normal law with information-based variance, not MoM identity."
    ),
    (
        "cs1010-3.1.5-ar-01",
        "c",
    ): (
        "That choice gives the MLE a chi-square law with n degrees of freedom. "
        "Under regularity the large-sample law is Normal about the true parameter with variance tied to Fisher information."
    ),
    (
        "cs1010-3.1.5-ar-01",
        "d",
    ): (
        "That choice equates asymptotic MLE theory with bootstrap resampling. "
        "Bootstrap redraws the sample to estimate properties; it is a different tool from the information-based Normal limit."
    ),
    (
        "cs1010-3.1.5-cp-01",
        "b",
    ): (
        "That choice reads Var(theta-hat_n) = I(theta) exactly for every finite n. "
        "The result is a large-sample approximation: variance is about 1/(n I(theta))."
    ),
    (
        "cs1010-3.1.5-cp-01",
        "c",
    ): (
        "That choice discards the asymptotic Normal MLE result whenever bootstrap is available. "
        "Bootstrap is a different estimation tool; it does not erase the asymptotic claim."
    ),
    (
        "cs1010-3.1.5-cp-01",
        "d",
    ): (
        "That choice drops the sqrt(n) scaling and sends theta-hat_n itself to N(0, 1/I(theta)). "
        "The limit applies to the sqrt(n)-scaled error, so the variance of theta-hat_n is about 1/(n I(theta))."
    ),
    (
        "cs1010-3.1.6-ar-01",
        "b",
    ): (
        "That choice replaces the estimator by its asymptotic Normal approximation and calls that bootstrap. "
        "Bootstrap resamples, recomputes the estimator, and summarises replicates."
    ),
    (
        "cs1010-3.1.6-ar-01",
        "c",
    ): (
        "That choice collapses estimating an estimator's standard error into building a percentile confidence interval. "
        "Both use bootstrap replicates, but SE estimation and CI construction are different learning objectives."
    ),
    (
        "cs1010-3.1.6-ar-01",
        "d",
    ): (
        "That choice draws one replicate and reports it as the property estimate. "
        "Property estimation needs many replicates and a summary such as an empirical standard deviation."
    ),
    (
        "cs1016-3.1.1-ar-01",
        "b",
    ): (
        "That choice maximises the likelihood and calls the maximiser method of moments. "
        "MoM matches sample moments to population moments; MLE is a different construction."
    ),
    (
        "cs1016-3.1.1-ar-01",
        "c",
    ): (
        "That choice treats a confidence interval as the MoM estimator. "
        "MoM builds a point estimator by matching moments, not an interval."
    ),
    (
        "cs1016-3.1.1-ar-01",
        "d",
    ): (
        "That choice treats any convenient closed form as MoM. "
        "Method of moments means deriving the estimator by equating moments, not merely having a formula."
    ),
    (
        "cs1003-4.2.1-ar-01",
        "b",
    ): (
        "That choice collapses GLM into renamed OLS. "
        "A GLM needs a named exponential-family response (and a link); package naming alone does not define the model class."
    ),
    (
        "cs1003-4.2.1-ar-01",
        "c",
    ): (
        "That choice treats Normal as the only GLM response. "
        "Poisson and binomial are standard exponential-family GLM members; Normal with identity link is a special case inside the family list, not the whole definition."
    ),
    (
        "cs1003-4.2.1-ar-01",
        "d",
    ): (
        "That choice treats any exp() in a density as exponential-family membership. "
        "Family membership is a specific exponential-family structure for named responses, not the mere presence of an exponential symbol."
    ),
    (
        "cs1003-4.2.1-cp-01",
        "b",
    ): (
        "That choice collapses GLM into renamed OLS. "
        "A GLM needs a named exponential-family response (and a link); package naming alone does not define the model class."
    ),
    (
        "cs1003-4.2.1-cp-01",
        "c",
    ): (
        "That choice treats Normal as the only exponential-family GLM response. "
        "Poisson and binomial are standard members; Normal is one case inside the family list, not the whole definition."
    ),
    (
        "cs1003-4.2.1-cp-01",
        "d",
    ): (
        "That choice treats any exp() in a Poisson pmf as the family definition. "
        "Family membership needs the exponential-family structure tied to the response, not the mere presence of an exponential symbol."
    ),
    (
        "cs1003-4.2.2-ar-01",
        "b",
    ): (
        "That choice treats choosing the logit link as finishing mean, variance, variance function, and scale. "
        "Those quantities come from the response family; the link maps mu to eta and is a separate object."
    ),
    (
        "cs1003-4.2.2-ar-01",
        "c",
    ): (
        "That choice forces Var[Y] = sigma^2 with V(mu) = 1 for every GLM response. "
        "Poisson has V(mu) = mu; constant variance is the Normal case, not a universal GLM rule."
    ),
    (
        "cs1003-4.2.2-ar-01",
        "d",
    ): (
        "That choice postpones mean and variance until eta is written. "
        "Family mean-variance structure is primary; the linear predictor comes after the response family is named."
    ),
    (
        "cs1003-4.2.2-cp-01",
        "b",
    ): (
        "That choice treats choosing the logit link as finishing E[Y], Var[Y], V(mu), and scale for Poisson and Normal. "
        "Link choice does not replace those family facts."
    ),
    (
        "cs1003-4.2.2-cp-01",
        "c",
    ): (
        "That choice swaps the variance stories: Poisson with constant sigma^2 and Normal with Var[Y] = mu. "
        "Poisson has mean-variance equality; Normal has constant variance with scale sigma^2."
    ),
    (
        "cs1003-4.2.2-cp-01",
        "d",
    ): (
        "That choice sets V(mu) = mu for every exponential-family response. "
        "Normal uses V(mu) = 1 with scale sigma^2; that is not the Poisson variance function."
    ),
    (
        "cs1014-4.2.2-ar-01",
        "b",
    ): (
        "That choice treats choosing the logit link as finishing mean, variance, variance function, and scale. "
        "Those quantities come from the response family; the link maps mu to eta and is a separate object."
    ),
    (
        "cs1014-4.2.2-ar-01",
        "c",
    ): (
        "That choice forces Var[Y] = sigma^2 with V(mu) = 1 for every GLM response. "
        "Poisson has V(mu) = mu; constant variance is the Normal case, not a universal GLM rule."
    ),
    (
        "cs1014-4.2.2-ar-01",
        "d",
    ): (
        "That choice postpones mean and variance until eta is written. "
        "Family mean-variance structure is primary; the linear predictor comes after the response family is named."
    ),
    (
        "cs1014-4.2.2-cp-01",
        "b",
    ): (
        "That choice treats choosing the logit link as finishing E[Y], Var[Y], V(mu), and scale for Poisson and Normal. "
        "Link choice does not replace those family facts."
    ),
    (
        "cs1014-4.2.2-cp-01",
        "c",
    ): (
        "That choice swaps the variance stories: Poisson with constant sigma^2 and Normal with Var[Y] = mu. "
        "Poisson has mean-variance equality; Normal has constant variance with scale sigma^2."
    ),
    (
        "cs1014-4.2.2-cp-01",
        "d",
    ): (
        "That choice sets V(mu) = mu for every exponential-family response. "
        "Normal uses V(mu) = 1 with scale sigma^2; that is not the Poisson variance function."
    ),
    (
        "cs1003-4.2.3-ar-01",
        "b",
    ): (
        "That choice treats eta and the link as the same object. "
        "The link g is the map from mu to eta; eta = X beta is the linear predictor, a distinct structural piece."
    ),
    (
        "cs1003-4.2.3-ar-01",
        "c",
    ): (
        "That choice lets the link replace the exponential-family response and discards eta once a family is named. "
        "A GLM still needs the named family, eta, and g(mu) = eta together."
    ),
    (
        "cs1003-4.2.3-ar-01",
        "d",
    ): (
        "That choice restricts GLMs to Normal with identity and no separate link idea. "
        "Non-Normal exponential-family responses with nontrivial links are standard GLM members."
    ),
    (
        "cs1003-4.2.3-cp-01",
        "b",
    ): (
        "That choice calls any software default automatically canonical for any family. "
        "Canonical means the family link that equates eta with the natural parameter, warranted by mean range."
    ),
    (
        "cs1003-4.2.3-cp-01",
        "c",
    ): (
        "That choice assigns logit as Poisson's canonical link because counts look like probabilities. "
        "Poisson means are positive; the canonical link is log, mapping (0, infinity) to the reals."
    ),
    (
        "cs1003-4.2.3-cp-01",
        "d",
    ): (
        "That choice takes identity as binomial's canonical link. "
        "Probabilities in (0,1) need a map such as logit onto the real line for eta; identity does not match that mean-range warrant."
    ),
    (
        "cs1014-4.2.3-ar-01",
        "b",
    ): (
        "That choice treats the software default link as automatically canonical. "
        "Canonical is the family-specific natural-parameter link; a default still needs that warrant."
    ),
    (
        "cs1014-4.2.3-ar-01",
        "c",
    ): (
        "That choice makes identity canonical for every family. "
        "Binomial's canonical link is logit and Poisson's is log; identity is not universal."
    ),
    (
        "cs1014-4.2.3-ar-01",
        "d",
    ): (
        "That choice equates the link function with the linear predictor eta. "
        "The link maps mu to eta; eta = X beta is the predictor, not the link itself."
    ),
    (
        "cs1014-4.2.3-cp-01",
        "b",
    ): (
        "That choice takes software defaults (binomial identity, gamma log) as canonical by definition. "
        "Canonical links are family definitions tied to mean range, not GUI defaults."
    ),
    (
        "cs1014-4.2.3-cp-01",
        "c",
    ): (
        "That choice gives both binomial and gamma the logit link. "
        "Logit matches binomial means in (0,1); gamma's canonical form is reciprocal for a positive mean."
    ),
    (
        "cs1014-4.2.3-cp-01",
        "d",
    ): (
        "That choice lets in-sample deviance minimisation define the canonical link. "
        "Canonical is a family property equating eta with the natural parameter, not an empirical fit choice."
    ),
}

_PRIOR_FIFTY_NINE_FEEDBACK: dict[tuple[str, str], str] = {
    **_PRIOR_TWENTY_EIGHT_FEEDBACK,
    **_CAF_WAVE3_FEEDBACK,
}

_CAF_WAVE4_FEEDBACK: dict[tuple[str, str], str] = {
    (
        "cs1003-4.2.4-ar-01",
        "b",
    ): (
        "That choice swaps the examples: region North/South is categorical, while age in years is continuous. "
        "An interaction is still useful when one covariate’s effect depends on the level of another, beyond additive main effects."
    ),
    (
        "cs1003-4.2.4-ar-01",
        "c",
    ): (
        "That choice treats continuous and factor predictors as the same object and reduces an interaction to another main-effect slope. "
        "A factor uses level coding, and an interaction lets a continuous slope change by level."
    ),
    (
        "cs1003-4.2.4-ar-01",
        "d",
    ): (
        "That choice claims factors apply only outside GLMs and that the linear predictor uses only continuous covariates. "
        "GLMs routinely include factor indicators alongside continuous terms."
    ),
    (
        "cs1003-4.2.4-cp-01",
        "b",
    ): (
        "That choice stops at eta = beta0 + beta1 x and treats knowing the region as finishing the model. "
        "You still need a factor indicator so region enters the linear predictor."
    ),
    (
        "cs1003-4.2.4-cp-01",
        "c",
    ): (
        "That choice keeps only a South main-effect shift and treats that constant shift as the interaction. "
        "An age-by-region interaction changes the age slope by region, not just a level shift."
    ),
    (
        "cs1003-4.2.4-cp-01",
        "d",
    ): (
        "That choice codes region as numeric 1/2 on the same slope as age. "
        "Region should enter as a factor indicator, with an interaction if the age effect may differ by region."
    ),
    (
        "cs1014-4.2.4-cp-01",
        "b",
    ): (
        "That choice stops at eta = beta0 + beta1 x and treats knowing the region as finishing the model. "
        "You still need a factor indicator so region enters the linear predictor."
    ),
    (
        "cs1014-4.2.4-cp-01",
        "c",
    ): (
        "That choice keeps only a South main-effect shift and treats that constant shift as the interaction. "
        "An age-by-region interaction changes the age slope by region, not just a level shift."
    ),
    (
        "cs1014-4.2.4-cp-01",
        "d",
    ): (
        "That choice codes region as numeric 1/2 on the same slope as age. "
        "Region should enter as a factor indicator, with an interaction if the age effect may differ by region."
    ),
    (
        "cs1014-4.2.4-ar-01",
        "b",
    ): (
        "That choice treats an interaction as just another main-effect slope that never changes slope by level. "
        "An interaction lets the effect of one covariate depend on the level of another."
    ),
    (
        "cs1014-4.2.4-ar-01",
        "c",
    ): (
        "That choice restricts factors to non-GLM settings and says GLMs use only continuous covariates. "
        "Factor level coding belongs in the GLM linear predictor whenever categories matter."
    ),
    (
        "cs1014-4.2.4-ar-01",
        "d",
    ): (
        "That choice uses eta = beta0 + beta1 x with no factor indicators and claims that fully explains categorical region. "
        "Categorical region needs indicator coding in eta."
    ),
    (
        "cs1003-4.2.5-ar-01",
        "b",
    ): (
        "That choice writes every case as eta = beta0 alone and leaves factors and polynomials to the link. "
        "Simple slope, baseline factor coding, and a quadratic all live in the linear predictor through terms in eta."
    ),
    (
        "cs1003-4.2.5-ar-01",
        "c",
    ): (
        "That choice forces a two-level factor into a multiplicative link term and writes a quadratic without coefficients. "
        "The factor enters eta via level coding, and a quadratic needs explicit beta terms on the powers of x."
    ),
    (
        "cs1003-4.2.5-ar-01",
        "d",
    ): (
        "That choice bans quadratic terms and claims factor coding removes beta0. "
        "Polynomials are allowed in eta, and an intercept remains unless you deliberately omit it."
    ),
    (
        "cs1014-4.2.5-ar-01",
        "b",
    ): (
        "That choice equates the link function with the linear predictor because g(mu) = eta. "
        "The equation relates them: the link is the function g, while eta is the linear predictor X beta."
    ),
    (
        "cs1014-4.2.5-ar-01",
        "c",
    ): (
        "That choice sets eta equal to mu for every GLM and drops the link. "
        "In general eta = g(mu), and eta = mu only for the identity link."
    ),
    (
        "cs1014-4.2.5-ar-01",
        "d",
    ): (
        "That choice allows polynomial terms only in Normal linear models and forbids x squared in a Poisson eta. "
        "Polynomials may enter any GLM linear predictor when the mean structure needs them."
    ),
    (
        "cs1003-4.2.6-ar-01",
        "b",
    ): (
        "That choice defines deviance by deleting insignificant terms until p-values look nice. "
        "Deviance compares log-likelihoods of fitted models; estimation is maximum likelihood, not p-value chopping."
    ),
    (
        "cs1003-4.2.6-ar-01",
        "c",
    ): (
        "That choice equates deviance with the sum of Pearson residuals and treats scaled deviance as unchanged without a scale divisor. "
        "Deviance comes from a likelihood ratio, and scaled deviance divides by dispersion when that is part of the definition."
    ),
    (
        "cs1003-4.2.6-ar-01",
        "d",
    ): (
        "That choice says GLMs are estimated by moment matching with deviance only as a display label. "
        "GLM coefficients are estimated by maximum likelihood; deviance is a likelihood-based fit measure."
    ),
    (
        "cs1014-4.2.6-ar-01",
        "b",
    ): (
        "That choice defines deviance by deleting insignificant terms until p-values look nice. "
        "Deviance compares log-likelihoods of fitted models; estimation is maximum likelihood, not p-value chopping."
    ),
    (
        "cs1014-4.2.6-ar-01",
        "c",
    ): (
        "That choice equates deviance with the sum of Pearson residuals and treats scaled deviance as unchanged without a scale divisor. "
        "Deviance comes from a likelihood ratio, and scaled deviance divides by dispersion when that is part of the definition."
    ),
    (
        "cs1014-4.2.6-ar-01",
        "d",
    ): (
        "That choice says GLMs are estimated by moment matching with deviance only as a display label. "
        "GLM coefficients are estimated by maximum likelihood; deviance is a likelihood-based fit measure."
    ),
    (
        "cs1003-4.2.6-cp-01",
        "b",
    ): (
        "That choice defines deviance as an AIC difference, scaled deviance as AIC over n, and estimation as dropping p greater than 0.10. "
        "Deviance is a likelihood-ratio measure of fit, and GLM estimation is maximum likelihood."
    ),
    (
        "cs1003-4.2.6-cp-01",
        "c",
    ): (
        "That choice sets deviance equal to the sum of squared residuals and claims every GLM is OLS on the link scale. "
        "Deviance is likelihood-based, and GLM fitting maximises the likelihood for the chosen family and link."
    ),
    (
        "cs1003-4.2.6-cp-01",
        "d",
    ): (
        "That choice says deviance and scaled deviance are identical for Poisson and binomial because scale is always 1, with no further definition. "
        "Even when the scale is 1, scaled deviance is still deviance divided by that scale."
    ),
    (
        "cs1014-4.2.6-cp-01",
        "b",
    ): (
        "That choice defines deviance as an AIC difference, scaled deviance as AIC over n, and estimation as dropping p greater than 0.10. "
        "Deviance is a likelihood-ratio measure of fit, and GLM estimation is maximum likelihood."
    ),
    (
        "cs1014-4.2.6-cp-01",
        "c",
    ): (
        "That choice sets deviance equal to the sum of squared residuals and claims every GLM is OLS on the link scale. "
        "Deviance is likelihood-based, and GLM fitting maximises the likelihood for the chosen family and link."
    ),
    (
        "cs1014-4.2.6-cp-01",
        "d",
    ): (
        "That choice says deviance and scaled deviance are identical for Poisson and binomial because scale is always 1, with no further definition. "
        "Even when the scale is 1, scaled deviance is still deviance divided by that scale."
    ),
    (
        "cs1003-4.2.7-ar-01",
        "b",
    ): (
        "That choice treats a Pearson residual plot as finishing analysis of deviance, with large residuals crowning the full model. "
        "For nested models, AoD uses the deviance difference, not residual plots as the model-choice test."
    ),
    (
        "cs1003-4.2.7-ar-01",
        "c",
    ): (
        "That choice compares models by raw R-squared on the link scale and limits deviance differences to Normal identity. "
        "Nested AoD uses deviance differences for GLMs generally, not raw link-scale R-squared."
    ),
    (
        "cs1003-4.2.7-ar-01",
        "d",
    ): (
        "That choice skips deviance comparison whenever every p in the larger model is below 0.05. "
        "Nested comparison still uses the deviance contrast between models, not coefficient p-values alone."
    ),
    (
        "cs1014-4.2.7-ar-01",
        "b",
    ): (
        "That choice says plotting Pearson residuals finishes model choice via AoD because large residuals imply the full model wins. "
        "AoD for nested models compares deviance differences, not residual magnitude as a substitute test."
    ),
    (
        "cs1014-4.2.7-ar-01",
        "c",
    ): (
        "That choice always compares non-nested models by raw R-squared on the link scale and restricts deviance differences to Normal GLMs. "
        "Nested analysis of deviance uses deviance differences across GLM families."
    ),
    (
        "cs1014-4.2.7-ar-01",
        "d",
    ): (
        "That choice lets parameter significance alone replace deviance comparison. "
        "Coefficient tests and nested deviance comparison answer related but different questions."
    ),
    (
        "cs1003-4.2.7-cp-01",
        "b",
    ): (
        "That choice finishes nested model choice by plotting Pearson residuals under AoD. "
        "For nested models, compare through the deviance difference, not residual plots alone."
    ),
    (
        "cs1003-4.2.7-cp-01",
        "c",
    ): (
        "That choice selects the full model whenever any single added coefficient has p below 0.05 and calls the deviance difference redundant. "
        "Nested comparison still uses the joint deviance contrast for the added terms."
    ),
    (
        "cs1003-4.2.7-cp-01",
        "d",
    ): (
        "That choice limits AoD to Normal identity GLMs and sends Poisson to raw AIC only. "
        "Analysis of deviance applies to nested GLMs more generally, including Poisson."
    ),
    (
        "cs1014-4.2.7-cp-01",
        "b",
    ): (
        "That choice finishes nested model choice by plotting Pearson residuals under AoD. "
        "For nested models, compare through the deviance difference, not residual plots alone."
    ),
    (
        "cs1014-4.2.7-cp-01",
        "c",
    ): (
        "That choice selects the full model whenever any single added coefficient has p below 0.05 and calls the deviance difference redundant. "
        "Nested comparison still uses the joint deviance contrast for the added terms."
    ),
    (
        "cs1014-4.2.7-cp-01",
        "d",
    ): (
        "That choice limits AoD to Normal identity GLMs and sends Poisson to raw AIC only. "
        "Analysis of deviance applies to nested GLMs more generally, including Poisson."
    ),
    (
        "cs1003-4.2.8-ar-01",
        "b",
    ): (
        "That choice treats an LRT as finishing the explanation of Pearson and deviance residuals because LRT and residuals are the same diagnostic. "
        "Likelihood-ratio tests compare models; Pearson and deviance residuals are observation-level fit diagnostics."
    ),
    (
        "cs1003-4.2.8-ar-01",
        "c",
    ): (
        "That choice sets both Pearson and deviance residuals equal to y minus mu-hat with no variance scaling. "
        "Pearson residuals scale the raw residual by a variance factor; deviance residuals come from the signed square root of the observation’s deviance contribution."
    ),
    (
        "cs1003-4.2.8-ar-01",
        "d",
    ): (
        "That choice allows deviance residuals only for Normal GLMs and forces Poisson and binomial to Pearson only. "
        "Deviance residuals are defined for those families from each observation’s deviance contribution."
    ),
    (
        "cs1014-4.2.8-ar-01",
        "b",
    ): (
        "That choice treats an LRT as finishing the explanation of Pearson and deviance residuals because LRT and residuals are the same diagnostic. "
        "Likelihood-ratio tests compare models; Pearson and deviance residuals are observation-level fit diagnostics."
    ),
    (
        "cs1014-4.2.8-ar-01",
        "c",
    ): (
        "That choice sets both Pearson and deviance residuals equal to y minus mu-hat with no variance scaling. "
        "Pearson residuals scale the raw residual by a variance factor; deviance residuals come from the signed square root of the observation’s deviance contribution."
    ),
    (
        "cs1014-4.2.8-ar-01",
        "d",
    ): (
        "That choice allows deviance residuals only for Normal GLMs and forces Poisson and binomial to Pearson only. "
        "Deviance residuals are defined for those families from each observation’s deviance contribution."
    ),
    (
        "cs1003-4.2.9-ar-01",
        "b",
    ): (
        "That choice treats coefficient reading and R-squared as the Pearson chi-square and LRT. "
        "Pearson chi-square aggregates squared Pearson residuals against a chi-squared reference, and the LRT compares likelihood or deviance to a nested or saturated alternative."
    ),
    (
        "cs1003-4.2.9-ar-01",
        "c",
    ): (
        "That choice collapses Pearson chi-square and the LRT into one large-sample test with vendor-only names. "
        "The two tests answer different questions: aggregate residual adequacy versus a likelihood or deviance comparison."
    ),
    (
        "cs1003-4.2.9-ar-01",
        "d",
    ): (
        "That choice confines acceptability checks to the pre-fit stage and treats Fit as the end of formal testing. "
        "After fitting you still need Pearson chi-square and LRT assessments of the fitted model."
    ),
    (
        "cs1014-4.2.9-ar-01",
        "b",
    ): (
        "That choice treats coefficient reading and R-squared as the Pearson chi-square and LRT. "
        "Pearson chi-square aggregates squared Pearson residuals against a chi-squared reference, and the LRT compares likelihood or deviance to a nested or saturated alternative."
    ),
    (
        "cs1014-4.2.9-ar-01",
        "c",
    ): (
        "That choice collapses Pearson chi-square and the LRT into one large-sample test with vendor-only names. "
        "The two tests answer different questions: aggregate residual adequacy versus a likelihood or deviance comparison."
    ),
    (
        "cs1014-4.2.9-ar-01",
        "d",
    ): (
        "That choice confines acceptability checks to the pre-fit stage and treats Fit as the end of formal testing. "
        "After fitting you still need Pearson chi-square and LRT assessments of the fitted model."
    ),
    (
        "cs1003-4.2.9-cp-01",
        "b",
    ): (
        "That choice treats reading every coefficient as finishing acceptability testing. "
        "Coefficient interpretation is separate; you still apply Pearson chi-square for aggregate adequacy and the LRT for likelihood or deviance comparison."
    ),
    (
        "cs1003-4.2.9-cp-01",
        "c",
    ): (
        "That choice swaps the test definitions: Pearson chi-square is not the nested deviance difference, and the LRT is not the sum of squared Pearson residuals. "
        "Pearson chi-square aggregates squared Pearson residuals; the LRT compares likelihood or deviance."
    ),
    (
        "cs1003-4.2.9-cp-01",
        "d",
    ): (
        "That choice treats residual plots as the only acceptability judgment and the named tests as plot labels. "
        "Plots support inspection, but Pearson chi-square and the LRT remain distinct formal comparisons."
    ),
    (
        "cs1014-4.2.9-cp-01",
        "b",
    ): (
        "That choice treats reading every coefficient as finishing acceptability testing. "
        "Coefficient interpretation is separate; you still apply Pearson chi-square for aggregate adequacy and the LRT for likelihood or deviance comparison."
    ),
    (
        "cs1014-4.2.9-cp-01",
        "c",
    ): (
        "That choice swaps the test definitions: Pearson chi-square is not the nested deviance difference, and the LRT is not the sum of squared Pearson residuals. "
        "Pearson chi-square aggregates squared Pearson residuals; the LRT compares likelihood or deviance."
    ),
    (
        "cs1014-4.2.9-cp-01",
        "d",
    ): (
        "That choice treats residual plots as the only acceptability judgment and the named tests as plot labels. "
        "Plots support inspection, but Pearson chi-square and the LRT remain distinct formal comparisons."
    ),
    (
        "cs1003-4.2.10-ar-01",
        "b",
    ): (
        "That choice treats the Fit command as supplying all actuarial interpretation and validation automatically. "
        "Beyond fitting you still need to interpret coefficients and run diagnostics on the fitted GLM."
    ),
    (
        "cs1003-4.2.10-ar-01",
        "c",
    ): (
        "That choice limits interpretation to the intercept and denies response-scale meaning for factor coefficients. "
        "Factor effects still need interpretation on the response scale alongside diagnostics."
    ),
    (
        "cs1003-4.2.10-ar-01",
        "d",
    ): (
        "That choice equates fitting a GLM with completing Bayesian credibility because both can model claim counts. "
        "GLM fitting does not finish Bayesian credibility work."
    ),
    (
        "cs1014-4.2.10-ar-01",
        "b",
    ): (
        "That choice treats clicking Fit as finishing interpretation and diagnostics because the software shows conclusions automatically. "
        "Beyond Fit you still interpret coefficients, fit measures, and diagnostics."
    ),
    (
        "cs1014-4.2.10-ar-01",
        "c",
    ): (
        "That choice treats fitting a GLM as finishing Bayesian credibility because both use statistical software output. "
        "Shared software does not make GLM fitting complete Bayesian credibility work."
    ),
    (
        "cs1014-4.2.10-ar-01",
        "d",
    ): (
        "That choice restricts interpretation to the intercept and treats factor coefficients and diagnostics as optional. "
        "Factor coefficients and diagnostics remain required beyond the intercept."
    ),
    (
        "cs1014-cx-r1-ar-01",
        "b",
    ): (
        "That choice treats the link as mapping each residual to a probability density. "
        "The link maps the mean mu to the linear predictor eta = X beta."
    ),
    (
        "cs1014-cx-r1-ar-01",
        "c",
    ): (
        "That choice claims the link forces every response distribution to become Normal. "
        "The link maps mu to eta; it does not turn the response family into Normal."
    ),
    (
        "cs1014-cx-r1-ar-01",
        "d",
    ): (
        "That choice treats the link as specifying covariance among all observations. "
        "The link maps mu to eta; dependence is not what the link encodes."
    ),
    (
        "cs1014-cx-r1-cp-01",
        "b",
    ): (
        "That choice always prefers the larger model because deviance cannot increase with more parameters. "
        "Nested deviance differences are judged against a chi-squared reference under nesting and the same family and scale, not by parameter count alone."
    ),
    (
        "cs1014-cx-r1-cp-01",
        "c",
    ): (
        "That choice always compares a deviance difference with a standard Normal. "
        "For nested GLMs with the same family and scale, the deviance difference is compared with a chi-squared reference."
    ),
    (
        "cs1014-cx-r1-cp-01",
        "d",
    ): (
        "That choice takes a non-significant deviance difference as proof that every residual assumption holds. "
        "A non-significant nested comparison does not certify residual or independence assumptions."
    ),
    (
        "cs1003-cd-r2-ar-01",
        "b",
    ): (
        "That choice gives the family the role of determining X and has the link turn predictors into response variance. "
        "The family sets the mean-variance relationship, eta = X beta, and the link satisfies g(mu) = eta."
    ),
    (
        "cs1003-cd-r2-ar-01",
        "c",
    ): (
        "That choice treats eta as the observed response and the link as its density. "
        "Eta = X beta is the linear predictor, and the link maps mu via g(mu) = eta."
    ),
    (
        "cs1003-cd-r2-ar-01",
        "d",
    ): (
        "That choice claims the link requires the response itself to be Normal. "
        "The family sets mean-variance behaviour and g(mu) = eta; Normality of Y is not required."
    ),
    (
        "cs1003-cd-r2-cp-01",
        "b",
    ): (
        "That choice sets the Poisson canonical link as mu squared equals eta and equates deviance with residual sum of squares in every GLM. "
        "For Poisson the canonical link is log(mu) = eta, and deviance compares fitted and saturated models through likelihoods."
    ),
    (
        "cs1003-cd-r2-cp-01",
        "c",
    ): (
        "That choice allows only the identity link for Poisson because counts stay untransformed. "
        "The Poisson canonical link is log(mu) = eta; identity is not the only valid link."
    ),
    (
        "cs1003-cd-r2-cp-01",
        "d",
    ): (
        "That choice treats small deviance as proof of every distributional and independence assumption. "
        "Deviance compares fitted versus saturated likelihoods; it does not certify all assumptions by itself."
    ),
    (
        "cs1002-2.1a-ar-01",
        "b",
    ): (
        "That choice shortens the discrete roster and collapses negative binomial into geometric, with hypergeometric optional. "
        "Syllabus 2.1.1 needs the full six discrete families with their situation cues."
    ),
    (
        "cs1002-2.1a-ar-01",
        "c",
    ): (
        "That choice swaps the situation cues for binomial, hypergeometric, and Poisson. "
        "Match each family to its cue: fixed independent trials, without-replacement finite sampling, and counts with a rate story."
    ),
    (
        "cs1002-2.1a-ar-01",
        "d",
    ): (
        "That choice lists continuous families while attaching discrete count cues. "
        "The six Syllabus 2.1.1 discrete families are the discrete roster with discrete situation cues."
    ),
    (
        "cs1002-2.1a-cp-01",
        "b",
    ): (
        "That choice applies binomial automatically to any claim count, including without-replacement sampling. "
        "Sampling without replacement from a finite portfolio is a hypergeometric setting."
    ),
    (
        "cs1002-2.1a-cp-01",
        "c",
    ): (
        "That choice defaults to Poisson for every claim count and ignores without-replacement structure. "
        "Finite without-replacement sampling of policies points to the hypergeometric."
    ),
    (
        "cs1002-2.1a-cp-01",
        "d",
    ): (
        "That choice uses discrete uniform because policies look equally likely and rejects hypergeometric for insurance. "
        "Equal likelihood of units does not remove the without-replacement finite-population structure."
    ),
    (
        "cs1002-2.1b-ar-01",
        "b",
    ): (
        "That choice keeps only Normal and treats the other continuous names as optional without cues. "
        "You need Normal, lognormal, exponential, and gamma, each with continuous situation cues."
    ),
    (
        "cs1002-2.1b-ar-01",
        "c",
    ): (
        "That choice reverses the continuous cues for Normal, lognormal, exponential, and gamma. "
        "Match each family to its correct support and shape story."
    ),
    (
        "cs1002-2.1b-ar-01",
        "d",
    ): (
        "That choice lists discrete count families as the continuous roster. "
        "Continuous families here include Normal, lognormal, exponential, and gamma with continuous cues."
    ),
    (
        "cs1002-2.1b-cp-01",
        "b",
    ): (
        "That choice defaults to Normal for individual claim sizes because the CLT supposedly always Normalises them. "
        "For strictly positive, right-skewed claim sizes, start with lognormal or gamma rather than Normal by default."
    ),
    (
        "cs1002-2.1b-cp-01",
        "c",
    ): (
        "That choice uses continuous uniform on all reals and treats positive skew as irrelevant. "
        "Strictly positive right-skewed claim sizes point to lognormal or gamma."
    ),
    (
        "cs1002-2.1b-cp-01",
        "d",
    ): (
        "That choice refuses lognormal and gamma and prefers Normal because negatives supposedly never appear in practice. "
        "Prefer lognormal or gamma for positive skewed sizes; do not default to Normal."
    ),
    (
        "cs1004-2.1c-ar-01",
        "b",
    ): (
        "That choice treats naming the family as already completing both probability and quantile evaluation. "
        "Naming the distribution is not the calculation; you still distinguish probability, quantile, and method class."
    ),
    (
        "cs1004-2.1c-ar-01",
        "c",
    ): (
        "That choice swaps the tasks: it treats a quantile as P(X less than or equal to a) and a probability question as finding x for a given cumulative probability. "
        "Probability asks for a probability from a threshold; a quantile asks for x at a stated cumulative probability."
    ),
    (
        "cs1004-2.1c-ar-01",
        "d",
    ): (
        "That choice counts only software menus as method class and rejects hand calculation and tables. "
        "Method class includes hand calculation and tables as well as software."
    ),
    (
        "cs1004-2.1d-ar-01",
        "b",
    ): (
        "That choice treats a Poisson process as only another name for the Poisson PMF with no continuous-time arrival story. "
        "The Poisson process is the continuous-time arrival model whose interval counts follow a Poisson distribution."
    ),
    (
        "cs1004-2.1d-ar-01",
        "c",
    ): (
        "That choice gives fixed-interval counts a continuous Normal law under a Poisson process and reserves the Poisson distribution for waiting times. "
        "Under a Poisson process, counts in a fixed interval follow a Poisson distribution."
    ),
    (
        "cs1004-2.1d-ar-01",
        "d",
    ): (
        "That choice swaps roles: distribution for continuous-time arrivals and process for the discrete interval count law. "
        "The process models continuous-time arrivals; the Poisson distribution is the count law in a fixed interval."
    ),
    (
        "cs1004-2.1d-cp-01",
        "b",
    ): (
        "That choice agrees that process language is optional once the discrete Poisson PMF is named. "
        "Process talk is not decoration; it links continuous-time arrivals to the Poisson count law in an interval."
    ),
    (
        "cs1004-2.1d-cp-01",
        "c",
    ): (
        "That choice refuses only the word process while accepting interval counts with no distributional link to arrivals. "
        "Interval counts still need that link from the Poisson process to the Poisson distribution."
    ),
    (
        "cs1004-2.1d-cp-01",
        "d",
    ): (
        "That choice claims the discrete Poisson already includes continuous-time arrivals so distinguishing is unnecessary. "
        "Naming the PMF does not replace the process-to-distribution connection."
    ),
    (
        "cs1004-2.1e-ar-01",
        "b",
    ): (
        "That choice draws X directly from F and treats the inverse CDF as optional. "
        "Inverse transform starts from U ~ Uniform(0,1) and sets X = F inverse(U)."
    ),
    (
        "cs1004-2.1e-ar-01",
        "c",
    ): (
        "That choice draws U ~ Normal(0,1) and sets X = F(U) with the CDF instead of the inverse. "
        "Use Uniform(0,1) and the inverse CDF: X = F inverse(U)."
    ),
    (
        "cs1004-2.1e-ar-01",
        "d",
    ): (
        "That choice sets X = F(U) with U already equal to X and drops Uniform. "
        "The method needs a fresh Uniform draw and the inverse map X = F inverse(U)."
    ),
    (
        "cs1004-2.1e-cp-01",
        "b",
    ): (
        "That choice skips Uniform and thresholds and treats library calls such as rbinom as replacing the discrete method. "
        "Discrete inverse transform still uses Uniform draws and cumulative thresholds even when software is available."
    ),
    (
        "cs1004-2.1e-cp-01",
        "c",
    ): (
        "That choice uses Normal draws for discrete inverse transform and treats understanding as optional once a library exists. "
        "The discrete method uses Uniform draws and cumulative probability thresholds."
    ),
    (
        "cs1004-2.1e-cp-01",
        "d",
    ): (
        "That choice assigns outcomes by sorting probabilities alphabetically with no Uniform threshold. "
        "Discrete inverse transform compares a Uniform draw to cumulative probabilities."
    ),
    (
        "cs1004-2.1f-ar-01",
        "b",
    ): (
        "That choice generates both samples and accepts them without checking support or summaries because the library supposedly cannot fail. "
        "After generation you still check Poisson and Exponential support and basic summaries."
    ),
    (
        "cs1004-2.1f-ar-01",
        "c",
    ): (
        "That choice checks Poisson as positive reals and Exponential as non-negative integers. "
        "Poisson draws are non-negative integers; Exponential draws are positive reals."
    ),
    (
        "cs1004-2.1f-ar-01",
        "d",
    ): (
        "That choice treats a matching sample mean as proof even if Poisson values are fractional or Exponential values are negative. "
        "A mean match does not override support failures."
    ),
    (
        "cs1004-2.1f-cp-01",
        "b",
    ): (
        "That choice lets the built-in sampler remove the need to inspect support or means. "
        "After simulating Poisson(lambda = 3) and Exponential with mean 2, still check support and that sample means are near 3 and 2."
    ),
    (
        "cs1004-2.1f-cp-01",
        "c",
    ): (
        "That choice expects the Poisson sample near 2 and the Exponential near 3 by treating lambda as a waiting-time mean. "
        "Poisson(lambda = 3) should average near 3 and Exponential with mean 2 near 2."
    ),
    (
        "cs1004-2.1f-cp-01",
        "d",
    ): (
        "That choice accepts both samples as only integers because Exponential waiting times are treated as discrete event counts. "
        "Exponential waiting times are continuous positive reals, not integer event counts."
    ),
    (
        "cs1016-2.1.3-ar-01",
        "b",
    ): (
        "That choice treats naming the family as completing evaluation with no further calculation. "
        "For a named univariate distribution you still compute the required probability or quantile."
    ),
    (
        "cs1016-2.1.3-ar-01",
        "c",
    ): (
        "That choice equates every quantile with the sample mean and pulls probabilities from a joint (X, Y) table. "
        "A univariate quantile is the x at a stated cumulative probability from that distribution alone."
    ),
    (
        "cs1016-2.1.3-ar-01",
        "d",
    ): (
        "That choice requires summing out Y to obtain marginals before any univariate probability. "
        "Univariate evaluation uses the named distribution of X directly."
    ),
    (
        "cs1017-2.1.1-ar-01",
        "b",
    ): (
        "That choice models all discrete count data as Normal by default for any numeric column. "
        "Named discrete families are matched to count situations, not replaced by a Normal default."
    ),
    (
        "cs1017-2.1.1-ar-01",
        "c",
    ): (
        "That choice treats hypergeometric and Poisson as interchangeable whenever counts are non-negative integers. "
        "Non-negative integers alone do not make those families interchangeable."
    ),
    (
        "cs1017-2.1.1-ar-01",
        "d",
    ): (
        "That choice applies discrete families only after continuous models fail and lets integer support alone determine Poisson. "
        "Integer support is not enough; choose the discrete family from the situation cues."
    ),
    (
        "cs1017-2.1.1-cp-01",
        "b",
    ): (
        "That choice fits Normal(mu, sigma squared) because mean and variance can always be matched. "
        "For a single policy’s claims in a fixed year with a constant rare-event rate and independent increments, Poisson fits."
    ),
    (
        "cs1017-2.1.1-cp-01",
        "c",
    ): (
        "That choice requires hypergeometric because every insurance count is treated as without-replacement from a finite population. "
        "This rare-event independent-increments story in a fixed year is Poisson."
    ),
    (
        "cs1017-2.1.1-cp-01",
        "d",
    ): (
        "That choice forces binomial because one policy supposedly means n = 1 always defines annual claims. "
        "One policy with a rare constant rate and independent increments points to Poisson, not mandatory binomial n = 1."
    ),
    (
        "cs1004-cgr1-ar-01",
        "b",
    ): (
        "That choice sets X = F(U) using the CDF rather than its inverse. "
        "When F is continuous and strictly increasing and U ~ Uniform(0,1), X = F inverse(U) has distribution function F."
    ),
    (
        "cs1004-cgr1-ar-01",
        "c",
    ): (
        "That choice sets X = 1 minus U for every F. "
        "That map does not produce DF F in general; you need X = F inverse(U)."
    ),
    (
        "cs1004-cgr1-ar-01",
        "d",
    ): (
        "That choice sets X = log(U) regardless of the support of F. "
        "A fixed log map ignores F; the transform that yields DF F is X = F inverse(U)."
    ),
}

def setup_function() -> None:
    reset_educational_package_cache()


_PRIOR_ONE_HUNDRED_FEEDBACK: dict[tuple[str, str], str] = {
    **_PRIOR_FIFTY_NINE_FEEDBACK,
    **_CAF_WAVE4_FEEDBACK,
}

_CAF_WAVE5_FEEDBACK: dict[tuple[str, str], str] = {
    # --- cs1005-2.2.1-ar-01 ---
    (
        "cs1005-2.2.1-ar-01",
        "b",
    ): (
        "That choice treats the joint as already numerically equal to every marginal and conditional. "
        "You still sum or integrate out partners for a marginal, and divide by the conditioning marginal for a conditional."
    ),
    (
        "cs1005-2.2.1-ar-01",
        "c",
    ): (
        "That choice reverses the operations: dividing for a marginal and summing for a conditional. "
        "A marginal sums or integrates the joint over the other variable; a conditional divides joint by the conditioning marginal."
    ),
    (
        "cs1005-2.2.1-ar-01",
        "d",
    ): (
        "That choice sets a conditional equal to its joint numerator just because the table totals one. "
        "A conditional still divides by the marginal of the conditioning value."
    ),
    # --- cs1005-2.2.2-ar-01 ---
    (
        "cs1005-2.2.2-ar-01",
        "b",
    ): (
        "That choice treats a defined covariance as enough for independence even when the joint does not factor. "
        "Independence needs joint equals product of marginals (or an equivalent form), not merely that Cov exists."
    ),
    (
        "cs1005-2.2.2-ar-01",
        "c",
    ): (
        "That choice writes independence as joint equals the sum of the marginals. "
        "The factorisation hinge is a product of marginals, not a sum."
    ),
    (
        "cs1005-2.2.2-ar-01",
        "d",
    ): (
        "That choice stops once each marginal exists and drops the joint-factorisation requirement. "
        "Independence still needs the joint to equal the product of those marginals on the support."
    ),
    # --- cs1005-2.2.2-cp-01 ---
    (
        "cs1005-2.2.2-cp-01",
        "b",
    ): (
        "That choice accepts zero correlation as necessary and sufficient for independence in all bivariate settings. "
        "Uncorrelated is weaker than independence; you still need joint factorisation (or equivalent)."
    ),
    (
        "cs1005-2.2.2-cp-01",
        "c",
    ): (
        "That choice refuses independence language and treats zero correlation as proving the joint cannot factor. "
        "Zero correlation does not by itself prove or disprove factorisation."
    ),
    (
        "cs1005-2.2.2-cp-01",
        "d",
    ): (
        "That choice treats zero correlation as stronger than independence and drops the factorisation check. "
        "Factorisation is the independence warrant; zero correlation is not a stronger substitute."
    ),
    # --- cs1005-2.2.3-ar-01 ---
    (
        "cs1005-2.2.3-ar-01",
        "b",
    ): (
        "That choice computes E[g(X,Y)] from marginal means alone for every g. "
        "Joint expectation weights g by the joint distribution; marginal means are not enough for arbitrary g."
    ),
    (
        "cs1005-2.2.3-ar-01",
        "c",
    ): (
        "That choice multiplies covariance by both standard deviations and keeps units. "
        "Correlation divides Cov by SD(X)SD(Y), so it is dimensionless."
    ),
    (
        "cs1005-2.2.3-ar-01",
        "d",
    ): (
        "That choice treats covariance as all dependence and zero Cov as proof of independence. "
        "Cov captures linear co-movement; zero Cov does not prove independence in general."
    ),
    # --- cs1005-2.2.4-ar-01 ---
    (
        "cs1005-2.2.4-ar-01",
        "b",
    ): (
        "That choice leaves a and b unsquared inside Var(aX+bY). "
        "Variance scales with a squared and b squared, then adds the 2ab Cov term."
    ),
    (
        "cs1005-2.2.4-ar-01",
        "c",
    ): (
        "That choice drops the covariance term for every X and Y. "
        "Without independence (or Cov = 0), Var(aX+bY) keeps 2ab Cov(X,Y)."
    ),
    (
        "cs1005-2.2.4-ar-01",
        "d",
    ): (
        "That choice squares a and b inside the expectation. "
        "Expectation is linear: E[aX+bY] = a E[X] + b E[Y], without squaring those coefficients."
    ),
    # --- cs1006-2.3.1-ar-01 ---
    (
        "cs1006-2.3.1-ar-01",
        "b",
    ): (
        "That choice sets E[Y|X=x] equal to the unconditional mean for every x. "
        "Conditional expectation uses the distribution of Y given X=x, and it need not equal E[Y]."
    ),
    (
        "cs1006-2.3.1-ar-01",
        "c",
    ): (
        "That choice replaces E[Y|X=x] with a joint probability at the largest y. "
        "Conditional expectation averages Y under the conditional distribution, not a raw joint cell."
    ),
    (
        "cs1006-2.3.1-ar-01",
        "d",
    ): (
        "That choice treats conditional expectation as a fixed constant that cannot depend on x. "
        "As x varies, E[Y|X=x] is a function of x."
    ),
    # --- cs1006-2.3.2-ar-01 ---
    (
        "cs1006-2.3.2-ar-01",
        "b",
    ): (
        "That choice sets E[Y] equal to E[Y|X] for every realised X and skips the outer average. "
        "The tower property recovers E[Y] = E[E[Y|X]]."
    ),
    (
        "cs1006-2.3.2-ar-01",
        "c",
    ): (
        "That choice keeps only Var(E[Y|X]) and drops average within-condition variance. "
        "Total variance also includes E[Var(Y|X)]."
    ),
    (
        "cs1006-2.3.2-ar-01",
        "d",
    ): (
        "That choice keeps only E[Var(Y|X)] and drops variation of conditional means. "
        "Total variance also includes Var(E[Y|X])."
    ),
    # --- cs1016-2.2.1-ar-01 ---
    (
        "cs1016-2.2.1-ar-01",
        "b",
    ): (
        "That choice treats marginals and conditionals as optional once the joint is written. "
        "You still extract a marginal by summing or integrating, and a conditional by dividing by the conditioning marginal."
    ),
    (
        "cs1016-2.2.1-ar-01",
        "c",
    ): (
        "That choice sets P(Y given X=x) equal to the joint entry with no division by P(X=x). "
        "Conditioning renormalises by that marginal probability."
    ),
    (
        "cs1016-2.2.1-ar-01",
        "d",
    ): (
        "That choice forms every marginal and conditional by dividing each joint cell by the grand total. "
        "A marginal sums over partners; a conditional divides by the conditioning event\u2019s probability, not by a single grand-total rescaling rule for both."
    ),
    # --- cs1005-ce-r1-ar-01 ---
    (
        "cs1005-ce-r1-ar-01",
        "b",
    ): (
        "That choice treats Cov(X,Y) = 0 as independence in every case. "
        "Independence needs joint factorisation on the support; zero covariance is generally insufficient."
    ),
    (
        "cs1005-ce-r1-ar-01",
        "c",
    ): (
        "That choice writes the joint as the sum of the marginals. "
        "Independence factorises the joint as a product of marginals."
    ),
    (
        "cs1005-ce-r1-ar-01",
        "d",
    ): (
        "That choice treats E[X] = E[Y] as independence. "
        "Equal means do not establish joint factorisation."
    ),
    # --- cs1005-ce-r1-cp-01 ---
    (
        "cs1005-ce-r1-cp-01",
        "b",
    ): (
        "That choice writes Var(aX+bY) as a Var(X) + b Var(Y). "
        "Variance scales with a squared and b squared, then adds the covariance cross-term."
    ),
    (
        "cs1005-ce-r1-cp-01",
        "c",
    ): (
        "That choice drops the covariance term in all cases. "
        "Without a warrant for Cov = 0, keep 2ab Cov(X,Y)."
    ),
    (
        "cs1005-ce-r1-cp-01",
        "d",
    ): (
        "That choice uses ab Cov instead of 2ab Cov. "
        "The cross-product term is 2ab Cov(X,Y)."
    ),
    # --- cs1006-cz-r1-ar-01 ---
    (
        "cs1006-cz-r1-ar-01",
        "b",
    ): (
        "That choice sets E[Y] equal to E[Y given X] for every realised X. "
        "The law of total expectation averages the conditional mean over X: E[Y] = E[E[Y given X]]."
    ),
    (
        "cs1006-cz-r1-ar-01",
        "c",
    ): (
        "That choice replaces the tower identity with Var(E[Y given X]). "
        "Total expectation averages conditional means; that variance object is part of the variance decomposition, not E[Y]."
    ),
    (
        "cs1006-cz-r1-ar-01",
        "d",
    ): (
        "That choice equates E[Y given X] with E[X given Y] in general. "
        "Those conditional expectations are not the same object."
    ),
    # --- cs1006-cz-r1-cp-01 ---
    (
        "cs1006-cz-r1-cp-01",
        "b",
    ): (
        "That choice writes Var(Y) as Var(Y given X) + Var(X). "
        "The lawful split is E[Var(Y given X)] + Var(E[Y given X])."
    ),
    (
        "cs1006-cz-r1-cp-01",
        "c",
    ): (
        "That choice keeps only E[Var(Y given X)]. "
        "You also need Var(E[Y given X]), the between-condition piece."
    ),
    (
        "cs1006-cz-r1-cp-01",
        "d",
    ): (
        "That choice keeps only Var(E[Y given X]). "
        "You also need E[Var(Y given X)], the within-condition piece."
    ),
    # --- cs1011-3.2.1-ar-01 ---
    (
        "cs1011-3.2.1-ar-01",
        "b",
    ): (
        "That choice reads a confidence interval as covering the next future observation with the stated probability. "
        "A parameter CI targets an unknown parameter; covering a future observation is a prediction interval."
    ),
    (
        "cs1011-3.2.1-ar-01",
        "c",
    ): (
        "That choice treats a realised 95% CI as a 95% posterior probability that the fixed parameter lies in that interval. "
        "Frequentist coverage is about the procedure under repeated sampling, not that Bayesian post-data reading."
    ),
    (
        "cs1011-3.2.1-ar-01",
        "d",
    ): (
        "That choice calls any interval estimate of a future loss a confidence interval. "
        "A CI targets an unknown parameter with a stated coverage interpretation, not an arbitrary future-loss band."
    ),
    # --- cs1011-3.2.1-cp-01 ---
    (
        "cs1011-3.2.1-cp-01",
        "b",
    ): (
        "That choice reads (120, 140) as a 95% probability for the next claim amount. "
        "Coverage is for the parameter mu under repeated sampling, not for the next observation."
    ),
    (
        "cs1011-3.2.1-cp-01",
        "c",
    ): (
        "That choice treats mu as a random variable equal to 130 with probability 95%. "
        "In the frequentist reading, mu is fixed; the interval procedure is what has coverage."
    ),
    (
        "cs1011-3.2.1-cp-01",
        "d",
    ): (
        "That choice equates a narrow interval with 100% coverage for this sample. "
        "Narrowness does not change the procedure\u2019s coverage probability."
    ),
    # --- cs1011-3.2.2-ar-01 ---
    (
        "cs1011-3.2.2-ar-01",
        "b",
    ): (
        "That choice treats a prediction interval and a parameter CI as covering the same numerical object. "
        "A prediction interval targets a future observation; a parameter CI targets an unknown parameter."
    ),
    (
        "cs1011-3.2.2-ar-01",
        "c",
    ): (
        "That choice claims a prediction interval is always narrower than the matching parameter CI. "
        "Prediction intervals are typically wider because they include process or residual variation as well as parameter uncertainty."
    ),
    (
        "cs1011-3.2.2-ar-01",
        "d",
    ): (
        "That choice limits a prediction interval to sampling variance of an estimator and excludes residual variation. "
        "Prediction must account for process or residual variation, not only estimator SE."
    ),
    # --- cs1011-3.2.2-cp-01 ---
    (
        "cs1011-3.2.2-cp-01",
        "b",
    ): (
        "That choice treats a CI for mean loss as already covering Y_new with the same coverage. "
        "A mean CI does not finish the prediction-interval task for the future observation."
    ),
    (
        "cs1011-3.2.2-cp-01",
        "c",
    ): (
        "That choice assigns covering E[Y] to the prediction interval and covering Y_new to a parameter CI. "
        "Prediction targets Y_new; the parameter CI targets the mean."
    ),
    (
        "cs1011-3.2.2-cp-01",
        "d",
    ): (
        "That choice builds prediction from residual variance alone with parameters treated as known. "
        "A proper prediction interval also carries parameter uncertainty."
    ),
    # --- cs1011-3.2.3-ar-01 ---
    (
        "cs1011-3.2.3-ar-01",
        "b",
    ): (
        "That choice always forces the Normal-mean cookbook regardless of the sampling distribution given. "
        "Invert the distributional relationship you were actually given to isolate the parameter."
    ),
    (
        "cs1011-3.2.3-ar-01",
        "c",
    ): (
        "That choice uses the sampling distribution only to simulate data and picks endpoints by eye. "
        "The move is to invert the given sampling or pivotal relationship, not to sketch a histogram."
    ),
    (
        "cs1011-3.2.3-ar-01",
        "d",
    ): (
        "That choice takes the support of the sampling distribution as the CI with no inversion. "
        "You still rearrange the pivotal statement to bound the parameter."
    ),
    # --- cs1011-3.2.3-cp-01 ---
    (
        "cs1011-3.2.3-cp-01",
        "b",
    ): (
        "That choice ignores the given chi-square pivot and forces a Normal-mean CI for theta. "
        "Use the stated 2n X-bar / theta ~ chi-square relationship and invert it."
    ),
    (
        "cs1011-3.2.3-cp-01",
        "c",
    ): (
        "That choice reports (chi-square_L, chi-square_U) with no dependence on X-bar. "
        "Isolating theta from the pivot still involves 2n X-bar over the chi-square critical values."
    ),
    (
        "cs1011-3.2.3-cp-01",
        "d",
    ): (
        "That choice multiplies 2n X-bar by the chi-square critical values instead of dividing. "
        "From chi-square_L < 2n X-bar / theta < chi-square_U, the bounds for theta use 2n X-bar / chi-square."
    ),
    # --- cs1011-3.2.4-ar-01 ---
    (
        "cs1011-3.2.4-ar-01",
        "b",
    ): (
        "That choice treats the mean CI as finishing the variance requirement and reuses the t formula with s^2 in place of s. "
        "Variance intervals use a chi-square pivot on the sample variance, not the mean formula."
    ),
    (
        "cs1011-3.2.4-ar-01",
        "c",
    ): (
        "That choice forces a binomial Normal-approximation interval for both Normal mean and variance. "
        "Those Normal pivots are t/z and chi-square, not a binomial recipe."
    ),
    (
        "cs1011-3.2.4-ar-01",
        "d",
    ): (
        "That choice centres a CI for sigma^2 at x-bar with the mean SE. "
        "A variance CI inverts a chi-square structure based on s^2, not the mean interval."
    ),
    # --- cs1011-3.2.4-cp-01 ---
    (
        "cs1011-3.2.4-cp-01",
        "b",
    ): (
        "That choice uses z with s even though sigma is unknown, and skips the variance CI. "
        "With sigma unknown, the mean CI uses t_15, and you still need the chi-square interval for sigma^2."
    ),
    (
        "cs1011-3.2.4-cp-01",
        "c",
    ): (
        "That choice reuses the numerical mean interval as the variance interval. "
        "Mean and variance CIs are different objects with different pivots."
    ),
    (
        "cs1011-3.2.4-cp-01",
        "d",
    ): (
        "That choice centres a Normal interval at s^2 using the mean SE s/sqrt(n). "
        "For sigma^2, invert the chi-square pivot on (n-1)s^2 / sigma^2."
    ),
    # --- cs1011-3.2.5-ar-01 ---
    (
        "cs1011-3.2.5-ar-01",
        "b",
    ): (
        "That choice reuses the binomial p formula, including p(1-p) variance, after renaming p as lambda. "
        "Poisson mean intervals use the Poisson variance function, not Bernoulli variance."
    ),
    (
        "cs1011-3.2.5-ar-01",
        "c",
    ): (
        "That choice bans Normal approximation for all discrete data. "
        "Normal approximation is allowed for binomial p and Poisson mean when that approximation is justified."
    ),
    (
        "cs1011-3.2.5-ar-01",
        "d",
    ): (
        "That choice replaces single-sample binomial and Poisson intervals with two-sample difference intervals. "
        "This setting still needs the single-sample forms for p and lambda."
    ),
    # --- cs1011-3.2.5-cp-01 ---
    (
        "cs1011-3.2.5-cp-01",
        "b",
    ): (
        "That choice keeps variance p-hat(1-p-hat)/n after renaming the centre as lambda-hat. "
        "Poisson uses variance lambda-hat/n (or a matching total-count form), not Bernoulli variance."
    ),
    (
        "cs1011-3.2.5-cp-01",
        "c",
    ): (
        "That choice gives binomial the Poisson-style variance p-hat/n and Poisson the Bernoulli-style variance. "
        "Swap those variance functions back: binomial uses p(1-p)/n; Poisson uses lambda/n."
    ),
    (
        "cs1011-3.2.5-cp-01",
        "d",
    ): (
        "That choice drops the Poisson form and forces a continuous Normal mean interval with s^2/n. "
        "Both single-sample binomial and Poisson Normal-approximation forms are required here."
    ),
    # --- cs1011-3.2.6-ar-01 ---
    (
        "cs1011-3.2.6-ar-01",
        "b",
    ): (
        "That choice treats equal sample sizes as paired data without matching. "
        "Equal n does not create pairing; two-sample CIs still need independent groups (or a true paired design)."
    ),
    (
        "cs1011-3.2.6-ar-01",
        "c",
    ): (
        "That choice pools both samples into one and uses a one-sample CI for the grand mean. "
        "That erases the two-group contrast the interval is meant to cover."
    ),
    (
        "cs1011-3.2.6-ar-01",
        "d",
    ): (
        "That choice requires dependent pairs for any two-sample CI and sends independent groups to prediction intervals. "
        "Independent two-sample CIs are valid without pairing."
    ),
    # --- cs1011-3.2.6-cp-01 ---
    (
        "cs1011-3.2.6-cp-01",
        "b",
    ): (
        "That choice analyses A and B as paired differences merely because n_A = n_B. "
        "Without natural matching, keep an independent two-sample contrast for mu_A - mu_B."
    ),
    (
        "cs1011-3.2.6-cp-01",
        "c",
    ): (
        "That choice treats independence between samples as optional for the mean-difference CI. "
        "The usual two-sample mean-difference interval assumes independent groups."
    ),
    (
        "cs1011-3.2.6-cp-01",
        "d",
    ): (
        "That choice allows only the ratio mu_A / mu_B as the two-sample target under Normal data. "
        "A Normal two-sample CI typically targets a difference of means such as mu_A - mu_B."
    ),
    # --- cs1011-3.2.7-ar-01 ---
    (
        "cs1011-3.2.7-ar-01",
        "b",
    ): (
        "That choice runs an independent two-sample mean-difference CI on before and after columns. "
        "Pairing needs within-pair differences and a one-sample CI for the mean difference."
    ),
    (
        "cs1011-3.2.7-ar-01",
        "c",
    ): (
        "That choice ignores pairing and compares pooled before vs after under independence. "
        "That drops the dependence pairing is meant to exploit."
    ),
    (
        "cs1011-3.2.7-ar-01",
        "d",
    ): (
        "That choice equates paired mean-difference CIs with bootstrap CI construction. "
        "Bootstrap is a different endpoint method; paired analysis still forms differences first."
    ),
    # --- cs1011-3.2.7-cp-01 ---
    (
        "cs1011-3.2.7-cp-01",
        "b",
    ): (
        "That choice uses a two-sample CI for mu_Y - mu_X that assumes independent samples because the columns have equal length. "
        "Matched pairs need D_i differences and a one-sample CI for mu_D."
    ),
    (
        "cs1011-3.2.7-cp-01",
        "c",
    ): (
        "That choice forms separate CIs for mu_X and mu_Y and skips a difference parameter. "
        "The paired target is the mean of within-pair differences."
    ),
    (
        "cs1011-3.2.7-cp-01",
        "d",
    ): (
        "That choice discards half the data at random to force independence. "
        "Pairing is handled by analysing differences, not by throwing away matched observations."
    ),
    # --- cs1011-3.2.8-ar-01 ---
    (
        "cs1011-3.2.8-ar-01",
        "b",
    ): (
        "That choice stops at a bootstrap SE and treats that SE as already a confidence interval. "
        "A bootstrap CI still needs interval endpoints from the replicate distribution (for example percentiles)."
    ),
    (
        "cs1011-3.2.8-ar-01",
        "c",
    ): (
        "That choice equates bootstrap CIs with a hypothesis test\u2019s reject/retain decision. "
        "Forming CI endpoints from replicates is not the same task as testing a null."
    ),
    (
        "cs1011-3.2.8-ar-01",
        "d",
    ): (
        "That choice replaces s in a Normal-mean cookbook with a single bootstrap draw. "
        "Percentile-style bootstrap CIs use many replicates\u2019 quantiles, not one plugged-in draw."
    ),
    # --- cs1011-3.2.8-cp-01 ---
    (
        "cs1011-3.2.8-cp-01",
        "b",
    ): (
        "That choice reports only (theta-hat - SE, theta-hat + SE) from a bootstrap SE and rejects quantile endpoints. "
        "A percentile bootstrap CI uses the alpha/2 and 1-alpha/2 quantiles of the replicates."
    ),
    (
        "cs1011-3.2.8-cp-01",
        "c",
    ): (
        "That choice finishes a bootstrap CI by rejecting H0 whenever theta-hat misses a fixed null, without endpoints. "
        "You still form interval endpoints from the replicate distribution."
    ),
    (
        "cs1011-3.2.8-cp-01",
        "d",
    ): (
        "That choice draws one resample and reports the singleton [theta-hat*, theta-hat*]. "
        "Percentile intervals need many replicates and their quantiles."
    ),
    # --- cs1012-3.3.1-ar-01 ---
    (
        "cs1012-3.3.1-ar-01",
        "b",
    ): (
        "That choice swaps Type I and Type II and reads the p-value as the probability the alternative is true. "
        "Type I is rejecting a true null; Type II is failing to reject a false null; a p-value is a tail probability under the null."
    ),
    (
        "cs1012-3.3.1-ar-01",
        "c",
    ): (
        "That choice reads the p-value as P(null true given data) and sets power to one minus the p-value. "
        "A p-value is P(data as extreme as observed | H0); power is P(reject | H1 true)."
    ),
    (
        "cs1012-3.3.1-ar-01",
        "d",
    ): (
        "That choice treats null and alternative as interchangeable labels. "
        "Which statement is labelled null frames Type I/II, the p-value, and the decision rule."
    ),
    # --- cs1012-3.3.1-cp-01 ---
    (
        "cs1012-3.3.1-cp-01",
        "b",
    ): (
        "That choice swaps the screening errors: Type I as missed disease and Type II as false disease call. "
        "With H0 = healthy, Type I is a false positive and Type II is a false negative."
    ),
    (
        "cs1012-3.3.1-cp-01",
        "c",
    ): (
        "That choice reads the p-value as the probability of disease and power as the probability of no disease. "
        "Keep p-value as a tail probability under H0 and power as P(reject | H1 true)."
    ),
    (
        "cs1012-3.3.1-cp-01",
        "d",
    ): (
        "That choice treats a software z-test click as replacing Type I/II, p-value, and power. "
        "Running a test does not by itself supply that vocabulary."
    ),
    # --- cs1012-3.3.2-ar-01 ---
    (
        "cs1012-3.3.2-ar-01",
        "b",
    ): (
        "That choice sends paired data to the independent two-sample test whenever n1 = n2. "
        "Paired designs analyse matched differences, not independent two-sample comparisons."
    ),
    (
        "cs1012-3.3.2-ar-01",
        "c",
    ): (
        "That choice treats label permutation as the basic parametric Normal-mean test. "
        "Permutation is a different approach; basic procedures here include Normal mean and binomial/Poisson tests under CMP conditions."
    ),
    (
        "cs1012-3.3.2-ar-01",
        "d",
    ): (
        "That choice bans basic tests for binomial and Poisson data. "
        "Basic procedures include binomial/Poisson tests as well as Normal mean tests."
    ),
    # --- cs1012-3.3.2-cp-01 ---
    (
        "cs1012-3.3.2-cp-01",
        "b",
    ): (
        "That choice mismatches families: chi-square GOF for one Normal mean, paired t on unpaired columns, and independent two-sample z on matched pairs. "
        "Match one-sample z, two-sample proportions, and paired differences to those three settings."
    ),
    (
        "cs1012-3.3.2-cp-01",
        "c",
    ): (
        "That choice handles all three settings by shuffling labels and treats parametric tests as optional flavour. "
        "Permutation is separate; these basic parametric tests still follow the sampling model and design."
    ),
    (
        "cs1012-3.3.2-cp-01",
        "d",
    ): (
        "That choice scrambles designs: two-sample z for one mean, one-sample Poisson for two proportions, binomial for paired Normal differences. "
        "Keep the design and model aligned with each procedure."
    ),
    # --- cs1012-3.3.3-ar-01 ---
    (
        "cs1012-3.3.3-ar-01",
        "b",
    ): (
        "That choice treats a permutation test as identical to a Normal two-sample z-test. "
        "Permutation builds a reference distribution by reshuffling under exchangeability; it is not the Normal cookbook by another name."
    ),
    (
        "cs1012-3.3.3-ar-01",
        "c",
    ): (
        "That choice describes permutation as resampling with replacement to form a CI, like bootstrap. "
        "Permutation tests reassign labels under an exchangeable null to test a hypothesis, not to build a bootstrap CI."
    ),
    (
        "cs1012-3.3.3-ar-01",
        "d",
    ): (
        "That choice equates permutation with chi-square GOF to a named distribution. "
        "GOF compares frequencies to a stated law; permutation compares an observed statistic to a label-shuffle reference."
    ),
    # --- cs1012-3.3.3-cp-01 ---
    (
        "cs1012-3.3.3-cp-01",
        "b",
    ): (
        "That choice computes one Normal two-sample z and treats \u201cpermutation\u201d as only a label for that test. "
        "Under exchangeability you shuffle labels, recompute the statistic many times, and compare the observed value to that reference."
    ),
    (
        "cs1012-3.3.3-cp-01",
        "c",
    ): (
        "That choice finishes the permutation requirement with a Poisson chi-square GOF. "
        "That is a different procedure from a permutation reference distribution."
    ),
    (
        "cs1012-3.3.3-cp-01",
        "d",
    ): (
        "That choice builds a percentile CI by resampling with replacement and calls rejecting when zero is outside a permutation test. "
        "That is bootstrap CI logic, not label permutation under H0."
    ),
    # --- cs1012-3.3.4-ar-01 ---
    (
        "cs1012-3.3.4-ar-01",
        "b",
    ): (
        "That choice equates GOF with a two-way independence test that always uses row and column totals. "
        "GOF compares one sample to a stated distribution; independence in a contingency table is a different chi-square procedure."
    ),
    (
        "cs1012-3.3.4-ar-01",
        "c",
    ): (
        "That choice increases degrees of freedom when parameters are estimated. "
        "Estimating parameters from the same sample reduces DF under CMP rules."
    ),
    (
        "cs1012-3.3.4-ar-01",
        "d",
    ): (
        "That choice sets expected frequencies equal to observed frequencies so chi-square is automatically zero. "
        "Expected counts come from the hypothesised probabilities (and fitted parameters), not from copying the observed table."
    ),
    # --- cs1012-3.3.4-cp-01 ---
    (
        "cs1012-3.3.4-cp-01",
        "b",
    ): (
        "That choice uses lambda-hat in expected counts but leaves DF at bins - 1. "
        "Subtract one more for the estimated Poisson mean: DF = bins - 1 - 1."
    ),
    (
        "cs1012-3.3.4-cp-01",
        "c",
    ): (
        "That choice replaces Poisson GOF with a two-way independence test because lambda is estimated. "
        "Estimating lambda still leaves a one-sample GOF to the fitted Poisson probabilities."
    ),
    (
        "cs1012-3.3.4-cp-01",
        "d",
    ): (
        "That choice sets every expected count to n / lambda-hat, ignoring Poisson probabilities by bin. "
        "Expected counts are n times the fitted Poisson probability in each bin."
    ),
    # --- cs1012-3.3.5-ar-01 ---
    (
        "cs1012-3.3.5-ar-01",
        "b",
    ): (
        "That choice treats independence testing as one-sample GOF to a named distribution such as Poisson. "
        "Independence uses product-of-margins expected counts in a two-way table, not a named one-sample law."
    ),
    (
        "cs1012-3.3.5-ar-01",
        "c",
    ): (
        "That choice sets every expected cell to n divided by the number of cells. "
        "Under independence, E_ij uses (row total \u00d7 column total) / n from the observed margins."
    ),
    (
        "cs1012-3.3.5-ar-01",
        "d",
    ): (
        "That choice claims a contingency table classifies only one factor. "
        "A two-way table cross-classifies two criteria under an independence null."
    ),
    # --- cs1012-3.3.5-cp-01 ---
    (
        "cs1012-3.3.5-cp-01",
        "b",
    ): (
        "That choice puts a fitted Poisson GOF hypothesis in place of independence. "
        "For rating \u00d7 claim/no-claim, H0 is independence with E_ij = (row total \u00d7 column total) / n."
    ),
    (
        "cs1012-3.3.5-cp-01",
        "c",
    ): (
        "That choice sets expected counts equal to observed counts under an independence null. "
        "That forces chi-square to zero and is not the independence construction."
    ),
    (
        "cs1012-3.3.5-cp-01",
        "d",
    ): (
        "That choice forms E_ij as row total + column total without dividing by n. "
        "Independence expected counts are the product of marginal totals divided by n."
    ),
    # --- cs1016-3.2.1-ar-01 ---
    (
        "cs1016-3.2.1-ar-01",
        "b",
    ): (
        "That choice reads a CI as a probability that the next observation falls inside the interval. "
        "A CI targets an unknown parameter with frequentist coverage, not the next observation."
    ),
    (
        "cs1016-3.2.1-ar-01",
        "c",
    ): (
        "That choice collapses a CI into the same accept/reject procedure as a hypothesis test. "
        "Interval estimation and testing are related but not the same object."
    ),
    (
        "cs1016-3.2.1-ar-01",
        "d",
    ): (
        "That choice assigns 95% probability that the parameter equals the interval midpoint after seeing the data. "
        "Coverage is about the procedure and the parameter interval, not a midpoint probability."
    ),
    # --- cs1016-3.2.1-cp-01 ---
    (
        "cs1016-3.2.1-cp-01",
        "b",
    ): (
        "That choice reads (80, 100) as a 95% chance the next claim falls there. "
        "Coverage is for mu under repeated sampling, not for the next claim."
    ),
    (
        "cs1016-3.2.1-cp-01",
        "c",
    ): (
        "That choice treats the interval as a hypothesis test that automatically rejects every null outside (80, 100). "
        "A CI is not by itself that decision procedure."
    ),
    (
        "cs1016-3.2.1-cp-01",
        "d",
    ): (
        "That choice sets P(mu = 90) = 95% because 90 is the midpoint. "
        "Frequentist coverage does not put a 95% probability on the midpoint."
    ),
    # --- cs1016-3.3.1-ar-01 ---
    (
        "cs1016-3.3.1-ar-01",
        "b",
    ): (
        "That choice swaps Type I and Type II. "
        "Type I is rejecting a true null; Type II is failing to reject a false null."
    ),
    (
        "cs1016-3.3.1-ar-01",
        "c",
    ): (
        "That choice confines null and alternative to linear regression fitting and removes them from hypothesis-testing vocabulary. "
        "Those labels are foundational HT language, not a regression-only device."
    ),
    (
        "cs1016-3.3.1-ar-01",
        "d",
    ): (
        "That choice treats Type I and Type II as the same event whenever p < 5%. "
        "They remain distinct error types; a small p-value does not merge them."
    ),
    # --- cs1016-3.3.1-cp-01 ---
    (
        "cs1016-3.3.1-cp-01",
        "b",
    ): (
        "That choice swaps the fraud errors: Type I as missed fraud and Type II as a false fraud flag. "
        "With H0 = genuine, Type I is flagging fraud when genuine and Type II is missing fraud when present."
    ),
    (
        "cs1016-3.3.1-cp-01",
        "c",
    ): (
        "That choice treats a software z-test click as making Type I/II, p-value, and power optional. "
        "Those definitions still frame the test; a click does not replace them."
    ),
    (
        "cs1016-3.3.1-cp-01",
        "d",
    ): (
        "That choice equates HT foundations with fitting a linear regression of loss on covariates. "
        "Regression fitting is a different topic from Type I/II, p-value, and power."
    ),
}

def _scoreable_for(item_id: str) -> ScoreablePracticeItem:
    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    for stem, want_id in _PROTOTYPE_PACKAGES:
        if want_id != item_id:
            continue
        packs = [
            p
            for p in loader.all_approved()
            if p.source_path and Path(p.source_path).stem == stem
        ]
        assert packs, f"package for {stem} not found"
        pack = packs[0]
        substance = substance_from_package(
            pack,
            curriculum_identity=f"CS1:choice-aware:{stem}",
            topic_id=pack.topic_code,
        )
        for act in substance.activities:
            if (
                act.stage is EducationalStage.PRACTICE
                and act.scoreable is not None
                and act.scoreable.item_id == item_id
            ):
                return act.scoreable
        raise AssertionError(f"scoreable {item_id} not found in {stem}")
    raise AssertionError(f"unknown prototype item_id {item_id}")


def test_prototype_allowlist_is_exactly_one_hundred_forty_two_items() -> None:
    assert PROTOTYPE_ITEM_IDS == {want for _, want in _PROTOTYPE_PACKAGES}
    assert len(PROTOTYPE_ITEM_IDS) == 142
    assert len(_ORIGINAL_PILOT_PACKAGES) == 4
    assert len(_EXPANSION_PACKAGES) == 10
    assert len(_EXISTING_FOURTEEN_PACKAGES) == 14
    assert len(_CAF_WAVE1_PACKAGES) == 10
    assert len(_PRIOR_TWENTY_FOUR_PACKAGES) == 24
    assert len(_CREDIBILITY_WAVE_PACKAGES) == 4
    assert len(_PRIOR_TWENTY_EIGHT_PACKAGES) == 28
    assert len(_CAF_WAVE3_PACKAGES) == 31
    assert len(_CAF_WAVE3_CONFLICT_NUMERIC_CPS) == 4
    assert len(_PRIOR_FIFTY_NINE_PACKAGES) == 59
    assert len(_CAF_WAVE4_PACKAGES) == 41
    assert len(_CAF_WAVE4_CONFLICT_NUMERIC_CPS) == 2
    assert len(_PRIOR_ONE_HUNDRED_PACKAGES) == 100
    assert len(_CAF_WAVE5_PACKAGES) == 42


def test_original_four_pilot_items_unaffected() -> None:
    """Expansion must not alter the original four items' authored copy."""
    original_ids = {want for _, want in _ORIGINAL_PILOT_PACKAGES}
    assert original_ids <= PROTOTYPE_ITEM_IDS
    for key, text in _ORIGINAL_PILOT_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == text
    for item_id in sorted(original_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _ORIGINAL_PILOT_FEEDBACK[(item_id, cid)]


def test_existing_fourteen_live_items_unaffected() -> None:
    """CAF Wave 1 must leave the prior 14 items byte-identical."""
    existing_ids = {want for _, want in _EXISTING_FOURTEEN_PACKAGES}
    assert existing_ids <= PROTOTYPE_ITEM_IDS
    assert len(_EXISTING_FOURTEEN_FEEDBACK) == 42
    for key, text in _EXISTING_FOURTEEN_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == text
    for item_id in sorted(existing_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _EXISTING_FOURTEEN_FEEDBACK[(item_id, cid)]


def test_wrong_answers_on_same_item_yield_distinct_choice_aware_feedback() -> None:
    item = _scoreable_for("cs1014-4.2.1-ar-01")
    assert item.response_type is PracticeResponseType.MCQ

    bad_b = score_practice_response(item, "b")
    bad_c = score_practice_response(item, "c")
    assert bad_b.scored is True and bad_b.correct is False
    assert bad_c.scored is True and bad_c.correct is False
    assert bad_b.common_mistake != bad_c.common_mistake
    assert bad_b.common_mistake == PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1014-4.2.1-ar-01", "b")
    ]
    assert bad_c.common_mistake == PROTOTYPE_CHOICE_FEEDBACK[
        ("cs1014-4.2.1-ar-01", "c")
    ]
    # Distinct from the bundled generic common_mistake.
    assert bad_b.common_mistake != item.common_mistake
    assert bad_c.common_mistake != item.common_mistake


def test_expansion_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 10 expansion items returns approved copy per distractor."""
    for _, item_id in _EXPANSION_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)]
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_caf_wave1_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 10 CAF Wave 1 items returns approved copy per distractor."""
    for _, item_id in _CAF_WAVE1_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)]
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_prior_twenty_four_live_items_unaffected() -> None:
    """Credibility wave must leave the prior 24 items byte-identical."""
    prior_ids = {want for _, want in _PRIOR_TWENTY_FOUR_PACKAGES}
    assert prior_ids <= PROTOTYPE_ITEM_IDS
    assert len(prior_ids) == 24
    assert len(_PRIOR_TWENTY_FOUR_FEEDBACK) == 72
    for key, text in _PRIOR_TWENTY_FOUR_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == text
    for item_id in sorted(prior_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _PRIOR_TWENTY_FOUR_FEEDBACK[(item_id, cid)]


def test_credibility_wave_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 4 credibility-wave AR items returns approved copy per distractor."""
    assert len(_CREDIBILITY_WAVE_FEEDBACK) == 12
    for _, item_id in _CREDIBILITY_WAVE_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = _CREDIBILITY_WAVE_FEEDBACK[(item_id, cid)]
            assert PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)] == expected
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_correct_answer_path_unaffected() -> None:
    item = _scoreable_for("cs1010-3.1.3-cp-01")
    ok = score_practice_response(item, "a")
    assert ok.scored is True
    assert ok.correct is True
    assert ok.feedback_outcome == "Correct"
    assert ok.common_mistake == ""
    assert ok.selected_misconception_tag == ""
    assert ok.explanation == item.explanation
    assert ok.model_answer == item.model_answer
    assert ok.marks_awarded == float(item.mark_scheme.max_marks)


def test_scoring_correctness_logic_unchanged_for_choice_tuples() -> None:
    """_match_mcq returns the same verdicts with or without misconception_tag."""
    item = _scoreable_for("cs1017-2.1.2-cp-01")
    stripped_choices = tuple((c[0], c[1]) for c in item.choices)
    stripped = ScoreablePracticeItem(
        item_id=item.item_id,
        prompt=item.prompt,
        response_type=item.response_type,
        answer_key=item.answer_key,
        explanation=item.explanation,
        model_answer=item.model_answer,
        mark_scheme=item.mark_scheme,
        common_mistake=item.common_mistake,
        next_action=item.next_action,
        choices=stripped_choices,
        emit_structured=item.emit_structured,
        body=item.body,
        supporting_material=item.supporting_material,
        hints=item.hints,
    )
    for response in ("a", "b", "c", "d"):
        assert _match_mcq(item, response) == _match_mcq(stripped, response)


def test_misconception_tag_captured_on_score_and_evidence_log() -> None:
    item = _scoreable_for("cs1010-ck-r1-cp-01")
    bad = score_practice_response(item, "b")
    assert bad.correct is False
    assert bad.selected_misconception_tag == "unsquared_bias"
    opaque = bad.to_opaque()
    assert opaque["selected_misconception_tag"] == "unsquared_bias"
    # Tag must not appear in student-facing common_mistake copy.
    assert "unsquared_bias" not in bad.common_mistake

    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    packs = [
        p
        for p in loader.all_approved()
        if p.source_path and Path(p.source_path).stem == "revision-estimators-cs1010"
    ]
    assert packs
    pack = packs[0]
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:choice-aware-evidence",
        topic_id=pack.topic_code,
    )
    store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=store)
    engine = PackageActivityEngine(store=store, persistence=persistence)
    engine.provision_sequence("stu-ca", session_id="sess-ca", substance=substance)

    current = engine.get_current_activity_opaque("stu-ca", session_id="sess-ca")
    while current is not None:
        seq = store.get(
            PackageActivityEngine.NS_SEQUENCE,
            PackageActivityEngine._key("stu-ca", "sess-ca"),
        )
        assert seq is not None
        index = int(seq.get("index") or 1)
        act = list(seq.get("activities") or [])[index - 1]
        item_id = str((act.get("scoreable") or {}).get("item_id") or "")
        if item_id == "cs1010-ck-r1-cp-01":
            result = engine.submit_response_opaque(
                "stu-ca",
                session_id="sess-ca",
                activity_id=str(current["activity_id"]),
                response="b",
            )
            assert result.get("common_mistake") == PROTOTYPE_CHOICE_FEEDBACK[
                ("cs1010-ck-r1-cp-01", "b")
            ]
            responses = store.get(
                PackageActivityEngine.NS_RESPONSES,
                PackageActivityEngine._key("stu-ca", "sess-ca"),
            )
            assert responses is not None
            logged = responses["items"][-1]
            assert logged["selected_misconception_tag"] == "unsquared_bias"
            assert logged["score"]["selected_misconception_tag"] == "unsquared_bias"
            return
        engine.submit_response_opaque(
            "stu-ca",
            session_id="sess-ca",
            activity_id=str(current["activity_id"]),
            response="a" if current.get("response_type") == "mcq" else "noted",
        )
        current = engine.advance_activity_opaque("stu-ca", session_id="sess-ca")

    raise AssertionError("checkpoint practice item never reached")


def test_all_prototype_items_have_authored_feedback_for_distractors() -> None:
    for item_id in sorted(PROTOTYPE_ITEM_IDS):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            text, tag = assemble_choice_aware_mistake(item, cid, correct=False)
            assert (item_id, cid) in PROTOTYPE_CHOICE_FEEDBACK
            assert text == PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)]
            assert text != item.common_mistake
            assert tag  # every distractor carries a misconception_tag
            assert tag not in text  # slug not echoed to the student


def test_caf_wave1_items_live_render_in_session_feedback(app) -> None:
    """At least two CAF Wave 1 items display choice-aware copy in session HTML."""
    samples = (
        ("cs1010-ck-r1-ar-01", "b"),
        ("cs1003-5.1.3-cp-01", "c"),
    )
    for item_id, choice_id in samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html


def test_expansion_items_live_render_in_session_feedback(app) -> None:
    """At least two prior-expansion items still display choice-aware copy."""
    samples = (
        ("cs1003-5.1.1-ar-01", "b"),
        ("cs1010-3.1.4-cp-01", "c"),
    )
    for item_id, choice_id in samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html

def test_credibility_wave_items_live_render_in_session_feedback(app) -> None:
    """At least two credibility-wave AR items display choice-aware copy in session HTML."""
    samples = (
        ("cs1003-5.1.7-ar-01", "b"),
        ("cs1015-5.1.8-ar-01", "d"),
    )
    for item_id, choice_id in samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = _CREDIBILITY_WAVE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html


def test_prior_twenty_eight_live_items_unaffected() -> None:
    """CAF Wave 3 must leave the prior 28 items byte-identical."""
    prior_ids = {want for _, want in _PRIOR_TWENTY_EIGHT_PACKAGES}
    assert prior_ids <= PROTOTYPE_ITEM_IDS
    assert len(prior_ids) == 28
    assert len(_PRIOR_TWENTY_EIGHT_FEEDBACK) == 84
    for key, frozen in _PRIOR_TWENTY_EIGHT_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == frozen
    for item_id in sorted(prior_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _PRIOR_TWENTY_EIGHT_FEEDBACK[(item_id, cid)]


def test_caf_wave3_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 31 Wave 3 items returns approved copy for every wrong choice."""
    assert len(_CAF_WAVE3_FEEDBACK) == 93
    for _, item_id in _CAF_WAVE3_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = _CAF_WAVE3_FEEDBACK[(item_id, cid)]
            assert PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)] == expected
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert "\u2014" not in expected
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_four_conflict_cps_are_numeric_without_choice_aware_wiring() -> None:
    """Conflict CPs ship numeric only; sibling ARs stay on the CAF allowlist."""
    sibling_ars = {
        "cs1016-5.1.1-cp-01": "cs1016-5.1.1-ar-01",
        "cs1003-5.1.4-cp-01": "cs1003-5.1.4-ar-01",
        "cs1015-5.1.4-cp-01": "cs1015-5.1.4-ar-01",
        "cs1010-3.1.6-cp-01": "cs1010-3.1.6-ar-01",
    }
    for cp_id in _CAF_WAVE3_CONFLICT_NUMERIC_CPS:
        assert cp_id not in PROTOTYPE_ITEM_IDS
        assert not any(k[0] == cp_id for k in PROTOTYPE_CHOICE_FEEDBACK)
        assert sibling_ars[cp_id] in PROTOTYPE_ITEM_IDS

    reset_educational_package_cache()
    accepted = {
        "cs1016-5.1.1-cp-01": "0.0876",
        "cs1003-5.1.4-cp-01": "5.45",
        "cs1015-5.1.4-cp-01": "2.1",
        "cs1010-3.1.6-cp-01": "8.602",
    }
    for pack in EducationalPackageLoader().all_approved():
        for check in pack.knowledge_checks:
            if check.item_id not in _CAF_WAVE3_CONFLICT_NUMERIC_CPS:
                continue
            assert check.response_type == "numeric"
            assert check.accepted_keywords[0] == accepted[check.item_id]
            assert check.numeric_tolerance == 0.001
            assert not check.choices


def test_caf_wave3_and_numeric_wave3_live_render_in_session_feedback(app) -> None:
    """Sample newly wired CAF and numeric items display correctly in session HTML."""
    caf_samples = (
        ("cs1003-5.1.5-ar-01", "b"),
        ("cs1003-4.2.1-ar-01", "c"),
        ("cs1010-3.1.1-ar-01", "d"),
    )
    for item_id, choice_id in caf_samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html

    from tests.application.learning_session.test_numeric_parse import (
        _scoreable_by_item_id,
    )

    for item_id, response in (
        ("cs1016-5.1.1-cp-01", "0.0876"),
        ("cs1003-5.1.4-cp-01", "5.45"),
    ):
        item = _scoreable_by_item_id(item_id)
        scored = score_practice_response(item, response)
        assert scored.correct is True

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=response,
            response_type="numeric",
            scored_correct=True,
            practice_choices=(),
        )
        assert parts["what_happened"]

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=response,
            response_type="numeric",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert "Correct" in html or parts["what_happened"] in html

def test_prior_fifty_nine_live_items_unaffected() -> None:
    """CAF Wave 4 must leave the prior 59 items byte-identical."""
    prior_ids = {want for _, want in _PRIOR_FIFTY_NINE_PACKAGES}
    assert prior_ids <= PROTOTYPE_ITEM_IDS
    assert len(prior_ids) == 59
    assert len(_PRIOR_FIFTY_NINE_FEEDBACK) == 177
    for key, frozen in _PRIOR_FIFTY_NINE_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == frozen
    for item_id in sorted(prior_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _PRIOR_FIFTY_NINE_FEEDBACK[(item_id, cid)]


def test_caf_wave4_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 41 Wave 4 items returns approved copy for every wrong choice."""
    assert len(_CAF_WAVE4_FEEDBACK) == 123
    for _, item_id in _CAF_WAVE4_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = _CAF_WAVE4_FEEDBACK[(item_id, cid)]
            assert PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)] == expected
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert "—" not in expected
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_two_wave4_conflict_cps_are_numeric_without_choice_aware_wiring() -> None:
    """Wave 4 conflict CPs ship numeric only; sibling ARs stay on the CAF allowlist."""
    sibling_ars = {
        "cs1003-4.2.5-cp-01": "cs1003-4.2.5-ar-01",
        "cs1003-4.2.8-cp-01": "cs1003-4.2.8-ar-01",
    }
    for cp_id in _CAF_WAVE4_CONFLICT_NUMERIC_CPS:
        assert cp_id not in PROTOTYPE_ITEM_IDS
        assert not any(k[0] == cp_id for k in PROTOTYPE_CHOICE_FEEDBACK)
        assert sibling_ars[cp_id] in PROTOTYPE_ITEM_IDS
        assert sibling_ars[cp_id] in {want for _, want in _CAF_WAVE4_PACKAGES}

    reset_educational_package_cache()
    accepted = {
        "cs1003-4.2.5-cp-01": "3.9749",
        "cs1003-4.2.8-cp-01": "-1.2247",
    }
    for pack in EducationalPackageLoader().all_approved():
        for check in pack.knowledge_checks:
            if check.item_id not in _CAF_WAVE4_CONFLICT_NUMERIC_CPS:
                continue
            assert check.response_type == "numeric"
            assert check.accepted_keywords[0] == accepted[check.item_id]
            assert check.numeric_tolerance == 0.001
            assert not check.choices


def test_caf_wave4_and_numeric_wave4_live_render_in_session_feedback(app) -> None:
    """Sample newly wired CAF and numeric items display correctly in session HTML."""
    caf_samples = (
        ("cs1003-4.2.4-ar-01", "b"),
        ("cs1002-2.1a-cp-01", "c"),
        ("cs1014-cx-r1-ar-01", "d"),
    )
    for item_id, choice_id in caf_samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html

    from tests.application.learning_session.test_numeric_parse import (
        _scoreable_by_item_id,
    )

    for item_id, response in (
        ("cs1003-4.2.5-cp-01", "3.9749"),
        ("cs1003-4.2.8-cp-01", "-1.2247"),
    ):
        item = _scoreable_by_item_id(item_id)
        scored = score_practice_response(item, response)
        assert scored.correct is True

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=response,
            response_type="numeric",
            scored_correct=True,
            practice_choices=(),
        )
        assert parts["what_happened"]

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=response,
            response_type="numeric",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert "Correct" in html or parts["what_happened"] in html

def test_prior_one_hundred_live_items_unaffected() -> None:
    """CAF Wave 5 must leave the prior 100 choice-aware items byte-identical."""
    prior_ids = {want for _, want in _PRIOR_ONE_HUNDRED_PACKAGES}
    assert prior_ids <= PROTOTYPE_ITEM_IDS
    assert len(prior_ids) == 100
    assert len(_PRIOR_ONE_HUNDRED_FEEDBACK) == 300
    for key, frozen in _PRIOR_ONE_HUNDRED_FEEDBACK.items():
        assert PROTOTYPE_CHOICE_FEEDBACK[key] == frozen
    for item_id in sorted(prior_ids):
        item = _scoreable_for(item_id)
        correct_id = item.answer_key.correct_choice_id
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            scored = score_practice_response(item, cid)
            assert scored.correct is False
            assert scored.common_mistake == _PRIOR_ONE_HUNDRED_FEEDBACK[(item_id, cid)]


def test_caf_wave5_items_yield_specific_choice_aware_feedback() -> None:
    """Each of the 42 Wave 5 items returns approved copy for every wrong choice."""
    assert len(_CAF_WAVE5_FEEDBACK) == 126
    for _, item_id in _CAF_WAVE5_PACKAGES:
        item = _scoreable_for(item_id)
        assert item.response_type is PracticeResponseType.MCQ
        correct_id = item.answer_key.correct_choice_id
        assert correct_id == "a"
        seen: set[str] = set()
        for choice in item.choices:
            cid = choice[0]
            if cid == correct_id:
                continue
            assert cid in {"b", "c", "d"}
            scored = score_practice_response(item, cid)
            assert scored.scored is True and scored.correct is False
            expected = _CAF_WAVE5_FEEDBACK[(item_id, cid)]
            assert PROTOTYPE_CHOICE_FEEDBACK[(item_id, cid)] == expected
            assert scored.common_mistake == expected
            assert scored.common_mistake != item.common_mistake
            assert "—" not in expected
            assert expected not in seen
            seen.add(expected)
        assert len(seen) == 3


def test_thirty_live_numeric_checkpoints_unaffected_by_caf_wave5() -> None:
    """Wave 5 adds no numeric conversions; the existing 30 numeric CPs stay numeric."""
    from tests.application.learning_session.test_numeric_parse import (
        LIVE_NUMERIC_ACCEPTED,
    )

    assert len(LIVE_NUMERIC_ACCEPTED) == 30
    reset_educational_package_cache()
    found: dict[str, tuple[str, float | None]] = {}
    for pack in EducationalPackageLoader().all_approved():
        for check in pack.knowledge_checks:
            if check.kind == "checkpoint" and check.response_type == "numeric":
                found[check.item_id] = (
                    check.accepted_keywords[0],
                    check.numeric_tolerance,
                )
    assert len(found) == 30
    for item_id, accepted, tol in LIVE_NUMERIC_ACCEPTED:
        assert item_id not in PROTOTYPE_ITEM_IDS
        assert not any(k[0] == item_id for k in PROTOTYPE_CHOICE_FEEDBACK)
        assert item_id in found
        assert found[item_id][0] == accepted
        assert found[item_id][1] == tol


def test_caf_wave5_live_render_in_session_feedback(app) -> None:
    """Sample newly wired CAF items display correctly, including markup-fixed CPs."""
    caf_samples = (
        ("cs1005-2.2.1-ar-01", "b"),
        ("cs1011-3.2.6-cp-01", "d"),
        ("cs1011-3.2.7-cp-01", "c"),
        ("cs1016-3.3.1-cp-01", "d"),
    )
    for item_id, choice_id in caf_samples:
        item = _scoreable_for(item_id)
        scored = score_practice_response(item, choice_id)
        assert scored.correct is False
        expected = PROTOTYPE_CHOICE_FEEDBACK[(item_id, choice_id)]
        assert scored.common_mistake == expected

        parts = _practice_feedback_parts(
            outcome=scored.feedback_outcome,
            explanation=scored.explanation,
            common_mistake=scored.common_mistake,
            submitted_response=choice_id,
            response_type="mcq",
            scored_correct=False,
            practice_choices=tuple((c[0], c[1]) for c in item.choices),
        )
        assert parts["what_to_understand"] == expected

        study = _base_page(
            content_stage="practice",
            stage_position_label="Practice",
            feedback_what_happened=parts["what_happened"],
            feedback_what_it_means=parts["what_it_means"],
            feedback_what_to_understand=parts["what_to_understand"],
            feedback_locked=True,
            submitted_response=choice_id,
            response_type="mcq",
            show_answer_input=False,
            common_mistake=scored.common_mistake,
        )
        html = _render(app, study)
        assert 'data-feedback-what-to-understand="true"' in html
        assert expected in html

    # Markup-fixed choice labels must keep closed mu subscripts through markup prep.
    from app.presentation.session.math_markup import prepare_math_markup

    for item_id, choice_id, needles in (
        ("cs1011-3.2.6-cp-01", "d", (r"\mu_{A}", r"\mu_{B}")),
        ("cs1011-3.2.7-cp-01", "c", (r"\mu_{X}", r"\mu_{Y}")),
    ):
        item = _scoreable_for(item_id)
        label = next(c[1] for c in item.choices if c[0] == choice_id)
        assert "$_" not in label
        for needle in needles:
            assert needle in label
        assert prepare_math_markup(label) == label
