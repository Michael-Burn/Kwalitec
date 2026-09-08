"""Wave 11: catalogue-wide manual-review close-out (batches 1–3).

Applies the locked classifications from
``docs/handoff/MATH_NOTATION_WAVE11_MANUAL_REVIEW.md`` (batch 1: 64 of 239),
``docs/handoff/MATH_NOTATION_WAVE11_BATCH2_MANUAL_REVIEW.md`` (batch 2:
60 of the 175 remaining after batch 1), and
``docs/handoff/MATH_NOTATION_WAVE11_BATCH3_MANUAL_REVIEW.md`` (batch 3:
62 of the 115 remaining after batch 2).

This module is the locked record of package files and field paths touched by
each batch. Application of package text and ``_MANUAL_PROSE_EXCLUSIONS`` is done
in the content commit; re-run ``scripts/inventory_math_notation.py`` after.
"""

from __future__ import annotations

WAVE11_BATCH1_FILES: tuple[str, ...] = (
    "1.2.2-eda-association-ep001.json",
    "2.1.2-continuous-cs1002.json",
    "2.1.3-prob-quantiles-cs1004.json",
    "2.1.4-poisson-process-cs1004.json",
    "2.1.6-software-generation-cs1004.json",
    "2.2.4-linear-combinations-cs1005.json",
    "2.5.2-simulated-sample-normal-cs1008.json",
    "2.6.2-sampling-distribution-statistic-cs1009.json",
    "2.6.3-mean-var-sample-cs1009.json",
    "2.6.4-normal-sample-mean-var-cs1009.json",
    "2.6.5-t-statistic-cs1009.json",
    "2.6.6-f-distribution-cs1009.json",
    "3.1.1-method-of-moments-cs1010.json",
    "3.1.4-comparison-mse-cs1010.json",
    "3.1.5-asymptotic-mle-cs1010.json",
    "3.1.6-bootstrap-estimator-cs1010.json",
    "3.2.1-confidence-interval-parameter-cs1011.json",
    "3.2.2-prediction-interval-cs1011.json",
    "3.2.3-ci-given-sampling-distribution-cs1011.json",
    "3.2.4-ci-normal-mean-variance-cs1011.json",
)

WAVE11_BATCH2_FILES: tuple[str, ...] = (
    "3.2.5-ci-binomial-poisson-cs1011.json",
    "3.2.6-ci-two-sample-cs1011.json",
    "3.2.8-bootstrap-confidence-interval-cs1011.json",
    "3.3.1-hypothesis-concepts-cs1012.json",
    "3.3.2-basic-tests-cs1012.json",
    "3.3.3-permutation-tests-cs1012.json",
    "3.3.4-chi-square-gof-cs1012.json",
    "3.3.5-contingency-independence-cs1012.json",
    "4.1.2-simple-multiple-cs1003.json",
    "4.1.2-simple-multiple-cs1013.json",
    "4.1.4-software-fit-cs1013.json",
    "4.1.4-software-inference-cs1003.json",
    "4.1.5-variable-selection-cs1003.json",
    "4.1.5-variable-selection-cs1013.json",
    "4.2.1-exponential-family-cs1003.json",
    "4.2.1-exponential-family-cs1014.json",
    "4.2.10-fit-interpret-cs1014.json",
    "4.2.2-mean-variance-cs1003.json",
    "4.2.2-mean-variance-cs1014.json",
    "4.2.3-link-canonical-cs1003.json",
    "4.2.3-link-canonical-cs1014.json",
    "4.2.4-factors-interactions-cs1003.json",
)

WAVE11_BATCH3_FILES: tuple[str, ...] = (
    "4.2.4-factors-interactions-cs1014.json",
    "4.2.5-linear-predictor-cs1003.json",
    "4.2.5-linear-predictor-cs1014.json",
    "4.2.6-deviance-estimation-cs1014.json",
    "4.2.7-model-choice-cs1003.json",
    "4.2.7-model-choice-cs1014.json",
    "4.2.9-goodness-tests-cs1003.json",
    "4.2.9-goodness-tests-cs1014.json",
    "5.1.2-prior-posterior-cs1003.json",
    "5.1.2-prior-posterior-cs1015.json",
    "5.1.3-posterior-simple-cs1015.json",
    "5.1.4-loss-estimators-cs1015.json",
    "5.1.5-credible-intervals-cs1015.json",
    "5.1.6-credibility-premium-cs1003.json",
)

# Packages that still carry needs_manual_review after batches 1–3 (remainder).
WAVE11_REMAINDER_START_PACKAGE = "5.1.6-credibility-premium-cs1015.json"

WAVE11_REMAINDER_PACKAGES: tuple[str, ...] = (
    "5.1.6-credibility-premium-cs1015.json",
    "5.1.7-bayesian-credibility-cs1003.json",
    "5.1.7-bayesian-credibility-cs1015.json",
    "5.1.8-empirical-bayes-cs1003.json",
    "5.1.8-empirical-bayes-cs1015.json",
    "5.1.9-bayes-vs-eb-cs1003.json",
    "5.1.9-bayes-vs-eb-cs1015.json",
    "cp-3.1.1-estimators-cs1016.json",
    "cp-3.2.1-ci-sample-cs1016.json",
    "cp-3.3.1-hypothesis-testing-cs1016.json",
    "cr-1.2.2-correlation-cs1017.json",
    "cr-2.1.2-continuous-cs1017.json",
    "revision-confidence-intervals-cs1011.json",
    "revision-distributions-generation-cs1004.json",
    "revision-glm-cs1014.json",
    "revision-linear-models-cs1003.json",
    "revision-linear-regression-cs1013.json",
    "revision-regression-glm-cs1003.json",
    "revision-sampling-distributions-cs1009.json",
)
