# Blind Review Protocol

**Authority:** Permanent Kwalitec research infrastructure  
**Applies to:** Every execution of SV-001 through SV-020 (and any future reviewer registered in this framework)  
**Companion files:** [`REVIEW_TEMPLATE.md`](REVIEW_TEMPLATE.md) · [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md) · [`personas/`](personas/)

This is the permanent review protocol. Re-runs must obey it without rewriting prompts.

---

## 1. Independent personas

Each reviewer is a distinct named student persona defined in `personas/SV-XXX.yaml`.

- Personas are not interchangeable “generic users.”
- Demographics, exam context, attempt, time-to-exam, occupation, hypothesis, and evaluation dimension are fixed in the YAML.
- The agent must inhabit **only** the loaded persona for the duration of the review.

---

## 2. One reviewer at a time

- Execute exactly one reviewer per review run unless the operator explicitly requested a batch.
- In a batch (“Run all reviewers”, “Run all CM1 reviewers”), still complete reviewers **sequentially**, one full review before the next.
- Never merge voices, scores, or conclusions across personas inside a single output file.

---

## 3. Latest review package verification

Before judging the product, confirm:

| Check | Path / action |
|---|---|
| Student review package | `knowledge/reviews/V1_REVIEW_PACKAGE/` |
| Package reflects current student-facing build | Compare overview / walkthrough / screens / known limitations to the live app |
| Product chrome (when available) | Note version / Internal Alpha / Founding Cohort / build label as observed |

If the package and live student experience diverge, record the divergence in the review and judge the **live student-facing experience**.

---

## 4. Baseline verification

Before reviewing:

1. Confirm the application is running from the approved private-beta baseline (see [`../REVIEW_BASELINE_AUDIT.md`](../REVIEW_BASELINE_AUDIT.md) when present).
2. Confirm critical student paths needed for the persona’s task are reachable (login → start session → study → finish / record).
3. Do not treat engineering fix notes as part of the study experience.

Baseline checks are facilitator hygiene. They are not the educational evaluation.

---

## 5. Ignore engineering documentation

Out of scope for every reviewer:

- Application source code
- Engineering documentation and RCA notes
- Implementation write-ups
- Developer comments and historical bug reports
- Internal architecture / curriculum-engine docs

In scope:

- What a student can see and do in the product
- Student-facing review package materials that describe the experience (overview, journeys, screens, known limitations, beta expectations)

---

## 6. Student-only perspective

- Review as an IFoA (or designated exam) student preparing for the persona’s paper.
- Evaluate educational usefulness, trust, workflow fit, and learning behaviour — not software craftsmanship.
- Ignore visual polish except where it blocks studying or understanding.
- Do not propose product roadmaps, tickets, or engineering solutions inside the review transcript.

---

## 7. One hypothesis per reviewer

- Each persona has exactly one `educational_hypothesis` and one `central_question`.
- Answer that hypothesis. Do not expand into adjacent research questions belonging to other reviewers.
- Scoring dimensions listed in the persona YAML are the only required scores for that run.

---

## 8. No comparison with previous reviewers

- Assume this is the only participant in the beta.
- Do not read, cite, rank against, or reconcile with other `blind_reviews/SV-*.md` files while writing.
- Do not mention other reviewer IDs, names, or scores.

Independence is a methodological requirement, not a style preference.

---

## 9. No interim synthesis

During a review run (including mid-batch):

- Do not average scores
- Do not declare programme winners/losers
- Do not update meta-analysis conclusions
- Do not produce product recommendations for the company

Synthesis belongs only in an explicit meta-analysis task after a completed corpus, never inside a persona review.

---

## 10. Review output format

Write the review to the persona’s `output` path (normally `knowledge/product/ep004_private_beta/blind_reviews/SV-XXX.md`).

Required structure (see [`REVIEW_TEMPLATE.md`](REVIEW_TEMPLATE.md)):

1. Title and persona header metadata
2. Baseline / package confirmation (brief)
3. How the persona used the product (narrative)
4. Answers to every persona question
5. Scoring table (1–10 per listed dimension + Overall)
6. Central question answer (explicit)

Tone: first-person student interview transcript. Honest. Specific. Evidence from screens and actions taken.

---

## 11. Repeat runs

When the operator says **Repeat SV-XXX** or **Run reviewer SV-XXX** after a prior file exists:

- Re-load protocol, template, and persona YAML
- Re-verify package and baseline against the **current** student experience
- Overwrite the review file unless the operator asked to archive the previous run
- Still forbid comparison with other reviewers (including the prior version of the same ID, except as a fresh independent session)

---

## 12. New reviewers

To add a reviewer beyond SV-020:

1. Assign the next free ID (`SV-021`, …).
2. Create `personas/SV-0XX.yaml` using the same schema.
3. Add a registry row in [`REVIEWER_REGISTRY.md`](REVIEWER_REGISTRY.md).
4. Choose a **new** educational hypothesis not already owned by an existing reviewer, unless the intent is a deliberate replication study (document that in the YAML).
5. Execute via the same protocol — never by pasting a one-off mega-prompt.
