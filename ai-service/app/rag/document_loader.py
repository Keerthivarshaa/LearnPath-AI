"""
Document Loader for LearnPath AI RAG.

Supports loading plain text from:

- PDF
- DOCX
- TXT

The extracted text is normalized before entering
the chunking stage.
"""

from pathlib import Path

import docx
from pypdf import PdfReader


class DocumentLoader:
    """
    Loads supported document types and extracts plain text.
    """

    SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}

    @classmethod
    def load(cls, file_path: str) -> tuple[str, str]:
        """
        Loads a document and returns:

        (document_name, extracted_text)
        """

        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"Document not found: {file_path}")

        extension = path.suffix.lower()

        if extension not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document type: {extension}"
            )

        if extension == ".pdf":
            text = cls._load_pdf(path)

        elif extension == ".docx":
            text = cls._load_docx(path)

        else:
            text = cls._load_txt(path)

        text = cls._normalize(text)

        return path.name, text

    @staticmethod
    def _load_pdf(path: Path) -> str:
        """
        Extract text from PDF.
        """

        reader = PdfReader(str(path))

        pages = []

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                pages.append(page_text)

        return "\n".join(pages)

    @staticmethod
    def _load_docx(path: Path) -> str:
        """
        Extract text from DOCX.
        """

        document = docx.Document(str(path))

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs)

    @staticmethod
    def _load_txt(path: Path) -> str:
        """
        Extract text from TXT.
        """

        return path.read_text(
            encoding="utf-8",
            errors="ignore",
        )

    @staticmethod
    def _normalize(text: str) -> str:
        """
        Normalize whitespace.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)