"""PDF and DOCX file parsing."""

import io
import logging
from typing import BinaryIO, Union

import pdfplumber
from docx import Document

from app.exceptions import InvalidFileError
from app.utils.validators import validate_file_upload

logger = logging.getLogger(__name__)

FileLike = Union[BinaryIO, bytes]


def _to_bytes(file: FileLike) -> bytes:
    if isinstance(file, bytes):
        return file
    return file.read()


def parse_pdf(file: FileLike, filename: str = "upload.pdf") -> str:
    """Extract text from a PDF file.

    Args:
        file: File-like object or raw bytes.
        filename: Original filename for validation.

    Returns:
        Extracted plain text.

    Raises:
        InvalidFileError: If parsing fails or file is invalid.
    """
    data = _to_bytes(file)
    validate_file_upload(filename, len(data))
    try:
        text_parts: list[str] = []
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        text = "\n".join(text_parts).strip()
        if not text:
            raise InvalidFileError("No text could be extracted from PDF.")
        return text
    except InvalidFileError:
        raise
    except Exception as exc:
        logger.exception("PDF parsing failed")
        raise InvalidFileError(f"Failed to parse PDF: {exc}") from exc


def parse_docx(file: FileLike, filename: str = "upload.docx") -> str:
    """Extract text from a DOCX file.

    Args:
        file: File-like object or raw bytes.
        filename: Original filename for validation.

    Returns:
        Extracted plain text.

    Raises:
        InvalidFileError: If parsing fails or file is invalid.
    """
    data = _to_bytes(file)
    validate_file_upload(filename, len(data))
    try:
        document = Document(io.BytesIO(data))
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
        text = "\n".join(paragraphs).strip()
        if not text:
            raise InvalidFileError("No text could be extracted from DOCX.")
        return text
    except InvalidFileError:
        raise
    except Exception as exc:
        logger.exception("DOCX parsing failed")
        raise InvalidFileError(f"Failed to parse DOCX: {exc}") from exc


def parse_uploaded_file(
    file: FileLike,
    filename: str,
) -> str:
    """Parse uploaded file based on extension.

    Args:
        file: Uploaded file bytes or buffer.
        filename: Original filename.

    Returns:
        Extracted text content.
    """
    ext = "." + filename.rsplit(".", 1)[-1].lower()
    if ext == ".pdf":
        return parse_pdf(file, filename)
    if ext == ".docx":
        return parse_docx(file, filename)
    raise InvalidFileError("Only PDF and DOCX files are supported.")
