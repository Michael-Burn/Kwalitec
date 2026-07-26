# Lessons Learned — EP-004 Private Beta Execution

**Programme:** EP-004  
**Date:** 2026-07-24  
**Scope:** Stage 0 execution + programme packaging (Stage 1–2 not yet live)

---

## 1. What worked

1. **Separating execution from definition** — EP-003 froze M1–M9 and protocol; EP-004 only fills evidence. Prevented metric drift under launch pressure.  
2. **Stage 0 before external invites** — Internal participants + GREEN monitoring create a safe on-ramp without privacy exposure.  
3. **Honest empty cells** — Labelling Week 0 as exploratory / insufficient N preserved Vision trust posture better than inventing “on track” KPIs.  
4. **EP-002 kill switch as rollback** — Env flag OFF is sufficient rollback for analytics without code revert or educational behaviour change.  
5. **Feedback coding early** — Seeding the register from educational review themes (naming, Twin, Journey provisional) means Stage 1 interviews start with a prior, not a blank wishlist.

---

## 2. What was harder than expected

1. **Privacy sign-off is the real critical path** — Not engineering. Stage 1 cannot honestly start without checklist signatures.  
2. **Two different “GO” meanings** — Easy to conflate “GO to run closed beta” with “GO educational effectiveness.” EP-004 must keep both verdicts explicit.  
3. **M5 / Journey** — Provisional sources require constant labelling discipline until ADR-026 production emit.  
4. **Staff vs external N** — Dogfood participants must not silently inflate the 20–50 exit bar.

---

## 3. Process changes to keep

| Practice | Keep? |
|---|---|
| Pseudonymous cohort IDs in knowledge docs (no PII) | Yes |
| Per-stage Go / Rollback / Monitoring triad | Yes |
| Weekly scorecard with claim-level row | Yes |
| Feedback categories Bug / UX / EDU / OPS / FPRD | Yes |
| Conditions list on Go / No-Go | Yes |

---

## 4. Follow-ups (not EP-004 scope to implement)

| Item | Owner programme |
|---|---|
| Sign Privacy Review | Ops / Security + Product |
| Journey production emit | ADR-026 follow-through |
| Staffed support rota | Version 1 Readiness — Support |
| Production cohort load test | GA residual |
| Recommendation effectiveness PRD | Future PRD (excluded) |
| Copy governance for Coach / Session naming | Product language / experience |

---

## 5. Anti-patterns observed / avoided

| Anti-pattern | Status |
|---|---|
| Fabricating external KPI values to “complete” the programme | Avoided |
| Enabling analytics for external users without privacy | Avoided (HOLD) |
| Counting Stage 0 staff toward EP-003 N=20 | Avoided (explicit table) |
| Changing Twin / ESS to improve scorecard optics | Avoided |
| Treating GA certification as educational GO | Avoided (dual verdict) |

---

## 6. One-sentence takeaway

**Controlled private beta is an operations and honesty problem first: freeze the metrics, stage the risk, and refuse to claim learning outcomes until the cohort and weeks exist.**
