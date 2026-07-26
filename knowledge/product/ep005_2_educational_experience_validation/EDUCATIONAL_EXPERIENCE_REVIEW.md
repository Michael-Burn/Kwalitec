# EP-005.2 — Educational Experience Review

**Programme:** EP-005.2 — Educational Experience Validation  
**Version:** 1.0  
**Date:** 2026-07-26  
**Status:** Evidence audit (no runtime / UI / API changes)  
**Validated baseline:** KSI **59** (EP-005.1 W-PROD)  
**Does not:** Implement remediations; does not amend constitutions  

---

## 1. Executive verdict

Runtime A intelligence from EP-003.1–.3 delivered **schema-complete, checklist-passing** recommendation, readiness, and planning contracts. Validated educational usefulness moved only **58 → 59**. The dominant explanation is not “the engines are wrong” — it is that **correct reasoning is often invisible, collapsed, inconsistent across homes, or gated OFF**, so students cannot use it as educational authority.

| Lens | Finding |
|---|---|
| Structural capability | Partial–Strong (contracts, tests, P-001.2/P-001.3 Pass) |
| Student-perceived usefulness | Weak–Partial (pre-change blind corpus; no post-change Tier B) |
| Version 1 G1 | **FAIL** (gap 21; K8 65 &lt; 70; effectiveness NO-GO) |

---

## 2. Scope of review

| Reviewed | Sources |
|---|---|
| Product Success Framework | `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` |
| Version 1 Release Framework | `../p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` |
| EP-003.1–.4 / EP-004.1–.3 | Completion, SIA, KSI impact, explainability/recommendation reviews |
| EP-005.1 validation | Validated report, evidence register, G1 status, confidence |
| Student surfaces | Dashboard / Student Home / Mission / Session / Analytics templates + presentation adapters |
| Perception corpus | EP-004 SV-001–020; Meta Analysis V2; Evidence-to-Strategy |

Constitutional STOP check: recommendations below preserve Vision Final Test, Educational honesty, Architecture one-runtime, and forbid opaque AI educational truth. No remediation proposed here invents a second educational brain or mastery theatre.

---

## 3. Explainability audit

Evaluate against P-001.2 levels and Mandatory Explanation Schema (MES).

### 3.1 Visibility

| Surface | MES in service payload? | Student-visible completeness |
|---|---|---|
| RecommendationService → legacy Dashboard expand | Yes | Partial — Observed/Estimates/Advice when expanded |
| RecommendationService → canonical Coach | Yes | **Poor** — compressed prose; evidence card unused on Home |
| PlanningService → Mission / Unified Journey | Yes | Partial — “why” labels; drivers/review_point unbound |
| ReadinessService → Analytics | Yes | Partial — narrative + evidence basis; drivers unbound |
| ReadinessService → canonical Home card | Yes | **Poor** — metric/confidence without why/evidence |
| Personalisation factors (EP-004.2/.3) | When flag ON | **Absent in templates** — no binding found |
| `review_point`, `change_reasoning`, `*_drivers` | Attached | **No direct template keys** found in inventory |

**Finding:** Explainability Pass at service/review level **overstates** student-visible explainability. This is the primary mechanism keeping validated **K8 at 65** (below V1 floor 70).

### 3.2 Timing

| Pattern | Assessment |
|---|---|
| Why before commit (plan/start) | Inconsistent — often collapsed behind disclosure or thin overview |
| Why after answer (session activity) | Good on canonical activity explanation cards |
| Why after poor practice (adaptation) | **Missing in perception** — “ledger update, not intelligent response” (SV-012) |
| Why on readiness change | Weak — change_reasoning not surfaced as dedicated control |

### 3.3 Length

| Level (P-001.2) | Observed behaviour |
|---|---|
| Level 1 (≤40 words, why + next) | Often replaced by generic “highest-value / learning evidence” speech **or** omitted when collapsed |
| Level 2 (≤120 words / scan ≤45s) | Available in expand patterns on some legacy surfaces; not default on Coach |
| Level 3 diagnostic | Not required on daily path — correctly avoided; but Level 2 opt-in is uneven |

### 3.4 Usefulness

Students trusted **falsifiable rules** (e.g. Learning Mode next unfinished topic) more than composite intelligence speech (SV-014). Usefulness fails when explanations:

- restate the mission without new instructional value;  
- cite “learning evidence” beside empty Readiness/Journey;  
- omit alternatives considered;  
- omit weak-topic naming after shock assessments.

### 3.5 Consistency

EP-002.8 consolidated Runtime A narrators on Dashboard / Analytics / Mission index (consistency score reported 0.92) but **explicitly excluded** `/student/*` and session start/outcome forms. Dual-stack presentation remains a consistency debt. Same decision class can appear as expandable EIP-003 blocks on legacy and opaque Coach prose on canonical Home — violates spirit of P-001.2 principle P7 for student experience even when adapters share a narrator inside one stack.

### 3.6 Correct reasoning students are unlikely to notice

| Runtime A artefact | Why students miss it |
|---|---|
| Plan coherence labels vs Mission authority | Easy to miss vs hero CTA; advisory vs authoritative distinction subtle |
| Decision Framework ladder rank | Not rendered as student control |
| Confidence level chips | Payload present; EP-002.8 accepted missing dedicated UI chip |
| Readiness drivers (coverage, knowledge, review, evidence density) | Flattened into prose / omitted on Home |
| Review points (“reassess after…”) | Schema field unbound |
| Change reasoning after new practice | Not a first-class completion/Home signal |
| Personalisation factors / profile explanation | Flag OFF; even when ON, no template binding |
| Honest refusal copy | Present in contracts; may feel like “emptiness” if not framed as protective honesty |
| Recovery plan rationale (lighter day) | Structural EP-003.3; perception of restorative restart still weak |

---

## 4. Recommendation experience assessment (K2)

| Dimension | Score band | Evidence |
|---|---|---|
| Discoverability | Partial | Tips appear on Dashboard / Home / Revision; Coach competes with Mission for attention |
| Clarity | Weak–Partial | Titles clear; reasons often generic or collapsed |
| Actionability | Partial–Strong | Next-action fields and CTAs exist; dual-home start friction remains |
| Trust | Weak | Near-universal Coach opacity; marketing freeze intact; no acceptance KPI |
| Perceived usefulness | Weak–Partial | Validated K2 **53** (floor only); organisational sequencing valued more than “intelligence” |

### Is RecommendationService quality limited by presentation rather than decision quality?

**Yes — primarily presentation and trust, for W-PROD.**

Evidence:

1. EP-003.1 Decision Framework, refusal, and plan-coherence contracts **Pass** with automated tests (EV-REC-001…003).  
2. Validated K2 rose only to **53** with Medium confidence and **no Tier B post-change perception**.  
3. Blind corpus distrust attaches to **speech without working**, not to documented wrong-topic-family failures in production defaults.  
4. EP-004.2 personalisation (estimated K2 +4) is flag OFF and would still need visible `personalisation_factors` to feel personal.

**Caveat:** Presentation fixes alone do not unlock recommendation-**effectiveness** marketing (EP-001 O8 / PRD). K2 Strong-band still needs acceptance / follow-through evidence (GAP-06).

---

## 5. Planning experience assessment (K1)

| Dimension | Assessment |
|---|---|
| Clarity | Strong on single path; weak under dual homes |
| Perceived workload | Undermined by 30-vs-90 duration conflict (Universal) |
| Recovery understanding | Structural recovery exists; restorative “smaller restart that counts” still missing in perception |
| Motivation | Calm non-shaming tone helps open the app; does not rebuild commitment after failure |
| Completion likelihood | Threatened when duration exceeds available weeknight time |

### Are PlanningService improvements visible enough to affect KSI?

**Partially — enough for validated +6 (62→68), not enough for Strong-band or large composite movement.**

EP-003.3 schema completeness, recovery paths, and explainability Pass support Partial-band credit. Residual dual-home / duration themes (EV-PLAN-006) and missing Tier B re-test **cap** further lift. EP-004.3 personalisation (estimated K1 +5) is invisible under flag OFF.

Weighted contribution of K1 +6 is only **+0.9** composite points — planning can improve without moving KSI much if other pillars stall.

---

## 6. Readiness experience assessment (K3)

| Dimension | Assessment |
|---|---|
| Score comprehension | Weak — number visible, meaning contested |
| Confidence understanding | Partial — labels exist; linkage to evidence thin on Home |
| Driver clarity | Weak — drivers in service, unbound in templates |
| Next-action usefulness | Partial — suggested action merged into narrative |

Validated K3 **57** (+5 vs baseline) credits honesty (refusal, separation of coverage vs readiness) more than unpackability cure. EP-003.2 explicitly did not recalibrate against exam outcomes.

**Risk:** Persuasive readiness language without inspectable drivers violates Educational honesty spirit even if estimates are “correct.” Prefer honest absence / Level-2 drivers over soothing composites.

---

## 7. Cross-cutting root pattern

```
Service contracts (MES, quality)  →  Adapter compression  →  Template subset rendering
         ↓                                    ↓                         ↓
   Checklist Pass                      Narrative prose              Student sees
   Estimated ΔKSI                      Lost fields                 Opacity / mismatch
```

EP-005.1 already rejected naive +12 estimate stacks. This programme adds the **experience mechanism**: validated usefulness stalls because the pipeline drops inspectability before the student.

Secondary pattern: **capability behind OFF flags** (feedback, profile, personalisation) cannot move K4/K6 in W-PROD — estimated closed-loop programmes are infrastructure relative to validated G1.

---

## 8. Constitutional alignment check

| Constraint | This review’s stance |
|---|---|
| Vision Final Test | Prefer inspectable nightly director over intelligence theatre |
| Never-Build / vanity | Do not remediate via streak pressure or activity dashboards |
| Educational Constitution | Keep refusal paths; separate facts/estimates/advice; no dual truths |
| Architecture Art. IV | Unexplainable guidance = incomplete — remediate visibility, not new brains |
| One Education OS runtime | Unify presentation path; do not add competing educational authorities |
| Product Constitution STOP | No recommendation herein requires constitution soft-amendment |

**STOP result:** No conflict requiring halt. Proceed to gap analysis and prioritised plan.

---

## References

- [`STUDENT_JOURNEY_REVIEW.md`](STUDENT_JOURNEY_REVIEW.md)  
- [`KSI_GAP_ANALYSIS.md`](KSI_GAP_ANALYSIS.md)  
- [`PRIORITISED_REMEDIATION_PLAN.md`](PRIORITISED_REMEDIATION_PLAN.md)  
- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`  
- `../p001_2_explainability_standard/EXPLAINABILITY_STANDARD.md`  
- `../p001_3_recommendation_quality_standard/RECOMMENDATION_QUALITY_STANDARD.md`  

---

**End of EDUCATIONAL_EXPERIENCE_REVIEW**
