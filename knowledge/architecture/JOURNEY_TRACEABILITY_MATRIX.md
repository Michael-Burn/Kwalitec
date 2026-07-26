# MS-002 — Journey Traceability Matrix

**Milestone:** MS-002 — Educational Continuity  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `EDUCATIONAL_JOURNEY_ARCHITECTURE.md`  
**Contracts:** `JOURNEY_INTERFACE_SPECIFICATION.md` (`TraceRef`)

---

## 1. Purpose

Every Journey (and History) item must answer four questions:

| # | Question | TraceRef field |
|---|---|---|
| 1 | What happened? | `what` |
| 2 | Why did it happen? | `why.reason_codes` + `why.summary` |
| 3 | Which evidence supports it? | `evidence_refs` |
| 4 | Which recommendation changed because of it? | `recommendation.*` |

This matrix defines **required answers per event type**. Adapters project these fields from Runtime A; they do not invent educational causation.

---

## 2. Matrix

| Event type | What happened? | Why did it happen? | Evidence refs | Recommendation change |
|---|---|---|---|---|
| **PlanActivated** | Active study plan set / updated for exam window | Plan wizard / activation; continuity policy if copied | Plan id; prior TopicProgress continuity refs if any | Usually `not_applicable` unless plan change forces next-topic shift — then prior/next labels if reconstructable |
| **MissionEnsured** | Today’s mission created/ensured | Planning policy (next incomplete / revision template) | Mission id; curriculum topic code | May set “next focus” to mission topic (`mission_aligned=true`); prior Home recommendation if known |
| **SessionStarted** | Mission moved to In Progress | Student start / Resume continuity | Mission id | Typically no change (`not_applicable`) unless start coincides with first alignment |
| **SessionCompleted** | Mission completed | Evidence Before Completion succeeded | Mission id + accepted Attempt ids | Recompute/project next recommendation after progress update; record prior vs next labels when available |
| **EvidenceCommitted** | Practice attempt authorised | Evidence Authority acceptance rules | Attempt id(s); linked Mission | If mastery changed weak-topic set → recommendation may change; else `changed=false` |
| **ProgressChanged** | TopicProgress mastery/coverage updated | Gated AdaptiveLearning update after evidence | TopicProgress topic code + Attempt ids | Same as EvidenceCommitted |
| **RecommendationProjected** | Explainable next focus produced for a date | RecommendationService rules + mission alignment (MS-001 §5.3) | Inputs: TopicProgress / readiness / mission | Self-describing: this **is** the recommendation; delta vs previous day if reconstructable |
| **LifecycleStageChanged** | Learning → Revision (or reverse) | Leaf completion / plan revision fields via LifecycleService | Plan id; completion evidence set | Often changes recommendation policy (revision templates); prior/next required when reconstructable |
| **RevisionActivity** | Revision-stage session occurred | Weak-topic / revision template policy | Mission id + attempts | Recommendation may rotate among weak topics; capture prior/next labels |
| **ContinuityPreserved** | History protected across plan edit | EducationalContinuityService policy (DP-013) | Source/target TopicProgress refs | Usually `not_applicable`; if next topic changes, document delta |
| **ReadinessSample** | Aggregate readiness recorded/projected | ReadinessService aggregates | Underlying TopicProgress set (summary, not dump) | Optional correlation only; do not claim causal change unless known |
| **ProgressMilestone** | Coverage / stage gate reached | Derived from plan coverage + lifecycle | Supporting completed missions / topics | Often precedes recommendation shift; link if known |

---

## 3. Recommendation delta states

| State | When to use |
|---|---|
| `changed: true` + prior/next | Reconstructable labels before and after event |
| `changed: false` | Event occurred; recommendation label unchanged |
| `changed: null` + `unavailable_reason: "unavailable"` | Cannot reconstruct without inventing |
| `changed: null` + `unavailable_reason: "not_applicable"` | Event type does not affect recommendations |

**Forbidden:** Fabricating prior/next labels to avoid `unavailable`.

---

## 4. Evidence ref kinds

| `kind` | `id` | Notes |
|---|---|---|
| `mission` | MissionId | Session identity |
| `attempt` | AttemptId | StudyAttempt |
| `topic_progress` | topic_code (+ user) | Mastery row identity |
| `study_plan` | plan id | Context only |

Multiple refs allowed. Empty `evidence_refs` only when truly contextual (e.g. some PlanActivated) — still require honest `why`.

---

## 5. Experience mapping

| Surface | How matrix appears |
|---|---|
| Journey timeline item | Full `TraceRef` on each `EducationalTimelineEvent` |
| Journey topic card | Optional compact trace (current topic ← mission / progress) |
| History session card | `trace` optional; Inspect Evidence expands evidence_refs |
| Recommendation change panel | `get_recommendation_change` expands recommendation block |
| Home snippets | Trace may be omitted for size; detail pages remain authoritative |

---

## 6. Acceptance checks (traceability)

| ID | Check |
|---|---|
| T-1 | Every Journey timeline item has non-empty `what` |
| T-2 | Every item has `why.summary` or explicit empty with `reason_codes` including `unspecified` only if Runtime A provides none — prefer real codes |
| T-3 | SessionCompleted / EvidenceCommitted items include ≥1 evidence ref |
| T-4 | Recommendation field always present as object (never omitted); uses one of §3 states |
| T-5 | No timeline item cites another student’s ids |
| T-6 | Golden learner fixtures document expected What/Why/Evidence/Delta for ≥3 event types |

---

## 7. Worked examples (illustrative)

### SessionCompleted

```
what: "Completed mission on Core methods"
why: { reason_codes: ["session_finished", "evidence_accepted"], summary: "Session finished after authorised practice evidence." }
evidence_refs: [{ kind: "mission", id: "42" }, { kind: "attempt", id: "901" }]
recommendation: {
  changed: true,
  prior_label: "Core methods",
  next_label: "Advanced applications",
  decision_ids: []
}
```

### ReadinessSample (no causal recommendation claim)

```
what: "Readiness sample recorded"
why: { reason_codes: ["readiness_aggregate"], summary: "Aggregate exam readiness from authorised progress." }
evidence_refs: [{ kind: "topic_progress", id: "topic:core-methods" }]
recommendation: { changed: null, unavailable_reason: "not_applicable" }
```

### Recommendation change unavailable

```
what: "Completed mission on Ethics"
why: { reason_codes: ["session_finished"], summary: "Session finished." }
evidence_refs: [{ kind: "mission", id: "77" }]
recommendation: { changed: null, unavailable_reason: "unavailable" }
```

---

## Stop condition

Matrix is normative for implementation milestones. No code in this directive.
