import joblib

store = joblib.load("app/model/embedding_store.joblib")
print(store["labels"][:5])
