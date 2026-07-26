# Student Impact Assessment — EP-007.1

**Template:** `../p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Programme / Milestone ID** | EP-007.1 |
| **Title** | Student Journey Consolidation |
| **Date** | 2026-07-26 |
| **Author** | Product / Engineering |
| **Student-visible change?** | Yes (when `KWALITEC_V2_SOLE_RUNTIME=1`) |
| **Production activation?** | Yes — production already sets sole runtime; this programme completes entry / duration / CTA consistency |
| **Related KSI categories** | K1, K5 (primary); K8 adjacency |

---

## 1. Student problem

**Student problem:**

> Students met two “homes” and two clocks for the same night of study — Dashboard vs Student Home, and 30 vs 90 minutes — so the product reintroduced the decision fatigue it claims to remove.

**Evidence:**

> EP-004 blind-review corpus (Near Universal dual-home / duration themes); EP-005.2 Student Journey Review + REM-02 / REM-03; EP-006.3 / EP-006.5 Tier B residuals naming dual homes as a trust cap after MES and readiness delivery.

---

## 2. Student benefit

| Design question | Helped? | How |
|---|---|---|
| What should I do now? | Yes | One Home after login; one Start / Resume path |
| How am I progressing? | Partial | Same journey continuity; no new progress math |
| What is stopping me? | Yes | Removes “which home / which clock?” friction |
| What happens next? | Yes | Session complete returns to the same Home |

**Student benefit summary:**

> Under sole runtime, students enter one Home, see one planned duration, start one session model, and return to the same Home — without competing Dashboard/Missions entry points.

**Final Test:** Does this help students become better professionals? **Yes** — by reducing organisational load so study time goes to learning, not navigation.

---

## 3. Learning benefit

| Check | Answer |
|---|---|
| Reinforces consistency / feedback / reflection / revision / confidence / understanding mistakes? | Reinforces **consistent nightly workflow**; reflection/session surfaces unchanged in educational meaning |
| Risks rewarding activity vanity? | No — presentation routing only |
| Educational Constitution / honesty risks? | Mitigated — duration prefers student-declared preferred session length; no invented mastery |

**Learning benefit summary:**

> Learning improves when the product stops fracturing “tonight’s plan” across two UIs. Educational decisions still come from Runtime A services; this programme makes those decisions reachable on one path.

---

## 4. Success metrics

| Metric | Baseline | Target | Result | Owner |
|---|---|---|---|---|
| Dual-home reachable under sole runtime | Yes (bounce / CTAs) | No competing home | **Removed** (redirects + entry helpers) | EP-007.1 |
| Duration agreement (preferred vs legacy) | Mismatch (30 vs 90) | Same preferred fact | **Aligned** via shared resolver | EP-007.1 |
| Login → canonical Home | Via Dashboard bounce | Direct | **Direct** under sole runtime | EP-007.1 |
| Tier B dual-home theme | Residual Fail | Majority clear | **Deferred** — ready for validation pack | Successor |

---

## 5. Estimated KSI contribution

| Category | ID | Weight | Delta | Rationale |
|---|---|---:|---:|---|
| Planning usefulness | K1 | 15 | +4 | Removes experiential dual-home / duration cap (est.; Tier B required) |
| Recommendation usefulness | K2 | 15 | 0 | No ranking change |
| Readiness usefulness | K3 | 12 | 0 | No readiness math |
| Personalisation | K4 | 12 | 0 | |
| Motivation | K5 | 10 | +3 | Lower decision fatigue on start path |
| Learning analytics | K6 | 10 | 0 | |
| Revision support | K7 | 12 | 0 | |
| Explainability | K8 | 14 | +1 | Consistency across surfaces (adjacency) |
| **Net ΔKSI** | | | **≈ +1.0** | Prefer-lower; **not validated** |

**Confidence:** Medium (implementation) / Low for claimable lift until Tier B  
**Assumes:** Production sole runtime ON; personalisation flags OFF; no educational service changes  

Weighted estimate: \(0.15\times4 + 0.10\times3 + 0.14\times1 \approx 1.04\). Under-claim **≈ +1.0**. Do **not** raise validated KSI until Tier B.

---

## 6. Validation plan

| Method | When | Success | Failure |
|---|---|---|---|
| Regression suite | This programme | Canonical nav / duration / compat pass | Redirect or duration regress |
| Tier B journey pack | Successor | Dual-home theme majority clear; duration conflict cleared | Reviewers still see two homes / clocks |
| Validated KSI update | After Tier B | Claimable K1 lift | Hold estimated-only |

---

## 7. Risks

| Risk | Likelihood | Impact | Student effect | Mitigation |
|---|---|---|---|---|
| Alpha dual-run confusion if flags mixed | Med | Med | Some cohorts still see Dashboard | Document flag posture; sole OFF preserves dual-run |
| Bookmarks to `/dashboard/` surprise redirect | Med | Low | Brief bounce | Redirect to Home; retain shells |
| Over-claiming K1 without Tier B | Med | High | False usefulness claims | Prefer-lower; defer validated lift |
| Welcome modal only on Home under sole | Low | Low | First-run CTA | Welcome included on Student Home |

---

## 8. Assumptions

1. Production continues `KWALITEC_V2_SOLE_RUNTIME=1`.
2. Preferred session minutes remain the honest session-length contract students set in the plan wizard.
3. Runtime A ownership of recommendations / planning / readiness remains unchanged.
4. Tier B will re-test dual-home / duration perception before validated KSI changes.

---

## 9. Evidence collected (exit)

| Evidence | Path / ID | Supports which claim? |
|---|---|---|
| Consolidation design | `STUDENT_JOURNEY_CONSOLIDATION.md` | Single journey design |
| Traceability | `JOURNEY_TRACEABILITY.md` | Path / ownership map |
| Regression tests | `tests/presentation/test_canonical_journey.py` | Nav, duration, compat |
| Prior findings | EP-005.2 / EP-006.3 / EP-006.5 | Problem evidence |

---

## 10. Lessons learned for student value (exit)

> Dual-home friction is a **presentation topology** problem: MES and readiness delivery can Pass while students still distrust the product if two homes compete. Consolidating entry and duration is necessary before Tier B can honestly clear REM-02 / REM-03 residuals — and estimated K1 lift must stay under-claimed until perception re-test.

---

## Appendix A — Blast radius

| Cohort / flag state | Student-visible change |
|---|---|
| Production (`SOLE_RUNTIME=1`) | Single Home; preferred duration; login → `/student/` |
| Dual-run / Alpha (`SOLE_RUNTIME=0`) | Dashboard home retained; duration still prefers preferred minutes |
| `UNIFIED_JOURNEY` ON/OFF | Unchanged — guided chrome independent |

---

**End of STUDENT_IMPACT_ASSESSMENT**
