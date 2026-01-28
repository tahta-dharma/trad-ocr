from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.pdf_service import pdf_bytes_to_images
from app.services.image_service import pil_image_from_bytes, enchance_image_for_ocr
from app.services.ocr_service import extract_text_from_images, extract_text_from_image, merge_page_texts
from app.utils.normalize import normalize_ocr_text
from typing import Optional
import mimetypes

app = FastAPI(title="Document OCR Service", version="0.1.0")

@app.get("/health")
def health_check():
  return { "status": "OK" }

@app.post("/extract-text")
async def extract_text_endpoint(
  file: UploadFile = File(...),
  lang: str = Form("eng"),
  min_confidence: Optional[int] = Form(None),
  debug: bool = Form(True)
):
  """
  Upload a PDF or image and extract text using OCR.
  """
  try:
    file_bytes = await file.read()
    mime_type, _ = mimetypes.guess_type(file.filename or "")
    filename = file.filename or "unknown"
    print(f"[main] Received file: {filename}, mime={mime_type}")

    # Step 1. Detect file type
    if filename.lower().endswith(".pdf") or mime_type == "application/pdf":
      images = pdf_bytes_to_images(file_bytes, dpi=300, debug=debug)
    else:
      img = pil_image_from_bytes(file_bytes)
      images = [img]

    # Step 2: Enchance each image for OCR
    enhanced_images = [enchance_image_for_ocr(img, debug=debug) for img in images]

    # Step 3: Run OCR
    page_texts = extract_text_from_images(
      enhanced_images,
      lang=lang,
      min_confidence=min_confidence,
      debug=debug
    )

    combined_text = merge_page_texts(page_texts)

    normalized_text = normalize_ocr_text(combined_text)

    return JSONResponse({
      "filename": filename,
      "pages": len(page_texts),
      "lang": lang,
      "text_preview": normalized_text[:500],
      "text": {
        "raw": combined_text,
        "normalized": normalized_text
      }
    })
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))