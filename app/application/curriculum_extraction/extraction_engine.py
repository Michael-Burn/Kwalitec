"""Curriculum Extraction Engine — public facade (EI-002).

Transforms Canonical Structured Documents (CMP + Syllabus) into a draft
Curriculum Knowledge Graph with provenance, confidence, and validation.

Does NOT publish. Does NOT accept PDF bytes. Does NOT touch Twin / missions /
student runtime.
"""

from __future__ import annotations

from app.application.curriculum_extraction.curriculum_segmentation_service import (
    CurriculumSegmentationService,
)
from app.application.curriculum_extraction.document_import_service import (
    DocumentImportService,
)
from app.application.curriculum_extraction.draft_edition_persistence_service import (
    DraftEditionPersistenceService,
)
from app.application.curriculum_extraction.draft_graph_constructor import (
    DraftGraphConstructor,
)
from app.application.curriculum_extraction.dto import (
    ExtractionRequest,
    ExtractionResult,
)
from app.application.curriculum_extraction.educational_object_extractor import (
    EducationalObjectExtractor,
)
from app.application.curriculum_extraction.exceptions import (
    CurriculumExtractionError,
)
from app.application.curriculum_extraction.graph_validation_service import (
    GraphValidationService,
)
from app.application.curriculum_extraction.relationship_discovery_service import (
    RelationshipDiscoveryService,
)
from app.application.curriculum_extraction.structural_parser_service import (
    StructuralParserService,
)
from app.domain.curriculum_extraction.validation import ValidationReport


class CurriculumExtractionEngine:
    """Orchestrate the modular Curriculum Extraction Pipeline."""

    ENGINE_ID = "curriculum_extraction"
    ENGINE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        importer: DocumentImportService | None = None,
        parser: StructuralParserService | None = None,
        segmenter: CurriculumSegmentationService | None = None,
        extractor: EducationalObjectExtractor | None = None,
        relationship_discovery: RelationshipDiscoveryService | None = None,
        constructor: DraftGraphConstructor | None = None,
        validator: GraphValidationService | None = None,
        persistence: DraftEditionPersistenceService | None = None,
    ) -> None:
        self.importer = importer or DocumentImportService()
        self.parser = parser or StructuralParserService()
        self.segmenter = segmenter or CurriculumSegmentationService()
        self.extractor = extractor or EducationalObjectExtractor()
        self.relationship_discovery = (
            relationship_discovery or RelationshipDiscoveryService()
        )
        self.constructor = constructor or DraftGraphConstructor()
        self.validator = validator or GraphValidationService()
        self.persistence = persistence or DraftEditionPersistenceService()

    def extract(self, request: ExtractionRequest) -> ExtractionResult:
        """Run the full extraction pipeline for CMP + Syllabus.

        When ``request.persist`` is True and validation passes, writes a draft
        edition to ``ckg_*`` tables. Validation blockers prevent persistence.
        """
        stage_trace: list[str] = []
        diagnostics: list[str] = []

        try:
            imported = self.importer.import_documents(
                cmp_document=request.cmp_document,
                syllabus_document=request.syllabus_document,
                subject_code=request.subject_code,
            )
            stage_trace.append(DocumentImportService.STAGE_ID)
            diagnostics.extend(imported.diagnostics)

            syllabus_parse = self.parser.parse(imported.syllabus)
            cmp_parse = self.parser.parse(imported.cmp)
            stage_trace.append(StructuralParserService.STAGE_ID)
            diagnostics.extend(syllabus_parse.diagnostics)
            diagnostics.extend(cmp_parse.diagnostics)

            tree = self.segmenter.segment(
                subject_code=request.subject_code,
                edition_label=request.edition_label,
                subject_title=request.subject_title,
                provider=request.provider,
                syllabus_parse=syllabus_parse,
                cmp_parse=cmp_parse,
            )
            stage_trace.append(CurriculumSegmentationService.STAGE_ID)
            diagnostics.extend(tree.diagnostics)

            catalogue = self.extractor.extract(tree)
            stage_trace.append(EducationalObjectExtractor.STAGE_ID)
            diagnostics.extend(catalogue.diagnostics)

            relationships = self.relationship_discovery.discover(
                catalogue, tree
            )
            stage_trace.append(RelationshipDiscoveryService.STAGE_ID)
            diagnostics.extend(relationships.diagnostics)

            bundle = self.constructor.construct(catalogue, relationships)
            stage_trace.append(DraftGraphConstructor.STAGE_ID)
            diagnostics.extend(bundle.diagnostics)

            validation = self.validator.validate(bundle)
            stage_trace.append(GraphValidationService.STAGE_ID)

            edition_id: str | None = None
            persisted = False
            if request.persist and validation.passed:
                edition_id = self.persistence.persist(
                    bundle=bundle,
                    validation=validation,
                    job_id=request.job_id,
                    source_cmp_ref=request.cmp_document.source_ref,
                    source_syllabus_ref=request.syllabus_document.source_ref,
                )
                stage_trace.append(DraftEditionPersistenceService.STAGE_ID)
                persisted = True
            elif request.persist and not validation.passed:
                diagnostics.append(
                    "Validation blockers present; draft not persisted"
                )

            return ExtractionResult(
                job_id=request.job_id,
                edition_id=edition_id,
                graph=bundle.graph,
                provenance=bundle.provenance,
                validation=validation,
                persisted=persisted,
                diagnostics=diagnostics,
                stage_trace=stage_trace,
            )
        except CurriculumExtractionError:
            raise
        except Exception as exc:  # noqa: BLE001 — map unexpected stage errors
            raise CurriculumExtractionError(
                f"Extraction failed: {exc}",
                stage=stage_trace[-1] if stage_trace else None,
            ) from exc

    def validate_only(self, request: ExtractionRequest) -> ValidationReport:
        """Run pipeline without persistence and return the validation report."""
        result = self.extract(
            ExtractionRequest(
                job_id=request.job_id,
                subject_code=request.subject_code,
                edition_label=request.edition_label,
                subject_title=request.subject_title,
                cmp_document=request.cmp_document,
                syllabus_document=request.syllabus_document,
                provider=request.provider,
                persist=False,
                metadata=request.metadata,
            )
        )
        return result.validation
