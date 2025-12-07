from pathlib import Path
from pypdf import PdfReader

from ..utils_chroma.config_chroma import RAW_PDF_DIR, PROCESSED_DIR
from ..utils_chroma.logging_utils_chroma import get_logger

logger = get_logger(__name__)

def list_pdfs():
    pdfs = sorted(RAW_PDF_DIR.glob("*.pdf"))
    if not pdfs:
        logger.warning(f"No PDFs found in: {RAW_PDF_DIR}")
    else:
        logger.info(f"Found {len(pdfs)} PDFs in raw_data/")
    return pdfs


def extract_text_from_pdf(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    text = "\n".join(pages)

    # save extracted text
    txt_path = PROCESSED_DIR / f"{pdf_path.stem}.txt"
    txt_path.write_text(text, encoding="utf-8")
    logger.info(f"Saved text → {txt_path}")

    return text
