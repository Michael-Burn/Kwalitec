"""Wave 11 batch 1: catalogue-wide manual-review close-out (64 strings).

Applies the locked classifications from
``docs/handoff/MATH_NOTATION_WAVE11_MANUAL_REVIEW.md`` for the first 64 of
239 provisionally-guessed prose strings (``correctly_excluded`` +
``needs_manual_review``).

This module is the locked record of package files and field paths touched by
batch 1. Application of package text and ``_MANUAL_PROSE_EXCLUSIONS`` is done
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

# Packages that still carry needs_manual_review after batch 1 (remainder tracker).
WAVE11_REMAINDER_START_PACKAGE = "3.2.5-ci-binomial-poisson-cs1011.json"
