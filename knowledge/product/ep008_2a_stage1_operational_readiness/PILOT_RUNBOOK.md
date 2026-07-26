# EP-008.2A — Pilot Runbook

**Programme:** EP-008.2A — Stage 1 Operational Readiness  
**Date:** 2026-07-26  
**Audience:** Founder / designated beta operator  
**Companions:** [`STAGE1_CHECKLIST.md`](STAGE1_CHECKLIST.md) · [`DATA_COLLECTION_PLAN.md`](DATA_COLLECTION_PLAN.md) · [`../ep004_private_beta/ROLLOUT.md`](../ep004_private_beta/ROLLOUT.md)  
**Does not:** Change product behaviour; authorise invites before Critical gates  

---

## 1. Purpose

Execute a **controlled Stage 1 external pilot** (5–10 invite-only students) safely: consent → onboard → study → measure → support → interview — without public launch and without educational-algorithm experiments.

---

## 2. Roles

| Role | Responsibility |
|---|---|
| **Beta operator** (founder default) | Invites, check-ins, triage, scorecard filing, Rollout log |
| **Security / ops** | Privacy Review signature; kill switch; env flag changes |
| **Product** | Claim language; enrollment Go; effectiveness freeze enforcement |
| **Educational governance** | Interview coding quality; Q1–Q5 honesty; no G1.9 overclaim |
| **On-call engineering** | Analytics drain / replay; P0/P1 reproduction |

---

## 3. Pre-flight (T− before first invite)

1. Complete [`STAGE1_CHECKLIST.md`](STAGE1_CHECKLIST.md) **Section A**.  
2. Confirm EP-007.3 design still governs selection and metrics.  
3. Rehearse:
   - Analytics kill switch (`ANALYTICS_EVENTS_V1=false` + restart)
   - `flask analytics-export-user <id>`
   - `flask analytics-delete-user <id> --yes` (staging / dry-run evidence)
4. Prepare invite pack: welcome note, privacy notice, support link, onboarding orientation.  
5. Record Stage 1 **Go** in `ROLLOUT.md` only when A clears.

**If any Critical item open → stop. Do not invite.**

---

## 4. Invite and account provisioning

```text
Select candidate (inclusion rules)
        ↓
Provision invite-only account (no public registration)
        ↓
Assign BETA-PIL-NNN (ops map private; knowledge repo pseudonymous only)
        ↓
Send invite + privacy notice + consent requests
        ↓
Capture: privacy ack + measurement consent (+ optional interview/quote)
        ↓
Mark registry: Invited → Accepted on first login
```

**Exclusion:** cannot consent → do not measure; do not pressure.

---

## 5. Day-0 participant instructions (ops script)

Use calm, honest language. Do **not** promise pass rates or “exam ready.”

1. Log in with the invite credentials.  
2. Complete any in-product calibration / onboarding.  
3. Open **Home** — read today’s tip (what / why / why now).  
4. Start **Today’s Session** when ready (“I’m doing this next” / Pattern A).  
5. Complete Session; use Reflection when prompted.  
6. Return to Home / History to see continuity.  
7. Report blockers via the support channel (login/Session = P1).  

Expectations: bugs may occur; educational honesty preferred over polish.

---

## 6. Analytics activation (Pilot)

Only after Pilot checklist signed:

1. Set `ANALYTICS_EVENTS_V1=true` on Pilot-hosting processes only.  
2. Restart web + worker.  
3. Verify `flask analytics-metrics` → `feature_flag_enabled: true`.  
4. Confirm worker draining; queue depth stable.  
5. Watch `analytics.emit_failed` for 24h.  
6. Log enable row in `ANALYTICS_ACTIVATION.md`.

**Abort:** flag false → restart → confirm disabled → educational smoke green.

Educational study must continue if analytics is OFF (fail-open / dark OK with manual scorecard label).

---

## 7. Weekly operating rhythm

| Cadence | Actions |
|---|---|
| **Daily (first 7 days / new accepts)** | P0/P1 watch; activation follow-ups |
| **Daily (flag ON)** | Glance metrics; DLQ |
| **Weekly** | Scorecard (M1–M4, M6–M7); support P2/P3 batch; monitoring report template |
| **Week 1** | Activation check-in |
| **Week 2–3** | Consistency / reflection check-in |
| **Week 4+** | Structured interview (30 min); code to M / Q / surface IDs |
| **Bi-weekly** | M5 if available (provisional if Journey emit gated) |
| **End window** | M8/M9 as available; Stage 1 ops exit review |

---

## 8. Support triage (quick reference)

| Tier | Target | Examples | First action |
|---|---|---|---|
| P0 | Immediate | Account takeover, data leak | Freeze affected access; kill switch if analytics involved; Security |
| P1 | Same day | Cannot login; Session broken; wrong student data | Reproduce; fix or workaround; confirm with student |
| P2 | 1–2 business days | Confusing guidance / navigation | Document; copy/orientation if non-algorithm |
| P3 | Weekly | Ideas / nits | Batch; decline Never-Build with Vision citation |

**Educational algorithm change requests:** STOP → Document → Recommend (PRD). Do not hot-fix Runtime A during pilot for metric gaming.

---

## 9. Incident playbooks

### 9.1 Privacy / data incident

1. Pause new invites.  
2. Analytics kill switch if emit path implicated.  
3. Freeze exports.  
4. Follow `../analytics/ep002/INCIDENT_RESPONSE.md` §D + Privacy Ops.  
5. Audit: `flask analytics-export-audit`.  
6. Notify Product + Security; update Rollout to HOLD.

### 9.2 Student cannot study (P1)

1. Confirm account + env.  
2. Reproduce on staging if needed.  
3. Workaround or fix via normal PR standards.  
4. Do not invent educational scores.  
5. Confirm with reporter same day.

### 9.3 Analytics backlog / DLQ (SEV-2)

1. `flask analytics-metrics`.  
2. Run worker; inspect dead letters.  
3. Replay only after root-cause fix (`REPLAY_SPECIFICATION.md`).  
4. If student UX impacted: kill switch.

### 9.4 Suspected educational honesty issue

1. Freeze claim language immediately.  
2. Open defect with educational-integrity tag.  
3. Do not ship speculative algorithm “fixes” under pilot pressure.

---

## 10. Measurement integrity rules

1. Pseudonymous IDs only in knowledge artefacts.  
2. Withdrawn measurement consent → exclude from numerators; may still study.  
3. Staff / Stage 0 never inflate Stage 1 N.  
4. Empty cells = `exploratory` / `insufficient N` — never greenwash.  
5. Commitment events = observational research only — not ranking inputs; not effectiveness marketing.  
6. Recommendation-effectiveness claims remain frozen (DR-036 / EP-004 C7).  
7. No experiment that changes educational behaviour without Approved PRD.

---

## 11. Interview procedure (week 4+)

**Length:** ~30 minutes.  
**Consent:** interview optional; quote optional separately.  

**Required theme coverage (map each note to an ID):**

| Theme | Maps to |
|---|---|
| Activation / first Session | M1 / onboarding ops |
| Consistency / weekly rhythm | M6, M7 |
| Session completion friction | M4 |
| Reflection usefulness | M3 |
| Trust in “why” / tip inspectability | Q3; K2 context |
| Preparedness without false certainty | Cohort design §4.2; readiness honesty |
| Final Test: “helped you study like a professional?” | Educational satisfaction |
| Commitment / defer honesty (if used) | Observational only |

Decline feature-wishlist expansion that violates Never-Build.

---

## 12. Data handling for operators

| Need | Command / path |
|---|---|
| Metrics snapshot | `flask analytics-metrics` |
| Student analytics export | `flask analytics-export-user <id>` |
| Delete analytics for user | `flask analytics-delete-user <id> --yes` |
| Consent verify | `flask analytics-verify-consent <id>` |
| Retention | `flask analytics-retention --execute` (scheduled) |
| Scorecard | EP-003 `PRODUCT_SCORECARD.md` + [`DATA_COLLECTION_PLAN.md`](DATA_COLLECTION_PLAN.md) |

Deliver exports securely; never include other users; do not reverse hashes.

---

## 13. Stage 1 stop / advance

| Outcome | Condition |
|---|---|
| **Continue Stage 1** | Monitoring GREEN/AMBER managed; no Critical privacy open; students studying |
| **HOLD / pause invites** | Section F abort triggers |
| **Stage 1 ops exit review** | EP-007.3 §8 checklist — then decide Stage 2 path or waiver |
| **Educational GO** | Not available from Stage 1 alone without C5–C6 floors / waiver |

---

## 14. Quick links

| Doc | Path |
|---|---|
| Ops readiness verdict | [`OPERATIONAL_READINESS_REPORT.md`](OPERATIONAL_READINESS_REPORT.md) |
| Checklist | [`STAGE1_CHECKLIST.md`](STAGE1_CHECKLIST.md) |
| Data plan | [`DATA_COLLECTION_PLAN.md`](DATA_COLLECTION_PLAN.md) |
| Risk review | [`RISK_REVIEW.md`](RISK_REVIEW.md) |
| Cohort design | `../ep007_3_educational_effectiveness_validation_stage1/COHORT_DESIGN.md` |
| Protocol | `../ep003_educational_effectiveness/PRIVATE_BETA_PROTOCOL.md` |
| Support | `../private_beta/SUPPORT_WORKFLOW.md` |
| Privacy review | `../private_beta/PRIVACY_REVIEW.md` |

---

**End of PILOT_RUNBOOK**
