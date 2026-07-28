# Educational Intelligence — Replay Report

**Milestone:** AP-002D7  
**Date:** 2026-07-28  
**Verdict:** PASS — identical evidence yields identical artefacts  

---

## Guarantee

For fixed timestamps and identical Evidence Bundle inputs, the certification harness produces identical:

- `EducationalObservationSet`
- `EducationalDecisionSet`
- Twin belief fingerprint (mastery / confidence / reasoning history ids)
- Learning Graph projection fingerprint
- `StudyMissionPlan` fingerprint
- `TutorExplanation` fingerprint

No nondeterministic ordering, wall-clock leakage, or random identifiers were observed under certified fixtures.

---

## Replay fixtures

| Scenario | Purpose | Result |
|---|---|---|
| `cold_start_learner` | Empty Twin, first evidence cycle | Identical replay |
| `returning_learner` | Prior belief + new evidence | Deterministic accumulation |
| `strong_evidence` | Multi-item correct evidence | Identical replay |
| `weak_evidence` | Thin / scaffolded evidence | Identical + honest uncertainty |
| `conflicting_evidence` | Correct/incorrect mix | Identical + no overstated mastery |
| `duplicate_submission` | Same bundle twice | Bitwise-identical fingerprints |
| `version_mismatch` | Unsupported packaging version | Rejected (`UnsupportedEvidenceSchema`) |
| `partial_evidence` | Single sparse item | Identical + honesty preserved |

Fixture source: `tests/certification/educational_intelligence/fixtures.py`.

---

## Method

1. Build scenario fixture (`EvidenceBundleDTO` at `AP-002C.1`, except version mismatch).
2. Run `EducationalIntelligencePipelineHarness.run_fixture`.
3. Re-run with a fresh harness instance and identical cold-start Twin seed.
4. Assert stage fingerprints equal.

---

## Findings

- Observation / decision / twin / projection / mission / explanation fingerprints match across replay.
- Unsupported packaging versions fail closed before interpretation completes.
- Returning-learner accumulation changes belief deterministically; replaying the same returning cycle from the same prior Twin seed remains identical.

---

## Residual notes

- In-process projection / planning / explanation ledgers remain process-local (as delivered in D4–D6). Cross-restart durable SQL audit is deferred, not required for this certification.
- Stage services intentionally remain separately invokable; certification does not wire a production auto-orchestrator.
