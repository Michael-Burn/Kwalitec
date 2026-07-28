# ILE-001C — Completion Report

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Milestone:** ILE-001C — Contextual Intent & Educational Framing  
**Date:** 2026-07-28  
**Status:** Complete  
**Commit message:** `feat(ile-001c): implement contextual intent and educational framing`

---

### Summary

ILE-001C delivers the first complete Study Sensei guidance experience on Adaptive Assessment entry points. When contextual framing is enabled, learners see a Context Card before Quick Check, an expanded reflection with student choice, an Educational Summary after completion, and recommendation framing (reason, evidence, qualitative confidence, expected benefit, uncertainty, and “Why this recommendation?”). All speech is composed from the copy registry per ILE-001C0 standards. Feature flag `KWALITEC_CONTEXTUAL_FRAMING` defaults OFF; with framing off, ILE-001B behaviour is preserved. No Twin, Reasoning, selection, Mission planning, Tutor, readiness, or curriculum logic changes.

### Files Created

**Application**

- `app/application/adaptive_assessment/educational_framing.py`

**Templates**

- `app/templates/adaptive_assessment/components/recommendation_frame.html`

**Tests**

- `tests/application/adaptive_assessment/test_contextual_framing.py`

**Documentation**

- `knowledge/product/ILE-001/CONTEXTUAL_INTENT_UX.md`
- `knowledge/product/ILE-001/IMPLEMENTATION_NOTES_ILE001C.md`
- `knowledge/product/ILE-001/ILE001C_COMPLETION_REPORT.md` (this report)
- `knowledge/product/ILE-001/ILE001C_EXPLAINABILITY_REVIEW.md`
- `knowledge/product/ILE-001/ILE001C_RECOMMENDATION_REVIEW.md`

### Files Modified

- `app/application/adaptive_assessment/__init__.py`
- `app/application/adaptive_assessment/copy_registry.py`
- `app/application/adaptive_assessment/feature_flags.py`
- `app/application/adaptive_assessment/telemetry.py`
- `app/application/adaptive_assessment/quick_check_contracts.py`
- `app/application/adaptive_assessment/quick_check_experience.py`
- `app/presentation/adaptive_assessment/forms.py`
- `app/presentation/adaptive_assessment/routes.py`
- `app/templates/adaptive_assessment/base.html`
- `app/templates/adaptive_assessment/introduction.html`
- `app/templates/adaptive_assessment/reflection.html`
- `app/templates/adaptive_assessment/completion.html`
- `app/templates/adaptive_assessment/components/entry_card.html`
- `app/static/css/adaptive_assessment/quick_check.css`
- `app/static/js/adaptive_assessment/quick_check.js`
- `tests/application/adaptive_assessment/test_product_foundations.py`
- `knowledge/product/ILE-001/QUICK_CHECK_UX.md`
- `knowledge/product/ILE-001/STUDENT_JOURNEYS.md`
- `knowledge/product/ILE-001/TELEMETRY_GUIDE.md`
- `knowledge/product/ILE-001/FEATURE_FLAG_STRATEGY.md`
- `knowledge/product/ILE-001/IMPLEMENTATION_ROADMAP.md`
- `knowledge/product/MICROCOPY_LIBRARY.md`

### Tests Executed

```bash
.venv/bin/python -m ruff check app/application/adaptive_assessment app/presentation/adaptive_assessment tests/application/adaptive_assessment
.venv/bin/python -m pytest tests/application/adaptive_assessment tests/architecture tests/certification/educational_intelligence -q
```

| Suite | Outcome |
|---|---|
| Adaptive Assessment + architecture + EI certification (2222) | Pass |
| Ruff (scoped) | Pass |

### Migration Impact

None.

### Architecture Compliance

- Layering preserved: templates/JS → blueprints → application framing/experience → registries; no educational engines touched.
- Curriculum V1/V2 invariants: **preserved** (no curriculum changes).
- Single Authority Rule: framing narrates presentation intent only; does not invent Twin/Reasoning ranking.
- Feature flags default OFF; backward compatible with ILE-001B when framing is off.

### Technical Debt

- Evidence band defaults to `emerging` (presentation stub); richer Mission/Twin-visible eligibility inputs deferred.
- Density / time-gate UX from ILE-001.C roadmap residual still open.
- Telemetry sink remains in-memory / port-only.
- Expand endpoint is fetch/204-only (no HTML fallback navigation).

### Known Limitations

- Framing flag OFF in production by default — no automatic activation.
- No adaptive selection, Twin writes, or recommendation engine changes.
- English defaults only.
- Confidence labels are qualitative copy, not live Twin confidence.

### Student Impact Assessment

**Template:** `knowledge/product/p001_1_ksi_baseline/STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`

| Field | Value |
|---|---|
| **Student-visible change?** | Yes, when AA + Quick Check + contextual framing flags are enabled |
| **Production activation?** | None by default (flags OFF) |
| **Related KSI categories** | K2 (recommendation clarity), K8 (explainability) — estimated only |

**Student problem:** Learners began Quick Checks without understanding why the check appeared now, and completion felt like a task receipt rather than educational guidance.

**Student benefit:** Every check can open with observation → meaning → purpose → benefit → invitation, and close with what was learned / evidence / meaning / next — plus honest recommendation framing and student choice.

**Final Test:** Helps students become better professionals? **Yes (when enabled)** — by making guidance explainable and agency-preserving rather than instructional.

**Learning benefit:** Reduces uncertainty about “why this activity”; keeps recommendations educational rather than algorithmic; never pretends certainty when evidence is thin.

**Success metrics:** Student can answer why / why now / what evidence / what next / what if I wait after a framed run; unit/integration/UI/a11y/telemetry tests green; ILE-001B path intact when framing off.

**Risks:** Copy still provisional until dogfood copy review; default emerging band may over-speak if enabled before eligibility wiring — mitigate by keeping flag OFF and reviewing before cohort enablement.

**Assumptions:** Downstream programmes will feed honest presentation intent bands without moving educational authority into the experience layer.

### Estimated KSI contribution

**ΔKSI ≈ +2 (estimated, not validated)** — presentation explainability and recommendation honesty on AA surfaces when enabled; no production activation, so validated ΔKSI = 0 until dogfood evidence.

| Category | Estimated delta | Notes |
|---|---|---|
| K2 Recommendation quality | +1 | Framing structure + uncertainty honesty |
| K8 Explainability | +1 | Context Card + Why recommendation |
| Others | 0 | |

### Evidence collected

- `tests/application/adaptive_assessment/test_contextual_framing.py`
- `tests/application/adaptive_assessment/test_quick_check.py` (regression)
- `knowledge/product/ILE-001/ILE001C_EXPLAINABILITY_REVIEW.md`
- `knowledge/product/ILE-001/ILE001C_RECOMMENDATION_REVIEW.md`
- Framing contracts and templates under `app/application|presentation|templates/adaptive_assessment/`

### Lessons learned for student value

Sensei behaviour becomes visible through arcs and uncertainty honesty, not through labelling the product “AI.” Keeping framing behind a separate flag lets Quick Check ship for perception safety while Sensei speech is reviewed independently.

### Explainability Review

See `ILE001C_EXPLAINABILITY_REVIEW.md` — **Pass** (presentation-level; no new intelligence claims).

### Recommendation Quality Review

See `ILE001C_RECOMMENDATION_REVIEW.md` — **Pass** (framing only; ranking/selection unchanged).

### Version 1 readiness residual

**N/A** — does not claim Version 1 production-ready progress. Residual gates remain per `VERSION_1_RELEASE_FRAMEWORK.md`.

---

**End of ILE001C_COMPLETION_REPORT**
