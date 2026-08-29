#!/usr/bin/env python3
"""Generate CS1-014 / Campaign Xi educational packages (catalogue only).

Continuity Front join Pilot Arc for Topic 4.2 (generalised linear models).
Topic 4.2 is already Published+LIVE via Trust Front CS1-003/Delta — Xi uses
distinct package IDs and must not be copied to educational_packages/ in this cycle.
Published Coverage and Student Reliance are unchanged by catalogue authoring.
"""
from __future__ import annotations

import json
from pathlib import Path

from _mcq_batch2_continuity_front_payload import apply_mcq_overlay
from _mcq_batch6b_revision_payload import apply_mcq_overlay as apply_batch6b_mcq_overlay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-xi-cs1014"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1014-campaign-xi-1.0.0",
    "publication_version": "cs1014-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-XI",
    "volume_id": "CS1-014",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1014_EDUCATIONAL_VOLUME.md",
        "CS1014_CERTIFICATION_REPORT.md",
        "EP012_WAVE12_PLAN.md",
    ],
    "author_id": "cs1014-educational-author",
    "authored_at": "2026-08-03",
}

TOPIC = {
    "topic_code": "4.2",
    "topic_title": "Understand and use generalised linear models",
    "topic_id": "CS1-D-T02",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "4.2", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1014-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1014-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1014-cs1-{d['slug']}",
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
                f"for later 4.2 LOs, Trust Front absorb of 5.1, first-pass spine PASS, or "
                "until-exam trust."
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
            "worked_examples_cue": (
                "Worked-example re-entry (CMP closed): attempt the hinge step before uncovering "
                f"the solution: stay inside {lo}."
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
                "episode_id": f"lep-cs1014-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1014-{lo}-ar-01",
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
                "episode_id": f"lep-cs1014-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1014-{lo}-cp-01",
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
        "revision_linkage": {
            "returns_on": "CX-R1",
            "campaign_revision_package": "CS1-EP001-PKG-REV-GLM-XI",
            "note": f"Syllabus {lo} is a CX-R1 return target after Learning span closes.",
        },
    }


def revision_pkg() -> dict:
    day = "CX-R1"
    pid = "CS1-EP001-PKG-REV-GLM-XI"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Xi revision: generalised linear models",
        "return_targets": [
            "4.2.1",
            "4.2.2",
            "4.2.3",
            "4.2.4",
            "4.2.5",
            "4.2.6",
            "4.2.7",
            "4.2.8",
            "4.2.9",
            "4.2.10",
        ],
        "topic_aliases": [day, "campaign-xi-revision"],
        "topic_title_keywords": [
            "revision",
            "GLM",
            "exponential family",
            "link",
            "deviance",
            "residuals",
            "likelihood-ratio",
        ],
        "golden_id": "GOLDEN-CS1014-CS1-CX-R1-GLM",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1014-cs1-cx-r1-glm",
            "display_title": "Retrieve GLM hinges (4.2)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Xi. Retrieving "
                "exponential-family placement through fit/interpret. So 4.2 does not evaporate "
                "before an honest stop / Wave 0 honesty / spine re-audit / Topic 5.1 successor."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Xi's Learning hinges. "
                "not a passive CMP re-read and not a Trust Front 5.1 absorb or until-exam claim."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: family → "
                "mean/variance → link → factors → linear predictor → deviance → model choice → "
                "residuals → acceptability tests → fit/interpret."
            ),
            "learning_objective": (
                "Retrieve and connect (1) exponential-family responses, (2) mean/variance/"
                "variance function/scale, (3) link and canonical link, (4) variables/factors/"
                "interactions, (5) linear predictor forms, (6) deviance and estimation, "
                "(7) analysis-of-deviance model choice, (8) Pearson and deviance residuals, "
                "(9) χ² and LRT acceptability, and (10) fit and interpret a GLM."
            ),
            "concept_focus": (
                "Campaign chain retrieval: family → moments → link → factors → η → deviance → "
                "choice → residuals → tests → fit/interpret."
            ),
            "prior_bridge": (
                "Yesterday you finished fit and interpret (4.2.10). Today is Revision mode: "
                "return to 4.2.1–4.2.10 under closed-book retrieval. No new first-pass LO."
            ),
            "why_now": (
                "You've just finished classical GLM; spaced retrieval now protects that chain "
                "before Bayesian work."
            ),
            "expected_benefit": (
                "You'll confirm the GLM chain still retrieves. Family through fit and interpret."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the ten 4.2 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse treating GLM revision as Bayesian Topic 5.1 finished.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Xi's chain from family placement to fit/"
                "interpret.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 50, "max": 75},
        },
        "session": {
            "session_id": "ssn-cs1014-cs1-cx-r1-glm",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Xi skills. Not to claim Trust Front absorb."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 50, "max": 75},
            "wrap_up": (
                "Revision Session complete. You stress-tested 4.2.1–4.2.10 return targets. "
                "This is revision Study Progress. Not Topic Complete for 5.1, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that GLM hinges will still retrieve in three days? "
                "Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Xi "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the ten 4.2 Learning hinges in order?",
                "Can you state family → link → η → deviance → residuals → tests → fit?",
                "What claim must you refuse (5.1 absorb / spine / until-exam)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Trust Front 5.1 / spine / until-exam complete.",
                "Watch for dropping Nu linear-regression memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not claim Trust Front absorb, "
                "spine PASS, or until-exam trust in this sitting"
            ),
            "out_of_scope_today": [
                "Bayesian / Topic 5.1 as primary",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Wave 0 Approver honesty clearance",
                "Certified Educational Coverage increase from catalogue alone",
            ],
            "annotation_task": "Before checks: sketch return-target chain from memory",
            "attempt_before_reveal": "Attempt each check before any targeted CMP reopen",
            "worked_examples_cue": (
                "Revision worked re-entry: attempt the failed hinge closed-book before "
                "targeted CMP reopen."
            ),
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
                "episode_id": "lep-cs1014-cx-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1014-cx-r1-ar-01",
                "title": "Active Recall: Xi chain",
                "prompt": (
                    "Closed-book. List the ten 4.2 Learning hinges in order as short phrases "
                    "(family → … → fit/interpret)."
                ),
                "response_type": "short_structured",
                "body": "Retrieve Campaign Xi Learning span.",
                "hints": ["Start from exponential family.", "End at fit and interpret."],
                "accepted_keywords": [
                    "family",
                    "mean",
                    "link",
                    "factor",
                    "predictor",
                    "deviance",
                    "choice",
                    "residual",
                    "chi-square",
                    "fit",
                ],
                "explanation": "Order retrieval for CX-R1.",
                "model_answer": (
                    "Family → mean/variance/scale → link/canonical → factors/interactions → "
                    "linear predictor → deviance/estimation → model choice → residuals → "
                    "acceptability tests → fit/interpret."
                ),
                "common_mistake": "Skipping mid-chain deviance/choice or collapsing into LM.",
                "success_criteria": ["Ten hinges named in lawful order."],
            },
            {
                "episode_id": "lep-cs1014-cx-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1014-cx-r1-cp-01",
                "title": "Checkpoint: refuse 5.1 / spine",
                "prompt": (
                    "Closed-book. A colleague says 'GLM revision finished Bayesian modelling "
                    "and the exam journey.' Refuse; name the weakest GLM link on today's "
                    "retrieval chain; name one concrete next rework (not a new topic)."
                ),
                "response_type": "short_structured",
                "body": "Refuse forbidden claims; harvest weakest link.",
                "hints": ["Refuse 5.1 absorb / spine / until-exam.", "Name one rework."],
                "accepted_keywords": [
                    "refuse",
                    "5.1",
                    "spine",
                    "Wave 0",
                    "weakest",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) Name weakest hinge + five-minute rework. (2) Refuse 5.1 absorb / "
                    "spine / until-exam. (3) Honest next is declared stop or Wave 0 honesty / "
                    "spine re-audit / Topic 5.1 successor Volume. Not claimed finished here."
                ),
                "common_mistake": "Spine / Trust Front absorb / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which GLM link retrieved least cleanly today and what one concrete rework will "
                "you schedule? Do not claim Bayesian Topic 5.1 is finished because GLM "
                "revision went well."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Confirm: 5.1 absorb / spine PASS / until-exam trust were out of scope.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "stop",
            "next_topic_title": (
                "Honest next: declared stop / Wave 0 honesty / spine re-audit / Topic 5.1 "
                "successor. Not Trust Front 5.1 absorb"
            ),
            "continuity_line": (
                "Campaign Xi / Volume CS1-014 completes after this Revision. Honest stop: "
                "4.2 Continuity Front join Pilot Arc closed. Not Trust Front 5.1 absorb; "
                "not first-pass spine; not until-exam trust. Successor geography is Wave 0 "
                "honesty / spine re-audit / Topic 5.1 under a later commission (or declared "
                "stop). CS1-003 Delta remains independent Trust Front LIVE inventory."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Xi / CS1-014 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await Wave 0 honesty / spine re-audit / Topic 5.1 "
                "successor Volume. Optional: schedule your weakest 4.2 rework only."
            ),
        },
        "revision_linkage": {
            "returns_on": "CX-R1",
            "return_targets": [
                "4.2.1",
                "4.2.2",
                "4.2.3",
                "4.2.4",
                "4.2.5",
                "4.2.6",
                "4.2.7",
                "4.2.8",
                "4.2.9",
                "4.2.10",
            ],
            "protect_prior_hinge": "Nu 4.1 as needed",
        },
    }


LEARNING = [
    dict(
        day="CX-D1",
        stem="4.2.1-exponential-family-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-EXPONENTIAL-FAMILY",
        lo="4.2.1",
        slug="4.2-exponential-family",
        keywords=["exponential", "family", "binomial", "Poisson", "gamma", "GLM"],
        title="Place GLM responses in the exponential family",
        purpose=(
            "Today's Mission exists to place binomial, Poisson, exponential, gamma and "
            "normal as exponential-family responses. So GLM starts from distributional "
            "honesty, without pretending mean/variance/scale (4.2.2) are finished."
        ),
        tutor=(
            "Today I will force exponential-family placement for named responses and refuse "
            "'GLM means linear regression in a package'."
        ),
        edu=(
            "Produce family placement as the Continuity Front join hinge from Nu linear "
            "regression into Topic 4.2 structure."
        ),
        lo_text=(
            "Recognise binomial, Poisson, exponential, gamma and normal distributions as "
            "members of an exponential family in the GLM setting."
        ),
        focus=(
            "Named response distributions → exponential-family membership in the "
            "GLM setting → refuse package-name GLM."
        ),
        prior=(
            "Campaign Nu closed linear regression (4.1) with Revision. Today opens Continuity "
            "Front join at Topic 4.2 LO 4.2.1. The next official syllabus topic after 4.1. "
            "Trust Front CS1-003 already holds LIVE 4.2 inventory independently; Xi is the "
            "Continuity Front native Pilot Arc."
        ),
        why=(
            "4.2.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at GLM structure, keeping moments for the following session."
        ),
        benefit=(
            "You will be able to recognise binomial, Poisson, exponential, gamma "
            "and Normal as exponential-family GLM responses."
        ),
        explain=(
            "Day 1 opens GLM by placing exponential-family responses. "
            "the natural next step after classical linear models."
        ),
        criteria=[
            "Closed-book, name five exponential-family GLM responses from 4.2.1.",
            "Mark which is the Normal special case inside the list.",
            "Refuse one 'GLM is just linear regression with a package name' claim.",
        ],
        tasks=[
            "Sketch family membership before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.1.",
            "Closed-book Knowledge Checks: family list + refuse package-name GLM.",
        ],
        next_code="4.2",
        next_title="Mean, variance, variance function and scale (4.2.2)",
        cont=(
            "Today you placed GLM responses in the exponential family; tomorrow continues "
            "4.2 at mean, variance, variance function and scale."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.2. Titles only tonight",
        student=(
            "Tomorrow: mean, variance, variance function and scale (4.2.2). Optional light "
            "prep: skim 4.2.2 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.1 exponential family responses for GLMs",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.1 "
            "(stop before mean/variance/scale 4.2.2)"
        ),
        oos=[
            "Mean / variance / variance function / scale as primary (4.2.2)",
            "Link / canonical link as primary (4.2.3)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating GLM with 'linear regression in software'.",
            "Watch for diving into mean/variance formulae (4.2.2) as today's finish.",
            "Watch for claiming Trust Front 5.1 absorb or spine PASS.",
        ],
        ar_prompt=(
            "Closed-book. (1) List five distributions named in 4.2.1 as exponential-family "
            "GLM responses. (2) Mark which is the Normal special case. (3) Name one reason "
            "mean/variance is not today's LO."
        ),
        ar_kw=["binomial", "Poisson", "exponential", "gamma", "normal", "family"],
        ar_model=(
            "Binomial, Poisson, exponential, gamma, normal. Normal is the special case "
            "inside the family list, not the definition of GLM. Mean/variance is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. (1) Name three of binomial, Poisson, exponential, "
            "gamma, Normal and state in one line why each belongs in the "
            "exponential family for GLM. (2) Refuse: 'GLM is just ordinary linear "
            "regression with a different software package name.'"
        ),
        cp_kw=["exponential family", "Poisson", "binomial", "Normal", "refuse", "package"],
        cp_model=(
            "(1) e.g. Poisson (counts with E[Y]=Var[Y]=μ); binomial (bounded "
            "proportion/count responses); Normal (continuous responses with "
            "constant variance): each has an exponential-family density form "
            "usable as a GLM response. (2) Refuse: package name ≠ GLM; a GLM "
            "response sits in an exponential family (with later η and link). "
            "Normal+identity is a special case, not the definition."
        ),
        reflect="Harvest family-placement wobble. Keep mean/variance out of tonight's claim.",
    ),
    dict(
        day="CX-D2",
        stem="4.2.2-mean-variance-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-MEAN-VARIANCE",
        lo="4.2.2",
        slug="4.2-mean-variance",
        keywords=["mean", "variance", "variance function", "scale", "GLM"],
        title="Evaluate mean, variance, variance function and scale",
        purpose=(
            "Today's Mission exists to state and evaluate mean, variance, variance function "
            "and scale for GLM binomial, Poisson, exponential, gamma and normal. Without "
            "pretending link/canonical link (4.2.3) are finished."
        ),
        tutor=(
            "Today I will force mean/variance/variance-function/scale statements per family "
            "and refuse treating link choice as today's LO."
        ),
        edu=(
            "Produce a cognitive move from family membership to lawful moment and scale "
            "structure under CMP."
        ),
        lo_text=(
            "State and evaluate mean, variance, variance function and scale parameter for "
            "GLM binomial, Poisson, exponential, gamma and normal distributions."
        ),
        focus="Family → E(Y) → Var(Y) → variance function V(μ) → scale parameter.",
        prior=(
            "Yesterday you placed responses in the exponential family (4.2.1). Today "
            "continues Topic 4.2 at moments and scale. Still Continuity Front join."
        ),
        why=(
            "4.2.2 is contiguous after family placement. Without moments/scale, link and "
            "deviance lack distributional warrant."
        ),
        benefit=(
            "You will be able to state mean, variance, variance function and "
            "scale for the standard GLM families."
        ),
        explain=(
            "Day 2 focuses the named learning objective. Link functions as tomorrow."
        ),
        criteria=[
            "Closed-book, for one named family state mean and variance (or variance function).",
            "State what the scale parameter does in that setting.",
            "Refuse one 'I chose the link, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch mean/variance/scale chain before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.2.",
            "Closed-book Knowledge Checks: moments + refuse link swallow.",
        ],
        next_code="4.2",
        next_title="Link function and canonical link (4.2.3)",
        cont=(
            "Today you established mean/variance/scale for GLM families; tomorrow continues "
            "4.2 at link and canonical link."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.3. Titles only tonight",
        student=(
            "Tomorrow: link and canonical link (4.2.3). Optional light prep: skim 4.2.3 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.2 mean, variance, variance function and scale",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.2 "
            "(stop before link / canonical link 4.2.3)"
        ),
        oos=[
            "Link / canonical link as primary (4.2.3)",
            "Factors / interactions as primary (4.2.4)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for collapsing variance function into OLS residual variance myth.",
            "Watch for jumping to link choice (4.2.3) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What four quantities does 4.2.2 ask you to handle? (2) Pick "
            "one family and state its mean and variance (or variance function). (3) Name one "
            "reason link/canonical is not today's LO."
        ),
        ar_kw=["mean", "variance", "variance function", "scale", "Poisson", "binomial"],
        ar_model=(
            "Mean, variance, variance function, and scale. Example: Poisson mean=λ, "
            "variance=λ (scale often 1). Link/canonical is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. For Poisson and Normal GLM responses: (1) state E[Y], "
            "Var[Y], and the variance function V(μ) for each. (2) Refuse: "
            "'Choosing the logit link finishes stating mean, variance, variance "
            "function and scale.'"
        ),
        cp_kw=["Poisson", "Normal", "variance function", "scale", "refuse", "link"],
        cp_model=(
            "(1) Poisson: E[Y]=μ, Var[Y]=μ, V(μ)=μ (scale typically 1). Normal: "
            "E[Y]=μ, Var[Y]=σ², V(μ)=1 with scale σ². (2) Refuse: the link maps μ "
            "to η; today requires the mean/variance/scale structure of the "
            "response family."
        ),
        reflect="Harvest moments/scale wobble. Keep link choice out of tonight's claim.",
    ),
    dict(
        day="CX-D3",
        stem="4.2.3-link-canonical-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-LINK-CANONICAL",
        lo="4.2.3",
        slug="4.2-link-canonical",
        keywords=["link", "canonical", "logit", "log", "identity", "GLM"],
        title="Choose link and canonical link with warrant",
        purpose=(
            "Today's Mission exists to explain the link function and the canonical link "
            "for the distributions in 4.2.1. Without pretending factors/interactions "
            "(4.2.4) are finished."
        ),
        tutor=(
            "Today I will force link vs canonical-link discrimination and refuse treating "
            "factor coding as today's LO."
        ),
        edu=(
            "Produce a cognitive move from moments/scale to lawful link and canonical link "
            "under CMP."
        ),
        lo_text=(
            "Explain the link function and the canonical link function for the distributions "
            "in 4.2.1."
        ),
        focus=(
            "g(μ)=η → link role → canonical link as natural-parameter pairing per "
            "family."
        ),
        prior=(
            "Yesterday you evaluated mean/variance/scale (4.2.2). Today continues Topic 4.2 "
            "at link functions."
        ),
        why=(
            "4.2.3 is contiguous after moments. Without link, the linear predictor has no "
            "mean map."
        ),
        benefit=(
            "You will be able to explain the link and canonical link for GLM "
            "families and refuse software-default myths."
        ),
        explain=(
            "Day 3 focuses the named learning objective. Factors/ interactions as tomorrow."
        ),
        criteria=[
            "Closed-book, state what a link function maps.",
            "Name the canonical link for at least two families from 4.2.1.",
            "Refuse one 'I coded factors, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch link vs canonical before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.3.",
            "Closed-book Knowledge Checks: link + refuse factors swallow.",
        ],
        next_code="4.2",
        next_title="Variables, factors and interactions (4.2.4)",
        cont=(
            "Today you established link and canonical link; tomorrow continues 4.2 at "
            "variables, factors and interactions."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.4. Titles only tonight",
        student=(
            "Tomorrow: variables, factors and interactions (4.2.4). Optional light prep: "
            "skim 4.2.4 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.3 link function and canonical link",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.3 "
            "(stop before factors / interactions 4.2.4)"
        ),
        oos=[
            "Factors / interactions as primary (4.2.4)",
            "Linear predictor writing as primary (4.2.5)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating any convenient link as automatically canonical.",
            "Watch for diving into factor/interaction coding (4.2.4) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does a link function connect? (2) What is a canonical "
            "link? (3) Name canonical links for binomial and Poisson. (4) Name one reason "
            "factors are not today's LO."
        ),
        ar_kw=["link", "canonical", "logit", "log", "mean", "eta"],
        ar_model=(
            "Link maps mean to linear predictor. Canonical is the natural family link "
            "(e.g. logit for binomial; log for Poisson). Factors/interactions are tomorrow."
        ),
        cp_prompt=(
            "Closed-book. (1) For binomial and gamma responses, name the "
            "canonical link and justify each from the mean's natural range. (2) "
            "Refuse: 'Whatever link the software defaults to is automatically the "
            "canonical link.'"
        ),
        cp_kw=["logit", "binomial", "gamma", "canonical", "refuse", "default"],
        cp_model=(
            "(1) Binomial: logit: μ ∈ (0,1) and logit maps to ℝ for η. Gamma: "
            "reciprocal (negative-reciprocal canonical form as in CMP). Μ > 0, "
            "mapping the positive mean onto the η scale for the gamma "
            "exponential-family form. (2) Refuse: a software default needs a "
            "warrant; canonical means the link that equates η with the natural "
            "parameter, not whatever the GUI chose."
        ),
        reflect="Harvest link/canonical wobble. Keep factors out of tonight's claim.",
    ),
    dict(
        day="CX-D4",
        stem="4.2.4-factors-interactions-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-FACTORS-INTERACTIONS",
        lo="4.2.4",
        slug="4.2-factors-interactions",
        keywords=["factor", "categorical", "interaction", "variable", "GLM"],
        title="Use variables, factors and interactions in GLMs",
        purpose=(
            "Today's Mission exists to explain variables, factors taking categorical values, "
            "and interaction terms in the GLM setting. Without pretending linear-predictor "
            "writing (4.2.5) is finished."
        ),
        tutor=(
            "Today I will force variable/factor/interaction discrimination and refuse "
            "treating η-form writing as today's LO."
        ),
        edu=(
            "Produce a cognitive move from link to lawful GLM covariate structure under CMP."
        ),
        lo_text=(
            "Explain variables, factors taking categorical values, and interaction terms in "
            "the GLM setting."
        ),
        focus=(
            "Continuous variable → categorical factor coding → interaction term "
            "changing a slope by level."
        ),
        prior=(
            "Yesterday you explained link and canonical link (4.2.3). Today continues Topic "
            "4.2 at variables, factors and interactions."
        ),
        why=(
            "4.2.4 is contiguous after link. Without factors/interactions, η forms lack "
            "actuarial covariate honesty."
        ),
        benefit=(
            "You will be able to explain variables, factors and interaction terms "
            "in a GLM linear predictor."
        ),
        explain=(
            "Day 4 focuses the named learning objective. Linear predictor forms as tomorrow."
        ),
        criteria=[
            "Closed-book, distinguish a continuous variable from a categorical factor.",
            "State what an interaction term allows.",
            "Refuse one 'I wrote η, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch variable/factor/interaction before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.4.",
            "Closed-book Knowledge Checks: factors + refuse η swallow.",
        ],
        next_code="4.2",
        next_title="Linear predictor forms (4.2.5)",
        cont=(
            "Today you established variables, factors and interactions; tomorrow continues "
            "4.2 at linear predictor forms."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.5. Titles only tonight",
        student=(
            "Tomorrow: linear predictor forms (4.2.5). Optional light prep: skim 4.2.5 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.4 variables, factors and interactions",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.4 "
            "(stop before linear predictor forms 4.2.5)"
        ),
        oos=[
            "Linear predictor writing as primary (4.2.5)",
            "Deviance / estimation as primary (4.2.6)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating every covariate as a continuous variable.",
            "Watch for jumping to full η polynomial forms (4.2.5) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a factor in the GLM setting? (2) What does an "
            "interaction term capture? (3) Name one reason writing the full linear "
            "predictor is not today's LO."
        ),
        ar_kw=["factor", "categorical", "interaction", "variable", "levels"],
        ar_model=(
            "A factor takes categorical levels; an interaction allows joint level effects "
            "beyond main effects. Full η-form writing is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. Rating: continuous age x and factor region (levels "
            "North/South). (1) Write a linear predictor that includes region as a "
            "factor (baseline North) and an age×region interaction. (2) Refuse: "
            "'Writing η = β₀ + β₁x with no factors finishes explaining factors "
            "and interactions' and 'an interaction is just another main-effect "
            "slope.'"
        ),
        cp_kw=["factor", "interaction", "I_South", "η", "refuse", "main effect"],
        cp_model=(
            "(1) η = β₀ + β₁x + β₂ I_South + β₃ x·I_South (North baseline). (2) "
            "Refuse: factors encode categorical levels; an interaction changes "
            "the age slope by region. It is not merely another additive main "
            "effect."
        ),
        reflect="Harvest factor/interaction wobble. Keep η-form writing out of tonight's claim.",
    ),
    dict(
        day="CX-D5",
        stem="4.2.5-linear-predictor-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-LINEAR-PREDICTOR",
        lo="4.2.5",
        slug="4.2-linear-predictor",
        keywords=["linear predictor", "eta", "polynomial", "factor", "GLM"],
        title="Write the linear predictor for simple GLM forms",
        purpose=(
            "Today's Mission exists to define the linear predictor and write its form for "
            "simple models, including polynomial models and models involving factors. "
            "without pretending deviance/estimation (4.2.6) are finished."
        ),
        tutor=(
            "Today I will force η-form writing for simple GLM structures and refuse treating "
            "deviance as today's LO."
        ),
        edu=(
            "Produce a cognitive move from covariate structure to lawful linear predictor "
            "forms under CMP."
        ),
        lo_text=(
            "Define the linear predictor and write its form for simple models, including "
            "polynomial models and models involving factors."
        ),
        focus=(
            "η = Xβ definition → polynomial and factor forms → refuse conflating "
            "η with the link function."
        ),
        prior=(
            "Yesterday you explained variables, factors and interactions (4.2.4). Today "
            "writes the linear predictor forms."
        ),
        why=(
            "4.2.5 is contiguous after factors. Without η forms, deviance and software fit "
            "lack structure."
        ),
        benefit=(
            "You will be able to define the linear predictor and write its form "
            "for polynomial and factor models."
        ),
        explain=(
            "Day 5 focuses the named learning objective. Deviance/ estimation as tomorrow."
        ),
        criteria=[
            "Closed-book, define the linear predictor η.",
            "Write or state one simple form and one form involving a factor or polynomial.",
            "Refuse one 'I computed deviance, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch η forms before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.5.",
            "Closed-book Knowledge Checks: η forms + refuse deviance swallow.",
        ],
        next_code="4.2",
        next_title="Deviance and GLM parameter estimation (4.2.6)",
        cont=(
            "Today you established linear predictor forms; tomorrow continues 4.2 at "
            "deviance and estimation."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.6. Titles only tonight",
        student=(
            "Tomorrow: deviance and GLM parameter estimation (4.2.6). Optional light prep: "
            "skim 4.2.6 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.5 linear predictor forms",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.5 "
            "(stop before deviance / estimation 4.2.6)"
        ),
        oos=[
            "Deviance / scaled deviance / estimation as primary (4.2.6)",
            "Analysis of deviance model choice as primary (4.2.7)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating η with μ without the link.",
            "Watch for jumping into deviance calculation (4.2.6) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) Define the linear predictor. (2) Give one simple η form. "
            "(3) Give one form involving a factor or polynomial term. (4) Name one reason "
            "deviance is not today's LO."
        ),
        ar_kw=["eta", "linear predictor", "beta", "polynomial", "factor"],
        ar_model=(
            "η is the linear predictor (typically Xβ). Example: η=β0+β1x; or with factor "
            "indicators / polynomial powers. Deviance/estimation is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. Poisson claim counts with log link, continuous exposure "
            "score x and two-level factor cover (Standard/Plus). (1) Write η for "
            "a model with x, a quadratic term in x, and cover. (2) Refuse: 'The "
            "link function is the linear predictor.'"
        ),
        cp_kw=["η", "quadratic", "factor", "link", "refuse", "linear predictor"],
        cp_model=(
            "(1) η = β₀ + β₁x + β₂x² + β₃ I_Plus (Standard baseline). (2) Refuse: "
            "η = Xβ is the linear predictor; the link g maps mean μ to η (e.g. "
            "log(μ)=η for Poisson log)."
        ),
        reflect="Harvest η-form wobble. Keep deviance out of tonight's claim.",
    ),
    dict(
        day="CX-D6",
        stem="4.2.6-deviance-estimation-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-DEVIANCE-ESTIMATION",
        lo="4.2.6",
        slug="4.2-deviance-estimation",
        keywords=["deviance", "scaled deviance", "estimation", "MLE", "GLM"],
        title="Use deviance and estimate GLM parameters",
        purpose=(
            "Today's Mission exists to explain deviance, scaled deviance, and estimation of "
            "GLM parameters. Without pretending analysis-of-deviance model choice (4.2.7) "
            "is finished."
        ),
        tutor=(
            "Today I will force deviance vs scaled deviance and estimation hinges and refuse "
            "treating model-choice theatre as today's LO."
        ),
        edu=(
            "Produce a cognitive move from η forms to lawful deviance and parameter "
            "estimation under CMP."
        ),
        lo_text=(
            "Explain deviance, scaled deviance, and estimation of the parameters of a "
            "generalised linear model."
        ),
        focus=(
            "Log-likelihood → deviance → scaled deviance → maximum-likelihood / "
            "IWLS parameter estimates."
        ),
        prior=(
            "Yesterday you wrote linear predictor forms (4.2.5). Today continues Topic 4.2 "
            "at deviance and estimation."
        ),
        why=(
            "4.2.6 is contiguous after η. Without deviance/estimation, model choice and "
            "diagnostics lack a criterion."
        ),
        benefit=(
            "You will be able to explain deviance, scaled deviance, and how GLM "
            "parameters are estimated."
        ),
        explain=(
            "Day 6 focuses the named learning objective. Analysis of deviance model choice as tomorrow."
        ),
        criteria=[
            "Closed-book, state what deviance compares.",
            "Distinguish deviance from scaled deviance in one sentence.",
            "Refuse one 'I picked the best model by p-hacking, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch deviance/estimation before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.6.",
            "Closed-book Knowledge Checks: deviance + refuse model-choice swallow.",
        ],
        next_code="4.2",
        next_title="Model choice via analysis of deviance (4.2.7)",
        cont=(
            "Today you established deviance and estimation; tomorrow continues 4.2 at "
            "analysis-of-deviance model choice."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.7. Titles only tonight",
        student=(
            "Tomorrow: model choice via analysis of deviance (4.2.7). Optional light prep: "
            "skim 4.2.7 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.6 deviance, scaled deviance and estimation",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.6 "
            "(stop before analysis-of-deviance model choice 4.2.7)"
        ),
        oos=[
            "Analysis of deviance model choice as primary (4.2.7)",
            "Pearson / deviance residuals as primary (4.2.8)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating deviance with OLS residual sum of squares without warrant.",
            "Watch for jumping into nested model-choice theatre (4.2.7) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is deviance in a GLM? (2) What does scaled deviance "
            "involve? (3) What is being estimated? (4) Name one reason model choice is not "
            "today's LO."
        ),
        ar_kw=["deviance", "scaled", "likelihood", "estimate", "parameters"],
        ar_model=(
            "Deviance compares fitted vs saturated likelihoods; scaled deviance divides by "
            "scale. Parameters of the GLM are estimated. Nested model choice is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. (1) In one sentence each, what are deviance and scaled "
            "deviance, and what estimation principle is typically used for GLM "
            "parameters? (2) Refuse: 'Deleting insignificant terms until p-values "
            "look nice finishes explaining deviance and GLM estimation.'"
        ),
        cp_kw=["deviance", "scaled", "likelihood", "IWLS", "refuse", "p-value"],
        cp_model=(
            "(1) Deviance compares the fitted model's log-likelihood to a "
            "saturated model (2{ℓ_sat − ℓ_model}); scaled deviance divides by the "
            "dispersion/scale when relevant. Parameters are typically estimated "
            "by maximum likelihood (often via IWLS). (2) Refuse: mechanical "
            "p-value chopping is model-choice behaviour, not the definition or "
            "estimation of deviance."
        ),
        reflect="Harvest deviance/estimation wobble. Keep model-choice theatre out of tonight.",
    ),
    dict(
        day="CX-D7",
        stem="4.2.7-model-choice-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-MODEL-CHOICE",
        lo="4.2.7",
        slug="4.2-model-choice",
        keywords=["analysis of deviance", "significance", "model choice", "nested", "GLM"],
        title="Choose a GLM using analysis of deviance",
        purpose=(
            "Today's Mission exists to choose a suitable model using analysis of deviance "
            "and examination of parameter significance. Without pretending Pearson/"
            "deviance residuals (4.2.8) are finished."
        ),
        tutor=(
            "Today I will force nested comparison via analysis of deviance and refuse "
            "treating residual plots as today's LO."
        ),
        edu=(
            "Produce a cognitive move from deviance definition to lawful model-choice "
            "practice under CMP."
        ),
        lo_text=(
            "Choose a suitable model using an analysis of deviance and examination of the "
            "significance of the parameters."
        ),
        focus=(
            "Nested models → analysis of deviance / likelihood-ratio comparison → "
            "parameter significance."
        ),
        prior=(
            "Yesterday you explained deviance and estimation (4.2.6). Today continues "
            "Topic 4.2 at model choice."
        ),
        why=(
            "4.2.7 is contiguous after deviance. Without model choice, residual diagnostics "
            "have no selected structure to check."
        ),
        benefit=(
            "You will be able to choose a GLM using analysis of deviance and "
            "examination of parameter significance."
        ),
        explain=(
            "Day 7 focuses the named learning objective. Residuals as tomorrow."
        ),
        criteria=[
            "Closed-book, state what analysis of deviance compares.",
            "Name one role of parameter significance in model choice.",
            "Refuse one 'I plotted residuals, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch nested comparison before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.7.",
            "Closed-book Knowledge Checks: model choice + refuse residuals swallow.",
        ],
        next_code="4.2",
        next_title="Pearson and deviance residuals (4.2.8)",
        cont=(
            "Today you practised analysis-of-deviance model choice; tomorrow continues 4.2 "
            "at Pearson and deviance residuals."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.8. Titles only tonight",
        student=(
            "Tomorrow: Pearson and deviance residuals (4.2.8). Optional light prep: skim "
            "4.2.8 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.7 analysis of deviance and model choice",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.7 "
            "(stop before Pearson / deviance residuals 4.2.8)"
        ),
        oos=[
            "Pearson / deviance residuals as primary (4.2.8)",
            "χ² / LRT acceptability tests as primary (4.2.9)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating every small p-value as automatic model truth.",
            "Watch for jumping into residual diagnostics (4.2.8) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does analysis of deviance compare? (2) How do parameter "
            "significance checks enter? (3) Name one reason residuals are not today's LO."
        ),
        ar_kw=["deviance", "nested", "significance", "choose", "model"],
        ar_model=(
            "Analysis of deviance compares nested models via deviance differences; "
            "parameter significance supports inclusion. Residuals are tomorrow."
        ),
        cp_prompt=(
            "Closed-book. Nested GLMs M_reduced ⊂ M_full. (1) Outline how an "
            "analysis of deviance (likelihood-ratio / deviance difference) plus "
            "parameter significance guides choosing between them. (2) Refuse: "
            "'Plotting Pearson residuals finishes model choice via analysis of "
            "deviance.'"
        ),
        cp_kw=["analysis of deviance", "nested", "χ²", "significance", "refuse", "residuals"],
        cp_model=(
            "(1) Compare deviance (or −2Δℓ) between nested models against a χ² "
            "reference on the degrees-of-freedom difference; also inspect whether "
            "added parameters are statistically and scientifically warranted. (2) "
            "Refuse: residual plots are diagnostics (a different LO); today is "
            "choosing a model via analysis of deviance and parameter "
            "significance."
        ),
        reflect="Harvest model-choice wobble. Keep residual diagnostics out of tonight.",
    ),
    dict(
        day="CX-D8",
        stem="4.2.8-residuals-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-RESIDUALS",
        lo="4.2.8",
        slug="4.2-residuals",
        keywords=["Pearson", "deviance residual", "diagnostic", "GLM"],
        title="Use Pearson and deviance residuals",
        purpose=(
            "Today's Mission exists to explain Pearson and deviance residuals and their "
            "use. Without pretending χ² / LRT acceptability tests (4.2.9) are finished."
        ),
        tutor=(
            "Today I will force Pearson vs deviance residual discrimination and refuse "
            "treating formal acceptability tests as today's LO."
        ),
        edu=(
            "Produce a cognitive move from selected model to lawful residual diagnostics "
            "under CMP."
        ),
        lo_text="Explain Pearson and deviance residuals and their use.",
        focus=(
            "Pearson residual → deviance residual → diagnostic use for fit, "
            "outliers and patterns."
        ),
        prior=(
            "Yesterday you chose a model via analysis of deviance (4.2.7). Today continues "
            "Topic 4.2 at residuals."
        ),
        why=(
            "4.2.8 is contiguous after model choice. Without residual literacy, "
            "acceptability tests lack diagnostic context."
        ),
        benefit=(
            "You will be able to explain Pearson and deviance residuals and how "
            "they are used diagnostically."
        ),
        explain=(
            "Day 8 focuses the named learning objective. Formal acceptability tests as tomorrow."
        ),
        criteria=[
            "Closed-book, state what a Pearson residual uses.",
            "State what a deviance residual uses.",
            "Refuse one 'I ran the LRT, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch residual types before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.8.",
            "Closed-book Knowledge Checks: residuals + refuse test swallow.",
        ],
        next_code="4.2",
        next_title="Acceptability tests for a fitted GLM (4.2.9)",
        cont=(
            "Today you established Pearson and deviance residuals; tomorrow continues 4.2 "
            "at formal acceptability tests."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.9. Titles only tonight",
        student=(
            "Tomorrow: Pearson χ² and likelihood-ratio acceptability tests (4.2.9). "
            "Optional light prep: skim 4.2.9 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.8 Pearson and deviance residuals",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.8 "
            "(stop before χ² / LRT acceptability tests 4.2.9)"
        ),
        oos=[
            "χ² / LRT acceptability tests as primary (4.2.9)",
            "Software fit/interpret as primary (4.2.10)",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating residual plots as automatic model proof.",
            "Watch for jumping into formal χ²/LRT (4.2.9) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What enters a Pearson residual? (2) What enters a deviance "
            "residual? (3) Name one diagnostic use. (4) Name one reason formal "
            "acceptability tests are not today's LO."
        ),
        ar_kw=["Pearson", "deviance", "residual", "fitted", "diagnostic"],
        ar_model=(
            "Pearson uses observed vs fitted scaled by variance structure; deviance "
            "residuals come from deviance contributions. Formal χ²/LRT tests are tomorrow."
        ),
        cp_prompt=(
            "Closed-book. (1) State the idea of a Pearson residual and a deviance "
            "residual for a GLM observation. (2) Refuse: 'Running a "
            "likelihood-ratio test finishes explaining Pearson and deviance "
            "residuals.'"
        ),
        cp_kw=["Pearson", "deviance residual", "standardised", "refuse", "likelihood-ratio"],
        cp_model=(
            "(1) Pearson residual: (y − μ̂)/√Var̂(Y). A standardised "
            "discrepancy. Deviance residual: the signed contribution of "
            "observation i to the deviance. Both help check fit, outliers and "
            "patterns. (2) Refuse: an LRT is a formal "
            "acceptability/model-comparison test: different from defining and "
            "using residual diagnostics."
        ),
        reflect="Harvest residual-type wobble. Keep χ²/LRT out of tonight's claim.",
    ),
    dict(
        day="CX-D9",
        stem="4.2.9-goodness-tests-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-GOODNESS-TESTS",
        lo="4.2.9",
        slug="4.2-goodness-tests",
        keywords=["chi-square", "likelihood-ratio", "acceptability", "goodness", "GLM"],
        title="Test acceptability of a fitted GLM",
        purpose=(
            "Today's Mission exists to apply statistical tests to determine acceptability "
            "of a fitted model (Pearson's chi-square test and the likelihood-ratio test)"
            "without pretending software fit/interpret (4.2.10) is finished."
        ),
        tutor=(
            "Today I will force χ² vs LRT acceptability discrimination and refuse treating "
            "full software interpretation as today's LO."
        ),
        edu=(
            "Produce a cognitive move from residual literacy to lawful formal acceptability "
            "tests under CMP."
        ),
        lo_text=(
            "Apply statistical tests to determine the acceptability of a fitted model: "
            "Pearson's chi-square test and the likelihood-ratio test."
        ),
        focus="Fitted GLM → Pearson χ² acceptability test → likelihood-ratio test.",
        prior=(
            "Yesterday you explained Pearson and deviance residuals (4.2.8). Today "
            "continues Topic 4.2 at formal acceptability tests."
        ),
        why=(
            "4.2.9 is contiguous after residuals. Without formal tests, fit/interpret "
            "lacks acceptability warrant."
        ),
        benefit=(
            "You will be able to apply Pearson's χ² and likelihood-ratio tests to "
            "judge acceptability of a fitted GLM."
        ),
        explain=(
            "Day 9 focuses the named learning objective. Fit/ interpret as tomorrow."
        ),
        criteria=[
            "Closed-book, name the two acceptability tests in 4.2.9.",
            "State one modelling question each test addresses.",
            "Refuse one 'I interpreted every coefficient in software, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch χ² vs LRT before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.9.",
            "Closed-book Knowledge Checks: tests + refuse fit/interpret swallow.",
        ],
        next_code="4.2",
        next_title="Fit a GLM and interpret the output (4.2.10)",
        cont=(
            "Today you established formal acceptability tests; tomorrow continues 4.2 at "
            "fitting and interpreting a GLM."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.2.10. Titles only tonight",
        student=(
            "Tomorrow: fit a GLM and interpret output (4.2.10). Optional light prep: skim "
            "4.2.10 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 4.2.9 Pearson chi-square and likelihood-ratio tests",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.9 "
            "(stop before fit / interpret 4.2.10)"
        ),
        oos=[
            "Software fit / full output interpretation as primary (4.2.10)",
            "Bayesian / Topic 5.1 as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating a non-significant χ² as automatic model perfection.",
            "Watch for jumping into full software interpretation (4.2.10) as today's finish.",
            "Watch for Trust Front 5.1 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) Name the two acceptability tests in 4.2.9. (2) What question "
            "does each address? (3) Name one reason full fit/interpret is not today's LO."
        ),
        ar_kw=["chi-square", "likelihood-ratio", "acceptability", "fitted", "test"],
        ar_model=(
            "Pearson's chi-square and the likelihood-ratio test assess fitted-model "
            "acceptability. Full software fit/interpret is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. You have a fitted GLM and want to judge acceptability. "
            "(1) State what Pearson's χ² test and the likelihood-ratio test each "
            "compare (in outline). (2) Refuse: 'Interpreting every coefficient in "
            "the software output finishes applying acceptability tests.'"
        ),
        cp_kw=["Pearson", "chi-square", "likelihood-ratio", "acceptability", "refuse", "interpret"],
        cp_model=(
            "(1) Pearson χ²: aggregate squared Pearson residuals against a χ² "
            "reference (adequacy of fit). LRT: compares likelihood/deviance of "
            "the fitted model to a relevant nested or saturated alternative. (2) "
            "Refuse: coefficient interpretation is a different LO; today requires "
            "applying the formal acceptability tests."
        ),
        reflect="Harvest test-choice wobble. Keep full software interpretation out of tonight.",
    ),
    dict(
        day="CX-D10",
        stem="4.2.10-fit-interpret-cs1014",
        pid="CS1-EP001-PKG-CX-4.2-FIT-INTERPRET",
        lo="4.2.10",
        slug="4.2-fit-interpret",
        keywords=["fit", "interpret", "output", "GLM", "software"],
        title="Fit a GLM and interpret the output",
        purpose=(
            "Today's Mission exists to fit a generalised linear model to a data set and "
            "interpret the output (completing Topic 4.2 Learning before Revision) without "
            "opening Bayesian Topic 5.1 or claiming spine / until-exam trust."
        ),
        tutor=(
            "Today I will force fit-and-interpret literacy and refuse treating Bayesian / "
            "spine / until-exam as finished."
        ),
        edu=(
            "Produce a cognitive move from acceptability tests to lawful software fit and "
            "interpretation, closing 4.2 Learning under Continuity Front join."
        ),
        lo_text="Fit a generalised linear model to a data set and interpret the output.",
        focus=(
            "Choose family/link → fit GLM → interpret coefficients on the mean "
            "scale → check fit/diagnostics."
        ),
        prior=(
            "Yesterday you applied formal acceptability tests (4.2.9). Today closes Topic "
            "4.2 Learning at fit and interpret."
        ),
        why=(
            "After goodness-of-fit tests, fit a GLM and interpret the output. Then revise the GLM chain."
        ),
        benefit=(
            "You will be able to fit a GLM and interpret coefficients and fit "
            "output in exam-style language."
        ),
        explain=(
            "Day 10 closes Topic 4.2 at fit and interpret. Then revise; Bayesian work comes later."
        ),
        criteria=[
            "Closed-book, name at least three output elements you must interpret after a GLM fit.",
            "State one warrant linking today's fit to earlier 4.2 hinges.",
            "Refuse one 'I finished Bayesian / the exam journey' claim.",
        ],
        tasks=[
            "Sketch fit → interpret checklist before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.2.10.",
            "Closed-book Knowledge Checks: interpret + refuse 5.1/spine swallow.",
        ],
        next_code="CX-R1",
        next_title="Campaign Xi Revision: retrieve GLM hinges (4.2)",
        cont=(
            "Today you closed Topic 4.2 Learning at fit/interpret; tomorrow is Campaign Xi "
            "Revision returning to 4.2.1–4.2.10."
        ),
        prep="No new LO tonight: rest or jot the stickiest 4.2 hinge for Revision",
        student=(
            "Tomorrow: CX-R1 Revision of 4.2. Optional: note your weakest 4.2 link. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 4.2.10 fit a GLM and interpret the output",
        stop=(
            "Through the CMP treatment of Syllabus 4.2.10 "
            "(stop before Bayesian 5.1 / spine trophy claims)"
        ),
        oos=[
            "Bayesian / Topic 5.1 as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Wave 0 Approver honesty clearance",
            "Certified Educational Coverage increase from catalogue alone",
        ],
        misconceptions=[
            "Watch for treating GUI Fit as automatic interpretation complete.",
            "Watch for claiming Bayesian / spine / until-exam finished Continuity Front.",
            "Watch for skipping earlier 4.2 hinges as irrelevant once software runs.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does 4.2.10 require beyond clicking Fit? (2) Name three "
            "output elements to interpret. (3) Name one reason this does not finish Topic "
            "5.1 or first-pass spine."
        ),
        ar_kw=["fit", "interpret", "coefficient", "deviance", "residual", "output"],
        ar_model=(
            "Fit and interpret: coefficients, fit measures, residuals/diagnostics as "
            "warranted. Topic 5.1 Bayesian and first-pass spine PASS are out of scope."
        ),
        cp_prompt=(
            "Closed-book. You fit a Poisson log-link GLM for claim counts with "
            "factor rating class. (1) Interpret a coefficient of 0.20 on class "
            "High vs baseline in terms of mean count. (2) Refuse: 'Clicking Fit "
            "finishes interpretation and diagnostics' and 'fitting a GLM finishes "
            "Bayesian credibility work.'"
        ),
        cp_kw=["Poisson", "log link", "e^{0.20}", "interpret", "refuse", "Fit"],
        cp_model=(
            "(1) Under log link, β̂ = 0.20 means the fitted mean for High is "
            "e^{0.20} ≈ 1.22 times the baseline class mean (multiplicative "
            "effect), other terms held fixed. (2) Refuse: fit without "
            "interpretation/diagnostics is incomplete; Bayesian modelling is a "
            "different topic."
        ),
        reflect=(
            "Harvest fit/interpret wobble. Revision protects the 4.2 chain tomorrow."
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
        path.write_text(json.dumps(pkg, indent=2) + "\n")
        inventory.append(d["pid"])
        span.append(d["lo"])

    rev = apply_batch6b_mcq_overlay(revision_pkg(), "revision-glm-cs1014")
    (PKG_DIR / "revision-glm-cs1014.json").write_text(json.dumps(rev, indent=2) + "\n")
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-XI",
        "campaign_version": "cs1014-1.0.0",
        "display_title": (
            "Campaign Xi. Generalised linear models (4.2) · Continuity Front join"
        ),
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-014",
        "prior_volume_id": "CS1-013",
        "day_count": {"learning": 10, "revision": 1, "total": 11},
        "syllabus_span": span,
        "out_of_scope": [
            "Bayesian / Topic 5.1 absorb",
            "first-pass spine PASS",
            "until-examination educational trust",
            "Trust Front whole-Delta absorb into Continuity Front credit",
            "Wave 0 Approver honesty clearance",
            "Wave 13 authoring",
            "coverage mirage / Student Reliance increase from catalogue alone",
            "LIVE copies in educational_packages/",
        ],
        "inventory": inventory,
        "trust_front_note": (
            "CS1-003 / Campaign Delta remains independent Trust Front LIVE inventory for "
            "4.1–5.1. Xi package IDs are CX-prefixed Continuity Front join catalogue. "
            "not LIVE this cycle; Published Coverage unchanged (4.2 already counted)."
        ),
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()
