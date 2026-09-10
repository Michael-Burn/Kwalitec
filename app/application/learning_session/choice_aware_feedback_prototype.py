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
# CAF Wave 3 remaining P1 / P2 / P3-through-4.2.3).
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
