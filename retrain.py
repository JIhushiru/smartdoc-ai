import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import os

def load_logged_data(log_path="logs/classifications.csv"):
    texts, labels = [], []
    if not os.path.exists(log_path):
        print("No logs to retrain on.")
        return texts, labels
    with open(log_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                texts.append(row[0])
                labels.append(row[1])
    return texts, labels

def retrain_and_save_model():
    texts, labels = load_logged_data()
    if not texts:
        print("No data to retrain.")
        return
    
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    clf = MultinomialNB()
    clf.fit(X,labels)

    os.makedirs("app/model", exist_ok=True)
    joblib.dump(clf, "app/model/classifier.pkl")
    joblib.dump(vectorizer, "app/model/vectorizer.pkl")
    print("Retrained model and saved.")

if __name__ == "__main__":
    retrain_and_save_model()
