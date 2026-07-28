# Release Checklist — Educational Intelligence Platform (PR-001)

Use this checklist before promoting a build that depends on the certified Educational Intelligence Platform.

---

## Pre-release

- [ ] AP-002D7 certification docs present under `knowledge/certification/`
- [ ] `EducationalPipelineOrchestrator` importable
- [ ] `GET /health/educational-intelligence` returns `ready: true`
- [ ] Contract versions match certified matrix (packaging → explanation)
- [ ] Projection / Mission / Tutor registrations available
- [ ] Certification CI job green on the candidate commit
- [ ] Regression fingerprint parity tests green
- [ ] Architecture purity tests green
- [ ] `ruff check .` green
- [ ] Alembic head unchanged (`202607270013` at time of PR-001)
- [ ] No Student UI / Founder UI diffs in the release candidate for this milestone
- [ ] No educational contract version bumps unless intentionally certified

---

## CI gates that must pass

1. Architecture Governance
2. Unit Tests
3. Integration Tests
4. **Educational Intelligence Certification** (`educational-intelligence-certification`)
5. Lint
6. Production Gates

Certification failure **blocks merge**.

---

## Post-deploy smoke

- [ ] `/health/live` → 200
- [ ] `/health/ready` → 200
- [ ] `/health/educational-intelligence` → 200 / `ready: true`
- [ ] Sample pipeline execution (non-production learner or harness) emits `PipelineStarted` … `PipelineCompleted`
- [ ] Logs contain timings without educational payload leakage

---

## Abort criteria

Abort or roll back caller wiring (not migrations) if:

- Health educational-intelligence is not ready
- Certification suite fails on the deployed revision
- Fingerprint parity between orchestrator and certification harness regresses
- Logs begin emitting forbidden educational fields
