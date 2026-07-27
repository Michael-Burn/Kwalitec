# PI-001B — Test Evidence

## Commands

```bash
python3 -m pytest tests/domain/educational_engine_foundation/test_derivation.py \
  tests/application/educational_engine_foundation/test_service.py \
  tests/application/educational_engine_foundation/test_equivalence.py -v

python3 -m pytest tests/application/curriculum_studio_foundation/test_integration.py -v

python3 -m pytest tests/curriculum/test_curriculum_parity.py -v

python3 -m ruff check app/application/educational_engine_foundation \
  app/domain/educational_engine_foundation \
  tests/application/educational_engine_foundation \
  tests/domain/educational_engine_foundation \
  app/application/curriculum_studio_foundation/service.py
```

## Results

- Educational engine foundation tests: **3 passed**
- Existing foundation integration tests: **3 passed**
- Existing curriculum parity tests: **15 passed**
- Ruff: **passed**

## Evidence summary

- Newly published subject derives curriculum graph, study-plan template, mission templates, journey structure, and progress model.
- CS1 published-package derivation matches existing JSON hierarchy/order counts.
- Existing student JSON path remains green after the additive package-shape change.
