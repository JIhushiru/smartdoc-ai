# SmartDoc AI

SmartDoc AI is an AI-powered document classifier built with OpenAI embeddings, scikit-learn, and React. It classifies uploaded PDFs (e.g., resumes, invoices) into predefined categories and improves over time through user feedback and retraining.

---

## Features

- Upload PDF documents via a clean drag-and-drop interface
- Classifies document types using OpenAI embeddings + trained ML model
- Real-time confidence score with visual display
- Feedback system for correcting predictions
- Automatic retraining pipeline on feedback
- Cosine similarity fallback if no classifier is found
- Template keyword fallback for low-confidence predictions

---

## AI Architecture

### Model Flow

```text
PDF Upload
    ↓
Text Extraction
    ↓
OpenAI Embedding
    ↓
Classifier (scikit-learn)
    ↓
┌──────────────────────┐
│  Confidence > 0.7?   │──> Use model prediction
└───┬──────────────────┘
    ↓
Use template matching fallback
