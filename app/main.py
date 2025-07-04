from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import extract_text, log_classification
from app.classify import classify_text
from fastapi import Form
import os, csv

app = FastAPI()


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
