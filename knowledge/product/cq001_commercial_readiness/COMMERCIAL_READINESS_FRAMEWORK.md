# Commercial Readiness Framework

**Programme:** CQ-001 — Commercial Readiness First  
**Version:** 1.0  
**Status:** Active — permanent Version 1 commercial-quality measurement and prioritisation authority  
**Effective:** 2026-07-28  
**Authority:** Product measurement law (subordinate to Vision 2030; complementary to KSI / P-001.1, P-002.1, OA-001 Product Constitution)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

This framework defines **how Kwalitec measures commercial readiness for Version 1** and **how Version 1 work must be prioritised**.

It exists so that:

- every Version 1 programme can estimate its contribution to founder-trusted daily use;
- work that does not measurably improve CRI is deferred to the Version 2 backlog;
- CRI claims stay evidence-bound (provisional vs validated);
- milestone tags (`cri-45` … `v1.0.0`) are only created when thresholds are genuinely achieved.

**CRI is not a second north star.** Vision 2030 remains the educational north star. KSI remains the educational-usefulness index. P-002.1 remains the production-ready gate law. CRI is the **operational commercial-quality index** for whether Version 1 is becoming the founder’s trusted, premium daily study operating system.

---

## 2. Version 1 objective

### 2.1 Objective statement

**Version 1 commercial progress** requires continuous, efficient increase of:

> **Commercial Readiness Index (CRI)**

while maintaining Version 1 scope discipline and without introducing Version 2 capabilities unless they directly improve current CRI.

### 2.2 Baseline and thresholds

| Measure | Value | Authority |
|---|---|---|
| Current baseline CRI | **43%** | [`BASELINE_CRI_ASSESSMENT.md`](BASELINE_CRI_ASSESSMENT.md) |
| Living board | [`COMMERCIAL_READINESS_BOARD.md`](COMMERCIAL_READINESS_BOARD.md) | Updated each CRI-affecting programme |
| Milestone tags | `cri-45`, `cri-50`, `cri-60`, `cri-70`, `cri-80`, `cri-90`, `v1.0.0` | Create **only** when threshold genuinely achieved |

`v1.0.0` additionally requires P-002.1 production-ready declaration — CRI alone is insufficient.

### 2.3 What CRI success is not

CRI progress is **not**:

- marketing launch readiness alone (CR9 is last in priority);
- KSI ≥ 80 alone (necessary for educational claims; not identical to commercial daily OS trust);
- engineering Conditional GO alone (CR7 is maintain-first);
- feature volume, Twin redesign, or Version 2 surface expansion.

---

## 3. Definition — Commercial Readiness Index (CRI)

### 3.1 Formal definition

The **Commercial Readiness Index (CRI)** is a weighted composite score (0–100, reported as a percentage) that estimates **how ready Kwalitec is to serve as a premium, founder-trusted daily study operating system** across nine commercial-quality domains.

CRI answers:

> If the founder used Kwalitec every day as their study OS, how commercially ready is the product — for substance, habit, trust, craft, evidence, and eventual commercial envelope — not merely for having features present?

### 3.2 Design principles

| Principle | Rule |
|---|---|
| Founder daily OS | Scores reward reliable daily study operation, not demo theatre |
| Scope discipline | Version 2 work deferred unless it directly raises current CRI |
| Evidence-bound | Domain scores require cited evidence; provisional vs validated must be labelled |
| Explainable | Every domain score must state why it was assigned |
| Efficient gain | Prefer smallest change with largest honest CRI delta |
| Non-greenwash | Do not re-weight domains mid-flight to manufacture threshold tags |

### 3.3 Relationship to existing systems

| System | Owns | Relationship to CRI |
|---|---|---|
| Vision 2030 | North star / Final Test | CRI serves founder trust in daily use toward that north star |
| KSI (P-001.1) | Educational usefulness | Overlaps CR1–CR4/CR8; KSI ≠ CRI; both may move together |
| P-002.1 gates | Production-ready declaration | Orthogonal gate law; `v1.0.0` needs both readiness and CRI maturity |
| ER-002 / CR7 | Engineering claim class | Feeds CR7; do not improve CR7 unless justified |
| Commercial tracker (historical) | Public launch / pricing | Maps primarily to CR9 — last priority |

---

## 4. CRI domains and weightings

Weights sum to **100**. Weights reflect Version 1 commercial priorities: core loop and habit first, then session substance and guidance trust, then cohesion/craft/evidence, with operations maintained and commercial envelope last.

| ID | Domain | Weight | Priority rank |
|---|---|---:|---:|
| CR1 | Core Study Loop | 18 | 1 |
| CR2 | Daily Habit Fit | 14 | 2 |
| CR4 | Session Substance | 14 | 3 |
| CR3 | Guidance Trust | 12 | 4 |
| CR5 | Experience Cohesion | 10 | 5 |
| CR6 | Premium Craft | 8 | 6 |
| CR8 | Evidence Confidence | 10 | 7 |
| CR7 | Operational Reliability | 8 | 8 (maintain) |
| CR9 | Commercial Envelope | 6 | 9 |
| | **Total** | **100** | |

Weight changes require an explicit Product amendment to this document (version bump + rationale).

### 4.1 Domain definitions

#### CR1 — Core Study Loop (18%)

**Definition:** Plan → primary recommendation → session start → meaningful completion → clear next step works as one reliable loop without dead ends, contradictory facts, or “what now?” moments.

**Founder benefit:** The product is usable as the primary daily study path.

#### CR2 — Daily Habit Fit (14%)

**Definition:** The product fits scarce daily study time: duration-aware planning, realistic missions, low restart friction, and continuity across days.

**Founder benefit:** Studying with Kwalitec becomes habitual rather than episodic.

#### CR4 — Session Substance (14%)

**Definition:** In-session work feels educationally substantive (questions, feedback, progress that matters) rather than empty activity or UI busywork.

**Founder benefit:** Time spent in sessions feels worth the attention.

#### CR3 — Guidance Trust (12%)

**Definition:** Recommendations, readiness, and explanations are believable, proportionate, and actionable — the founder trusts “what to do next.”

**Founder benefit:** Guidance is followed without second-guessing the product.

#### CR5 — Experience Cohesion (10%)

**Definition:** Home, Coach, Journey, Plan, Mission, and Session share one coherent story (single facts, consistent language, no competing authorities).

**Founder benefit:** The product feels like one OS, not a kit of screens.

#### CR6 — Premium Craft (8%)

**Definition:** Visual, interaction, and copy quality feel intentionally premium for a serious professional product — calm, clear, non-generic.

**Founder benefit:** Daily use feels like a product the founder is proud to operate.

#### CR8 — Evidence Confidence (10%)

**Definition:** Claims the product (and team) make are backed by appropriate evidence class; educational and commercial assertions do not outrun filed proof.

**Founder benefit:** The founder can speak honestly about what works.

#### CR7 — Operational Reliability (8%)

**Definition:** Invite-only / Alpha operation is safe enough: deployability, observability, security posture, and known HOLDs are managed without surprise failure.

**Founder benefit:** Running the product does not create operational anxiety. **Improve only when justified** — maintain first.

#### CR9 — Commercial Envelope (6%)

**Definition:** Pricing, packaging, public registration, and go-to-market readiness for eventual commercial offer.

**Founder benefit:** Path to revenue exists when educational/commercial freezes clear. **Last priority** for Version 1 optimisation.

---

## 5. Scoring methodology

### 5.1 Domain score (0–100)

Each domain is scored 0–100 with a short rationale and evidence citations.

| Band | Score | Meaning |
|---|---|---|
| Broken / absent | 0–24 | Domain fails for daily founder use |
| Weak | 25–44 | Present but unreliable or untrustworthy |
| Emerging | 45–64 | Usable with known friction |
| Strong | 65–84 | Reliable for invite-only daily use |
| Premium | 85–100 | Ready to defend as commercial-quality |

### 5.2 CRI formula

\[
\mathrm{CRI} = \sum_{d \in \{\mathrm{CR1}\ldots\mathrm{CR9}\}} \left(\mathrm{score}_d \times \frac{\mathrm{weight}_d}{100}\right)
\]

Report as integer percentage (round half up). Example: weighted sum 42.84 → **43%**.

### 5.3 Provisional vs validated

| Status | Meaning | Allowed use |
|---|---|---|
| **Provisional** | Estimated from internal evidence (dogfood notes, blind reviews, engineering artefacts, product boards) | Prioritisation; programme ΔCRI estimates; board trend |
| **Validated** | Re-scored against an agreed evidence package (founder dogfood window + cited artefacts; optional Tier B when student-facing) | Milestone tags `cri-45`+; public/internal commercial-quality claims |

**Rule:** Do not create `cri-*` tags on provisional-only increases. Threshold achievement must be **validated** (or an explicit Founder Review accepting provisional for that tag — exceptional; record on the Board).

### 5.4 Programme ΔCRI

Every material Version 1 programme completion must report:

| Field | Requirement |
|---|---|
| CRI domains improved | Which of CR1–CR9 |
| Estimated CRI delta | Net points (may be 0 with rationale) |
| Evidence supporting the increase | Paths / artefacts |
| Remaining blockers | What still caps the domain(s) |
| Provisional or validated | Label the delta |

Docs/infra programmes may record ΔCRI = 0 with rationale, but must still complete the pre-task intake fields when they consume Version 1 capacity.

---

## 6. Working rules (normative)

### 6.1 Pre-task intake (mandatory)

Before starting any Version 1 task, identify:

1. **CRI domains affected**
2. **Expected CRI increase**
3. **Founder benefit**
4. **Release risk**

Use [`TASK_INTAKE_TEMPLATE.md`](TASK_INTAKE_TEMPLATE.md).

### 6.2 Deferral rule

If a task does **not** measurably improve CRI → defer to [`VERSION_2_BACKLOG.md`](VERSION_2_BACKLOG.md).

Do **not** introduce Version 2 capabilities unless they directly improve current CRI.

### 6.3 Priority order

Execute Version 1 work in this order unless a higher domain is already Strong (≥ 65) **and** a Founder Review authorises skipping down:

```
CR1 Core Study Loop
  ↓
CR2 Daily Habit Fit
  ↓
CR4 Session Substance
  ↓
CR3 Guidance Trust
  ↓
CR5 Experience Cohesion
  ↓
CR6 Premium Craft
  ↓
CR8 Evidence Confidence
  ↓
CR7 Operational Reliability (maintain; improve only when justified)
  ↓
CR9 Commercial Envelope
```

### 6.4 Living board

Maintain [`COMMERCIAL_READINESS_BOARD.md`](COMMERCIAL_READINESS_BOARD.md) with:

- Current CRI  
- Domain scores  
- Trend  
- Active blockers  
- Current highest-priority programme  
- Next recommended programme  

Update at programme start and completion.

### 6.5 Git discipline

- Commits use Conventional Commits describing the **commercial-quality improvement** (e.g. `feat(cr1): …`, `docs(cq-001): …`).  
- Milestone tags (`cri-45` … `v1.0.0`) only when agreed thresholds are **genuinely achieved**.  
- Never create these tags prematurely.

---

## 7. Success criterion

Every completed programme should leave Kwalitec **measurably closer** to being the founder’s trusted, premium daily study operating system — evidenced by Board CRI movement (provisional or validated) and honest residual blockers.

---

## 8. Amendment

1. Propose change with impact on CR1–CR9 weights or definitions.  
2. Founder Review (Product Owner capacity).  
3. Version bump this file; update Board; note on OA-001 Programme Dashboard.  
4. Do not amend Vision 2030, KSI weights, or P-002.1 gates through this process.

---

**End of Commercial Readiness Framework**
