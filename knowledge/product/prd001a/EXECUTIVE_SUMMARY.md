# PRD-001A — Executive Summary

**Programme:** PRD-001A — Product Integrity & Blueprint Conformance Audit  
**Status:** Investigation complete  
**Date:** 2026-07-27  
**Scope:** Evidence only — no code, UI, architecture, or migration changes  
**Authority inputs:** `PRODUCT_BLUEPRINT.md` v1.1, Vision 2030, Educational Constitution, live Runtime A + EOS student surfaces under production flags (`render.yaml`)

---

## Verdict

Kwalitec **partially delivers** the Education Operating System described in the Product Blueprint.

The platform **does** answer “what to study next” for an invite-only Internal Alpha student with an active study plan. Curriculum is loaded, missions are generated, explainability fields exist on Home, Readiness and Journey surfaces exist, and DEP-003 unified the student chrome.

The platform **does not yet feel** like the evidence-driven Digital Twin companion promised by the Blueprint’s educational model. The dominant gap is not missing Flask routes — it is a **student-perceivable disconnect** between:

1. **Syllabus-sequential Learning Mode mission selection** (intentional Version 1 law), and  
2. **Blueprint / landing language** that implies personalised educational intelligence driven by understanding, readiness, and Twin state.

Founder observations about generic missions, hidden origin, invisible CMP, absent Twin, and Estimated Knowledge not shaping today’s session are **largely confirmed as product-experience gaps**, with precise category classifications below.

---

## What is real

| Capability | Student-visible reality (sole runtime) |
|---|---|
| Curriculum Intelligence | Official IFoA CS1/CM1/CB2 2026 JSON imported; V1+V2 traversal works |
| Study Plan | Exam-date wizard creates plan + `TopicProgress` rows |
| Today’s Mission | Persisted daily mission; typically next incomplete syllabus leaf |
| Explainability (MES) | Home shows Why / Why now / Next / Benefit + L2 disclosure |
| Readiness | Home panel with drivers/evidence disclosure |
| Journey | `/student/journey` maps current / completed / upcoming topics |
| Session + Reflection loop | Guided session path exists; commitment/reflection hooks on Home |
| EOS shell | DEP-003 — one student chrome under `KWALITEC_V2_SOLE_RUNTIME=1` |

---

## What is not what students expect

| Founder observation | Audit finding | Category |
|---|---|---|
| Daily Mission feels generic | Learning Mode selects first incomplete topic only; duration/tasks from plan minutes + preference templates — not Twin/EK | B + intentional V1 law |
| Title ≠ active curriculum | Titles include topic when bound (`Study {code} {name} — Day, Date`); generic fallbacks remain if curriculum unbound | A/B (when bound) / D (fallback) |
| Cannot see recommendation origin | Explainability exists, but does not clearly say “next incomplete syllabus leaf in CS1 order” | B |
| Dashboard ≠ syllabus progression | Journey page has progression; Home Journey panel is a short story, not a syllabus map | A/C |
| CMP workflow absent | Student CMP upload was never a product path; CMP is founder Studio packaging + BYO materials | E (student) / C (Studio UI) |
| Syllabus mapping invisible | No student-facing official syllabus / chapter / LO map comparable to CMP | E (student syllabus map) |
| Digital Twin not apparent | Twin is backend-only, **OFF** in production `render.yaml`, and deliberately unnamed in UI | A (by design) + D (authority off) |
| Estimated Knowledge not influencing recommendations | EK drives **weak-topic recommendations**; does **not** select Learning Mode mission topic; EK barely visible on EOS Home | A/C (visibility) + intentional selection law |

---

## Highest-value integrity gap

**Students cannot reconcile the landing promise (“Know exactly what to study next” as an Education Operating System) with the actual decision rule (syllabus order until revision stage), because the product neither names that rule clearly nor surfaces Estimated Knowledge / syllabus position on the primary Home decision surface.**

Closing this gap does **not** require enabling every Twin flag on day one. Highest-value work is to make the **true Version 1 educational contract** visible and trustworthy:

1. State clearly why today’s session exists (curriculum progression rule).  
2. Elevate syllabus position + completion on Home.  
3. Surface Estimated Knowledge where it already exists (Study Plan) into the EOS decision loop — or stop implying understanding drives today’s pick.  
4. Keep Twin/adaptive interruption as Version 2 cutover, not silent expectation.

---

## Document map

| Deliverable | Path |
|---|---|
| Capability inventory | `BLUEPRINT_CAPABILITY_MATRIX.md` |
| Implementation status | `IMPLEMENTATION_MATRIX.md` |
| Student experience | `STUDENT_EXPERIENCE_AUDIT.md` |
| Curriculum path | `CURRICULUM_INTELLIGENCE_AUDIT.md` |
| CMP | `CMP_AUDIT.md` |
| Mission trace | `MISSION_GENERATION_AUDIT.md` |
| Explainability | `EXPLAINABILITY_AUDIT.md` |
| Readiness / EK | `READINESS_AUDIT.md` |
| Dashboard components | `DASHBOARD_INTEGRITY_AUDIT.md` |
| Landing vs hour-one | `PRODUCT_PROMISE_AUDIT.md` |
| Gap taxonomy | `GAP_CLASSIFICATION.md` |
| Next work | `RECOMMENDED_ROADMAP.md` |
| Programme close | `COMPLETION_REPORT.md` |

---

## Explicit non-claims

- This programme did **not** change application code, templates, flags, or migrations.  
- This is **not** a UI aesthetic audit, code-quality audit, or architecture redesign.  
- Version 1 Blueprint already states Twin-first authority is **not** fully cut over on every legacy path — the audit measures student experience against that honesty, not against an imaginary finished Twin product.
