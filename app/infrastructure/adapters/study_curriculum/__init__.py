"""Runtime C adapters for the Study Curriculum assembler.

Read-only wiring of ``EducationalRuntimeEngineService.get_study_progress``
and published artefacts. Does not write Twin state, Study Progress, or
ADR-027 decisions.
"""

from __future__ import annotations
