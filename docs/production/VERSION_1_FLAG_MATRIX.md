# Version 1 Feature-Flag Matrix (G12)

**Programme:** EI-001.3 — Release Operations & Deployment Evidence  
**Authority:** P-002.1 Gate G12 · ER-RB-06 · `knowledge/release/RP-001/FEATURE_FLAG_REGISTER.md`  
**Date:** 2026-07-28  
**Claim class covered:** Invite-only Internal Alpha / engineering Version 1 evidence (not a Version 1 production-ready declaration)  
**Production source of truth:** `render.yaml`  
**Local template:** `.env.example` (commented defaults; unset = OFF unless noted)

---

## 1. Purpose

Publish the Version 1 **production flag matrix** so every student-visible educational flag has an intentional default, owner, soak prerequisite, and kill-switch / rollback path (G12.1–G12.6).

This artefact **does not** flip flags. It documents current production intent.

---

## 2. Production-ON flags (Render)

| Flag / env | Production default | Student-visible if ON? | Owner | Soak / cutover prerequisite | Rollback / kill-switch |
|------------|-------------------|------------------------|-------|-----------------------------|------------------------|
| `KWALITEC_V2_SOLE_RUNTIME` | **ON** (`1`) | Yes — canonical home `/student/` | Release + Architecture | EP-007.1 consolidation evidence; sole-runtime smoke | Set `0` / unset; redeploy — re-exposes legacy homes (CAP-30 risk; document) |
| `KWALITEC_V2_STUDENT_EXPERIENCE` | **ON** (`1`) | Yes — `/student/*` | Engineering | Forced ON when sole runtime ON | Unset with sole OFF together |
| `KWALITEC_V2_DURABLE_STORE` | **ON** (`1`) | Indirect — Experience/Session SQL | Engineering | Schema/migrations at head | Unset → in-memory / non-durable path; data loss risk — prefer forward fix |
| `KWALITEC_V2_INJECT_ENGINES` | **ON** (`1`) | Indirect — opaque bridges | Engineering | Durable store ON | Unset (also auto-ON when durable ON in resolver) |
| `KWALITEC_V2_SEED_DEMO` | **OFF** (`0`) | No (demo data) | Engineering | Must stay OFF in prod | Keep `0`; never set `1` in prod |
| `KWALITEC_V2_FOUNDER_INTELLIGENCE` | **ON** (`1`) | **No** — founder console only | Product / Founder | Console RBAC | Unset |
| `KWALITEC_EI_INTERNAL_ALPHA` | **ON** (`1`) | Indirect — Twin-first composer wiring; EI missions/explainability/progress remain OFF by code | Engineering + Product | RP-001 Alpha inventory | Unset — do **not** read as “all EI widgets ON” |
| `KWALITEC_COMMERCIAL_LOOP` | **ON** (`1`) | Indirect — enables SR student-value bundle when child flags inherit | Product + Engineering | KWP-002 commercial profile | Set `0` / unset; redeploy |

### 2.1 Deliberate hold — `SR_TWIN_DAILY_LOOP` (2026-08-30)

| Field | Record |
|-------|--------|
| **What** | Twin daily-loop consumption / new Twin writes paused (`SR_TWIN_DAILY_LOOP=0` in `render.yaml`) |
| **When** | 2026-08-30 |
| **Why** | Architecture review (ADR-027) found multiple unreconciled Estimated Knowledge / mastery representations. Continuing Twin daily-loop writes only grows the volume needing eventual reconciliation; raw session evidence packages persist independently and remain replayable later. |
| **Nature** | Deliberate hold — **not** a rollback of the underlying Twin capability, and **not** a change to `KWALITEC_COMMERCIAL_LOOP` or other SR_* commercial-bundle flags |
| **Production default** | **OFF** (`0`) — explicit override; without this key the flag would inherit ON from `KWALITEC_COMMERCIAL_LOOP` |
| **Data** | Existing Twin documents remain intact; nothing was deleted or modified. This hold affects **future writes only** |
| **Authority** | `docs/adr/ADR-027-student-knowledge-state-and-adaptive-decision-architecture.md` |
| **Resume** | After ADR-027 reconciliation work: remove the `SR_TWIN_DAILY_LOOP` env entry (restore inheritance) or set to `1`, then redeploy |
| **Deploy note** | Captured in version control; takes effect on production only at the next manual deploy (deploy was intentionally paused when this hold was recorded) |

---

## 3. Production-OFF educational / intelligence flags (must not be marketed as live)

| Flag / env | Production default | Student-visible if ON? | Owner | Soak / cutover prerequisite | Rollback / kill-switch |
|------------|-------------------|------------------------|-------|-----------------------------|------------------------|
| `KWALITEC_DIGITAL_TWIN` | **OFF** | Indirect DI / tutor dependency | Architecture | Dual-run / soak packs | Unset / `0` |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | **OFF** | Yes if ON (Twin Foundation port) | Architecture | Twin ON + soak | Unset |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | **OFF** | Yes if ON | Architecture | Twin ON; non-prod eligibility historically | Unset |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | **OFF** | Yes if ON | Architecture | Twin ON | Unset |
| `KWALITEC_DAILY_PLAN_CUTOVER` | **OFF** | Yes if ON | Architecture | Twin ON | Unset |
| `KWALITEC_UNIFIED_JOURNEY` | **OFF** | Yes if ON | Product | Journey soak | Unset |
| `KWALITEC_EXPERIENCE_FEEDBACK` | **OFF** | Yes if ON (Home “Your Journey”) | Product | Unified Journey ON | Unset |
| `KWALITEC_LEARNING_FEEDBACK` | **OFF** | No UI authority | Product | EP-004 soak | Unset |
| `KWALITEC_PERSONAL_LEARNING_PROFILE` | **OFF** | No educational authority | Product | EP-004.1 + G12 re-cert | Unset |
| `KWALITEC_ADAPTIVE_ENGINE` / `SHADOW` / `AUTHORITY` | **OFF** | Yes if authority ON | Engineering | Adaptive soak ladder | Unset |
| `KWALITEC_ADAPTIVE_ASSESSMENT` (+ Quick/Deep/…) | **OFF** | Yes if master ON | Product | ILE/adaptive inventory | Unset master |
| `KWALITEC_*_BRIDGE` / continuity / umbrella bridges | **OFF** unless explicitly set | Indirect | Engineering | Bridge soak | Unset |
| `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1` | **OFF** | No UI — emit only | Release | EP-002 go-live checklist + cron/worker | Unset |
| Advisory / recovery / simulation / trials / evidence review family | **OFF** | Mostly non-student or advisory | Architecture | Per programme soak | Unset each flag |
| Runtime C / founder-student bridge family | **OFF** | Yes if ON | Architecture | Platform integration soak | Unset |
| `KWALITEC_ADR027_M0_DECISION_BOUNDARY` | **OFF** (unset; never set in `render.yaml` for this merge) | Indirect: Decision Engine path for Runtime C daily sitting when ON | Architecture | ADR-027 M0 dual-path suite green; deliberate soak | Unset / `0`; redeploy returns to inlined `generate_daily_mission` selection |
| `KWALITEC_ADR027_PHASE2_TWIN_CUTOVER` | **OFF** (unset; never set in `render.yaml` for this merge) | Indirect: Stack A/C EK writes skipped and Stage A / Runtime C EK readers use Learner Twin Query when ON | Architecture | ADR-027 Phase 2 Stage 2 dual-path suite green; deliberate soak; resume of `SR_TWIN_DAILY_LOOP` is a separate operator step | Unset / `0`; redeploy restores Stack A/C EK write+read behaviour |

Full inventory (including Alpha posture notes): `knowledge/release/RP-001/FEATURE_FLAG_REGISTER.md`.

---

## 4. Claim language rules (G12.2–G12.3)

1. Version 1 **invite-only Alpha** claims may reference sole-runtime Education OS home behaviour (production-ON flags above).  
2. Twin cutovers, Unified Journey, personalisation, adaptive assessment, analytics emit, and Runtime C **must not** be marketed as live student capability while OFF.  
3. Flipping any production-OFF educational flag to ON requires: matrix update, soak evidence (G12.4), Product + Release acknowledgement, and claim-language refresh.

---

## 5. Emergency kill-switch procedure (G12.6)

For high-risk educational flags (Twin cutovers, adaptive authority, personalisation, Unified Journey):

1. Set the env var to `0` / unset in the hosting secret store (`render.yaml` / Render dashboard).  
2. Redeploy the same git tag (no code change required).  
3. Verify `/health/ready` and canonical student home smoke.  
4. Record the change in the release / incident report.  
5. Update this matrix if the new default is intended to persist.

Sole-runtime OFF is a **rollback of home authority**, not a feature expansion — treat as CAP-30 risk and document.

---

## 6. Config alignment checklist (G12.5)

| Source | Alignment |
|--------|-----------|
| `render.yaml` | Production-ON keys in §2 match values `1`/`0` as listed |
| `.env.example` | Documents the same env names; local defaults remain OFF unless operator sets |
| `app/application/config/v2_flags.py` | Resolver truth for V2 family |
| RP-001 Feature Flag Register | Detailed Alpha inventory; this matrix is the G12 declaration board |

---

## 7. Gate score (engineering)

| Criterion | Status |
|-----------|--------|
| G12.1 Published matrix | **Met** — this document |
| G12.2 ON flags match claimed behaviour | **Met** for invite-only Alpha claim class |
| G12.3 OFF flags not marketed live | **Met** — claim rules §4 |
| G12.4 Soak for every ON educational flag | **Met** for current ON set (sole-runtime stack); OFF flags N/A until enablement |
| G12.5 `.env.example` / config match | **Met** — names aligned; see checklist §6 |
| G12.6 Kill-switch documented | **Met** — §5 |

**Board posture:** G12 may be scored **PASS** for the invite-only / engineering claim class once Product + Release acknowledge this matrix. Does **not** alone declare Version 1 production-ready (G1–G6 educational gates remain).

---

**End of VERSION_1_FLAG_MATRIX**
