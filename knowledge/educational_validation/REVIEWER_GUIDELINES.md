# Reviewer Guidelines

**Framework ID:** EVF-050  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Validator and comparative reviewer handbook  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

These guidelines tell humans (and agent operators acting as validators) how to conduct EVF reviews without compromising independence, explainability, or Blind Review integrity.

---

## 2. Roles at a glance

| Role | Primary documents | Output |
|---|---|---|
| Educational Validator | Capability Guide, Dimensions | `capability_reviews/EC-*.md` |
| Comparative Reviewer | Blind Comparative Review, Benchmarks | Preference + reasoning filings |
| Comparative Facilitator | Blind Comparative Review | Sealed packs, unblinding, reports |
| Educational Gate Owner | Release Gate, Release Standard, Template | Version Approval Report |
| Blind Review Executor | EP-004 reviewer framework + cursor rule | `blind_reviews/SV-*.md` (unchanged process) |

---

## 3. Universal rules

1. **Student learning first** — judge educational usefulness, not engineering cleverness.  
2. **Evidence before opinion** — every material rating cites a path or observation.  
3. **No Runtime A inspection for scoring** — do not open recommendation engines to “explain” a verdict.  
4. **No decision mutation** — never change plans, missions, or scores as part of review.  
5. **Honesty about gaps** — Insufficient Evidence beats fabricated trust.  
6. **Preserve Blind Review** — do not edit SV transcripts or persona YAML for Gate convenience.  
7. **Explainability** — a second reader must understand why you scored as you did.  
8. **Independence** — do not average other validators’ unpublished drafts into your own.

---

## 4. Educational Validator practice (Layer 1 + 3)

### Do

- Work one capability at a time  
- Use the capability report template verbatim  
- Score only applicable dimensions  
- Map Blind Review citations by hypothesis/theme, not by rewriting them  
- State claim limits when issuing Conditionally Trusted  

### Do not

- Approve a capability because adjacent capabilities look strong  
- Treat UI delight as Educational Soundness  
- Convert Twin confidence internals into student trust scores  
- Hide dual-truth findings as “copy nits”

### Calibration anchors

| Observation | Lean toward |
|---|---|
| Clear What/Why/Next with bounded claims | Strong / Adequate on Explainability & Confidence |
| Empty readiness beside strong language | Weak / Failing on Confidence & Soundness |
| Practical tonight path under time scarcity | Strong / Adequate on Practicality |
| Conflicting duration or dual homes for same decision | Weak on Consistency; often Not Trusted for Daily Coach |

---

## 5. Comparative Reviewer practice (Layer 2)

### Do

- Treat Strategy A/B/C as equal unknowns  
- Rank by educational quality for the stated task  
- Write reasoning that another educator can audit  
- Tag decisive ED-IDs  

### Do not

- Guess brands or authors  
- Prefer verbosity or formatting polish  
- Discuss filings with other reviewers before lock  
- Change ranks after unblinding  

---

## 6. Comparative Facilitator practice

### Do

- Enforce shared artefact templates and length bands  
- Keep the sealed key offline from reviewers  
- File preferences before unblinding  
- Label `sealed_blind` vs `corpus_mapped` accurately  

### Do not

- Special-polish the Kwalitec artefact on Gate day  
- Unblind early to “help” a struggling review  
- Present corpus mapping as sealed blind win-rates  

---

## 7. Gate Owner practice (Layer 4)

### Do

- Verify prerequisites before scoring  
- Show the four-component worksheet  
- Apply Version 1.0 thresholds exactly  
- Write holds that a student-facing team can operationalise  

### Do not

- Round a 79% into APPROVED without Standard amendment  
- Accept engineering certification as Supporting Evidence Integrity  
- Issue APPROVED with a required capability Not Trusted  

---

## 8. Agent operators

When an AI agent assists EVF work:

1. Load this file plus the specific layer guide before writing reports.  
2. For Blind Review execution requests, follow `.cursor/rules/blind-review-framework.mdc` — **not** this document’s Layer 2 sealed protocol.  
3. Never claim sealed-blind preference results that were not actually run.  
4. Prefer citing existing Blind Review corpus with a Mapping Note when sealed packs are absent.

---

## 9. Ethics and student protection

- Do not shame simulated or real student failure modes in report prose.  
- Do not recommend dark-pattern motivation techniques.  
- Prefer releasing later over releasing with false educational confidence.

---

## 10. Cross references

- `EDUCATIONAL_VALIDATION_CONSTITUTION.md`  
- `CAPABILITY_VALIDATION_GUIDE.md`  
- `BLIND_COMPARATIVE_REVIEW.md`  
- `EDUCATIONAL_DIMENSIONS.md`  
- `VERSION_APPROVAL_WORKFLOW.md`  
- `knowledge/product/ep004_private_beta/reviewer_framework/REVIEW_PROTOCOL.md`  
