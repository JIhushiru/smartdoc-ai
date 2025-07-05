from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import extract_text, log_classification
from app.classify import classify_text
from fastapi import Form
import os
import csv
from retrain import rebuild_embedding_store
from fastapi.middleware.cors import CORSMiddleware
import hashlib
import datetime

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


def hash_text(text: str) -> str:
    return hashlib.sha256(text[:200].encode("utf-8")).hexdigest()


def feedback_hash_exists(new_hash: str, log_path="logs/feedback.csv") -> bool:
    if not os.path.exists(log_path):
        return False
    with open(log_path, "r", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) == 4 and row[3] == new_hash:
                return True
    return False

def get_feedback_stats(log_path="logs/feedback.csv"):
    if not os.path.exists(log_path):
        return {"count": 0, "last_entry":None}
    with open(log_path, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
        count = len(rows)
        last_time = os.path.getmtime(log_path)
        return {
            "count": count,
            "last_entry": datetime.datetime.fromtimestamp(last_time).isoformat()
        }

@app.get("/status", tags=["Admin"])
def status_endpoint(token: str = ""):
    verify_token(token)
    stats = get_feedback_stats()
    return {"message": "Model status", **stats}


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
    text_hash = hashlib.sha256(text[:200].encode("utf-8")).hexdigest()

    if feedback_hash_exists(text_hash):
        raise HTTPException(status_code=400, detail="Duplicate feedback detected.")

    with open("logs/feedback.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([text[:200], predicted_label, correct_label, text_hash])

    # Auto retrain if classifier is missing
    if not os.path.exists("app/model/classifier.joblib"):
        print("Classifier not found. Triggering retrain...")
        rebuild_embedding_store()

    return {"message": "Feedback saved. Thanks"}


@app.post("/classify/", tags=["Classification"])
async def classify_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text(file.filename, contents)
        doc_type, confidence = classify_text(text)
        log_classification(text, doc_type, confidence)

        return {"document_type": doc_type, "confidence": confidence, "text": text}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
