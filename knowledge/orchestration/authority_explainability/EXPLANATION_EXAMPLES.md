# Explanation Examples

**Programme:** VII — Workstream 2 — Educational Authority Engine  
**Milestone:** MS003 — Authority Decision Explainability  
**Classification:** Illustrative constitutional explanation patterns  
**Status:** APPROVED — governing as pattern law; examples are illustrative, not a closed product-copy catalogue  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document provides **illustrative constitutional explanation patterns** for authority decisions, delegations, and conflict resolutions.

Subordinate to:

1. [`AUTHORITY_DECISION_EXPLAINABILITY.md`](AUTHORITY_DECISION_EXPLAINABILITY.md)
2. [`EXPLANATION_PRINCIPLES.md`](EXPLANATION_PRINCIPLES.md)
3. [`EXPLANATION_COMPONENTS.md`](EXPLANATION_COMPONENTS.md)
4. [`EXPLANATION_BOUNDARIES.md`](EXPLANATION_BOUNDARIES.md)
5. [`../authority/`](../authority/)
6. [`../conflict_resolution/`](../conflict_resolution/)

> **Examples illustrate lawful shape.  
> They are not Runtime A copy, UI templates, or a scoring rubric.**

---

## 1. How to Read These Patterns

Each pattern includes:

| Section | Role |
|---------|------|
| **Situation** | Educational / constitutional setup |
| **Student speech** | Plain-language permission narrative (AEP-10) |
| **Developer trace** | Constitutional audit shape (AEC-01…AEC-10) |
| **AEQ coverage** | How AEQ1–AEQ4 are answered |
| **Unlawful contrast** | Narration that would cross AEB boundaries |

Patterns deliberately avoid binding product microcopy. Wording may vary; constitutional facts must not.

---

## 2. Pattern Catalogue

| ID | Pattern | Situation family |
|----|---------|------------------|
| **AXP-E01** | Ordinary authority decision | Single owner permitted; alternatives refused |
| **AXP-E02** | Delegated authority | AP-04 bounded exercise under standing owner |
| **AXP-E03** | Conflict resolution | CT concurrency → RP rules → RO dispositions |
| **AXP-E04** | Superseded recommendation | RO-02 action replacement; ownership intact |
| **AXP-E05** | Merged recommendations | RO-03 only with published merge pathway |

---

## 3. AXP-E01 — Ordinary Authority Decision

### Situation

The primary educational question is “what is most valuable *today* under the Canonical Study Plan?” Daily Coach (AD-02) owns the decision. Master Planner plan artefact is consumed. Recovery / Exam are not primary. No MS002 concurrency.

### Student speech (illustrative)

> “We’re choosing what is most useful for **today** under your Study Plan. Your day coach owns that choice. We’re **not** rewriting your long-term plan, and we’re **not** treating this as recovery coaching — ordinary daily focus is the question right now.”

### Developer trace (illustrative)

```
decision_class: today_primary_priority
owner: AD-02
authority_invoked: [AP-01, AP-03, AP-05, AD-02]
permission_warrant: primary_question_match=today_priority
refused_or_non_primary:
  - AD-01 → not_structural_plan_amendment
  - AD-04 → not_primary_question_recovery
consumed_recommendations: [AD-01_canonical_study_plan]
conflicts: none
rules_applied: [AP-01, AP-03, AP-05, AB-02_checked]
delegation: none
lawful_outcome:
  result: acted
  ownership_preserved: true
  meaning_preserved: true
programme_vi_explainability_ref: daily_coach/…
```

### AEQ coverage

| AEQ | Answer |
|-----|--------|
| AEQ1 | AD-02 permitted — today-priority domain match |
| AEQ2 | AD-01 not amending plan; AD-04 not primary |
| AEQ3 | AP-01 / AP-03 / AP-05 / AB-02 |
| AEQ4 | Day priority acted upon; ownership intact |

### Unlawful contrast

> “The app picked today’s tip.” / “Recovery and Daily co-own today.” / “Because `rank=0.88`…”

Violates AEP-01 / AEB-06 / AEB-07.

---

## 4. AXP-E02 — Delegated Authority

### Situation

Daily Coach owns today’s primary priority (AD-02). Within that goal, a study session may adjust *how* the student works (technique, pacing) under AP-04. The session does not become Master Planner or a new day-priority owner. Restoration returns full day-priority speech to Daily Coach when the session ends.

### Student speech (illustrative)

> “Today’s goal still comes from your day coach. Within that goal, this study sitting may adjust **how** you work — not what your Study Plan is, and not who owns today’s priority. When the sitting ends, ordinary daily guidance remains with your day coach.”

### Developer trace (illustrative)

```
decision_class: today_primary_priority
owner: AD-02
authority_invoked: [AP-01, AP-04, AP-07, AD-02]
permission_warrant: owner_warrant=AD-02; delegate_exercise=session_local_adaptation
refused_or_non_primary:
  - session_as_AD-01 → prohibited_plan_rewrite
  - session_as_standing_AD-02 → delegation_not_alienation
consumed_recommendations: [AD-02_today_goal]
conflicts: none
rules_applied: [AP-01, AP-04, AP-07, AB-02_checked, AB-04_checked]
delegation:
  owner: AD-02
  delegate: study_session
  scope: local_how_within_today_goal
  restore_when: session_complete
lawful_outcome:
  result: delegated_exercise
  ownership_preserved: true
  meaning_preserved: true
```

### AEQ coverage

| AEQ | Answer |
|-----|--------|
| AEQ1 | AD-02 permitted; session permitted only under AP-04 warrant |
| AEQ2 | Session not permitted as planner or standing day owner |
| AEQ3 | AP-04 / AP-07 / AB-02 / AB-04 |
| AEQ4 | Bounded exercise; owner unchanged; restore_when recorded |

### Unlawful contrast

> “Your session is now your planner.” / “Delegation transferred today’s ownership.”

Violates AEP-05 / AEP-08 / AEB-08.

---

## 5. AXP-E03 — Conflict Resolution

### Situation

CT-01 / CT-03: Daily Coach emitted a valid today-priority recommendation; Recovery Coach emitted a valid restorative recommendation after disruption. Both seek primary action. MS002 applies: higher restorative obligation leads (illustrative RP-03 application); Daily’s artefact is deferred (RO-01); Recovery’s is acted upon (RO-06). Owners unchanged.

### Student speech (illustrative)

> “You had more than one good kind of guidance at once: today’s planned focus, and restoring your study rhythm after a disruption. For now, **recovery leads** so continuity can be restored. Your day coach still owns ordinary daily priorities — that guidance **waits**; we are not throwing it away or rewriting what it means. We’re also **not** giving recovery coaching your day coach’s job.”

### Developer trace (illustrative)

```
decision_class: primary_action_under_concurrency
owner: AD-04                    # acted-upon artefact owner
authority_invoked: [AP-01, AP-06, AD-04, CT-01, CT-03, RP-01, RP-02, RP-03, RP-06, RP-07]
permission_warrant: temporary_primary_focus=recovery; higher_obligation=continuity_restore
refused_or_non_primary:
  - AD-02_as_primary_now → yielded_to_recovery_focus
  - ownership_transfer_AD-02→AD-04 → RP-08_not_applicable_no_dispute; transfer_forbidden
consumed_recommendations: [AD-02_day_priority_valid, AD-04_recovery_valid]
conflicts:
  type: [CT-01, CT-03]
  peers: [AD-02:day_priority, AD-04:recovery_posture]
rules_applied: [RP-01, RP-02, RP-03, RP-05, RP-06, RP-07, RP-10]
delegation: none
lawful_outcome:
  result: dispositioned
  dispositions:
    - AD-04_recovery → RO-06
    - AD-02_day_priority → RO-01
  ownership_preserved: true
  meaning_preserved: true
  owners_unchanged: [AD-02, AD-04]
resolution_ms002_explainability_ref: RESOLUTION_EXPLAINABILITY.md#RQ1-RQ4
```

### AEQ coverage

| AEQ | Answer |
|-----|--------|
| AEQ1 | AD-04 permitted to lead *action* under temporary primary / higher obligation |
| AEQ2 | AD-02 not permitted as primary *now*; ownership transfer refused |
| AEQ3 | CT-01/CT-03 + RP-01…RP-07 + RO-06/RO-01 |
| AEQ4 | Recovery acted upon; Daily deferred; owners and meanings intact |

### Unlawful contrast

> “Recovery now owns your daily plan.” / “The algorithm picked recovery.” / “Yesterday’s tip was wrong.”

Violates AEB-07 / AEB-08 / AEB-04.

---

## 6. AXP-E04 — Superseded Recommendation

### Situation

CT-04: Earlier the same day, Daily Coach’s day-priority recommendation was acted upon. Later, a warranted Recovery recommendation supersedes that *acted-upon status* (RO-02). Earlier artefact remains owned by AD-02 with meaning preserved; it is no longer the primary action.

### Student speech (illustrative)

> “Earlier today we were following your day coach’s focus. Things changed — restoring continuity needs to lead **now**, so that earlier next-step is **set aside for action**, not cancelled as educationally wrong. Your day coach still owns ordinary daily priorities; recovery leads the action for this moment.”

### Developer trace (illustrative)

```
decision_class: primary_action_under_concurrency
owner: AD-04
authority_invoked: [AP-06, CT-04, RP-01, RP-02, RP-07, RO-02, RO-06]
permission_warrant: later_valid_artefact_supersedes_earlier_action_status
refused_or_non_primary:
  - earlier_AD-02_as_primary_action → RO-02_superseded_action_only
consumed_recommendations: [AD-02_earlier_day_priority, AD-04_later_recovery]
conflicts:
  type: [CT-04]
  peers: [AD-02:earlier_day_priority, AD-04:later_recovery]
rules_applied: [RP-01, RP-02, RP-07, RP-10]
delegation: none
lawful_outcome:
  result: dispositioned
  dispositions:
    - AD-04_later_recovery → RO-06
    - AD-02_earlier_day_priority → RO-02
  ownership_preserved: true
  meaning_preserved: true
  note: RO-02_replaces_acted_upon_status_not_ownership
```

### AEQ coverage

| AEQ | Answer |
|-----|--------|
| AEQ1 | Later AD-04 artefact permitted as primary action |
| AEQ2 | Earlier AD-02 artefact not permitted to remain primary *action* |
| AEQ3 | CT-04 + RP-01/02/07 + RO-02/RO-06 |
| AEQ4 | Action superseded; ownership and meaning of earlier artefact preserved |

### Unlawful contrast

> “We replaced your day coach with recovery as owner.” / “That earlier tip was invalid.”

Violates AEB-08 / AEB-04 / RO-02 definition.

---

## 7. AXP-E05 — Merged Recommendations (Constitutionally Permitted)

### Situation

A **published constitutional merge pathway** explicitly permits a composite acted-upon outcome (RO-03) — for example, Revision Coach meaning *informing* Daily Coach day priority without absorbing either domain (illustrative; actual pathways live in Programme VI / MS001 / MS002 publications, not invented here). Both contributors remain named. No anonymous mega-coach. No ownership transfer.

### Student speech (illustrative)

> “Today’s focus comes from your **day coach**, informed by **revision** of material you’ve already learned. Revision is helping shape what is useful today — it is **not** rewriting your Study Plan, and it is **not** replacing your day coach. Both roles stay distinct.”

### Developer trace (illustrative)

```
decision_class: today_primary_priority_with_revision_input
owner: AD-02                         # standing day-priority owner
authority_invoked: [AP-01, AP-05, AP-06, AD-02, AD-05, RO-03, RP-01, RP-02, RP-06]
permission_warrant: published_merge_pathway=revision_informs_day_priority
refused_or_non_primary:
  - AD-05_as_standing_day_owner → prohibited
  - anonymous_merged_mega_coach → AB-08 / AP-01
consumed_recommendations: [AD-05_revision_warrant]
conflicts:
  type: [CT-01]                      # if concurrent seek-action; else pathway-only
  peers: [AD-02:day_priority, AD-05:revision_emphasis]
rules_applied: [RP-01, RP-02, RP-06, RO-03]
delegation: none
lawful_outcome:
  result: dispositioned
  dispositions:
    - composite → RO-03
  merge_pathway: published_citation_required
  contributors: [AD-02, AD-05]
  ownership_preserved: true
  meaning_preserved: true
```

### AEQ coverage

| AEQ | Answer |
|-----|--------|
| AEQ1 | AD-02 permitted as standing day owner; AD-05 permitted as informing contributor under published pathway |
| AEQ2 | AD-05 not permitted as standing day owner; anonymous merge refused |
| AEQ3 | AP-01/05/06 + RO-03 + cited merge pathway |
| AEQ4 | Composite acted upon; contributors named; owners intact |

### Unlawful contrast

> “We merged everything into one tip.” (no pathway) / “Revision now owns today.” / Hiding contributors.

Violates RO-03 exceptionalism / AEB-06 / AEB-08 / AB-08.

**Hard rule:** If no published merge pathway exists, do **not** narrate RO-03. Defer, queue, supersede action, or refuse — per MS002 — instead.

---

## 8. Cross-Cutting Unlawful Anti-Patterns

| Anti-pattern | Typical AEB / AEP breach |
|--------------|--------------------------|
| “The app decided” | AEP-01 / AEB-06 |
| Score / rank / confidence as permission | AEP-03 / AEB-07 |
| “Coach A now owns Coach B’s domain” | AEP-08 / AEB-08 |
| “Workflow recommends Topic X” | AEB-10 |
| Evidence reinterpreted in ownership speech | AEB-05 |
| Mastery claimed from clear ownership narration | AEB-04 / EIP-006 adjacency |
| Implementation service name as constitutional warrant | AEB-09 |
| Friendly merge hiding ownership dispute | AEP-04 / RP-08 |

---

## 9. Consistency with Sibling Examples

| When the journey also needs… | Also satisfy… |
|------------------------------|---------------|
| Programme VI educational warrant | Owner’s `*_EXPLAINABILITY.md` |
| Ownership-layer themes only | [`../authority/AUTHORITY_EXPLAINABILITY.md`](../authority/AUTHORITY_EXPLAINABILITY.md) |
| Conflict RQ1–RQ4 | [`../conflict_resolution/RESOLUTION_EXPLAINABILITY.md`](../conflict_resolution/RESOLUTION_EXPLAINABILITY.md) |
| Orchestration start / handoff / close | WS1 workflow / transition / completion explainability |

MS003 patterns **frame permission**. They do not replace educational or orchestration speech.

---

## 10. Closing

These patterns show the same constitutional truth in five shapes:

> **Ordinary permission · bounded delegation · conflict disposition · supersession of action · published merge — always with owners intact and alternatives honestly refused.**

Use them to test narration. Do not treat them as a closed catalogue of product strings.
