# FV-001A — Terminology Audit

**Date:** 2026-07-28  
**Rule:** Flag terms a first-time founder must mentally translate. Critical if SCI / Runtime / Twin / Educational Decision appear on student path.

---

## Scan result — forbidden Critical terms (student-facing)

| Term | Observed on student Home / Session / Wizard? |
|---|---|
| SCI | **Not observed** |
| Runtime | **Not observed** |
| Twin / Digital Twin | **Not observed** |
| Educational Decision | **Not observed** |

These specific Critical flags did **not** fire on the primary student journey screens in this walkthrough.

---

## Observed terminology problems

| Term | Surface | Plain-language problem | Severity |
|---|---|---|---|
| Education Operating System | Landing | Sounds like infrastructure, not “study app for CS1” | Major |
| Internal Alpha / Founding Cohort | Landing, footer | Fine for alpha; still jargon for outsiders | Observation |
| Study Sensei | Home, Help, onboarding | Implies a coach persona; no chat Coach exists | Major (expectation mismatch) |
| Mission | Home, Help | Learnable, but unfamiliar vs “today’s study block” | Minor |
| Estimated Knowledge | Home readiness | Opaque metric name | Major |
| Decision Journal | Help, History | Internal-sounding; not everyday student language | Major |
| Educational Timeline | Help, History | Abstract; requires Help essay to decode | Major |
| Curriculum Studio | Console Content | Acceptable for operators; heavy for day-one | Observation |
| Official CMP | Workspace | OK for IFoA-aware founders; still acronym-first | Observation |
| Curriculum Intelligence Pipeline | Workspace | Sounds like engineering tooling | **Critical** (founder calm) |
| Knowledge Graph | Workspace tab | Technical | **Critical** |
| Evidence Explorer | Workspace tab | Technical | **Critical** |
| Entity Details | Workspace tab | Technical | **Critical** |
| Platform Intelligence | Console quick action | Vague / internal | Major |
| Product Check-in | Console | Process jargon | Major |
| Validation / Preview / Approval | Studio workflow | Manageable if staged; overwhelming when empty | Major when premature |
| UPLOADED BY 1 | Document card | Exposes internal user id | Minor |

---

## Phrases that force self-explanation

> “This is the highest-value next step for this topic based on your recent practice.”

Founder must invent what “this topic” is.

> “Session started: your topic.”

Same opacity.

> “The Decision Journal is Study Sensei’s durable educational memory…”

Help text teaches an internal model instead of answering a question.

---

## Positive plain language (keep)

- “Know exactly what to study next.”  
- “Use a short syllabus code such as CS1.”  
- “Without an Official CMP the Studio cannot derive sections, topics, or learning objectives for students.”  
- “We couldn't publish this curriculum… would expose incomplete material to students.”  
- “No revision support is ready right now. Follow today's Mission on Home.”  
- Invite-only coordinator copy on login.

---

## Verdict on terminology

Student path avoids the worst EI/Runtime/Twin labels, but **Console Workspace** and **Help** still leak internal intelligence vocabulary. **Study Sensei** creates a Coach expectation the UI does not fulfil. **Estimated Knowledge** and unnamed “topic” language undermine explainability in practice.

---

**End of Terminology Audit**
