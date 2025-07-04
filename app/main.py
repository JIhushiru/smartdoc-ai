from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import extract_text, log_classification
from app.classify import classify_text
from fastapi import Form
import os
import csv
from retrain import rebuild_embedding_store
from fastapi.middleware.cors import CORSMiddleware

tags_metadata = [
    {
        "name": "Classification",
        "description": "Classify a document (PDF) into known types using embeddings.",
    },
    {
        "name": "Feedback",
        "description": "Submit corrections to improve the model.",
    },
    {
        "name": "Admin",
        "description": "Admin-only operations like retraining the model.",
    },
]


app = FastAPI(
    title="SmartDocAI API",
    description="Classify resumes, invoices, etc. using AI-powered embeddings.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_token(token: str = ""):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")


@app.post("/retrain/", tags=["Admin"])
def retrain_endpoint(token: str = Form(...)):
    verify_token(token)
    from retrain import rebuild_embedding_store

    rebuild_embedding_store()
    return {"message": "Embedding store updated from feedback."}


@app.post("/feedback", tags=["Feedback"])
async def submit_feedback(
    text: str = Form(...),
    predicted_label: str = Form(...),
    correct_label: str = Form(...),
):
    os.makedirs("logs", exist_ok=True)
    with open("logs/feedback.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([text[:200], predicted_label, correct_label])
    rebuild_embedding_store()
    return {"message": "Feedback saved. Thanks"}


@app.post("/classify/", tags=["Classification"])
async def classify_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text(file.filename, contents)
        doc_type, confidence = classify_text(text)
        log_classification(text, doc_type, confidence)

        return {"document_type": doc_type, "confidence": confidence}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
