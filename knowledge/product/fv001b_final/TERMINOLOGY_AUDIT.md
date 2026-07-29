# FV-001B Final — Terminology Audit

**Date:** 2026-07-29  
**Scope:** Visible Founder Console / Curriculum Studio surfaces during CS1F journey  
**Evidence:** `_evidence/phases.json` term scan + screenshots

---

## Product chrome language (good)

Observed Founder-facing terms that match curriculum authority work:

| Term | Where | Assessment |
|---|---|---|
| Kwalitec Console | Sidebar / header | Clear |
| CURRICULUM AUTHORITY | Sidebar | Clear |
| Curriculum Studio | Nav / titles | Clear |
| Subjects | Nav / hub | Clear |
| Official CMP | Upload slot | Clear (Curriculum Master Pack explained) |
| Official Syllabus | Upload slot | Clear |
| Validate Curriculum | Action | Clear |
| Build Preview | Action | Clear |
| Approve Curriculum | Action | Clear |
| Publish Verified Curriculum | Action | Clear |
| Ready | Document / subject status | Clear when used honestly |
| Version | Workspace / catalogue | Clear |

---

## Forbidden EI product jargon

Scanned for: SCI, Runtime, Twin, Educational Decision, Educational Intelligence, Experience Model, Learner Lifecycle, Inference, CKG, Digital Twin, Preferred Authority, Knowledge Graph, Entity Details.

| Hit | Phase | Assessment |
|---|---|---|
| “Inference” | Curriculum Structure topic “Chapter 4 Inference” | **Not product jargon** — syllabus/CMP content title. Acceptable. |
| All other terms | — | **Not found** in primary chrome |

**Verdict:** Primary product language avoids unnecessary EI terminology.

---

## Confusing / overloaded terms

| Term / phrase | Issue | Evidence |
|---|---|---|
| `in_progress` / `not_ready` / `preview_ready` | Machine-ish status fragments alongside human copy | Workspace status cards + version history |
| “Validation needs attention · in_progress” | Sounds unfinished after a Validate click that already returned a result | `phase5_validate.png` |
| “blocking findings” vs “0 validation errors” vs “warning” | Same concept, three severities | `phase5_validate.png`, `22_p5_validation_panel.png` |
| Approve vs Publish in refusal copy | Approve action explains publish refusal | `phase7_approve.png` |
| “Uploaded by 38” | Internal id | Document slots |
| Stage labels (`Content Sources`, `Subject`) | Understandable after learning; dense with version | Subjects list |

---

## Workflow strip vs workspace stages

Subjects hub strip:

1. New Subject  
2. Upload Official CMP  
3. Upload Official Syllabus  
4. Extraction  
5. Review & Corrections  
6. Publish Verified Curriculum  
7. Available to Students (Ready)

Workspace stepper:

Subject → Content Sources → Validation → Preview → Approval → Publish

**Assessment:** Both are Founder-readable, but they are **not the same model**. A Founder may wonder where “Extraction” and “Review & Corrections” sit relative to Validation / Preview. Major terminology alignment opportunity; not alone a NO-GO.

---

## Summary

- Founder vocabulary is mostly appropriate.
- No EI product-jargon problem in chrome.
- Critical terminology failures are **state and gate naming inconsistencies** (blocking vs warning vs errors; approve vs publish; ready vs not_ready), not missing CMP/Syllabus labels.
