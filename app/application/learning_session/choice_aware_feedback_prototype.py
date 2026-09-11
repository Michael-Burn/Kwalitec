"""Phase-0 prototype: choice-aware MCQ feedback for a fixed allowlist.

Proves misconception_tag plumbing and editorial feedback quality on 3–5 live
items before any full-inventory rollout. Correctness matching stays in
``score_practice_response`` / ``_match_mcq``; this module only supplies
student-facing mistake copy and the analytics tag for allowlisted items
(and resolves the tag for logging whenever a selected choice is known).

Do not expand ``PROTOTYPE_ITEM_IDS`` without an explicit editorial review.

Editorial review record (2026-09-09): ten additional items below were
reviewed and approved before wiring (Bayes cluster, MSE AR/CP siblings,
GLM CP sibling). Copy is frozen as approved; mechanism unchanged.

Editorial review record (2026-09-10): ten additional CAF Wave 1 items
were reviewed and approved before wiring (revision estimators AR,
continuous waiting AR, prior/posterior AR/CP twins, posterior-simple
AR/CP twins). Copy is frozen as approved; mechanism unchanged.

Editorial review record (2026-09-10): four Bayesian-credibility /
Empirical Bayes active-recall items (cs1003/cs1015 5.1.7 and 5.1.8)
were reviewed and approved before wiring as the choice-aware half of
the coordinated NUM Wave 2 / CAF credibility wave. Copy is frozen as
approved; mechanism unchanged.

Editorial review record (2026-09-10): thirty-one CAF Wave 3 items were
reviewed and approved before wiring (remaining P1 Bayesian/credibility
spine ARs and non-conflicting CPs, P2 estimator/MSE adjacency, and P3
GLM adjacency through 4.2.3). Four conflicting CPs from the same draft
(cs1016-5.1.1-cp-01, cs1003/cs1015-5.1.4-cp-01, cs1010-3.1.6-cp-01) were
converted to numeric instead and are intentionally not on this
allowlist, matching the 5.1.7/5.1.8 AR-only pattern. Copy is frozen as
approved; mechanism unchanged.

Editorial review record (2026-09-10): forty-one CAF Wave 4 items were
reviewed and approved before wiring (remaining P3 GLM/exponential-family
from 4.2.4 through revision, and entire P4 univariate 2.1 cluster). Two
conflicting CPs from the same draft (cs1003-4.2.5-cp-01, cs1003-4.2.8-cp-01)
were converted to numeric instead and are intentionally not on this
allowlist, matching the established AR-only pattern. Copy is frozen as
approved; mechanism unchanged.

Editorial review record (2026-09-10): forty-two CAF Wave 5 items were
reviewed and approved before wiring (entire remaining P5 joint/conditional
2.2-2.3 cluster, and P6 CI/hypothesis testing through learning plus
companion packages). No conflicting CPs in this draft; Part 3 found no
numeric conversion candidates. Copy is frozen as approved; mechanism
unchanged.

Editorial review record (2026-09-10): forty-three CAF Wave 6 items were
reviewed and approved before wiring (remaining P6 revision packages,
entire 4.1 linear regression cluster, and purpose/EDA Continuity Front
through purpose/EDA revision). No conflicting CPs in this draft; Part 3
found no numeric conversion candidates. Copy is frozen as approved;
mechanism unchanged. Item 26 twin feedback states the correct fact that
raw R-squared never decreases when variables are added; the source
distractor (d) now states the same fact as the premise of the wrong
selection rule (raw R-squared alone decides).

Editorial review record (2026-09-10): forty-eight CAF Final Wave items were
reviewed and approved before wiring (CR Publication Front 1.1/1.2 + revision,
sampling 2.6 including companions, CLT/MGF cluster, and misc revision/
companion packages). This closes the choice-aware feedback content expansion
for this programme. Two superseded outside-named leftovers (ea005-4.2-ar-01,
ea005-4.2-cp-01) remain intentionally unwired, matching the session policy
of excluding superseded package content from live CAF counts. No conflicting
CPs in this draft; Part 3 found no numeric conversion candidates. Copy is
frozen as approved; mechanism unchanged.
"""

from __future__ import annotations

from app.application.learning_session.scoreable_practice import (
    ScoreablePracticeItem,
    _normalise,
    choice_parts,
)

# Live Knowledge Check item_ids only — Batch 1 estimators (numeric),
# Batch 2 GLM, Batch 3 Rho conceptual vignette, Batch 6B revision,
# plus editorially reviewed expansions (Bayes / MSE / GLM siblings;
# CAF Wave 1 prior/posterior / posterior-simple / estimators AR;
# NUM Wave 2 / CAF credibility AR siblings;
# CAF Wave 3 remaining P1 / P2 / P3-through-4.2.3;
# CAF Wave 4 remaining P3 from 4.2.4 + entire P4 univariate 2.1;
# CAF Wave 5 remaining P5 joint/conditional + P6 CI/HT through companions;
# CAF Wave 6 P6 revisions + 4.1 linear regression + purpose/EDA Continuity Front;
# CAF Final Wave CR Publication Front + sampling 2.6 + CLT/MGF + misc
# revisions/companions; superseded ea005-4.2 leftovers intentionally excluded).
PROTOTYPE_ITEM_IDS: frozenset[str] = frozenset(
    {
        "cs1010-3.1.3-cp-01",  # Batch 1 — efficiency / MSE comparison
        "cs1014-4.2.1-ar-01",  # Batch 2 — exponential-family GLM
        "cs1017-2.1.2-cp-01",  # Batch 3 — Rho continuous waiting times
        "cs1010-ck-r1-cp-01",  # Batch 6B — revision MSE identity
        "cs1003-5.1.1-ar-01",  # Expansion: Bayes theorem AR (cs1003)
        "cs1003-5.1.1-cp-01",  # Expansion: Bayes theorem CP (cs1003)
        "cs1015-5.1.1-ar-01",  # Expansion: Bayes theorem AR (cs1015)
        "cs1015-5.1.1-cp-01",  # Expansion: Bayes theorem CP (cs1015)
        "cs1015-co-r1-ar-01",  # Expansion: Bayesian revision AR
        "cs1015-co-r1-cp-01",  # Expansion: Bayesian revision CP
        "cs1010-3.1.3-ar-01",  # Expansion: efficiency / bias / MSE AR
        "cs1010-3.1.4-ar-01",  # Expansion: MSE comparison AR
        "cs1010-3.1.4-cp-01",  # Expansion: MSE comparison CP
        "cs1014-4.2.1-cp-01",  # Expansion: exponential-family GLM CP
        "cs1010-ck-r1-ar-01",  # CAF Wave 1: revision estimators AR
        "cs1017-2.1.2-ar-01",  # CAF Wave 1: continuous waiting AR
        "cs1003-5.1.2-ar-01",  # CAF Wave 1: prior/posterior AR (cs1003)
        "cs1003-5.1.2-cp-01",  # CAF Wave 1: prior/posterior CP (cs1003)
        "cs1015-5.1.2-ar-01",  # CAF Wave 1: prior/posterior AR (cs1015)
        "cs1015-5.1.2-cp-01",  # CAF Wave 1: prior/posterior CP (cs1015)
        "cs1003-5.1.3-ar-01",  # CAF Wave 1: posterior-simple AR (cs1003)
        "cs1003-5.1.3-cp-01",  # CAF Wave 1: posterior-simple CP (cs1003)
        "cs1015-5.1.3-ar-01",  # CAF Wave 1: posterior-simple AR (cs1015)
        "cs1015-5.1.3-cp-01",  # CAF Wave 1: posterior-simple CP (cs1015)
        "cs1003-5.1.7-ar-01",  # NUM/CAF Wave 2: Bayesian credibility AR (cs1003)
        "cs1015-5.1.7-ar-01",  # NUM/CAF Wave 2: Bayesian credibility AR (cs1015)
        "cs1003-5.1.8-ar-01",  # NUM/CAF Wave 2: Empirical Bayes AR (cs1003)
        "cs1015-5.1.8-ar-01",  # NUM/CAF Wave 2: Empirical Bayes AR (cs1015)
        "cs1003-5.1.4-ar-01",  # CAF Wave 3: loss estimators AR (cs1003)
        "cs1015-5.1.4-ar-01",  # CAF Wave 3: loss estimators AR (cs1015)
        "cs1003-5.1.5-ar-01",  # CAF Wave 3: credible intervals AR (cs1003)
        "cs1003-5.1.5-cp-01",  # CAF Wave 3: credible intervals CP (cs1003)
        "cs1015-5.1.5-ar-01",  # CAF Wave 3: credible intervals AR (cs1015)
        "cs1015-5.1.5-cp-01",  # CAF Wave 3: credible intervals CP (cs1015)
        "cs1003-5.1.6-ar-01",  # CAF Wave 3: credibility premium AR (cs1003)
        "cs1015-5.1.6-ar-01",  # CAF Wave 3: credibility premium AR (cs1015)
        "cs1003-5.1.9-ar-01",  # CAF Wave 3: Bayes vs EB AR (cs1003)
        "cs1003-5.1.9-cp-01",  # CAF Wave 3: Bayes vs EB CP (cs1003)
        "cs1015-5.1.9-ar-01",  # CAF Wave 3: Bayes vs EB AR (cs1015)
        "cs1015-5.1.9-cp-01",  # CAF Wave 3: Bayes vs EB CP (cs1015)
        "cs1016-5.1.1-ar-01",  # CAF Wave 3: companion Bayes AR
        "cs1003-cd-r3-ar-01",  # CAF Wave 3: revision midspine AR
        "cs1003-cd-r3-cp-01",  # CAF Wave 3: revision midspine CP
        "cs1010-3.1.1-ar-01",  # CAF Wave 3: MoM AR
        "cs1010-3.1.2-ar-01",  # CAF Wave 3: MLE AR
        "cs1010-3.1.5-ar-01",  # CAF Wave 3: asymptotic MLE AR
        "cs1010-3.1.5-cp-01",  # CAF Wave 3: asymptotic MLE CP
        "cs1010-3.1.6-ar-01",  # CAF Wave 3: bootstrap AR
        "cs1016-3.1.1-ar-01",  # CAF Wave 3: companion estimators AR
        "cs1003-4.2.1-ar-01",  # CAF Wave 3: exponential-family AR (cs1003)
        "cs1003-4.2.1-cp-01",  # CAF Wave 3: exponential-family CP (cs1003)
        "cs1003-4.2.2-ar-01",  # CAF Wave 3: mean-variance AR (cs1003)
        "cs1003-4.2.2-cp-01",  # CAF Wave 3: mean-variance CP (cs1003)
        "cs1014-4.2.2-ar-01",  # CAF Wave 3: mean-variance AR (cs1014)
        "cs1014-4.2.2-cp-01",  # CAF Wave 3: mean-variance CP (cs1014)
        "cs1003-4.2.3-ar-01",  # CAF Wave 3: link-canonical AR (cs1003)
        "cs1003-4.2.3-cp-01",  # CAF Wave 3: link-canonical CP (cs1003)
        "cs1014-4.2.3-ar-01",  # CAF Wave 3: link-canonical AR (cs1014)
        "cs1014-4.2.3-cp-01",  # CAF Wave 3: link-canonical CP (cs1014)
        "cs1003-4.2.4-ar-01",  # CAF Wave 4: factors/interactions AR (cs1003)
        "cs1003-4.2.4-cp-01",  # CAF Wave 4: factors/interactions CP (cs1003)
        "cs1014-4.2.4-cp-01",  # CAF Wave 4: factors/interactions CP (cs1014)
        "cs1014-4.2.4-ar-01",  # CAF Wave 4: factors/interactions AR (cs1014)
        "cs1003-4.2.5-ar-01",  # CAF Wave 4: linear predictor AR (cs1003)
        "cs1014-4.2.5-ar-01",  # CAF Wave 4: linear predictor AR (cs1014)
        "cs1003-4.2.6-ar-01",  # CAF Wave 4: deviance AR (cs1003)
        "cs1014-4.2.6-ar-01",  # CAF Wave 4: deviance AR (cs1014)
        "cs1003-4.2.6-cp-01",  # CAF Wave 4: deviance CP (cs1003)
        "cs1014-4.2.6-cp-01",  # CAF Wave 4: deviance CP (cs1014)
        "cs1003-4.2.7-ar-01",  # CAF Wave 4: model choice AR (cs1003)
        "cs1014-4.2.7-ar-01",  # CAF Wave 4: model choice AR (cs1014)
        "cs1003-4.2.7-cp-01",  # CAF Wave 4: model choice CP (cs1003)
        "cs1014-4.2.7-cp-01",  # CAF Wave 4: model choice CP (cs1014)
        "cs1003-4.2.8-ar-01",  # CAF Wave 4: residuals AR (cs1003)
        "cs1014-4.2.8-ar-01",  # CAF Wave 4: residuals AR (cs1014)
        "cs1003-4.2.9-ar-01",  # CAF Wave 4: goodness tests AR (cs1003)
        "cs1014-4.2.9-ar-01",  # CAF Wave 4: goodness tests AR (cs1014)
        "cs1003-4.2.9-cp-01",  # CAF Wave 4: goodness tests CP (cs1003)
        "cs1014-4.2.9-cp-01",  # CAF Wave 4: goodness tests CP (cs1014)
        "cs1003-4.2.10-ar-01",  # CAF Wave 4: fit-interpret AR (cs1003)
        "cs1014-4.2.10-ar-01",  # CAF Wave 4: fit-interpret AR (cs1014)
        "cs1014-cx-r1-ar-01",  # CAF Wave 4: revision GLM AR
        "cs1014-cx-r1-cp-01",  # CAF Wave 4: revision GLM CP
        "cs1003-cd-r2-ar-01",  # CAF Wave 4: revision regression-GLM AR
        "cs1003-cd-r2-cp-01",  # CAF Wave 4: revision regression-GLM CP
        "cs1002-2.1a-ar-01",  # CAF Wave 4: discrete AR (cs1002)
        "cs1002-2.1a-cp-01",  # CAF Wave 4: discrete CP (cs1002)
        "cs1002-2.1b-ar-01",  # CAF Wave 4: continuous AR (cs1002)
        "cs1002-2.1b-cp-01",  # CAF Wave 4: continuous CP (cs1002)
        "cs1004-2.1c-ar-01",  # CAF Wave 4: prob/quantiles AR
        "cs1004-2.1d-ar-01",  # CAF Wave 4: Poisson process AR
        "cs1004-2.1d-cp-01",  # CAF Wave 4: Poisson process CP
        "cs1004-2.1e-ar-01",  # CAF Wave 4: inverse transform AR
        "cs1004-2.1e-cp-01",  # CAF Wave 4: inverse transform CP
        "cs1004-2.1f-ar-01",  # CAF Wave 4: software generation AR
        "cs1004-2.1f-cp-01",  # CAF Wave 4: software generation CP
        "cs1016-2.1.3-ar-01",  # CAF Wave 4: companion prob/quantiles AR
        "cs1017-2.1.1-ar-01",  # CAF Wave 4: discrete AR (cs1017)
        "cs1017-2.1.1-cp-01",  # CAF Wave 4: discrete CP (cs1017)
        "cs1004-cgr1-ar-01",  # CAF Wave 4: revision generation AR
        "cs1005-2.2.1-ar-01",  # CAF Wave 5: 2.2.1-marginal-conditional-cs1005
        "cs1005-2.2.2-ar-01",  # CAF Wave 5: 2.2.2-independence-cs1005
        "cs1005-2.2.2-cp-01",  # CAF Wave 5: 2.2.2-independence-cs1005
        "cs1005-2.2.3-ar-01",  # CAF Wave 5: 2.2.3-cov-corr-expectation-cs1005
        "cs1005-2.2.4-ar-01",  # CAF Wave 5: 2.2.4-linear-combinations-cs1005
        "cs1006-2.3.1-ar-01",  # CAF Wave 5: 2.3.1-conditional-expectation-cs1006
        "cs1006-2.3.2-ar-01",  # CAF Wave 5: 2.3.2-mean-variance-conditioning-cs1006
        "cs1016-2.2.1-ar-01",  # CAF Wave 5: cp-2.2.1-marginal-conditional-cs1016
        "cs1005-ce-r1-ar-01",  # CAF Wave 5: revision-joint-distributions-cs1005
        "cs1005-ce-r1-cp-01",  # CAF Wave 5: revision-joint-distributions-cs1005
        "cs1006-cz-r1-ar-01",  # CAF Wave 5: revision-conditional-expectations-cs1006
        "cs1006-cz-r1-cp-01",  # CAF Wave 5: revision-conditional-expectations-cs1006
        "cs1011-3.2.1-ar-01",  # CAF Wave 5: 3.2.1-confidence-interval-parameter-cs1011
        "cs1011-3.2.1-cp-01",  # CAF Wave 5: 3.2.1-confidence-interval-parameter-cs1011
        "cs1011-3.2.2-ar-01",  # CAF Wave 5: 3.2.2-prediction-interval-cs1011
        "cs1011-3.2.2-cp-01",  # CAF Wave 5: 3.2.2-prediction-interval-cs1011
        "cs1011-3.2.3-ar-01",  # CAF Wave 5: 3.2.3-ci-given-sampling-distribution-cs1011
        "cs1011-3.2.3-cp-01",  # CAF Wave 5: 3.2.3-ci-given-sampling-distribution-cs1011
        "cs1011-3.2.4-ar-01",  # CAF Wave 5: 3.2.4-ci-normal-mean-variance-cs1011
        "cs1011-3.2.4-cp-01",  # CAF Wave 5: 3.2.4-ci-normal-mean-variance-cs1011
        "cs1011-3.2.5-ar-01",  # CAF Wave 5: 3.2.5-ci-binomial-poisson-cs1011
        "cs1011-3.2.5-cp-01",  # CAF Wave 5: 3.2.5-ci-binomial-poisson-cs1011
        "cs1011-3.2.6-ar-01",  # CAF Wave 5: 3.2.6-ci-two-sample-cs1011
        "cs1011-3.2.6-cp-01",  # CAF Wave 5: 3.2.6-ci-two-sample-cs1011
        "cs1011-3.2.7-ar-01",  # CAF Wave 5: 3.2.7-ci-paired-means-cs1011
        "cs1011-3.2.7-cp-01",  # CAF Wave 5: 3.2.7-ci-paired-means-cs1011
        "cs1011-3.2.8-ar-01",  # CAF Wave 5: 3.2.8-bootstrap-confidence-interval-cs1011
        "cs1011-3.2.8-cp-01",  # CAF Wave 5: 3.2.8-bootstrap-confidence-interval-cs1011
        "cs1012-3.3.1-ar-01",  # CAF Wave 5: 3.3.1-hypothesis-concepts-cs1012
        "cs1012-3.3.1-cp-01",  # CAF Wave 5: 3.3.1-hypothesis-concepts-cs1012
        "cs1012-3.3.2-ar-01",  # CAF Wave 5: 3.3.2-basic-tests-cs1012
        "cs1012-3.3.2-cp-01",  # CAF Wave 5: 3.3.2-basic-tests-cs1012
        "cs1012-3.3.3-ar-01",  # CAF Wave 5: 3.3.3-permutation-tests-cs1012
        "cs1012-3.3.3-cp-01",  # CAF Wave 5: 3.3.3-permutation-tests-cs1012
        "cs1012-3.3.4-ar-01",  # CAF Wave 5: 3.3.4-chi-square-gof-cs1012
        "cs1012-3.3.4-cp-01",  # CAF Wave 5: 3.3.4-chi-square-gof-cs1012
        "cs1012-3.3.5-ar-01",  # CAF Wave 5: 3.3.5-contingency-independence-cs1012
        "cs1012-3.3.5-cp-01",  # CAF Wave 5: 3.3.5-contingency-independence-cs1012
        "cs1016-3.2.1-ar-01",  # CAF Wave 5: cp-3.2.1-ci-sample-cs1016
        "cs1016-3.2.1-cp-01",  # CAF Wave 5: cp-3.2.1-ci-sample-cs1016
        "cs1016-3.3.1-ar-01",  # CAF Wave 5: cp-3.3.1-hypothesis-testing-cs1016
        "cs1016-3.3.1-cp-01",  # CAF Wave 5: cp-3.3.1-hypothesis-testing-cs1016
        "cs1011-cl-r1-ar-01",  # CAF Wave 6: revision-confidence-intervals-cs1011
        "cs1011-cl-r1-cp-01",  # CAF Wave 6: revision-confidence-intervals-cs1011
        "cs1012-cm-r1-ar-01",  # CAF Wave 6: revision-hypothesis-testing-cs1012
        "cs1012-cm-r1-cp-01",  # CAF Wave 6: revision-hypothesis-testing-cs1012
        "cs1009-ci-r1-ar-01",  # CAF Wave 6: revision-sampling-distributions-cs1009
        "cs1009-ci-r1-cp-01",  # CAF Wave 6: revision-sampling-distributions-cs1009
        "cs1003-4.1.1-ar-01",  # CAF Wave 6: 4.1.1-response-explanatory-cs1003
        "cs1003-4.1.1-cp-01",  # CAF Wave 6: 4.1.1-response-explanatory-cs1003
        "cs1013-4.1.1-cp-01",  # CAF Wave 6: 4.1.1-response-explanatory-cs1013
        "cs1013-4.1.1-ar-01",  # CAF Wave 6: 4.1.1-response-explanatory-cs1013
        "cs1003-4.1.2-ar-01",  # CAF Wave 6: 4.1.2-simple-multiple-cs1003
        "cs1003-4.1.2-cp-01",  # CAF Wave 6: 4.1.2-simple-multiple-cs1003
        "cs1013-4.1.2-cp-01",  # CAF Wave 6: 4.1.2-simple-multiple-cs1013
        "cs1013-4.1.2-ar-01",  # CAF Wave 6: 4.1.2-simple-multiple-cs1013
        "cs1003-4.1.3-ar-01",  # CAF Wave 6: 4.1.3-least-squares-cs1003
        "cs1003-4.1.3-cp-01",  # CAF Wave 6: 4.1.3-least-squares-cs1003
        "cs1013-4.1.3-cp-01",  # CAF Wave 6: 4.1.3-least-squares-cs1013
        "cs1013-4.1.3-ar-01",  # CAF Wave 6: 4.1.3-least-squares-cs1013
        "cs1003-4.1.4-ar-01",  # CAF Wave 6: 4.1.4-software-inference-cs1003
        "cs1003-4.1.4-cp-01",  # CAF Wave 6: 4.1.4-software-inference-cs1003
        "cs1013-4.1.4-ar-01",  # CAF Wave 6: 4.1.4-software-fit-cs1013
        "cs1013-4.1.4-cp-01",  # CAF Wave 6: 4.1.4-software-fit-cs1013
        "cs1003-4.1.5-ar-01",  # CAF Wave 6: 4.1.5-variable-selection-cs1003
        "cs1013-4.1.5-ar-01",  # CAF Wave 6: 4.1.5-variable-selection-cs1013
        "cs1003-4.1.5-cp-01",  # CAF Wave 6: 4.1.5-variable-selection-cs1003
        "cs1013-4.1.5-cp-01",  # CAF Wave 6: 4.1.5-variable-selection-cs1013
        "cs1016-4.1.1-ar-01",  # CAF Wave 6: cp-4.1.1-linear-regression-cs1016
        "cs1016-4.1.1-cp-01",  # CAF Wave 6: cp-4.1.1-linear-regression-cs1016
        "cs1003-cd-r1-ar-01",  # CAF Wave 6: revision-linear-models-cs1003
        "cs1003-cd-r1-cp-01",  # CAF Wave 6: revision-linear-models-cs1003
        "cs1013-cn-r1-ar-01",  # CAF Wave 6: revision-linear-regression-cs1013
        "cs1013-cn-r1-cp-01",  # CAF Wave 6: revision-linear-regression-cs1013
        "ep001-1.1-ar-01",  # CAF Wave 6: 1.1-purpose-function-ep001
        "ep001-1.1-cp-01",  # CAF Wave 6: 1.1-purpose-function-ep001
        "ep001-1.2a-ar-01",  # CAF Wave 6: 1.2.1-eda-summaries-ep001
        "ep001-1.2a-cp-01",  # CAF Wave 6: 1.2.1-eda-summaries-ep001
        "ep001-1.2b-ar-01",  # CAF Wave 6: 1.2.2-eda-association-ep001
        "ep001-1.2b-cp-01",  # CAF Wave 6: 1.2.2-eda-association-ep001
        "cs1002-1.2c-ar-01",  # CAF Wave 6: 1.2.3-pca-cs1002
        "cs1002-1.2c-cp-01",  # CAF Wave 6: 1.2.3-pca-cs1002
        "ep001-ca-r1-ar-01",  # CAF Wave 6: revision-purpose-eda-ep001
        "ep001-ca-r1-cp-01",  # CAF Wave 6: revision-purpose-eda-ep001
        "ep001-ca-r1-cp-02",  # CAF Wave 6: revision-purpose-eda-ep001
        "cs1017-1.1.1-ar-01",  # CAF Final Wave: cr-1.1.1-aims-analysis-cs1017
        "cs1017-1.1.1-cp-01",  # CAF Final Wave: cr-1.1.1-aims-analysis-cs1017
        "cs1017-1.1.2-ar-01",  # CAF Final Wave: cr-1.1.2-stages-tools-cs1017
        "cs1017-1.1.2-cp-01",  # CAF Final Wave: cr-1.1.2-stages-tools-cs1017
        "cs1017-1.1.3-ar-01",  # CAF Final Wave: cr-1.1.3-data-sources-cs1017
        "cs1017-1.1.3-cp-01",  # CAF Final Wave: cr-1.1.3-data-sources-cs1017
        "cs1017-1.1.4-ar-01",  # CAF Final Wave: cr-1.1.4-reproducible-cs1017
        "cs1017-1.1.4-cp-01",  # CAF Final Wave: cr-1.1.4-reproducible-cs1017
        "cs1017-1.2.1-ar-01",  # CAF Final Wave: cr-1.2.1-eda-summaries-cs1017
        "cs1017-1.2.1-cp-01",  # CAF Final Wave: cr-1.2.1-eda-summaries-cs1017
        "cs1017-1.2.2-ar-01",  # CAF Final Wave: cr-1.2.2-correlation-cs1017
        "cs1017-1.2.2-cp-01",  # CAF Final Wave: cr-1.2.2-correlation-cs1017
        "cs1017-1.2.3-ar-01",  # CAF Final Wave: cr-1.2.3-pca-cs1017
        "cs1017-1.2.3-cp-01",  # CAF Final Wave: cr-1.2.3-pca-cs1017
        "cs1017-cr-r1-ar-01",  # CAF Final Wave: cr-revision-publication-front-cs1017
        "cs1017-cr-r1-cp-01",  # CAF Final Wave: cr-revision-publication-front-cs1017
        "cs1009-2.6.1-ar-01",  # CAF Final Wave: 2.6.1-random-samples-cs1009
        "cs1009-2.6.1-cp-01",  # CAF Final Wave: 2.6.1-random-samples-cs1009
        "cs1016-2.6.1-ar-01",  # CAF Final Wave: cp-2.6.1-random-samples-cs1016
        "cs1016-2.6.1-cp-01",  # CAF Final Wave: cp-2.6.1-random-samples-cs1016
        "cs1009-2.6.2-ar-01",  # CAF Final Wave: 2.6.2-sampling-distribution-cs1009
        "cs1009-2.6.2-cp-01",  # CAF Final Wave: 2.6.2-sampling-distribution-cs1009
        "cs1009-2.6.3-ar-01",  # CAF Final Wave: 2.6.3-mean-var-sample-cs1009
        "cs1009-2.6.3-cp-01",  # CAF Final Wave: 2.6.3-mean-var-sample-cs1009
        "cs1009-2.6.4-ar-01",  # CAF Final Wave: 2.6.4-normal-sample-mean-var-cs1009
        "cs1009-2.6.4-cp-01",  # CAF Final Wave: 2.6.4-normal-sample-mean-var-cs1009
        "cs1009-2.6.5-ar-01",  # CAF Final Wave: 2.6.5-t-statistic-cs1009
        "cs1009-2.6.5-cp-01",  # CAF Final Wave: 2.6.5-t-statistic-cs1009
        "cs1009-2.6.6-ar-01",  # CAF Final Wave: 2.6.6-f-distribution-cs1009
        "cs1009-2.6.6-cp-01",  # CAF Final Wave: 2.6.6-f-distribution-cs1009
        "cs1007-2.4.1-ar-01",  # CAF Final Wave: 2.4.1-mgf-cgf-cs1007
        "cs1007-2.4.1-cp-01",  # CAF Final Wave: 2.4.1-mgf-cgf-cs1007
        "cs1007-2.4.2-ar-01",  # CAF Final Wave: 2.4.2-moment-via-gf-cs1007
        "cs1007-2.4.2-cp-01",  # CAF Final Wave: 2.4.2-moment-via-gf-cs1007
        "cs1008-2.5.1-ar-01",  # CAF Final Wave: 2.5.1-clt-cs1008
        "cs1016-2.5.1-ar-01",  # CAF Final Wave: cp-2.5.1-clt-cs1016
        "cs1008-2.5.2-ar-01",  # CAF Final Wave: 2.5.2-simulated-sample-normal-cs1008
        "cs1008-2.5.2-cp-01",  # CAF Final Wave: 2.5.2-simulated-sample-normal-cs1008
        "cs1008-ct-r1-ar-01",  # CAF Final Wave: revision-central-limit-theorem-cs1008
        "cs1008-ct-r1-cp-01",  # CAF Final Wave: revision-central-limit-theorem-cs1008
        "cs1007-ch-r1-ar-01",  # CAF Final Wave: revision-generating-functions-cs1007
        "cs1007-ch-r1-cp-01",  # CAF Final Wave: revision-generating-functions-cs1007
        "cs1016-cp-r1-ar-01",  # CAF Final Wave: cp-revision-spine-memory-cs1016
        "cs1016-cp-r1-cp-01",  # CAF Final Wave: cp-revision-spine-memory-cs1016
        "cs1002-cb-r1-ar-01",  # CAF Final Wave: revision-pca-distributions-cs1002
        "cs1002-cb-r1-cp-01",  # CAF Final Wave: revision-pca-distributions-cs1002
        "cs1002-cb-r1-cp-02",  # CAF Final Wave: revision-pca-distributions-cs1002
        "cs1002-cb-r1-cp-03",  # CAF Final Wave: revision-pca-distributions-cs1002
    }
)

# Authored choice-aware mistake text: (item_id, wrong_choice_id) → copy.
# Keys are distractors only; correct choices are never looked up.
PROTOTYPE_CHOICE_FEEDBACK: dict[tuple[str, str], str] = {
    # --- cs1010-3.1.3-cp-01 ---
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
    # --- cs1014-4.2.1-ar-01 ---
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
    # --- cs1017-2.1.2-cp-01 ---
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
    # --- cs1010-ck-r1-cp-01 ---
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
    # --- cs1003-5.1.1-ar-01 ---
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
    # --- cs1003-5.1.1-cp-01 ---
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
    # --- cs1015-5.1.1-ar-01 ---
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
    # --- cs1015-5.1.1-cp-01 ---
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
    # --- cs1015-co-r1-ar-01 ---
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
    # --- cs1015-co-r1-cp-01 ---
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
    # --- cs1010-3.1.3-ar-01 ---
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
    # --- cs1010-3.1.4-ar-01 ---
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
    # --- cs1010-3.1.4-cp-01 ---
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
    # --- cs1014-4.2.1-cp-01 ---
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
    # --- cs1010-ck-r1-ar-01 ---
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
    # --- cs1017-2.1.2-ar-01 ---
    (
        "cs1017-2.1.2-ar-01",
        "b",
    ): (
        "That choice makes Normal the default for any positive quantity. "
        "Symmetric all-real support does not match strictly positive "
        "waiting-time support; family choice follows support and shape "
        "story."
    ),
    (
        "cs1017-2.1.2-ar-01",
        "c",
    ): (
        "That choice treats Exponential and Normal as interchangeable "
        "because each has one numeric parameter. Parameter count does not "
        "equate families; memoryless waiting under constant hazard points "
        "to exponential, not Normal."
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
    # --- cs1003-5.1.2-ar-01 ---
    (
        "cs1003-5.1.2-ar-01",
        "b",
    ): (
        "That choice treats naming a conjugate pair as finishing the "
        "numerical posterior. Conjugate closure keeps the posterior in the "
        "same family; you still obtain posterior parameters from prior "
        "plus data."
    ),
    (
        "cs1003-5.1.2-ar-01",
        "c",
    ): (
        "That choice collapses prior and posterior into one object and "
        "equates conjugate with the MLE. Prior is belief before data; "
        "posterior is after; conjugate means family closure under "
        "updating, not MLE equality."
    ),
    (
        "cs1003-5.1.2-ar-01",
        "d",
    ): (
        "That choice calls any zero-to-one prior conjugate and treats "
        "closure as optional. Conjugate means the prior family stays "
        "closed under updating so the posterior remains in that family."
    ),
    # --- cs1003-5.1.2-cp-01 ---
    (
        "cs1003-5.1.2-cp-01",
        "b",
    ): (
        "That choice treats the prior as the last observed sample. The "
        "prior is belief about theta before data; conjugate updating "
        "combines that prior with the likelihood, not a copied sample."
    ),
    (
        "cs1003-5.1.2-cp-01",
        "c",
    ): (
        "That choice treats naming Beta-Binomial as finishing the "
        "numerical posterior. Conjugate naming structures the update; you "
        "still calculate posterior parameters from prior plus data."
    ),
    (
        "cs1003-5.1.2-cp-01",
        "d",
    ): (
        "That choice makes prior and posterior identical once data arrive "
        "and equates conjugate with the MLE. Posterior updates the prior; "
        "conjugate means family closure, not MLE equality."
    ),
    # --- cs1015-5.1.2-ar-01 (content twin of cs1003-5.1.2-ar-01) ---
    (
        "cs1015-5.1.2-ar-01",
        "b",
    ): (
        "That choice treats naming a conjugate pair as finishing the "
        "numerical posterior. Conjugate closure keeps the posterior in the "
        "same family; you still obtain posterior parameters from prior "
        "plus data."
    ),
    (
        "cs1015-5.1.2-ar-01",
        "c",
    ): (
        "That choice collapses prior and posterior into one object and "
        "equates conjugate with the MLE. Prior is belief before data; "
        "posterior is after; conjugate means family closure under "
        "updating, not MLE equality."
    ),
    (
        "cs1015-5.1.2-ar-01",
        "d",
    ): (
        "That choice calls any zero-to-one prior conjugate and treats "
        "closure as optional. Conjugate means the prior family stays "
        "closed under updating so the posterior remains in that family."
    ),
    # --- cs1015-5.1.2-cp-01 ---
    (
        "cs1015-5.1.2-cp-01",
        "b",
    ): (
        "That choice treats naming Beta-Binomial as finishing the "
        "numerical posterior. Conjugate naming structures the update; you "
        "still calculate posterior parameters from prior plus data."
    ),
    (
        "cs1015-5.1.2-cp-01",
        "c",
    ): (
        "That choice sets the prior equal to the sample mean and leaves "
        "the posterior unchanged under conjugate updating. Conjugate "
        "updating revises parameters with the data; prior and posterior "
        "are distinct stages."
    ),
    (
        "cs1015-5.1.2-cp-01",
        "d",
    ): (
        "That choice keeps prior and likelihood as objects that never "
        "combine. Bayes forms the posterior from prior times likelihood, "
        "then normalises; conjugate pairs still combine."
    ),
    # --- cs1003-5.1.3-ar-01 ---
    (
        "cs1003-5.1.3-ar-01",
        "b",
    ): (
        "That choice treats having the posterior as finishing the "
        "squared-error point estimator. The posterior is the updated "
        "distribution; a loss-based point estimate is a further summary "
        "under a chosen loss."
    ),
    (
        "cs1003-5.1.3-ar-01",
        "c",
    ): (
        "That choice sets the simple posterior equal to the prior alone. "
        "Posterior comes from prior and likelihood together; likelihood "
        "is not reserved for frequentist intervals."
    ),
    (
        "cs1003-5.1.3-ar-01",
        "d",
    ): (
        "That choice replaces the posterior distribution with a credible "
        "interval as the only output. Intervals are summaries of the "
        "posterior; the primary object is the full posterior "
        "distribution."
    ),
    # --- cs1003-5.1.3-cp-01 ---
    (
        "cs1003-5.1.3-cp-01",
        "b",
    ): (
        "That choice treats Bayesian as a slogan and skips the posterior "
        "once Beta(2,2) is named. With Binomial n=10 and x=3, the "
        "conjugate update is Beta(5,9); Bayesian work needs that "
        "posterior distribution."
    ),
    (
        "cs1003-5.1.3-cp-01",
        "c",
    ): (
        "That choice leaves the posterior at Beta(2,2) as if n=10 were "
        "too small to update. Successes and failures revise the shapes: "
        "Beta(2+3, 2+7) = Beta(5,9)."
    ),
    (
        "cs1003-5.1.3-cp-01",
        "d",
    ): (
        "That choice treats having Beta(5,9) as finishing the "
        "squared-error point estimator. Beta(5,9) is the posterior "
        "distribution; a loss-based point estimate is a further step."
    ),
    # --- cs1015-5.1.3-ar-01 (content twin of cs1003-5.1.3-ar-01) ---
    (
        "cs1015-5.1.3-ar-01",
        "b",
    ): (
        "That choice treats having the posterior as finishing the "
        "squared-error point estimator. The posterior is the updated "
        "distribution; a loss-based point estimate is a further summary "
        "under a chosen loss."
    ),
    (
        "cs1015-5.1.3-ar-01",
        "c",
    ): (
        "That choice sets the simple posterior equal to the prior alone. "
        "Posterior comes from prior and likelihood together; likelihood "
        "is not reserved for frequentist intervals."
    ),
    (
        "cs1015-5.1.3-ar-01",
        "d",
    ): (
        "That choice replaces the posterior distribution with a credible "
        "interval as the only output. Intervals are summaries of the "
        "posterior; the primary object is the full posterior "
        "distribution."
    ),
    # --- cs1015-5.1.3-cp-01 ---
    (
        "cs1015-5.1.3-cp-01",
        "b",
    ): (
        "That choice leaves the posterior at Beta(2,2) as if n=10 were "
        "too small to update. Successes and failures revise the shapes: "
        "Beta(2+3, 2+7) = Beta(5,9)."
    ),
    (
        "cs1015-5.1.3-cp-01",
        "c",
    ): (
        "That choice treats the sample proportion three-tenths as the "
        "posterior distribution. The conjugate posterior is Beta(5,9); "
        "that ratio is a point summary, not the full posterior."
    ),
    (
        "cs1015-5.1.3-cp-01",
        "d",
    ): (
        "That choice treats having Beta(5,9) as finishing the "
        "squared-error point estimator. Beta(5,9) is the posterior "
        "distribution; a loss-based point estimate is a further step."
    ),
    # --- cs1003-5.1.7-ar-01 ---
    (
        "cs1003-5.1.7-ar-01",
        "b",
    ): (
        "That choice treats the blend formula as Bayesian credibility by "
        "itself. Bayesian credibility needs a prior or structural story "
        "that warrants mu and Z, then the premium."
    ),
    (
        "cs1003-5.1.7-ar-01",
        "c",
    ): (
        "That choice collapses Bayesian credibility into finishing "
        "Empirical Bayes. A shared numeric premium does not make the "
        "approaches the same; Bayes treats structurals as known from the "
        "prior, EB estimates them from data."
    ),
    (
        "cs1003-5.1.7-ar-01",
        "d",
    ): (
        "That choice forces full credibility and parks the prior in "
        "Empirical Bayes alone. In simple Bayesian credibility the prior "
        "structure supplies mu and k; Z = n/(n+k) with individual "
        "experience, and need not be 1."
    ),
    # --- cs1015-5.1.7-ar-01 ---
    (
        "cs1015-5.1.7-ar-01",
        "b",
    ): (
        "That choice treats a shared numeric premium as finishing "
        "Empirical Bayes. Bayesian credibility and Empirical Bayes differ "
        "in how structural parameters are obtained, even when both "
        "produce a premium."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "c",
    ): (
        "That choice reserves mu and Z for Empirical Bayes alone. In "
        "simple Bayesian credibility the prior or structural distribution "
        "supplies mu and k; Z = n/(n+k) also uses the amount of "
        "individual experience."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "d",
    ): (
        "That choice drops the credibility premium form. In simple cases "
        "the premium object is Z times X-bar plus one minus Z times mu, "
        "with mu and k from the prior structure and Z = n/(n+k) from "
        "that structure together with individual experience."
    ),
    # --- cs1003-5.1.8-ar-01 ---
    (
        "cs1003-5.1.8-ar-01",
        "b",
    ): (
        "That choice equates Empirical Bayes with a fully specified "
        "Bayesian prior. EB estimates structurals from collective data; "
        "full Bayes treats them as given by the prior."
    ),
    (
        "cs1003-5.1.8-ar-01",
        "c",
    ): (
        "That choice reduces Empirical Bayes to a single-claim Bayes "
        "update. EB uses collective experience to estimate structurals "
        "before forming the credibility premium."
    ),
    (
        "cs1003-5.1.8-ar-01",
        "d",
    ): (
        "That choice forces Z equal to one whenever data appear. EB still "
        "forms Z-hat as n over n plus k-hat, and the blend Z-hat times "
        "X-bar plus one minus Z-hat times mu-hat; full credibility is not "
        "automatic."
    ),
    # --- cs1015-5.1.8-ar-01 (content twin of cs1003-5.1.8-ar-01) ---
    (
        "cs1015-5.1.8-ar-01",
        "b",
    ): (
        "That choice equates Empirical Bayes with a fully specified "
        "Bayesian prior. EB estimates structurals from collective data; "
        "full Bayes treats them as given by the prior."
    ),
    (
        "cs1015-5.1.8-ar-01",
        "c",
    ): (
        "That choice reduces Empirical Bayes to a single-claim Bayes "
        "update. EB uses collective experience to estimate structurals "
        "before forming the credibility premium."
    ),
    (
        "cs1015-5.1.8-ar-01",
        "d",
    ): (
        "That choice forces Z equal to one whenever data appear. EB still "
        "forms Z-hat as n over n plus k-hat, and the blend Z-hat times "
        "X-bar plus one minus Z-hat times mu-hat; full credibility is not "
        "automatic."
    ),
    # --- CAF Wave 3 (2026-09-10 editorial review) ---
    # --- cs1003-5.1.4-ar-01 ---
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
    # --- cs1015-5.1.4-ar-01 ---
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
    # --- cs1003-5.1.5-ar-01 ---
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
    # --- cs1003-5.1.5-cp-01 ---
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
    # --- cs1015-5.1.5-ar-01 ---
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
    # --- cs1015-5.1.5-cp-01 ---
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
    # --- cs1003-5.1.6-ar-01 ---
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
    # --- cs1015-5.1.6-ar-01 ---
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
    # --- cs1003-5.1.9-ar-01 ---
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
    # --- cs1003-5.1.9-cp-01 ---
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
    # --- cs1015-5.1.9-ar-01 ---
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
    # --- cs1015-5.1.9-cp-01 ---
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
    # --- cs1016-5.1.1-ar-01 ---
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
    # --- cs1003-cd-r3-ar-01 ---
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
    # --- cs1003-cd-r3-cp-01 ---
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
    # --- cs1010-3.1.1-ar-01 ---
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
    # --- cs1010-3.1.2-ar-01 ---
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
    # --- cs1010-3.1.5-ar-01 ---
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
    # --- cs1010-3.1.5-cp-01 ---
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
    # --- cs1010-3.1.6-ar-01 ---
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
    # --- cs1016-3.1.1-ar-01 ---
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
    # --- cs1003-4.2.1-ar-01 ---
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
    # --- cs1003-4.2.1-cp-01 ---
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
    # --- cs1003-4.2.2-ar-01 ---
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
    # --- cs1003-4.2.2-cp-01 ---
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
    # --- cs1014-4.2.2-ar-01 ---
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
    # --- cs1014-4.2.2-cp-01 ---
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
    # --- cs1003-4.2.3-ar-01 ---
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
    # --- cs1003-4.2.3-cp-01 ---
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
    # --- cs1014-4.2.3-ar-01 ---
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
    # --- cs1014-4.2.3-cp-01 ---
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
    # --- CAF Wave 4 (2026-09-10 editorial review) ---
    # --- cs1003-4.2.4-ar-01 ---
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
    # --- cs1003-4.2.4-cp-01 ---
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
    # --- cs1014-4.2.4-cp-01 ---
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
    # --- cs1014-4.2.4-ar-01 ---
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
    # --- cs1003-4.2.5-ar-01 ---
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
    # --- cs1014-4.2.5-ar-01 ---
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
    # --- cs1003-4.2.6-ar-01 ---
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
    # --- cs1014-4.2.6-ar-01 ---
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
    # --- cs1003-4.2.6-cp-01 ---
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
    # --- cs1014-4.2.6-cp-01 ---
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
    # --- cs1003-4.2.7-ar-01 ---
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
    # --- cs1014-4.2.7-ar-01 ---
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
    # --- cs1003-4.2.7-cp-01 ---
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
    # --- cs1014-4.2.7-cp-01 ---
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
    # --- cs1003-4.2.8-ar-01 ---
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
    # --- cs1014-4.2.8-ar-01 ---
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
    # --- cs1003-4.2.9-ar-01 ---
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
    # --- cs1014-4.2.9-ar-01 ---
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
    # --- cs1003-4.2.9-cp-01 ---
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
    # --- cs1014-4.2.9-cp-01 ---
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
    # --- cs1003-4.2.10-ar-01 ---
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
    # --- cs1014-4.2.10-ar-01 ---
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
    # --- cs1014-cx-r1-ar-01 ---
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
    # --- cs1014-cx-r1-cp-01 ---
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
    # --- cs1003-cd-r2-ar-01 ---
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
    # --- cs1003-cd-r2-cp-01 ---
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
    # --- cs1002-2.1a-ar-01 ---
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
    # --- cs1002-2.1a-cp-01 ---
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
    # --- cs1002-2.1b-ar-01 ---
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
    # --- cs1002-2.1b-cp-01 ---
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
    # --- cs1004-2.1c-ar-01 ---
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
    # --- cs1004-2.1d-ar-01 ---
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
    # --- cs1004-2.1d-cp-01 ---
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
    # --- cs1004-2.1e-ar-01 ---
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
    # --- cs1004-2.1e-cp-01 ---
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
    # --- cs1004-2.1f-ar-01 ---
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
    # --- cs1004-2.1f-cp-01 ---
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
    # --- cs1016-2.1.3-ar-01 ---
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
    # --- cs1017-2.1.1-ar-01 ---
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
    # --- cs1017-2.1.1-cp-01 ---
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
    # --- cs1004-cgr1-ar-01 ---
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

    # --- cs1011-cl-r1-ar-01 ---
    (
        "cs1011-cl-r1-ar-01",
        "b",
    ): (
        "That choice treats the realised interval as a 0.95 probability that fixed theta lies inside it given these data. "
        "Frequentist coverage is about the procedure under repeated samples, not a posterior probability for a fixed parameter."
    ),
    (
        "cs1011-cl-r1-ar-01",
        "c",
    ): (
        "That choice puts ninety-five percent of sample values inside the interval. "
        "A parameter CI targets the unknown parameter, not the fraction of observations that fall inside the band."
    ),
    (
        "cs1011-cl-r1-ar-01",
        "d",
    ): (
        "That choice turns the confidence level into a probability that the statistical model is true. "
        "Coverage concerns how often intervals capture the parameter under the assumed model, not a probability that the model itself is true."
    ),
    # --- cs1011-cl-r1-cp-01 ---
    (
        "cs1011-cl-r1-cp-01",
        "b",
    ): (
        "That choice makes the prediction interval narrower because only one future value is considered. "
        "Predicting one future response adds observation-level noise, so the interval is typically wider than a mean-response CI at the same x."
    ),
    (
        "cs1011-cl-r1-cp-01",
        "c",
    ): (
        "That choice treats the two intervals as always identical. "
        "A mean-response CI targets E[Y|x]; a prediction interval also carries future residual variance and is typically wider."
    ),
    (
        "cs1011-cl-r1-cp-01",
        "d",
    ): (
        "That choice puts future observation noise into the mean-response CI and removes it from the prediction interval. "
        "The extra observation variance belongs on the prediction side, not the reverse."
    ),
    # --- cs1012-cm-r1-ar-01 ---
    (
        "cs1012-cm-r1-ar-01",
        "b",
    ): (
        "That choice makes the p-value the probability that the null is true after seeing the data. "
        "A p-value is computed under the null; it is not a posterior probability that the null holds."
    ),
    (
        "cs1012-cm-r1-ar-01",
        "c",
    ): (
        "That choice makes the p-value the probability that the alternative is false. "
        "The p-value is a tail probability for the test statistic under the null, not a probability statement about the alternative."
    ),
    (
        "cs1012-cm-r1-ar-01",
        "d",
    ): (
        "That choice treats the p-value as the chance the same sample result occurs again. "
        "It measures incompatibility of data at least as extreme as observed under the null, not a replication probability."
    ),
    # --- cs1012-cm-r1-cp-01 ---
    (
        "cs1012-cm-r1-cp-01",
        "b",
    ): (
        "That choice treats a tiny p-value as proof of the alternative with probability one. "
        "Significance signals tension with the null under the assumptions; it does not prove the alternative."
    ),
    (
        "cs1012-cm-r1-cp-01",
        "c",
    ): (
        "That choice sets the Type I error probability of the completed test equal to the p-value. "
        "The Type I rate is a pre-chosen long-run property of the procedure, not the observed p-value."
    ),
    (
        "cs1012-cm-r1-cp-01",
        "d",
    ): (
        "That choice equates a small p-value with a large, practically important effect. "
        "Statistical significance is not the same as practical importance or effect size."
    ),
    # --- cs1009-ci-r1-ar-01 ---
    (
        "cs1009-ci-r1-ar-01",
        "b",
    ): (
        "That choice equates the sampling distribution with the single realised sample mean. "
        "The sampling distribution is the law of that statistic across repeated samples of the same size."
    ),
    (
        "cs1009-ci-r1-ar-01",
        "c",
    ): (
        "That choice treats the empirical distribution of observations in one sample as the sampling distribution of the mean. "
        "Those are different objects: one describes data in a sample, the other describes the statistic over repeated samples."
    ),
    (
        "cs1009-ci-r1-ar-01",
        "d",
    ): (
        "That choice forces the sampling distribution of the mean to be standard Normal for every population and every n. "
        "Normality of the mean needs model or large-sample warrant; it is not automatic."
    ),
    # --- cs1009-ci-r1-cp-01 ---
    (
        "cs1009-ci-r1-cp-01",
        "b",
    ): (
        "That choice divides by S without the root-n factor and claims a standard Normal law. "
        "With unknown variance the studentised mean uses S/√n and follows t with n−1 degrees of freedom."
    ),
    (
        "cs1009-ci-r1-cp-01",
        "c",
    ): (
        "That choice gives that studentised mean a chi-squared law. "
        "The mean pivot is t_{n−1}; chi-square is the usual law for scaled sample variance, not for the mean pivot."
    ),
    (
        "cs1009-ci-r1-cp-01",
        "d",
    ): (
        "That choice says the raw sample mean itself is t with n degrees of freedom. "
        "The t law applies to the studentised mean with n−1 df, not to the unstandardised mean with n df."
    ),
    # --- cs1003-4.1.1-ar-01 ---
    (
        "cs1003-4.1.1-ar-01",
        "b",
    ): (
        "That choice makes age the response and puts claim frequency on the right-hand side because every column looks like a predictor. "
        "Y is the outcome you set out to model; here that is claim frequency, with age and territory as explanatory rating factors."
    ),
    (
        "cs1003-4.1.1-ar-01",
        "c",
    ): (
        "That choice treats age and territory as responses and frequency as an explanatory variable just because frequency is numeric. "
        "Numeric type does not assign roles; the modelling question does."
    ),
    (
        "cs1003-4.1.1-ar-01",
        "d",
    ): (
        "That choice refuses to name Y and X until a multiple regression equation is written. "
        "Response and explanatory roles can be stated from the modelling question before choosing simple versus multiple form."
    ),
    # --- cs1003-4.1.1-cp-01 ---
    (
        "cs1003-4.1.1-cp-01",
        "b",
    ): (
        "That choice makes claim count the response and dumps every other numeric column on the right-hand side. "
        "For a severity question Y is claim amount; warranted X variables need a severity story, not column-soup."
    ),
    (
        "cs1003-4.1.1-cp-01",
        "c",
    ): (
        "That choice forces claim count into the severity X set just because it shares the policy record. "
        "Claim count is a frequency outcome; it is not automatically an explanatory variable for severity."
    ),
    (
        "cs1003-4.1.1-cp-01",
        "d",
    ): (
        "That choice blocks naming the response until a full multiple regression equation is written. "
        "Severity modelling still starts by naming Y versus warranted X, not by writing the equation first."
    ),
    # --- cs1013-4.1.1-cp-01 ---
    (
        "cs1013-4.1.1-cp-01",
        "b",
    ): (
        "That choice makes claim count the response and dumps every other numeric column on the right-hand side. "
        "For a severity question Y is claim amount; warranted X variables need a severity story, not column-soup."
    ),
    (
        "cs1013-4.1.1-cp-01",
        "c",
    ): (
        "That choice forces claim count into the severity X set just because it shares the policy record. "
        "Claim count is a frequency outcome; it is not automatically an explanatory variable for severity."
    ),
    (
        "cs1013-4.1.1-cp-01",
        "d",
    ): (
        "That choice blocks naming the response until a full multiple regression equation is written. "
        "Severity modelling still starts by naming Y versus warranted X, not by writing the equation first."
    ),
    # --- cs1013-4.1.1-ar-01 ---
    (
        "cs1013-4.1.1-ar-01",
        "b",
    ): (
        "That choice makes every numeric column an automatic X and picks Y by largest variance. "
        "Roles come from the modelling question, not from variance ranking or column-soup."
    ),
    (
        "cs1013-4.1.1-ar-01",
        "c",
    ): (
        "That choice always puts claim count on the right-hand side when modelling severity because both fields are numeric. "
        "Sharing a policy record does not make count an explanatory variable for severity."
    ),
    (
        "cs1013-4.1.1-ar-01",
        "d",
    ): (
        "That choice says roles exist only after writing simple versus multiple equations. "
        "You can name Y and X from the question before choosing model form."
    ),
    # --- cs1003-4.1.2-ar-01 ---
    (
        "cs1003-4.1.2-ar-01",
        "b",
    ): (
        "That choice swaps the equations: two predictors for simple and one for multiple. "
        "Simple has one explanatory variable; multiple has more than one entering jointly."
    ),
    (
        "cs1003-4.1.2-ar-01",
        "c",
    ): (
        "That choice replaces model-form statement with estimated beta-hat from least squares. "
        "Writing the simple versus multiple equations in beta is model form; OLS is estimation of those betas."
    ),
    (
        "cs1003-4.1.2-ar-01",
        "d",
    ): (
        "That choice says simple and multiple differ only in a software menu and that one-predictor notation covers both. "
        "The forms differ in how many explanatory variables enter the equation."
    ),
    # --- cs1003-4.1.2-cp-01 ---
    (
        "cs1003-4.1.2-cp-01",
        "b",
    ): (
        "That choice writes the two-predictor equation as simple and the one-predictor equation as multiple. "
        "Count of explanatory variables defines the forms, not the size of the least-squares criterion."
    ),
    (
        "cs1003-4.1.2-cp-01",
        "c",
    ): (
        "That choice treats clicking Fit / writing beta-hat formulae as stating simple versus multiple form. "
        "Estimation is not the same as stating which predictors enter the linear model."
    ),
    (
        "cs1003-4.1.2-cp-01",
        "d",
    ): (
        "That choice collapses simple and multiple because age and sum insured are both continuous. "
        "Continuity of predictors does not erase the one-versus-several explanatory-variable distinction."
    ),
    # --- cs1013-4.1.2-cp-01 ---
    (
        "cs1013-4.1.2-cp-01",
        "b",
    ): (
        "That choice writes the two-predictor equation as simple and the one-predictor equation as multiple. "
        "Count of explanatory variables defines the forms, not the size of the least-squares criterion."
    ),
    (
        "cs1013-4.1.2-cp-01",
        "c",
    ): (
        "That choice treats clicking Fit / writing beta-hat formulae as stating simple versus multiple form. "
        "Estimation is not the same as stating which predictors enter the linear model."
    ),
    (
        "cs1013-4.1.2-cp-01",
        "d",
    ): (
        "That choice collapses simple and multiple because age and sum insured are both continuous. "
        "Continuity of predictors does not erase the one-versus-several explanatory-variable distinction."
    ),
    # --- cs1013-4.1.2-ar-01 ---
    (
        "cs1013-4.1.2-ar-01",
        "b",
    ): (
        "That choice says simple and multiple differ only in how least-squares estimates are computed. "
        "The forms differ in how many explanatory variables enter; OLS is how you estimate whichever form you stated."
    ),
    (
        "cs1013-4.1.2-ar-01",
        "c",
    ): (
        "That choice forces interactions into every multiple model and removes the intercept from every simple model. "
        "Multiple means several explanatory variables; interactions and intercepts are separate modelling choices."
    ),
    (
        "cs1013-4.1.2-ar-01",
        "d",
    ): (
        "That choice reserves simple regression for frequency and multiple for severity. "
        "Either outcome can use either form; the distinction is the number of explanatory variables, not frequency versus severity."
    ),
    # --- cs1003-4.1.3-ar-01 ---
    (
        "cs1003-4.1.3-ar-01",
        "b",
    ): (
        "That choice minimises absolute residuals and equates the slope with Corr(X, Y). "
        "Ordinary least squares minimises squared residuals; correlation is not the OLS slope by definition."
    ),
    (
        "cs1003-4.1.3-ar-01",
        "c",
    ): (
        "That choice treats clicking Fit as the least-squares criterion. "
        "Fit may implement OLS, but the criterion is still minimise the sum of squared residuals."
    ),
    (
        "cs1003-4.1.3-ar-01",
        "d",
    ): (
        "That choice sets the slope to SD(Y)/SD(X) and says least squares minimises R-squared. "
        "The OLS slope is Cov/Var (with intercept through the means); least squares minimises residual sum of squares, not R-squared."
    ),
    # --- cs1003-4.1.3-cp-01 ---
    (
        "cs1003-4.1.3-cp-01",
        "b",
    ): (
        "That choice makes clicking Fit the criterion and treats the closed-form slope as optional. "
        "Software Fit implements OLS; the criterion remains minimise sum of squared residuals, with slope Cov/Var."
    ),
    (
        "cs1003-4.1.3-cp-01",
        "c",
    ): (
        "That choice equates the OLS slope with Corr(X, Y) because both measure association. "
        "Correlation and the OLS slope are related but not the same scale or formula."
    ),
    (
        "cs1003-4.1.3-cp-01",
        "d",
    ): (
        "That choice minimises absolute residuals while still quoting the OLS Cov/Var slope. "
        "Least squares uses squared residuals; absolute-residual minimisation is a different criterion."
    ),
    # --- cs1013-4.1.3-cp-01 ---
    (
        "cs1013-4.1.3-cp-01",
        "b",
    ): (
        "That choice makes clicking Fit the criterion and treats the closed-form slope as optional. "
        "Software Fit implements OLS; the criterion remains minimise sum of squared residuals, with slope Cov/Var."
    ),
    (
        "cs1013-4.1.3-cp-01",
        "c",
    ): (
        "That choice equates the OLS slope with Corr(X, Y) because both measure association. "
        "Correlation and the OLS slope are related but not the same scale or formula."
    ),
    (
        "cs1013-4.1.3-cp-01",
        "d",
    ): (
        "That choice minimises absolute residuals while still quoting the OLS Cov/Var slope. "
        "Least squares uses squared residuals; absolute-residual minimisation is a different criterion."
    ),
    # --- cs1013-4.1.3-ar-01 ---
    (
        "cs1013-4.1.3-ar-01",
        "b",
    ): (
        "That choice treats Fit as an opaque internal criterion with no closed form. "
        "Least squares still means minimise the sum of squared residuals, whether or not software prints the algebra."
    ),
    (
        "cs1013-4.1.3-ar-01",
        "c",
    ): (
        "That choice sets the OLS slope equal to Corr(X, Y) by definition. "
        "Correlation is not the slope estimate; OLS uses the Cov/Var (or equivalent) slope with an intercept."
    ),
    (
        "cs1013-4.1.3-ar-01",
        "d",
    ): (
        "That choice minimises absolute residuals and freezes the slope at the sample correlation. "
        "Ordinary least squares estimates both slope and intercept by minimising squared residuals."
    ),
    # --- cs1003-4.1.4-ar-01 ---
    (
        "cs1003-4.1.4-ar-01",
        "b",
    ): (
        "That choice runs variable selection after fit and declares validity from R-squared without residual checks. "
        "Post-fit work still needs slope inference, prediction limits, and residual checks, not selection alone."
    ),
    (
        "cs1003-4.1.4-ar-01",
        "c",
    ): (
        "That choice reads only the slope sign and sends prediction limits and residual checks to GLM-only land. "
        "Those moves are part of linear-model software fit and interpretation as well."
    ),
    (
        "cs1003-4.1.4-ar-01",
        "d",
    ): (
        "That choice inspects residuals before fitting and skips slope inference as automatic. "
        "Fit first, then infer, predict with limits, and check residuals against that fit."
    ),
    # --- cs1003-4.1.4-cp-01 ---
    (
        "cs1003-4.1.4-cp-01",
        "b",
    ): (
        "That choice stops once the model is fitted and treats residuals as optional after a significant slope. "
        "Fit alone is not enough; slope inference, GOF, prediction limits, and residual checks still matter."
    ),
    (
        "cs1003-4.1.4-cp-01",
        "c",
    ): (
        "That choice calls residual plots optional theatre because the slope is significant. "
        "Significance does not validate constant variance, linearity, or other modelling assumptions that residuals probe."
    ),
    (
        "cs1003-4.1.4-cp-01",
        "d",
    ): (
        "That choice makes mean-response and prediction intervals the same width because both supposedly estimate only E[Y|x*]. "
        "The prediction interval adds residual variance and is typically wider."
    ),
    # --- cs1013-4.1.4-ar-01 ---
    (
        "cs1013-4.1.4-ar-01",
        "b",
    ): (
        "That choice drops residual plots once the slope is significant. "
        "Significance is not a substitute for checking whether the linear model is suitable."
    ),
    (
        "cs1013-4.1.4-ar-01",
        "c",
    ): (
        "That choice equates mean-response and individual-response intervals because both supposedly target E[Y|x*]. "
        "An individual prediction interval covers a new observation and typically adds residual variance."
    ),
    (
        "cs1013-4.1.4-ar-01",
        "d",
    ): (
        "That choice reduces goodness-of-fit to adjusted R-squared alone and excludes slope inference and prediction limits from software-fit work. "
        "Post-fit interpretation still includes those pieces alongside GOF."
    ),
    # --- cs1013-4.1.4-cp-01 ---
    (
        "cs1013-4.1.4-cp-01",
        "b",
    ): (
        "That choice treats best-subset selection as finishing software fit and inference for this model. "
        "Selection is separate; after a fit you still need slope inference, GOF, prediction limits, and residual checks."
    ),
    (
        "cs1013-4.1.4-cp-01",
        "c",
    ): (
        "That choice makes residual plots optional because the slope is significant. "
        "Significance does not clear residual diagnostics."
    ),
    (
        "cs1013-4.1.4-cp-01",
        "d",
    ): (
        "That choice gives mean-response and prediction intervals the same width as estimators of E[Y|x*] only. "
        "Prediction intervals cover a new observation and are typically wider."
    ),
    # --- cs1003-4.1.5-ar-01 ---
    (
        "cs1003-4.1.5-ar-01",
        "b",
    ): (
        "That choice finishes selection by keeping every term with p less than 0.05. "
        "Mechanical p-chopping is not a complete warrant; use fit measures that balance fit against complexity."
    ),
    (
        "cs1003-4.1.5-ar-01",
        "c",
    ): (
        "That choice equates linear explanatory-variable selection with choosing a GLM link, both finished by raw R-squared. "
        "Those are different tasks; raw R-squared alone is not a selection rule for either."
    ),
    (
        "cs1003-4.1.5-ar-01",
        "d",
    ): (
        "That choice always keeps every numeric column to avoid wasting information. "
        "Extra variables can overfit and dilute interpretation; more is not automatically better."
    ),
    # --- cs1013-4.1.5-ar-01 ---
    (
        "cs1013-4.1.5-ar-01",
        "b",
    ): (
        "That choice finishes selection by keeping every term with p less than 0.05. "
        "Mechanical p-chopping is not a complete warrant; use fit measures that balance fit against complexity."
    ),
    (
        "cs1013-4.1.5-ar-01",
        "c",
    ): (
        "That choice equates linear explanatory-variable selection with choosing a GLM link, both finished by raw R-squared. "
        "Those are different tasks; raw R-squared alone is not a selection rule for either."
    ),
    (
        "cs1013-4.1.5-ar-01",
        "d",
    ): (
        "That choice always keeps every numeric column to avoid wasting information. "
        "Extra variables can overfit and dilute interpretation; more is not automatically better."
    ),
    # --- cs1003-4.1.5-cp-01 ---
    (
        "cs1003-4.1.5-cp-01",
        "b",
    ): (
        "That choice ends selection once every M2 term has p less than 0.05. "
        "You still need a fit-measure comparison that penalises unnecessary complexity, not p-chopping alone."
    ),
    (
        "cs1003-4.1.5-cp-01",
        "c",
    ): (
        "That choice treats predictor selection as finishing GLM modelling. "
        "GLM also needs link and exponential-family response choices; linear selection is not that whole task."
    ),
    (
        "cs1003-4.1.5-cp-01",
        "d",
    ): (
        "That choice lets raw R-squared alone decide because it never decreases when variables are added. "
        "Raw R-squared never decreases when you add variables, which is why it is a poor complexity penalty; prefer adjusted R², AIC, or BIC."
    ),
    # --- cs1013-4.1.5-cp-01 ---
    (
        "cs1013-4.1.5-cp-01",
        "b",
    ): (
        "That choice ends selection once every M2 term has p less than 0.05. "
        "You still need a fit-measure comparison that penalises unnecessary complexity, not p-chopping alone."
    ),
    (
        "cs1013-4.1.5-cp-01",
        "c",
    ): (
        "That choice treats predictor selection as finishing GLM modelling. "
        "GLM also needs link and exponential-family response choices; linear selection is not that whole task."
    ),
    (
        "cs1013-4.1.5-cp-01",
        "d",
    ): (
        "That choice lets raw R-squared alone decide because it never decreases when variables are added. "
        "Raw R-squared never decreases when you add variables, which is why it is a poor complexity penalty; prefer adjusted R², AIC, or BIC."
    ),
    # --- cs1016-4.1.1-ar-01 ---
    (
        "cs1016-4.1.1-ar-01",
        "b",
    ): (
        "That choice makes every numeric column an automatic X and picks Y by largest variance. "
        "Roles follow the modelling question and a warrant for each predictor, not variance ranking."
    ),
    (
        "cs1016-4.1.1-ar-01",
        "c",
    ): (
        "That choice delays roles until the full multiple regression equation is written. "
        "You can name Y and X before locking equation form."
    ),
    (
        "cs1016-4.1.1-ar-01",
        "d",
    ): (
        "That choice defines the response as whichever column is entered last in the formula. "
        "Estimation order in software does not assign the modelling response."
    ),
    # --- cs1016-4.1.1-cp-01 ---
    (
        "cs1016-4.1.1-cp-01",
        "b",
    ): (
        "That choice makes sum insured the response and dumps premium onto the right-hand side with the other numerics. "
        "For this question Y is renewal premium; column-soup is not role modelling."
    ),
    (
        "cs1016-4.1.1-cp-01",
        "c",
    ): (
        "That choice keeps premium as Y but also forces premium to be an explanatory variable for bedrooms. "
        "That answers a different question; do not put the response on both sides."
    ),
    (
        "cs1016-4.1.1-cp-01",
        "d",
    ): (
        "That choice refuses to name Y until a regression equation is fully written. "
        "Premium modelling still starts with Y versus warranted X."
    ),
    # --- cs1003-cd-r1-ar-01 ---
    (
        "cs1003-cd-r1-ar-01",
        "b",
    ): (
        "That choice has OLS choosing Y to minimise the sum of squared fitted values. "
        "OLS chooses beta to minimise the sum of squared residuals for the stated response Y."
    ),
    (
        "cs1003-cd-r1-ar-01",
        "c",
    ): (
        "That choice requires every explanatory variable to be independent of every other. "
        "Multiple regression allows correlated predictors; independence of the X columns is not an OLS requirement."
    ),
    (
        "cs1003-cd-r1-ar-01",
        "d",
    ): (
        "That choice fits a separate response for each predictor. "
        "Multiple regression keeps one response Y and several explanatory columns in X."
    ),
    # --- cs1003-cd-r1-cp-01 ---
    (
        "cs1003-cd-r1-cp-01",
        "b",
    ): (
        "That choice treats increasing residual spread as proof that the fitted mean is exactly correct. "
        "A funnel pattern casts doubt on constant variance; it does not confirm the mean structure."
    ),
    (
        "cs1003-cd-r1-cp-01",
        "c",
    ): (
        "That choice dismisses the pattern whenever R-squared is high. "
        "High R-squared does not repair doubtful constant-variance assumptions or unreliable usual standard errors."
    ),
    (
        "cs1003-cd-r1-cp-01",
        "d",
    ): (
        "That choice always deletes the largest residuals. "
        "Investigate structure and consider a proper remedy; automatic deletion is not the default fix."
    ),
    # --- cs1013-cn-r1-ar-01 ---
    (
        "cs1013-cn-r1-ar-01",
        "b",
    ): (
        "That choice minimises the sum of fitted responses squared. "
        "OLS minimises the sum of squared residuals, observed minus fitted."
    ),
    (
        "cs1013-cn-r1-ar-01",
        "c",
    ): (
        "That choice maximises sample correlation as the OLS criterion in every regression. "
        "Ordinary least squares minimises residual sum of squares, not maximises correlation."
    ),
    (
        "cs1013-cn-r1-ar-01",
        "d",
    ): (
        "That choice requires every residual to be zero regardless of parameter count. "
        "OLS does not demand perfect interpolation; it minimises squared residuals for the chosen model."
    ),
    # --- cs1013-cn-r1-cp-01 ---
    (
        "cs1013-cn-r1-cp-01",
        "b",
    ): (
        "That choice treats high R-squared as proof that the linear mean form is adequate. "
        "Clear residual curvature still signals likely mean misspecification."
    ),
    (
        "cs1013-cn-r1-cp-01",
        "c",
    ): (
        "That choice says variable selection guarantees unbiased coefficients and valid inference. "
        "Selection does not waive residual structure or deliver those guarantees by itself."
    ),
    (
        "cs1013-cn-r1-cp-01",
        "d",
    ): (
        "That choice deletes observations on one side of the curve until residuals look flat. "
        "Investigate justified transformations or nonlinear terms instead of carving the scatter to look linear."
    ),
    # --- ep001-1.1-ar-01 ---
    (
        "ep001-1.1-ar-01",
        "b",
    ): (
        "That choice lists plotting, means, and software as the three aims. "
        "Aims are descriptive, inferential, and predictive purposes; tools are how you pursue them."
    ),
    (
        "ep001-1.1-ar-01",
        "c",
    ): (
        "That choice collapses all three aims into one vague inspect-the-data example. "
        "The three aims stay distinct: summarise a sample, make a population claim, and forecast unseen outcomes."
    ),
    (
        "ep001-1.1-ar-01",
        "d",
    ): (
        "That choice swaps the aims: descriptive as forecast, inferential as sample-only summary, predictive as population mean without prediction. "
        "Keep each aim matched to its actuarial job."
    ),
    # --- ep001-1.1-cp-01 ---
    (
        "ep001-1.1-cp-01",
        "b",
    ): (
        "That choice treats stages as unordered so exploratory work can sit anywhere. "
        "Keep a sensible order and place EDA in clean/explore."
    ),
    (
        "ep001-1.1-cp-01",
        "c",
    ): (
        "That choice parks EDA after final communication and treats earlier stages as optional. "
        "EDA sits in clean/explore, before analysis and communication."
    ),
    (
        "ep001-1.1-cp-01",
        "d",
    ): (
        "That choice makes software fitting the only required stage and skips communication. "
        "Fitting is one stage; the path still runs through to communicating results."
    ),
    # --- ep001-1.2a-ar-01 ---
    (
        "ep001-1.2a-ar-01",
        "b",
    ): (
        "That choice leads with the mean because software defaults to it. "
        "For right-skewed claim sizes a descriptive brief usually leads with the median and IQR or percentiles."
    ),
    (
        "ep001-1.2a-ar-01",
        "c",
    ): (
        "That choice leads with the sample maximum as the typical claim size. "
        "The maximum emphasises one extreme; it is not a robust summary of typical size under right skew."
    ),
    (
        "ep001-1.2a-ar-01",
        "d",
    ): (
        "That choice says any single summary is fine because skew does not distort a mean. "
        "Right skew pulls the mean into the tail and can mislead a typical-size description."
    ),
    # --- ep001-1.2a-cp-01 ---
    (
        "ep001-1.2a-cp-01",
        "b",
    ): (
        "That choice uses a pie chart to show a continuous tail and refuses histograms. "
        "Histograms or boxplots reveal skew and extremes; pies hide continuous shape."
    ),
    (
        "ep001-1.2a-cp-01",
        "c",
    ): (
        "That choice names a boxplot without saying what pattern to look for and accepts a mean-only dashboard. "
        "Pair the plot with the skew/extremes pattern it should reveal."
    ),
    (
        "ep001-1.2a-cp-01",
        "d",
    ): (
        "That choice treats any decorative chart as acceptable exploratory work. "
        "Visualisation choice can mislead; refuse displays that hide the tail."
    ),
    # --- ep001-1.2b-ar-01 ---
    (
        "ep001-1.2b-ar-01",
        "b",
    ): (
        "That choice collapses Pearson, Spearman, and Kendall into the same linear raw-value association. "
        "They answer different association questions: linear raw, rank monotone, and pairwise concordance."
    ),
    (
        "ep001-1.2b-ar-01",
        "c",
    ): (
        "That choice makes Pearson the rank-based robust measure and Spearman/Kendall the linear raw measures. "
        "That reverses the usual roles."
    ),
    (
        "ep001-1.2b-ar-01",
        "d",
    ): (
        "That choice assigns causation, prediction accuracy, and sample size as the three measures’ targets. "
        "None of those is what Pearson, Spearman, or Kendall measure."
    ),
    # --- ep001-1.2b-cp-01 ---
    (
        "ep001-1.2b-cp-01",
        "b",
    ): (
        "That choice defaults to Pearson for every numeric pair and treats large r as proof that changing X causes Y. "
        "Prefer a rank measure for monotone nonlinear outliers, and never read association as causation."
    ),
    (
        "ep001-1.2b-cp-01",
        "c",
    ): (
        "That choice treats the measures as interchangeable and upgrades a large coefficient into control of Y by changing X. "
        "Measure choice still matters, and association is not a control warrant."
    ),
    (
        "ep001-1.2b-cp-01",
        "d",
    ): (
        "That choice prefers Spearman only for perfect linear scatters without outliers and refuses ranks under skew. "
        "Rank measures are especially useful for monotone nonlinear association with outliers."
    ),
    # --- cs1002-1.2c-ar-01 ---
    (
        "cs1002-1.2c-ar-01",
        "b",
    ): (
        "That choice has PCA invent causal risk factors and treats every PC as equally meaningful. "
        "PCA summarises shared variation; early components usually dominate, and causation needs external warrant."
    ),
    (
        "cs1002-1.2c-ar-01",
        "c",
    ): (
        "That choice reduces PCA to eigenvector computation with later components dominating shared structure. "
        "State the dimensionality-reduction purpose; early components typically capture major shared variation."
    ),
    (
        "cs1002-1.2c-ar-01",
        "d",
    ): (
        "That choice lets PCA replace subject-matter judgment and auto-name business drivers. "
        "Components still need external warrant before they become named drivers."
    ),
    # --- cs1002-1.2c-cp-01 ---
    (
        "cs1002-1.2c-cp-01",
        "b",
    ): (
        "That choice accepts PC1 as a true business risk factor by construction. "
        "PC1 may summarise shared variation; it does not by itself prove a causal driver."
    ),
    (
        "cs1002-1.2c-cp-01",
        "c",
    ): (
        "That choice rejects PCA entirely once causation is mentioned. "
        "Exploratory use as a summary of correlated structure can still be valid without a causal claim."
    ),
    (
        "cs1002-1.2c-cp-01",
        "d",
    ): (
        "That choice treats largest variance share as proof of causation needing no external warrant. "
        "Explained variance is not a causal certificate."
    ),
    # --- ep001-ca-r1-ar-01 ---
    (
        "ep001-ca-r1-ar-01",
        "b",
    ): (
        "That choice lists plotting, means, and software as the three aims. "
        "Aims are descriptive, inferential, and predictive purposes; tools are how you pursue them."
    ),
    (
        "ep001-ca-r1-ar-01",
        "c",
    ): (
        "That choice collapses all three aims into one vague inspect-the-data example. "
        "The three aims stay distinct: summarise a sample, make a population claim, and forecast unseen outcomes."
    ),
    (
        "ep001-ca-r1-ar-01",
        "d",
    ): (
        "That choice swaps the aims: descriptive as forecast, inferential as sample-only summary, predictive as population mean without prediction. "
        "Keep each aim matched to its actuarial job."
    ),
    # --- ep001-ca-r1-cp-01 ---
    (
        "ep001-ca-r1-cp-01",
        "b",
    ): (
        "That choice reports only the mean as the standard summary. "
        "For strongly right-skewed claims prefer median and IQR with a histogram or boxplot."
    ),
    (
        "ep001-ca-r1-cp-01",
        "c",
    ): (
        "That choice uses a pie chart to display continuous claim-amount shape. "
        "A histogram or boxplot shows skew and extremes; a pie does not."
    ),
    (
        "ep001-ca-r1-cp-01",
        "d",
    ): (
        "That choice deletes every claim above the upper quartile before summarising. "
        "Investigate large claims; do not delete them automatically."
    ),
    # --- ep001-ca-r1-cp-02 ---
    (
        "ep001-ca-r1-cp-02",
        "b",
    ): (
        "That choice forces Pearson correlation to equal 1 because the relationship is monotone. "
        "Monotone is not the same as perfectly linear; Pearson can be well below 1."
    ),
    (
        "ep001-ca-r1-cp-02",
        "c",
    ): (
        "That choice treats Kendall’s tau as proof that changing one variable causes the other. "
        "Rank association is not causation."
    ),
    (
        "ep001-ca-r1-cp-02",
        "d",
    ): (
        "That choice says no correlation measure can describe a nonlinear monotone relationship. "
        "Spearman and Kendall are built for monotone association without requiring linearity."
    ),
    # --- cs1017-1.1.1-ar-01 ---
    (
        "cs1017-1.1.1-ar-01",
        "b",
    ): (
        "That choice collapses descriptive, inferential, and predictive into one EDA label. "
        "Aims differ by target: summarise observed data, generalise to a population quantity, or forecast future outcomes."
    ),
    (
        "cs1017-1.1.1-ar-01",
        "c",
    ): (
        "That choice swaps inferential with forecasting and descriptive with hypothesis testing. "
        "Inferential targets parameters under uncertainty; predictive targets future values; descriptive summarises what was observed."
    ),
    (
        "cs1017-1.1.1-ar-01",
        "d",
    ): (
        "That choice reverses the aims: predictive as last-year summary and inferential as histogram-only work. "
        "Keep each aim matched to its target."
    ),
    # --- cs1017-1.1.1-cp-01 ---
    (
        "cs1017-1.1.1-cp-01",
        "b",
    ): (
        "That choice calls histogram, CI, and forecast all descriptive because each uses historical claims. "
        "Shared history does not erase aim: A summarises, B targets a parameter, C forecasts."
    ),
    (
        "cs1017-1.1.1-cp-01",
        "c",
    ): (
        "That choice labels A predictive, B descriptive, and C inferential. "
        "Histogram work is descriptive; a mean CI is inferential; next-year severity is predictive."
    ),
    (
        "cs1017-1.1.1-cp-01",
        "d",
    ): (
        "That choice merges B and C as inferential because both use models or intervals. "
        "A forecast targets a future value; a CI targets a parameter."
    ),
    # --- cs1017-1.1.2-ar-01 ---
    (
        "cs1017-1.1.2-ar-01",
        "b",
    ): (
        "That choice treats opening a notebook and loading packages as finishing analysis stages. "
        "Tools serve named stages; they do not replace aim → data → explore → analyse → communicate."
    ),
    (
        "cs1017-1.1.2-ar-01",
        "c",
    ): (
        "That choice communicates first, then obtains data, then defines the aim. "
        "Stage order starts with the aim and ends with communication, not the reverse."
    ),
    (
        "cs1017-1.1.2-ar-01",
        "d",
    ): (
        "That choice collapses clean/explore with final inference because any plot appears. "
        "Exploratory plots sit in explore; inference is a later analyse stage."
    ),
    # --- cs1017-1.1.2-cp-01 ---
    (
        "cs1017-1.1.2-cp-01",
        "b",
    ): (
        "That choice ends the reserves path in clean/explore once plots appear. "
        "Plots support exploration; they do not complete inference or communication."
    ),
    (
        "cs1017-1.1.2-cp-01",
        "c",
    ): (
        "That choice treats successful package load as analysis complete. "
        "Loading tools is not a staged path and does not replace ordered stages."
    ),
    (
        "cs1017-1.1.2-cp-01",
        "d",
    ): (
        "That choice communicates before defining the aim. "
        "Stakeholder output still needs a defined aim before data, exploration, and analysis."
    ),
    # --- cs1017-1.1.3-ar-01 ---
    (
        "cs1017-1.1.3-ar-01",
        "b",
    ): (
        "That choice treats a larger file as automatically better and representative. "
        "Volume does not remove selection, coverage, or measurement concerns."
    ),
    (
        "cs1017-1.1.3-ar-01",
        "c",
    ): (
        "That choice postpones source trust until modelling is finished. "
        "Source origin and quality shape bias and coverage during exploration, not only after a model."
    ),
    (
        "cs1017-1.1.3-ar-01",
        "d",
    ): (
        "That choice says extreme volume always removes sampling and compute constraints. "
        "Large sets often add storage, compute, or sampling needs rather than erase them."
    ),
    # --- cs1017-1.1.3-cp-01 ---
    (
        "cs1017-1.1.3-cp-01",
        "b",
    ): (
        "That choice crowns the administrative extract for having more rows and skips source comparison. "
        "Bias and coverage still differ by mechanism; row count is not a quality certificate."
    ),
    (
        "cs1017-1.1.3-cp-01",
        "c",
    ): (
        "That choice treats both sources as equally trustworthy in EDA because trust waits for the final model. "
        "Compare selection, response bias, completeness, and measurement error up front."
    ),
    (
        "cs1017-1.1.3-cp-01",
        "d",
    ): (
        "That choice claims a large survey file removes bias because every respondent row is present. "
        "Including every row in a voluntary file does not fix selection or response bias."
    ),
    # --- cs1017-1.1.4-ar-01 ---
    (
        "cs1017-1.1.4-ar-01",
        "b",
    ): (
        "That choice reduces reproducibility to re-running one local notebook cell. "
        "Reconstruction needs shared data identity, scripted paths, and documented environment, not a private one-off rerun."
    ),
    (
        "cs1017-1.1.4-ar-01",
        "c",
    ): (
        "That choice treats the author’s memory of steps as enough. "
        "Memory is not a reconstructible artefact for others or a future you."
    ),
    (
        "cs1017-1.1.4-ar-01",
        "d",
    ): (
        "That choice confines reproducibility to published papers. "
        "Internal pricing and reserves work need the same reconstructible artefacts."
    ),
    # --- cs1017-1.1.4-cp-01 ---
    (
        "cs1017-1.1.4-cp-01",
        "b",
    ): (
        "That choice treats a second local cell run as proof of reproducibility. "
        "Duplicate output on one laptop is not reconstruction from shared inputs and steps."
    ),
    (
        "cs1017-1.1.4-cp-01",
        "c",
    ): (
        "That choice replaces documentation with email comments. "
        "Email notes are not versioned data, scripted code, and environment records others can rerun."
    ),
    (
        "cs1017-1.1.4-cp-01",
        "d",
    ): (
        "That choice treats a dated notebook filename as versioning and makes data identity optional. "
        "A filename date does not identify the extract or the executable path."
    ),
    # --- cs1017-1.2.1-ar-01 ---
    (
        "cs1017-1.2.1-ar-01",
        "b",
    ): (
        "That choice always leads with the sample mean and a pie chart for any numeric column. "
        "Tool choice must match variable type and the exploratory question, not a fixed mean-and-pie habit."
    ),
    (
        "cs1017-1.2.1-ar-01",
        "c",
    ): (
        "That choice drops exploratory plots once correlations are computed. "
        "Coefficients do not replace shape and association visuals."
    ),
    (
        "cs1017-1.2.1-ar-01",
        "d",
    ): (
        "That choice defaults every frequency exploration to a pie chart. "
        "Pies are a narrow part-to-whole display, not the default for count shape and tails."
    ),
    # --- cs1017-1.2.1-cp-01 ---
    (
        "cs1017-1.2.1-cp-01",
        "b",
    ): (
        "That choice summarises zero-inflated claim counts with the mean alone. "
        "A single mean hides mass at zero and the right tail that the frequency aim needs."
    ),
    (
        "cs1017-1.2.1-cp-01",
        "c",
    ): (
        "That choice uses a pie of policy segments to show zero-inflation. "
        "Pies do not reveal zero mass and tail shape in the count distribution."
    ),
    (
        "cs1017-1.2.1-cp-01",
        "d",
    ): (
        "That choice skips shape plots and jumps to correlation with premium. "
        "Association coefficients do not replace frequency-shape diagnostics."
    ),
    # --- cs1017-1.2.2-ar-01 ---
    (
        "cs1017-1.2.2-ar-01",
        "b",
    ): (
        "That choice treats Pearson, Spearman, and Kendall as the same formula under three names. "
        "They measure different association structures (linear versus rank/monotone)."
    ),
    (
        "cs1017-1.2.2-ar-01",
        "c",
    ): (
        "That choice reads a significant Pearson correlation as proof that changing X causes Y. "
        "Association is not causation."
    ),
    (
        "cs1017-1.2.2-ar-01",
        "d",
    ): (
        "That choice assigns Kendall only to PCA inputs and Pearson only after PCA scores. "
        "Correlation choice is about association type, not a PCA pipeline rule."
    ),
    # --- cs1017-1.2.2-cp-01 ---
    (
        "cs1017-1.2.2-cp-01",
        "b",
    ): (
        "That choice forces Pearson whenever a scatter is drawn. "
        "With monotone nonlinear shape and outliers, rank measures are the better association tools here."
    ),
    (
        "cs1017-1.2.2-cp-01",
        "c",
    ): (
        "That choice treats a strong negative Spearman as proof that reducing years licensed reduces frequency. "
        "Rank association still does not prove causation."
    ),
    (
        "cs1017-1.2.2-cp-01",
        "d",
    ): (
        "That choice picks Kendall because it supposedly measures variance explained by PC1. "
        "Kendall is a bivariate rank association measure, not a PCA variance summary."
    ),
    # --- cs1017-1.2.3-ar-01 ---
    (
        "cs1017-1.2.3-ar-01",
        "b",
    ): (
        "That choice has PCA select the single causal factor behind rating variables. "
        "PCA summarises shared variation; it does not prove a causal driver."
    ),
    (
        "cs1017-1.2.3-ar-01",
        "c",
    ): (
        "That choice lets PCA replace correlation analysis because components look like causal scores. "
        "Components still need external warrant; they do not retire association checks."
    ),
    (
        "cs1017-1.2.3-ar-01",
        "d",
    ): (
        "That choice equates PC1 with the sample mean vector of the originals. "
        "A principal component is a weighted combination ordered by explained variation, not the mean vector."
    ),
    # --- cs1017-1.2.3-cp-01 ---
    (
        "cs1017-1.2.3-cp-01",
        "b",
    ): (
        "That choice accepts PC1 as the true latent risk score and auto-decline warrant. "
        "PC1 may summarise shared variation; causal underwriting policy needs external subject-matter warrant."
    ),
    (
        "cs1017-1.2.3-cp-01",
        "c",
    ): (
        "That choice lets largest-variance PC1 replace correlation analysis and hypothesis testing. "
        "Variance rank is not a substitute for those checks."
    ),
    (
        "cs1017-1.2.3-cp-01",
        "d",
    ): (
        "That choice equates PC1 with the average of standardised factors and with portfolio mean premium. "
        "Averaging standardised inputs is not the same as a validated premium or risk driver."
    ),
    # --- cs1017-cr-r1-ar-01 ---
    (
        "cs1017-cr-r1-ar-01",
        "b",
    ): (
        "That choice makes claim count continuous because a year is continuous, then forces Normal. "
        "The recorded variable is a non-negative integer count, not a continuous calendar length."
    ),
    (
        "cs1017-cr-r1-ar-01",
        "c",
    ): (
        "That choice calls the count categorical because zeros appear. "
        "Zero is a legitimate count value, not a reason to reclassify as categories."
    ),
    (
        "cs1017-cr-r1-ar-01",
        "d",
    ): (
        "That choice forces Exponential because claims occur over time. "
        "Waiting times can be Exponential; the recorded annual claim count is still a discrete count."
    ),
    # --- cs1017-cr-r1-cp-01 ---
    (
        "cs1017-cr-r1-cp-01",
        "b",
    ): (
        "That choice reads the curved scatter as proof that more advertising causes more sales. "
        "The plot supports association, not causal attribution."
    ),
    (
        "cs1017-cr-r1-cp-01",
        "c",
    ): (
        "That choice forces Pearson correlation to zero because the pattern is curved. "
        "Curvature can still show association; Pearson may be a poor summary, not automatically zero."
    ),
    (
        "cs1017-cr-r1-cp-01",
        "d",
    ): (
        "That choice says a scatter cannot evidence association between continuous variables. "
        "A scatter is exactly a descriptive association display."
    ),
    # --- cs1009-2.6.1-ar-01 ---
    (
        "cs1009-2.6.1-ar-01",
        "b",
    ): (
        "That choice calls any n observations a random sample once mean and variance can be computed. "
        "Calculable summaries do not create a sampling model or population warrant."
    ),
    (
        "cs1009-2.6.1-ar-01",
        "c",
    ): (
        "That choice treats equality of sample mean and population mean as proof of randomness. "
        "A lucky mean match does not certify the selection mechanism."
    ),
    (
        "cs1009-2.6.1-ar-01",
        "d",
    ): (
        "That choice says sampling design becomes irrelevant after an estimator formula is chosen. "
        "Estimators presuppose a sampling story; they do not repair a broken one."
    ),
    # --- cs1009-2.6.1-cp-01 ---
    (
        "cs1009-2.6.1-cp-01",
        "b",
    ): (
        "That choice treats n=40 as enough for a random sample of the whole book. "
        "Large n does not fix one-client consecutive selection and dependence."
    ),
    (
        "cs1009-2.6.1-cp-01",
        "c",
    ): (
        "That choice validates randomness when the extract mean is close to the book mean. "
        "Mean proximity is not a sampling-mechanism certificate."
    ),
    (
        "cs1009-2.6.1-cp-01",
        "d",
    ): (
        "That choice expects a later t statistic to correct client-level selection bias. "
        "A pivot assumes a sampling warrant; it does not create one."
    ),
    # --- cs1016-2.6.1-ar-01 ---
    (
        "cs1016-2.6.1-ar-01",
        "b",
    ): (
        "That choice treats any collected n observations as a random sample because data exist. "
        "Having a pile of rows is not an iid population draw."
    ),
    (
        "cs1016-2.6.1-ar-01",
        "c",
    ): (
        "That choice verifies the sampling model when the sample mean equals the population mean. "
        "Equality of means does not prove the selection mechanism."
    ),
    (
        "cs1016-2.6.1-ar-01",
        "d",
    ): (
        "That choice makes sampling vocabulary optional and applies estimator formulas to any spreadsheet column. "
        "Estimators require a population and sampling model first."
    ),
    # --- cs1016-2.6.1-cp-01 ---
    (
        "cs1016-2.6.1-cp-01",
        "b",
    ): (
        "That choice uses n=40 as a rule-of-thumb proof of randomness regardless of selection. "
        "Threshold n does not override one-client clustering and selection bias."
    ),
    (
        "cs1016-2.6.1-cp-01",
        "c",
    ): (
        "That choice validates the extract as random when mean claim size is near the book average. "
        "A close mean does not repair the selection mechanism."
    ),
    (
        "cs1016-2.6.1-cp-01",
        "d",
    ): (
        "That choice postpones random-sample language until an estimator is chosen. "
        "Sampling warrant comes before estimator construction, not after."
    ),
    # --- cs1009-2.6.2-ar-01 ---
    (
        "cs1009-2.6.2-ar-01",
        "b",
    ): (
        "That choice treats a statistic as a fixed population parameter and its sampling distribution as that same constant. "
        "A statistic is a sample function; the parameter is a population quantity."
    ),
    (
        "cs1009-2.6.2-ar-01",
        "c",
    ): (
        "That choice equates the sampling distribution with the single realised sample mean you hold. "
        "One realised value is a draw from the repeated-sample law, not the law itself."
    ),
    (
        "cs1009-2.6.2-ar-01",
        "d",
    ): (
        "That choice collapses realised statistic and sampling distribution whenever n>30. "
        "Large n does not turn one number into a distribution."
    ),
    # --- cs1009-2.6.2-cp-01 ---
    (
        "cs1009-2.6.2-cp-01",
        "b",
    ): (
        "That choice accepts that the sampling distribution equals the current sample mean. "
        "Refuse: a realised statistic is one draw, not the repeated-sample distribution."
    ),
    (
        "cs1009-2.6.2-cp-01",
        "c",
    ): (
        "That choice accepts the collapse for large n only. "
        "Sample size does not turn a realised mean into its sampling distribution."
    ),
    (
        "cs1009-2.6.2-cp-01",
        "d",
    ): (
        "That choice equates parameters with sampling distributions once a mean is computed. "
        "Parameters, realised statistics, and sampling distributions remain distinct objects."
    ),
    # --- cs1009-2.6.3-ar-01 ---
    (
        "cs1009-2.6.3-ar-01",
        "b",
    ): (
        "That choice sets \\(E[\\bar X]=\\mu/n\\) because averaging seems to divide the mean. "
        "Averaging preserves the mean; it does not divide \\(\\mu\\) by n."
    ),
    (
        "cs1009-2.6.3-ar-01",
        "c",
    ): (
        "That choice keeps \\(\\mathrm{Var}(\\bar X)=\\sigma^2\\) after averaging. "
        "Independent averaging reduces variance to \\(\\sigma^2/n\\)."
    ),
    (
        "cs1009-2.6.3-ar-01",
        "d",
    ): (
        "That choice sets \\(E[S^2]=\\sigma^2/n\\) as if \\(S^2\\) estimated \\(\\mathrm{Var}(\\bar X)\\). "
        "Usual \\(S^2\\) targets population variance \\(\\sigma^2\\), not the variance of the mean."
    ),
    # --- cs1009-2.6.3-cp-01 ---
    (
        "cs1009-2.6.3-cp-01",
        "b",
    ): (
        "That choice reads \\(\\mathrm{Var}(\\bar X)=\\sigma^2/n\\) as proof that \\(\\bar X\\) is exactly Normal for every parent and every n. "
        "Moments do not by themselves give exact Normal laws."
    ),
    (
        "cs1009-2.6.3-cp-01",
        "c",
    ): (
        "That choice jumps from \\(E[S^2]=\\sigma^2\\) to a t law with no population assumptions. "
        "Unbiasedness of \\(S^2\\) does not create the Normal-sample t pivot."
    ),
    (
        "cs1009-2.6.3-cp-01",
        "d",
    ): (
        "That choice reads \\(E[\\bar X]=\\mu\\) as \\(\\bar X=\\mu\\) in every sample. "
        "Unbiasedness is about expectation across samples, not zero sampling variability."
    ),
    # --- cs1009-2.6.4-ar-01 ---
    (
        "cs1009-2.6.4-ar-01",
        "b",
    ): (
        "That choice leaves \\(\\bar X\\sim N(\\mu,\\sigma^2)\\) without the \\(1/n\\) variance scale. "
        "Averaging scales variance by \\(1/n\\)."
    ),
    (
        "cs1009-2.6.4-ar-01",
        "c",
    ): (
        "That choice uses \\(S^2/\\sigma^2\\sim\\chi^2_n\\) and drops the \\(n-1\\) scaling. "
        "The chi-square law uses \\((n-1)S^2/\\sigma^2\\) with \\(n-1\\) degrees of freedom."
    ),
    (
        "cs1009-2.6.4-ar-01",
        "d",
    ): (
        "That choice forces dependence of \\(\\bar X\\) and \\(S^2\\) because both use the same observations. "
        "Under Normal sampling they are independent despite sharing the sample."
    ),
    # --- cs1009-2.6.4-cp-01 ---
    (
        "cs1009-2.6.4-cp-01",
        "b",
    ): (
        "That choice gives \\(\\bar X\\) a \\(t_{n-1}\\) law before studentising. "
        "The mean itself is Normal; t appears after dividing by \\(S/\\sqrt{n}\\)."
    ),
    (
        "cs1009-2.6.4-cp-01",
        "c",
    ): (
        "That choice treats \\((n-1)S^2/\\sigma^2\\) as \\(N(0,1)\\). "
        "Scaled sample variance is chi-square, not standard Normal."
    ),
    (
        "cs1009-2.6.4-cp-01",
        "d",
    ): (
        "That choice treats the Normal and chi-square component laws as finishing t work before S replaces \\(\\sigma\\). "
        "The t pivot is the combination after studentising with S."
    ),
    # --- cs1009-2.6.5-ar-01 ---
    (
        "cs1009-2.6.5-ar-01",
        "b",
    ): (
        "That choice uses \\(T=(\\bar X-\\mu)/S\\) with \\(t_n\\) and drops \\(\\sqrt{n}\\). "
        "The standard error is \\(S/\\sqrt{n}\\), and the df are \\(n-1\\)."
    ),
    (
        "cs1009-2.6.5-ar-01",
        "c",
    ): (
        "That choice keeps an exact \\(N(0,1)\\) law after replacing \\(\\sigma\\) by S. "
        "Estimating \\(\\sigma\\) produces a t law, not an exact z law."
    ),
    (
        "cs1009-2.6.5-ar-01",
        "d",
    ): (
        "That choice reserves t only for comparing two sample variances. "
        "One-sample mean inference with unknown \\(\\sigma\\) is a primary t use; variance ratios use F."
    ),
    # --- cs1009-2.6.5-cp-01 ---
    (
        "cs1009-2.6.5-cp-01",
        "b",
    ): (
        "That choice keeps an exact \\(N(0,1)\\) pivot after using S in place of \\(\\sigma\\). "
        "With unknown \\(\\sigma\\), \\((\\bar X-\\mu)/(S/\\sqrt{n})\\) is \\(t_{n-1}\\), not z."
    ),
    (
        "cs1009-2.6.5-cp-01",
        "c",
    ): (
        "That choice treats S itself as the standard error in \\((\\bar X-\\mu)/S\\). "
        "The standard error still divides by \\(\\sqrt{n}\\)."
    ),
    (
        "cs1009-2.6.5-cp-01",
        "d",
    ): (
        "That choice gives \\(S_1^2/S_2^2\\) a \\(t_{n-1}\\) law. "
        "Variance ratios use F, not t; t supports mean pivots."
    ),
    # --- cs1009-2.6.6-ar-01 ---
    (
        "cs1009-2.6.6-ar-01",
        "b",
    ): (
        "That choice defines F as a two-sample mean difference over a pooled SE. "
        "That construction is a two-sample t pattern, not an F variance-ratio law."
    ),
    (
        "cs1009-2.6.6-ar-01",
        "c",
    ): (
        "That choice gives F a single degrees-of-freedom parameter because sample sizes must match. "
        "F has separate numerator and denominator df."
    ),
    (
        "cs1009-2.6.6-ar-01",
        "d",
    ): (
        "That choice claims any variance ratio is exactly F even under dependence or non-Normal parents. "
        "The exact F law needs independence and Normal-sample conditions."
    ),
    # --- cs1009-2.6.6-cp-01 ---
    (
        "cs1009-2.6.6-cp-01",
        "b",
    ): (
        "That choice assigns \\(S_1^2/S_2^2\\) a \\(t_{n_1+n_2-2}\\) law. "
        "Shared use of sample variances does not turn a variance ratio into t."
    ),
    (
        "cs1009-2.6.6-cp-01",
        "c",
    ): (
        "That choice uses \\(F_{n_1,n_2}\\) without reducing for estimated means. "
        "Each sample variance contributes \\(n_i-1\\) degrees of freedom."
    ),
    (
        "cs1009-2.6.6-cp-01",
        "d",
    ): (
        "That choice treats the variance ratio as standard Normal because its expectation is near one. "
        "Near-one expectation is not an \\(N(0,1)\\) law."
    ),
    # --- cs1007-2.4.1-ar-01 ---
    (
        "cs1007-2.4.1-ar-01",
        "b",
    ): (
        "That choice sets \\(M_X(t)=E[tX]\\) and \\(K_X(t)=e^{M_X(t)}\\). "
        "The MGF is \\(E[e^{tX}]\\); the CGF is \\(\\log M_X(t)\\), not an exponential of the MGF."
    ),
    (
        "cs1007-2.4.1-ar-01",
        "c",
    ): (
        "That choice replaces the MGF by the pair \\((E[X],\\mathrm{Var}(X))\\). "
        "A few moments are not the generating function of t."
    ),
    (
        "cs1007-2.4.1-ar-01",
        "d",
    ): (
        "That choice asserts every random variable has a finite MGF for all real t. "
        "Existence in a neighbourhood of 0 is a real condition, not automatic."
    ),
    # --- cs1007-2.4.1-cp-01 ---
    (
        "cs1007-2.4.1-cp-01",
        "b",
    ): (
        "That choice uses \\(M(t)=\\exp(\\lambda t)\\) and \\(K(t)=\\lambda t\\) from the mean alone. "
        "The Poisson MGF carries \\(e^t\\) inside the exponential, not a linear \\(\\lambda t\\) form."
    ),
    (
        "cs1007-2.4.1-cp-01",
        "c",
    ): (
        "That choice swaps MGF and CGF: puts \\(\\lambda(e^t-1)\\) as M and the exponential as K. "
        "Logarithm converts M to K, not the reverse."
    ),
    (
        "cs1007-2.4.1-cp-01",
        "d",
    ): (
        "That choice sets \\(M=\\lambda\\) and \\(K=\\log\\lambda\\) from mean=variance=\\(\\lambda\\). "
        "Moments are not the generating functions."
    ),
    # --- cs1007-2.4.2-ar-01 ---
    (
        "cs1007-2.4.2-ar-01",
        "b",
    ): (
        "That choice reads \\(M_X(0)=E[X]\\). \\(M_X(0)=1\\); the mean is the first derivative at 0."
    ),
    (
        "cs1007-2.4.2-ar-01",
        "c",
    ): (
        "That choice evaluates \\(M_X'(1)=E[X]\\). Raw moments use derivatives at \\(t=0\\), not at "
        "\\(t=1\\)."
    ),
    (
        "cs1007-2.4.2-ar-01",
        "d",
    ): (
        "That choice stops after writing \\(M_X(t)=E[e^{tX}]\\). "
        "Definition alone does not extract moments; differentiate or match Taylor coefficients."
    ),
    # --- cs1007-2.4.2-cp-01 ---
    (
        "cs1007-2.4.2-cp-01",
        "b",
    ): (
        "That choice equates \\(M(0)=1\\) with \\(E[X]=1\\) for every Poisson. "
        "\\(M(0)=1\\) is normalisation; the mean is \\(M'(0)=\\lambda\\)."
    ),
    (
        "cs1007-2.4.2-cp-01",
        "c",
    ): (
        "That choice claims \\(M'(0)=e^\\lambda\\) after dropping the chain-rule \\(\\lambda e^t\\) factor. "
        "Differentiate the composition carefully, then set \\(t=0\\)."
    ),
    (
        "cs1007-2.4.2-cp-01",
        "d",
    ): (
        "That choice treats the MGF definition as already stating the mean. You still need "
        "\\(M'(0)\\)."
    ),
    # --- cs1008-2.5.1-ar-01 ---
    (
        "cs1008-2.5.1-ar-01",
        "b",
    ): (
        "That choice applies the CLT to each individual observation as n grows. "
        "The theorem targets the standardised sample mean (or sum), not single \\(X_i\\)."
    ),
    (
        "cs1008-2.5.1-ar-01",
        "c",
    ): (
        "That choice requires an already-Normal parent. "
        "Finite mean and variance with iid sampling are the usual conditions; Normality of the parent is not required."
    ),
    (
        "cs1008-2.5.1-ar-01",
        "d",
    ): (
        "That choice keeps \\(\\mathrm{Var}(\\bar X)=\\sigma^2\\) after averaging. "
        "Averaging reduces variance to \\(\\sigma^2/n\\)."
    ),
    # --- cs1016-2.5.1-ar-01 ---
    (
        "cs1016-2.5.1-ar-01",
        "b",
    ): (
        "That choice declares every insurance quantity Normal without IID conditions or a theorem statement. "
        "Casual Normal habit is not the CLT."
    ),
    (
        "cs1016-2.5.1-ar-01",
        "c",
    ): (
        "That choice applies the CLT to a single observation \\(X_1\\) from a finite-mean population. "
        "The approximation is for the sample mean (or its standardised form) as n grows."
    ),
    (
        "cs1016-2.5.1-ar-01",
        "d",
    ): (
        "That choice allows the CLT only for already-Normal populations. "
        "Non-Normal parents with finite variance still support a Normal approximation for \\(\\bar X\\) at large n."
    ),
    # --- cs1008-2.5.2-ar-01 ---
    (
        "cs1008-2.5.2-ar-01",
        "b",
    ): (
        "That choice simulates one parent draw and compares it to a Normal density. "
        "CLT checks need the empirical distribution of repeated sample means."
    ),
    (
        "cs1008-2.5.2-ar-01",
        "c",
    ): (
        "That choice treats stating the theorem as the same as an empirical simulation comparison. "
        "A theorem statement is not a Monte Carlo check across sample sizes."
    ),
    (
        "cs1008-2.5.2-ar-01",
        "d",
    ): (
        "That choice says a skewed parent forever blocks approximately Normal means. "
        "Skewed finite-variance parents can still yield approximately Normal means as n grows."
    ),
    # --- cs1008-2.5.2-cp-01 ---
    (
        "cs1008-2.5.2-cp-01",
        "b",
    ): (
        "That choice keeps \\(\\bar X\\) exactly Exponential with mean 1 at every n. "
        "Averaging changes the sampling distribution; it does not preserve the parent family."
    ),
    (
        "cs1008-2.5.2-cp-01",
        "c",
    ): (
        "That choice keeps n=100 means as skewed as single Exponential draws. "
        "Larger n should move the mean’s distribution closer to Normal."
    ),
    (
        "cs1008-2.5.2-cp-01",
        "d",
    ): (
        "That choice makes n=5 exactly Normal by the CLT and n=100 Exponential again. "
        "Approximation typically improves as n grows, not the reverse."
    ),
    # --- cs1008-ct-r1-ar-01 ---
    (
        "cs1008-ct-r1-ar-01",
        "b",
    ): (
        "That choice makes the sample mean equal \\(\\mu\\) with probability 1 at every finite n. "
        "The CLT is a limiting distributional statement, not exact equality for finite n."
    ),
    (
        "cs1008-ct-r1-ar-01",
        "c",
    ): (
        "That choice makes each \\(X_i\\) become Normal as n grows. "
        "The limit concerns the centred and scaled mean, not individual observations."
    ),
    (
        "cs1008-ct-r1-ar-01",
        "d",
    ): (
        "That choice sends the unstandardised sum to standard Normal without centring or scaling. "
        "The CLT uses proper centring and \\(\\sqrt{n}\\) scaling."
    ),
    # --- cs1008-ct-r1-cp-01 ---
    (
        "cs1008-ct-r1-cp-01",
        "b",
    ): (
        "That choice calls every sample mean exactly Normal because a mean was calculated. "
        "Exact Normality of \\(\\bar X\\) needs stronger model conditions; CLT is approximate at finite n."
    ),
    (
        "cs1008-ct-r1-cp-01",
        "c",
    ): (
        "That choice bans the CLT for every skewed distribution. "
        "Finite-variance skewed parents can still satisfy the CLT, often needing larger n."
    ),
    (
        "cs1008-ct-r1-cp-01",
        "d",
    ): (
        "That choice says increasing n reduces skewness of the original observations. "
        "Larger n changes the sampling distribution of the mean, not the shape of each \\(X_i\\)."
    ),
    # --- cs1007-ch-r1-ar-01 ---
    (
        "cs1007-ch-r1-ar-01",
        "b",
    ): (
        "That choice sets \\(M_X(t)=E[tX]\\) and makes K its derivative. "
        "The MGF is \\(E[\\exp(tX)]\\); the CGF is \\(\\log M\\), not \\(M'\\)."
    ),
    (
        "cs1007-ch-r1-ar-01",
        "c",
    ): (
        "That choice confuses the MGF with a CDF and the CGF with a survival function. "
        "Generating functions are exponential expectations and their logs, not distribution functions."
    ),
    (
        "cs1007-ch-r1-ar-01",
        "d",
    ): (
        "That choice sets \\(K_X(t)=\\exp(M_X(t))\\). "
        "The CGF is the logarithm of the MGF, not an exponential of it."
    ),
    # --- cs1007-ch-r1-cp-01 ---
    (
        "cs1007-ch-r1-cp-01",
        "b",
    ): (
        "That choice reads \\(E[X]=M(0)\\) and \\(E[X^2]=M'(0)\\). "
        "\\(M(0)=1\\); the first two raw moments are the first two derivatives at 0."
    ),
    (
        "cs1007-ch-r1-cp-01",
        "c",
    ): (
        "That choice equates \\(\\mathrm{Var}(X)\\) with \\(M''(0)\\) in every case. "
        "\\(M''(0)\\) is \\(E[X^2]\\); variance still subtracts \\((E[X])^2\\)."
    ),
    (
        "cs1007-ch-r1-cp-01",
        "d",
    ): (
        "That choice sets \\(E[X^2]=(M'(0))^2\\). Squaring the mean gives \\((E[X])^2\\), not the "
        "second raw moment."
    ),
    # --- cs1016-cp-r1-ar-01 ---
    (
        "cs1016-cp-r1-ar-01",
        "b",
    ): (
        "That choice makes unbiased T exactly Normal for every n. "
        "Unbiasedness fixes the mean; it does not give the finite-sample law."
    ),
    (
        "cs1016-cp-r1-ar-01",
        "c",
    ): (
        "That choice scales the variance as about \\(9n\\). "
        "The asymptotic Normal limit with variance 9 for the \\(\\sqrt{n}\\) scale matches \\(\\mathrm{Var}(T)\\approx 9/n\\), not \\(9n\\)."
    ),
    (
        "cs1016-cp-r1-ar-01",
        "d",
    ): (
        "That choice sends T to \\(N(0,9)\\) without centring or scaling. "
        "The stated limit is for \\(\\sqrt{n}(T-\\theta)\\), not for raw T."
    ),
    # --- cs1016-cp-r1-cp-01 ---
    (
        "cs1016-cp-r1-cp-01",
        "b",
    ): (
        "That choice equates the MoM estimating equation with the sampling distribution. "
        "The equation defines the estimator; the sampling distribution is the law of that estimator over repeated samples."
    ),
    (
        "cs1016-cp-r1-cp-01",
        "c",
    ): (
        "That choice gives the estimator zero variance because the sample moment is observed. "
        "Observing one sample does not erase sampling variability across samples."
    ),
    (
        "cs1016-cp-r1-cp-01",
        "d",
    ): (
        "That choice claims MoM and MLE share the same finite-sample distribution by construction. "
        "Matching moments does not guarantee MLE’s finite-sample law."
    ),
    # --- cs1002-cb-r1-ar-01 ---
    (
        "cs1002-cb-r1-ar-01",
        "b",
    ): (
        "That choice has PCA identify which observed variables causally determine a response. "
        "PCA is unsupervised variance summarisation, not causal attribution."
    ),
    (
        "cs1002-cb-r1-ar-01",
        "c",
    ): (
        "That choice says PCA keeps every original variable unchanged while reducing dimension. "
        "Dimension reduction works through new linear combinations, not by leaving all originals untouched as the reduced set."
    ),
    (
        "cs1002-cb-r1-ar-01",
        "d",
    ): (
        "That choice has PCA maximise each original variable’s variance separately. "
        "Components maximise variance of linear combinations under orthogonality constraints."
    ),
    # --- cs1002-cb-r1-cp-01 ---
    (
        "cs1002-cb-r1-cp-01",
        "b",
    ): (
        "That choice picks Hypergeometric because the number of inspections is fixed. "
        "Fixed n with independent equal-p trials is Binomial; Hypergeometric needs sampling without replacement from a finite population of defectives."
    ),
    (
        "cs1002-cb-r1-cp-01",
        "c",
    ): (
        "That choice uses Poisson with parameter p and ignores n=40. "
        "A Poisson count needs a rate/mean on the count scale, not the Bernoulli p alone."
    ),
    (
        "cs1002-cb-r1-cp-01",
        "d",
    ): (
        "That choice picks Geometric because each item is defective or not. "
        "Geometric waits for the first success; here the count of defectives in 40 trials is Binomial."
    ),
    # --- cs1002-cb-r1-cp-02 ---
    (
        "cs1002-cb-r1-cp-02",
        "b",
    ): (
        "That choice defaults waiting time to Normal because it is continuous. "
        "Continuity alone does not choose Normal; Poisson-process interarrivals are Exponential."
    ),
    (
        "cs1002-cb-r1-cp-02",
        "c",
    ): (
        "That choice keeps a Poisson count law for the waiting time. "
        "Poisson counts events in an interval; the wait to the next event is Exponential."
    ),
    (
        "cs1002-cb-r1-cp-02",
        "d",
    ): (
        "That choice uses Uniform on the next unit interval because hazard is constant. "
        "Constant hazard is the Exponential memoryless property, not a Uniform waiting time."
    ),
    # --- cs1002-cb-r1-cp-03 ---
    (
        "cs1002-cb-r1-cp-03",
        "b",
    ): (
        "That choice claims Pearson measures every monotone relationship exactly. "
        "Pearson targets linear association; monotone nonlinear structure is why rank measures are used here."
    ),
    (
        "cs1002-cb-r1-cp-03",
        "c",
    ): (
        "That choice treats significant rank correlation as proof of causation. "
        "Association, even ranked, is not a causal warrant."
    ),
    (
        "cs1002-cb-r1-cp-03",
        "d",
    ): (
        "That choice forces correlation to zero whenever the relationship is nonlinear. "
        "Nonlinear monotone association can still be strong on a rank scale."
    ),

}


def find_selected_choice(
    item: ScoreablePracticeItem,
    response: str,
) -> tuple[str, str, str] | None:
    """Locate the learner's selected MCQ choice by id or label."""
    raw = (response or "").strip()
    if not raw or not item.choices:
        return None
    normalised = _normalise(raw, case_sensitive=False)
    for choice in item.choices:
        cid, label, tag = choice_parts(choice)
        if normalised in {
            _normalise(cid, case_sensitive=False),
            _normalise(label, case_sensitive=False),
        }:
            return cid, label, tag
    return None


def assemble_choice_aware_mistake(
    item: ScoreablePracticeItem,
    response: str,
    *,
    correct: bool,
) -> tuple[str, str]:
    """Return (student-facing common_mistake, misconception_tag for logging).

    Correct answers: empty mistake text and empty tag.
    Non-prototype items: existing bundled ``item.common_mistake``; tag still
    resolved from the selected choice when available (analytics plumbing).
    Prototype items: authored choice-specific copy when the selected
    distractor is mapped; otherwise fall back to the bundled common_mistake.
    """
    if correct:
        return "", ""
    selected = find_selected_choice(item, response)
    tag = selected[2] if selected else ""
    if item.item_id in PROTOTYPE_ITEM_IDS and selected is not None:
        authored = PROTOTYPE_CHOICE_FEEDBACK.get((item.item_id, selected[0]))
        if authored:
            return authored, tag
    return item.common_mistake, tag
