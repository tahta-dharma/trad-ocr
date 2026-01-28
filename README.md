# FastAPI Traditional OCR Service

A RESTful OCR service built with **FastAPI** using **traditional OCR techniques**.  
This project focuses on classical image preprocessing + OCR engines rather than end-to-end deep learning.

---
## ⚙️ Requirements
### Install Tesseract OCR
macOS
brew install tesseract

Ubuntu / Debian
sudo apt install tesseract-ocr

Windows
https://github.com/tesseract-ocr/tesseract

---
## ⚙️ Installation
### 1. Clone the repository
https://github.com/tahta-dharma/trad-ocr.git

### 2. Create virtual environment
python3 -m venv venv


### 3. Run virtual environtment
macOS / Linux
source venv/bin/activate

Windows
venv\Scripts\activate

### 4. Install dependencies
pip install -r requirements.txt

### 5. Run FastAPI
uvicorn app.main:app --reload

then access to swagger ui /docs

---

## 🛠 Tech Stack

- **Python 3.x**
- **FastAPI**
- **Uvicorn**
- **Tesseract OCR**

---

## 📋 TO DO
- Image processing ✅
- OCR ✅
- Extract structured information using AI Model 🔛