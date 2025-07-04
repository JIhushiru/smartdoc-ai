import pdfplumber
import docx
import pytesseract
from PIL import Image
import io
import os
import csv
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = "azure"
openai.api_version = "2024-12-01-preview"
DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME")


def get_embedding(text: str) -> list:
    response = openai.embeddings.create(input=[text], model=DEPLOYMENT_NAME)
    return response.data[0].embedding


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
