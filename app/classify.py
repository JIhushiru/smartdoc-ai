import numpy as np
from app.utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity
import os
import joblib

EMBEDDING_STORE_PATH = "app/model/embedding_store.joblib"


def classify_text(text):
    # Generate embedding for new input
    new_embedding = np.array(get_embedding(text)).reshape(1, -1)

    # Load existing embeddings and labels
    if not os.path.exists(EMBEDDING_STORE_PATH):
        raise ValueError("Embedding store not found. Retrain model first.")

    data = joblib.load(EMBEDDING_STORE_PATH)
    existing_embeddings = np.array(data["embeddings"])
    labels = data["labels"]

    # Compute cosine similarity
    similarities = cosine_similarity(new_embedding, existing_embeddings)[0]
    best_idx = np.argmax(similarities)
    return labels[best_idx], float(similarities[best_idx])
