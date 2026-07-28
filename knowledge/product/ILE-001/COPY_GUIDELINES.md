# ILE-001A — Copy Guidelines

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001A  
**Status:** Active  
**Effective:** 2026-07-28  
**Source of truth:** `app/application/adaptive_assessment/copy_registry.py`

---

## Purpose

Centralise all Adaptive Assessment learner-facing copy so tone stays calm, explainable, and educationally honest — never exam-like or overwhelming.

---

## Rules

1. **No hard-coded AA strings in templates/JS** — resolve via the copy registry / localisation catalogue.  
2. **Tone** — steady coach: clear, brief, respectful (`USER_EXPERIENCE_PHILOSOPHY.md`).  
3. **Always answer why** — entry frames and “Why am I seeing this?” must explain purpose and evidence use.  
4. **Uncertainty is honest** — “Not enough evidence yet” beats fake confidence.  
5. **Actions are learning-forward** — Continue Learning, Strengthen Understanding, Build Confidence.  
6. **Readiness never guarantees** — mandatory non-guarantee line for Readiness Check.  
7. **Terminology** — pass `TERMINOLOGY_STANDARD.md` validation.

---

## Canonical examples (English defaults)

| Key | Default |
|---|---|
| `session.quick_check.name` | Quick Check |
| `action.continue_learning` | Continue Learning |
| `action.strengthen_understanding` | Strengthen Understanding |
| `action.build_confidence` | Build Confidence |
| `explain.why_am_i_seeing_this` | Why am I seeing this? |
| `uncertainty.not_enough_evidence` | Not enough evidence yet |
| `uncertainty.gather_more` | Let's gather a little more information |
| `feedback.use_to_guide` | We'll use this to guide practice. |
| `readiness.non_guarantee` | This guides what to study next. It does not predict your result. |

---

## Do / Do not

| Do | Do not |
|---|---|
| Frame checks as study support | “You must pass to continue” |
| Show effort estimates | Hide length until trapped |
| Allow defer / pause language | Guilt for incomplete checks |
| Specific, constructive recovery | Red FAILED stamps, rankings |

---

## Adding copy

1. Add an `AdaptiveAssessmentCopy` entry to the registry.  
2. Ensure terminology validation passes.  
3. Prefer `{placeholders}` for variables; mark `pluralizable=True` when count-sensitive.  
4. Do not translate in ILE-001A — English defaults only.

---

**End of COPY_GUIDELINES**
