import pymupdf
from fastapi import HTTPException, UploadFile

from app.core.config import settings


async def extract_pdf_text(file: UploadFile) -> tuple[str, str]:
    filename = file.filename or "resume.pdf"
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(415, "Only PDF resumes are supported.")
    data = await file.read()
    if not data:
        raise HTTPException(400, "Uploaded file is empty.")
    if len(data) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb} MB.")
    if not data.startswith(b"%PDF-"):
        raise HTTPException(415, "Invalid PDF signature.")
    try:
        doc = pymupdf.open(stream=data, filetype="pdf")
        if doc.page_count > settings.max_pdf_pages:
            raise HTTPException(413, f"PDF exceeds {settings.max_pdf_pages} pages.")
        pages = []
        for page in doc:
            page_text = page.get_text("text")
            if isinstance(page_text, str):
                pages.append(page_text)
        text = "\n".join(pages).strip()
        doc.close()
    except HTTPException:
        raise
    except pymupdf.FileDataError:
        raise HTTPException(400, "Could not parse this PDF.")
    if len(text) < 80:
        raise HTTPException(
            422, "No usable text found. Scanned PDF/OCR support is not included yet."
        )
    return filename, text
