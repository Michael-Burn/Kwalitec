# IA-003 — Student-Centred Educational Messaging

**Capability ID:** IA-003  
**Programme:** Internal Alpha Stabilization  
**Priority:** P2  
**Status:** Implemented — pending Architecture Review  
**Date:** 2026-07-15

---

## Problem

Internal Alpha testers saw recommendation copy that exposed engineering vocabulary
instead of educational guidance.

Observed example on the dashboard **Today's Recommendation** card:

> `18 evidence creating - Based on your current study progress, a short
> diagnostic will help identify the most useful next step.`

The leading fragment came from presentation leakage:

- `curriculum_entity_id` is an opaque syllabus key (often a numeric ORM PK such
  as `"18"`)
- `intent.value` is domain vocabulary (`evidence_creating`)

Those values were joined into the card subtitle. Students cannot act on internal
identifiers or ActionIntent enums. Recommendations must answer what to do, why,
and what happens next — in plain educational language.

---

## Educational Principles

Every student-facing message should answer at least one of:

1. **What should I do?**
2. **Why should I do it?**
3. **What happens next?**

Use plain educational language. Avoid student-facing use of:

| Forbidden (examples) | Prefer |
|----------------------|--------|
| evidence / evidence_creating | study activity, short check, practice |
| pipeline / intelligence | (omit — do not name layers) |
| classification / learning event | study progress, completed session |
| digital twin | learning profile |
| mission generation | today's recommended focus |
| warrant / cold_start / thin_warrant | (omit — keep honesty internal) |
| numeric entity ids | topic titles / educational phrases |

Domain Educational Intelligence may continue to use these terms internally.
Presentation must map them before render.

---

## Message Strategy

| Surface | Strategy |
|---------|----------|
| EI Recommendation card title | Map `ActionFamily` → educational verb phrase |
| EI Recommendation card subtitle | Family situating line only — **never** dump intent enums or entity ids |
| EI Recommendation card reason | Plain “Based on …” / “You've completed …” explanations |
| Today's Mission (ORM path) | Keep plan-bound mission title; educational “why” copy |
| Learning Progress / ready cards | “Overall progress”, “average topic progress” — not composite/system jargon |
| Study pattern notice badges | Human labels (Accuracy drop, Long sessions, …) |
| Daily briefing | “topics that still need more practice” — not `mastery < 60` |
| Internal Alpha settings | “Learning profile status” — not Digital Twin |
| Legacy rest recommendations | Study-pattern wording — not “burnout risk detected” as theatre |

**Out of scope (unchanged):** Decision / Recommendation ranking, Educational
Intelligence domain packages, Founder Operating System, UI redesign,
AI-generated messaging.

---

## Before / After Examples

### Today's Recommendation (EI card)

**Before**

| Field | Copy |
|-------|------|
| Title | `Diagnostic` |
| Subtitle | `18 · evidence_creating` |
| Why | `Based on your current study progress, a short diagnostic will help identify the most useful next step.` |

**After**

| Field | Copy |
|-------|------|
| Title | `Find your next focus` |
| Subtitle | `A short check to guide today's recommendation` |
| Why | `You've completed valuable study activities. A short check now will help identify the most useful next step.` |

### Learning Progress (legacy composite path)

**Before:** `Composite Score` · `avg mastery`  
**After:** `Overall progress` · `average topic progress`

### Settings (Internal Alpha)

**Before:** `Digital Twin status: Present` / `… Educational Intelligence behaviour`  
**After:** `Learning profile status: Ready` / `… your study recommendations`

---

## Validation

Reviewed student-facing messaging for:

- Dashboard (command cards, recommendation card, pattern notice, empty states)
- Mission page (hero why-copy, empty states)
- Study-plan surfaces (left educational; no EI tag dumps)
- Completion / review flash
- Internal Alpha settings labels
- Daily briefing strings

Confirmed:

- Consistent supportive tone
- Plain educational language on EI recommendation projection
- No intentional engineering terminology on those surfaces

---

## Regression Testing

`tests/test_ia003_student_centred_educational_messaging.py`

| Test | Intent |
|------|--------|
| `test_no_evidence_creating_in_card_copy` | Card fields free of forbidden vocabulary |
| `test_entity_id_and_intent_enum_never_dumped` | Domain ids/intents not echoed |
| `test_titles_are_educational_family_labels` | Stable educational family titles |
| `test_reason_answers_why` | Reason explains motivation |
| `test_builder_source_never_joins_raw_intent` | Source guard against regressions |
| `test_dashboard_has_no_engineering_recommendation_leak` | Rendered dashboard HTML |
| `test_mission_page_uses_educational_why_copy` | Mission surface |
| `test_settings_learning_profile_not_digital_twin` | Settings labels |
| `test_recommendation_logic_unchanged_domain_intents` | Ranking / domain intents untouched |

Also: existing recommendation-card and dashboard integration tests updated for
new presentation strings.

---

## Known Limitations

1. **Topic display names on the EI card** — `curriculum_entity_id` remains an
   opaque key in the domain Experience. This capability refuses to dump the id;
   it does not yet resolve official syllabus codes (e.g. Topic 4.2) into the
   EI subtitle. Product mission titles (PlanningService) already carry human
   topic labels on the Today's Mission card.
2. **ViewModel internal cargo** — `DashboardViewModel.warnings` /
   `empty_states` may still hold structural tags for Application consumers.
   Those tags are not rendered by current student templates.
3. **Analytics “Mastery” chart label** — retained as educational progress
   language, distinct from forbidden EI eng vocabulary.
4. **Founder Dashboard / Internal Alpha pipeline docs** — founder-facing;
   intentionally out of student messaging scope.

---

## Related

- [IA-001 Mission Recommendation Integrity](IA-001_MISSION_RECOMMENDATION_INTEGRITY.md)
- [IA-002 Study Plan State Synchronization](IA-002_STUDY_PLAN_STATE_SYNCHRONIZATION.md)
- Feedback: `research/internal_alpha/week_001/` (educational finding on
  “18 evidence creating”)
