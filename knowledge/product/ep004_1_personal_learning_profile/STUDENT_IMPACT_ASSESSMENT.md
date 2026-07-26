# Student Impact Assessment — EP-004.1

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-004.1 |
| **Title** | Personal Learning Profile |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | No direct UX change — profile infrastructure gated OFF by default |
| **Production activation?** | Gated — `KWALITEC_PERSONAL_LEARNING_PROFILE` default OFF |
| **Related KSI categories** | K4 (primary), K6 (supporting), K8 (supporting / explainability of attributes) |

**Template:** [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

---

## 1. Student problem

**Student problem:**

> Students experience tips, readiness, and plans that do not yet “know” their long-term study habits. After EP-003.4, the product can observe accept/dismiss, completion, recovery, and consistency — but those observations are not yet summarised into a stable, honest learning profile. Future personalisation therefore risks guessing or inventing preferences.

**Evidence:**

> EP-003.4 completion: feedback loop does not close into adaptation; P-001.1 K4 Personalisation remains a Version 1 gap; IA-003 student language already expects a “learning profile” without engineering “digital twin” jargon.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A (this milestone) | No new guidance speech / ranking |
| How am I progressing? | Indirect / future | Behavioural rates available for later honest analytics |
| What is stopping me? | Indirect / future | Consistency / recovery / completion summaries with confidence |
| What happens next? | N/A (this milestone) | No automatic adaptation yet |

**Student benefit summary:**

> Immediate UX is unchanged. The benefit is a **trustworthy personalisation substrate**: when Kwalitec later adapts study experience, it can cite observed behavioural attributes (with confidence and provenance) rather than inventing a profile.

**Final Test:** Does this help students become better professionals? **Yes (enabling)** — professionals improve when feedback is summarised honestly; this installs the profile without pretending it already personalises learning.

---

## 3. Learning benefit

- Separates observed / derived / unsupported attributes (protects educational honesty).
- Prevents “accept rate = mastery” and “recovery rate = fixed deficit” anti-patterns.
- Keeps one educational brain: Rec / Readiness / Planning still decide; profile only summarises.

---

## 4. Success metrics

| Metric | Target | Measurement |
|---|---|---|
| Profile aggregation deterministic | Identical evidence → identical serialize | Unit tests |
| Evidence provenance present | Derived attributes carry `evidence_refs` | Unit tests |
| Confidence updates with sample size | `min(1, n/10)` | Contract / aggregator tests |
| Fail-open on profile failure | Student path continues | Integration tests |
| No ownership delegation | Services use Port; collectors untouched | Ownership tests |
| Student-visible regression | None | Flag default OFF; no presentation changes |

---

## 5. Estimated KSI (summary)

See [`KSI_IMPACT_ASSESSMENT.md`](KSI_IMPACT_ASSESSMENT.md). Estimated weighted ΔKSI ≈ **+1.1** (K4 primary). Under-claimed pending durable profile UX and live re-score.

---

## 6. Validation plan

- Unit / integration tests in `tests/infrastructure/adapters/personal_learning_profile/`.
- Constitutional verification checklist.
- Live cohort personalisation usefulness deferred to a future closed-loop programme.

---

## 7. Risks to students

| Risk | Mitigation |
|---|---|
| Future misuse of profile as authority | Ownership tests + architecture STOP |
| Invented preferences | Unsupported attributes without evidence |
| Privacy if durable store later | Process-local now; future publish must review PII |

---

## 8. Assumptions

- Flag remains OFF in production until product/architecture review.
- Learning Feedback flag may be ON independently to supply events.
- Declared session minutes are optional observed preferences, not measured duration.

---

## 9. Evidence collected

- Tests: `tests/infrastructure/adapters/personal_learning_profile/`
- Architecture: `knowledge/architecture/PERSONAL_LEARNING_PROFILE_ARCHITECTURE.md`
- Programme folder artefacts

---

## 10. Lessons learned for student value

Observed evidence alone (EP-003.4) is necessary but not sufficient for personalisation claims. Students benefit only when observations become a **stable, explainable profile** that services can read without surrendering educational ownership. Over-claiming K4 from an offline aggregator would violate the Product Success Framework’s under-claim rule.

---

## Appendix A — Blast radius

| Surface | Effect when flag OFF | Effect when flag ON |
|---|---|---|
| Dashboard / tips / readiness / plan UX | Unchanged | Unchanged (consume is side-effect / optional input) |
| Decision Journal | Unchanged | May refresh profile after record |
| Twin | Unchanged | Unchanged (no Twin write) |
| Presentation adapter | Unchanged | Unchanged |
| Learning Feedback | Independent | Profile reads buffer when available |
