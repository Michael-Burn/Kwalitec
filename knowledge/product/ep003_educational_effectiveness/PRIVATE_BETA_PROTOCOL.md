# Private Beta Protocol

**Programme:** EP-003 — Workstream 2  
**Version:** 1.0  
**Status:** Protocol approved for operations — cohort expansion pending privacy sign-off  
**Updated:** 2026-07-24  
**Authority:** Product  
**Companion ops docs:** `knowledge/product/private_beta/`  
**Does not:** Redesign product, open public registration, or change educational algorithms

---

## 1. Purpose

Run a **closed private beta** that observes, measures, and interviews students against Educational Metrics (EP-003) and EP-001 outcomes — without public launch.

This protocol consolidates eligibility, consent, onboarding, feedback cadence, support, and exit criteria into one governing checklist. Detailed runbooks remain in `private_beta/`.

---

## 2. Eligibility

| Rule | Spec |
|---|---|
| Audience | IFoA (or designated professional exam) students preparing for an in-scope subject |
| Cohort size | Target **20–50** invite-only students (EP-001 exit bar) |
| Account model | Invite-only; **no** public self-service registration |
| Platform | Version 1 Platform Baseline (GA-certified operational surface + Education OS runtime) |
| Exclusions | Staff accounts used only for dogfooding do not count toward cohort N unless marked “participant” |
| Conflict | Anyone who cannot consent to measurement / interview terms is ineligible |

Provisioning: admin / controlled account creation only (`create-admin` or equivalent founder ops). Align with Vision Data Principles.

---

## 3. Consent

Before productive study data is used for effectiveness reporting:

1. **Privacy notice** — honest scope: what is stored, what analytics observe (metadata / hashes, not reflection body text), retention, support access.
2. **Measurement consent** — agreement that aggregate educational KPIs (M1–M9) and anonymised interview themes may inform product decisions.
3. **Interview consent** — optional separately; no coercion; decline does not remove study access.
4. **Quote consent** — optional for anonymous quotes in internal reports.
5. **Withdrawal** — student may withdraw measurement consent; ops follow export/delete path (manual acceptable in beta — see Privacy Review).

Privacy checklist must be signed before **expanded** cohort (`private_beta/PRIVACY_REVIEW.md`). Dogfood / founder accounts may proceed under internal alpha rules; external participants require checklist completion.

Analytics flag `ANALYTICS_EVENTS_V1` remains OFF until EP-002 go-live checklist allows staged activation for the beta environment.

---

## 4. Onboarding

Follow [`../private_beta/BETA_ONBOARDING.md`](../private_beta/BETA_ONBOARDING.md):

1. Invite + welcome note (intelligent study companion; learning outcomes, not gamification).
2. First Session — calibration / onboarding already in product; start Today's Session.
3. Orientation — Home, Journey, History, Revision, Reflection when prompted.
4. Expectations — bugs expected; educational honesty preferred; feedback channels linked.
5. No pass guarantees in welcome copy (Blueprint product promise).

**Success of onboarding (ops):** participant completes ≥1 productive Session within 7 days of invite acceptance.

---

## 5. Feedback cadence

| Cadence | Activity | Maps to |
|---|---|---|
| Continuous | In-product founder feedback + issue reports | Trust / defects |
| Week 1 | Check-in: understood? stuck? first Session done? | Activation |
| Week 2–3 | Check-in: consistency, reflection, Journey clarity | M3, M6, educational review |
| Week 4+ | Structured interview (30 min) against protocol themes | Go / No-Go questions |
| Weekly (ops) | Triage batch of P2/P3; KPI review | Support + metrics |

Interview themes must map to an Educational Metric ID (M1–M9), EP-001 outcome (O1–O9), educational review surface (Mission / Reflection / Coach / Journey / Twin), or a quality-gate defect — **not** an unconstrained feature wishlist.

Decline Never-Build requests (vanity engagement, opaque AI, public launch features) with Vision citation.

Details: [`../private_beta/FEEDBACK_SYSTEM.md`](../private_beta/FEEDBACK_SYSTEM.md), [`../private_beta/ISSUE_REPORTING.md`](../private_beta/ISSUE_REPORTING.md).

---

## 6. Support workflow

| Tier | Response target | Examples |
|---|---|---|
| P0 Security / data | Immediate | Account takeover, data leak |
| P1 Cannot study | Same day | Login failure, Session broken, wrong student data |
| P2 Confusing guidance | 1–2 business days | Unclear Coach copy, navigation confusion |
| P3 Suggestion | Weekly batch | UX ideas, copy nits |

Workflow: intake → triage → reproduce → fix via normal PR standards **or** document + hold if educational algorithm involved (requires PRD / educational governance) → confirm → release notes if user-visible.

Ownership: Founder / designated beta operator until a support role exists.

Details: [`../private_beta/SUPPORT_WORKFLOW.md`](../private_beta/SUPPORT_WORKFLOW.md).

---

## 7. Measurement loop

```text
Invite → Consent → Onboard → Study (Sessions)
                │
                ▼
     Emit / collect KPIs (M1–M9) when analytics flag ON
                │
                ▼
     Weekly scorecard review + support triage
                │
                ▼
     Interviews (week 4+) → themes coded to metric / surface IDs
                │
                ▼
     Cohort report → feeds Go / No-Go + product decisions
```

No experiment may change educational behaviour without an approved PRD ([`EXPERIMENT_FRAMEWORK.md`](EXPERIMENT_FRAMEWORK.md)).

Recommendations remain **out of effectiveness claims** for this protocol until a future recommendation PRD.

---

## 8. Exit criteria (private beta “successful”)

Private beta is successful when **all** of the following hold:

| # | Criterion |
|---|---|
| 1 | Cohort size 20–50 external invite-only students (or documented waiver with Educational + Product sign-off) |
| 2 | Privacy Review checklist signed |
| 3 | ≥4 weeks of measurement window for ≥20 active students (or exploratory label if below) |
| 4 | Cohort report against M1–M4, M6–M7 at minimum; M5/M8/M9 as available |
| 5 | Interview sample completed (target ≥8 interviews or 25% of active cohort, whichever smaller) |
| 6 | Support P0/P1 closed or accepted with owners; no unresolved “cannot study” backlog |
| 7 | No public registration / public launch |
| 8 | Findings coded to metrics / educational review — not a raw feature backlog |

Exit of an **individual** participant: withdrawal of consent, exam completion, or ops removal for abuse/safety — with data handling per Privacy Review.

---

## 9. Deliverables of this protocol

| Artefact | Location |
|---|---|
| This protocol | `PRIVATE_BETA_PROTOCOL.md` (EP-003) |
| Onboarding / feedback / support / privacy | `knowledge/product/private_beta/` |
| KPI definitions | [`EDUCATIONAL_METRICS.md`](EDUCATIONAL_METRICS.md) |
| Cohort measurement report | *To be written after cohort window* (not part of EP-003 doc freeze) |

---

## 10. Sign-off

| Role | Name | Date | Decision |
|---|---|---|---|
| Product | | | Protocol APPROVED for use |
| Security / ops | | | Privacy checklist (before expanded cohort) |
| Educational governance | | | Measurement mapping APPROVED |

Document status **Protocol approved** means the written protocol may be followed. It does **not** mean the private-beta cohort has succeeded.

---

## References

- [`../private_beta/README.md`](../private_beta/README.md)
- [`../ep001_product_validation/V1_EXIT_CRITERIA.md`](../ep001_product_validation/V1_EXIT_CRITERIA.md)
- [`GO_NO_GO_REPORT.md`](GO_NO_GO_REPORT.md)
- EP-002 go-live checklist — `knowledge/product/analytics/ep002/GO_LIVE_CHECKLIST.md`
