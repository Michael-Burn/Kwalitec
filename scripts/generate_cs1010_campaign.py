#!/usr/bin/env python3
"""Generate CS1-010 / Campaign Kappa educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

from _mcq_batch1_section3_payload import apply_mcq_overlay
from _mcq_batch6b_revision_payload import apply_mcq_overlay as apply_batch6b_mcq_overlay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-kappa-cs1010"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1010-campaign-kappa-1.0.0",
    "publication_version": "cs1010-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-KAPPA",
    "volume_id": "CS1-010",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1010_EDUCATIONAL_VOLUME.md",
        "CS1010_CERTIFICATION_REPORT.md",
        "EP008_WAVE8_PLAN.md",
    ],
    "author_id": "cs1010-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "3.1",
    "topic_title": "Construct estimators and discuss their properties",
    "topic_id": "CS1-C-T01",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "3.1", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1010-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1010-cs1-{d['slug']}",
            "display_title": d["title"],
            "mission_purpose": d["purpose"],
            "tutor_intent": d["tutor"],
            "educational_intent": d["edu"],
            "learning_objective": d["lo_text"],
            "concept_focus": d["focus"],
            "prior_bridge": d["prior"],
            "why_now": d["why"],
            "expected_benefit": d["benefit"],
            "explainability": d["explain"],
            "success_criteria": d["criteria"],
            "task_descriptions": d["tasks"],
            "estimated_study_time_minutes": {"min": 55, "max": 75},
        },
        "session": {
            "session_id": f"ssn-cs1010-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Mission for Syllabus {lo}. Not the next LO as primary."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo}, exit to CMP, retrieve today's hinge, refuse swallowed next LO."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo}. This is Study Progress for today's block. Not Topic Complete "
                f"for later 3.1 LOs, Chapter 3 trophy, intervals (3.2), hypothesis testing (3.3), "
                "or until-exam trust."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} hinge closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to extract Syllabus {lo}–"
                f"{d['title'].lower()}. Stop before out-of-scope later LOs."
            ),
            "focus_questions": [
                f"What is the core move of Syllabus {lo}?",
                "What warrant separates today's skill from yesterday's?",
                "What claim must you refuse today?",
                "What will you practise in Knowledge Checks after the CMP?",
            ],
            "misconception_watch": d["misconceptions"],
            "open_point": d["open"],
            "stop_condition": d["stop"],
            "out_of_scope_today": d["oos"],
            "annotation_task": "Before deep reading: sketch today's concept chain in notes",
            "attempt_before_reveal": (
                "At the first worked example, cover the answer and attempt the middle step"
            ),
            "exit_line": (
                f"Open your CMP (IFoA CS1 Core Reading / CMP · 2026 syllabus alignment) at "
                f"{d['open']}. Kwalitec is the guide; the CMP is the authoritative material. "
                "do not treat this activity body as a substitute textbook. Hunt with the focus "
                "questions; watch the misconception list. Ignore items in out_of_scope_today. "
                f"Stop when: {d['stop']}. Then close the CMP and return here. Next in-app "
                "activity: Worked-example re-entry (CMP closed), then Knowledge Checks."
            ),
            "return_cue": (
                f"You are finished with Guided Reading when the CMP {lo} block meets the stop "
                "condition and you can answer today's focus questions from your notes. Close the "
                "CMP and return to Kwalitec. Immediate next activity: Worked-example re-entry, "
                "then Knowledge Checks (Active Recall → Checkpoint)."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause. Write today's core move in one sentence.",
                    "student_action": "Annotate",
                },
                {
                    "id": "PP2",
                    "cue": "Attempt the next worked step before uncovering the solution.",
                    "student_action": "Attempt",
                },
            ],
            "reentry_line": (
                "Welcome back. Keep your CMP closed. Immediate next activity: "
                "Worked-example re-entry, then Knowledge Checks."
            ),
        },
        "knowledge_checks": [
            {
                "episode_id": f"lep-cs1010-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1010-{lo}-ar-01",
                "title": f"Active Recall: {lo}",
                "prompt": d["ar_prompt"],
                "response_type": "short_structured",
                "body": f"Retrieve {lo} closed-book.",
                "hints": ["Use CMP language from today's notes.", "Stay inside today's LO."],
                "accepted_keywords": d["ar_kw"],
                "explanation": f"Active recall for {lo}.",
                "model_answer": d["ar_model"],
                "common_mistake": "Skipping the LO hinge or swallowing the next LO.",
                "success_criteria": ["Addresses the prompt structure.", "Stays inside today's LO."],
            },
            {
                "episode_id": f"lep-cs1010-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1010-{lo}-cp-01",
                "title": f"Checkpoint: {lo}",
                "prompt": d["cp_prompt"],
                "response_type": "short_structured",
                "body": f"Checkpoint refuse/warrant for {lo}.",
                "hints": ["Name the refusal clearly.", "Give a positive warrant."],
                "accepted_keywords": d["cp_kw"],
                "explanation": f"Checkpoint for {lo}.",
                "model_answer": d["cp_model"],
                "common_mistake": "Accepting the forbidden claim.",
                "success_criteria": ["Refusal present.", "Positive warrant present."],
            },
        ],
        "reflection": {
            "framing": d["reflect"],
            "prompt": (
                f"Which part of today's {lo} move is stickiest and why? Quote or paraphrase "
                "the single CMP cue still unclear. If you had five minutes tomorrow, what one "
                "move would you rework?"
            ),
            "prompts": [
                f"Which part of {lo} is stickiest and why?",
                "Quote or paraphrase the single CMP cue still unclear.",
                "If you had five minutes tomorrow, what one move would you rework?",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": d["next_code"],
            "next_topic_title": d["next_title"],
            "continuity_line": d["cont"],
            "light_prep_cue": d["prep"],
            "student_facing": d["student"],
        },
    }


def revision_pkg() -> dict:
    day = "CK-R1"
    pid = "CS1-EP001-PKG-REV-ESTIMATORS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Kappa revision: estimators and their properties",
        "return_targets": ["3.1.1", "3.1.2", "3.1.3", "3.1.4", "3.1.5", "3.1.6"],
        "topic_aliases": [day, "campaign-kappa-revision"],
        "topic_title_keywords": [
            "revision",
            "estimator",
            "moments",
            "likelihood",
            "bias",
            "MSE",
            "efficiency",
            "consistency",
            "asymptotic",
            "bootstrap",
        ],
        "golden_id": "GOLDEN-CS1010-CS1-CK-R1-ESTIMATORS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1010-cs1-ck-r1-estimators",
            "display_title": "Retrieve estimator hinges (3.1)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Kappa. Retrieving "
                "method of moments, maximum likelihood, efficiency/bias/consistency/MSE, "
                "estimator comparison, asymptotic MLE behaviour, and bootstrap. So 3.1 does "
                "not evaporate before intervals (3.2)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Kappa's Learning hinges. "
                "not a passive CMP re-read and not a first-pass 3.2 intervals lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: moments → "
                "MLE → estimator properties → comparison → asymptotic MLE → bootstrap."
            ),
            "learning_objective": (
                "Retrieve and connect (1) method of moments, (2) maximum likelihood, "
                "(3) efficiency / bias / consistency / MSE, (4) comparison via MSE and bias, "
                "(5) asymptotic distribution of MLEs, and (6) bootstrap for estimator properties."
            ),
            "concept_focus": (
                "Campaign chain retrieval: MoM → MLE → properties → comparison → asymptotics "
                "→ bootstrap."
            ),
            "prior_bridge": (
                "Yesterday you finished bootstrap for estimator properties (3.1.6). Today is "
                "Revision mode: return to 3.1.1–3.1.6 under closed-book retrieval. No new "
                "first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 3.2 work."
            ),
            "expected_benefit": (
                "Evidence that the 3.1 chain retrieves. Revision Study Progress, not a claim "
                "that Chapter 3 / the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the six 3.1 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse Chapter 3 complete / spine / until-exam / 3.2-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Kappa's chain: MoM → MLE → properties → "
                "comparison → asymptotics → bootstrap.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 45, "max": 60},
        },
        "session": {
            "session_id": "ssn-cs1010-cs1-ck-r1-estimators",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Kappa skills. Not to teach 3.2."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 45, "max": 60},
            "wrap_up": (
                "Revision Session complete. You stress-tested 3.1.1–3.1.6 return targets. "
                "This is revision Study Progress. Not Topic Complete for 3.2, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that estimator hinges will still retrieve in three "
                "days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Kappa "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the six 3.1 Learning hinges in order?",
                "Can you state when MoM vs MLE and when MSE comparison enters?",
                "What claim must you refuse (Chapter 3 complete / spine / until-exam / 3.2 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 3 / spine / until-exam complete.",
                "Watch for dropping Iota sampling-distribution memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not begin Syllabus 3.2 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass confidence / prediction intervals (3.2)",
                "Hypothesis testing primary (3.3)",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Chapter 3 complete trophy claim",
            ],
            "annotation_task": "Before checks: sketch return-target chain from memory",
            "attempt_before_reveal": "Attempt each check before any targeted CMP reopen",
            "exit_line": (
                "Begin closed-book retrieval. Reopen CMP only at a failed locus. After checks, "
                "complete Reflection."
            ),
            "return_cue": (
                "Revision reading stage is complete when checks are attempted and any failed "
                "locus has a targeted reopen plan."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause. Mark the weakest link before checks.",
                    "student_action": "Annotate",
                }
            ],
            "reentry_line": "Stay closed-book unless a check failed. Continue retrieval.",
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1010-ck-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1010-ck-r1-ar-01",
                "title": "Active Recall: CK-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) method of "
                    "moments; (2) maximum likelihood; (3) efficiency / bias / consistency / "
                    "MSE; (4) comparison via MSE and bias; (5) asymptotic distribution of "
                    "MLEs; (6) bootstrap for estimator properties."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 3.1.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "moments",
                    "likelihood",
                    "bias",
                    "MSE",
                    "efficiency",
                    "consistency",
                    "asymptotic",
                    "bootstrap",
                    "estimator",
                ],
                "explanation": "Revision retrieves the 3.1 arc.",
                "model_answer": (
                    "Example: (1) equate sample moments to population moments; (2) maximise "
                    "likelihood / log-likelihood; (3) define bias, variance, MSE, efficiency, "
                    "consistency; (4) compare estimators by MSE / bias; (5) asymptotic Normal "
                    "behaviour of MLEs under CMP conditions; (6) resample to estimate "
                    "estimator properties."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Six hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1010-ck-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1010-ck-r1-cp-01",
                "title": "Checkpoint: CK-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest estimator link and one concrete "
                    "rework. (2) Refuse: 'Moments and MLE are interchangeable, so Chapter 3 "
                    "is done.' (3) Name the honest next topic (confidence intervals, 3.2) or "
                    "confirm you are stopping here."
                ),
                "response_type": "short_structured",
                "body": "Weakest link + honest next.",
                "hints": ["Name a concrete rework.", "Refuse forbidden claims."],
                "accepted_keywords": [
                    "weak",
                    "rework",
                    "refuse",
                    "spine",
                    "chapter",
                    "3.2",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. asymptotic MLE variance. Five-minute rework. (2) Refuse "
                    "Chapter 3 complete / spine / until-exam. (3) Honest next is 3.2 "
                    "(successor Volume) or declared stop. Not claimed finished here."
                ),
                "common_mistake": "Spine / Chapter 3 / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which link retrieved least cleanly today and what one concrete rework will "
                "you schedule? Do not claim the rest of Chapter 3 is finished from one retrieval sitting."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Do not claim the rest of Chapter 3 is finished from one retrieval sitting.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "3.2",
            "next_topic_title": (
                "Honest next: confidence and prediction intervals (3.2) under a successor "
                "Volume (or declared stop)"
            ),
            "continuity_line": (
                "Campaign Kappa / Volume CS1-010 completes after this Revision. Honest stop: "
                "3.1 Pilot Arc closed. Not Chapter 3 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 3.2 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Kappa / CS1-010 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 3.2 successor Volume. Optional: schedule your "
                "weakest 3.1 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CK-D1",
        stem="3.1.1-method-of-moments-cs1010",
        pid="CS1-EP001-PKG-3.1-METHOD-OF-MOMENTS",
        lo="3.1.1",
        slug="3.1-method-of-moments",
        keywords=["moments", "method", "estimator", "population", "sample", "parameter"],
        title="Construct estimators by the method of moments",
        purpose=(
            "Today's Mission exists to construct estimators of population parameters by the "
            "method of moments (so the MoM move is usable) without pretending maximum "
            "likelihood (3.1.2) is finished."
        ),
        tutor=(
            "Today I will force the candidate to equate sample moments to population moments "
            "and solve for the parameter. And refuse treating 'I wrote an estimator' as "
            "having the MoM LO."
        ),
        edu=(
            "Produce a cognitive move from population moments to a method-of-moments "
            "estimator under CMP language."
        ),
        lo_text=(
            "Method of moments for constructing estimators of population parameters."
        ),
        focus="Population moments → sample moments → solve for parameter → refuse MLE-as-done.",
        prior=(
            "Campaign Iota closed sampling distributions (2.6) with Revision. Today opens "
            "topic 3.1 at LO 3.1.1. The named Continuity Front after CS1-009."
        ),
        why=(
            "3.1.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at estimators, keeping maximum likelihood for the following session."
        ),
        benefit=(
            "You will be able to construct a method-of-moments estimator by equating "
            "sample moments to population moments and solving."
        ),
        explain=(
            "Day 1 opens 3.1 at the named learning objective. "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, state the method-of-moments construction move in CMP-usable form.",
            "Name how sample moments replace population moments.",
            "Refuse one 'any formula for θ̂ is MoM' claim.",
        ],
        tasks=[
            "Sketch population moments → sample moments → estimator before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.1.",
            "Closed-book Knowledge Checks: MoM construction + refuse MLE swallow.",
        ],
        next_code="3.1",
        next_title="Maximum likelihood estimators (3.1.2)",
        cont=(
            "Today you constructed estimators by method of moments; tomorrow continues 3.1 "
            "at maximum likelihood."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.1.2. Titles only tonight",
        student=(
            "Tomorrow: maximum likelihood (3.1.2). Optional light prep: skim 3.1.2 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.1.1 method of moments",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.1 "
            "(stop before maximum likelihood 3.1.2)"
        ),
        oos=[
            "Maximum likelihood as primary (3.1.2)",
            "Efficiency / bias / MSE primary (3.1.3)",
            "Asymptotics / bootstrap primary",
            "Confidence intervals (3.2)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating any estimator with method of moments.",
            "Watch for starting MLE drills (3.1.2) inside this sitting.",
            "Watch for interval construction (3.2) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the method-of-moments construction move? "
            "(2) What replaces population moments in the equations? (3) Name one reason "
            "'I have a formula for θ̂' is not automatically MoM."
        ),
        ar_kw=[
            "moments",
            "sample",
            "population",
            "equate",
            "estimator",
            "parameter",
        ],
        ar_model=(
            "Method of moments equates sample moments to the corresponding population "
            "moments (as functions of parameters) and solves for the parameter(s). Having "
            "any estimator formula is not the same as using that moment-matching move."
        ),
        cp_prompt=(
            "Closed-book. Claim sizes are modelled as Exponential with mean θ. A "
            "sample has mean x̄ = 4. (1) Write the population first-moment equation "
            "and the method-of-moments estimator for θ. (2) Refuse: 'I maximised the "
            "likelihood, so I already have the method-of-moments estimator.'"
        ),
        cp_kw=["moments", "equate", "sample", "population", "mean", "refuse", "likelihood", "MLE", "MoM"],
        cp_model=(
            "(1) E[X] = θ; equate x̄ = θ, so θ̂_MoM = x̄ = 4. (2) Refuse: maximising "
            "the likelihood is MLE, not MoM. MoM equates sample moments to "
            "population moments and solves."
        ),
        reflect="Harvest MoM algebra wobble. Keep MLE out of tonight's claim.",
    ),
    dict(
        day="CK-D2",
        stem="3.1.2-maximum-likelihood-cs1010",
        pid="CS1-EP001-PKG-3.1-MAXIMUM-LIKELIHOOD",
        lo="3.1.2",
        slug="3.1-maximum-likelihood",
        keywords=["likelihood", "maximum", "MLE", "log-likelihood", "estimator"],
        title="Construct estimators by maximum likelihood",
        purpose=(
            "Today's Mission exists to construct estimators by maximum likelihood. So the "
            "MLE move is usable. Without pretending efficiency/bias/MSE (3.1.3) is finished."
        ),
        tutor=(
            "Today I will force the candidate to form the likelihood / log-likelihood and "
            "maximise for the parameter. And refuse treating yesterday's MoM as finishing MLE."
        ),
        edu=(
            "Produce a cognitive move from a parametric model to an MLE under CMP language."
        ),
        lo_text=(
            "Method of maximum likelihood for constructing estimators of population parameters."
        ),
        focus="Likelihood / log-likelihood → maximise → MLE → refuse properties-as-done.",
        prior=(
            "Yesterday you constructed method-of-moments estimators (3.1.1). Today continues "
            "topic 3.1 at LO 3.1.2: maximum likelihood."
        ),
        why=(
            "3.1.2 is contiguous after MoM. Closing it prevents a cliff at MLE while keeping "
            "estimator properties as day three."
        ),
        benefit=(
            "You will be able to form and maximise a likelihood (or log-likelihood) "
            "to obtain an MLE for a simple parametric model."
        ),
        explain=(
            "Day 2 continues at the named learning objective. MLE immediately after MoM."
        ),
        criteria=[
            "Closed-book, state the maximum-likelihood construction move.",
            "Name why log-likelihood is often used.",
            "Refuse one 'MoM finished MLE' claim.",
        ],
        tasks=[
            "Sketch likelihood → log-likelihood → maximise before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.2.",
            "Closed-book Knowledge Checks: MLE construction + refuse MoM collapse.",
        ],
        next_code="3.1",
        next_title="Efficiency, bias, consistency and MSE (3.1.3)",
        cont=(
            "Today you constructed MLEs; tomorrow continues 3.1 at efficiency, bias, "
            "consistency and mean square error."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.1.3. Titles only tonight",
        student=(
            "Tomorrow: efficiency / bias / consistency / MSE (3.1.3). Optional light prep: "
            "skim 3.1.3 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.1.2 maximum likelihood",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.2 "
            "(stop before efficiency / bias / MSE 3.1.3)"
        ),
        oos=[
            "Efficiency / bias / consistency / MSE as primary (3.1.3)",
            "Estimator comparison as primary (3.1.4)",
            "Asymptotic MLE / bootstrap primary",
            "Confidence intervals (3.2)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating MoM as finishing today's LO.",
            "Watch for jumping into bias/MSE definitions as primary.",
            "Watch for CI construction (3.2) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the maximum-likelihood construction move? "
            "(2) Why is the log-likelihood often maximised instead? (3) How does this differ "
            "from method of moments?"
        ),
        ar_kw=[
            "likelihood",
            "log-likelihood",
            "maximise",
            "MLE",
            "parameter",
            "moments",
        ],
        ar_model=(
            "Maximum likelihood chooses the parameter value that maximises the likelihood "
            "(equivalently the log-likelihood under regularity). MoM matches moments; MLE "
            "maximises the model likelihood."
        ),
        cp_prompt=(
            "Closed-book. IID claims X₁,…,Xₙ ~ Exponential with rate λ (pdf λ "
            "e^{−λx} for x>0). (1) Write the log-likelihood for λ and state the MLE. "
            "(2) Refuse: 'Yesterday's method-of-moments estimator is the same skill "
            "as maximum likelihood.'"
        ),
        cp_kw=["likelihood", "log-likelihood", "maximise", "MLE", "rate", "refuse", "moments", "MoM"],
        cp_model=(
            "(1) ℓ(λ) = n ln λ − λ Σ xᵢ; MLE λ̂ = n/Σ xᵢ = 1/x̄. (2) Refuse: MoM "
            "matches moments; MLE maximises the likelihood (or log-likelihood). "
            "Different construction: even when numerical answers coincide."
        ),
        reflect="Harvest likelihood / score algebra wobble. Keep properties out of tonight.",
    ),
    dict(
        day="CK-D3",
        stem="3.1.3-efficiency-bias-consistency-mse-cs1010",
        pid="CS1-EP001-PKG-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE",
        lo="3.1.3",
        slug="3.1-efficiency-bias-consistency-mse",
        keywords=[
            "efficiency",
            "bias",
            "consistency",
            "MSE",
            "variance",
            "estimator",
        ],
        title="Discuss efficiency, bias, consistency and MSE of an estimator",
        purpose=(
            "Today's Mission exists to discuss efficiency, bias, consistency and mean square "
            "error of an estimator (so property language is usable) without pretending "
            "comparison of estimators (3.1.4) is finished."
        ),
        tutor=(
            "Today I will force the candidate to define bias, MSE, efficiency and consistency "
            "with CMP warrants. And refuse treating 'I can write an MLE' as finishing properties."
        ),
        edu=(
            "Produce a cognitive move from an estimator to its key properties under CMP "
            "language."
        ),
        lo_text=(
            "Efficiency, bias, consistency and mean square error of an estimator."
        ),
        focus="Bias · variance · MSE · efficiency · consistency. Refuse comparison-as-done.",
        prior=(
            "Yesterday you constructed MLEs (3.1.2). Today continues topic 3.1 at LO 3.1.3. "
            "estimator properties."
        ),
        why=(
            "3.1.3 is contiguous after construction methods. Closing it prevents a cliff at "
            "property language while keeping comparison as day four."
        ),
        benefit=(
            "You will be able to distinguish bias, MSE, efficiency, and consistency "
            "on a concrete estimator claim."
        ),
        explain=(
            "Day 3 continues at the named learning objective. Properties after construction."
        ),
        criteria=[
            "Closed-book, define bias and MSE of an estimator.",
            "State what consistency and efficiency mean at CMP level.",
            "Refuse one 'construction finished properties' claim.",
        ],
        tasks=[
            "Sketch bias / variance / MSE / efficiency / consistency before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.3.",
            "Closed-book Knowledge Checks: properties + refuse comparison swallow.",
        ],
        next_code="3.1",
        next_title="Comparison of estimators via MSE and bias (3.1.4)",
        cont=(
            "Today you discussed estimator properties; tomorrow continues 3.1 at comparing "
            "estimators using MSE and bias."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.1.4. Titles only tonight",
        student=(
            "Tomorrow: comparison of estimators (3.1.4). Optional light prep: skim 3.1.4 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.1.3 efficiency, bias, consistency and MSE",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.3 "
            "(stop before estimator comparison 3.1.4)"
        ),
        oos=[
            "Estimator comparison as primary (3.1.4)",
            "Asymptotic MLE distribution as primary (3.1.5)",
            "Bootstrap primary (3.1.6)",
            "Confidence intervals (3.2)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating construction methods as finishing properties.",
            "Watch for jumping into pairwise comparison drills as primary.",
            "Watch for confusing consistency with unbiasedness.",
        ],
        ar_prompt=(
            "Closed-book. (1) Define bias of an estimator. (2) How does MSE relate to bias "
            "and variance? (3) In one sentence each, what do efficiency and consistency mean?"
        ),
        ar_kw=[
            "bias",
            "MSE",
            "variance",
            "efficiency",
            "consistency",
            "estimator",
        ],
        ar_model=(
            "Bias is E[θ̂] − θ (CMP form). MSE = Var(θ̂) + (bias)² under standard "
            "decomposition. Efficiency compares variance (or MSE) relative to a benchmark; "
            "consistency concerns convergence in probability as sample size grows."
        ),
        cp_prompt=(
            "Closed-book. Estimator A is unbiased with Var(A)=4/n. Estimator B has "
            "Bias(B)=1/n and Var(B)=1/n. (1) Give MSE(A) and MSE(B). (2) For large "
            "n, which has smaller MSE? (3) Refuse: 'Unbiased always beats biased' "
            "and 'consistency means the estimator is unbiased.'"
        ),
        cp_kw=["bias", "MSE", "variance", "consistency", "efficiency", "unbiased", "refuse"],
        cp_model=(
            "(1) MSE(A)=4/n; MSE(B)=(1/n)² + 1/n = 1/n² + 1/n. (2) For large n, "
            "MSE(B)≈1/n < 4/n = MSE(A), so B is preferred on MSE. (3) Refuse: "
            "unbiasedness is not MSE optimality; consistency is large-sample "
            "concentration on the true value, not the same as unbiasedness."
        ),
        reflect="Harvest bias/MSE definition wobble. Keep comparison for tomorrow.",
    ),
    dict(
        day="CK-D4",
        stem="3.1.4-comparison-mse-cs1010",
        pid="CS1-EP001-PKG-3.1-COMPARISON-MSE",
        lo="3.1.4",
        slug="3.1-comparison-mse",
        keywords=["comparison", "MSE", "bias", "unbiased", "estimator"],
        title="Compare estimators using MSE and bias",
        purpose=(
            "Today's Mission exists to compare estimators using mean square error and bias "
            "or unbiasedness (so comparison is usable) without pretending asymptotic MLE "
            "laws (3.1.5) are finished."
        ),
        tutor=(
            "Today I will force the candidate to compare two estimators with MSE / bias "
            "warrants. And refuse treating property definitions alone as finishing comparison."
        ),
        edu=(
            "Produce a cognitive move from property definitions to an explicit estimator "
            "comparison under CMP language."
        ),
        lo_text=(
            "Comparison of estimators using their mean square error and bias or unbiasedness."
        ),
        focus="Two estimators → MSE / bias comparison → refuse asymptotics-as-done.",
        prior=(
            "Yesterday you discussed efficiency, bias, consistency and MSE (3.1.3). Today "
            "continues topic 3.1 at LO 3.1.4: comparison."
        ),
        why=(
            "3.1.4 is contiguous after property language. Closing it prevents a cliff at "
            "comparison while keeping asymptotic MLE as day five."
        ),
        benefit=(
            "You will be able to compare two estimators explicitly via MSE (and "
            "bias), not just recall the definitions."
        ),
        explain=(
            "Day 4 continues at the named learning objective. Comparison after property definitions."
        ),
        criteria=[
            "Closed-book, compare two estimators using MSE and/or bias.",
            "State when unbiasedness alone is insufficient.",
            "Refuse one 'definitions finished comparison' claim.",
        ],
        tasks=[
            "Sketch a two-estimator MSE/bias comparison before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.4.",
            "Closed-book Knowledge Checks: comparison + refuse asymptotics swallow.",
        ],
        next_code="3.1",
        next_title="Asymptotic distribution of MLEs (3.1.5)",
        cont=(
            "Today you compared estimators via MSE and bias; tomorrow continues 3.1 at the "
            "asymptotic distribution of MLEs."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.1.5. Titles only tonight",
        student=(
            "Tomorrow: asymptotic distribution of MLEs (3.1.5). Optional light prep: skim "
            "3.1.5 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.1.4 comparison of estimators using MSE and bias",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.4 "
            "(stop before asymptotic MLE 3.1.5)"
        ),
        oos=[
            "Asymptotic distribution of MLEs as primary (3.1.5)",
            "Bootstrap as primary (3.1.6)",
            "Confidence intervals (3.2)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating property definitions as finishing comparison.",
            "Watch for jumping into asymptotic Normal MLE laws as primary.",
            "Watch for CI width arguments as today's LO.",
        ],
        ar_prompt=(
            "Closed-book. (1) How do you compare two estimators using MSE? (2) When can an "
            "unbiased estimator lose to a biased one on MSE? (3) What claim must you refuse "
            "about asymptotics today?"
        ),
        ar_kw=["MSE", "bias", "unbiased", "compare", "variance", "estimator"],
        ar_model=(
            "Prefer the estimator with smaller MSE (CMP examples). A biased estimator can "
            "have smaller MSE than an unbiased one if variance reduction outweighs squared "
            "bias. Asymptotic MLE laws are tomorrow. Not today's LO."
        ),
        cp_prompt=(
            "Closed-book. Two estimators of θ: θ̂₁ is unbiased with Var=2/n; θ̂₂ has "
            "Bias=0.5/√n and Var=0.5/n. (1) Compare them using MSE. Which do you "
            "prefer for large n? (2) Refuse: 'Bias and MSE are defined, so "
            "comparison is automatic without computing either estimator's MSE.'"
        ),
        cp_kw=["MSE", "bias", "compare", "variance", "prefer", "refuse"],
        cp_model=(
            "(1) MSE₁=2/n; MSE₂=(0.5/√n)² + 0.5/n = 0.25/n + 0.5/n = 0.75/n. Prefer "
            "θ̂₂ on MSE (0.75/n < 2/n). (2) Refuse: comparison requires an explicit "
            "MSE (or bias) comparison of the named estimators. Definitions alone "
            "are not a comparison."
        ),
        reflect="Harvest comparison warrant wobble. Keep asymptotics for tomorrow.",
    ),
    dict(
        day="CK-D5",
        stem="3.1.5-asymptotic-mle-cs1010",
        pid="CS1-EP001-PKG-3.1-ASYMPTOTIC-MLE",
        lo="3.1.5",
        slug="3.1-asymptotic-mle",
        keywords=["asymptotic", "MLE", "distribution", "Normal", "large-sample"],
        title="Discuss the asymptotic distribution of MLEs",
        purpose=(
            "Today's Mission exists to discuss the asymptotic distribution of maximum "
            "likelihood estimators (so large-sample MLE behaviour is usable) without "
            "pretending bootstrap (3.1.6) is finished."
        ),
        tutor=(
            "Today I will force the candidate to state asymptotic Normal (or CMP-equivalent) "
            "behaviour of MLEs under regularity. And refuse treating finite-sample MSE "
            "comparison as finishing asymptotics."
        ),
        edu=(
            "Produce a cognitive move from finite-sample properties to asymptotic MLE "
            "distribution under CMP language."
        ),
        lo_text="Asymptotic distribution of maximum likelihood estimators.",
        focus="Large-sample MLE behaviour → asymptotic distribution → refuse bootstrap-as-done.",
        prior=(
            "Yesterday you compared estimators via MSE and bias (3.1.4). Today continues "
            "topic 3.1 at LO 3.1.5: asymptotic distribution of MLEs."
        ),
        why=(
            "3.1.5 is contiguous after comparison. Closing it prevents a cliff at asymptotic "
            "MLE while keeping bootstrap as day six."
        ),
        benefit=(
            "You will be able to state the asymptotic Normal claim for MLEs and use "
            "it for large-sample inference."
        ),
        explain=(
            "Day 5 continues at the named learning objective. Asymptotics after comparison."
        ),
        criteria=[
            "Closed-book, state the asymptotic distribution claim for MLEs (CMP form).",
            "Name at least one regularity / conditions cue.",
            "Refuse one 'bootstrap finished' claim.",
        ],
        tasks=[
            "Sketch asymptotic Normal MLE claim before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.5.",
            "Closed-book Knowledge Checks: asymptotics + refuse bootstrap swallow.",
        ],
        next_code="3.1",
        next_title="Bootstrap for estimator properties (3.1.6)",
        cont=(
            "Today you discussed asymptotic MLE behaviour; tomorrow continues 3.1 at "
            "bootstrap methods for estimator properties."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.1.6. Titles only tonight",
        student=(
            "Tomorrow: bootstrap for estimator properties (3.1.6). Optional light prep: skim "
            "3.1.6 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.1.5 asymptotic distribution of MLEs",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.5 "
            "(stop before bootstrap 3.1.6)"
        ),
        oos=[
            "Bootstrap as primary (3.1.6)",
            "Confidence intervals as primary (3.2)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating finite-sample MSE comparison as finishing asymptotics.",
            "Watch for jumping into bootstrap resampling as primary.",
            "Watch for CI construction as today's LO.",
        ],
        ar_prompt=(
            "Closed-book. (1) What asymptotic distribution claim does the CMP make for "
            "MLEs (in outline)? (2) What regularity / large-sample cue matters? (3) Why is "
            "bootstrap not today's LO?"
        ),
        ar_kw=[
            "asymptotic",
            "Normal",
            "MLE",
            "large",
            "sample",
            "variance",
            "regularity",
        ],
        ar_model=(
            "Under CMP regularity conditions, MLEs are asymptotically Normal with variance "
            "tied to information / large-sample results in the CMP. Bootstrap is a separate "
            "resampling LO (3.1.6)."
        ),
        cp_prompt=(
            "Closed-book. Under regularity conditions, an MLE θ̂ₙ satisfies √n (θ̂ₙ "
            "− θ) →ᵈ N(0, 1/I(θ)). (1) What does this asymptotic Normal claim give "
            "you for large-sample inference about θ? (2) Refuse: 'I'll bootstrap the "
            "sampling distribution, so I do not need the asymptotic MLE result.'"
        ),
        cp_kw=["asymptotic", "Normal", "MLE", "Fisher", "information", "large-sample", "bootstrap", "refuse"],
        cp_model=(
            "(1) For large n, θ̂ₙ is approximately Normal about θ with variance ≈ "
            "1/(n I(θ)), supporting large-sample SEs and Wald-type intervals/tests "
            "from Fisher information. (2) Refuse: bootstrap estimates properties by "
            "resampling; it does not replace stating the asymptotic distribution of "
            "the MLE."
        ),
        reflect="Harvest asymptotic variance / regularity wobble. Keep bootstrap for tomorrow.",
    ),
    dict(
        day="CK-D6",
        stem="3.1.6-bootstrap-estimator-cs1010",
        pid="CS1-EP001-PKG-3.1-BOOTSTRAP-ESTIMATOR",
        lo="3.1.6",
        slug="3.1-bootstrap-estimator",
        keywords=["bootstrap", "resample", "estimator", "properties", "sampling"],
        title="Use bootstrap to estimate properties of an estimator",
        purpose=(
            "Today's Mission exists to use the bootstrap method for estimating properties of "
            "an estimator (so resampling is usable) without pretending intervals (3.2) or "
            "Chapter 3 complete are finished."
        ),
        tutor=(
            "Today I will force the candidate to describe bootstrap resampling for estimator "
            "properties. And refuse treating asymptotic MLE laws as finishing bootstrap, and "
            "refuse Chapter 3 trophy claims."
        ),
        edu=(
            "Produce a cognitive move from an estimator to bootstrap estimation of its "
            "properties under CMP language."
        ),
        lo_text="Bootstrap method for estimating properties of an estimator.",
        focus=(
            "Resample → estimate estimator properties → refuse "
            "asymptotics-as-bootstrap / bootstrap-CI-as-same."
        ),
        prior=(
            "Yesterday you discussed asymptotic MLE behaviour (3.1.5). Today continues topic "
            "3.1 at LO 3.1.6 (bootstrap) completing the Learning span."
        ),
        why=(
            "3.1.6 completes topic 3.1 Learning. Closing it prevents a cliff before Revision "
            "while keeping intervals (3.2) as a later Volume."
        ),
        benefit=(
            "You will be able to use bootstrap resampling to estimate a property of "
            "an estimator (such as its standard error)."
        ),
        explain=(
            "Day 6 closes this stretch at the named learning objective. 3.1 Learning at bootstrap before Revision."
        ),
        criteria=[
            "Closed-book, describe the bootstrap move for estimating estimator properties.",
            "Name what is being estimated (e.g. SE / bias / sampling behaviour as CMP).",
            "Refuse Chapter 3 complete and 3.2-as-done claims.",
        ],
        tasks=[
            "Sketch resample → property estimate before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.1.6.",
            "Closed-book Knowledge Checks: bootstrap + refuse Ch3 / 3.2 swallow.",
        ],
        next_code="CK-R1",
        next_title="Campaign Kappa revision: retrieve 3.1 hinges",
        cont=(
            "Today you used bootstrap for estimator properties; tomorrow is Revision. "
            "retrieve 3.1.1–3.1.6 closed-book (not first-pass 3.2)."
        ),
        prep="Optional: list the six 3.1 LO titles from memory. No new reading tonight",
        student=(
            "Tomorrow: Revision (CK-R1): retrieve estimator hinges. Optional: list 3.1.1–"
            "3.1.6 titles from memory tonight."
        ),
        open="CMP · Syllabus 3.1.6 bootstrap for estimator properties",
        stop=(
            "Through the CMP treatment of Syllabus 3.1.6 "
            "(stop before confidence / prediction intervals 3.2)"
        ),
        oos=[
            "Confidence and prediction intervals as primary (3.2)",
            "Hypothesis testing primary (3.3)",
            "Chapter 3 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating asymptotic MLE as finishing bootstrap.",
            "Watch for claiming Chapter 3 / 3.2 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the bootstrap move for estimating properties of an "
            "estimator? (2) What property might you estimate (CMP examples)? (3) What must "
            "you refuse about Chapter 3 / 3.2 today?"
        ),
        ar_kw=[
            "bootstrap",
            "resample",
            "estimator",
            "standard",
            "error",
            "bias",
            "property",
        ],
        ar_model=(
            "Bootstrap resamples from the observed sample (CMP procedure) to approximate "
            "sampling behaviour of an estimator. E.g. SE or bias. Completing 3.1.6 closes "
            "topic 3.1 Learning, not Chapter 3 or intervals."
        ),
        cp_prompt=(
            "Closed-book. You have an estimator θ̂ computed from a sample of size n. "
            "(1) Describe the bootstrap move to estimate the standard error of θ̂. "
            "(2) Refuse: 'The asymptotic Normal law for the MLE already finished "
            "bootstrap estimation of estimator properties' and 'a bootstrap "
            "confidence interval is the same LO.'"
        ),
        cp_kw=["bootstrap", "resample", "standard error", "properties", "refuse", "asymptotic", "confidence"],
        cp_model=(
            "(1) Draw resamples with replacement from the original sample, recompute "
            "θ̂* on each resample, and use the empirical SD (or other summary) of "
            "the θ̂* values as the SE estimate. (2) Refuse: asymptotics ≠ bootstrap "
            "resampling for properties; constructing a bootstrap CI is a different "
            "LO (interval construction, not property estimation)."
        ),
        reflect=(
            "Harvest bootstrap procedure wobble. Revision protects the 3.1 chain tomorrow."
        ),
    ),
]


def main() -> None:
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    inventory: list[str] = []
    span: list[str] = []

    for d in LEARNING:
        pkg = apply_mcq_overlay(learning_pkg(d), d["stem"])
        path = PKG_DIR / f"{d['stem']}.json"
        path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n")
        inventory.append(d["pid"])
        span.append(d["lo"])

    rev = apply_batch6b_mcq_overlay(revision_pkg(), "revision-estimators-cs1010")
    (PKG_DIR / "revision-estimators-cs1010.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-KAPPA",
        "campaign_version": "cs1010-1.0.0",
        "display_title": "Campaign Kappa: Estimators and their properties (3.1)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-010",
        "prior_volume_id": "CS1-009",
        "day_count": {"learning": 6, "revision": 1, "total": 7},
        "syllabus_span": span,
        "out_of_scope": [
            "3.2+",
            "Chapter 3 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 9 / remainder / spine re-audit authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()
