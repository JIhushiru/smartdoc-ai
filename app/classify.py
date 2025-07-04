import csv
import numpy as np
from app.utils import get_embedding
from sklearn.metrics.pairwise import cosine_similarity


def classify_text(text: str):
    query_vec = np.array(get_embedding(text)).reshape(1, -1)

    with open("data/embeddings.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    best_score = -1
    best_label = "unknown"

    for row in rows:
        doc_text, label, *vec_strs = row
        vec = np.array([float(v) for v in vec_strs]).reshape(1, -1)
        score = cosine_similarity(query_vec, vec)[0][0]
        if score > best_score:
            best_score = score
            best_label = label

    return best_label, float(best_score)
