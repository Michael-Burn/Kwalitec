"""pypdf-based deterministic PDF extractor (no OCR / LLM)."""

from __future__ import annotations

import logging
import re
from uuid import uuid4

from app.application.curriculum_intelligence.exceptions import ExtractionError
from app.application.curriculum_intelligence.ports.pdf_extraction_port import (
    PdfExtractionPort,
)
from app.domain.curriculum_intelligence.extracted_document import (
    BlockKind,
    ExtractedBlock,
    ExtractedDocument,
    ExtractedPage,
)

logger = logging.getLogger(__name__)

_HEADING_LINE = re.compile(r"^[A-Z0-9][A-Z0-9 \-/,:]{2,80}$")
_LIST_LINE = re.compile(r"^(?:[-*•]|\d+[.)])\s+\S")
_TABLE_LINE = re.compile(r".+\|.+\|")


class PyPdfExtractionAdapter(PdfExtractionPort):
    """Extract text, headings, list items, and simple tables via pypdf."""

    def extract(
        self,
        pdf_bytes: bytes,
        *,
        extraction_id: str,
        document_id: int,
    ) -> ExtractedDocument:
        try:
            from pypdf import PdfReader
        except ImportError as exc:  # pragma: no cover
            raise ExtractionError(
                "pypdf is required for deterministic PDF extraction.",
                code="missing_pypdf",
            ) from exc

        try:
            from io import BytesIO

            reader = PdfReader(BytesIO(pdf_bytes), strict=False)
        except Exception as exc:  # noqa: BLE001
            raise ExtractionError(
                f"Unable to open PDF: {exc}",
                code="pdf_unreadable",
            ) from exc

        meta_pairs: list[tuple[str, str]] = []
        meta = reader.metadata
        if meta is not None:
            for key in ("/Title", "/Author", "/Subject", "/Creator", "/Producer"):
                value = meta.get(key) if hasattr(meta, "get") else None
                if value:
                    meta_pairs.append((key.lstrip("/").lower(), str(value)))
        meta_pairs.append(("page_count", str(len(reader.pages))))

        pages: list[ExtractedPage] = []
        diagnostics: list[str] = []
        for index, page in enumerate(reader.pages, start=1):
            try:
                raw = page.extract_text() or ""
            except Exception as exc:  # noqa: BLE001
                diagnostics.append(f"page {index} text extraction warning: {exc}")
                raw = ""
            width = None
            height = None
            try:
                box = page.mediabox
                width = float(box.width)
                height = float(box.height)
            except Exception:  # noqa: BLE001
                pass

            blocks = self._blocks_from_text(raw, page_number=index)
            # Image placeholders (count only — no OCR)
            try:
                resources = page.get("/Resources")
                if resources is not None:
                    xobject = (
                        resources.get("/XObject") if hasattr(resources, "get") else None
                    )
                    if xobject is not None:
                        for name in xobject:
                            blocks.append(
                                ExtractedBlock(
                                    block_id=f"blk-{uuid4().hex[:10]}",
                                    kind=BlockKind.IMAGE,
                                    text=f"[image:{name}]",
                                    order_index=len(blocks),
                                    attributes=(("xobject", str(name)),),
                                )
                            )
            except Exception:  # noqa: BLE001
                diagnostics.append(f"page {index}: image inventory unavailable")

            pages.append(
                ExtractedPage(
                    page_number=index,
                    width=width,
                    height=height,
                    blocks=tuple(blocks),
                    raw_text=raw,
                )
            )

        if not pages:
            raise ExtractionError("PDF contains no pages.", code="no_pages")

        return ExtractedDocument(
            extraction_id=extraction_id,
            document_id=document_id,
            page_count=len(pages),
            pages=tuple(pages),
            metadata=tuple(meta_pairs),
            diagnostics=tuple(diagnostics),
        )

    def _blocks_from_text(self, raw: str, *, page_number: int) -> list[ExtractedBlock]:
        _ = page_number
        blocks: list[ExtractedBlock] = []
        paragraphs = re.split(r"\n\s*\n", raw or "")
        order = 0
        for para in paragraphs:
            text = para.strip()
            if not text:
                continue
            lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
            if not lines:
                continue
            # Table heuristic: multiple pipe-separated lines
            if len(lines) >= 2 and sum(1 for ln in lines if _TABLE_LINE.match(ln)) >= 2:
                blocks.append(
                    ExtractedBlock(
                        block_id=f"blk-{uuid4().hex[:10]}",
                        kind=BlockKind.TABLE,
                        text="\n".join(lines),
                        order_index=order,
                    )
                )
                order += 1
                continue
            for line in lines:
                kind = BlockKind.PARAGRAPH
                if _LIST_LINE.match(line):
                    kind = BlockKind.LIST_ITEM
                elif _HEADING_LINE.match(line) and len(line.split()) <= 12:
                    kind = BlockKind.HEADING
                elif len(lines) == 1 and len(line) < 90 and not line.endswith("."):
                    # Single short line — possible heading
                    if line[:1].isupper():
                        kind = BlockKind.HEADING
                blocks.append(
                    ExtractedBlock(
                        block_id=f"blk-{uuid4().hex[:10]}",
                        kind=kind,
                        text=line,
                        order_index=order,
                    )
                )
                order += 1
        if not blocks and (raw or "").strip():
            blocks.append(
                ExtractedBlock(
                    block_id=f"blk-{uuid4().hex[:10]}",
                    kind=BlockKind.PARAGRAPH,
                    text=raw.strip(),
                    order_index=0,
                )
            )
        return blocks
