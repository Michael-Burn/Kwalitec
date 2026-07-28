# CP-001 — Decision Journal Domain Model

**Programme:** CP-001 — Capability Programme  
**Version:** 1.0  
**Status:** Active — conceptual domain model (design only)  
**Effective:** 2026-07-28  
**Companion to:** `CP001_DECISION_JOURNAL_ARCHITECTURE.md`  
**Constraint:** Conceptual entities only — no schema, ORM, or API changes in this programme.

---

## 1. Purpose

Define the conceptual **domain model** for the Decision Journal capability: entities, relationships, lifecycle states, choice/rationale structures, and educational purpose binding.

This model is implementation-neutral. Future programmes may map it to ILE-002 tables or successor persistence via ADR. CP-001 does not prescribe columns.

---

## 2. Aggregate overview

```
DecisionJournal (per learner)
   └── DecisionRecord (1..n)           ← significant educational interaction
         ├── GuidanceSnapshot          ← immutable at create
         ├── ExplanationSnapshot       ← P-001.2 freeze
         ├── StudentChoice?            ← disposition + optional rationale
         ├── EvidenceEvent (0..n)      ← append-only
         ├── ReflectionAttachment?     ← optional
         ├── OutcomeLink (0..n)        ← Mission / Session / learning signals
         └── EvaluationStub?           ← measurement readiness metadata
```

**Aggregate root (design):** `DecisionRecord` under learner-scoped `DecisionJournal`.

---

## 3. Core entities

### 3.1 DecisionJournal

| Field (conceptual) | Meaning |
|--------------------|---------|
| `learner_id` | Owning student (scoped; never expose foreign ids without ownership checks) |
| `records[]` | Chronological DecisionRecords |
| `retention_class` | Default `account_lifetime` (see Privacy Model) |

Invariant: one journal per learner educational identity. Plan deletion must not erase journal continuity (ILE-002 retention posture).

### 3.2 DecisionRecord

| Field (conceptual) | Meaning |
|--------------------|---------|
| `decision_id` | Stable opaque id |
| `educational_purpose_code` | Closed catalogue EV-* (Architecture §8) — **required** |
| `catalogue_decision_id?` | Optional ILE-011 Decision Catalogue id (e.g. `D-L01`) |
| `lifecycle_status` | See §5 |
| `created_at` / `updated_at` | Timestamps; updates only via append or status transition |
| `si_capability_tags[]` | Primary SI-C* tags (usually C2 ± C4/C5/C7) |
| `eligibility` | Whether this was an eligible primary recommendation under flag honesty |

**Invariant:** No DecisionRecord without `educational_purpose_code`.

### 3.3 GuidanceSnapshot (immutable)

Frozen at recommendation time. Never edited.

| Field (conceptual) | Meaning |
|--------------------|---------|
| `recommendation_ref` | Link to recommendation / tip / Mission brief identity |
| `action_summary` | Student-safe “what was suggested” |
| `observation_summary` | What happened / context (student-safe) |
| `meaning_summary` | Why it matters educationally |
| `expected_benefit` | Why bother |
| `curriculum_refs[]` | Topic / syllabus refs via CurriculumService ids (V1/V2 safe) |
| `surface` | Coach / Insights / Plan / Mission / Recovery / … |
| `recommendation_quality_class?` | Optional P-001.3 class label (not ranking dump) |

### 3.4 ExplanationSnapshot (immutable)

P-001.2 freeze. Detail: `CP001_EXPLAINABILITY_INTEGRATION.md`.

| Field (conceptual) | Meaning |
|--------------------|---------|
| `explanation_level` | 1 / 2 / (3 opt-in) |
| `why` | Primary educational reason |
| `evidence_summary` | Identifiable supporting evidence (student-safe) |
| `confidence_band` | Qualitative band aligned with ILE-011 / P-001.2 |
| `next_action` | Clear suggested next step |
| `uncertainty` | What remained unknown |
| `fact_estimate_advice_separation` | Boolean design flag: speech lawfully separated |

### 3.5 StudentChoice

| Field (conceptual) | Meaning |
|--------------------|---------|
| `disposition` | `accept` \| `defer` \| `reject` \| `dismiss` \| `none_yet` |
| `chosen_at` | When recorded |
| `rationale?` | Optional StudentRationale |
| `agency_note` | Always treat as student-owned; never auto-filled as accept |

### 3.6 StudentRationale

Optional structured + free-text model of *why the student chose as they did*.

| Field (conceptual) | Meaning |
|--------------------|---------|
| `rationale_mode` | `none` \| `structured_tags` \| `free_text` \| `both` |
| `structured_tags[]` | Closed tag catalogue (design) |
| `free_text?` | Optional; privacy-elevated |
| `consent_scope` | Whether free text may feed Twin / research |
| `captured_at` | Timestamp |

#### Structured tag catalogue (design — closed)

| Tag | Meaning |
|-----|---------|
| `TIME` | Not enough time today |
| `ENERGY` | Energy / focus too low |
| `PLAN_CONFLICT` | Conflicts with authorised Mission / tutor homework |
| `TOPIC_PREFERENCE` | Prefers different lawful topic today |
| `DOUBT_FIT` | Doubts this is the highest-value action |
| `NEED_CLARITY` | Explanation / confidence insufficient |
| `ALREADY_DONE` | Believes action already completed |
| `OTHER` | Catch-all (prefer free text only when needed) |

**Rules:**

- Rationale is **never required** to accept or defer.  
- Tags are preferred over free text for Twin / analytics.  
- Free text must not appear in research extracts without consent and privacy review.  
- Rationale must not be used to shame or reduce student status.

### 3.7 EvidenceEvent (append-only)

| Field (conceptual) | Meaning |
|--------------------|---------|
| `event_id` | Stable id |
| `event_type` | e.g. `evidence_appended`, `started`, `progress_note` |
| `student_safe_summary` | Append narrative |
| `source_ref?` | Runtime A / Evidence / Mission refs |
| `recorded_at` | Timestamp |

Invariant: never mutates GuidanceSnapshot or ExplanationSnapshot.

### 3.8 ReflectionAttachment

| Field (conceptual) | Meaning |
|--------------------|---------|
| `reflection_status` | `pending` \| `reflected` \| `not_applicable` |
| `reflection_ref?` | Link to Guided Reflection / experience id |
| `summary_student_safe?` | Optional short reflection summary |
| `sensitivity_class` | Default `elevated` for free text |
| `coercion_flag` | Must remain false; true = quality incident (OM-REF-03) |

### 3.9 OutcomeLink

Joins journal decisions to later measurable outcomes without inventing learning depth.

| Field (conceptual) | Meaning |
|--------------------|---------|
| `outcome_kind` | `mission_started` \| `mission_completed` \| `practice_evidence` \| `revision_return` \| `readiness_delta` \| `abandoned` \| `other_lawful` |
| `outcome_ref` | Mission / Session / Evidence id |
| `observed_at` | Timestamp |
| `claim_boundary` | OM claim boundary tag (`organisation`, `learning_signal`, …) |
| `om_metric_hints[]` | Optional OM-REC-06/07/08 etc. design hints |

**Rule:** `readiness_delta` / learning links are **observations of system estimates**, labelled as estimates — never facts of mastery.

### 3.10 EvaluationStub

Measurement readiness metadata for OM packs (not a score brain).

| Field (conceptual) | Meaning |
|--------------------|---------|
| `completeness_ok` | Choice disposition recorded when eligible |
| `explanation_frozen_ok` | ExplanationSnapshot present |
| `outcome_link_pending` | Waiting for start/complete window |
| `excluded_reason?` | Why omitted from a metric pack (flag-OFF, ineligible, …) |

---

## 4. Relationships (normative)

| From | To | Cardinality | Nature |
|------|----|-------------|--------|
| DecisionJournal | DecisionRecord | 1:N | Ownership |
| DecisionRecord | GuidanceSnapshot | 1:1 | Immutable composition |
| DecisionRecord | ExplanationSnapshot | 1:1 | Immutable composition |
| DecisionRecord | StudentChoice | 1:0..1 | Mutable until terminal disposition |
| StudentChoice | StudentRationale | 1:0..1 | Optional |
| DecisionRecord | EvidenceEvent | 1:N | Append-only |
| DecisionRecord | ReflectionAttachment | 1:0..1 | Optional |
| DecisionRecord | OutcomeLink | 1:N | Append-only links |
| DecisionRecord | EvaluationStub | 1:0..1 | Measurement helper |
| DecisionRecord | Recommendation Engine | N:1 | Reference only |
| DecisionRecord | Twin | N:0..1 | Signal emission (not ownership) |
| DecisionRecord | OM packs | N:N | Metric membership via ids |

---

## 5. Lifecycle states

Aligned with ILE-002 product vocabulary; capability view adds evaluation clarity.

| Status | Meaning | Terminal? |
|--------|---------|-----------|
| `recommended` | Guidance offered; no learner choice yet | No |
| `accepted` | Learner accepted | No (outcomes may follow) |
| `deferred` | Learner deferred / set aside (may include dismiss posture) | No |
| `rejected` | Explicit reject (if distinguished in product) | No |
| `evidence_evolving` | Append-only evidence after snapshot | No |
| `reflected` | Reflection closed loop | No |
| `outcome_recorded` | Downstream outcome known | No |
| `evaluated` | Included in or explicitly excluded from OM pack | Soft |
| `archived` | Soft archive; remains readable | Soft terminal |

### Allowed transitions (design)

```
recommended → accepted | deferred | rejected | archived
accepted | deferred | rejected → evidence_evolving | reflected | outcome_recorded | archived
evidence_evolving → reflected | outcome_recorded | archived
reflected → outcome_recorded | archived
outcome_recorded → evaluated | archived
evaluated → archived
* → archived (soft; never delete)
```

Illegal: rewriting snapshots; jumping to `outcome_recorded` without disposition when eligibility required capture; auto-`accepted` without student action.

---

## 6. Decision type catalogue (significant interactions)

What **may** become a DecisionRecord (must still pass Educational Value Test):

| Type | Purpose codes | Notes |
|------|---------------|-------|
| Primary next-action recommendation | EV-NEXT | SI-C2 primary |
| Revision recommendation | EV-REVISE | |
| Mission / Session commitment | EV-MISSION | May mirror EP-008.3 / ILE-004 |
| Recovery recommendation | EV-RECOVER | |
| Readiness / pacing honesty advisory | EV-READY | Humble speech only |
| Learning milestone | EV-MILESTONE | Continuity memory |
| Reflection prompt close | EV-REFLECT | Optional |
| Lawful refusal of certainty | EV-REFUSE | System or student |

What **must not** become a DecisionRecord: page views, individual MCQ clicks, tooltip hovers, streak increments, internal dual-run diagnostics.

---

## 7. Student rationale → Twin / OM mapping (design)

| Rationale artefact | Twin domain (Constitution) | OM use |
|--------------------|----------------------------|--------|
| Disposition only | Behaviour (engagement pattern) | OM-REC-03…05 |
| Structured tags | Behaviour / constraints | Qualitative ops; not mastery |
| Free text | Default **not** Twin-ingested | Privacy-elevated; research only with consent |
| Reflection attachment | SI-C5 path; ADR for Evidence writes | OM-REF-* |

---

## 8. Identity and provenance

| Concern | Rule |
|---------|------|
| Learner scoping | All queries scoped to current user |
| Opaque ids | Prefer opaque decision ids in exports |
| Provenance | Link recommendation_ref + Runtime A / Evidence ids where applicable |
| Flag honesty | Ineligible / flag-OFF guidance must not enter “live Twin” metric narratives |
| Reproducibility | Same guidance inputs → same ExplanationSnapshot content (deterministic cores) |

---

## 9. Mapping to ILE-002 (informational)

| CP-001 concept | ILE-002 analogue (current) |
|----------------|----------------------------|
| DecisionRecord | `DecisionJournalEntry` |
| EvidenceEvent | `decision_journal_evidence_events` |
| StudentChoice dispositions | `accepted` / `deferred` / `dismissed` / `none_yet` |
| Lifecycle | `ENTRY_LIFECYCLE.md` statuses |
| Soft archive | `archived` status |

CP-001 may extend conceptually (e.g. explicit `rejected`, rationale tags, OutcomeLink, EvaluationStub) **without** requiring immediate schema change. Implementation programmes must ADR gaps.

---

## 10. Explicit non-goals

- SQLAlchemy models, migrations, or DTO changes in this programme  
- Changing recommendation ranking structures  
- Defining UI wireframes  
- Authorising Twin write paths  

---

**End of CP001_DOMAIN_MODEL**
