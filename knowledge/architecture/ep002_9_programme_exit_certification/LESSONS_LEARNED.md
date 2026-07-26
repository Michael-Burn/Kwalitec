# EP-002.9 — Lessons Learned

**Programme:** EP-002 — Student Intelligence Surface  
**Milestone:** EP-002.9  
**Date:** 2026-07-26

---

## 1. What worked

1. **Observation before authority** — EP-002.1 telemetry and EP-002.4 dual-run prevented premature UX flips and made cutover evidence speakable.  
2. **Ownership speech in every milestone** — repeating Twin / Planner / Readiness / Insight / Runtime A write boundaries prevented scope creep into new engines.  
3. **Fail-open + production hard-ineligibility** — defaults OFF plus `_PRODUCTION_ENVS` gave a stronger safety net than flags alone.  
4. **Shared Foundation DI before multi-surface cutover** — measuring and cutting nested CLS assemble cost early reduced latent latency risk.  
5. **MissionOptimizer explicit quarantine** — deciding “do not wire” removed a latent second mission authority before Daily Plan cutover.  
6. **Presentation consolidation last** — collapsing dual narrators after cutovers (WS7 after WS4–6) avoided inventing a third path during change.  
7. **Explicit non-claims** — refusing T7 / GA / effectiveness claims kept programme success criteria honest.

---

## 2. What was harder than expected

1. **Evidence quality vs harness green** — controlled benches repeatedly passed while live staging packs remained incomplete; architecture completion and ops readiness diverged.  
2. **Process-local metrics** — fast to ship, easy to over-read as durable ops signal.  
3. **Display vs persistence tension (Daily Plan)** — constitutional compliance (no Twin ORM writes) created an accepted student-visible mismatch risk.  
4. **Parallel Experience surfaces** — Runtime A consolidation did not automatically solve `/student` or EI Stage A narrators.  
5. **Programme ID collision with Analytics EP-002** — naming discipline required continuous full-title usage.

---

## 3. Process lessons

1. Require a **staging evidence artefact** as an explicit exit gate when milestones only produce harness benches.  
2. Prefer **surrogate constitutional packs with documented drift** over inventing missing review artefacts (EP-002.7A lesson).  
3. Keep **Outcome A/B/C decision records** for presentation SoT choices — Outcome B (legacy adapter) was the constitutionally safe path.  
4. Treat **hard environment gates** as first-class architecture, not ops folklore.

---

## 4. Architectural lessons

1. Consumer Chain should own **gates and observation**, never maths.  
2. Presentation should own **selection**, never evaluation.  
3. Quarantine orphan optimizers early; do not “wire to make use of them.”  
4. Bundled Shadow / Adaptive TwinInput under Twin ON is acceptable if docs match code.  
5. HTTP cutover ≠ Experience TwinPort Ready ≠ Twin Ready (T7). Keep these gates separate.

---

## 5. Product / student lessons

1. Honest limitation / unavailable speech is part of constitutional compliance, not a UX failure.  
2. Mutual exclusion between EI Stage A and Insight is necessary but not sufficient — residual dual narrators still confuse operators.  
3. Students should not see Twin display claims that contradict the mission they will actually execute without product acceptance of that tension.

---

## 6. What we would repeat

- Sequenced dual-run → gated cutover → presentation consolidation  
- Constitutional impact assessments before implementation milestones  
- Rollback plans with flag-level kill switches and no schema dependency  

## 7. What we would change next time

- Budget a **mandatory live staging soak pack** before programme exit, not as an afterthought  
- Introduce durable metrics earlier for cutover health  
- Decide Experience `/student` narrator scope at programme planning if SOLE_RUNTIME is on the near-term roadmap  
