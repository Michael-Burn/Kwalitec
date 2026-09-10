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
# CAF Wave 1 prior/posterior / posterior-simple / estimators AR).
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
