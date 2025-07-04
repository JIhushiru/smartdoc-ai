import csv
import os
from app.utils import get_embedding

os.makedirs("data", exist_ok=True)

feedback_path = "logs/feedback.csv"
output_path = "data/embeddings.csv"

if not os.path.exists(feedback_path):
    print("No feedback found.")
    exit()

with open(feedback_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    rows = list(reader)

with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for text, _, correct_label in rows:
        vec = get_embedding(text)
        writer.writerow([text, correct_label] + vec)

print(f"Rebuilt embedding store from {len(rows)} feedback entries.")
