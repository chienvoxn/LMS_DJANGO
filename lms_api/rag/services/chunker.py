import re
from dataclasses import dataclass

from .document_parser import ParsedUnit


@dataclass(frozen=True)
class TextChunk:
    content: str
    chunk_index: int
    page_number: int | None = None
    section_title: str = ""


def _split_long_text(text, size, overlap):
    parts = []
    start = 0
    text = text.strip()
    while start < len(text):
        end = min(start + size, len(text))
        if end < len(text):
            boundary = max(
                text.rfind(". ", start, end),
                text.rfind("\n", start, end),
                text.rfind(" ", start, end),
            )
            if boundary > start + size // 2:
                end = boundary + 1
        piece = text[start:end].strip()
        if piece:
            parts.append(piece)
        if end >= len(text):
            break
        next_start = max(end - overlap, start + 1)
        start = next_start
    return parts


def chunk_units(
    units: list[ParsedUnit],
    size: int = 1000,
    overlap: int = 180,
) -> list[TextChunk]:
    if size <= 0:
        raise ValueError("Chunk size phải lớn hơn 0.")
    if overlap < 0 or overlap >= size:
        raise ValueError("Overlap phải >= 0 và nhỏ hơn chunk size.")

    chunks = []
    chunk_index = 0

    for unit in units:
        paragraphs = [
            part.strip()
            for part in re.split(r"\n\s*\n|\n", unit.text)
            if part.strip()
        ]
        current = ""

        def emit(value):
            nonlocal chunk_index
            value = value.strip()
            if not value:
                return
            chunks.append(
                TextChunk(
                    content=value,
                    chunk_index=chunk_index,
                    page_number=unit.page_number,
                    section_title=unit.section_title,
                )
            )
            chunk_index += 1

        for paragraph in paragraphs:
            if len(paragraph) > size:
                if current:
                    emit(current)
                    current = ""
                for part in _split_long_text(paragraph, size, overlap):
                    emit(part)
                continue

            candidate = f"{current}\n{paragraph}".strip() if current else paragraph
            if len(candidate) <= size:
                current = candidate
                continue

            emit(current)
            prefix = current[-overlap:].strip() if overlap and current else ""
            current = f"{prefix}\n{paragraph}".strip() if prefix else paragraph
            if len(current) > size:
                pieces = _split_long_text(current, size, overlap)
                for part in pieces[:-1]:
                    emit(part)
                current = pieces[-1] if pieces else ""

        if current:
            emit(current)

    return chunks
