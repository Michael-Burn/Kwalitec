# EP-004.3 — Risk Assessment

**Programme:** EP-004.3 — Adaptive Planning Personalisation  
**Date:** 2026-07-26  

| ID | Risk | Likelihood | Impact | Mitigation | Residual |
|---|---|---|---|---|---|
| R1 | Profile becomes a second planner | Low | Critical | Evidence-only Port; no mission invention; educational order hard-check | Low |
| R2 | Educational priorities silently reordered | Low | High | Abort personalisation on order violation; tests | Low |
| R3 | Over-personalisation from thin samples | Medium | Medium | Confidence ≥ 0.3 and sample ≥ 3 | Low–Med |
| R4 | Accept/dismiss drives plans | Low | High | Responsiveness attribute explicitly unused | Low |
| R5 | Equivalent topic swap feels arbitrary | Medium | Medium | Only among revision_priorities; explain factor; only when follow-through low | Med |
| R6 | Presentation invents personalisation | Low | High | Adapter pass-through only; docs + tests | Low |
| R7 | Flag-OFF regression | Low | Medium | Fail-open; EP-003.3 tests retained | Low |
| R8 | Process-local profile drift across workers | Medium | Low | Inherited EP-004.1 limitation; gated OFF by default | Med |

**Stop condition:** Halt if constitutional ownership would be violated (profile inventing missions or owning educational priorities).
