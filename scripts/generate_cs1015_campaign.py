#!/usr/bin/env python3
"""Generate CS1-015 / Campaign Omicron educational packages (catalogue only).

Continuity Front join Pilot Arc for Topic 5.1 (Bayesian statistics).
Topic 5.1 is already Published+LIVE via Trust Front CS1-003/Delta — Omicron uses
distinct package IDs and must not be copied to educational_packages/ in this cycle.
Published Coverage and Student Reliance are unchanged by catalogue authoring.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-omicron-cs1015"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1015-campaign-omicron-1.0.0",
    "publication_version": "cs1015-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-OMICRON",
    "volume_id": "CS1-015",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1015_EDUCATIONAL_VOLUME.md",
        "CS1015_CERTIFICATION_REPORT.md",
        "EP013_WAVE13_PLAN.md",
    ],
    "author_id": "cs1015-educational-author",
    "authored_at": "2026-08-03",
}

TOPIC = {
    "topic_code": "5.1",
    "topic_title": (
        "Explain fundamental concepts of Bayesian statistics and use these concepts "
        "to calculate Bayesian estimators"
    ),
    "topic_id": "CS1-E-T01",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "5.1", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1015-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1015-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1015-cs1-{d['slug']}",
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
                f"for later 5.1 LOs, whole-Delta absorb, first-pass spine PASS, or "
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
                "episode_id": f"lep-cs1015-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1015-{lo}-ar-01",
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
                "episode_id": f"lep-cs1015-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1015-{lo}-cp-01",
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
            "returns_on": "CO-R1",
            "campaign_revision_package": "CS1-EP001-PKG-REV-BAYESIAN-OMICRON",
            "note": f"Syllabus {lo} is a CO-R1 return target after Learning span closes.",
        },
    }


def revision_pkg() -> dict:
    day = "CO-R1"
    pid = "CS1-EP001-PKG-REV-BAYESIAN-OMICRON"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Omicron revision: Bayesian statistics",
        "return_targets": [
            "5.1.1",
            "5.1.2",
            "5.1.3",
            "5.1.4",
            "5.1.5",
            "5.1.6",
            "5.1.7",
            "5.1.8",
            "5.1.9",
        ],
        "topic_aliases": [day, "campaign-omicron-revision"],
        "topic_title_keywords": [
            "revision",
            "Bayesian",
            "prior",
            "posterior",
            "credible",
            "credibility",
            "Empirical Bayes",
        ],
        "golden_id": "GOLDEN-CS1015-CS1-CO-R1-BAYESIAN",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1015-cs1-co-r1-bayesian",
            "display_title": "Retrieve Bayesian hinges (5.1)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Omicron. Retrieving "
                "Bayes' theorem through Bayes vs EB contrast. So 5.1 does not evaporate "
                "before an honest stop / Wave 0 honesty / spine re-audit."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Omicron's Learning hinges. "
                "not a passive CMP re-read and not a spine PASS or until-exam claim."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: theorem → "
                "prior/posterior/conjugate → simple posterior → loss/estimators → credible "
                "intervals → premium/factor → Bayesian credibility → EB → contrast."
            ),
            "learning_objective": (
                "Retrieve and connect (1) Bayes' theorem, (2) prior/posterior/conjugate, "
                "(3) simple posterior, (4) loss-based estimators, (5) credible intervals, "
                "(6) credibility premium/factor, (7) Bayesian credibility, "
                "(8) Empirical Bayes, and (9) Bayes vs EB assumptions."
            ),
            "concept_focus": (
                "Campaign chain retrieval: theorem → prior language → posterior → loss → "
                "credible → premium → Bayesian credibility → EB → contrast."
            ),
            "prior_bridge": (
                "Yesterday you finished Bayes vs EB contrast (5.1.9). Today is Revision mode: "
                "return to 5.1.1–5.1.9 under closed-book retrieval. No new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects that chain before you stop."
            ),
            "expected_benefit": (
                "You'll confirm the Bayesian chain still retrieves. Theorem through credibility and Bayes vs EB."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the nine 5.1 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse treating one retrieval sitting as Topic mastery.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Omicron's chain from Bayes' theorem to contrast.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 50, "max": 75},
        },
        "session": {
            "session_id": "ssn-cs1015-cs1-co-r1-bayesian",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Omicron skills. Not to claim spine PASS."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 50, "max": 75},
            "wrap_up": (
                "Revision Session complete. You stress-tested 5.1.1–5.1.9 return targets. "
                "This is revision Study Progress. Not Topic Complete beyond 5.1, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that Bayesian hinges will still retrieve in three days? "
                "Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Omicron "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the nine 5.1 Learning hinges in order?",
                "Can you state theorem → prior → posterior → loss → credible → premium → Bayes → EB → contrast?",
                "What claim must you refuse (spine / until-exam / Wave 0 clearance)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming spine / until-exam / Wave 0 complete.",
                "Watch for dropping Xi GLM memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not claim spine PASS, "
                "until-exam trust, or Wave 0 clearance in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Wave 0 Approver honesty clearance",
                "Certified Educational Coverage increase from catalogue alone",
                "New first-pass LO beyond 5.1",
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
                "episode_id": "lep-cs1015-co-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1015-co-r1-ar-01",
                "title": "Active Recall: Omicron chain",
                "prompt": (
                    "Closed-book. List the nine 5.1 Learning hinges in order as short phrases "
                    "(theorem → … → contrast)."
                ),
                "response_type": "short_structured",
                "body": "Retrieve Campaign Omicron Learning span.",
                "hints": ["Start from Bayes' theorem.", "End at Bayes vs EB contrast."],
                "accepted_keywords": [
                    "Bayes",
                    "prior",
                    "posterior",
                    "loss",
                    "credible",
                    "premium",
                    "credibility",
                    "Empirical",
                    "contrast",
                ],
                "explanation": "Order retrieval for CO-R1.",
                "model_answer": (
                    "Theorem → prior/posterior/conjugate → simple posterior → loss/estimators → "
                    "credible intervals → premium/factor → Bayesian credibility → EB → contrast."
                ),
                "common_mistake": "Skipping mid-chain credibility or collapsing Bayes with EB.",
                "success_criteria": ["Nine hinges named in lawful order."],
            },
            {
                "episode_id": "lep-cs1015-co-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1015-co-r1-cp-01",
                "title": "Checkpoint: Bayesian revision honesty",
                "prompt": (
                    "Closed-book. A colleague says 'Contrasting Bayes and Empirical Bayes means "
                    "Topic 5.1 is exam-ready.' Refuse; name the weakest link on today's "
                    "Bayesian retrieval chain; name one concrete next rework (not a new topic)."
                ),
                "response_type": "short_structured",
                "body": "Refuse forbidden claims; harvest weakest link.",
                "hints": ["Refuse spine / until-exam / Wave 0 clearance.", "Name one rework."],
                "accepted_keywords": [
                    "refuse",
                    "spine",
                    "Wave 0",
                    "weakest",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) Name weakest hinge + five-minute rework. (2) Refuse spine PASS / "
                    "until-exam / Wave 0 clearance. (3) Honest next is declared stop or Wave 0 "
                    "honesty / spine re-audit. Not claimed finished here."
                ),
                "common_mistake": "Spine / until-exam / Wave 0 claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which Bayesian link retrieved least cleanly today. Theorem, "
                "prior/posterior/conjugate, loss/estimators, credible intervals, premium "
                "factors, credibility, EB, or Bayes-vs-EB contrast. And what one concrete "
                "rework will you schedule? Do not claim Topic 5.1 mastery from one retrieval "
                "sitting."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Do not claim Topic mastery from one retrieval sitting.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "stop",
            "next_topic_title": (
                "Honest next (declared stop / Wave 0 honesty / spine re-audit)"
                "not first-pass spine PASS"
            ),
            "continuity_line": (
                "Campaign Omicron / Volume CS1-015 completes after this Revision. Honest stop: "
                "5.1 Continuity Front join Pilot Arc closed. Not first-pass spine PASS; "
                "not until-exam trust; not Wave 0 Approver honesty clearance. Successor "
                "geography is Wave 0 honesty / spine re-audit under a later commission "
                "(or declared stop). CS1-003 Delta remains independent Trust Front LIVE inventory."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Omicron / CS1-015 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await Wave 0 honesty / spine re-audit. Optional: schedule "
                "your weakest 5.1 rework only."
            ),
        },
        "revision_linkage": {
            "returns_on": "CO-R1",
            "return_targets": [
                "5.1.1",
                "5.1.2",
                "5.1.3",
                "5.1.4",
                "5.1.5",
                "5.1.6",
                "5.1.7",
                "5.1.8",
                "5.1.9",
            ],
            "protect_prior_hinge": "Xi 4.2 as needed",
        },
    }


LEARNING = LEARNING = [
    dict(
        day="CO-D1",
        stem="5.1.1-bayes-theorem-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-BAYES-THEOREM",
        lo="5.1.1",
        slug="5.1-bayes-theorem",
        keywords=["Bayes", "theorem", "conditional", "probability"],
        title="Apply Bayes' theorem to simple conditionals",
        purpose="Today's Mission exists to apply Bayes' theorem to simple conditional probabilities. So Bayesian entry starts from theorem honesty, without pretending prior/posterior/conjugate (5.1.2) are finished.",
        tutor="Today I will force Bayes' theorem on simple conditionals and refuse 'Bayesian means credibility premium on day one'.",
        edu="Produce Bayes' theorem application as the Continuity Front join hinge from Xi GLM into Topic 5.1.",
        lo_text="Use Bayes' theorem to calculate simple conditional probabilities.",
        focus=(
            "Prior / base rate → likelihood of data → Bayes update → posterior "
            "probability → refuse inverse-probability confusion."
        ),
        prior="Campaign Xi closed generalised linear models (4.2) with Revision. Today opens Continuity Front join at Topic 5.1 LO 5.1.1. The next official syllabus topic after 4.2. Trust Front CS1-003 already holds LIVE 5.1 inventory independently; Omicron is the Continuity Front native Pilot Arc.",
        why="5.1.1 opens this stretch at the natural next learning objective. Close it to avoid a cliff at Bayesian entry, keeping prior/posterior for the following session.",
        benefit=(
            "You will be able to apply Bayes' theorem to compute a simple "
            "posterior probability and refuse inverse-probability errors."
        ),
        explain="Day 1 opens Bayesian foundations at Bayes' theorem. The natural next step after classical GLM.",
        criteria=["Closed-book, state Bayes' theorem in probability form for a simple case.", "Compute or outline one simple conditional update.", "Refuse one 'Bayesian starts at credibility premium' claim."],
        tasks=["Sketch Bayes' theorem before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.1.", "Closed-book Knowledge Checks: theorem + refuse prior swallow."],
        next_code="5.1",
        next_title="Prior, posterior and conjugate priors (5.1.2)",
        cont="Today you applied Bayes' theorem to simple conditionals; tomorrow continues 5.1 at prior, posterior and conjugate priors.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.2. Titles only tonight",
        student="Tomorrow: prior, posterior and conjugate priors (5.1.2). Optional light prep: skim 5.1.2 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.1 Bayes' theorem and simple conditional probabilities",
        stop="Through the CMP treatment of Syllabus 5.1.1 (stop before prior/posterior/conjugate primary 5.1.2)",
        oos=["Prior / posterior / conjugate as primary", "Credibility premium as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for equating Bayes' theorem with credibility premium.", "Watch for finishing prior/posterior on day one.", "Watch for claiming spine / until-exam from theorem practice."],
        ar_prompt="Closed-book. (1) State Bayes' theorem for events A and B. (2) What one simple conditional does 5.1.1 require you to update? (3) Name one reason this does not finish prior/posterior (5.1.2).",
        ar_kw=["Bayes", "conditional", "probability", "prior", "likelihood"],
        ar_model="Bayes' theorem updates P(A|B) from P(B|A), P(A), P(B). Today is theorem/conditionals. Prior/posterior/conjugate are tomorrow.",
        cp_prompt=(
            "Closed-book. Fraud screen: P(fraud)=0.02, P(flag|fraud)=0.90, "
            "P(flag|genuine)=0.05. A claim is flagged. (1) Compute P(fraud|flag) "
            "via Bayes. (2) Refuse: 'P(fraud|flag) equals P(flag|fraud)=0.90.'"
        ),
        cp_kw=["Bayes", "0.269", "base rate", "posterior", "refuse", "likelihood"],
        cp_model=(
            "(1) P(flag)=0.90·0.02 + 0.05·0.98 = 0.018 + 0.049 = 0.067. "
            "P(fraud|flag)=0.018/0.067 ≈ 0.269. (2) Refuse: that equates "
            "posterior with likelihood and ignores the base rate. Bayes "
            "multiplies prior × likelihood and normalises."
        ),
        reflect="Harvest Bayes' theorem wobble: prior/posterior opens tomorrow.",
    ),
    dict(
        day="CO-D2",
        stem="5.1.2-prior-posterior-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR",
        lo="5.1.2",
        slug="5.1-prior-posterior",
        keywords=["prior", "posterior", "conjugate"],
        title="Explain prior, posterior and conjugate priors",
        purpose="Today's Mission exists to explain prior, posterior and conjugate prior distributions. Without pretending simple posterior calculation (5.1.3) is finished.",
        tutor="Today I will force prior/posterior/conjugate vocabulary with warrants and refuse 'conjugate means I already calculated the posterior'.",
        edu="Produce prior/posterior/conjugate as the contiguous hinge after Bayes' theorem.",
        lo_text="Explain prior distribution, posterior distribution and conjugate prior distribution.",
        focus=(
            "Prior → likelihood → posterior; conjugate pairs keep the posterior "
            "in the same family."
        ),
        prior="Yesterday you applied Bayes' theorem (5.1.1). Today continues Topic 5.1 at prior, posterior and conjugate.",
        why="5.1.2 unlocks lawful language before simple posterior calculations (5.1.3).",
        benefit=(
            "You will be able to explain prior, posterior and conjugate prior "
            "distributions with a concrete pair."
        ),
        explain="Day 2 focuses the named learning objective. Join keeps after theorem entry.",
        criteria=["Closed-book, define prior, posterior and conjugate prior.", "Name one conjugate pair example from CMP.", "Refuse one 'I already finished the posterior calculation' claim."],
        tasks=["Sketch prior → posterior chain before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.2.", "Closed-book Knowledge Checks: definitions + refuse calc swallow."],
        next_code="5.1",
        next_title="Posterior distribution in simple cases (5.1.3)",
        cont="Today you explained prior, posterior and conjugate; tomorrow continues 5.1 at posterior in simple cases.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.3. Titles only tonight",
        student="Tomorrow: posterior distribution for a parameter in simple cases (5.1.3). Optional light prep: skim 5.1.3 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.2 prior, posterior, conjugate prior",
        stop="Through the CMP treatment of Syllabus 5.1.2 (stop before simple posterior calculation primary 5.1.3)",
        oos=["Simple posterior calculation as primary", "Loss functions as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for treating conjugate as automatic posterior finished.", "Watch for skipping prior honesty.", "Watch for swallowing 5.1.3 calculation."],
        ar_prompt="Closed-book. (1) Define prior and posterior. (2) What makes a prior conjugate? (3) Why does naming conjugate not finish 5.1.3?",
        ar_kw=["prior", "posterior", "conjugate", "likelihood"],
        ar_model="Prior encodes belief before data; posterior after. Conjugate priors keep posterior in the same family. Calculation of a simple posterior is tomorrow.",
        cp_prompt=(
            "Closed-book. (1) In one sentence each, define prior, posterior, and "
            "conjugate prior. Name one conjugate pair used in actuarial "
            "modelling. (2) Refuse: 'Naming a conjugate pair finishes obtaining "
            "the numerical posterior for a parameter.'"
        ),
        cp_kw=["prior", "posterior", "conjugate", "Beta", "Binomial", "refuse"],
        cp_model=(
            "(1) Prior: belief about θ before data. Posterior: updated belief "
            "after data. Conjugate: a prior family closed under updating so the "
            "posterior stays in the same family. Example: Beta–Binomial or "
            "Gamma–Poisson. (2) Refuse: conjugate language structures the update; "
            "you still must obtain the actual posterior (parameters/distribution) "
            "from prior + data."
        ),
        reflect="Harvest prior/posterior wobble: simple posterior calc opens tomorrow.",
    ),
    dict(
        day="CO-D3",
        stem="5.1.3-posterior-simple-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE",
        lo="5.1.3",
        slug="5.1-posterior-simple",
        keywords=["posterior", "parameter", "simple"],
        title="Obtain posteriors in simple cases",
        purpose="Today's Mission exists to obtain the posterior for a parameter in simple cases. Without pretending loss-based estimators (5.1.4) are finished.",
        tutor="Today I will force a simple posterior calculation path and refuse 'posterior means point estimate under loss'.",
        edu="Produce simple posterior calculation as contiguous after prior/conjugate language.",
        lo_text="Obtain the posterior distribution for a parameter in simple cases.",
        focus="Prior + data → posterior distribution in a simple conjugate case.",
        prior="Yesterday you explained prior/posterior/conjugate (5.1.2). Today calculates a simple posterior.",
        why="5.1.3 is the calculation hinge before loss-based estimators (5.1.4).",
        benefit=(
            "You will be able to obtain the posterior distribution for a "
            "parameter in a simple conjugate case."
        ),
        explain="Day 3 continues Bayesian foundations. Calculation after vocabulary.",
        criteria=["Closed-book, outline steps to obtain a simple posterior.", "Name the object obtained (distribution, not yet loss estimate).", "Refuse one loss-function swallow."],
        tasks=["Sketch posterior update before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.3.", "Closed-book Knowledge Checks: posterior steps + refuse loss swallow."],
        next_code="5.1",
        next_title="Loss functions and Bayesian estimators (5.1.4)",
        cont="Today you obtained a simple posterior; tomorrow continues 5.1 at loss functions and Bayesian estimators.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.4. Titles only tonight",
        student="Tomorrow: loss functions and Bayesian estimators (5.1.4). Optional light prep: skim 5.1.4 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.3 posterior distribution for a parameter in simple cases",
        stop="Through the CMP treatment of Syllabus 5.1.3 (stop before loss/estimators primary 5.1.4)",
        oos=["Loss functions / Bayesian estimators as primary", "Credible intervals as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for collapsing posterior into a single point estimate under loss.", "Watch for skipping distributional warrant.", "Watch for swallowing 5.1.4."],
        ar_prompt="Closed-book. (1) What inputs yield a simple posterior? (2) What object do you obtain? (3) Why is a loss-based point estimate not today's primary?",
        ar_kw=["posterior", "prior", "likelihood", "parameter", "distribution"],
        ar_model="Prior and likelihood yield a posterior distribution for the parameter. Loss-based estimators are tomorrow.",
        cp_prompt=(
            "Closed-book. Binomial n=10 with x=3 successes and Beta(2,2) prior. "
            "(1) State the posterior distribution (parameters). (2) Refuse: "
            "'Having the posterior distribution finishes choosing the Bayesian "
            "point estimator under squared-error loss.'"
        ),
        cp_kw=["Beta(5,9)", "posterior", "refuse", "squared-error", "estimator"],
        cp_model=(
            "(1) Posterior Beta(2+3, 2+7) = Beta(5,9). (2) Refuse: the posterior "
            "is the full distribution; a loss-based point estimator (e.g. "
            "posterior mean under squared-error loss) is a further step."
        ),
        reflect="Harvest posterior-calc wobble: loss/estimators open tomorrow.",
    ),
    dict(
        day="CO-D4",
        stem="5.1.4-loss-estimators-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS",
        lo="5.1.4",
        slug="5.1-loss-estimators",
        keywords=["loss", "estimator", "Bayesian", "squared"],
        title="Derive Bayesian estimators from simple loss functions",
        purpose="Today's Mission exists to derive Bayesian estimates from simple loss functions. Without pretending credible intervals (5.1.5) are finished.",
        tutor="Today I will force loss → estimator mapping and refuse 'estimator equals credible interval'.",
        edu="Produce loss-based Bayesian estimators as contiguous after simple posterior.",
        lo_text="Use simple loss functions to derive Bayesian estimates of parameters.",
        focus=(
            "Loss function → Bayesian point estimator (mean / median) → refuse "
            "conflating with credible intervals."
        ),
        prior="Yesterday you obtained a simple posterior (5.1.3). Today derives estimators under simple loss.",
        why="5.1.4 precedes credible intervals (5.1.5).",
        benefit=(
            "You will be able to derive Bayesian point estimators from simple "
            "loss functions."
        ),
        explain="Day 4 continues Bayesian foundations. Estimator after posterior.",
        criteria=["Closed-book, name at least two simple loss functions and their estimator link.", "State that today's object is a point estimate under loss.", "Refuse one credible-interval swallow."],
        tasks=["Sketch loss → estimator before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.4.", "Closed-book Knowledge Checks: loss/estimator + refuse interval swallow."],
        next_code="5.1",
        next_title="Credible intervals in simple cases (5.1.5)",
        cont="Today you derived Bayesian estimators under simple loss; tomorrow continues 5.1 at credible intervals.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.5. Titles only tonight",
        student="Tomorrow: credible intervals in simple cases (5.1.5). Optional light prep: skim 5.1.5 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.4 loss functions and Bayesian estimators",
        stop="Through the CMP treatment of Syllabus 5.1.4 (stop before credible intervals primary 5.1.5)",
        oos=["Credible intervals as primary", "Credibility premium as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for equating Bayesian estimator with credible interval.", "Watch for forgetting loss choice matters.", "Watch for swallowing 5.1.5."],
        ar_prompt="Closed-book. (1) Name two simple loss functions. (2) What estimator does each typically justify? (3) Why are credible intervals not today's primary?",
        ar_kw=["loss", "squared", "absolute", "estimator", "posterior"],
        ar_model="Squared/absolute (and similar) loss map to posterior mean/median-type estimators as taught. Credible intervals are tomorrow.",
        cp_prompt=(
            "Closed-book. Posterior for θ is available. (1) Under squared-error "
            "loss, what Bayesian point estimator do you use, and under "
            "absolute-error loss? (2) Refuse: 'The Bayesian point estimator under "
            "loss is the same object as a credible interval.'"
        ),
        cp_kw=["posterior mean", "median", "squared-error", "refuse", "credible"],
        cp_model=(
            "(1) Squared-error loss → posterior mean; absolute-error loss → "
            "posterior median. (2) Refuse: a point estimator summarises the "
            "posterior under a loss; a credible interval is a posterior "
            "probability set for θ: different objects."
        ),
        reflect="Harvest loss/estimator wobble: credible intervals open tomorrow.",
    ),
    dict(
        day="CO-D5",
        stem="5.1.5-credible-intervals-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS",
        lo="5.1.5",
        slug="5.1-credible-intervals",
        keywords=["credible", "interval", "posterior"],
        title="Construct credible intervals in simple cases",
        purpose="Today's Mission exists to construct credible intervals in simple cases. Without pretending credibility premium (5.1.6) is finished.",
        tutor="Today I will force credible-interval construction from the posterior and refuse 'credible equals confidence interval under frequentist law'.",
        edu="Produce credible intervals as contiguous after loss-based estimators.",
        lo_text="Construct credible intervals in simple cases.",
        focus=(
            "Posterior → credible interval construction → refuse copying "
            "frequentist CI coverage slogans."
        ),
        prior="Yesterday you derived loss-based estimators (5.1.4). Today constructs credible intervals.",
        why="5.1.5 completes core Bayesian estimation objects before credibility theory.",
        benefit=(
            "You will be able to construct a credible interval in a simple case "
            "and interpret it as a posterior probability statement."
        ),
        explain="Day 5 continues Bayesian foundations. Intervals after estimators.",
        criteria=["Closed-book, state what a credible interval asserts about the parameter.", "Outline construction in a simple case.", "Refuse one credibility-premium swallow."],
        tasks=["Sketch credible-interval idea before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.5.", "Closed-book Knowledge Checks: interval + refuse premium swallow."],
        next_code="5.1",
        next_title="Credibility premium formula and factor (5.1.6)",
        cont="Today you constructed credible intervals; tomorrow continues 5.1 at credibility premium and factor.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.6. Titles only tonight",
        student="Tomorrow: credibility premium formula and credibility factor (5.1.6). Optional light prep: skim 5.1.6 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.5 credible intervals in simple cases",
        stop="Through the CMP treatment of Syllabus 5.1.5 (stop before credibility premium primary 5.1.6)",
        oos=["Credibility premium as primary", "Empirical Bayes as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for equating credible and confidence intervals without warrant.", "Watch for finishing credibility premium today.", "Watch for swallowing 5.1.6."],
        ar_prompt="Closed-book. (1) What does a credible interval say? (2) What posterior object do you use? (3) Why is credibility premium not today's primary?",
        ar_kw=["credible", "interval", "posterior", "probability"],
        ar_model="A credible interval is a posterior probability statement for the parameter. Credibility premium formula is tomorrow.",
        cp_prompt=(
            "Closed-book. Posterior for a risk parameter θ is Normal(0.10, "
            "0.02²). (1) Construct an approximate 95% equal-tailed credible "
            "interval for θ. (2) Refuse: 'A 95% credible interval means that in "
            "repeated samples the random interval covers θ 95% of the time' "
            "without noting the Bayesian reading."
        ),
        cp_kw=["0.0608", "0.1392", "credible", "posterior", "refuse", "confidence"],
        cp_model=(
            "(1) ≈ 0.10 ± 1.96·0.02 → about (0.0608, 0.1392). (2) Refuse: that is "
            "the frequentist coverage slogan for a confidence interval; a "
            "credible interval is a posterior probability statement about θ given "
            "the data."
        ),
        reflect="Harvest credible-interval wobble: credibility premium opens tomorrow.",
    ),
    dict(
        day="CO-D6",
        stem="5.1.6-credibility-premium-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM",
        lo="5.1.6",
        slug="5.1-credibility-premium",
        keywords=["credibility", "premium", "factor"],
        title="Use the credibility premium formula and factor",
        purpose="Today's Mission exists to use the credibility premium formula and credibility factor. Without pretending Bayesian credibility approach (5.1.7) is finished.",
        tutor="Today I will force premium = Z·mean + (1−Z)·collateral structure and refuse 'Z finished Bayesian credibility theory'.",
        edu="Produce credibility premium/factor as the entry to credibility theory after Bayesian estimation objects.",
        lo_text="Use the credibility premium formula and explain the role of the credibility factor.",
        focus=(
            "Individual experience + collateral mean → credibility factor Z → "
            "credibility premium."
        ),
        prior="Yesterday you constructed credible intervals (5.1.5). Today opens credibility theory at the premium formula.",
        why="5.1.6 opens credibility theory before Bayesian vs EB approaches.",
        benefit=(
            "You will be able to compute a credibility premium and explain the "
            "role of the credibility factor Z."
        ),
        explain="Day 6 continues Bayesian foundations. Premium formula before approach LO.",
        criteria=["Closed-book, write the credibility premium formula with Z.", "State what Z balances.", "Refuse one 'Bayesian credibility finished today' claim."],
        tasks=["Sketch premium formula before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.6.", "Closed-book Knowledge Checks: formula + refuse 5.1.7 swallow."],
        next_code="5.1",
        next_title="Bayesian approach to credibility (5.1.7)",
        cont="Today you used the credibility premium and factor; tomorrow continues 5.1 at Bayesian credibility.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.7. Titles only tonight",
        student="Tomorrow: Bayesian approach to credibility theory (5.1.7). Optional light prep: skim 5.1.7 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.6 credibility premium formula and credibility factor",
        stop="Through the CMP treatment of Syllabus 5.1.6 (stop before Bayesian credibility approach primary 5.1.7)",
        oos=["Bayesian credibility approach as primary", "Empirical Bayes as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for treating Z as always 1.", "Watch for finishing Bayesian credibility approach today.", "Watch for swallowing 5.1.7."],
        ar_prompt="Closed-book. (1) Write the credibility premium with Z. (2) What does Z weight? (3) Why is Bayesian credibility approach not today's primary?",
        ar_kw=["credibility", "premium", "Z", "factor", "collateral"],
        ar_model="Premium mixes individual experience and collateral mean via Z. Bayesian approach to credibility is tomorrow.",
        cp_prompt=(
            "Closed-book. Individual mean claim X̄ = 1200, collateral/manual mean "
            "μ = 1000, credibility factor Z = 0.4. (1) Compute the credibility "
            "premium and state what Z represents. (2) Refuse: 'Always use full "
            "credibility Z = 1.'"
        ),
        cp_kw=["1080", "Z", "credibility", "refuse", "full credibility"],
        cp_model=(
            "(1) Premium = Z·X̄ + (1−Z)·μ = 0.4·1200 + 0.6·1000 = 480 + 600 = "
            "1080. Z is the weight on the individual experience (versus the "
            "collateral mean). (2) Refuse: with limited or noisy data, Z < 1 "
            "shrinks toward the collateral/manual mean."
        ),
        reflect="Harvest premium/factor wobble. Bayesian credibility opens tomorrow.",
    ),
    dict(
        day="CO-D7",
        stem="5.1.7-bayesian-credibility-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY",
        lo="5.1.7",
        slug="5.1-bayesian-credibility",
        keywords=["Bayesian", "credibility", "premium"],
        title="Apply Bayesian credibility in simple cases",
        purpose="Today's Mission exists to apply the Bayesian approach to credibility in simple cases. Without pretending Empirical Bayes (5.1.8) is finished.",
        tutor="Today I will force Bayesian credibility premiums in simple cases and refuse 'Bayesian credibility finished Empirical Bayes'.",
        edu="Produce Bayesian credibility as contiguous after the premium formula.",
        lo_text="Apply the Bayesian approach to credibility theory and calculate credibility premiums in simple cases.",
        focus=(
            "Bayesian credibility with known structural/prior parameters → Z and "
            "μ → credibility premium."
        ),
        prior="Yesterday you used the credibility premium formula (5.1.6). Today applies the Bayesian approach.",
        why="5.1.7 precedes Empirical Bayes (5.1.8) contrast.",
        benefit=(
            "You will be able to apply the Bayesian approach to credibility and "
            "compute a premium in a simple case."
        ),
        explain="Day 7 continues Bayesian foundations. Bayesian approach before EB.",
        criteria=["Closed-book, outline Bayesian credibility inputs in a simple case.", "State how today's approach uses prior structure.", "Refuse one Empirical Bayes swallow."],
        tasks=["Sketch Bayesian credibility path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.7.", "Closed-book Knowledge Checks: Bayesian credibility + refuse EB swallow."],
        next_code="5.1",
        next_title="Empirical Bayes credibility (5.1.8)",
        cont="Today you applied Bayesian credibility; tomorrow continues 5.1 at Empirical Bayes.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.8. Titles only tonight",
        student="Tomorrow: Empirical Bayes approach to credibility (5.1.8). Optional light prep: skim 5.1.8 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.7 Bayesian approach to credibility theory",
        stop="Through the CMP treatment of Syllabus 5.1.7 (stop before Empirical Bayes primary 5.1.8)",
        oos=["Empirical Bayes as primary", "Bayes vs EB contrast as primary", "First-pass spine PASS", "Until-exam educational trust"],
        misconceptions=["Watch for equating Bayesian credibility with EB.", "Watch for finishing contrast LO today.", "Watch for swallowing 5.1.8."],
        ar_prompt="Closed-book. (1) What distinguishes the Bayesian credibility approach in simple cases? (2) What premium object do you calculate? (3) Why is EB not today's primary?",
        ar_kw=["Bayesian", "credibility", "prior", "premium"],
        ar_model="Bayesian credibility uses an explicit prior structure for risk parameters. Empirical Bayes is tomorrow.",
        cp_prompt=(
            "Closed-book. In a simple Bayesian credibility setup with known "
            "structural parameters, the credibility premium takes the form Z·X̄ + "
            "(1−Z)·μ. (1) What do the prior/structural assumptions supply that "
            "lets you compute Z and μ? (2) Refuse: 'Applying Bayesian credibility "
            "finishes the Empirical Bayes approach.'"
        ),
        cp_kw=["structural", "prior", "Z", "μ", "refuse", "Empirical Bayes"],
        cp_model=(
            "(1) The prior (or known structural distribution) supplies the "
            "overall mean and variance components so μ and Z are determined "
            "theoretically, then combined with observed X̄. (2) Refuse: Empirical "
            "Bayes estimates those structural parameters from data. A different "
            "approach from treating them as known in the Bayesian calculation."
        ),
        reflect="Harvest Bayesian-credibility wobble. EB opens tomorrow.",
    ),
    dict(
        day="CO-D8",
        stem="5.1.8-empirical-bayes-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES",
        lo="5.1.8",
        slug="5.1-empirical-bayes",
        keywords=["Empirical", "Bayes", "credibility"],
        title="Apply Empirical Bayes credibility in simple cases",
        purpose="Today's Mission exists to apply Empirical Bayes credibility in simple cases. Without pretending the Bayes vs EB contrast (5.1.9) is finished.",
        tutor="Today I will force EB credibility premiums in simple cases and refuse 'EB finished the contrast LO'.",
        edu="Produce Empirical Bayes credibility as contiguous after Bayesian credibility.",
        lo_text="Apply the Empirical Bayes approach to credibility theory and derive credibility premiums in simple cases.",
        focus=(
            "Estimate structural parameters from collective data → plug into "
            "credibility formula → EB premium."
        ),
        prior="Yesterday you applied Bayesian credibility (5.1.7). Today applies Empirical Bayes.",
        why="5.1.8 sets up the contrast LO 5.1.9.",
        benefit=(
            "You will be able to apply Empirical Bayes to estimate structural "
            "parameters and form a credibility premium."
        ),
        explain="Day 8 continues Bayesian foundations. EB before contrast.",
        criteria=["Closed-book, outline how EB uses data for structural parameters.", "State one EB premium move in a simple case.", "Refuse one contrast-finished claim."],
        tasks=["Sketch EB path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.8.", "Closed-book Knowledge Checks: EB + refuse contrast swallow."],
        next_code="5.1",
        next_title="Bayes vs Empirical Bayes differences (5.1.9)",
        cont="Today you applied Empirical Bayes credibility; tomorrow continues 5.1 at Bayes vs EB differences.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.9. Titles only tonight",
        student="Tomorrow: differences between Bayesian and Empirical Bayes approaches (5.1.9). Optional light prep: skim 5.1.9 headings. Titles only tonight.",
        open="CMP · Syllabus 5.1.8 Empirical Bayes approach to credibility",
        stop="Through the CMP treatment of Syllabus 5.1.8 (stop before contrast primary 5.1.9)",
        oos=["Bayes vs EB contrast as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for treating EB as identical to Bayesian credibility.", "Watch for finishing contrast today.", "Watch for swallowing 5.1.9."],
        ar_prompt="Closed-book. (1) How does EB obtain structural parameters differently from a fully specified Bayesian prior? (2) What premium do you derive? (3) Why is contrast not today's primary?",
        ar_kw=["Empirical", "Bayes", "credibility", "structural", "data"],
        ar_model="EB estimates structural parameters from data rather than a fully specified prior alone. Contrast LO is tomorrow.",
        cp_prompt=(
            "Closed-book. (1) Outline the Empirical Bayes move to obtain a "
            "credibility premium when structural parameters are unknown. (2) "
            "Refuse: 'Computing one EB premium finishes explaining how Bayesian "
            "and Empirical Bayes differ in assumptions.'"
        ),
        cp_kw=["Empirical Bayes", "structural", "estimate", "Ẑ", "refuse", "contrast"],
        cp_model=(
            "(1) Estimate structural parameters (e.g. overall mean and "
            "process/variance components) from the collective data, plug them "
            "into the credibility formula to get Ẑ and μ̂, then form Ẑ·X̄ + "
            "(1−Ẑ)·μ̂ for the risk. (2) Refuse: applying EB is not the same LO "
            "as contrasting the assumption sets of Bayes vs EB."
        ),
        reflect="Harvest EB wobble: contrast opens tomorrow.",
    ),
    dict(
        day="CO-D9",
        stem="5.1.9-bayes-vs-eb-cs1015",
        pid="CS1-EP001-PKG-CO-5.1-BAYES-VS-EB",
        lo="5.1.9",
        slug="5.1-bayes-vs-eb",
        keywords=["Bayes", "Empirical", "assumptions", "contrast"],
        title="Contrast Bayesian and Empirical Bayes assumptions",
        purpose="Today's Mission exists to contrast Bayesian and Empirical Bayes approaches and their assumptions. Without pretending first-pass spine PASS, until-exam trust, or Wave 0 clearance.",
        tutor="Today I will force Bayes vs EB assumption contrast and refuse 'Topic 5.1 finished the exam journey / first-pass spine'.",
        edu="Produce Bayes vs EB contrast as the Topic 5.1 Learning close before Revision.",
        lo_text="Understand the differences between Bayesian and Empirical Bayes approaches and the assumptions underlying each.",
        focus=(
            "Bayesian assumptions (prior/structural known in model) ↔ EB "
            "assumptions (structural parameters estimated from data)."
        ),
        prior="Yesterday you applied Empirical Bayes (5.1.8). Today closes Topic 5.1 Learning at the contrast.",
        why="Contrast Bayesian vs Empirical Bayes assumptions to close Bayesian foundations before revision.",
        benefit=(
            "You will be able to state how Bayesian and Empirical Bayes differ in "
            "assumptions and what each is entitled to claim."
        ),
        explain="Day 9 focuses the named learning objective (join closes Topic 5.1 Learning before Revision) not spine trophy.",
        criteria=["Closed-book, name at least two assumption differences between Bayes and EB.", "State one warrant why approaches can diverge.", "Refuse one spine / until-exam / Wave 0 clearance claim."],
        tasks=["Sketch contrast table before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.9.", "Closed-book Knowledge Checks: contrast + refuse spine swallow."],
        next_code="CO-R1",
        next_title="Campaign Omicron Revision: retrieve Bayesian hinges (5.1)",
        cont="Today you closed Topic 5.1 Learning at Bayes vs EB contrast; tomorrow is Campaign Omicron Revision returning to 5.1.1–5.1.9.",
        prep="No new LO tonight: rest or jot the stickiest 5.1 hinge for Revision",
        student="Tomorrow: CO-R1 Revision of 5.1. Optional: note your weakest 5.1 link. Titles only tonight.",
        open="CMP · Syllabus 5.1.9 Bayes vs Empirical Bayes differences and assumptions",
        stop="Through the CMP treatment of Syllabus 5.1.9 (stop before terminal Revision as Learning; no spine / until-exam claim)",
        oos=["First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance", "Certified Educational Coverage increase from catalogue alone", "New first-pass LO beyond 5.1"],
        misconceptions=["Watch for claiming spine / until-exam from contrast day.", "Watch for collapsing Bayes and EB as identical.", "Watch for skipping Revision."],
        ar_prompt="Closed-book. (1) Name two assumption differences Bayes vs EB. (2) Why might premiums differ? (3) Name one reason this does not finish first-pass spine or until-exam trust.",
        ar_kw=["Bayes", "Empirical", "assumption", "prior", "data"],
        ar_model="Bayes uses a specified prior structure; EB estimates structural parameters from data. Assumptions differ. Spine PASS and until-exam remain out of scope.",
        cp_prompt=(
            "Closed-book. (1) State one key assumption difference between a fully "
            "Bayesian credibility approach and Empirical Bayes. (2) Refuse: "
            "'Bayesian and Empirical Bayes are the same method with different "
            "names' and 'contrasting them means all of Topic 5.1 is finished.'"
        ),
        cp_kw=["Bayesian", "Empirical Bayes", "structural", "estimate", "refuse", "assumptions"],
        cp_model=(
            "(1) Bayesian treats structural/prior parameters as specified within "
            "a prior model; Empirical Bayes estimates those structural parameters "
            "from the observed collective data. (2) Refuse: they differ in how "
            "structural knowledge enters; a contrast does not replace the "
            "separate calculation LOs across Topic 5.1."
        ),
        reflect="Harvest contrast wobble. Revision protects the 5.1 chain tomorrow.",
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
    (PKG_DIR / "revision-bayesian-cs1015.json").write_text(json.dumps(rev, indent=2) + "\n")
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-OMICRON",
        "campaign_version": "cs1015-1.0.0",
        "display_title": (
            "Campaign Omicron. Bayesian statistics (5.1) · Continuity Front join"
        ),
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-015",
        "prior_volume_id": "CS1-014",
        "day_count": {"learning": 9, "revision": 1, "total": 10},
        "syllabus_span": span,
        "out_of_scope": [
            "first-pass spine PASS",
            "until-examination educational trust",
            "Trust Front whole-Delta absorb into Continuity Front credit",
            "Wave 0 Approver honesty clearance",
            "Wave 14 authoring",
            "coverage mirage / Student Reliance increase from catalogue alone",
            "LIVE copies in educational_packages/",
        ],
        "inventory": inventory,
        "trust_front_note": (
            "CS1-003 / Campaign Delta remains independent Trust Front LIVE inventory for "
            "4.1–5.1. Omicron package IDs are CO-prefixed Continuity Front join catalogue. "
            "not LIVE this cycle; Published Coverage unchanged (5.1 already counted)."
        ),
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()
