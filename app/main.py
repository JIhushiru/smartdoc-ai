from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import extract_text, log_classification
from app.classify import classify_text
from fastapi import Form
import os, csv
from retrain import rebuild_embedding_store

app = FastAPI()

ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
def verify_token(token: str = ""):
    if token != ADMIN_TOKEN:
        raise HTTPException(status_code=403, detail="Forbidden")

@app.post("/retrain")
def retrain_endpoint(token: str = Form(...)):
    verify_token(token)
    from retrain import rebuild_embedding_store
    rebuild_embedding_store()
    return {"message":"Embedding store updated from feedback."}

@app.post("/feedback")
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


@app.post("/classify/")
async def classify_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        text = extract_text(file.filename, contents)
        doc_type, confidence = classify_text(text)
        log_classification(text, doc_type, confidence)

        return {"document_type": doc_type, "confidence": confidence}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
