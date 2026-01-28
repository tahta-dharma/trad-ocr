import io
import numpy as np
from PIL import Image, ImageOps
import cv2
import os

def pil_image_from_bytes(image_bytes: bytes) -> Image.Image:
  """
  Load an image from raw bytes into a PIL.Image (RGB).
  """
  try:
      img = Image.open(io.BytesIO(image_bytes))
      img = img.convert("RGB")
      print(f"[image_service] Loaded image: size={img.size}, mode={img.mode}")
      return img
  except Exception as e:
      print(f"[image_service] Failed to read image bytes: {e}")
      raise

def enchance_image_for_ocr(pil_img: Image.Image, debug: bool = True, debug_dir: str = "/tmp") -> Image.Image:
  """
  Enhance an image to improve OCR accuracy.
  Saves debug images if debug=True.

  Args:
      pil_img: The input PIL Image.
      debug: Whether to print and save intermediate results.
      debug_dir: Directory to save debug images (default /tmp).
  """
  if debug:
     print(f"[image_service] Starting enhancement for OCR. Input size={pil_img.size}")
     os.makedirs(debug_dir, exist_ok=True)

  # --- Step 1: Convert to OpenCV BGR array ---
  img = np.array(pil_img)
  img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

  # --- Step 2: Grayscale ---
  gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
  if debug:
     print(f"[image_service] Converted to grayscale. Shape={gray.shape}")

  # --- Step 3: Denoise ---
  denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

  # --- Step 4: Resize small images ---
  height, width = denoised.shape
  if height < 1000:
     scale = 1000 / height
     denoised = cv2.resize(denoised, (int(width * scale), 1000), interpolation=cv2.INTER_LINEAR)
     if debug:
        print(f"[image_service] Upscaled small image by {scale:.2f}x -> {denoised.shape[::-1]}")

  # --- Step 5: Adaptive threshold ---
  th = cv2.adaptiveThreshold(
     denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 12
  )

  # --- Step 6: Morphological cleanup ---
  kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
  cleaned = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
 
  # --- Step 7: Convert back to PIL and autocontrast ---
  enchanced_pil = Image.fromarray(cleaned)
  enchanced_pil = ImageOps.autocontrast(enchanced_pil)

  if debug:
     enhanced_path = os.path.join(debug_dir, "enhanced_image_debug.png")
     enchanced_pil.save(enhanced_path)
     print(f"[image_service] Saved enchanced image to {enhanced_path}")
     print(f"[image_service] Enhancement complete. Output size={enchanced_pil.size}")

  return enchanced_pil
