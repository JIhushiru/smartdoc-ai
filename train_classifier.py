import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Sample training data
documents = [
    # Invoices
    "Invoice #123 from ACME Corp for $1,200 due on June 20.",
    "Billing statement for April. Total: $450. Thank you for your business.",
    "INVOICE: Net payment 30 days. Vendor: Xfinity. Total: $89.99",
    # Resumes
    "John Doe — Software Engineer with 5 years of Python experience",
    "Skills: Java, C++, SQL. Education: B.S. in Computer Science",
    "Work experience includes Microsoft, Google and Amazon.",
    # Receipts
    "Walmart Receipt — Item: Milk $3.49, Bread $2.99, Total: $6.48",
    "Thank you for shopping. Subtotal: $20.99, Tax: $1.67, Total: $22.66",
    "POS RECEIPT\nStore #: 404\nVisa ending in 1234",
    # Contracts
    "This Agreement is entered into on the 15th day of April...",
    "Party A agrees to deliver the goods no later than...",
    "This contract is governed by the laws of the State of California.",
    # Reports
    "Quarterly Report Q1 2023 — Revenue up 12% YoY",
    "Findings show increase in customer engagement by 25%",
    "Report generated using BI tools for internal audit team",
    # 5. Evaluate
]

labels = [
    "invoice",
    "invoice",
    "invoice",
    "resume",
    "resume",
    "resume",
    "receipt",
    "receipt",
    "receipt",
    "contract",
    "contract",
    "contract",
    "report",
    "report",
    "report",
]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    documents, labels, test_size=0.2, random_state=42
)

# Pipeline
pipeline = Pipeline(
    [
        ("vectorizer", TfidfVectorizer()),
        ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
    ]
)

# Train
pipeline.fit(X_train, y_train)

# Evaluate
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))
os.makedirs("models", exist_ok=True)

# Save the model and vectorizer
joblib.dump(pipeline.named_steps["classifier"], "models/classifier.pkl")
joblib.dump(pipeline.named_steps["vectorizer"], "models/vectorizer.pkl")

print("Model and vectorizer saved successfully.")
