import joblib 
from sklearn.feature_extraction.text import TfidfVectorizer

def classify_text(text: str) -> tuple[str, float]:
    model = joblib.load("models/classifier.pkl")
    vectorizer = joblib.load("models/vectorizer.pkl")
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X).max()
    return pred, float(prob)