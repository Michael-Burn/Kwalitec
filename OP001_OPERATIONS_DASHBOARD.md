# OP-001 — Operations Dashboard Specification

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `KSI002_PARTICIPANT_PROTOCOL.md`

**Specification only.** No analytics engine implementation. No product dashboard feature work under OP-001. Counts may be maintained in a spreadsheet, ops console notes, or manual markdown snapshots under `knowledge/evidence/releases/OP001/dashboard/snapshots/` (pseudonymous aggregates only).

---

## 1. Purpose

Give Founder and the Early Access operator a single funnel view of cohort health — enrollment through interview — without inventing behavioural KPIs or implementing a new analytics system.

---

## 2. Audience and refresh

| Item | Spec |
|------|------|
| Primary users | Founder · Early Access operator |
| Refresh cadence | At least **daily** during invite/accept wave; **weekly** during observation hold |
| Source of truth | Ops enrollment register (outside git for PII) + pseudonymous snapshot files |
| Non-goal | Real-time product analytics; M1–M9 engines; recommendation rates |

---

## 3. Required funnel states

Display **counts** (integers) and optional **participant ID lists** (pseudonymous only) for each state:

| State | Definition | Notes |
|-------|------------|-------|
| **Invited** | Invite email sent | Provisioned-but-not-invited ≠ Invited |
| **Accepted** | Invite accepted; acceptance timestamp recorded; account reachable | = ITT-Accepted for study counting |
| **Activated** | Accepted **and** ≥1 productive Session completed | Subset of Accepted |
| **Week 1** | Accepted participants whose personal start is in calendar week 1 of their observation clock **or** cohort ops week 1 — **choose one convention and freeze it** (default: **personal start + days 0–6**) | Mutually exclusive week buckets per person |
| **Week 2** | Personal start + days 7–13 | |
| **Week 3** | Personal start + days 14–20 | |
| **Week 4** | Personal start + days 21–27 | |
| **Completed** | Reached end of planned Early Access / study observation window (≥4 weeks) **or** Founder-marked cohort complete without withdrawal | Not the same as “passed exam” |
| **Withdrawn** | Measurement/study/account withdrawal logged | Remains visible; do not delete history |
| **Interview scheduled** | Structured interview booked | Requires interview consent |
| **Interview complete** | Interview conducted; notes archived (pseudonymous) | |

### 3.1 Display layout (conceptual)

```text
Early Access Operations — Cohort [WAVE-ID] — as of [ISO timestamp]

Invited                [ n ]
Accepted               [ n ]
Activated              [ n ]
Week 1                 [ n ]
Week 2                 [ n ]
Week 3                 [ n ]
Week 4                 [ n ]
Completed              [ n ]
Withdrawn              [ n ]
Interview scheduled    [ n ]
Interview complete     [ n ]
```

Optional derived (manual, not an engine):

| Derived | Formula |
|---------|---------|
| Acceptance rate | Accepted / Invited |
| Activation rate | Activated / Accepted |
| Never-activated | Accepted − Activated (among those past day 7) |
| Interview completion rate | Interview complete / Interview scheduled |

---

## 4. Counting rules (honesty)

1. **Selected ≠ Invited ≠ Accepted.** KSI-003 pending pilots must not inflate Accepted.  
2. Stage 0 internal / staff **excluded** from external funnel unless dual-marked and labelled.  
3. Duplicates: count retained ID only.  
4. Withdrawn participants: count in **Withdrawn**; remove from Week buckets going forward; retain historical snapshot integrity.  
5. Week buckets: a person appears in **at most one** current week bucket; Completed supersedes week buckets.  
6. Interview scheduled/complete may overlap with Week 4 / Completed.  
7. Empty cohort: show **zeros** — never fabricate.

---

## 5. Snapshot artefact (empty structure)

Path pattern:

`knowledge/evidence/releases/OP001/dashboard/snapshots/YYYY-MM-DD.md`

Suggested empty template (fill only with real counts later):

```markdown
# Dashboard snapshot — YYYY-MM-DD

| State | N |
|-------|--:|
| Invited | |
| Accepted | |
| Activated | |
| Week 1 | |
| Week 2 | |
| Week 3 | |
| Week 4 | |
| Completed | |
| Withdrawn | |
| Interview scheduled | |
| Interview complete | |

Notes:
- Wave ID:
- Convention: personal-start weeks
- Operator:
```

**Do not** create filled snapshots until real ops data exists.

---

## 6. Non-implementation clause

OP-001 does **not** require:

- New Flask blueprints or console pages  
- New database tables or migrations  
- Analytics SDK or recommendation telemetry engines  
- Automated week assignment jobs  

A manual spreadsheet matching §3 is compliant.

---

## 7. STOP

Dashboard may be prepared empty.  
Do not publish marketing metrics from this funnel.  
Do not treat funnel movement as educational effectiveness GO.

Signed: OP-001 Operations Dashboard Spec · 2026-08-04
