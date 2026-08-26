#!/usr/bin/env python3
"""Generate CS1-005 / Campaign Epsilon educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-epsilon-cs1005"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1005-campaign-epsilon-1.0.0",
    "publication_version": "cs1005-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-EPSILON",
    "volume_id": "CS1-005",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1005_EDUCATIONAL_VOLUME.md",
        "CS1005_CERTIFICATION_REPORT.md",
        "EP003_WAVE3_PLAN.md",
    ],
    "author_id": "cs1005-educational-author",
    "authored_at": "2026-08-01",
}

TOPIC = {
    "topic_code": "2.2",
    "topic_title": "Determine the characteristics of jointly distributed random variables",
    "topic_id": "CS1-B-T02",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "2.2", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1005-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1005-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1005-cs1-{d['slug']}",
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
                f"for later 2.2 LOs or Chapter 2."
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
                "episode_id": f"lep-cs1005-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1005-{lo}-ar-01",
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
                "episode_id": f"lep-cs1005-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1005-{lo}-cp-01",
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
    day = "CE-R1"
    pid = "CS1-EP001-PKG-REV-JOINT-DISTRIBUTIONS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Epsilon revision: jointly distributed random variables",
        "return_targets": ["2.2.1", "2.2.2", "2.2.3", "2.2.4"],
        "topic_aliases": [day, "campaign-epsilon-revision"],
        "topic_title_keywords": [
            "revision",
            "joint",
            "marginal",
            "independence",
            "covariance",
            "linear",
        ],
        "golden_id": "GOLDEN-CS1005-CS1-CE-R1-JOINT-DISTRIBUTIONS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1005-cs1-ce-r1-joint-distributions",
            "display_title": "Retrieve joint-distribution hinges (2.2)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Epsilon. Retrieving "
                "marginal/conditional distributions, independence conditions, covariance/"
                "correlation/E[g(X,Y)], and mean/variance of linear combinations. So 2.2 does "
                "not evaporate before conditional expectation (2.3)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Epsilon's Learning hinges. "
                "not a passive CMP re-read and not a first-pass 2.3 lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: marginal/"
                "conditional → independence → dependence measures → linear combinations."
            ),
            "learning_objective": (
                "Retrieve and connect (1) marginal/conditional from a joint, (2) independence "
                "conditions, (3) covariance/correlation/E[g(X,Y)], and (4) mean and variance of "
                "a linear combination."
            ),
            "concept_focus": (
                "Campaign chain retrieval: joint → marginal/conditional → independence → "
                "cov/corr → linear combinations."
            ),
            "prior_bridge": (
                "Yesterday you finished mean and variance of linear combinations (2.2.4). "
                "Today is Revision mode: return to 2.2.1–2.2.4 under closed-book retrieval. "
                "no new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 2.3 work."
            ),
            "expected_benefit": (
                "Evidence that the 2.2 chain retrieves. Revision Study Progress, not a claim "
                "that Chapter 2 or the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, outline marginal or conditional from a joint.",
                "Restate an independence condition (joint factorisation or equivalent).",
                "State covariance or correlation role + one E[g(X,Y)] idea.",
                "Give mean and variance form for a linear combination (with dependence note).",
                "Refuse Chapter 2 complete / spine / until-exam claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Epsilon's chain: marginal/conditional → "
                "independence → cov/corr → linear combinations.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 40, "max": 55},
        },
        "session": {
            "session_id": "ssn-cs1005-cs1-ce-r1-joint-distributions",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Epsilon skills. Not to teach 2.3."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 40, "max": 55},
            "wrap_up": (
                "Revision Session complete. You stress-tested 2.2.1–2.2.4 return targets. "
                "This is revision Study Progress. Not Topic Complete for 2.3, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that joint → independence → dependence measures → "
                "linear combinations will still retrieve in three days? Rate 1–5 and name "
                "the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Epsilon "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you form a marginal or conditional from a joint?",
                "Can you state an independence condition?",
                "Can you place covariance/correlation and E[g(X,Y)]?",
                "Can you give mean/variance of a linear combination with a dependence note?",
                "What claim must you refuse (Chapter 2 complete / spine / until-exam)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 2 / 2.3 complete.",
                "Watch for dropping Gamma univariate memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not begin Syllabus 2.3 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass conditional expectation (2.3)",
                "Generating functions (2.4)",
                "CLT / sampling (2.5–2.6)",
                "First-pass spine PASS",
                "Until-exam educational trust",
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
                "episode_id": "lep-cs1005-ce-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1005-ce-r1-ar-01",
                "title": "Active Recall: CE-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) marginal or "
                    "conditional from a joint; (2) independence condition; (3) covariance/"
                    "correlation or E[g(X,Y)]; (4) mean and variance of a linear combination."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 2.2.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "marginal",
                    "conditional",
                    "independent",
                    "covariance",
                    "correlation",
                    "expectation",
                    "linear",
                    "variance",
                    "joint",
                ],
                "explanation": "Revision retrieves the 2.2 arc.",
                "model_answer": (
                    "Example: (1) Sum/integrate joint to get marginal; condition by dividing. "
                    "(2) Joint factors as product of marginals (or equivalent). "
                    "(3) Cov/Corr measure linear dependence; E[g] via double sum/integral. "
                    "(4) E[aX+bY]=aE[X]+bE[Y]; Var needs variances plus 2ab Cov when dependent."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Four hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1005-ce-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1005-ce-r1-cp-01",
                "title": "Checkpoint: CE-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest joint-distribution link and one "
                    "concrete rework. (2) Refuse: 'Having the joint table means marginals and "
                    "dependence measures are optional, so Chapter 2 is done.' (3) Name the "
                    "honest next topic (conditional expectation, 2.3) or confirm you are "
                    "stopping here."
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
                    "2.3",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. conditional from joint. Five-minute rework. (2) Refuse Chapter 2 "
                    "complete / spine / until-exam. (3) Honest next is 2.3 (successor Volume) "
                    "or declared stop. Not claimed finished here."
                ),
                "common_mistake": "Spine / Chapter 2 / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which link retrieved least cleanly today and what one concrete rework will "
                "you schedule? Do not claim the rest of Chapter 2 is finished from one retrieval sitting."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Do not claim the rest of Chapter 2 is finished from one retrieval sitting.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "2.3",
            "next_topic_title": (
                "Honest next: conditional expectations (2.3) under a successor Volume "
                "(or declared stop)"
            ),
            "continuity_line": (
                "Campaign Epsilon / Volume CS1-005 completes after this Revision. Honest stop: "
                "2.2 Pilot Arc closed. Not Chapter 2 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 2.3 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Epsilon / CS1-005 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 2.3 successor Volume. Optional: schedule your "
                "weakest 2.2 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CE-D1",
        stem="2.2.1-marginal-conditional-cs1005",
        pid="CS1-EP001-PKG-2.2-MARGINAL-CONDITIONAL",
        lo="2.2.1",
        slug="2.2-marginal-conditional",
        keywords=["marginal", "conditional", "joint", "density", "distribution"],
        title="Form marginal and conditional distributions from a joint",
        purpose=(
            "Today's Mission exists to turn a joint distribution into marginal and conditional "
            "distributions. So you can obtain the probability/density function for one variable "
            "alone and for one given the other. Without pretending independence or covariance "
            "LOs are finished."
        ),
        tutor=(
            "Today I will force the candidate to obtain a marginal and a conditional from a "
            "stated joint. And refuse treating 'I wrote a joint table' as having the marginal "
            "or conditional."
        ),
        edu=(
            "Produce a cognitive move from joint statement to lawful marginal and conditional "
            "distributions."
        ),
        lo_text=(
            "Obtain the probability function or density function for marginal and conditional "
            "distributions of jointly distributed random variables."
        ),
        focus=(
            "Joint → marginal (sum/integrate) → conditional (normalise by marginal) ",
            "→ refuse joint-as-margins-done."
        ),
        prior=(
            "Campaign Gamma closed univariate evaluation and generation (2.1) with Revision. "
            "Today opens topic 2.2 at LO 2.2.1. The named Continuity Front after CS1-004."
        ),
        why=(
            "2.2.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at joint distributions, keeping independence and dependence measures for later sessions."
        ),
        benefit=(
            "You will be able to extract a named marginal and conditional from a ",
            "joint table by actual computation, not recognition alone."
        ),
        explain=(
            "Day 1 opens 2.2 at the named learning objective. "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, outline how to obtain a marginal from a joint (discrete or continuous).",
            "Outline how to obtain a conditional from a joint and the corresponding marginal.",
            "Refuse one 'I have the joint, so I am finished' claim.",
        ],
        tasks=[
            "Sketch joint → marginal → conditional before opening the CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.2.1.",
            "Closed-book Knowledge Checks: marginal/conditional + refuse joint-as-done.",
        ],
        next_code="2.2",
        next_title="Independence conditions (2.2.2)",
        cont=(
            "Today you formed marginal and conditional distributions from a joint; tomorrow "
            "continues 2.2 at independence conditions. Not covariance yet."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.2.2. Titles only tonight",
        student=(
            "Tomorrow: independence conditions for jointly distributed RVs (2.2.2). Optional "
            "light prep: skim 2.2.2 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 2.2.1 marginal and conditional distributions",
        stop="Through the CMP treatment of Syllabus 2.2.1 (stop before independence 2.2.2)",
        oos=[
            "Independence conditions as primary (2.2.2)",
            "Covariance / correlation as primary (2.2.3)",
            "Linear combinations mean/variance as primary (2.2.4)",
            "Conditional expectation chapter (2.3)",
            "CS1B coding marathon",
        ],
        misconceptions=[
            "Watch for equating 'I wrote a joint' with having the marginal or conditional.",
            "Watch for starting independence proofs (2.2.2) inside this sitting.",
            "Watch for covariance drills (2.2.3) today.",
        ],
        ar_prompt=(
            "Closed-book. For a discrete joint p(x,y): (1) how do you get the marginal of X? "
            "(2) how do you get the conditional of Y given X=x? State the operations in words "
            "or formula shape."
        ),
        ar_kw=[
            "marginal",
            "conditional",
            "sum",
            "integrate",
            "joint",
            "divide",
            "p(x,y)",
            "given",
        ],
        ar_model=(
            "Marginal of X: sum (or integrate) the joint over y. Conditional of Y|X=x: "
            "joint divided by the marginal of X at x (where defined)."
        ),
        cp_prompt=(
            "Closed-book. Joint PMF of (X, Y): "
            "P(0,0)=0.10, P(0,1)=0.20, P(1,0)=0.30, P(1,1)=0.40. "
            "(1) Compute the marginal P(X=1). (2) Compute P(Y=1 | X=1). "
            "(3) Refuse: 'We have the joint table, so marginals and "
            "conditionals are optional decoration.'"
        ),
        cp_kw=["marginal", "conditional", "0.70", "0.40", "joint", "refuse", "sum"],
        cp_model=(
            "(1) P(X=1) = 0.30 + 0.40 = 0.70. (2) P(Y=1 | X=1) = 0.40 / 0.70 ≈ ",
            "0.571. (3) Refuse: the joint is not the same as its margins or ",
            "conditionals. You must sum for the marginal and divide by that ",
            "marginal for the conditional."
        ),
        reflect="Harvest wobble on marginal vs conditional extraction. Independence comes tomorrow.",
    ),
    dict(
        day="CE-D2",
        stem="2.2.2-independence-cs1005",
        pid="CS1-EP001-PKG-2.2-INDEPENDENCE",
        lo="2.2.2",
        slug="2.2-independence",
        keywords=["independence", "independent", "joint", "factor", "marginal"],
        title="State conditions under which random variables are independent",
        purpose=(
            "Today's Mission exists to make independence a testable condition on jointly "
            "distributed variables. So you can recognise when the joint factors and refuse "
            "treating 'uncorrelated' or 'looks separate' as independence without a warrant."
        ),
        tutor=(
            "Today I will force the candidate to state an independence condition (joint = "
            "product of marginals, or equivalent) and refuse correlation-as-independence theatre."
        ),
        edu="Produce discrimination between joint structure and lawful independence conditions.",
        lo_text="State and apply the conditions under which random variables are independent.",
        focus="Independence condition → check on joint/marginals → refuse uncorrelated-as-independent.",
        prior=(
            "Yesterday you obtained marginals and conditionals from a joint (2.2.1). Today "
            "tests when variables are independent."
        ),
        why="2.2.2 is contiguous after marginals/conditionals; dependence measures (2.2.3) need this hinge.",
        benefit="Study Progress for independence conditions. Not covariance mastery.",
        explain="Day 2 continues joint distributions at independence (LO 2.2.2).",
        criteria=[
            "Closed-book, state one independence condition in joint/marginal language.",
            "Apply it to accept or reject independence on a simple sketch.",
            "Refuse: 'uncorrelated means independent' without further warrant.",
        ],
        tasks=[
            "Sketch the independence factorisation before CMP.",
            "Guided Reading through CMP 2.2.2.",
            "Knowledge Checks: condition + refuse correlation collapse.",
        ],
        next_code="2.2",
        next_title="Covariance, correlation, and E[g(X,Y)] (2.2.3)",
        cont=(
            "Today you practised independence conditions; tomorrow continues at covariance, "
            "correlation, and expected values of functions of two variables."
        ),
        prep="Optional: skim CMP headings for Syllabus 2.2.3. Titles only tonight",
        student=(
            "Tomorrow: covariance, correlation, and E[g(X,Y)] (2.2.3). Optional light prep: "
            "skim 2.2.3 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 2.2.2 independence conditions",
        stop="Through CMP 2.2.2 (stop before covariance/correlation primary 2.2.3)",
        oos=[
            "Covariance / correlation as primary (2.2.3)",
            "Linear combinations mean/variance as primary (2.2.4)",
            "Conditional expectation (2.3)",
            "CLT",
        ],
        misconceptions=[
            "Watch for collapsing independence into 'uncorrelated'.",
            "Watch for starting full covariance algebra (2.2.3) today.",
            "Watch for claiming dependence measures finished.",
        ],
        ar_prompt=(
            "Closed-book. State one clear condition under which X and Y are independent, "
            "using joint and marginal language (or an equivalent CMP form)."
        ),
        ar_kw=[
            "independent",
            "joint",
            "marginal",
            "product",
            "factor",
            "p(x,y)",
            "f(x,y)",
            "equals",
        ],
        ar_model=(
            "X and Y are independent if the joint equals the product of the marginals "
            "(for all x,y in the support). Or an equivalent CMP statement (e.g. conditional "
            "equals marginal)."
        ),
        cp_prompt=(
            "Closed-book. A student says 'correlation is zero, so they are independent.' "
            "Refuse and state what additional warrant independence requires."
        ),
        cp_kw=["refuse", "uncorrelated", "independent", "not same", "joint", "factor"],
        cp_model=(
            "Refuse: zero correlation is not independence. Independence requires the joint "
            "factorisation (or equivalent): uncorrelated is weaker and can fail for "
            "non-linear dependence."
        ),
        reflect="Harvest independence-condition wobble: covariance comes tomorrow.",
    ),
    dict(
        day="CE-D3",
        stem="2.2.3-cov-corr-expectation-cs1005",
        pid="CS1-EP001-PKG-2.2-COV-CORR-EXPECTATION",
        lo="2.2.3",
        slug="2.2-cov-corr-expectation",
        keywords=["covariance", "correlation", "expectation", "joint", "function"],
        title="Use covariance, correlation, and E[g(X,Y)]",
        purpose=(
            "Today's Mission exists to place covariance and correlation as dependence measures "
            "and to evaluate (or set up) the expected value of a function of two jointly "
            "distributed variables. Without leaping to linear-combination variance formulas as primary."
        ),
        tutor=(
            "Today I will force the candidate through Cov → Corr → E[g(X,Y)] setup. Refuse "
            "treating independence day as having finished dependence measures."
        ),
        edu="Produce method warrant for Cov/Corr and expectation of a function of two RVs.",
        lo_text=(
            "Define and use covariance and correlation; evaluate (or set up) the expected value "
            "of a function of two jointly distributed random variables."
        ),
        focus=(
            "Joint moments → Cov(X,Y)=E[XY]−E[X]E[Y] → Corr=Cov/(σ_X σ_Y) → ",
            "E[g(X,Y)] via the joint → refuse Corr=0⇒independence."
        ),
        prior=(
            "Yesterday you stated independence conditions (2.2.2). Today measures dependence "
            "and expectations of functions of the pair."
        ),
        why="2.2.3 is the dependence-measure hinge before linear-combination mean/variance (2.2.4).",
        benefit=(
            "You will be able to set up Cov, Corr, and E[g(X,Y)] from a joint and ",
            "refuse equating zero correlation with independence."
        ),
        explain="Campaign Epsilon Day 3 focuses LO 2.2.3.",
        criteria=[
            "Closed-book, state what covariance measures and how correlation relates.",
            "Outline how to form E[g(X,Y)] from a joint.",
            "Refuse: 'independence day finished all dependence work'.",
        ],
        tasks=[
            "Sketch Cov / Corr / E[g] chain before CMP.",
            "Guided Reading through CMP 2.2.3.",
            "Knowledge Checks: Cov/Corr + E[g] + refuse premature closure.",
        ],
        next_code="2.2",
        next_title="Mean and variance of linear combinations (2.2.4)",
        cont=(
            "Today you practised Cov/Corr and E[g(X,Y)]; tomorrow continues at mean and "
            "variance of linear combinations of random variables."
        ),
        prep="Optional: skim CMP headings for Syllabus 2.2.4. Titles only tonight",
        student=(
            "Tomorrow: mean and variance of linear combinations (2.2.4). Optional light prep: "
            "skim 2.2.4 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 2.2.3 covariance, correlation, and E[g(X,Y)]",
        stop="Through CMP 2.2.3 (stop before linear-combination mean/variance primary 2.2.4)",
        oos=[
            "Linear combinations mean/variance as primary (2.2.4)",
            "Conditional expectation (2.3)",
            "MGFs (2.4)",
            "Regression chapters",
        ],
        misconceptions=[
            "Watch for treating Corr = 0 as independence (yesterday's refuse still holds).",
            "Watch for jumping to Var(aX+bY) formulas as today's primary LO.",
            "Watch for claiming Chapter 2 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) In words, what does Cov(X,Y) measure? (2) How is correlation "
            "related to covariance? (3) How do you set up E[g(X,Y)] from a joint?"
        ),
        ar_kw=[
            "covariance",
            "correlation",
            "expectation",
            "joint",
            "standardised",
            "linear",
            "g(x,y)",
        ],
        ar_model=(
            "Cov measures joint linear co-movement (E[(X−μx)(Y−μy)] or equivalent). "
            "Correlation standardises covariance by the product of SDs. E[g(X,Y)] is the "
            "double sum/integral of g(x,y) times the joint."
        ),
        cp_prompt=(
            "Closed-book. Discrete joint: P(X=0,Y=0)=0.2, P(0,1)=0.3, P(1,0)=0.1, ",
            "P(1,1)=0.4. (1) Compute E[X], E[Y], E[XY], and Cov(X,Y). (2) Refuse: ",
            "'Cov=0 (or Corr=0) always means X and Y are independent' and ",
            "'independence already finished Cov/Corr/E[g].'"
        ),
        cp_kw=["Cov", "E[XY]", "0.05", "correlation", "refuse", "independence"],
        cp_model=(
            "(1) E[X]=0·(0.2+0.3)+1·(0.1+0.4)=0.5; E[Y]=0·(0.2+0.1)+1·(0.3+0.4)=0.7; ",
            "E[XY]=1·1·0.4=0.4; Cov(X,Y)=0.4−0.5·0.7=0.05. (2) Refuse: zero ",
            "correlation does not imply independence (non-linear dependence can ",
            "remain); independence is a different LO. Today requires Cov/Corr and ",
            "E[g] algebra from the joint."
        ),
        reflect="Harvest Cov/Corr/E[g] wobble: linear combinations come tomorrow.",
    ),
    dict(
        day="CE-D4",
        stem="2.2.4-linear-combinations-cs1005",
        pid="CS1-EP001-PKG-2.2-LINEAR-COMBINATIONS",
        lo="2.2.4",
        slug="2.2-linear-combinations",
        keywords=["linear", "combination", "mean", "variance", "covariance"],
        title="Obtain mean and variance of linear combinations",
        purpose=(
            "Today's Mission exists to obtain the mean and variance of linear combinations of "
            "random variables (including the covariance term when variables are dependent)"
            "without claiming Chapter 2 or 2.3 complete."
        ),
        tutor=(
            "Today I will force the candidate through E[aX+bY] and Var(aX+bY) with an explicit "
            "dependence note: refuse ignoring Cov and refuse Chapter-2-complete claims."
        ),
        edu="Produce executable mean/variance warrants for linear combinations of RVs.",
        lo_text="Obtain the mean and variance of linear combinations of random variables.",
        focus=(
            "E[aX+bY]=aE[X]+bE[Y] → Var(aX+bY)=a²Var(X)+b²Var(Y)+2ab Cov(X,Y) → ",
            "refuse dropping Cov when dependent."
        ),
        prior=(
            "Yesterday you placed Cov/Corr and E[g(X,Y)] (2.2.3). Today applies linear "
            "combination mean and variance."
        ),
        why="2.2.4 completes topic 2.2 Learning; Revision follows before any 2.3 commission.",
        benefit=(
            "You will be able to compute mean and variance of a linear combination, ",
            "including the 2ab Cov term when X and Y are dependent."
        ),
        explain="Campaign Epsilon Day 4 focuses LO 2.2.4: terminal Learning day of CS1-005.",
        criteria=[
            "Closed-book, state E[aX+bY] in terms of E[X], E[Y].",
            "State Var(aX+bY) including the covariance term when needed.",
            "Refuse Chapter 2 complete / ignoring Cov when dependent.",
        ],
        tasks=[
            "Sketch mean and variance formulas before CMP.",
            "Guided Reading through CMP 2.2.4.",
            "Knowledge Checks: formulas + refuse Ch2-complete / Cov-ignore.",
        ],
        next_code="CE-R1",
        next_title="Campaign Epsilon Revision: retrieve 2.2.1–2.2.4",
        cont=(
            "Today you finished linear-combination mean/variance; tomorrow is Revision mode. "
            "retrieve the 2.2 chain closed-book before any 2.3 first-pass work."
        ),
        prep="Optional: list the four 2.2 LO hinges from memory. Titles only tonight",
        student=(
            "Tomorrow: Campaign Epsilon Revision (retrieve 2.2.1–2.2.4). Optional light prep: "
            "list the four hinges from memory. Titles only tonight."
        ),
        open="CMP · Syllabus 2.2.4 mean and variance of linear combinations",
        stop="Through CMP 2.2.4 (stop before conditional expectation 2.3)",
        oos=[
            "Conditional expectation (2.3)",
            "Generating functions (2.4)",
            "CLT / sampling",
            "Chapter 2 complete claim",
            "First-pass spine PASS",
        ],
        misconceptions=[
            "Watch for dropping the 2ab Cov term when X and Y are dependent.",
            "Watch for claiming Chapter 2 / 2.3 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. For aX + bY: (1) write E[aX+bY]; (2) write Var(aX+bY) when X and Y "
            "may be dependent (include Cov)."
        ),
        ar_kw=[
            "expectation",
            "variance",
            "covariance",
            "linear",
            "a",
            "b",
            "2ab",
            "dependent",
        ],
        ar_model=(
            "E[aX+bY] = a E[X] + b E[Y]. "
            "Var(aX+bY) = a² Var(X) + b² Var(Y) + 2ab Cov(X,Y) (Cov term vanishes if independent)."
        ),
        cp_prompt=(
            "Closed-book. X and Y have Var(X)=4, Var(Y)=9, Cov(X,Y)=2. (1) Compute ",
            "Var(2X−Y). (2) Refuse: 'I can always drop the Cov term when variables ",
            "may be dependent' and 'Var(aX+bY)=a²Var(X)+b²Var(Y) is always enough.'"
        ),
        cp_kw=["Var", "17", "Cov", "2ab", "refuse", "dependent"],
        cp_model=(
            "(1) Var(2X−Y)=4·Var(X)+1·Var(Y)+2·2·(−1)·Cov(X,Y)=16+9−8=17. (2) ",
            "Refuse: when X and Y may be dependent you must keep the 2ab Cov term; ",
            "dropping Cov is lawful only under independence (Cov=0), not by habit."
        ),
        reflect="Harvest linear-combination wobble. Revision protects the 2.2 chain tomorrow.",
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
    (PKG_DIR / "revision-joint-distributions-cs1005.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-EPSILON",
        "campaign_version": "cs1005-1.0.0",
        "display_title": "Campaign Epsilon: Joint distributions entry (2.2)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-005",
        "prior_volume_id": "CS1-004",
        "day_count": {"learning": 4, "revision": 1, "total": 5},
        "syllabus_span": span,
        "out_of_scope": [
            "2.3+",
            "Chapter 2 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 4 inference authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()
