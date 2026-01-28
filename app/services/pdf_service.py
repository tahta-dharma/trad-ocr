from pdf2image import convert_from_bytes
from PIL import Image
from typing import List, Optional

def pdf_bytes_to_images(
  pdf_bytes: bytes, 
  dpi: int = 300, 
  max_pages: Optional[int] = None,
  debug: bool = True
) -> List[Image.Image]:
  """
  Convert PDF bytes to a list of PIL.Image objects.
  
  Args:
      pdf_bytes: Raw bytes of the PDF.
      dpi: Resolution for conversion (higher DPI = better OCR accuracy).
      max_pages: Limit number of pages converted.
      debug: If True, logs detailed info about each image.
  """
  
  images = convert_from_bytes(pdf_bytes, dpi=dpi)
  if max_pages is not None:
    images = images[:max_pages]

  if debug:
    print(f"[pdf_service] Converted PDF to {len(images)} image(s) at {dpi} DPI")
    for idx, img in enumerate(images, start=1):
      w, h = img.size
      mode = img.mode
      mem_est = (w * h * len(mode)) / (1024 * 1024)
      print(f"[pdf_service] Page {idx}: size={w}x{h}, mode={mode}, ~{mem_est:.2f} MB")
      
  return images