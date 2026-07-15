# Kwalitec v0.9.2

## Internal Alpha Stabilization Sprint

Version:

v0.9.2

Status:

Production (Internal Alpha)

---

## Overview

Version 0.9.2 ships the Internal Alpha Stabilization Sprint: mission recommendation integrity, study-plan state synchronization, and student-centred educational messaging.

---

## Highlights

### IA-001 — Mission Recommendation Integrity

Missions are bound to the active study plan (`missions.study_plan_id`). Generate and retrieve paths are plan-scoped so dashboard recommendations and today's mission launch cannot disagree across plan switches or curricula. Legacy unfinished unbound missions are adopted onto the active plan on next generation.

### IA-002 — Study Plan State Synchronization

Activating a study plan synchronizes derived student surfaces (today's mission) and redirects to the dashboard so recommendation, mission, and plan context update without a manual refresh.

### IA-003 — Student-Centred Educational Messaging

Student-facing recommendation and status copy maps Educational Intelligence domain vocabulary to plain educational language. Internal identifiers and intent enums are no longer shown on the recommendation card.

---

## Operator notes

- Classification: Feature Release + Migration Release + Internal Alpha Release
- Risk: High
- Educational data compatibility: **Self-healing** (nullable `study_plan_id`; unfinished orphans rebound on generate; no Internal Alpha reset required)
- Alembic: previous head `202607130002` → new head `202607150001`
- After deploy, confirm Alembic head `202607150001`, `/health` OK, and deployment fingerprint matches tag `v0.9.2`
- Notify Internal Alpha testers of the release window and baseline (`v0.9.2` / release commit)

---

## Rollback

- Application-only: redeploy previous known-good tag and re-verify fingerprint
- Migration: `downgrade()` drops `study_plan_id` / index / FK; prefer forward-fix if live rows already use the column

---

Thank you to everyone contributing to Kwalitec.
