"""Internal Alpha pipeline coordinator (FOS-003).

Orchestrates validation → ingest → classify → duplicates → aggregate → export.
No classification or aggregation business logic lives here.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.founder.internal_alpha.aggregators import WeeklyAggregator
from app.founder.internal_alpha.classifiers import RuleBasedClassifier
from app.founder.internal_alpha.classifiers.duplicate_detector import DuplicateDetector
from app.founder.internal_alpha.config import (
    InternalAlphaPipelineConfig,
    default_config,
)
from app.founder.internal_alpha.exporters import InternalAlphaExportBundle
from app.founder.internal_alpha.models import ClassifiedFeedback, PipelineResult
from app.founder.internal_alpha.processors import FeedbackProcessor
from app.founder.internal_alpha.validators import FeedbackFolderValidator


class InternalAlphaPipelineService:
    """Run the Version 1 Internal Alpha Processing Pipeline.

    Order:
    1. Discover week
    2. Validate
    3. Read files
    4. Classify
    5. Detect duplicates
    6. Aggregate
    7. Export
    8. Return PipelineResult
    """

    def __init__(
        self,
        config: InternalAlphaPipelineConfig | None = None,
        *,
        folder_validator: FeedbackFolderValidator | None = None,
        processor: FeedbackProcessor | None = None,
        classifier: RuleBasedClassifier | None = None,
        duplicate_detector: DuplicateDetector | None = None,
        aggregator: WeeklyAggregator | None = None,
        exporters: InternalAlphaExportBundle | None = None,
    ) -> None:
        self._config = config or default_config()
        self._folder_validator = folder_validator or FeedbackFolderValidator(
            self._config
        )
        self._processor = processor or FeedbackProcessor(self._config)
        self._classifier = classifier or RuleBasedClassifier(self._config)
        self._duplicate_detector = duplicate_detector or DuplicateDetector(
            self._config
        )
        self._aggregator = aggregator or WeeklyAggregator(self._config)
        self._exporters = exporters or InternalAlphaExportBundle(self._config)

    def run(
        self,
        week_dir: Path | str,
        *,
        week: str | None = None,
        generated_at: datetime | None = None,
        output_dir: Path | str | None = None,
    ) -> PipelineResult:
        """Execute the pipeline for one week folder.

        Args:
            week_dir: Path to the week directory.
            week: Optional week label (defaults to directory name).
            generated_at: Optional fixed timestamp for deterministic tests.
            output_dir: Optional export directory (defaults to ``processed/``).

        Returns:
            PipelineResult describing success, items, warnings, and outputs.
        """
        week_path = Path(week_dir)
        week_label = week if week is not None else week_path.name
        stamp = generated_at if generated_at is not None else datetime.now(tz=UTC)
        warnings: list[str] = []

        # 1–2 Discover + validate
        report = self._folder_validator.validate(week_path)
        if not report.ok:
            messages = tuple(f"{i.code}: {i.message}" for i in report.issues)
            return PipelineResult(
                success=False,
                processed_items=(),
                warnings=messages,
                output_files=(),
            )

        # 3 Read files
        items, read_warnings = self._processor.process(week_path, week=week_label)
        warnings.extend(read_warnings)
        if not items:
            warnings.append("no_items: No feedback items could be read")
            return PipelineResult(
                success=False,
                processed_items=(),
                warnings=tuple(warnings),
                output_files=(),
            )

        # 4 Classify
        classified = self._classifier.classify_many(items)

        # 5 Detect duplicates
        relations = self._duplicate_detector.detect(items)
        dup_map = {r.source_id: r.target_id for r in relations}
        processed: tuple[ClassifiedFeedback, ...] = tuple(
            ClassifiedFeedback(
                feedback_item=c.feedback_item,
                category=c.category,
                confidence=c.confidence,
                duplicate_of=dup_map.get(c.feedback_item.id),
            )
            for c in classified
        )

        # 6 Aggregate
        summary = self._aggregator.aggregate(
            processed,
            relations,
            week=week_label,
            generated_at=stamp,
        )

        # 7 Export
        export_root = (
            Path(output_dir)
            if output_dir is not None
            else week_path / self._config.processed_dirname
        )
        output_files = self._exporters.export_all(
            export_root,
            processed,
            summary,
            relations,
        )

        # 8 Result
        return PipelineResult(
            success=True,
            processed_items=processed,
            warnings=tuple(warnings),
            output_files=output_files,
        )
