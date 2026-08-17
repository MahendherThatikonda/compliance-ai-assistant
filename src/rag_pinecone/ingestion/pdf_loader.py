import os
from pypdf import PdfReader
from ..config import PDF_FOLDER
from ..utils.logging_utils import get_logger

logger = get_logger(__name__)

def list_pdfs():
    files = [os.path.join(PDF_FOLDER,f) for f in os.listdir(PDF_FOLDER) if f.endswith(".pdf")]
    logger.info(f"Found {len(files)} PDFs")
    return files

def extract_text_from_pdf(path):
    logger.info(f"Reading {path}")
    text = ""
    reader = PdfReader(path)

    # 🚨 If encrypted, try to decrypt
    if reader.is_encrypted:
        try:
            reader.decrypt("")   # Try opening with no password
        except:
            logger.error(f"PDF is encrypted and requires password: {path}")
            return ""            # Skip or handle manually

    for page in reader.pages:
        t = page.extract_text() or ""
        text += t

    return text
