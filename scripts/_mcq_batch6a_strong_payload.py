#!/usr/bin/env python3
# ruff: noqa: E501
"""Batch 6A MCQ conversion payload for 16 already-STRONG short_structured packages.

Applies deterministic four-option MCQ rewrites to Active Recall and Checkpoint
items. Content is format conversion from known-good refuse framing and named
misconceptions (not a content rewrite). Does not modify publication/status
metadata.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

Choice = dict[str, str]


def _item(
    *,
    prompt: str,
    body: str,
    choices: list[Choice],
    correct: str,
    explanation: str,
    model_answer: str,
    common_mistake: str,
    hints: list[str] | None = None,
    success_criteria: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "prompt": prompt,
        "response_type": "mcq",
        "body": body,
        "hints": hints
        or [
            "Select the single best statement.",
            "Use the concept from this learning objective only.",
        ],
        "accepted_keywords": [],
        "choices": choices,
        "correct_choice_id": correct,
        "explanation": explanation,
        "model_answer": model_answer,
        "common_mistake": common_mistake,
        "success_criteria": success_criteria
        or [
            "Selects the correct choice.",
            "Rejects the named misconception distractors.",
        ],
    }


def c(cid: str, label: str, tag: str = "") -> Choice:
    return {"id": cid, "label": label, "misconception_tag": tag}


CONVERSIONS: dict[str, dict[str, dict]] = {
    "1.1-purpose-function-ep001.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly names the three primary aims of CS1 data analysis with distinct actuarial examples?",
            body="Select the aims-and-examples statement.",
            choices=[
                c(
                    "a",
                    "Descriptive: summarise claim sizes in a portfolio year. Inferential: estimate mean claim severity for a population of similar risks. Predictive: forecast next year's claim count for pricing.",
                ),
                c(
                    "b",
                    "The three aims are plotting, computing means, and using software, illustrated by making a histogram, a sample mean, and an R call.",
                    "tools_as_aims",
                ),
                c(
                    "c",
                    "All three aims collapse into looking at data carefully, so one example such as 'inspect claims' covers descriptive, inferential, and predictive work.",
                    "aims_collapsed",
                ),
                c(
                    "d",
                    "Descriptive forecasts next year's claims, inferential summarises the sample only, and predictive estimates a population mean without prediction.",
                    "aims_swapped",
                ),
            ],
            correct="a",
            explanation="CS1 frames data analysis around descriptive, inferential, and predictive aims. Tools are not aims, and the three aims must stay distinct.",
            model_answer="Descriptive summarise sample; inferential population estimate; predictive forecast unseen outcomes, each with a distinct actuarial example.",
            common_mistake="Listing tools instead of aims, or collapsing all three into 'look at data.'",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly links analysis stages, data-source trust cues, and a reproducibility element?",
            body="Choose the pipeline, source, and reproducibility warrant.",
            choices=[
                c(
                    "a",
                    "A sensible order is define aim, obtain data, clean/explore, analyse or predict, then communicate, with EDA in clean/explore. Source trust changes with traits such as sampling bias or coarse granularity. Reproducibility needs something concrete such as versioned data and a scripted code path.",
                ),
                c(
                    "b",
                    "Stages need not be ordered because exploratory work can sit anywhere, and saying 'be careful with data' is enough for source trust and reproducibility.",
                    "vague_care_only",
                ),
                c(
                    "c",
                    "EDA belongs only after final communication, source characteristics never affect trust, and reproducibility is automatic once a plot is saved.",
                    "eda_and_repro_wrong",
                ),
                c(
                    "d",
                    "The only required stage is software fitting; source bias is irrelevant if the model converges, and naming a package version replaces scripted reproducibility.",
                    "software_stage_only",
                ),
            ],
            correct="a",
            explanation="Purpose and function includes pipeline location, what the data can support, and how another analyst could repeat the work.",
            model_answer="Ordered stages with EDA in explore/clean; name concrete source traits; name a concrete reproducibility element.",
            common_mistake="Saying 'be careful with data' without naming source traits or a concrete reproducibility element.",
        ),
    },
    "1.2.1-eda-summaries-ep001.json": {
        "ar": _item(
            prompt="Closed-book. For a descriptive aim on right-skewed claim sizes, which statement correctly chooses and justifies the lead summary?",
            body="Select the shape-aware descriptive summary.",
            choices=[
                c(
                    "a",
                    "Lead with the median (and IQR or percentiles). The mean is pulled by the long right tail and can mislead a descriptive brief about typical claim size.",
                ),
                c(
                    "b",
                    "Lead with the mean alone because that is the default statistic software computes for every numeric variable.",
                    "mean_by_habit",
                ),
                c(
                    "c",
                    "Lead with the sample maximum because descriptive work on claims should always emphasise the single largest observation.",
                    "max_as_typical",
                ),
                c(
                    "d",
                    "Any single summary is fine for a descriptive aim because skew does not affect how a mean represents typical size.",
                    "skew_ignored",
                ),
            ],
            correct="a",
            explanation="Descriptive EDA on skewed claim sizes should not hide behind a lone mean; shape-aware summaries protect the aim.",
            model_answer="Median and IQR/percentiles for right-skewed claim sizes; mean alone is distorted by the tail.",
            common_mistake="Defaulting to the mean because that is what is always computed.",
        ),
        "cp": _item(
            prompt="Closed-book. For the same right-skewed claim-size case, which statement pairs a suitable exploratory plot with a refused misuse?",
            body="Choose plot-plus-pattern and refuse a misuse.",
            choices=[
                c(
                    "a",
                    "Use a histogram or boxplot to reveal right skew and extreme claims. Refuse a pie chart or a mean-only table that hides the tail.",
                ),
                c(
                    "b",
                    "Use a pie chart of claim sizes to reveal the continuous tail shape, and refuse any histogram because histograms hide extremes.",
                    "pie_preferred",
                ),
                c(
                    "c",
                    "Name a boxplot without saying what pattern it should reveal, and accept a mean-only dashboard as fully informative for skew.",
                    "plot_without_pattern",
                ),
                c(
                    "d",
                    "Any decorative chart is acceptable for exploratory work because visualisation choice cannot mislead a descriptive aim.",
                    "decorative_ok",
                ),
            ],
            correct="a",
            explanation="Exploratory visualisations exist to reveal shape and extremes; refusing decorative or misleading displays is part of professional EDA.",
            model_answer="Histogram or boxplot for skew and extremes; refuse pie charts or mean-only summaries that hide the tail.",
            common_mistake="Naming a plot without saying what pattern it reveals.",
        ),
    },
    "1.2.2-eda-association-ep001.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly distinguishes Pearson, Spearman, and Kendall correlation and names one rank-versus-Pearson difference?",
            body="Select the three-measure discrimination.",
            choices=[
                c(
                    "a",
                    "Pearson measures linear association of raw values. Spearman measures monotonic association via ranks. Kendall measures pairwise concordance of orderings. Rank measures are more robust to some nonlinear monotone relationships and some outlier patterns than Pearson.",
                ),
                c(
                    "b",
                    "Pearson, Spearman, and Kendall all measure the same linear association of raw values, so choosing among them is only a naming preference.",
                    "all_same",
                ),
                c(
                    "c",
                    "Pearson is rank-based and robust to outliers, while Spearman and Kendall measure only linear association of raw values.",
                    "roles_reversed",
                ),
                c(
                    "d",
                    "Kendall measures causation, Spearman measures prediction accuracy, and Pearson measures only sample size.",
                    "wrong_targets",
                ),
            ],
            correct="a",
            explanation="The three measures answer related but different association questions; treating them as synonyms fails examiner discrimination.",
            model_answer="Pearson linear raw; Spearman monotonic ranks; Kendall concordance; ranks more robust for monotone nonlinear or some outlier cases.",
            common_mistake="Saying only that they all measure correlation without discrimination.",
        ),
        "cp": _item(
            prompt="Closed-book. Two skewed positive variables show outliers and a roughly increasing but nonlinear scatter. Which statement is correct?",
            body="Choose measure preference and refuse an overclaim.",
            choices=[
                c(
                    "a",
                    "Prefer Spearman or Kendall because the relationship looks monotone but nonlinear with outliers that can distort Pearson. A large coefficient still does not prove that changing X causes Y to change.",
                ),
                c(
                    "b",
                    "Prefer Pearson by habit for every numeric pair, and treat a large r as proof that changing X causes Y.",
                    "pearson_and_causation",
                ),
                c(
                    "c",
                    "Any correlation measure is interchangeable here, and a large coefficient justifies controlling Y by changing X.",
                    "control_claim",
                ),
                c(
                    "d",
                    "Prefer Spearman only when the scatter is perfectly linear with no outliers, and refuse rank measures when skew is present.",
                    "rank_when_linear",
                ),
            ],
            correct="a",
            explanation="Measure choice follows shape and robustness; interpretation discipline refuses causal theatre from exploratory association.",
            model_answer="Prefer Spearman or Kendall for monotone nonlinear association with outliers; refuse causation from the coefficient.",
            common_mistake="Choosing Pearson by habit, or claiming causation from r.",
        ),
    },
    "1.2.3-pca-cs1002.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly states the purpose of PCA and what early versus later components typically capture?",
            body="Select purpose and capture-order.",
            choices=[
                c(
                    "a",
                    "PCA reduces the dimensionality of a complex correlated data set by summarising shared variation into fewer principal components. Early components typically capture major shared structure; later components tend to hold residual or smaller-scale variation.",
                ),
                c(
                    "b",
                    "PCA invents causal risk factors from eigenvectors alone, and every principal component is equally meaningful by construction.",
                    "causal_equal_pcs",
                ),
                c(
                    "c",
                    "PCA exists only to compute eigenvectors; purpose need not be stated, and later components always dominate major shared structure.",
                    "eigen_only_order_wrong",
                ),
                c(
                    "d",
                    "PCA replaces all subject-matter judgment and proves that early components are named business drivers without external warrant.",
                    "replaces_judgment",
                ),
            ],
            correct="a",
            explanation="PCA is an exploratory reduction tool; purpose and capture order must retrieve before interpretation theatre.",
            model_answer="Dimensionality reduction of correlated structure; early PCs major shared variation; later PCs residual or smaller variation.",
            common_mistake="Describing only eigenvectors without a purpose sentence, or claiming every PC is equally meaningful.",
        ),
        "cp": _item(
            prompt="Closed-book. A colleague says PC1 is the true underlying risk factor driving claims, so it can be treated as a causal driver. Which statement is correct?",
            body="Allow exploratory usefulness; refuse causal invention.",
            choices=[
                c(
                    "a",
                    "PC1 may usefully summarise major shared variation among correlated variables for exploration or visualisation. It does not by itself prove a causal business driver or invent a named risk factor without external subject-matter warrant.",
                ),
                c(
                    "b",
                    "Accept the causal claim because the first principal component is always a true business risk factor by construction.",
                    "accept_causal",
                ),
                c(
                    "c",
                    "Reject PCA entirely as useless for exploration once someone mentions causation, even as a summary of correlated structure.",
                    "reject_all_pca",
                ),
                c(
                    "d",
                    "PC1 proves causation for claims whenever it explains the largest share of variance, so naming a risk factor needs no external warrant.",
                    "variance_proves_cause",
                ),
            ],
            correct="a",
            explanation="PCA can aid exploration; it does not mint causal business factors by construction.",
            model_answer="PC1 can summarise shared variation exploratorily; refuse automatic causation or invented named factors without external warrant.",
            common_mistake="Accepting the causal claim, or rejecting PCA entirely as useless.",
        ),
    },
    "2.1.1-discrete-cs1002.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly lists the six Syllabus 2.1.1 discrete families with a short situation cue for each?",
            body="Select the complete roster with cues.",
            choices=[
                c(
                    "a",
                    "Geometric: trials to first success. Binomial: successes in fixed trials. Negative binomial: trials to r successes. Hypergeometric: successes in a without-replacement sample. Poisson: counts with a rate story. Discrete uniform: equally likely finite outcomes.",
                ),
                c(
                    "b",
                    "Geometric, binomial, Poisson, and discrete uniform only; negative binomial collapses into geometric, and hypergeometric is optional decoration.",
                    "roster_incomplete",
                ),
                c(
                    "c",
                    "Binomial is without-replacement sampling, hypergeometric is fixed independent trials, and Poisson is any continuous waiting time.",
                    "cues_swapped",
                ),
                c(
                    "d",
                    "The six families are Normal, lognormal, exponential, gamma, beta, and continuous uniform, each with a discrete count cue.",
                    "continuous_roster",
                ),
            ],
            correct="a",
            explanation="Chapter 2 entry requires the discrete family roster to retrieve before calculation theatre.",
            model_answer="Geometric, binomial, negative binomial, hypergeometric, Poisson, discrete uniform, each with its situation cue.",
            common_mistake="Omitting hypergeometric or collapsing negative binomial into geometric.",
        ),
        "cp": _item(
            prompt="Closed-book. From a finite portfolio you sample without replacement and count how many policies are in claim. Which statement is correct?",
            body="Choose the fitting family and refuse a habitual mismatch.",
            choices=[
                c(
                    "a",
                    "Hypergeometric fits because successes are counted in a without-replacement sample from a finite population. Refuse binomial here when depletion makes trials dependent with non-constant success probability, or refuse Poisson-by-habit without a rate-process warrant.",
                ),
                c(
                    "b",
                    "Binomial fits automatically for any count of claims, including without-replacement sampling from a finite portfolio.",
                    "binomial_by_habit",
                ),
                c(
                    "c",
                    "Poisson fits by default for every claim count, so without-replacement structure can be ignored.",
                    "poisson_by_habit",
                ),
                c(
                    "d",
                    "Discrete uniform fits because each policy is equally likely, and hypergeometric never applies to insurance portfolios.",
                    "uniform_mismatch",
                ),
            ],
            correct="a",
            explanation="Situation discipline prevents treating every count as binomial or Poisson when without-replacement structure matters.",
            model_answer="Hypergeometric for without-replacement from a finite population; refuse binomial or Poisson-by-habit when that structure matters.",
            common_mistake="Default binomial or Poisson without noticing without-replacement structure.",
        ),
    },
    "2.1.2-continuous-cs1002.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly names the Syllabus 2.1.2 continuous families and gives support or role cues for Normal, lognormal, exponential, and gamma?",
            body="Select roster plus core placement cues.",
            choices=[
                c(
                    "a",
                    "Families include Normal, lognormal, exponential, gamma, chi-square, t, F, beta, and continuous uniform. Cues: Normal for symmetric continuous approximation; lognormal for positive skewed magnitudes; exponential for waiting or memoryless times; gamma for flexible positive continuous shapes.",
                ),
                c(
                    "b",
                    "Only Normal is needed in 2.1.2; other continuous families are optional names without placement cues.",
                    "normal_only",
                ),
                c(
                    "c",
                    "Normal has strictly positive support, lognormal is symmetric on all reals, exponential is for without-replacement counts, and gamma is only for probabilities on (0,1).",
                    "cues_reversed",
                ),
                c(
                    "d",
                    "The continuous roster is geometric, binomial, negative binomial, hypergeometric, Poisson, and discrete uniform.",
                    "discrete_roster",
                ),
            ],
            correct="a",
            explanation="Continuous entry requires roster and core placement cues before calculation days.",
            model_answer="Name the continuous families; cue Normal, lognormal, exponential, and gamma by support or modelling role.",
            common_mistake="Naming only Normal, or dumping formulae without placement cues.",
        ),
        "cp": _item(
            prompt="Closed-book. Individual claim sizes are strictly positive and right-skewed. Which statement is correct?",
            body="Prefer a positive skewed family; refuse Normal-by-default.",
            choices=[
                c(
                    "a",
                    "Start with lognormal or gamma because claim sizes are strictly positive and right-skewed. Refuse Normal-by-default because a symmetric all-real support model mismatches the support and skew of the quantity.",
                ),
                c(
                    "b",
                    "Use Normal by default because the central limit theorem always makes individual claim sizes Normal.",
                    "normal_by_clt",
                ),
                c(
                    "c",
                    "Use continuous uniform on all reals because positive skew is irrelevant once a continuous family is chosen.",
                    "uniform_mismatch",
                ),
                c(
                    "d",
                    "Refuse lognormal and gamma for positive skewed sizes, and prefer Normal specifically because it cannot produce negative draws in practice.",
                    "refuse_good_families",
                ),
            ],
            correct="a",
            explanation="Continuous judgement refuses Normal theatre for positive skewed claim sizes.",
            model_answer="Prefer lognormal or gamma; refuse Normal on support and skew grounds for individual claim sizes.",
            common_mistake="Default Normal because of the CLT without addressing support and skew of the individual size.",
        ),
    },
    "2.1.3-prob-quantiles-cs1004.json": {
        "ar": _item(
            prompt="Closed-book. For a named continuous family, which statement correctly distinguishes a probability question, a quantile question, and an acceptable method class?",
            body="Select evaluation-type discrimination.",
            choices=[
                c(
                    "a",
                    "Probability: find P(X <= 2) for X ~ Exp(lambda). Quantile: find x such that P(X <= x) = 0.95. Method class: calculation, tables, or software CDF/quantile functions as appropriate.",
                ),
                c(
                    "b",
                    "Naming the family is already both the probability and the quantile evaluation, so no method class is required.",
                    "name_is_evaluation",
                ),
                c(
                    "c",
                    "A quantile question asks for P(X <= a), while a probability question asks for the x with given cumulative probability.",
                    "types_reversed",
                ),
                c(
                    "d",
                    "Only software menus count as a method class; hand calculation and tables are never acceptable for continuous families.",
                    "software_only_method",
                ),
            ],
            correct="a",
            explanation="Evaluation skill starts by discriminating the question type and naming a method class.",
            model_answer="State a P-question, a quantile question, and a method class such as calculation, tables, or software.",
            common_mistake="Restating the family name without posing an evaluation question.",
        ),
        "cp": _item(
            prompt="Closed-book. A portfolio loss is modelled as approximately Normal and you need the 95th percentile loss. Which statement is correct?",
            body="Identify quantile task; refuse recognition-as-done.",
            choices=[
                c(
                    "a",
                    "This is a quantile or percentile evaluation. Compute or call the Normal quantile at 0.95 with the fitted mean and sd. Knowing the family names the model; it does not produce the percentile without evaluation.",
                ),
                c(
                    "b",
                    "This is only a probability evaluation of P(X <= 0.95), and naming Normal finishes the numerical answer.",
                    "wrong_type_done",
                ),
                c(
                    "c",
                    "Because the loss is Normal, the 95th percentile equals the mean, so no quantile step is needed.",
                    "percentile_is_mean",
                ),
                c(
                    "d",
                    "Family recognition replaces tables and software: once Normal is named, the percentile is already known.",
                    "recognition_theatre",
                ),
            ],
            correct="a",
            explanation="Quantile evaluation for Normal is not completed by family placement alone.",
            model_answer="Quantile task; Normal quantile at 0.95 with mean and sd; refuse recognition-as-done.",
            common_mistake="Stopping at 'use Normal' without stating the quantile step.",
        ),
    },
    "2.1.4-poisson-process-cs1004.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly connects a Poisson process to the Poisson distribution for counts in an interval?",
            body="Select the process-to-count warrant.",
            choices=[
                c(
                    "a",
                    "A Poisson process models random arrivals or events in continuous time at a constant average rate under standard assumptions. The number of events in a fixed interval then follows a Poisson distribution with mean equal to rate times length.",
                ),
                c(
                    "b",
                    "A Poisson process is only another name for the Poisson PMF, with no continuous-time arrival story required.",
                    "pmf_only",
                ),
                c(
                    "c",
                    "Counts in a fixed interval follow a continuous Normal distribution under a Poisson process, while the Poisson distribution is only for waiting times.",
                    "count_law_wrong",
                ),
                c(
                    "d",
                    "The Poisson distribution models arrivals in continuous time, and the Poisson process is the discrete count law in an interval.",
                    "roles_reversed",
                ),
            ],
            correct="a",
            explanation="The learning objective is the process-to-distribution connection, not a rote PMF dump.",
            model_answer="Process: continuous-time arrivals at a rate. Count in an interval: Poisson with mean rate times length.",
            common_mistake="Only restating the Poisson PMF without the process story.",
        ),
        "cp": _item(
            prompt="Closed-book. A student says Poisson just means the discrete distribution and process talk is optional decoration. Which statement is correct?",
            body="Refuse the collapse; state the connection.",
            choices=[
                c(
                    "a",
                    "Refuse: the Poisson process is the continuous-time arrival model; the Poisson distribution is the law for the count in an interval under that process. Collapsing them loses the required connection.",
                ),
                c(
                    "b",
                    "Agree: process language is optional decoration once the discrete Poisson PMF is named.",
                    "agree_optional",
                ),
                c(
                    "c",
                    "Refuse only the word process, but accept that interval counts need no distributional link to arrivals.",
                    "refuse_word_only",
                ),
                c(
                    "d",
                    "The discrete Poisson distribution already includes continuous-time arrivals, so distinguishing process from count law is unnecessary.",
                    "distribution_includes_process",
                ),
            ],
            correct="a",
            explanation="Syllabus 2.1.4 requires the process-to-count connection, not optional decoration.",
            model_answer="Process is continuous-time arrivals; distribution is the interval count law; refuse collapsing them.",
            common_mistake="Agreeing that process language is optional.",
        ),
    },
    "2.1.5-inverse-transform-cs1004.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly lists the inverse-transform steps for a continuous random variable with CDF F?",
            body="Select Uniform source plus inverse CDF.",
            choices=[
                c(
                    "a",
                    "Draw U ~ Uniform(0,1). Set X = F^{-1}(U), the quantile function. Then X has CDF F under standard conditions.",
                ),
                c(
                    "b",
                    "Draw X directly from F without a Uniform source, because the inverse CDF step is optional.",
                    "omit_uniform",
                ),
                c(
                    "c",
                    "Draw U ~ Normal(0,1) and set X = F(U), using the CDF rather than the inverse CDF.",
                    "wrong_source_and_map",
                ),
                c(
                    "d",
                    "Set X = F(U) with U already equal to X, which makes Uniform sampling unnecessary.",
                    "circular_definition",
                ),
            ],
            correct="a",
            explanation="Method fluency requires naming Uniform(0,1) and applying the inverse CDF.",
            model_answer="U ~ Uniform(0,1); X = F^{-1}(U).",
            common_mistake="Omitting the Uniform source.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly outlines discrete inverse-transform sampling and refuses a software-only substitute for the method?",
            body="Choose discrete outline plus method warrant.",
            choices=[
                c(
                    "a",
                    "Draw U ~ Uniform(0,1) and assign the discrete value whose CDF first exceeds U (inverse CDF or threshold rule). Software sampling can implement the draw, but the learning objective requires understanding inverse transform, not only calling a black box.",
                ),
                c(
                    "b",
                    "For discrete variables, skip Uniform and thresholds and only call a sampler such as rbinom, because software replaces the method.",
                    "software_replaces_method",
                ),
                c(
                    "c",
                    "Discrete inverse transform uses Normal draws rather than Uniform, and understanding the method is optional once a library exists.",
                    "normal_not_uniform",
                ),
                c(
                    "d",
                    "Assign outcomes by sorting probabilities alphabetically with no Uniform threshold, which finishes the inverse-transform LO.",
                    "alphabetical_rule",
                ),
            ],
            correct="a",
            explanation="2.1.5 is method competence; software alone does not satisfy the learning objective.",
            model_answer="Discrete: Uniform then CDF threshold. Refuse treating a sampler call as a substitute for the method.",
            common_mistake="Only saying use rbinom without the inverse idea.",
        ),
    },
    "2.2.2-independence-cs1005.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly gives a clear independence condition for X and Y using joint and marginal language?",
            body="Select the factorisation warrant.",
            choices=[
                c(
                    "a",
                    "X and Y are independent if the joint equals the product of the marginals for all (x, y) in the support (or an equivalent form such as conditional equals marginal).",
                ),
                c(
                    "b",
                    "X and Y are independent whenever their covariance is defined, even if the joint does not factor into marginals.",
                    "covariance_as_independence",
                ),
                c(
                    "c",
                    "Independence means the joint equals the sum of the marginals for all (x, y).",
                    "sum_not_product",
                ),
                c(
                    "d",
                    "Independence requires only that each marginal exists; the joint need not equal the product of those marginals.",
                    "marginals_only",
                ),
            ],
            correct="a",
            explanation="Independence is joint factorisation into marginals, or an equivalent CMP form.",
            model_answer="Joint equals product of marginals on the support (or equivalent conditional-equals-marginal form).",
            common_mistake="Skipping the factorisation hinge or confusing independence with weaker association summaries.",
        ),
        "cp": _item(
            prompt="Closed-book. A student says correlation is zero, so X and Y are independent. Which statement is correct?",
            body="Refuse the claim; state the stronger warrant.",
            choices=[
                c(
                    "a",
                    "Refuse: zero correlation is not independence. Independence requires joint factorisation (or equivalent). Uncorrelated is weaker and can fail under nonlinear dependence.",
                ),
                c(
                    "b",
                    "Accept: zero correlation is necessary and sufficient for independence in all bivariate settings.",
                    "accept_zero_corr",
                ),
                c(
                    "c",
                    "Refuse independence language entirely, and treat zero correlation as proving the joint cannot factor.",
                    "corr_blocks_factor",
                ),
                c(
                    "d",
                    "Zero correlation is stronger than independence, so factorisation of the joint is unnecessary once corr(X,Y)=0.",
                    "corr_stronger",
                ),
            ],
            correct="a",
            explanation="Uncorrelated does not imply independent; independence needs the joint factorisation warrant.",
            model_answer="Refuse equating zero correlation with independence; require joint factorisation or equivalent.",
            common_mistake="Accepting the forbidden zero-correlation claim.",
        ),
    },
    "2.6.2-sampling-distribution-statistic-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly distinguishes a statistic, its sampling distribution, and one realised value from one sample?",
            body="Select the three-way discrimination.",
            choices=[
                c(
                    "a",
                    "A statistic is a function of the sample. Its sampling distribution is the distribution of that statistic over repeated random samples. One realised value is a single draw from that distribution, not the distribution itself.",
                ),
                c(
                    "b",
                    "A statistic is a fixed population parameter, and its sampling distribution is that same constant number.",
                    "statistic_is_parameter",
                ),
                c(
                    "c",
                    "The sampling distribution is the single realised sample mean from the data set you hold, and repeated-sample language is optional.",
                    "realised_is_distribution",
                ),
                c(
                    "d",
                    "A realised statistic equals its sampling distribution whenever the sample size is larger than 30.",
                    "n30_collapse",
                ),
            ],
            correct="a",
            explanation="The learning objective separates the statistic, its repeated-sample distribution, and one realised draw.",
            model_answer="Statistic = function of sample; sampling distribution = law over repeated samples; realised value = one draw.",
            common_mistake="Collapsing the realised value into the sampling distribution.",
        ),
        "cp": _item(
            prompt="Closed-book. A colleague says my sample mean is 12, so the sampling distribution is 12. Which statement is correct?",
            body="Refuse the collapse; restate the LO.",
            choices=[
                c(
                    "a",
                    "Refuse: a realised statistic is not its sampling distribution. The skill is describing the distribution of the statistic over repeated samples.",
                ),
                c(
                    "b",
                    "Accept: the sampling distribution equals whatever number the current sample mean takes.",
                    "accept_realised",
                ),
                c(
                    "c",
                    "Refuse only if n is small; for large n the realised mean is the sampling distribution.",
                    "large_n_exception",
                ),
                c(
                    "d",
                    "The claim is correct because parameters and sampling distributions are the same object once a mean is computed.",
                    "parameter_collapse",
                ),
            ],
            correct="a",
            explanation="A realised statistic is one draw; the sampling distribution is the repeated-sample law.",
            model_answer="Refuse equating the realised mean with the sampling distribution; describe the repeated-sample distribution of the statistic.",
            common_mistake="Accepting the forbidden realised-value claim.",
        ),
    },
    "4.2-glm-structure-ea006.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly explains how a GLM joins an exponential-family response, a linear predictor, and a link function?",
            body="Select the three-part structure with eta distinguished from the link.",
            choices=[
                c(
                    "a",
                    "A GLM specifies an exponential-family response, forms a linear predictor eta = X beta, and connects the mean to eta through a link g(mu) = eta. Non-Normal outcomes stay inside a linear modelling frame. The link is not the same object as the linear predictor.",
                ),
                c(
                    "b",
                    "A GLM is linear regression with different software, and the link function is identical to the linear predictor eta.",
                    "software_and_conflation",
                ),
                c(
                    "c",
                    "GLMs allow only Normal responses with identity link; exponential-family language is optional decoration.",
                    "normal_only",
                ),
                c(
                    "d",
                    "The linear predictor maps the mean into restricted support, while the link is the design matrix X without coefficients.",
                    "roles_scrambled",
                ),
            ],
            correct="a",
            explanation="A GLM joins exponential-family response, eta = X beta, and g(mu) = eta. Normal plus identity is a special case, not the definition.",
            model_answer="Exponential-family response; eta = X beta; g(mu) = eta; distinguish link from linear predictor.",
            common_mistake="Treating GLM as linear regression with software, or conflating the link with the linear predictor.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly pairs a non-Normal GLM family with a justified canonical link?",
            body="Justify from mean range, not software defaults.",
            choices=[
                c(
                    "a",
                    "Poisson with log link (canonical): the mean must stay positive, and log maps (0, infinity) onto the real line for eta. Binomial with logit is a similar mean-range pairing.",
                ),
                c(
                    "b",
                    "Poisson with log link only because glm() defaults to it, with no mean-range reasoning required.",
                    "software_default",
                ),
                c(
                    "c",
                    "Poisson with identity link as canonical because counts already live on the whole real line.",
                    "identity_for_poisson",
                ),
                c(
                    "d",
                    "Binomial with log link as the usual canonical choice because probabilities are unrestricted on the real line.",
                    "wrong_binomial_link",
                ),
            ],
            correct="a",
            explanation="Canonical links map the mean into an unrestricted linear predictor while respecting response support.",
            model_answer="Poisson-log (or binomial-logit) justified by mean range, not by software habit.",
            common_mistake="Saying the link is used because software defaults to it.",
        ),
    },
    "4.2.3-link-canonical-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly explains how a GLM joins exponential-family response, linear predictor eta, and link g(mu)=eta while distinguishing eta from the link?",
            body="Select the structure discrimination for the link LO.",
            choices=[
                c(
                    "a",
                    "The response is in an exponential family; eta = X beta is the linear predictor; g(mu) = eta links the mean to that predictor. The link function is not the same object as eta.",
                ),
                c(
                    "b",
                    "Eta and the link are the same object, so writing g(mu) = eta is only optional notation.",
                    "eta_is_link",
                ),
                c(
                    "c",
                    "The link replaces the exponential-family response, and eta is unused once a family is named.",
                    "link_replaces_family",
                ),
                c(
                    "d",
                    "GLMs join only a Normal response to an identity mean with no separate link idea.",
                    "normal_identity_only",
                ),
            ],
            correct="a",
            explanation="Link competence requires naming response family, eta, and g(mu)=eta as distinct structural pieces.",
            model_answer="Exponential-family response; eta = X beta; g(mu)=eta; link is not eta.",
            common_mistake="Conflating the link with the linear predictor or skipping the three-part join.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly names a non-Normal family with its canonical link and justifies the choice from mean range?",
            body="Choose distributional link warrant; refuse software-default theatre.",
            choices=[
                c(
                    "a",
                    "Poisson with log (canonical): mean is positive and log maps (0, infinity) to the reals for eta. Binomial with logit is similarly justified by mapping probabilities in (0,1) to the real line.",
                ),
                c(
                    "b",
                    "Any link is canonical for any family because software will pick a default automatically.",
                    "any_link_canonical",
                ),
                c(
                    "c",
                    "Poisson with logit as canonical because counts are probabilities on (0,1).",
                    "poisson_logit",
                ),
                c(
                    "d",
                    "Binomial with identity as canonical because probabilities already equal eta with no transform needed for mean range.",
                    "binomial_identity",
                ),
            ],
            correct="a",
            explanation="Canonical links are justified by mean range and support, not by software defaults.",
            model_answer="Poisson-log or binomial-logit with mean-range justification.",
            common_mistake="Accepting a software-default justification without mean-range reasoning.",
        ),
    },
    "4.2.5-linear-predictor-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly writes linear predictors for a simple slope, a two-level factor with baseline coding, and a quadratic term in x?",
            body="Select the three eta forms.",
            choices=[
                c(
                    "a",
                    "Simple slope: eta = beta0 + beta1 x. Two-level factor with baseline coding: eta = beta0 + beta_A I_A (versus baseline). Quadratic: eta = beta0 + beta1 x + beta2 x^2.",
                ),
                c(
                    "b",
                    "All three cases use only eta = beta0, because factors and polynomials are handled entirely by the link function.",
                    "intercept_only",
                ),
                c(
                    "c",
                    "A two-level factor must enter as a multiplicative link term rather than an indicator in eta, and a quadratic term is written without coefficients.",
                    "factor_in_link",
                ),
                c(
                    "d",
                    "Quadratic terms are forbidden in linear predictors, and factor coding always absorbs the intercept so beta0 disappears.",
                    "no_quadratic",
                ),
            ],
            correct="a",
            explanation="Linear-predictor fluency covers continuous slopes, baseline factor coding, and polynomial terms inside eta.",
            model_answer="beta0+beta1x; beta0+beta_A I_A; beta0+beta1x+beta2x^2.",
            common_mistake="Skipping factor or polynomial forms, or moving structure into the link by habit.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly refuses treating the link function as the linear predictor and restates both objects?",
            body="Refuse conflation; restate eta and the link.",
            choices=[
                c(
                    "a",
                    "Refuse: the link is not the linear predictor. Eta = X beta is the linear predictor; the link g maps the mean mu to eta.",
                ),
                c(
                    "b",
                    "Accept: link and linear predictor are two names for the same eta object.",
                    "accept_conflation",
                ),
                c(
                    "c",
                    "Refuse the word link, but treat g(mu) as identical to X beta with no mapping role for the mean.",
                    "refuse_word_only",
                ),
                c(
                    "d",
                    "The linear predictor maps mu to a restricted range, while the link is only the coefficient vector beta.",
                    "roles_reversed",
                ),
            ],
            correct="a",
            explanation="Eta is X beta; the link maps mean to eta. Conflating them breaks GLM structure.",
            model_answer="Refuse conflation. Eta = X beta; link g maps mu to eta.",
            common_mistake="Accepting that the link function is the linear predictor.",
        ),
    },
    "5.1.1-bayes-theorem-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly states Bayes' theorem connecting prior, likelihood, and posterior?",
            body="Select the update warrant.",
            choices=[
                c(
                    "a",
                    "Posterior is proportional to prior times likelihood (then normalised). Bayes updates beliefs about an event or parameter given the data.",
                ),
                c(
                    "b",
                    "Posterior equals the likelihood alone; the prior is discarded once data arrive.",
                    "likelihood_only",
                ),
                c(
                    "c",
                    "Posterior equals the prior alone; likelihood is used only for frequentist tests.",
                    "prior_only",
                ),
                c(
                    "d",
                    "Bayes equates P(A|B) with P(B|A) automatically, so prior and likelihood need not be combined.",
                    "inverse_collapse",
                ),
            ],
            correct="a",
            explanation="Bayes updates by combining prior and likelihood into a normalised posterior.",
            model_answer="Posterior proportional to prior times likelihood (normalised).",
            common_mistake="Skipping the prior-likelihood product or equating inverse conditionals.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly refuses treating P(disease|positive) as equal to P(positive|disease) without calculation?",
            body="Refuse inverse confusion; state what Bayes requires.",
            choices=[
                c(
                    "a",
                    "Refuse inverse confusion. The two conditionals are not equal. Bayes combines a prior (base rate) with the likelihood of the data to obtain the posterior.",
                ),
                c(
                    "b",
                    "Accept the equality because positive tests and disease status are interchangeable labels.",
                    "accept_inverse",
                ),
                c(
                    "c",
                    "Refuse only when base rates are unknown; if prevalence is known, P(disease|positive) equals P(positive|disease) automatically.",
                    "base_rate_makes_equal",
                ),
                c(
                    "d",
                    "Bayes requires replacing the prior with the likelihood alone, which makes the two conditionals equal after any positive test.",
                    "replace_prior",
                ),
            ],
            correct="a",
            explanation="Inverse probability confusion ignores base rates; Bayes combines prior and likelihood.",
            model_answer="Refuse equating the inverse conditionals; combine prior (base rate) with likelihood.",
            common_mistake="Accepting P(disease|positive) = P(positive|disease) without Bayes.",
        ),
    },
    "5.1.5-credible-intervals-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly gives the Bayesian probability claim made by a 95% credible interval?",
            body="Select the posterior probability reading.",
            choices=[
                c(
                    "a",
                    "Under the posterior, the parameter lies in the interval with probability 95% (for a 95% credible interval).",
                ),
                c(
                    "b",
                    "In repeated samples, 95% of such random intervals will cover the fixed parameter, which is the credible-interval reading.",
                    "frequentist_slogan",
                ),
                c(
                    "c",
                    "The interval contains 95% of the sample observations, not a probability statement about the parameter.",
                    "sample_coverage",
                ),
                c(
                    "d",
                    "A 95% credible interval means the posterior mean equals 0.95, with no probability claim about an interval for the parameter.",
                    "mean_is_95",
                ),
            ],
            correct="a",
            explanation="A credible interval is a posterior probability statement about the parameter.",
            model_answer="Posterior probability 95% that the parameter lies in the interval.",
            common_mistake="Copying a frequentist coverage slogan onto the credible interval.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly refuses copying a frequentist confidence slogan onto a credible interval and states what differs?",
            body="Refuse slogan copy; contrast the readings.",
            choices=[
                c(
                    "a",
                    "Refuse slogan copy. Credible intervals are posterior probability statements about the parameter. Confidence intervals have a different frequentist coverage reading over repeated samples.",
                ),
                c(
                    "b",
                    "Accept the copy: credible and confidence intervals always have identical probability readings about the parameter.",
                    "accept_slogan_copy",
                ),
                c(
                    "c",
                    "Refuse credible intervals entirely because only frequentist coverage language is ever valid for interval estimates.",
                    "reject_credible",
                ),
                c(
                    "d",
                    "The difference is only notation: once an interval is computed, posterior probability and frequentist coverage are the same claim.",
                    "notation_only",
                ),
            ],
            correct="a",
            explanation="Credible and confidence intervals answer different probability questions; slogans must not be copied blindly.",
            model_answer="Refuse slogan copy. Credible: posterior probability for the parameter. Confidence: frequentist coverage reading.",
            common_mistake="Accepting a frequentist confidence slogan as the credible-interval meaning.",
        ),
    },
}

STEM_TO_INVENTORY: dict[str, str] = {
    inv_key.removesuffix(".json"): inv_key for inv_key in CONVERSIONS
}
INVENTORY_TO_STEM: dict[str, str] = {v: k for k, v in STEM_TO_INVENTORY.items()}

# Inventory filename -> campaign twin relative path under educational_campaigns/cs1/
# Alpha/Beta use shorter campaign filenames; ea006 is catalogue-only.
CAMPAIGN_TWINS: dict[str, str] = {
    "1.1-purpose-function-ep001.json": "campaign-alpha-ep001/packages/1.1-purpose-function-ep001.json",
    "1.2.1-eda-summaries-ep001.json": "campaign-alpha-ep001/packages/1.2-eda-summaries-ep001.json",
    "1.2.2-eda-association-ep001.json": "campaign-alpha-ep001/packages/1.2-eda-association-ep001.json",
    "1.2.3-pca-cs1002.json": "campaign-beta-cs1002/packages/1.2-pca-cs1002.json",
    "2.1.1-discrete-cs1002.json": "campaign-beta-cs1002/packages/2.1-discrete-cs1002.json",
    "2.1.2-continuous-cs1002.json": "campaign-beta-cs1002/packages/2.1-continuous-cs1002.json",
    "2.1.3-prob-quantiles-cs1004.json": "campaign-gamma-cs1004/packages/2.1.3-prob-quantiles-cs1004.json",
    "2.1.4-poisson-process-cs1004.json": "campaign-gamma-cs1004/packages/2.1.4-poisson-process-cs1004.json",
    "2.1.5-inverse-transform-cs1004.json": "campaign-gamma-cs1004/packages/2.1.5-inverse-transform-cs1004.json",
    "2.2.2-independence-cs1005.json": "campaign-epsilon-cs1005/packages/2.2.2-independence-cs1005.json",
    "2.6.2-sampling-distribution-statistic-cs1009.json": "campaign-iota-cs1009/packages/2.6.2-sampling-distribution-statistic-cs1009.json",
    "4.2.3-link-canonical-cs1003.json": "campaign-delta-cs1003/packages/4.2.3-link-canonical-cs1003.json",
    "4.2.5-linear-predictor-cs1003.json": "campaign-delta-cs1003/packages/4.2.5-linear-predictor-cs1003.json",
    "5.1.1-bayes-theorem-cs1003.json": "campaign-delta-cs1003/packages/5.1.1-bayes-theorem-cs1003.json",
    "5.1.5-credible-intervals-cs1003.json": "campaign-delta-cs1003/packages/5.1.5-credible-intervals-cs1003.json",
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace in-scope Active Recall and Checkpoint checks with Batch 6A MCQs."""
    inv_key = STEM_TO_INVENTORY.get(stem)
    if not inv_key:
        return pkg
    parts = CONVERSIONS[inv_key]
    updated_checks: list[dict[str, Any]] = []
    for check in pkg.get("knowledge_checks") or []:
        updated = dict(check)
        if check.get("kind") == "active_recall":
            updated.update(parts["ar"])
        elif check.get("kind") == "checkpoint":
            updated.update(parts["cp"])
        updated_checks.append(updated)
    pkg["knowledge_checks"] = updated_checks
    return pkg


def sync_catalogue_twins(root: Path | None = None) -> int:
    """Patch catalogue twins with Batch 6A MCQ knowledge checks."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key in CONVERSIONS:
        path = catalogue_dir / inv_key
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def sync_campaign_twins(root: Path | None = None) -> int:
    """Patch campaign twins with Batch 6A MCQ knowledge checks."""
    repo = root or Path(__file__).resolve().parents[1]
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        path = campaign_dir / rel_path
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    """Scan synced checks for structural and student-facing writing defects."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    duplicate = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
    # Avoid flagging mathematical "x x" style; keep prior-batch meta patterns.
    meta_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bcampaign\b",
            r"\bjourney\b",
            r"Batch \d",
            r"Wave \d",
            r"Isolated Golden Day",
            r"spine claims",
        )
    ]
    # Known false-positive duplicate tokens in maths (e.g. "x x" in x^2 prose).
    duplicate_allow = {"x"}
    defects: list[str] = []
    paths: list[Path] = []
    for inv_key in CONVERSIONS:
        paths.append(catalogue_dir / inv_key)
        twin = CAMPAIGN_TWINS.get(inv_key)
        if twin:
            paths.append(campaign_dir / twin)
    for path in paths:
        if not path.exists():
            defects.append(f"MISSING: {path}")
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        checks = {
            check.get("kind"): check for check in pkg.get("knowledge_checks") or []
        }
        for kind in ("active_recall", "checkpoint"):
            check = checks.get(kind)
            if check is None:
                defects.append(f"{path.name} {kind}: missing")
                continue
            if check.get("response_type") != "mcq":
                defects.append(f"{path.name} {kind}: not mcq")
            choices = check.get("choices") or []
            if [choice.get("id") for choice in choices] != ["a", "b", "c", "d"]:
                defects.append(f"{path.name} {kind}: bad choice ids")
            if len(choices) != 4:
                defects.append(f"{path.name} {kind}: not 4 choices")
            if check.get("correct_choice_id") not in {"a", "b", "c", "d"}:
                defects.append(f"{path.name} {kind}: bad correct_choice_id")
            for field in ("explanation", "model_answer", "common_mistake", "body"):
                if not check.get(field):
                    defects.append(f"{path.name} {kind}: missing {field}")
            if not str(check.get("prompt", "")).startswith("Closed-book."):
                defects.append(f"{path.name} {kind}: prompt is not closed-book")
            for choice in choices:
                tag = choice.get("misconception_tag")
                if choice.get("id") == check.get("correct_choice_id") and tag:
                    defects.append(f"{path.name} {kind}: correct choice has tag")
                if choice.get("id") != check.get("correct_choice_id") and not tag:
                    defects.append(f"{path.name} {kind}: distractor missing tag")
            blob = json.dumps(check, ensure_ascii=False)
            if "\u2014" in blob:
                defects.append(f"{path.name} {kind}: em dash found")
            for match in duplicate.finditer(blob):
                word = match.group(1)
                if word.lower() in duplicate_allow:
                    continue
                defects.append(
                    f"{path.name} {kind}: duplicate word '{word}'"
                )
            for pattern in meta_patterns:
                if pattern.search(blob):
                    defects.append(
                        f"{path.name} {kind}: meta language '{pattern.pattern}'"
                    )
    return defects


if __name__ == "__main__":
    campaign_count = sync_campaign_twins()
    catalogue_count = sync_catalogue_twins()
    scan = mechanical_defect_scan()
    print(
        f"Synced {campaign_count} campaign + {catalogue_count} catalogue twins."
    )
    if scan:
        print("DEFECTS:")
        for defect in scan:
            print(" ", defect)
    else:
        print("Mechanical defect scan: PASS (0 issues)")
