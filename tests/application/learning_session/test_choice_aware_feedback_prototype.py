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

_PROTOTYPE_PACKAGES: tuple[tuple[str, str], ...] = (
    *_PRIOR_TWENTY_FOUR_PACKAGES,
    *_CREDIBILITY_WAVE_PACKAGES,
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


def setup_function() -> None:
    reset_educational_package_cache()


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


def test_prototype_allowlist_is_exactly_twenty_eight_items() -> None:
    assert PROTOTYPE_ITEM_IDS == {want for _, want in _PROTOTYPE_PACKAGES}
    assert len(PROTOTYPE_ITEM_IDS) == 28
    assert len(_ORIGINAL_PILOT_PACKAGES) == 4
    assert len(_EXPANSION_PACKAGES) == 10
    assert len(_EXISTING_FOURTEEN_PACKAGES) == 14
    assert len(_CAF_WAVE1_PACKAGES) == 10
    assert len(_PRIOR_TWENTY_FOUR_PACKAGES) == 24
    assert len(_CREDIBILITY_WAVE_PACKAGES) == 4


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

