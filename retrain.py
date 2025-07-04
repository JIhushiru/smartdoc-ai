from app.utils import get_embedding
import joblib, os
import numpy as np
import csv

EMBEDDING_STORE_PATH = "app/model/embedding_store.joblib"

def load_feedback(log_path="logs/feedback.csv"):
    texts, labels = [], []
    if not os.path.exists(log_path):
        return texts, labels
    with open(log_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                texts.append(row[0])
                labels.append(row[2])
    return texts, labels

def rebuild_embedding_store():
    texts, labels = load_feedback()
    if not texts:
        print("No feedback available.")
        return

    embeddings = [get_embedding(text) for text in texts]
    os.makedirs("app/model", exist_ok=True)
    joblib.dump({"embeddings": embeddings, "labels": labels}, EMBEDDING_STORE_PATH)
    print(f"Rebuilt embedding store from {len(texts)} feedback entries.")

if __name__ == "__main__":
    rebuild_embedding_store()
