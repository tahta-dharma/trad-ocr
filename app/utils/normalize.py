import re

def normalize_ocr_text(text: str) -> str:
  """
  Lightly clean OCR text for better AI model input.
  Does NOT try to parse sections or extract meaning.
  """
  # Remove common page markers
  text = re.sub(r"-{2,}\s*Page\s*\d+\s*-{2,}", "", text)

  # Normalize bullet points (•, *, =)
  text = re.sub(r"[•*=]\s*", "\n- ", text)

  # Replace multiple newlines with just two
  text = re.sub(r"\n{3,}", "\n\n", text)

  # Remove trailing spaces and weird spacing
  text = re.sub(r"[ \t]+", " ", text).strip()

  return text