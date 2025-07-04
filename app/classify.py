import joblib 
from sklearn.feature_extraction.text import TfidfVectorizer

model = joblib.load("models/classifier.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

def classify_text(text: str) -> tuple[str, float]:
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()
    return pred, float(prob)