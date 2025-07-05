import numpy as np
from app.utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib

EMBEDDING_STORE_PATH = "app/model/embedding_store.joblib"
CLASSIFIER_PATH = "app/model/classifier.joblib"

def classify_text(text):
    embedding = np.array(get_embedding(text)).reshape(1, -1)

    if os.path.exists(CLASSIFIER_PATH):
        # Use trained classifier
        clf = joblib.load(CLASSIFIER_PATH)
        pred = clf.predict(embedding)[0]
        prob = max(clf.predict_proba(embedding)[0])
        return pred, float(prob)
    
    # Fallback to cosine similarity
    if not os.path.exists(EMBEDDING_STORE_PATH):
        raise ValueError("No classifier or embedding store found. Please retrain.")

    data = joblib.load(EMBEDDING_STORE_PATH)
    existing_embeddings = np.array(data["embeddings"])
    labels = data["labels"]

    similarities = cosine_similarity(embedding, existing_embeddings)[0]
    best_idx = np.argmax(similarities)
    return labels[best_idx], float(similarities[best_idx])
