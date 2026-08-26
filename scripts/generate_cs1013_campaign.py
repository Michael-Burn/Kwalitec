#!/usr/bin/env python3
"""Generate CS1-013 / Campaign Nu educational packages (catalogue only).

Continuity Front join Pilot Arc for Topic 4.1 (linear regression models).
Topic 4.1 is already Published+LIVE via Trust Front CS1-003/Delta — Nu uses
distinct package IDs and must not be copied to educational_packages/ in this cycle.
Published Coverage and Student Reliance are unchanged by catalogue authoring.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-nu-cs1013"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1013-campaign-nu-1.0.0",
    "publication_version": "cs1013-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-NU",
    "volume_id": "CS1-013",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1013_EDUCATIONAL_VOLUME.md",
        "CS1013_CERTIFICATION_REPORT.md",
        "EP011_WAVE11_PLAN.md",
    ],
    "author_id": "cs1013-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "4.1",
    "topic_title": "Understand and use linear regression models",
    "topic_id": "CS1-D-T01",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "4.1", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1013-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1013-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1013-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Mission for Syllabus {lo} — not the next LO as primary."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo}, exit to CMP, retrieve today's hinge, refuse swallowed next LO."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo}. This is Study Progress for today's block — not Topic Complete "
                f"for later 4.1 LOs, Trust Front absorb of 4.2/5.1, first-pass spine PASS, or "
                "until-exam trust."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} hinge closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to extract Syllabus {lo} — "
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
                f"{d['open']}. Kwalitec is the guide; the CMP is the authoritative material — "
                "do not treat this activity body as a substitute textbook. Hunt with the focus "
                "questions; watch the misconception list. Ignore items in out_of_scope_today. "
                f"Stop when: {d['stop']}. Then close the CMP and return here — next in-app "
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
                    "cue": "Pause — write today's core move in one sentence.",
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
                "episode_id": f"lep-cs1013-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1013-{lo}-ar-01",
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
                "episode_id": f"lep-cs1013-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1013-{lo}-cp-01",
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
    day = "CN-R1"
    pid = "CS1-EP001-PKG-REV-LINEAR-REGRESSION-NU"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Nu revision — linear regression models",
        "return_targets": [
            "4.1.1",
            "4.1.2",
            "4.1.3",
            "4.1.4",
            "4.1.5",
        ],
        "topic_aliases": [day, "campaign-nu-revision"],
        "topic_title_keywords": [
            "revision",
            "regression",
            "response",
            "explanatory",
            "least squares",
            "residuals",
            "variable selection",
        ],
        "golden_id": "GOLDEN-CS1013-CS1-CN-R1-LINEAR-REGRESSION",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1013-cs1-cn-r1-linear-regression",
            "display_title": "Retrieve linear-regression hinges (4.1)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Nu — retrieving response "
                "vs explanatory roles, simple vs multiple models, least squares, software fit "
                "and inference, and variable-selection fit measures — so 4.1 does not evaporate "
                "before an honest stop / Wave 0 honesty / spine re-audit successor."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Nu's Learning hinges — "
                "not a passive CMP re-read and not a Trust Front 4.2/5.1 absorb or until-exam claim."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: response/"
                "explanatory → simple/multiple → least squares → software fit/inference → "
                "variable selection."
            ),
            "learning_objective": (
                "Retrieve and connect (1) response and explanatory variables, (2) simple and "
                "multiple linear regression models, (3) least squares slope and intercept, "
                "(4) software fit with inference, GOF, prediction, and residual checks, and "
                "(5) measures of model fit for variable selection."
            ),
            "concept_focus": (
                "Campaign chain retrieval: response/explanatory → simple/multiple → least "
                "squares → software fit/inference → variable selection."
            ),
            "prior_bridge": (
                "Yesterday you finished variable selection (4.1.5). Today is Revision mode: "
                "return to 4.1.1–4.1.5 under closed-book retrieval — no new first-pass LO."
            ),
            "why_now": (
                "You've just finished linear regression; spaced retrieval now protects that chain "
                "before you stop."
            ),
            "expected_benefit": (
                "You'll confirm the linear-regression chain still retrieves — roles through variable selection."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the five 4.1 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse Trust Front 4.2/5.1 absorb / spine / until-exam claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Nu's chain: response/explanatory → "
                "simple/multiple → least squares → software fit → variable selection.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 45, "max": 65},
        },
        "session": {
            "session_id": "ssn-cs1013-cs1-cn-r1-linear-regression",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Nu skills — not to claim Trust Front absorb."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link — Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 45, "max": 65},
            "wrap_up": (
                "Revision Session complete. You stress-tested 4.1.1–4.1.5 return targets. "
                "This is revision Study Progress — not Topic Complete for 4.2/5.1, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that linear-regression hinges will still retrieve in "
                "three days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Nu "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the five 4.1 Learning hinges in order?",
                "Can you state least-squares vs software-fit inference vs variable selection?",
                "What claim must you refuse (4.2/5.1 absorb / spine / until-exam)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Trust Front 4.2/5.1 / spine / until-exam complete.",
                "Watch for dropping Mu hypothesis-testing memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection — do not claim Trust Front absorb, "
                "spine PASS, or until-exam trust in this sitting"
            ),
            "out_of_scope_today": [
                "GLM / Topic 4.2 as primary",
                "Bayesian / Topic 5.1 as primary",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Wave 0 Approver honesty clearance",
                "Certified Educational Coverage increase from catalogue alone",
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
                    "cue": "Pause — mark the weakest link before checks.",
                    "student_action": "Annotate",
                }
            ],
            "reentry_line": "Stay closed-book unless a check failed. Continue retrieval.",
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1013-cn-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1013-cn-r1-ar-01",
                "title": "Active Recall: CN-R1",
                "prompt": (
                    "Closed-book. Name the five Campaign Nu Learning hinges in order "
                    "(4.1.1→4.1.5) in short phrases."
                ),
                "response_type": "short_structured",
                "body": "Retrieve Nu chain closed-book.",
                "hints": ["Response/explanatory first.", "End with variable selection."],
                "accepted_keywords": [
                    "response",
                    "explanatory",
                    "simple",
                    "multiple",
                    "least squares",
                    "software",
                    "residuals",
                    "variable selection",
                ],
                "explanation": "RV retrieves the Campaign chain.",
                "model_answer": (
                    "4.1.1 response/explanatory → 4.1.2 simple/multiple → 4.1.3 least squares "
                    "→ 4.1.4 software fit/inference/prediction/residuals → 4.1.5 variable "
                    "selection by fit measures."
                ),
                "common_mistake": "Skipping least squares or collapsing software day into selection.",
                "success_criteria": ["Five hinges in order.", "Short phrases sufficient."],
            },
            {
                "episode_id": "lep-cs1013-cn-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1013-cn-r1-cp-01",
                "title": "Checkpoint: CN-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest linear-regression link and one "
                    "concrete rework. (2) Refuse: 'Variable selection finished GLM and "
                    "Bayesian modelling.' (3) Name whether you stop here or what syllabus "
                    "topic honestly comes next — not 'exam ready.'"
                ),
                "response_type": "short_structured",
                "body": "Weakest link + honest next.",
                "hints": ["Name a rework, not a vague review.", "Refuse trophy claims."],
                "accepted_keywords": [
                    "weakest",
                    "rework",
                    "refuse",
                    "4.2",
                    "spine",
                    "Wave 0",
                    "remainder",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. residual diagnostics — five-minute rework. (2) Refuse 4.2/5.1 "
                    "absorb / spine / until-exam. (3) Honest next is declared stop or Wave 0 "
                    "honesty / spine re-audit successor Volume — not claimed finished here."
                ),
                "common_mistake": "Spine / Trust Front absorb / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which linear-regression link retrieved least cleanly today and what one "
                "concrete rework will you schedule? Do not claim GLM (4.2) or Bayesian "
                "(5.1) are finished."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Confirm: 4.2/5.1 absorb / spine PASS / until-exam trust were out of scope.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "stop",
            "next_topic_title": (
                "Honest next — declared stop / Wave 0 honesty / spine re-audit successor "
                "— not Trust Front 4.2 absorb"
            ),
            "continuity_line": (
                "Campaign Nu / Volume CS1-013 completes after this Revision. Honest stop: "
                "4.1 Continuity Front join Pilot Arc closed — not Trust Front 4.2/5.1 absorb; "
                "not first-pass spine; not until-exam trust. Successor geography is Wave 0 "
                "honesty / spine re-audit under a later commission (or declared stop). "
                "CS1-003 Delta remains independent Trust Front LIVE inventory."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight — rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Nu / CS1-013 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await Wave 0 honesty / spine re-audit successor Volume. "
                "Optional: schedule your weakest 4.1 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CN-D1",
        stem="4.1.1-response-explanatory-cs1013",
        pid="CS1-EP001-PKG-CN-4.1-RESPONSE-EXPLANATORY",
        lo="4.1.1",
        slug="4.1-response-explanatory",
        keywords=[
            "response",
            "explanatory",
            "variable",
            "regression",
            "outcome",
            "predictor",
        ],
        title="Name response and explanatory variables with modelling intent",
        purpose=(
            "Today's Mission exists to make response vs explanatory naming a deliberate "
            "modelling move — so you enter linear regression with a clear outcome variable "
            "and predictors, without pretending simple/multiple model forms (4.1.2) are finished."
        ),
        tutor=(
            "Today I will force the candidate to discriminate response from explanatory "
            "variables on an actuarial data sketch and refuse treating 'all columns are "
            "predictors' as modelling."
        ),
        edu=(
            "Produce a cognitive move from hypothesis-testing closure (3.3) to lawful "
            "response/explanatory roles at the Continuity Front join into Section 4."
        ),
        lo_text="Response and explanatory variables",
        focus=(
            "Data sketch → name response Y → name explanatory X's with warrants → "
            "refuse column-soup modelling."
        ),
        prior=(
            "Campaign Mu closed hypothesis testing and goodness of fit (3.3) with Revision. "
            "Today opens Continuity Front join at Topic 4.1 LO 4.1.1 — the next official "
            "syllabus topic after 3.3. Trust Front CS1-003 already holds LIVE 4.1 inventory "
            "independently; Nu is the Continuity Front native Pilot Arc."
        ),
        why=(
            "4.1.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at regression roles, keeping simple/multiple models for the following session."
        ),
        benefit=(
            "You will be able to name response and explanatory variables with "
            "modelling warrants for a stated actuarial sketch."
        ),
        explain=(
            "Day 1 opens linear regression at response vs explanatory roles — "
            "the natural next step after hypothesis testing."
        ),
        criteria=[
            "Closed-book, name one response and at least one explanatory variable for a "
            "stated scenario.",
            "Justify each role in one sentence.",
            "Refuse one 'every column is a predictor' claim.",
        ],
        tasks=[
            "Sketch response vs explanatory roles before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.1.1.",
            "Closed-book Knowledge Checks: roles + refuse column-soup.",
        ],
        next_code="4.1",
        next_title="Simple and multiple linear regression models (4.1.2)",
        cont=(
            "Today you established response and explanatory roles; tomorrow continues 4.1 at "
            "simple vs multiple linear models."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.1.2 — titles only tonight",
        student=(
            "Tomorrow: simple and multiple linear regression models (4.1.2). Optional light "
            "prep: skim 4.1.2 headings — titles only tonight."
        ),
        open="CMP · Syllabus 4.1.1 response and explanatory variables",
        stop=(
            "Through the CMP treatment of Syllabus 4.1.1 "
            "(stop before simple/multiple model forms 4.1.2)"
        ),
        oos=[
            "Simple vs multiple model forms as primary (4.1.2)",
            "Least squares estimation as primary (4.1.3)",
            "Software fit / inference as primary (4.1.4)",
            "Variable selection as primary (4.1.5)",
            "GLM / Topic 4.2 as primary",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating every column as a predictor by default.",
            "Watch for starting simple/multiple algebra (4.1.2) inside this sitting.",
            "Watch for claiming Trust Front 4.2/5.1 absorb or spine PASS.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a response variable? (2) What is an explanatory "
            "variable? (3) Give one actuarial-flavoured pair (Y, X). (4) Name one reason "
            "simple vs multiple models are not today's LO."
        ),
        ar_kw=[
            "response",
            "explanatory",
            "outcome",
            "predictor",
            "Y",
            "X",
            "model",
        ],
        ar_model=(
            "Response is the outcome modelled; explanatory variables are the predictors. "
            "Example: claim severity (Y) vs age and sum insured (X's). Simple/multiple "
            "model forms are tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Motor book: you want to model claim severity. Columns "
            "include age, sum insured, claim amount, NCD discount, and claim "
            "count. (1) Name the response and two explanatory variables with a "
            "one-sentence warrant each. (2) Refuse: 'Put every numeric column on "
            "the right-hand side — that finishes variable-role modelling.'"
        ),
        cp_kw=["response", "explanatory", "severity", "claim amount", "refuse", "column"],
        cp_model=(
            "(1) Response Y = claim amount (severity — the outcome to "
            "explain/predict). Explanatory examples: age and sum insured "
            "(predictors of severity). Claim count is a frequency outcome, not "
            "automatically an X for severity. (2) Refuse: column-soup is not "
            "modelling — choose Y for the modelling question, then choose X's "
            "with warrants."
        ),
        reflect="Harvest role-naming wobble — keep simple/multiple forms out of tonight's claim.",
    ),
    dict(
        day="CN-D2",
        stem="4.1.2-simple-multiple-cs1013",
        pid="CS1-EP001-PKG-CN-4.1-SIMPLE-MULTIPLE",
        lo="4.1.2",
        slug="4.1-simple-multiple",
        keywords=[
            "simple",
            "multiple",
            "linear",
            "regression",
            "model",
            "explanatory",
        ],
        title="Distinguish simple and multiple linear regression models",
        purpose=(
            "Today's Mission exists to distinguish the simple regression model (one "
            "explanatory variable) from the multiple linear regression model (several "
            "explanatory variables) — without pretending least squares estimation (4.1.3) "
            "is finished."
        ),
        tutor=(
            "Today I will force the candidate to write the model forms and refuse treating "
            "least-squares algebra as today's LO."
        ),
        edu=(
            "Produce a cognitive move from variable roles to lawful simple vs multiple "
            "linear model statements under CMP."
        ),
        lo_text=(
            "Simple regression model (with a single explanatory variable) and multiple "
            "linear regression model (with several explanatory variables)"
        ),
        focus=(
            "One explanatory variable → simple linear form → several explanatory "
            "variables → multiple linear form."
        ),
        prior=(
            "Yesterday you named response and explanatory variables (4.1.1). Today continues "
            "Topic 4.1 at model forms — still Continuity Front join, still refuse 4.2/5.1."
        ),
        why=(
            "4.1.2 is contiguous after roles. Without model forms, least squares and "
            "software fit have no structure to estimate."
        ),
        benefit=(
            "You will be able to write simple and multiple linear regression "
            "model forms and distinguish them from OLS estimation."
        ),
        explain=(
            "Day 2 focuses the named learning objective — estimation as tomorrow."
        ),
        criteria=[
            "Closed-book, write or state the simple linear model form.",
            "State how the multiple linear model extends it.",
            "Refuse one 'I fitted least squares, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch simple vs multiple forms before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.1.2.",
            "Closed-book Knowledge Checks: forms + refuse least-squares swallow.",
        ],
        next_code="4.1",
        next_title="Least squares estimates of slope and intercept (4.1.3)",
        cont=(
            "Today you established simple vs multiple linear models; tomorrow continues 4.1 "
            "at least squares estimation."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.1.3 — titles only tonight",
        student=(
            "Tomorrow: least squares slope and intercept (4.1.3). Optional light prep: "
            "skim 4.1.3 headings — titles only tonight."
        ),
        open="CMP · Syllabus 4.1.2 simple and multiple linear regression models",
        stop=(
            "Through the CMP treatment of Syllabus 4.1.2 "
            "(stop before least squares estimation 4.1.3)"
        ),
        oos=[
            "Least squares estimation as primary (4.1.3)",
            "Software fit / inference as primary (4.1.4)",
            "Variable selection as primary (4.1.5)",
            "GLM / Topic 4.2 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating 'multiple' with GLM / non-linear models.",
            "Watch for diving into least-squares formulae (4.1.3) as today's finish.",
            "Watch for Trust Front 4.2 absorb claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a simple linear regression model? (2) What is a "
            "multiple linear regression model? (3) Name one modelling reason to prefer "
            "multiple over simple. (4) Name one reason least squares is not today's LO."
        ),
        ar_kw=[
            "simple",
            "multiple",
            "linear",
            "explanatory",
            "single",
            "several",
            "model",
        ],
        ar_model=(
            "Simple has one explanatory variable; multiple has several. Multiple can hold "
            "additional predictors jointly. Least squares estimation is tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Claim severity Y with predictors age (x₁) and sum "
            "insured (x₂). (1) Write the simple linear model using only age, and "
            "the multiple linear model using both predictors. (2) Refuse: "
            "'Writing the least-squares formulae for β̂ finishes stating the "
            "model forms.'"
        ),
        cp_kw=["simple", "multiple", "β₀", "age", "refuse", "least squares"],
        cp_model=(
            "(1) Simple: Y = β₀ + β₁ age + ε. Multiple: Y = β₀ + β₁ age + β₂ "
            "sum_insured + ε. (2) Refuse: least squares is the estimation "
            "criterion; today is stating the simple vs multiple linear model "
            "forms."
        ),
        reflect="Harvest form-statement wobble — keep least squares out of tonight's claim.",
    ),
    dict(
        day="CN-D3",
        stem="4.1.3-least-squares-cs1013",
        pid="CS1-EP001-PKG-CN-4.1-LEAST-SQUARES",
        lo="4.1.3",
        slug="4.1-least-squares",
        keywords=[
            "least squares",
            "slope",
            "intercept",
            "estimate",
            "simple",
            "linear",
        ],
        title="Obtain least squares estimates of slope and intercept",
        purpose=(
            "Today's Mission exists to obtain least squares estimates of the slope and "
            "intercept parameters in a simple linear regression model — without pretending "
            "software fit and inference (4.1.4) are finished."
        ),
        tutor=(
            "Today I will force the candidate to connect residuals to the least-squares "
            "criterion and refuse treating GUI software output as today's LO."
        ),
        edu=(
            "Produce a cognitive move from model forms to the least-squares estimation "
            "criterion and slope/intercept estimates for the simple linear model."
        ),
        lo_text=(
            "Least squares estimates of the slope and intercept parameters in a simple "
            "linear regression model"
        ),
        focus=(
            "Residual → sum of squared residuals → least-squares slope and "
            "intercept formulae."
        ),
        prior=(
            "Yesterday you distinguished simple and multiple linear models (4.1.2). Today "
            "estimates the simple linear parameters by least squares."
        ),
        why=(
            "4.1.3 is contiguous after model forms. Without least squares, software fit "
            "is black-box theatre."
        ),
        benefit=(
            "You will be able to state the OLS criterion and the closed-form "
            "slope and intercept for simple linear regression."
        ),
        explain=(
            "Day 3 focuses the named learning objective — software interpretation as tomorrow."
        ),
        criteria=[
            "Closed-book, state what least squares minimises.",
            "Name the two parameters estimated in the simple linear model.",
            "Refuse one 'I clicked Fit in software, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch residual → SS criterion before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.1.3.",
            "Closed-book Knowledge Checks: least squares + refuse software swallow.",
        ],
        next_code="4.1",
        next_title="Software fit, inference, prediction, and residual checks (4.1.4)",
        cont=(
            "Today you established least squares for the simple linear model; tomorrow "
            "continues 4.1 at software fit and interpretation."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.1.4 — titles only tonight",
        student=(
            "Tomorrow: software fit, inference, prediction, residuals (4.1.4). Optional "
            "light prep: skim 4.1.4 headings — titles only tonight."
        ),
        open="CMP · Syllabus 4.1.3 least squares estimates (simple linear regression)",
        stop=(
            "Through the CMP treatment of Syllabus 4.1.3 "
            "(stop before software fit / inference 4.1.4)"
        ),
        oos=[
            "Software fit / inference / prediction / residual diagnostics as primary (4.1.4)",
            "Variable selection as primary (4.1.5)",
            "GLM / Topic 4.2 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating least squares with maximum likelihood without CMP warrant.",
            "Watch for jumping into software output interpretation (4.1.4) as today's finish.",
            "Watch for multiple-regression matrix algebra as the required hinge today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What quantity does least squares minimise? (2) Which two "
            "parameters are estimated in the simple linear model? (3) What is a residual? "
            "(4) Name one reason software fit is not today's LO."
        ),
        ar_kw=[
            "least squares",
            "residual",
            "slope",
            "intercept",
            "minimise",
            "sum of squares",
        ],
        ar_model=(
            "Least squares minimises the sum of squared residuals. Slope and intercept are "
            "estimated. A residual is observed minus fitted. Software fit/inference is "
            "tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Simple linear model Y = β₀ + β₁x + ε with data pairs "
            "(xᵢ, yᵢ). (1) State the least-squares criterion and the closed-form "
            "slope (in terms of sums or covariance). (2) Refuse: 'Least squares "
            "is just clicking Fit' and 'the OLS slope equals Corr(X,Y).'"
        ),
        cp_kw=["least squares", "minimise", "slope", "intercept", "refuse", "correlation"],
        cp_model=(
            "(1) Choose β₀, β₁ to minimise Σ(yᵢ − β₀ − β₁xᵢ)². Slope β̂₁ = "
            "Σ(xᵢ−x̄)(yᵢ−ȳ)/Σ(xᵢ−x̄)² = Cov̂(X,Y)/Var̂(X); intercept β̂₀ = ȳ − "
            "β̂₁ x̄. (2) Refuse: Fit implements OLS but is not the criterion; "
            "Corr(X,Y) is dimensionless association, not the OLS slope (which "
            "scales by SD_Y/SD_X)."
        ),
        reflect="Harvest least-squares criterion wobble — keep software day out of tonight's claim.",
    ),
    dict(
        day="CN-D4",
        stem="4.1.4-software-fit-cs1013",
        pid="CS1-EP001-PKG-CN-4.1-SOFTWARE-FIT",
        lo="4.1.4",
        slug="4.1-software-fit",
        keywords=[
            "software",
            "inference",
            "goodness of fit",
            "prediction",
            "residuals",
            "confidence",
        ],
        title="Fit a linear regression in software and interpret the output",
        purpose=(
            "Today's Mission exists to use appropriate software to fit a linear regression "
            "model and interpret the output: inference on the slope, measures of goodness "
            "of fit, prediction of mean or individual response with confidence limits, and "
            "residual checks of suitability — without pretending variable selection (4.1.5) "
            "is finished."
        ),
        tutor=(
            "Today I will force the candidate to read software output as evidence — slope "
            "inference, GOF, prediction limits, residual checks — and refuse treating "
            "variable-selection shopping as today's LO."
        ),
        edu=(
            "Produce a cognitive move from hand least squares to software-mediated fit, "
            "inference, prediction, and residual diagnostics under CMP."
        ),
        lo_text=(
            "Use of appropriate software to fit a linear regression model to a data set and "
            "interpret the output: Perform statistical inference on the slope parameter; "
            "Describe the use of measures of goodness of fit of a linear regression model; "
            "Use a fitted linear relationship to predict a mean response or an individual "
            "response with confidence limits; Use residuals to check the suitability and "
            "validity of a linear regression model"
        ),
        focus=(
            "Software fit → slope inference → GOF measures → mean vs individual "
            "prediction limits → residual checks."
        ),
        prior=(
            "Yesterday you obtained least squares estimates for the simple linear model "
            "(4.1.3). Today practises software fit and interpretation of that fitted relationship."
        ),
        why=(
            "4.1.4 is contiguous after least squares. Examiners expect software output "
            "literacy — not GUI tourism and not jumping to selection theatre."
        ),
        benefit=(
            "You will be able to interpret a fitted linear regression: slope "
            "inference, GOF, prediction limits, and residual checks."
        ),
        explain=(
            "Day 4 focuses the named learning objective — variable selection as the final Learning day."
        ),
        criteria=[
            "Closed-book, name the four interpretation moves in 4.1.4 (inference, GOF, "
            "prediction limits, residual checks).",
            "Distinguish mean-response vs individual-response prediction intervals.",
            "Refuse one 'I picked the best subset today' variable-selection claim.",
        ],
        tasks=[
            "Sketch the four interpretation moves before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.1.4.",
            "Closed-book Knowledge Checks: software interpretation + refuse selection swallow.",
        ],
        next_code="4.1",
        next_title="Measures of model fit for variable selection (4.1.5)",
        cont=(
            "Today you practised software fit and interpretation; tomorrow continues 4.1 at "
            "variable selection using measures of model fit."
        ),
        prep="Optional: glance at CMP headings for Syllabus 4.1.5 — titles only tonight",
        student=(
            "Tomorrow: variable selection via fit measures (4.1.5). Optional light prep: "
            "skim 4.1.5 headings — titles only tonight."
        ),
        open="CMP · Syllabus 4.1.4 software fit and interpretation of linear regression",
        stop=(
            "Through the CMP treatment of Syllabus 4.1.4 "
            "(stop before variable selection 4.1.5)"
        ),
        oos=[
            "Variable selection as primary (4.1.5)",
            "GLM / Topic 4.2 as primary",
            "Bayesian / Topic 5.1 as primary",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating confidence limits for a mean response with prediction of "
            "an individual.",
            "Watch for treating residual plots as optional decoration.",
            "Watch for starting variable-selection shopping (4.1.5) as today's finish.",
        ],
        ar_prompt=(
            "Closed-book. (1) What inference on the slope do you report from software? "
            "(2) Name one goodness-of-fit measure use. (3) How do mean-response and "
            "individual-response prediction limits differ? (4) What do residuals check? "
            "(5) Name one reason variable selection is not today's LO."
        ),
        ar_kw=[
            "slope",
            "inference",
            "goodness of fit",
            "prediction",
            "confidence",
            "residuals",
            "mean",
            "individual",
        ],
        ar_model=(
            "Slope inference uses the software estimate and its uncertainty under CMP. GOF "
            "summarises how well the linear relationship describes the data. Individual "
            "prediction limits are wider than mean-response limits. Residuals check "
            "suitability/validity. Variable selection is tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. After fitting Y = β₀ + β₁x in software you see β̂₁, "
            "SE(β̂₁), R², and residual plots. (1) For a new x*, distinguish "
            "predicting the mean response E[Y|x*] from predicting an individual "
            "Y_new — which interval is typically wider? (2) Refuse: 'Running "
            "best-subset selection finishes software fit/inference' and "
            "'residuals are optional after a significant slope.'"
        ),
        cp_kw=["mean response", "prediction", "wider", "residuals", "refuse", "selection"],
        cp_model=(
            "(1) A mean-response interval covers E[Y|x*]; a prediction interval "
            "covers a new observation and is typically wider (adds residual "
            "variance). (2) Refuse: variable selection is a different LO; slope "
            "inference, GOF, prediction limits, and residual checks are all "
            "required after a fit."
        ),
        reflect=(
            "Harvest prediction-limit or residual-check wobble — keep selection out of "
            "tonight's claim."
        ),
    ),
    dict(
        day="CN-D5",
        stem="4.1.5-variable-selection-cs1013",
        pid="CS1-EP001-PKG-CN-4.1-VARIABLE-SELECTION",
        lo="4.1.5",
        slug="4.1-variable-selection",
        keywords=[
            "variable selection",
            "model fit",
            "explanatory",
            "measure",
            "compare",
        ],
        title="Select explanatory variables using measures of model fit",
        purpose=(
            "Today's Mission exists to use measures of model fit to select an appropriate "
            "set of explanatory variables — without pretending GLM (4.2) or Bayesian (5.1) "
            "are finished, and without claiming first-pass spine PASS."
        ),
        tutor=(
            "Today I will force the candidate to compare candidate explanatory sets using "
            "fit measures and refuse treating Trust Front 4.2/5.1 absorb as Continuity "
            "Front credit."
        ),
        edu=(
            "Produce a cognitive move from a single fitted linear model to disciplined "
            "variable selection using measures of model fit under CMP."
        ),
        lo_text=(
            "Measures of model fit to select an appropriate set of explanatory variables"
        ),
        focus=(
            "Candidate explanatory sets → fit measures (e.g. adjusted R², "
            "AIC/BIC) → select an appropriate set."
        ),
        prior=(
            "Yesterday you practised software fit, inference, prediction, and residual "
            "checks (4.1.4). Today closes Topic 4.1 Learning at variable selection."
        ),
        why=(
            "Finish Topic 4.1 by selecting variables using fit measures — then revise before moving into GLM."
        ),
        benefit=(
            "You will be able to use measures of model fit to select an "
            "appropriate set of explanatory variables."
        ),
        explain=(
            "Day 5 closes Topic 4.1 at variable selection — GLM and Bayesian work come later."
        ),
        criteria=[
            "Closed-book, name what 'selecting explanatory variables using measures of "
            "model fit' means in CMP-usable form.",
            "State one reason more variables is not automatically better.",
            "Refuse one 'I finished 4.2/GLM / spine / until-exam' claim.",
        ],
        tasks=[
            "Sketch selection-by-fit-measure logic before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 4.1.5.",
            "Closed-book Knowledge Checks: selection hinge + refuse 4.2/spine swallow.",
        ],
        next_code="CN-R1",
        next_title="Campaign Nu Revision — retrieve 4.1 hinges",
        cont=(
            "Today you closed Topic 4.1 Learning at variable selection; tomorrow is "
            "Campaign Nu Revision returning to 4.1.1–4.1.5."
        ),
        prep="No new LO tonight — rest or jot the stickiest 4.1 hinge for Revision",
        student=(
            "Tomorrow: CN-R1 Revision of 4.1. Optional: note your weakest 4.1 link — "
            "titles only tonight."
        ),
        open="CMP · Syllabus 4.1.5 measures of model fit for variable selection",
        stop=(
            "Through the CMP treatment of Syllabus 4.1.5 "
            "(stop before GLM 4.2 / Bayesian 5.1 / spine trophy claims)"
        ),
        oos=[
            "GLM / Topic 4.2 as primary",
            "Bayesian / Topic 5.1 as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Wave 0 Approver honesty clearance",
            "Certified Educational Coverage increase from catalogue alone",
        ],
        misconceptions=[
            "Watch for equating 'best R²' with automatically correct selection without CMP caveat.",
            "Watch for claiming GLM/Bayesian finished Continuity Front.",
            "Watch for claiming spine / until-exam complete after Topic 4.1.",
        ],
        ar_prompt=(
            "Closed-book. (1) What decision does 4.1.5 ask you to make? (2) What role do "
            "measures of model fit play? (3) Name one reason more explanatory variables is "
            "not automatically better. (4) Name one reason this does not finish Topic 4.2 "
            "or first-pass spine."
        ),
        ar_kw=[
            "selection",
            "explanatory",
            "model fit",
            "measure",
            "compare",
            "overfit",
            "4.2",
        ],
        ar_model=(
            "4.1.5 selects an appropriate explanatory set using fit measures. More "
            "variables can overfit or dilute interpretation. Topic 4.2 GLM and first-pass "
            "spine PASS are out of scope."
        ),
        cp_prompt=(
            "Closed-book. Two nested linear models for claim severity: M1 uses "
            "age only; M2 adds sum insured and NCD. (1) Name two fit measures you "
            "could use to choose between candidate explanatory sets and what each "
            "rewards or penalises. (2) Refuse: 'Keep every term with p<0.05 and "
            "selection is done' and 'variable selection finishes GLM modelling.'"
        ),
        cp_kw=["adjusted R²", "AIC", "BIC", "selection", "refuse", "p-value"],
        cp_model=(
            "(1) e.g. adjusted R² (rewards fit while adjusting for unused "
            "complexity vs raw R²); AIC/BIC (likelihood fit with a "
            "parameter-count penalty). (2) Refuse: mechanical p-value chopping is "
            "not a complete selection warrant; GLM is a different topic — today "
            "is selecting explanatory variables for linear models via fit "
            "measures."
        ),
        reflect=(
            "Harvest selection / fit-measure wobble — Revision protects the 4.1 chain tomorrow."
        ),
    ),
]


def main() -> None:
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    inventory: list[str] = []
    span: list[str] = []

    for d in LEARNING:
        pkg = learning_pkg(d)
        path = PKG_DIR / f"{d['stem']}.json"
        path.write_text(json.dumps(pkg, indent=2) + "\n")
        inventory.append(d["pid"])
        span.append(d["lo"])

    rev = revision_pkg()
    (PKG_DIR / "revision-linear-regression-cs1013.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-NU",
        "campaign_version": "cs1013-1.0.0",
        "display_title": (
            "Campaign Nu — Linear regression models (4.1) · Continuity Front join"
        ),
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-013",
        "prior_volume_id": "CS1-012",
        "day_count": {"learning": 5, "revision": 1, "total": 6},
        "syllabus_span": span,
        "out_of_scope": [
            "GLM / Topic 4.2 absorb",
            "Bayesian / Topic 5.1 absorb",
            "first-pass spine PASS",
            "until-examination educational trust",
            "Trust Front whole-Delta absorb into Continuity Front credit",
            "Wave 0 Approver honesty clearance",
            "Wave 12 authoring",
            "coverage mirage / Student Reliance increase from catalogue alone",
            "LIVE copies in educational_packages/",
        ],
        "inventory": inventory,
        "trust_front_note": (
            "CS1-003 / Campaign Delta remains independent Trust Front LIVE inventory for "
            "4.1–5.1. Nu package IDs are CN-prefixed Continuity Front join catalogue — "
            "not LIVE this cycle; Published Coverage unchanged (4.1 already counted)."
        ),
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()
