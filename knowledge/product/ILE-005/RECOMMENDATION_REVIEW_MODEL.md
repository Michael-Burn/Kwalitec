# Recommendation Review Model

**Programme:** ILE-005 — Educational Feedback Loop  

---

## Purpose

Define how Study Sensei guidance is reviewed after the fact — without rewriting the original recommendation or inventing a second selection engine.

---

## Inputs (educational only)

Drawn from Decision Journal records:

- Original observation, meaning, recommendation, evidence, confidence, benefit, uncertainty
- Student action (accepted / deferred / none yet)
- Outcome summary (when recorded)
- Optional student reflection
- Append-only evidence updates

**Excluded inputs:** clicks, streaks, screen time, DAU, engagement scores.

---

## Evidence quality bands

| Band | Typical signals |
|---|---|
| Insufficient | Thin prior evidence; no outcome; no reflection; no updates |
| Limited | One educational signal (action, outcome, reflection, or update) |
| Adequate | Several converging educational signals |
| Strong | Outcome + reflection + prior evidence + confident band |

---

## Review states

| State | When |
|---|---|
| Requires future observation | No learner response yet, or response without outcome/reflection |
| Evidence insufficient | Confidence / evidence still too thin to judge usefulness |
| Inconclusive | Signals present but not decisive |
| Partially supported | Mixed reflection, or outcome without affirming reflection |
| Supported by later evidence | Affirming reflection + outcome (and adequate evidence) |

Assessment is **deterministic** from the same inputs.

---

## Append-only rule

- Original recommendation snapshots are immutable.
- Reviews append Sensei educational review rows and optional journal evidence lines.
- Student-facing journal never shows Sensei “future learning” governance text as a score.

---

## Non-goals

- No re-ranking of next tips
- No Twin mutation
- No mastery theatre
- No engagement optimisation
