# Student Impact Assessment — EP-003.4

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-003.4 |
| **Title** | Learning Feedback Loop |
| **Date** | 2026-07-26 |
| **Author** | Auto (programme execution) |
| **Student-visible change?** | No direct UX change — observational infrastructure gated OFF by default |
| **Production activation?** | Gated — `KWALITEC_LEARNING_FEEDBACK` default OFF |
| **Related KSI categories** | K6 (primary), K4 (supporting), K2/K1/K3 enabling (0 direct claim) |

**Template:** [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)

---

## 1. Student problem

**Student problem:**

> Students do not feel today’s tip, readiness, or plan “learns” from how they actually respond. The product can improve explanation quality (EP-003.1–3) but still lacks a governed way to observe whether students accept tips, complete plans, miss sessions, or keep study rhythm — so future personalisation risks guessing rather than observing.

**Evidence:**

> EP-003.1 deferred acceptance/completion instrumentation; EP-003.2 lacks readiness history; EP-003.3 recovery is signal-driven without outcome attribution; P-001.1 K6 Learning analytics = Partial (~50).

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | N/A (this milestone) | No new guidance speech |
| How am I progressing? | Indirect / future | Enables later honest progress analytics from observed behaviour |
| What is stopping me? | Indirect / future | Missed-session / recovery observations available for review |
| What happens next? | N/A (this milestone) | No automatic adaptation yet |

**Student benefit summary:**

> Immediate student UX is unchanged. The benefit is **trustworthy future adaptation**: when Kwalitec later personalises, it can cite observed interactions rather than inventing educational conclusions from clicks alone.

**Final Test:** Does this help students become better professionals? **Yes (enabling)** — professionals learn from honest feedback loops; this installs the observational substrate without pretending it already improves learning.

---

## 3. Learning benefit

- Separates observed behaviour from mastery claims (protects educational honesty).
- Prevents “acceptance = learning” anti-pattern.
- Keeps one educational brain: services still decide; feedback only records.

---

## 4. Success metrics

| Metric | Target | Measurement |
|---|---|---|
| Events recorded when flag ON | Deterministic for emit paths | Unit tests |
| Fail-open on recorder failure | Student path continues | Integration tests |
| Forbidden inference rejected | 100% of forbidden keys | Contract tests |
| Student-visible regression | None | No presentation changes |

---

## 5. Risks to students

| Risk | Mitigation |
|---|---|
| Future misuse of accept as mastery | Claim boundaries + constitution docs |
| Silent adaptation without review | Explicit STOP — no closed loop this programme |
| Privacy concern if durable store later | Process-local now; future publish must review PII |

---

## 6. Assumptions

- Flag remains OFF in production until product/architecture review.
- Live KSI lift from analytics (K6) requires later durable analytics + cohort validation.
- Title-based revision adherence is a temporary heuristic.

---

## 7. Blast radius (appendix)

| Surface | Effect when flag OFF | Effect when flag ON |
|---|---|---|
| Dashboard / tips / readiness / plan UX | Unchanged | Unchanged (side-effect recording only) |
| Decision Journal | Unchanged | Also emits preference feedback |
| Twin | Unchanged | Unchanged (no Twin write) |
| Presentation adapter | Unchanged | Unchanged |
