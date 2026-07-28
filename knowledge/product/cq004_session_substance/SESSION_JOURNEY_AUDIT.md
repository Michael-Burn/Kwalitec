# CQ-004 — Session Journey Audit

**Programme:** CQ-004 — Session Substance  
**Date:** 2026-07-28  
**Path audited:** Production sole-runtime (`KWALITEC_V2_SOLE_RUNTIME=1`) — Activity entry through session completion  
**Method:** Code + template inspection; CQ-002/CQ-003 residual inventory; CR4 lens

---

## 1. Journey map

```
Session entry
  Home/Revision auto-begin → Activity
  (fallback) Overview → Start Session → Activity
  Friction: Overview intro ignores topic; duplicate Time card;
            auto-begin failure forces second Start

Active study
  Activity N of M · question · answer · explanation · advance
  Friction: generic prompts; thin/dict explanations;
            mechanical Submit→reload→Continue; Quick Check fork;
            final CTA still “Continue”

Progress feedback
  Progress bar on Activity only (% / completed / remaining)
  Friction: bar lags until advance; lost after last activity

Session completion
  Reflection → Summary → Return Home (POST finish)
  Friction: long reflection disclaimer; “Session summary”
            not celebratory; Complete template unused on happy path

Exit / next-step continuity
  Flash → Home with commitment reflection (5 fields) + next Mission
  Friction: double reflection (session + Home); flash is generic
```

---

## 2. Friction inventory (substance lens)

| ID | Moment | Friction | Severity | V1 fix? |
|---|---|---|---|---|
| S01 | Activity content | Generic “Practice item N” / “Question N” — not topic-threaded | **Critical** | Yes |
| S02 | Activity feedback | Explanation dict / Twin-evidence wording — weak payoff | **Critical** | Yes |
| S03 | Activity loop | Two POSTs; final CTA not “Continue to Reflection” | **Major** | Yes (labels + flash) |
| S04 | Overview | Intro ignores `topic_title`; duplicate timer card | **Major** | Yes |
| S05 | Activity | Quick Check embed mid-practice | **Med** | Yes (suppress) |
| S06 | Reflection entry | No “activities complete” transition | **Med** | Yes |
| S07 | Summary | “Session summary” not completion celebration | **Major** | Yes |
| S08 | Home after finish | Five-field commitment reflection after session reflection | **Med** | Yes (compact) |
| S09 | Question card | Duplicate answer_prompt as H2 + label | **Minor** | Yes |
| S10 | Mid-session leave | Brand Home without confirm (CQ-003 H07) | **Med** | Deferred |
| S11 | Resume hop | Continue → overview redirect (CQ-003 residual) | **Minor** | Deferred |

---

## 3. What already works (substance enablers)

- Linear Overview → Activity → Reflection → Summary with enforced navigation
- Honest 4-step chrome (phantom Complete removed in CQ-002)
- One-click Home/Revision entry into Activity (CQ-002/CQ-003)
- Resume integrity restores active surface
- Reflection framing separates Session reflection from Decision Journal
- Finish links commitment lifecycle; next recommendation on Summary

---

## 4. Audit verdict

**CR4 remains Emerging (45)** because the **educational core inside Activity** often reads as placeholder while Home promises topic-specific mission value. Highest-leverage V1 work: thread topic into activity/explanation copy, fix explanation rendering, strengthen completion closure, remove Activity Quick Check fork — without new capabilities.

---

**End of Session Journey Audit**
