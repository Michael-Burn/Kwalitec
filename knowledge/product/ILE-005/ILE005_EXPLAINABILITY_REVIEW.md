# ILE-005 — Explainability Review

**Programme / Milestone ID:** ILE-005  
**Title:** Educational Feedback Loop  
**Date:** 2026-07-28  
**Reviewer:** Implementation (completion gate)  
**Surfaces / contracts in scope:** Optional Decision Journal reflection form; internal Sensei review records (not learner-visible)  
**Default explanation level(s):** L2 for reflection invite; governance-only for Sensei assessment  
**Runtime A surfaces touched:** Decision Journal (reflection); Mission complete fail-open review refresh  

---

## Mandatory verification

| # | Requirement | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| R1 | Explanations are evidence-backed | **Pass** | Review assessment cites journal observation/outcome/reflection/evidence only |
| R2 | Confidence communicated appropriately | **Pass** | Evidence quality bands + review states; no numeric fake precision |
| R3 | Student action is clear | **Pass** | Optional Save reflection; skip lawful; no forced CTA on Home |
| R4 | Avoid unnecessary technical detail | **Pass** | Forbidden student + calibration/engagement terms enforced |
| R5 | Consistent across Runtime A | **Pass** | Does not invent alternate tips; journals authorised recommendations only |

## Schema & level checks

| # | Check | Pass / Fail / N/A | Evidence |
|---|---|---|---|
| S1 | Schema fields at declared level | **Pass** | Reflection questions map to usefulness / timing / why / decision quality |
| S2 | Default level matches surface job | **Pass** | Journal reflection is judgement, not daily primary CTA |
| S3 | Reading-time / length targets | **Pass** | Four short optional questions + optional note |
| S4 | EIP-003 four questions | **Pass** | Help / timing / why / same decision |
| S5 | Facts, estimates, advice distinguishable | **Pass** | Student answers vs Sensei assessment separation (`learner_visible=false`) |
| S6 | Advice does not replace Mission authority | **Pass** | No re-selection; calibration only |
| S7 | Pattern catalogue | **Pass** | Aligns with ILE-003 reflection principles |
| S8 | Accessibility | **Pass** | Fieldsets + legends; text labels for choices |

## Verdict

**Pass** — explainability complete for ILE-005 scope (optional reflection + internal calibration).
