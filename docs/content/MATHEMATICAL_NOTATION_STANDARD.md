# Mathematical Notation Standard

**Status:** Active (authoring and migration law)  
**Scope:** Student-facing authored content in educational packages (CS1 live catalogue and future subjects)  
**Related inventory:** `docs/content/math_notation_inventory.json` (ledger), `scripts/inventory_math_notation.py` (generator)

---

## 1. Principle

**Every mathematical object in authored content is represented as proper mathematical notation; ordinary prose stays prose.**

The distinction is **semantic role**, not visual complexity or current readability.

- A Greek letter, Latin letter, or function used **as a variable or expression** inside a mathematical statement is a mathematical object and must be properly typeset, even when its current plain-text or Unicode form already looks acceptable.
- The same letter or word **merely mentioned** in descriptive prose (for example explaining what a symbol means, in narrative text) is **not** converted.
- The success criterion is **appropriate mathematical notation representation**, not a specific rendering technology (KaTeX, MathML, or another typesetter may implement the representation).

Summations and integrals fall under this standard **automatically whenever they appear**. None currently exist in the live CS1 catalogue; no live examples are required for that clause.

---

## 2. What counts as a mathematical object

Treat as a mathematical object (must be proper notation) when the string uses any of the following **as mathematics**, not as prose vocabulary:

| Category | Includes |
|---|---|
| Variables and parameters | Latin or Greek letters standing for quantities (`μ`, `σ`, `λ`, `β`, `θ`, `n`, `X`) |
| Greek symbols used as variables | Same letters when they participate in a statement or calculation |
| Functions | `P(…)`, `E[…]`, `Var(…)`, `Cov(…)`, `Φ(…)`, `sd(…)`, and similar |
| Operators | Arithmetic and algebraic operators inside expressions |
| Relationships / inequalities | `=`, `≠`, `≈`, `≤`, `≥`, and related relational statements used mathematically |
| Powers and roots | Superscripts, `e^{…}`, Unicode `²`, `√`, nested radicals |
| Subscripts | `X̄` components, `σ_X`, `xᵢ`, Unicode subscripts |
| Fractions | Inline slash forms that mean division of mathematical quantities (`σ²/n`, `(y−μ̂)/√V(μ̂)`) |
| Structured multi-step derivations | Calculation boards with chained equals, score expansions, likelihood derivatives |
| Summations and integrals | `∑`, `∫`, and equivalents, whenever authored |

---

## 3. Worked examples from the live catalogue

Examples below are taken from publication-approved CS1 packages. **Current** text is what students see today. **Intent** states how the standard classifies the occurrence.

### 3.1 Greek letter that **is** a mathematical object (needs proper notation)

**Source:** `2.5.1-clt-cs1008.json` · `worked_example.problem_statement`

> Pet-insurance claim severities are iid with mean μ = 180 and standard deviation σ = 60. A sample of n = 36 claims is drawn. Using the CLT, approximate P(X̄ < 170). Use Φ(1) ≈ 0.841.

Here `μ`, `σ`, `n`, `P(X̄ < 170)`, and `Φ(1)` are live mathematical objects inside a problem statement. Readability of Unicode Greek does **not** exempt them.

### 3.2 Similar wording that **stays prose** (not converted)

**Source:** `2.6.3-mean-var-sample-cs1009.json` · step explanation (narrative)

> For a random sample with finite mean, the sample mean is unbiased for μ.

When a sentence only **names** the parameter in explanatory prose (what the estimator is unbiased for), without posing a calculation or typesetting an expression board, the mention may remain prose under this standard. Borderline cases are recorded as **needs manual review** in the inventory rather than forced either way.

Clearer prose-only pattern (concept without a live expression): instructional text that discusses “the population mean” or “the rate parameter” in words, with **no** symbol and **no** expression present, is ordinary prose and is out of scope for conversion.

### 3.3 Functions: `P(…)`, `E[…]`, `Var(…)`

**`P(…)`** · `2.1.1-discrete-cs1002.json` · worked-example final answer (excerpt)

> … with p = 0.1, P(X = 0) ≈ 0.0424.

**`E[…]` and `Var(…)`** · `2.2.4-linear-combinations-cs1005.json` · `worked_example.problem_statement`

> Portfolio losses X and Y (£000) satisfy E[X] = 10, E[Y] = 4, Var(X) = 9, Var(Y) = 4, and Cov(X, Y) = 3. For the linear combination L = 2X − Y, compute E[L] and Var(L).

These function applications are mathematical objects. They must be proper notation even though actuarial plain text is conventional and currently readable.

### 3.4 Fractions

**Source:** `2.5.1-clt-cs1008.json` · knowledge-check model answer

> For iid finite-variance data, X̄≈N(μ,σ²/n) for large n.

The slash form `σ²/n` is a mathematical fraction (variance of the sample mean). Proper notation represents it as a fraction (or an equivalent unambiguous mathematical form), not as flattened prose punctuation.

### 3.5 Roots

**Source:** `2.5.1-clt-cs1008.json` · `worked_example.steps[0].calculation`

> σ/√n = 60 / √36 = 60 / 6 = 10

**Source:** `4.2.8-residuals-cs1003.json` · `worked_example.steps[0].calculation`

> r_P = (3 − 6)/√6 = −3/√6 = −√(9/6) = −√1.5 ≈ −1.2247

Roots and nested radicals are mathematical objects whenever they appear in expressions.

### 3.6 Subscripts and superscripts

**Source:** `3.1.2-maximum-likelihood-cs1010.json` · `worked_example.steps[0].calculation`

> Σxᵢ = 2+3+1+4 = 10;  ℓ(λ) = 4 ln λ − 10λ

**Source:** `2.2.3-cov-corr-expectation-cs1005.json` · step explanation (excerpt)

> … Var(X) = Var(Y) = 0.25 and σ_X = σ_Y = 0.5.

Subscripts (`xᵢ`, `σ_X`) and powered or decorated parameters (`λ̂`, `σ²`, `e^{−λx}`) used in mathematics must be proper notation.

### 3.7 Multi-step derivations

**Source:** `4.1.3-least-squares-cs1003.json` · step calculations (board)

> x̄ = (2+3+4+5)/4 = 14/4 = 3.5;  ȳ = (4+6+7+9)/4 = 26/4 = 6.5  
> S_xx = (−1.5)²+(−0.5)²+(0.5)²+(1.5)² = 2.25+0.25+0.25+2.25 = 5; S_xy = …  
> β̂₁ = 8/5 = 1.6;  β̂₀ = 6.5 − 1.6 × 3.5 = …

**Source:** `3.1.2-maximum-likelihood-cs1010.json` · derivative steps

> dℓ/dλ = 4/λ − 10 = 0  ⇒  λ̂ = 4/10 = 0.4  
> d²ℓ/dλ² = −4/λ² < 0 at λ̂ = 0.4

Chained calculation boards are mathematical objects end to end.

---

## 4. What does **not** get converted

Do **not** convert:

1. **Pure prose mentions** of a symbol or concept where no mathematical expression is present (discussing “correlation”, “variance”, or “the rate parameter” in words only).
2. **Metalinguistic explanation** that only talks about notation without posing mathematics (for example a sentence whose sole job is to say what a name refers to, with no live formula). Use manual review when a symbol appears in such a sentence and role is unclear.
3. **Non-mathematical typography** (section separators, bullets, currency, ordinary punctuation).
4. **Metadata and non-student fields** (ids, tags, internal keys) even if a pattern matcher would fire.

The inventory script marks ambiguous symbol-in-prose cases as **needs manual review** instead of silently forcing migration or exclusion.

---

## 5. Summations and integrals

Summation and integral notation is in scope under Section 2 the moment it is authored. The live CS1 catalogue currently contains **no** `∑` / `∫` (or equivalent ASCII `sum_` integral forms used as live catalogue content in the sense of displayed calculus notation boards). Future packages that introduce them must use proper mathematical notation from the first draft; no retrospective live examples are needed to establish the rule.

---

## 6. Compliance today vs migration

| State | Meaning |
|---|---|
| **Already compliant** | Mathematical objects in the string are already in a form that is properly typeset for students today (for example fully covered by delimited math, or solely by bare LaTeX fragments the session render path already wraps). |
| **Needs migration** | At least one genuine mathematical object is present and is not yet properly represented. |
| **Correctly excluded** | The string was mathish under pattern detection, but under this standard it is prose (or otherwise not a conversion target). |
| **Needs manual review** | Automated classification cannot reliably decide object vs prose; a human must decide before migration work treats the string as done or skipped. |

Technology note: extending render-time heuristics is **not** a substitute for meeting this standard where compound structure (fractions, roots, derivation boards) requires authored mathematical notation.

---

## 7. Operational use

1. Authors and converters follow this document when creating or editing package mathematics.
2. `scripts/inventory_math_notation.py` classifies the live catalogue against this standard and refreshes `docs/content/math_notation_inventory.json`.
3. Migration waves pick bounded package batches from the ledger (prefer highest-risk compound calculations first for student benefit). Order of waves does **not** narrow the ultimate scope: every `needs_migration` string remains in backlog until done or reclassified by manual review.

---

## 8. Non-goals (this standard document)

- Does not choose a single required markup syntax beyond “proper mathematical notation.”
- Does not modify render wrappers, KaTeX configuration, or package JSON by itself.
- Does not define regression-prevention tooling (that follows once real migrated content exists to protect).
