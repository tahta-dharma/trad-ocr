# FastAPI Traditional OCR Service

A RESTful OCR service built with **FastAPI** using **traditional OCR techniques**.  
This project focuses on classical image preprocessing + OCR engines rather than end-to-end deep learning.

---
## ⚙️ Requirements
### Install Tesseract OCR
**macOS**
```bash
brew install tesseract
```

**Ubuntu / Debian**
```bash
sudo apt install tesseract-ocr
```

**Windows**
```bash
https://github.com/tesseract-ocr/tesseract
```

---
## ⚙️ Installation
### 1. Clone the repository
```bash
https://github.com/tahta-dharma/trad-ocr.git
```

### 2. Create virtual environment
```bash
python3 -m venv venv
```


### 3. Run virtual environtment
**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

### 5. Run FastAPI
```bash
uvicorn app.main:app --reload
```

then access to swagger ui
```bash
http://localhost:8000/docs
```

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