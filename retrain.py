from sklearn.linear_model import LogisticRegression
from app.utils import get_embedding
import joblib
import os
import csv

EMBEDDING_STORE_PATH = "app/model/embedding_store.joblib"
CLASSIFIER_PATH = "app/model/classifier.joblib"


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

    # Train logistic regression classifier
    clf = LogisticRegression(max_iter=1000)
    clf.fit(embeddings, labels)
    joblib.dump(clf, CLASSIFIER_PATH)
    print(f"Rebuilt classifier from {len(texts)} feedback entries.")


if __name__ == "__main__":
    rebuild_embedding_store()
