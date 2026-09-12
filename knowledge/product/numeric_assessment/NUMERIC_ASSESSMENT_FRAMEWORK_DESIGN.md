# Numeric Assessment Framework Design

**Status:** Locked design for the Numeric Assessment Framework (standalone; unwired)  
**Date:** 2026-09-12  
**Scope:** Answer Specification contract, parser/normalizer, evaluation-policy comparison, precision/rounding, representation/unit handling, and three-tier feedback for CS1 live numeric checkpoints  
**Related:** Live scoring in `app/application/learning_session/scoreable_practice.py`; 30 publication-approved CS1 numeric checkpoints under `app/curriculum/data/educational_packages/cs1/`

---

## Purpose

This document locks the Numeric Assessment Framework design so it lives in the repository, not only in external conversation.

The framework answers four progressively harder questions about a student numeric response:

1. Does the value match the authored answer under an explicit evaluation policy?
2. Does the response comply with the authored precision / format instruction?
3. Is the response an author-declared accepted representation of that value?
4. When wrong, is there an authored diagnostic rule that the observed response unambiguously satisfies?

It does **not** claim to be a general mathematical solver, a symbolic-equivalence engine, or a system that can infer the specific calculation error from a final wrong number alone.

---

## Terminology

| Term | Meaning |
|------|---------|
| **Answer Specification** | Authored, per-question contract describing what is assessed and how it is evaluated |
| **Evaluation policy** | Explicit enum choosing how numerical closeness is judged (no universal tolerance) |
| **value_correct** | Internal fact: the parsed value matches the canonical answer under the comparison policy |
| **precision_compliant** | Internal fact: the response matches the authored precision / format requirements |
| **accepted_forms** | Author-declared list of allowed representations (for example decimal, percentage); not inferred symbolically |
| **Tier 1 feedback** | Deterministic evaluation outcome (parse, compare, precision, representation, invalid input) |
| **Tier 2 feedback** | Deterministic mistake classification only when an authored diagnostic rule unambiguously matches |
| **Tier 3 feedback** | Honest fallback stating that the specific calculation error cannot be determined from the final answer alone |
| **Parse outcome** | Explicit result of interpreting the raw string: valid, invalid, or uninterpretable (locale ambiguity) |

Correct framing: **authored evaluation contract**, not an implicit float compare with a hidden default.

---

## Why this exists

Tonight's live scoring path already showed the failure mode this framework exists to prevent:

- A question's stem can ask for one precision while `numeric_tolerance` encodes a different closeness rule.
- That mismatch is not enforced by the product; it is an authoring accident that can silently drift.
- One such case was found and fixed; four milder instances of the same pattern are already banked for migration under this framework.

A second failure mode is diagnostic overclaim:

- A wrong final number is genuinely underdetermined. Many different real mistakes can produce the identical wrong value.
- Unlike an MCQ distractor (authored to one misconception), inventing a general numeric diagnosis manufactures false confidence.
- Bundling an unverified list of possible mistakes is worse than honest uncertainty.

---

## Current mechanism this framework supersedes

Confirmed live path (do not duplicate; replace later under a separate wiring brief):

| Concern | Today |
|---------|-------|
| Parser | `_parse_number` in `scoreable_practice.py` (strict US-thousands shape; rejects fractions/units/EU decimals) |
| Comparison | Absolute `|candidate - expected| <= numeric_tolerance`, defaulting to `1e-6` when omitted |
| Precision check | None |
| Representation / units | None (parser rejects `%`, currency, and similar) |
| Feedback | Single static `common_mistake` string on incorrect |
| Live count | 30 publication-approved numeric checkpoints; tolerances `0.001` (21), `0.5` (8), `0.005` (1) |

This framework is the locked replacement contract. Wiring into `score_practice_response` and migrating package JSON are **out of scope for the first implementation pass**.

---

## Philosophy

### Four capabilities, not one engine

| Capability | Role | Built in this pass |
|------------|------|--------------------|
| Value comparison | Decide numerical match under an explicit policy | Yes |
| Precision / format compliance | Decide whether the response obeys authored precision instructions | Yes |
| Equivalent-representation handling | Accept only author-declared forms | Yes |
| Diagnostic interpretation | Optional authored rules; never a general solver | Structure yes; general diagnosis deferred forever |

### Authored contract, not ad-hoc conditionals

Every numeric question carries an explicit Answer Specification. Evaluation behaviour is derived from that contract. Authors do not embed one-off scoring conditionals in application code.

### No universal tolerance

There is no product-wide default tolerance that silently applies when authors forget to choose a policy. The evaluation policy is mandatory and explicit. The relationship between what the question asks for and how strictly it is checked must be authored, visible, and enforceable.

### Two correctness facts

`value_correct` and `precision_compliant` are tracked separately. Future student-facing feedback may honestly say that a value is numerically correct but did not match the requested precision. Collapsing both into one boolean loses that truth.

### No giant symbolic engine

Equivalent forms are declared by authors (`accepted_forms`), for example decimal and percentage, or decimal only. The system does not pretend to understand every mathematically equivalent representation.

### Honest uncertainty over fake diagnosis

When no authored Tier 2 rule matches, Tier 3 states that Kwalitec cannot determine the specific calculation error from the final answer alone. That replaces generic bundled lists of unverified possible mistakes.

---

## Standing principles

1. **Explicit evaluation policy per question.** One of: `exact`, `decimal_precision`, `absolute_tolerance`, `relative_tolerance`, `significant_figures`, `interval_range`, `custom_domain_rule`. No implicit fallback that invents a tolerance.
2. **Parsing never silently guesses on genuine locale ambiguity.** Ambiguous comma usage becomes an explicit invalid / uninterpretable outcome, not a guessed float.
3. **Raw and normalized values are both preserved** on the evidence / evaluation record.
4. **Tier 2 phrasing is "consistent with," never "you did X,"** and only when the observed response unambiguously satisfies an authored rule.
5. **Assessment intent is part of the authoring model** (for example calculating a value, applying a formula, rounding, converting units, interpreting a result). Different intents may require different evaluation semantics.
6. **Standalone until proven.** This package must not be wired into live scoring, routes, or student-facing surfaces until a separate scoped brief authorizes cutover.
7. **Cross-question evaluation invariant.** Two questions that share the same evaluation policy (and matching policy parameters) must exhibit identical boundary behaviour. The test harness enforces this.

---

## Answer Specification contract

Every numeric question authors the following fields:

| Field | Purpose |
|-------|---------|
| `canonical_value` | Authoritative numeric answer (as a decimal string / float contract value) |
| `quantity_type` | What kind of quantity is assessed (probability, count, rate, currency-like scalar, residual, factor, etc.) |
| `unit` | Authored unit if any (empty when dimensionless) |
| `assessment_intent` | What the question is actually assessing |
| `representation_policy` | How representations are handled (restrict to accepted forms; optional unit handling) |
| `precision_policy` | Required precision / format rules (or none) |
| `comparison_policy` | Evaluation-policy enum plus its parameters |
| `accepted_forms` | Explicit list of allowed response forms |
| `rounding_policy` | How rounding is interpreted relative to the precision and comparison policies |
| `diagnostic_rules` | Optional Tier 2 rules (may be empty) |
| `feedback_policy` | How Tier 1 / 2 / 3 feedback is assembled for this item |

### Assessment intent (authoring model)

| Intent | Meaning |
|--------|---------|
| `calculate_value` | Produce a numeric result from given data |
| `apply_formula` | Apply a named relationship correctly |
| `round_value` | Demonstrate correct rounding to a required precision |
| `convert_units` | Convert between authored units / scales |
| `interpret_result` | Interpret a computed quantity (for example a residual sign or a factor vs percentage) |

These intents are part of the authoring model because they are genuinely different assessment jobs. They are not one generic compare-the-number treatment.

### Evaluation policy (comparison_policy)

| Policy | Semantics |
|--------|-----------|
| `exact` | Parsed value must equal canonical value exactly (after normalization) |
| `decimal_precision` | Match after rounding / comparing at an authored number of decimal places |
| `absolute_tolerance` | `|candidate - canonical| <= absolute_tolerance` |
| `relative_tolerance` | Relative difference within authored relative tolerance (with defined zero handling) |
| `significant_figures` | Match under authored significant-figure rules |
| `interval_range` | Candidate must lie inside an authored closed interval |
| `custom_domain_rule` | Explicit named domain rule declared on the specification (not free-form code in the scorer) |

Parameters live on the specification beside the policy (for example `absolute_tolerance`, `decimal_places`, `relative_tolerance`, `interval_low` / `interval_high`, `significant_figures`, `custom_rule_id`). Authors choose the policy that matches the question's instruction. The framework refuses a specification that omits required parameters for its chosen policy.

### Precision policy

Precision compliance is independent of value comparison.

Examples:

- Require exactly N decimal places in the raw response.
- Require at most / at least N decimal places.
- Require trailing zeros when the instruction asks for a fixed decimal display.
- No precision requirement (`none`), when the stem does not instruct a display format.

A response may be `value_correct=True` and `precision_compliant=False` at the same time.

### Representation policy and accepted_forms

`accepted_forms` is an explicit list, for example:

- `decimal` only
- `decimal` and `percentage`
- `integer` (whole-number display)

The parser / normalizer converts an accepted form into a comparable numeric value when the form is unambiguous. Forms not listed are not accepted, even if mathematically related. Units follow the same discipline: only authored unit handling applies; the system does not invent unit conversions.

### Rounding policy

Rounding policy states how the framework treats values that are numerically near the canonical answer under the chosen comparison policy, relative to the precision instruction. It must not silently enlarge tolerance. Rounding behaviour is authored, not inferred from float noise.

### Diagnostic rules (Tier 2)

Each rule is authored and defensible:

| Field | Purpose |
|-------|---------|
| `rule_id` | Stable id |
| `match_value` | Observed numeric value that triggers the rule |
| `match_policy` | How the observed value is matched (typically absolute or exact under the same discipline as comparison) |
| `consistent_with` | Student-facing phrase stem: what the response is consistent with |
| `rationale` | Author-only note explaining why the rule is defensible |

Rules fire only when the observed parsed value unambiguously satisfies the rule and the response is not value-correct. Wording is always "consistent with …", never "you did X".

Empty `diagnostic_rules` is valid and common. Absence of rules is not a defect; it routes incorrect answers to Tier 3.

### Feedback policy

Controls Tier assembly:

- Always emit Tier 1 evaluation facts.
- Emit Tier 2 only when a rule matches.
- Otherwise emit Tier 3 honest uncertainty for incorrect value outcomes.
- Do not emit the legacy bundled unverified mistake list as if it were diagnosis.

---

## Parsing layer

Parsing is its own explicit layer.

Responsibilities:

1. Preserve the raw response string unchanged on the evaluation record.
2. Produce a normalized parsed value when interpretation is unambiguous.
3. Record parse status: `parsed`, `invalid`, or `uninterpretable`.
4. Never silently guess on genuine locale ambiguity (for example whether a comma is a decimal separator or a thousands separator).
5. Reject non-numeric shapes that would previously have been mangled (fractions, units glued to digits without an accepted form, mixed punctuation).

Uninterpretable / invalid input is an explicit evaluation outcome. It is not scored as a confident numerical incorrectness that pretends the system understood the number.

---

## Evaluation record (internal)

The framework returns a structured result including at least:

| Field | Meaning |
|-------|---------|
| `raw_response` | Exact student string |
| `parse_status` | `parsed` / `invalid` / `uninterpretable` |
| `parsed_value` | Normalized float when parsed |
| `value_correct` | Numerical match under comparison policy (False when unparsed) |
| `precision_compliant` | Precision / format compliance (None when not applicable or unparsed, per policy) |
| `representation_accepted` | Whether the response used an accepted form |
| `matched_diagnostic_rule_id` | Tier 2 rule id if any |
| `feedback_tier` | `1`, `2`, or `3` (Tier 1 always underlies; 2/3 classify the incorrect path) |
| `feedback_message` | Assembled message under feedback_policy |
| `evaluation_policy` | Echo of the policy used (for audit / invariant tests) |

Overall learner-facing correctness for future wiring may combine these facts, but the framework itself must not collapse them into a single boolean as its only output.

---

## Three-tier feedback model

### Tier 1: Deterministic evaluation (required for every question)

Covers:

- Parsing and normalization
- Comparison under the authored evaluation policy
- Precision and rounding handling
- Representation and unit handling
- Invalid / uninterpretable input handling

This tier must work correctly for every numeric question. It is the bulletproof floor.

### Tier 2: Deterministic mistake classification (optional)

Activated only when:

1. The question authors one or more diagnostic rules, and
2. The observed response unambiguously satisfies exactly one such rule (or a defined precedence if multiple could match; default: first authored unambiguous match, with tests forbidding overlapping rules on the same item unless precedence is declared).

Phrasing: "consistent with …". Never claims certain knowledge of the student's private calculation steps.

### Tier 3: Honest general fallback

When the answer is not value-correct and no Tier 2 rule applies:

> Kwalitec cannot determine the specific calculation error from the final answer alone.

This replaces the current pattern of presenting a generic bundled list of unverified possible mistakes as if it were diagnostic sophistication the product does not have.

---

## Scope for this implementation pass

### In scope

1. Permanent locked design document (this file) and product README index entry.
2. Canonical Answer Specification data model.
3. Parser / normalizer layer.
4. Evaluation-policy-driven comparator.
5. Precision / rounding rules.
6. Representation / unit handling under authored policies.
7. Three-tier feedback classifier.
8. Strong test harness, including:
   - Representative cases drawn from the real 30 live numeric questions
   - Exact correct, accepted equivalents, just outside tolerance, substantially wrong
   - Excessive / insufficient precision, trailing zeros, negative values
   - Malformed / invalid / locale-ambiguous input
   - Boundary tolerance cases
   - Cross-question invariant: shared evaluation policy ⇒ identical boundary behaviour
9. Standalone package under `app/application/numeric_assessment/`, unwired from live scoring.

### Explicitly out of scope (framework build pass; migration now done separately)

- Wiring into `score_practice_response`, routes, templates, or any student-facing surface
- Symbolic mathematics platform
- Structured multi-step intermediate-work capture
- Twin, Policy V1, OEA, Spacing, VP-001, arbitration, or Progression Readiness changes
- Building a general diagnostic solver

The 30 live questions now carry authored `answer_specification` blocks. Live scoring cutover remains a separate step.

---

## Migration posture

**Migration status (2026-09-12):** All 30 live numeric checkpoints carry an authored `answer_specification` object on the checkpoint entry in `app/curriculum/data/educational_packages/cs1/`. Specs are loaded by `app/application/numeric_assessment/catalogue.py`. Live scoring still uses legacy `numeric_tolerance` / `accepted_keywords` until a separate wiring brief.

Completed in the migration pass:

1. Each of the 30 items has an Answer Specification whose `comparison_policy` and `precision_policy` match its stem instruction (fixing the stem-vs-tolerance drift class, including the four banked 4dp / 0.001 cases).
2. Legacy `numeric_tolerance` values remain on the packages for the unwired live path; the new specs express the chosen policy explicitly (`decimal_precision`, `absolute_tolerance`, or `exact`) rather than wrapping tolerance unexamined.
3. Existing `common_mistake` prose remains on packages for the live path. Where a wrong value was unambiguous, a Tier 2 `diagnostic_rules` entry was also authored on the specification; otherwise Tier 3 applies under the new framework.
4. Live scoring cutover remains a deliberate later step.

---

## Implementation location

- Design: this file under `knowledge/product/numeric_assessment/`
- Code: `app/application/numeric_assessment/` (standalone application package; unwired)
- Tests: `tests/application/numeric_assessment/`

Package layout (locked for this pass):

| Module | Role |
|--------|------|
| `specs.py` | Answer Specification and policy enums / dataclasses |
| `parser.py` | Raw preservation, normalization, ambiguity handling |
| `comparator.py` | Evaluation-policy comparison; precision / representation checks |
| `feedback.py` | Three-tier feedback assembly |
| `evaluator.py` | Public `evaluate(spec, raw_response)` entry point |
| `results.py` | Evaluation result vocabulary |
| `__init__.py` | Public exports |

---

## Non-goals (this implementation)

- Live product wiring of any kind
- Changing educational package JSON
- Claiming diagnostic certainty from final answers without authored rules
- Introducing a universal tolerance constant anywhere in the new package
- Redesigning Educational Framework law (EF-001 remains frozen; this is assessment execution infrastructure)
