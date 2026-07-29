# Cognitive Load Review

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Scale:** Low · Moderate · High · Very High

---

## Definition

Cognitive load here means **competing decisions and explanations** the user must process before acting — not educational difficulty of the exam content.

---

## Primary path scores

| Screen | Load | Primary source of unnecessary complexity |
|---|---|---|
| Curriculum Workspace | **Very High** | Parallel steppers, KPI cards, upload, pipeline, 9 tabs, multi-actions |
| Console Home | **Very High** | Dual KPI grids + Quick Actions + detail cards |
| Studio hubs (×5) | **High** | Repeated tutorials + duplicate catalogues |
| Student Home | **High** | Layered explanations + secondary CTAs + context cards |
| History | **High** | Epistemology teaching + KPIs + dual archive CTAs |
| Help | **High** | Ontology essays compensating for product IA |
| Decision Journal / Timeline | **Moderate–High** | Conceptual overlap with History |
| Console secondary reports | **Moderate–High** | Engineering terminology + sparse actions |
| Profile | **Moderate** | Card sprawl / stats |
| Login | **Moderate** | Marketing list + form dual focus |
| Begin Learning review | **Moderate** | Surfacing unchosen defaults |
| Onboarding | **Moderate** | Multi-CTA orientation |
| Choose Exam | **Low–Moderate** | Catalogue OK; gate copy when blocked |
| Journey / Revision | **Moderate** | Contained if Home stays primary |
| Session activity | **Low–Moderate** | Focused; card chrome minor |
| Session complete | **Low** | Single exit action |
| Auth form alone | **Low** | Clear |
| Confirm modal | **Low** | Focused |

---

## Load drivers (taxonomy)

| Driver | Examples | Fix |
|---|---|---|
| **Choice overload** | Many equal buttons; 9 tabs | One Primary; stage tabs |
| **Conceptual overload** | History vs Journal vs Timeline | Merge Progress |
| **Explanatory overload** | Home why×N; Help essays | One layer; IA fix |
| **Monitoring overload** | KPI mosaics | Delete non-decision metrics |
| **Navigational overload** | 10+13 Console destinations | Cap at 6 |
| **Implementation overload** | Entity ids, ms, retrieval profiles | Advanced only |
| **Status overload** | Repeated badges/alphas | Once per shell |

---

## Necessary vs unnecessary load

| Necessary (keep) | Unnecessary (cut) |
|---|---|
| Choosing an exam | Learning three memory product names |
| Understanding a blocking validation finding | Reading workflow essay on every hub visit |
| One why for today’s mission | Six paraphrases of the same why |
| Confirming publish | Watching embedding vector counts |
| Session question difficulty | Dashboard mosaic before mission start |

---

## Estimated reduction

After P0/P1 IA execution (content + structure, before visual polish):

| Path | Now | Target |
|---|---|---|
| Publish a subject (Workspace) | Very High | Moderate |
| Founder morning open (Overview) | Very High | Low–Moderate |
| Student start study (Home) | High | Low–Moderate |
| Understand progress | High | Moderate |

**Product-wide competing-element reduction on primary paths: ~35–45%.**

---

## Guardrail

Do not reduce cognitive load by removing **educational explainability**. Reduce by removing **duplicate** explainability and **non-decision** chrome.
