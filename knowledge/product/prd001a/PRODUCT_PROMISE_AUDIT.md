# PRD-001A — Product Promise Audit

## Question

> If a student reads the landing page and then uses the product for one hour, does the experience fulfil the promises made?

**Landing surface:** `app/templates/auth/login.html` + `app/brand_identity.py` (no separate marketing site).

---

## Promise-by-promise

| Landing / Blueprint promise | One-hour experience | Fulfilled? | Evidence |
|---|---|---|---|
| **Education Operating System** | Single EOS chrome after DEP-003; jargon may confuse but shell is unified | **Mostly** | Sole runtime + eos layout |
| **Know exactly what to study next** | After plan creation, Home offers a concrete session CTA | **Yes operationally** / **Partial intellectually** | Mission generated; reason may feel generic |
| Always know what to study next | Holds once plan + mission exist; empty before | **Yes with setup** | Wizard → Home |
| Plans that fit your exam date | Wizard collects exam date + minutes; creates plan | **Yes** | Study Plan wizard |
| Focused sessions without decision fatigue | `/session/*` guided flow reduces in-session choice | **Yes** | Session routes |
| Honest progress you can trust | Progress vs EK distinction exists in constitution/legacy; EOS under-shows EK; History simpler than legacy analytics | **Partial** | Journey yes; EK weak; charts redirected |
| Sustainable pace through exam season | Minutes from plan; burnout recs exist but quiet | **Partial** | Plan minutes; limited pacing UI |
| Blueprint: what / why / understand / next | What + next strong; why medium; **understand weak** | **Partial** | Readiness helps; EK/Twin weak |
| Blueprint: Digital Twin companion | Twin OFF; unnamed; not experienced | **No** (V1 admits incomplete cutover — still a promise gap vs “what Kwalitec is”) | Flags + product language |
| Blueprint: evidence-driven recommendations | Sequential curriculum + packaged explanations; limited evidence influence on mission | **Partial** | Mission audit |
| Invite-only Internal Alpha | Accurate | **Yes** | Login note |

---

## One-hour narrative (CS1 founding cohort)

1. Sign in — brand promise set high (“Education Operating System”).  
2. Onboarding + wizard — planning promise kept.  
3. Calibration — coverage declarations (easy to confuse with understanding).  
4. Home — today’s mission for topic 1.1 with Why/Why now if MES filled.  
5. Start session — focused work; CMP still on desk (correct adjacency).  
6. Look for Twin / EK / CMP map / analytics depth — **not found** on primary surfaces.  
7. Emotional residue: “It told me what to do” **and** “I don’t feel known.”

---

## Overall answer

**No — not fully.**  
**Yes — for the narrow operational promise of a planned next session.**

The landing page’s strongest line (“Know exactly what to study next”) is the most fulfilled. The Blueprint’s richer identity (“Digital Twin of the student's educational journey”, evidence-driven understanding, explainable educational intelligence as lived experience) is **not** fulfilled in one hour under current production flags and Learning Mode law.

That mismatch — not missing login or missing mission rows — is the Product Integrity failure mode.

---

## Promise integrity recommendation

Either:

1. **Narrow landing/Blueprint student language** to Version 1’s true contract (syllabus-guided daily session + readiness honesty), or  
2. **Raise the experience** to match Twin/EK/syllabus-visibility expectations,

…but do not leave high Twin/OS rhetoric beside sequential Learning Mode without naming the contract.
