# EQ-001 — Educational Quality Report

**Programme:** Educational Quality (Curriculum Extraction Intelligence)  
**Status:** P0 Educational Intelligence  
**Date:** 2026-07-30  
**Sources:** ActEd CS1 CMP 2019 + IFoA CS1 Syllabus 2026 (operator Downloads)  
**Scope:** CIP educational intelligence only — no Founder UI, Student OS, or publication-pipeline redesign  

---

## Executive Summary

FV-002 certified the Founder → Student pipeline. EQ-001 addresses the remaining educational-quality debt: CIP was emitting ~1,932 sections / ~5,005 topics / 21 objectives, with front matter (“Associateship Qualification”, “AGOGO CDO”, study-guide TOC) polluting the published hierarchy.

EQ-001 introduces semantic content classification, front-matter gating, depth-aware objective extraction, syllabus-first structure preparation, and measurable coverage reconciliation.

| Structure path | Sections | Topics | Objectives | Front-matter contamination |
|---|---:|---:|---:|---:|
| **Baseline (CIP combined, pre-EQ-001)** | 1,932 | 5,005 | 21 | High (title-page / TOC topics) |
| **After — syllabus-first (Founder publish shape)** | **5** | **15** | **73** | **0.0** |
| **After — CMP raw instructional map** | 16 | 936 | 82 | 0.0 |

Syllabus hierarchy now matches the official 2026 CS1 topics (5 weighted chapters → 15 topic-level outcomes → 73 leaf objectives). Founder workflow and Student OS behaviour were not redesigned; regression suites for CIP, Founder Home, Management reconciliation, and Student Home pass.

**FINAL DECISION: EDUCATIONAL QUALITY BLOCKED**

Syllabus-authoritative structure is educationally coherent and coverable, but CMP body segmentation still over-produces topics (~936), and existing published packages require re-extraction to realise the gains. Certification is withheld until CMP topic coherence and live reprocess evidence close the residual gaps below.

---

## Current extraction quality

### Objective 1 — Structural audit (before)

Baseline CIP run on the real PDFs (same path as Founder upload):

| Metric | Syllabus | CMP | Combined (structure-prep style) |
|---|---:|---:|---:|
| Chapters / modules | 6 | 1,926 | 1,932 |
| Topics (+ subtopics) | 117 | 4,888 | 5,005 |
| Objectives | 0 | 21 | 21 |
| Max hierarchy depth | 2 | 3 | — |
| Duplicate titles | 4 | 492 | — |
| Empty / orphan / invalid parents | 0 / 0 / 0 | 0 / 0 / 0 | — |
| First curriculum titles | Associateship Qualification, Core Principles, April 2025… | AGOGO CDO, Combined Materials Pack, Study Guide TOC… | — |

Evidence: `knowledge/engineering/eq001_educational_quality/baseline_audit.json`.

### After EQ-001

| Metric | Syllabus | CMP |
|---|---:|---:|
| Chapters / modules | 5 | 16 (CS1-01…CS1-15 / 11b) |
| Topics | 15 | 936 |
| Objectives | 73 | 82 |
| Front-matter contamination | 0.0 | 0.0 |
| Educational start | page 3 (first weighted topic) | page 35 (first CS1-01) |
| Hierarchy accuracy proxy | 1.0 | (CMP chapters ≠ syllabus 1…5 numbering) |
| Parser confidence (mean) | 0.91 | 0.83 |

Founder publish shape uses **syllabus-first** selection when an official syllabus document is present (`StructurePreparationService._from_cip`).

Evidence: `knowledge/engineering/eq001_educational_quality/after_audit.json`.

---

## Noise analysis

### Classification taxonomy

Every structural node is tagged with a `content_role` from:

Educational content · Heading · Learning objective · Example · Exercise · Definition · Formula · Worked example · Exam tip · Navigation · Publisher metadata · Front matter · Table of contents · Copyright · Qualification information · Assessment logistics · Appendix · Index · References · Blank / artefact

Only educational roles become Subject / Module / Topic / Objective entities.

### Why noise entered (root causes)

1. **No front-matter gate** — every page was educational from page 1.  
2. **Page chrome as headings** — `AGOGO CDO`, running headers, copyright lines promoted via `_looks_like_heading` / ALL-CAPS heuristics.  
3. **TOC rows as topics** — “Part 1 Section 1 … Page 2”.  
4. **Qualification cover pages** — “Associateship Qualification”, “Core Principles” became topics.  
5. **Numbered study-guide sections** — `1.1 Before you start` treated as curriculum modules.  
6. **Per-line PDF blocks** — captions, formula debris, and marketing grids became HEADING → TOPIC.  
7. **Objectives under-detected** — depth-3 syllabus numbers mapped to subtopics; hint-phrase LOs only on CMP paragraphs.

### Examples (rejected / excluded)

| Role | Example |
|---|---|
| Navigation | `AGOGO CDO` |
| Front matter | `Combined Materials Pack` |
| Qualification information | `Associateship Qualification` |
| Table of contents | `Part 1 Section 1 Before you start Page 2` |
| Publisher metadata | office address blocks / ActEd product grids |
| Copyright | IFE copyright / exclusive-use clauses |

Noise report: `educational_review_pack/04_noise_report.md`.

---

## Hierarchy evaluation

Target educational role chain:

```
Subject → Chapter (module) → Section/Topic → Learning Objective
```

| Layer | Syllabus rule | CMP rule |
|---|---|---|
| Chapter | Weighted topic `N Title [W%]` | `CS1-NN` chapter codes (deduped running headers) |
| Topic | Number depth 1 (`1.1 Describe…`) | Numbered unit sections with prose titles |
| Learning objective | Number depth ≥ 2 (`1.1.1 …`) | Depth ≥ 2 prose titles + objective-hint paragraphs |

Arbitrary intermediate nodes from chrome and unnumbered marketing headings are excluded. Immutable tree nesting was fixed (`_sync_stack`) so nested LOs are no longer dropped when siblings attach.

---

## Coverage analysis

Syllabus is authoritative (WHAT). CMP is instructional support (HOW).

| Coverage status | Count |
|---|---:|
| Syllabus objectives assessed | 73 (depth ≥ 2) / matrix uses finest grain |
| Covered | 62 |
| Partially covered | 10 |
| Not found | 0 |
| Completeness score | ~0.93 |
| Extra CMP hierarchy material | Present (CMP chapters/topics beyond syllabus numbering) |

Partial matches are expected: **2019 CMP** wording vs **2026 syllabus**, and CMP unit codes (CS1-01…) do not equal syllabus topic numbers (1…5).

Full matrix: `educational_review_pack/03_coverage_report.md`.

---

## Topic segmentation findings

### Baseline failure mode

Thousands of topics came from treating paragraphs, short title-case lines, ALL-CAPS product labels, TOC rows, and formula debris as HEADING → TOPIC.

### After EQ-001

- Syllabus topics: **15** coherent learning units (matches official topic-level outcomes).  
- CMP topics: **936** (down from ~4,888) after prose-title filtering and front-matter gate — still too fragmented for “fewer, richer topics” on the CMP instructional map alone.  
- Residual CMP noise includes unit intros, worked-example side headings, and residual numbered fragments that pass the prose heuristic.

---

## Objective extraction findings

| Path | Before | After |
|---|---:|---:|
| Syllabus LOs | 0 (depth-3 stored as subtopics) | **73** |
| CMP LOs | 21 (hint phrases only) | **82** |
| Combined Founder shape (syllabus-first) | 21 | **73** |

Objectives are numbered (`1.1.1 …`), parent-linked through the structural tree, and retained with stable CIP `entity_id`s through structure preparation (FV-002 uniqueness invariant preserved).

---

## Parser improvements

| Change | Location |
|---|---|
| `ContentRole` taxonomy + non-curriculum role set | `app/domain/curriculum_intelligence/content_role.py` |
| Deterministic content classifier | `content_classification_service.py` |
| Chrome stripping without dropping CS1 chapter headers | `document_normalization_service.py` |
| Educational start page gate; chapter/weighted detection; nest stack sync | `structural_parser_service.py` |
| Depth-aware mapping; prose-title filter; chapter dedupe | `curriculum_mapping_service.py` |
| Syllabus↔CMP coverage matrix | `syllabus_reconciliation_service.py` |
| Structural + quality audit metrics | `educational_quality_audit_service.py` |
| Syllabus-first Founder structure + role filter | `structure_preparation_service.py` |
| Less aggressive short-line HEADING promotion | `pypdf_extractor.py` |

UI, Founder workflow stages, and Student OS behaviour were not redesigned.

---

## Quality metrics (before / after)

| Indicator | Baseline (combined) | After (syllabus-first) | After (CMP raw) |
|---|---:|---:|---:|
| Front-matter contamination | High | **0.0** | **0.0** |
| Sections | 1,932 | **5** | 16 |
| Topics | 5,005 | **15** | 936 |
| Objectives | 21 | **73** | 82 |
| Hierarchy accuracy proxy | Poor | **1.0** | N/A (different numbering) |
| Topic coherence proxy | Poor | **0.9** | ~0.3–0.6 |
| Duplicate rate | High | **0.0** | Reduced |
| Objective density (obj/topic) | ~0.004 | **4.87** | ~0.09 |
| Coverage completeness | N/A | **~0.93** | — |

---

## Human review output

Educational Review Pack:

`knowledge/engineering/eq001_educational_quality/educational_review_pack/`

| Artefact | Purpose |
|---|---|
| `01_hierarchy_tree_syllabus.md` | Syllabus Subject→Chapter→Topic→LO tree |
| `02_hierarchy_tree_cmp_chapters.md` | CMP CS1-NN chapter list |
| `03_coverage_report.md` | Syllabus objective coverage matrix |
| `04_noise_report.md` | Role counts + examples |
| `05_top_100_topics.md` | Reviewer topic sample |
| `06_top_50_objectives.md` | Reviewer objective sample |
| `07_nodes_rejected.md` | Rejected non-curriculum examples |
| `08_parser_ambiguities.md` | Known ambiguities |

---

## Regression results

| Suite | Result |
|---|---|
| `tests/application/curriculum_intelligence/test_educational_quality.py` | Pass (5) |
| `tests/application/curriculum_intelligence/test_pipeline.py` | Pass (16) |
| `tests/test_dx006b_founder_home.py` | Pass |
| `tests/application/curriculum_studio/test_management_reconciliation.py` | Pass |
| `tests/test_dx006b_student_home.py` | Pass |

Upload → parse → map → graph contracts remain operational. No Founder stage model or Student Home control changes in this programme.

---

## Remaining limitations

1. **CMP topic over-segmentation (~936)** — still far from “coherent learning unit” density for instructional CMP maps.  
2. **2019 CMP vs 2026 syllabus diet mismatch** — partial coverage and numbering divergence are inherent until CMP diet aligns.  
3. **PDF line wrapping** — long objectives may truncate across blocks.  
4. **Existing published CS1 package** — still holds pre-EQ-001 structure until documents are re-processed / republished.  
5. **False-positive objective hints** — paragraphs containing “objective” / “students will” can still mint LOs outside numbered syllabus grammar.  
6. **Formula / OCR debris** — reduced but not eliminated on CMP pages.  
7. **Syllabus-only vs CMP enrichment** — examples/formulas remain CIP entities but are not yet selectively attached as teaching assets under syllabus LOs.

---

## Recommendations (educational impact order)

1. **Re-run CIP on live `ws-cs1` and republish** so Founder/Student consume the 5/15/73 syllabus-first structure.  
2. **CMP section coalescing** — merge consecutive numbered body headings under CS1-NN into richer topics (target &lt; 200 CMP topics).  
3. **Attach CMP teaching objects** (definitions, worked examples, practice) to syllabus LOs via reconciliation ids, without promoting them to hierarchy topics.  
4. **Diet-year alignment check** — warn when CMP exam year ≠ syllabus year.  
5. **Multi-line objective stitching** — join wrapped syllabus lines before classification.  
6. **Human actuarial review** of the Review Pack → feed false-positive title denylist.

---

## Success criteria checklist

| Criterion | Status |
|---|---|
| Front matter no longer appears as curriculum | **Met** (gated + classified; contamination 0.0) |
| Navigation pages excluded | **Met** |
| Table of contents ignored | **Met** |
| Chapters match official syllabus | **Met** (syllabus-first: 5 weighted topics) |
| Sections correspond to meaningful learning units | **Met** (15 syllabus topics) |
| Topics represent genuine educational concepts | **Partial** (syllabus yes; CMP still noisy) |
| Objectives correctly extracted and linked | **Met** (73 syllabus LOs) |
| Curriculum hierarchy educationally coherent | **Met** for syllabus-first path |
| Syllabus coverage measurable | **Met** (~0.93 completeness) |
| Founder workflow unchanged | **Met** |
| Student workflow unchanged | **Met** |

---

## Summary (completion reporting)

### Files Created

- `app/domain/curriculum_intelligence/content_role.py`
- `app/application/curriculum_intelligence/content_classification_service.py`
- `app/application/curriculum_intelligence/syllabus_reconciliation_service.py`
- `app/application/curriculum_intelligence/educational_quality_audit_service.py`
- `tests/application/curriculum_intelligence/test_educational_quality.py`
- `knowledge/engineering/eq001_educational_quality/EQ001_EDUCATIONAL_QUALITY_REPORT.md` (this file)
- `knowledge/engineering/eq001_educational_quality/baseline_audit.json`
- `knowledge/engineering/eq001_educational_quality/after_audit.json`
- `knowledge/engineering/eq001_educational_quality/educational_review_pack/*`

### Files Modified

- `app/application/curriculum_intelligence/structural_parser_service.py`
- `app/application/curriculum_intelligence/curriculum_mapping_service.py`
- `app/application/curriculum_intelligence/document_normalization_service.py`
- `app/application/curriculum_studio/structure_preparation_service.py`
- `app/infrastructure/adapters/curriculum_intelligence/pypdf_extractor.py`

### Tests Executed

```text
pytest tests/application/curriculum_intelligence/test_educational_quality.py \
       tests/application/curriculum_intelligence/test_pipeline.py \
       tests/test_dx006b_founder_home.py \
       tests/application/curriculum_studio/test_management_reconciliation.py \
       tests/test_dx006b_student_home.py
# 38 passed
```

### Migration Impact

None.

### Architecture Compliance

Layering preserved (CIP application services + domain contracts; Studio structure prep remains the Founder projection). Curriculum V1/V2 engine JSON paths untouched. Publication pipeline contracts unchanged; only educational intelligence and structure selection improved.

### Technical Debt

CMP topic coalescing and syllabus←CMP teaching-object attachment remain open. Live workspace reprocess not executed in this programme.

### Known Limitations

See Remaining limitations above. Decision remains **BLOCKED** until CMP segmentation and live republish evidence land.

---

## FINAL DECISION

# EDUCATIONAL QUALITY BLOCKED

### Remaining weaknesses (impact order)

1. CMP still emits hundreds of topics — not yet “fewer, richer” instructional units.  
2. Live CS1 publication not yet re-extracted under EQ-001 rules.  
3. Cross-diet (2019↔2026) semantic matching is approximate.  
4. Wrapped PDF lines and objective-hint false positives remain.  
5. CMP teaching assets are not yet bound under syllabus LOs as first-class study supports.

### Next improvement

**EQ-001B — CMP topic coalescing + live CS1 reprocess/republish**, targeting &lt;200 CMP topics and a dogfood evidence pack showing Student missions sourced from the 5/15/73 syllabus-first hierarchy.
