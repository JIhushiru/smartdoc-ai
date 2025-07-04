import pdfplumber
import docx
import pytesseract
from PIL import Image
import io
import os
import csv


def extract_text(filename: str, content: bytes) -> str:
    if filename.endswith(".pdf"):
        return extract_pdf_text(content)
    elif filename.endswith(".docx"):
        return extract_docx_text(content)
    elif filename.endswith((".jpg", ".jpeg", ".png")):
        return extract_image_text(content)
    else:
        raise ValueError("Unsupported file type")


def extract_pdf_text(content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])


def extract_docx_text(content: bytes) -> str:
    file_stream = io.BytesIO(content)
    doc = docx.Document(file_stream)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_image_text(content: bytes) -> str:
    image = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(image)


def log_classification(text: str, label: str, confidence: float):
    os.makedirs("logs", exist_ok=True)
    log_path = "logs/classifications.csv"
    with open(log_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([text[:200], label, confidence])
