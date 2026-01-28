import tesserocr
from PIL import Image
from typing import List, Dict, Optional

def extract_text_from_image(
    pil_img: Image.Image,
    lang: str = "eng",
    psm: int = 3,
    oem: int = 3,
    min_confidence: Optional[int] = None,
    raise_on_low_conf: bool = False,
    debug: bool = True
) -> str:
  """
  Run OCR on a single PIL image using Tesseract (via tesserocr).

  Args:
      pil_img: The PIL image to process.
      lang: Tesseract language code (default English).
      psm: Page segmentation mode (default 3 = auto).
      oem: OCR engine mode (default 3 = both legacy + LSTM).
      min_confidence: Minimum acceptable OCR confidence (0–100).
      raise_on_low_conf: If True, raise ValueError when below threshold.
      debug: Print debug information.

  Returns:
      Extracted plain text string.
  """
  try:
    with tesserocr.PyTessBaseAPI(path="/opt/homebrew/share/tessdata", lang=lang, psm=psm, oem=oem) as api:
      api.SetImage(pil_img)
      text = api.GetUTF8Text()
      conf = api.MeanTextConf()
    
    if debug:
      print(f"[ocr_service] OCR completed: conf={conf}, len={len(text)} chars")

    if min_confidence is not None and conf < min_confidence:
      msg = f"[ocr_service] Warning: Low OCR confidence ({conf} < {min_confidence})"

      if raise_on_low_conf:
        raise ValueError(msg)
      else:
        print(msg)

    return text.strip()
  except Exception as e:
    print(f"[ocr_service] OCR failed: {e}")
    raise

def extract_text_from_images(
    images: List[Image.Image],
    lang: str = "eng",
    min_confidence: Optional[int] = None,
    raise_on_low_conf: bool = False,
    debug: bool = True
) -> Dict[int, str]:
  """
  Run OCR on a list of images (multi-page PDF scenario).

  Returns:
      Dict mapping page index (1-based) to extracted text.
  """
  page_texts = {}

  for i, img in enumerate(images, start=1):
    if debug:
      print(f"[ocr_service] Processing page {i}/{len(images)}...")
    text = extract_text_from_image(
      img,
      lang=lang,
      min_confidence=min_confidence,
      raise_on_low_conf=raise_on_low_conf,
      debug=debug
    )
    page_texts[i] = text

  if debug:
    print(f"[ocr_service] Extracted text from {len(page_texts)} page(s).")

  return page_texts

def merge_page_texts(page_texts: Dict[int, str]) -> str:
  """
  Combine multi-page OCR results into one text blob.
  """
  combined = "\n\n".join(
    f"--- Page {i} ---\n{text.strip()}" for i, text in page_texts.items()
  )

  return combined