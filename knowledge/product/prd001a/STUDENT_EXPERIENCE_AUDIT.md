# PRD-001A — Student Experience Audit

**Lens:** Ignore internal elegance. Evaluate what a student can perceive and decide after sign-in under sole runtime (`/student/*`).  
**Primary surfaces:** Login landing, Home, Journey, Revision, History, Study Plan, Session, Help/Onboarding.

---

## Experience questions

| # | Question | Answer | Evidence | Gap category |
|---|---|---|---|---|
| 1 | Can a student tell **why today's mission exists**? | **Partially.** Home shows Why / Why now / Next when MES fields populate. The underlying rule (“first incomplete syllabus leaf”) is rarely stated in plain curriculum language. | `home.html` MES L1 fields; `_select_topic_for_today` docstring (IA-004 Learning Mode) | B |
| 2 | Can a student see **curriculum progression**? | **Yes, if they open Journey or Study Plan.** Home Journey panel is a short story, not a syllabus map. | `/student/journey` timeline; Home `journey_story` | A/C |
| 3 | Can a student identify **today's chapter / topic**? | **Usually yes when mission is bound** — title pattern `Study {topic} — Day, Date`. Cold start / unbound fallbacks look generic (`Daily Study — …`). | `PlanningService` title generation ~L1006–1012 | B / D |
| 4 | Can a student see **syllabus completion**? | **Yes on Journey** (completed/upcoming) and Study Plan roadmap. Not as a first-viewport Home map. | `journey.html`; `study_plan/view.html` | A |
| 5 | Can a student understand **Estimated Knowledge**? | **Weak on EOS.** EK appears on Study Plan roadmap as `%`. Not on Home/Journey/History student templates. Constitution expects visibility when material. | Study Plan templates; no EK under `templates/student/` | A/C |
| 6 | Can a student understand **Readiness**? | **Yes at a glance + disclosure.** Home Readiness panel + “Why this estimate?” | `home.html` readiness article | — (meets bar when data exists) |
| 7 | Can a student understand **Coach**? | **Ambiguous.** Coach often repeats Mission explainability or shows cold-start placeholder / commitment status. Does not feel like a distinct Twin coach. | `home.html` Coach panel; PX-002A dedupe comments | B |
| 8 | Can a student recognise **learning milestones**? | **Partially.** Journey completed topics; History achievements/narrative; commitment “Session complete” reflection block. No strong milestone ceremony for syllabus sections. | Journey / History / Home commitment | B |
| 9 | Can a student understand **recommendations**? | **Partially.** Primary CTA is clear when MES is complete; alternatives in L2 disclosure. Competing signals (Readiness Next vs Mission Next) can dilute. | Home hero + explanation_card | B |
| 10 | Can a student **trust** recommendations? | **Fragile.** Trust UX exists (confidence, honest refusal, commitment/defer). Trust is undermined when students expect adaptive understanding-driven picks but receive syllabus-order missions without that contract being named. | EP-008.1 trust fields; Learning Mode law | B + educational contract gap |

---

## Founder observation check

| Observation | Student-experience confirmation |
|---|---|
| Daily Mission appears generic | Confirmed risk when topic label missing or when tasks are template splits of minutes without curriculum narrative depth |
| Mission title ≠ curriculum | Partially — when bound, titles encode syllabus topic; student may still not see section/chapter hierarchy |
| Cannot identify recommendation origin | Confirmed — origin is “decision packaging”, not “CS1 §1.1 next incomplete leaf” |
| Dashboard disconnected from syllabus | Confirmed on Home first viewport; Journey/Study Plan recover it |
| CMP workflow absent | Confirmed — no student CMP path |
| Syllabus mapping not visible | Confirmed as Home gap; partial on Journey |
| Digital Twin not apparent | Confirmed and **intentional** (product language); Twin also OFF in production |
| Estimated Knowledge not influencing recommendations | Confirmed for **mission topic**; false for **weak-topic recommendation rules** — but student cannot see EK driving anything on Home |

---

## Cold-start (brand-new student, first hour)

Typical path: login → onboarding gate → Study Plan wizard → calibration → Home.

| Moment | Experience |
|---|---|
| Before plan | Wizard in EOS chrome (DEP-003) — planning promise held |
| After plan, before sessions | Home may show mission once generated; Journey empty state until first session; Coach placeholder; Readiness thin |
| First mission | CS1 “not started” → topic **1.1** sequential — correct under V1 law, but feels non-personalised |
| Understanding gauges | EK remains 0 / not evidence-backed until practice outcomes — easy to misread as “system doesn’t know me” |

---

## Student experience verdict

The EOS shell successfully presents **one product**. It does **not** yet present **one intelligible educational contract**. Students can start a focused session. Students struggle to see themselves as progressing through an official syllabus under an understanding model.

**Primary experience failure mode:** Promise of personalised educational intelligence vs delivery of honest syllabus sequencing — without naming the latter.
