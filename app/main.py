from fastapi import FastAPI, UploadFile, File, HTTPException
from app.utils import extract_text, log_classification
from app.classify import classify_text

app = FastAPI()


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
