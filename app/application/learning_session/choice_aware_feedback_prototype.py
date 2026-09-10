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
# CAF Wave 4 remaining P3 from 4.2.4 + entire P4 univariate 2.1).
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
        "structure supplies mu and Z; Z need not be 1."
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
        "supplies mu and Z theoretically."
    ),
    (
        "cs1015-5.1.7-ar-01",
        "d",
    ): (
        "That choice drops the credibility premium form. In simple cases "
        "the premium object is Z times X-bar plus one minus Z times mu, "
        "with Z and mu from the prior structure."
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
