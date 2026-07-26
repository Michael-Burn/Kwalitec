# Version 1 Evidence Requirements

**Programme:** P-002.1 — Version 1 Release Framework  
**Version:** 1.1  
**Status:** Active — evidence catalogue for Version 1 production-ready declaration  
**Effective:** 2026-07-26  
**Amended:** 2026-07-26 — G1 slice pointer (EP-005.1); catalogue rules unchanged  
**Companion:** [`VERSION_1_RELEASE_FRAMEWORK.md`](VERSION_1_RELEASE_FRAMEWORK.md)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

Specify **what evidence is required** for each Version 1 gate, how fresh it must be, and how the **Version 1 Evidence Package** is assembled.

Scores and checklists without linked evidence are invalid. Placeholder “TBD = pass” is forbidden.

---

## 2. Evidence Package structure

Recommended path:

```
knowledge/product/p002_1_version_1_release_framework/evidence/<YYYY-MM-DD>_v1_declaration/
  README.md                          # index + claim window + candidate tag
  ACCEPTANCE_CHECKLIST.md            # completed copy
  GO_NO_GO_DECISION.md               # signed decision
  G1_ksi/ …
  G2_constitutional/ …
  G3_explainability/ …
  G4_recommendation_quality/ …
  G5_planning_quality/ …
  G6_readiness_quality/ …
  G7_performance/ …
  G8_reliability/ …
  G9_telemetry/ …
  G10_security/ …
  G11_tests/ …
  G12_flags/ …
```

Alternative: a single **manifest** markdown that links immutable existing paths (preferred when evidence already lives under `knowledge/product/`, `docs/ga/`, CI artefacts). The package is complete only if every hard-gate criterion has a resolvable link.

### Package header (required)

| Field | Requirement |
|---|---|
| Candidate version / git tag | Exact |
| Claim window | Start–end dates |
| Assembled by | Name / role |
| Assembly date | ISO date |
| Overall outcome | Filled after decision board |

---

## 3. Freshness rules

| Evidence class | Max age at declaration | Notes |
|---|---|---|
| Validated KSI assessment | **90 days** | PSF §5.4; older → G1 fail |
| EVF Version Approval / Gate outcome | Per EVF release class rules; must cover claim window | Stale or withdrawn → G2.4 fail |
| Security review residuals | Current for tag; re-ack if new criticals | G10 |
| CI pytest / ruff / perf soft budgets | Release candidate / tag build | G7.1, G11 |
| Production smoke / health fingerprint | Same deploy as claim | G8 |
| Flag matrix | Same as production defaults under claim | G12 |
| Explainability / Recommendation checklists | Claim window programmes | May cite earlier Pass if no subsequent regression |
| Blind-review / interview qualitative packs | Prefer ≤ 180 days; disclose if older | Feeds G1 confidence |

---

## 4. Gate-by-gate evidence catalogue

### G1 — Validated KSI

| Artefact | Acceptable sources |
|---|---|
| KSI assessment with category scores | Updated assessment under `p001_1_ksi_baseline/` or evidence-package copy citing methodology |
| Evidence paths per category | Blind reviews, EP-003 scorecard, interviews, dogfood, support themes |
| Confidence + limitations | Required on assessment |
| Re-score note | Second assessor or documented Product resolution if divergence > ±3 |
| EP-003 / EP-004 Go / No-Go status | `ep003_educational_effectiveness/GO_NO_GO_REPORT.md`, `ep004_private_beta/GO_NO_GO_DECISION.md` (or successors) |
| Honesty incident register | Empty / cleared statement |

**Insufficient alone:** Sum of programme Estimated ΔKSI from EP completion reports.

**Current G1 slice (2026-07-26, not a Version 1 declaration):**  
`knowledge/product/p002_1_version_1_release_framework/evidence/2026-07-26_ksi_validation/` indexes canonical artefacts in `knowledge/product/ep005_1_ksi_validation_evidence/` (Validated KSI **59**; Gate G1 **FAIL**). Refresh or replace this slice when re-scoring.

---

### G2 — Constitutional compliance

| Artefact | Acceptable sources |
|---|---|
| Final Test attestation | Short memo: claim set vs Vision 2030 Final Test |
| Never-Build scan | Checklist against Vision Never-Build for production defaults |
| EVF outcome | `knowledge/educational_validation/release_reports/` Version Approval Report + Gate outcome |
| Architecture attestation | One-runtime / no second brain statement; link consolidation / EP-002.9 baseline if used |
| Curriculum V1/V2 proof | CI architecture tests or explicit load/traversal evidence |
| SIA inventory | Index of material EP/P SIA paths since P-001.1 effective date |
| ADR currency | `docs/adr/README.md` + list of claim-window ADRs |

---

### G3 — Explainability coverage

| Artefact | Acceptable sources |
|---|---|
| Schema coverage proof | Tests / spot-check captures for Rec / Plan / Readiness surfaces |
| Programme checklists | Completed `EXPLAINABILITY_REVIEW_CHECKLIST.md` (or Pass records) for in-scope EP/P |
| Runtime A consistency pack | Side-by-side notes across Dashboard / Coach / Insights / Plan / Readiness / Journey |
| Defect register excerpt | Zero open P1 explainability honesty items |

---

### G4 — Recommendation Quality compliance

| Artefact | Acceptable sources |
|---|---|
| Programme checklists | `RECOMMENDATION_REVIEW_CHECKLIST.md` Pass / waiver records |
| Scorecard evaluation | Filled scorecard for claim window (`RECOMMENDATION_QUALITY_SCORECARD.md`) |
| Precision sample | Review / dogfood / labelled eval noting 0 hard-gate precision failures |
| Marketing freeze status | Explicit statement: freeze holds **or** PRD/O8 lift evidence |
| EP-003.1 contract tests | Pytest evidence for recommendation quality behaviour |

---

### G5 — Planning Quality compliance

| Artefact | Acceptable sources |
|---|---|
| Contract reference | `knowledge/architecture/PLANNING_SERVICE_QUALITY_CONTRACT.md` |
| Automated tests | `tests/services/test_planning_quality_ep003_3.py` (or successor) green log |
| Smoke / dogfood pack | No dual “today” / duration conflict notes |
| Personalisation posture | Flag state + EP-004.3 rules compliance note if ON |

---

### G6 — Readiness Quality compliance

| Artefact | Acceptable sources |
|---|---|
| Contract reference | `knowledge/architecture/READINESS_SERVICE_QUALITY_CONTRACT.md` |
| Automated tests | `tests/services/test_readiness_quality_ep003_2.py` (or successor) green log |
| Honest-refusal proof | Capture or test showing cannot-yet-be-estimated / refusal path |
| Overclaim scan | No Exam Ready marketing; defect register clear |

---

### G7 — Performance

| Artefact | Acceptable sources |
|---|---|
| CI soft budgets | Green `tests/ga/test_performance_benchmarks.py` for candidate |
| Baseline doc | `docs/ga/PERFORMANCE_BASELINE.md` |
| Operator sample | Staging/production timings for Dashboard / Journey / health **or** signed HOLD |

---

### G8 — Reliability

| Artefact | Acceptable sources |
|---|---|
| Health checks | live + ready against tagged fingerprint |
| Smoke results | Release Protocol / `docs/ga/RELEASE_CHECKLIST.md` / production smoke doc |
| Incident status | Sev-1 clear statement for claim window |
| Rollback note | Playbook reference + last verification / drill |
| Backup posture | Ack of `docs/production/BACKUP_AND_RECOVERY.md` for release class |

---

### G9 — Production telemetry

| Artefact | Acceptable sources |
|---|---|
| Analytics posture | EP-002 go-live checklist state **or** explicit flag-OFF + no overclaim |
| Operational logging | Sample logs / runbook confirming request/error/slow visibility |
| Soak / dual-run health | Telemetry summaries for flags intended ON |
| Privacy constraints | EVENT_CATALOGUE / analytics privacy acknowledgement |

---

### G10 — Security and data integrity

| Artefact | Acceptable sources |
|---|---|
| Security review | `docs/ga/SECURITY_REVIEW.md` + residual ack for tag |
| Secrets posture | Confirmation production key validation; no secrets in artefacts |
| Dependency audit | `pip-audit` (or successor) review note |
| AuthZ ownership | Test or review note for personal resource scoping |
| Migration / startup | Migration status + StartupService idempotency acknowledgement |

---

### G11 — Test coverage

| Artefact | Acceptable sources |
|---|---|
| CI summary | Pytest + ruff green for candidate |
| Architecture / curriculum suites | Green evidence |
| GA suites | As required for release class |
| Quality-contract suites | Rec / Plan / Readiness tests green when in production defaults |
| Quarantine list | Explicit list of quarantined tests (if any) |

---

### G12 — Production feature-flag readiness

| Artefact | Acceptable sources |
|---|---|
| **Version 1 flag matrix** | Table: flag name, production default, student-visible?, owner, rollback switch, soak prerequisite |
| Config docs | `.env.example` / config references matching matrix |
| Cutover health | Links to dual-run / soak health for each ON educational flag |
| Kill-switch note | How to disable high-risk flags in production |

#### Flag matrix template

| Flag / env | Production default | Student-visible if ON? | Owner | Soak / cutover prerequisite | Rollback |
|---|---|---|---|---|---|
| | ON / OFF | Yes / No | | | |

---

## 5. Validation artefacts (named outputs)

| Artefact | Role |
|---|---|
| Completed Acceptance Checklist | Gate scoring |
| Signed Go / No-Go Decision | Declaration authority |
| Validated KSI Assessment | G1 |
| Constitutional compliance memo | G2 |
| EVF Version Approval Report | G2.4 |
| Explainability coverage pack | G3 |
| Recommendation quality pack | G4 |
| Planning quality pack | G5 |
| Readiness quality pack | G6 |
| Performance pack | G7 |
| Reliability / smoke pack | G8 |
| Telemetry posture note | G9 |
| Security pack | G10 |
| Test / CI pack | G11 |
| Flag matrix | G12 |

---

## 6. Sign-off evidence

Signatures may be:

- Named ack lines in the Go / No-Go Decision, or  
- Linked review comments / email archive IDs, or  
- PR approvals explicitly citing the evidence package path  

Anonymous “LGTM” without package path is insufficient for Version 1 declaration.

---

## 7. Incomplete package rule

If any hard-gate criterion lacks linked evidence → overall outcome is **DEFER** (not silent GO).  
Do not fill gaps with estimated KSI or aspirational programme forecasts.

---

## References

- [`VERSION_1_RELEASE_FRAMEWORK.md`](VERSION_1_RELEASE_FRAMEWORK.md)
- [`VERSION_1_ACCEPTANCE_CHECKLIST.md`](VERSION_1_ACCEPTANCE_CHECKLIST.md)
- [`VERSION_1_GO_NO_GO_GUIDE.md`](VERSION_1_GO_NO_GO_GUIDE.md)
- `knowledge/product/p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md`
- `knowledge/educational_validation/EDUCATIONAL_RELEASE_GATE.md`
- `knowledge/RELEASE_PLAYBOOK.md`

---

**End of VERSION_1_EVIDENCE_REQUIREMENTS**
