# FV-001B — Terminology Audit

**Date:** 2026-07-28  
**Rule:** Flag language that a Founder preparing official IFoA curricula should not need, especially Educational Intelligence / engineering terms.  
**Method:** Visible text only (screens + captured body text).

---

## Summary

Founder-facing **workflow strip** language is largely excellent (Official CMP, Official Syllabus, Publish Verified Curriculum, Ready).

The **workspace** still exposes internal intelligence vocabulary that fails the acceptance criterion: *Never encounter unnecessary Educational Intelligence terminology.*

---

## Forbidden / EI-adjacent terms observed

| Term | Where observed | Founder impact |
|---|---|---|
| **Knowledge Graph** | Workspace tabs; Pipeline stage “Knowledge Graph Built”; Pipeline audit `graph_rebuilt` | Sounds like research tooling, not curriculum verify |
| **Pipeline** / **Curriculum Intelligence Pipeline** | Workspace section + tab | Engineering process metaphor |
| **Entity Details** | Workspace tab | Opaque; not Founder vocabulary |
| **Evidence Explorer** | Workspace tab | Ambiguous vs “proof of extraction quality” |
| **Inference** | Pipeline audit / topic mapping surface | Risk of conflating subject content with system inference |
| **Curriculum Intelligence** | Workspace panel heading | Abstract product jargon |
| **Platform Intelligence** | Console Home Quick Actions | Not curriculum-prep language |
| **nodes** | Preview: `0 nodes` | Engineering unit; Founder expects topics/objectives |
| **embeddings** | Pipeline audit: “ready for embeddings extension” | Unnecessary EI/ML language |

**Not observed on Founder chrome (good):** SCI, Runtime, Twin, Digital Twin, Educational Decision, Educational Intelligence (full phrase), Experience Model, Learner Lifecycle, CKG, Preferred Authority.

---

## Founder-aligned language (keep)

Observed and appropriate:

- Curriculum Authority
- Official CMP / Curriculum Master Pack
- Official Syllabus
- Extracted curriculum / Review & Corrections
- Publish Verified Curriculum
- Available to Students (Ready)
- Subject code / Version
- Validation findings with “Why it matters” / “What to do”

---

## Mismatched product language

| Phrase | Screen | Issue |
|---|---|---|
| *Know exactly what to study next* | Sign in | Student value prop for Curriculum Authority login |
| *Operational pulse* / Platform Health 0% | Console Home | Ops monitoring, not authoring |
| `sources_uploaded:` / `subject_created:` | Studio activity | Event-key style, not human activity labels |
| `UPLOADED BY 1` | Document cards | Internal user id |
| `Preview ready · not_ready` | Workspace | Contradictory compound status |
| `Document 1` / `Document 3` | Pipeline | Opaque vs Official CMP / Syllabus names |
| Encoding `â` in topic titles | Pipeline entities | Looks broken / untrustworthy |

---

## Acceptance criterion

> Never encounter unnecessary Educational Intelligence terminology.

**Result: FAIL**

Primary offenders on the core authoring surface: **Knowledge Graph**, **Pipeline**, **Entity Details**, **embeddings**, **nodes**.

---

## Recommended replacements (product copy only)

| Current | Prefer |
|---|---|
| Knowledge Graph | Curriculum structure / Topic map |
| Pipeline | Document processing / Extraction status |
| Entity Details | Topic details (or hide) |
| Evidence Explorer | Extraction evidence (or hide) |
| 0 nodes | 0 topics extracted |
| Curriculum Intelligence | Curriculum quality check |
| Platform Intelligence | (remove from Founder quick actions) |
