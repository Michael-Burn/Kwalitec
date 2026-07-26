# Blind Comparative Review

**Framework ID:** EVF-020  
**Programme:** Programme V — Educational Validation Framework  
**Classification:** Layer 2 — Blind Comparative Review  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Effective:** July 2026  

---

## 1. Purpose

Layer 2 records independent educational preference when reviewers compare strategies **without knowing which is which**.

Typical comparison set:

- **Kwalitec** (student-visible educational behaviour for the capability/task)  
- **Human Tutor** (experienced IFoA tutor strategy artefact)  
- **Alternative Planning Strategy** (registered non-Kwalitec planning approach)

Reviewers record:

1. Preference (ranked or forced choice), and  
2. Educational reasoning (why).

This layer validates relative educational quality. It does not replace Blind Review’s persona hypothesis programme.

---

## 2. Relationship to Blind Review (critical)

| Blind Review (existing) | Blind Comparative Review (EVF Layer 2) |
|---|---|
| Permanent research subsystem | EVF validation layer |
| SV personas review the live product experience | Reviewers compare anonymised strategy artefacts |
| Protocol frozen under `reviewer_framework/` | Protocol defined here |
| Outputs: `blind_reviews/SV-*.md` | Outputs: comparative records under `reports/` / `benchmark_reviews/` |

**Hard rules:**

1. Do **not** modify Blind Review protocol, personas, YAML, or execution guide to “fit” Layer 2.  
2. EVF **consumes** Blind Review outputs as supporting evidence and may map themes into comparative synthesis.  
3. A full Blind Review corpus (e.g. SV-001–SV-020 + meta-analysis) may satisfy part of Layer 2 **only when** a Comparative Mapping Note shows how preference/reasoning evidence was derived without breaking blindness or inventing head-to-head results that were not studied.  
4. When true three-way blind comparison has not yet been run, mark Comparative Preference Index evidence as **partial** and apply Gate CONDITIONAL / REJECTED rules accordingly — do not fabricate preference percentages.

---

## 3. Blindness protocol

### 3.1 Artefact preparation

For each comparative task:

1. Produce three strategy artefacts (Kwalitec / Human Tutor / Alternative) in a common template.  
2. Strip brand names, product chrome, and author identity.  
3. Label artefacts only as **Strategy A / B / C** with a sealed key held outside the reviewer session.  
4. Freeze the candidate version baseline for the Kwalitec artefact.

### 3.2 Reviewer constraints

- Reviewers must not be told which strategy is Kwalitec.  
- Reviewers must not consult engineering docs or Runtime A.  
- Reviewers answer only the registered educational task questions.  
- No cross-talk between reviewers before individual preferences are filed.

### 3.3 Unblinding

Unblinding occurs **after** preferences and reasoning are filed.  
The Version Approval Report may then map A/B/C → sources.

---

## 4. Comparative task catalogue (Version 1.0 minimum)

| Task ID | Educational job | Capabilities touched |
|---|---|---|
| CT-01 | Plan the next study block / week sequencing | EC-01 |
| CT-02 | Decide tonight’s mission under time scarcity | EC-02 |
| CT-03 | Explain why a recommendation or next step is suggested | EC-03 |
| CT-04 | Recover after missed days | EC-04 |
| CT-05 | Build a revision strategy with limited remaining weeks | EC-05 |
| CT-06 | Interpret readiness / exam preparation status honestly | EC-06 |

Additional tasks may be registered additively.

---

## 5. Preference recording

For each task and reviewer:

```markdown
## Comparative result — <Task ID>

- Reviewer ID:
- Strategies presented: A / B / C (blind)
- Preference rank (1 = best):
  1.
  2.
  3.
- Forced choice winner (if used):
- Educational reasoning:
- Dimensions most decisive (ED-IDs):
- Confidence in judgement: High / Medium / Low
```

Aggregate only after individual filings. Aggregation method must be stated in the comparative report (mean rank, win-rate, etc.).

---

## 6. Using Blind Review corpus as Layer 2 input

When a three-way blind pack is not yet available, operators may file a **Comparative Mapping Note**:

1. List Blind Review findings that speak to preference vs human systems / existing tools / alternative study methods (e.g. mature study system, CMP stack, tutor expectations).  
2. Separate **direct comparative evidence** from **thematic inference**.  
3. Assign Comparative Preference Index conservatively (see Gate bands).  
4. Flag `comparative_mode: corpus_mapped` vs `comparative_mode: sealed_blind`.

Sealed blind comparison is the target method. Corpus mapping is a bridge, not a permanent substitute for Version 1.0 APPROVED without holds when core tasks lack head-to-head evidence.

---

## 7. Output locations

| Artefact | Path |
|---|---|
| Sealed blind comparative report | `reports/COMPARATIVE_<version>_<YYYYMMDD>.md` |
| Mapping note (corpus bridge) | `reports/COMPARATIVE_MAPPING_<version>_<YYYYMMDD>.md` |
| Benchmark-specific write-ups | `benchmark_reviews/` |

---

## 8. Anti-patterns

- Revealing “Strategy B is Kwalitec” mid-review  
- Scoring UI polish instead of educational quality  
- Treating meta-analysis strategy recommendations as preference data  
- Editing Blind Review transcripts to strengthen a Gate outcome  
- Averaging unrelated SV scores into a fake win-rate  

---

## 9. Cross references

- `EDUCATIONAL_BENCHMARKS.md`  
- `EDUCATIONAL_RELEASE_GATE.md`  
- `REVIEWER_GUIDELINES.md`  
- `knowledge/product/ep004_private_beta/reviewer_framework/REVIEW_PROTOCOL.md`  
- `knowledge/architecture/BLIND_REVIEW_CURRENT_STATE.md`  
