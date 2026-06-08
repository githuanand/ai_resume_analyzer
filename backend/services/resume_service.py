import os

from utils.pdf_reader import extract_text_from_pdf
from utils.docx_reader import extract_text_from_docx


class ResumeService:

    def extract_text(
        self,
        file_path: str
    ) -> str:

        ext = os.path.splitext(
            file_path
        )[1].lower()

        if ext == ".pdf":
            return extract_text_from_pdf(
                file_path
            )

        if ext == ".docx":
            return extract_text_from_docx(
                file_path
            )

        raise Exception(
            "Unsupported file format"
        )