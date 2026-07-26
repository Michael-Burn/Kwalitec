# MS-006 — Migration Plan (Learning Evidence & Experimentation Platform)

**Milestone:** MS-006 — Learning Evidence & Experimentation Platform  
**Directive:** Engineering Directive 001  
**Status:** Architecture Design  
**Parent:** `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`  
**Risks:** `RISK_ANALYSIS_MS006.md`  
**Depends on:** MS-001 Runtime Bridge (Runtime A facts); recommended MS-002 continuity; optional MS-003/004/005 traces for richer linkage (not required for organisation outcome measurement from Runtime A alone)

---

## Principles

1. **Incremental** — each phase independently releasable.  
2. **Reversible** — feature-flag rollback per phase.  
3. **No big-bang** — never flip Evidence serve-arms + Adaptive Authority + Strategy Authority together.  
4. **No schema changes** for Evidence Platform Ready (observational store decisions deferred to ADR).  
5. **No UI redesign** for student Experience.  
6. **No educational writes** inside Evidence Platform.  
7. **No Runtime A / Twin / Adaptive / Strategy / Experience redesign** in Evidence phases.  
8. **Shadow before serve** — measure before any learner-visible experiment arm.  
9. **Empty authentic / honest inconclusive over theatrical significance.**  
10. **Runtime A wins** fact conflicts; measurement never becomes SoT.  
11. **SP8** — organisation metrics never promoted as learning-depth without explicit programme.  
12. **Architecture first** — this directive stops at docs; E0 begins only after architecture review PASS.

---

## Phase overview

| Phase | Name | Releasable? | Educational write? | Changes upstream engines? |
|---|---|---|---|---|
| — | Architecture docs (this directive) | Yes (docs) | No | No |
| E0 | Contracts, fixtures, ADRs | Yes (docs/tests) | No | No |
| E1 | Evidence intake & normalisation | Yes | No | No (read/consume only) |
| E2 | Outcome assembly & analytics contracts | Yes | No | No |
| E3 | Policy evaluation + explainability gate | Yes | No | No |
| E4 | Experiment assignment (shadow) | Yes | No | No |
| E5 | Observational Evidence Platform traceability | Yes | No | No |
| E6 | Shadow soak + monitors | Yes (ops) | No | No |
| E7 | Governance rehearsal + limited serve-arm (flagged) | Yes | No* | Flags only via owners |
| — | **Learning Evidence Platform Ready** | — | E0–E7 | — |

\*E7 must not write educational facts; any learner-visible difference is upstream-flag-mediated under governance.

---

## Architecture review gate (before E0)

### Scope

- Accept MS-006 architecture docs (this set).  
- Accept ADR-MS006-001 Evidence Platform Authority Boundaries.  
- Confirm dependency law: Runtime A → Twin → Adaptive → Strategy → Experience → Evidence Platform.  
- Confirm no implementation artefacts introduced by this directive.

### Exit criteria

- Architecture review **PASS**.  
- Acceptance criteria in parent §11 satisfied.

### Rollback

N/A (docs only).

---

## E0 — Contracts, fixtures, ADRs

### Scope

- Inert logical contracts / DTOs / port interfaces behind `ENABLE_EVIDENCE_PLATFORM` (default OFF).  
- Golden fixtures: empty evidence, sparse night, completed session, abandoned+resume, Adaptive/Strategy shadow traces present/absent, claim-boundary leakage negative fixtures.  
- Draft ADR-MS006-002 (retention), ADR-MS006-003/004 as needed.  
- **No** intake execution; **no** experiment assignment; **no** analytics export.

### Status

**Contracts / DTOs / EvidenceAdapter / DI / master flag — Implemented** (`app/infrastructure/adapters/evidence_platform/`).  
Golden fixtures and additional ADRs remain follow-ups within E0 scope or adjacent docs.

### Exit criteria

- Contract serialization / immutability tests.  
- Dependency boundary tests (Evidence Platform must not import Experience as write owner; must not write Runtime A).  
- Flag defaults OFF.

### Rollback

Disable Evidence Platform flag / leave unused.

---

## E1 — Evidence intake & normalisation

**Status:** **Implemented** (Engineering Directive 003)

### Scope

- Read-only intake producing `ObservationRef` → `EvidenceRecord` via
  `EvidenceCollector` / `EvidenceAssembler` / `EvidenceValidator` / `EvidenceFactory`.  
- Quality gate (privacy, freshness, claim boundary, Runtime A preference).  
- **No** evaluation; **no** student UX; **no** persistence.

### Exit criteria

- Identical Runtime A refs + normaliser version → identical `evidence_id`.  
- Missing upstream → unavailable honesty; never estimate facts.  
- No write APIs in intake call graph.

### Rollback

Disable Intake / Platform flags.

---

## E2 — Outcome assembly & analytics contracts

### Scope

- Registered outcome definitions; `EvidenceBundle` → `OutcomeObservation`.  
- Analytics export contracts (governance audience).  
- SP8 separation enforced in types.  
- **No** policy promote; **No** serve-arms.

### Exit criteria

- Organisation vs learning-depth cannot be silently aliased.  
- Thin N → `not_estimable` / limitations.  
- Flag defaults OFF.

### Rollback

Disable Analytics / Platform flags.

---

## E3 — Policy evaluation + explainability gate

### Scope

- `EvaluationRecord` + `PolicyEvaluationExplanationBundle`.  
- Enforce five mandatory explanation answers.  
- Emit `EVIDENCE_EVAL_*` telemetry.  
- Failed evaluations remain non-actionable for promote.

### Exit criteria

- Complete bundles PASS; incomplete FAIL.  
- Overclaim / claim-boundary leakage FAIL.  
- No Runtime A / Twin / Adaptive / Strategy / UI mutation.

### Rollback

Gate stays observational; no serve-arms.

---

## E4 — Experiment assignment (shadow)

### Scope

- `ENABLE_EXPERIMENT_ASSIGNMENT` + shadow exposure only.  
- Deterministic AssignmentRecords; exposure verification.  
- Measure → analyse → discard learner effects.  
- **No** flag-mediated serve difference owned by Evidence Platform.

### Exit criteria

- Shadow experiments never change Home / Start / Recommendation UX.  
- Exposure violations detected.  
- Flags default OFF.

### Rollback

Disable Assignment / Shadow / Platform.

---

## E5 — Observational Evidence Platform traceability

### Scope

- `EvidencePlatformTrace` + lineage reconstruction.  
- Linkage strength honesty.  
- Correlation with upstream traces when available.

### Exit criteria

- Deterministic reconstruction from frozen trace.  
- No educational SoT tables required.  
- Ambiguous linkage never upgraded silently.

### Rollback

Disable trace emission; Platform flag off.

---

## E6 — Shadow soak + monitors

### Scope

- Soak period with monitors: claim-boundary leakage, linkage ambiguity rate, gate failure rate, determinism drift, latency of measurement path, demo-marker detection.  
- Health + rollback runbooks.  
- Readiness report draft.

### Exit criteria

- Soak criteria met or gaps explicitly accepted by governance (not silent).  
- Rollback drill executed once.  
- No learner-visible Evidence Platform effects.

### Rollback

Disable all Evidence Platform flags.

---

## E7 — Governance rehearsal + limited serve-arm (optional, flagged)

### Scope

- Rehearse full Propose → Decide → Apply (upstream owners) → Verify loop.  
- Optional **limited** flag-mediated serve-arm under `GOVERNANCE_MODEL` bars — Evidence Platform still observational.  
- **Not** broad Adaptive/Strategy Authority promotion.  
- **Not** learning-depth/transfer product claims.

### Exit criteria

- Governance artefacts complete for rehearsal.  
- Rollback_map proven.  
- Evaluation gate PASS for any keep decision.  
- Architecture Guardian ACK on dependency law.

### Rollback

Execute rollback_map; disable experiment assignment / Platform as needed.

---

## Learning Evidence Platform Ready checklist

Ready may be declared only when:

| # | Criterion |
|---|---|
| 1 | E0–E6 complete (E7 rehearsal recommended; serve-arm optional) |
| 2 | ADR-MS006-001 ratified |
| 3 | Write-guard / dependency tests green |
| 4 | Explainability gate proven |
| 5 | SP8 claim-boundary monitors green |
| 6 | Shadow soak report accepted |
| 7 | Rollback drill documented |
| 8 | No schema required for Ready (or ADR explicitly accepts observational store) |
| 9 | Upstream Authority flags remain independently OFF by default unless separately governed |
| 10 | Programme explicitly does **not** treat Ready as exam-transfer proof |

**This directive does not declare Ready.**

---

## Flag matrix (design)

| Flag | E0 | E1 | E2 | E3 | E4 | E5 | E6 | E7 |
|---|---|---|---|---|---|---|---|---|
| `ENABLE_EVIDENCE_PLATFORM` | present OFF | ON (env) | ON | ON | ON | ON | ON | ON |
| `ENABLE_EVIDENCE_INTAKE` | OFF | ON | ON | ON | ON | ON | ON | ON |
| `ENABLE_OUTCOME_ANALYTICS` | OFF | OFF | ON | ON | ON | ON | ON | ON |
| `ENABLE_POLICY_EVALUATION` | OFF | OFF | OFF | ON | ON | ON | ON | ON |
| `ENABLE_EVIDENCE_SHADOW` | OFF | OFF | OFF | OFF | ON | ON | ON | ON |
| `ENABLE_EXPERIMENT_ASSIGNMENT` | OFF | OFF | OFF | OFF | ON | ON | ON | ON (limited) |

Defaults remain **OFF** in committed config until intentionally enabled per environment.

---

## Stop condition (this directive)

Stop after architecture documentation. Do not begin E0 implementation until architecture review PASS.
