from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_classify_pdf():
    with open("tests/test_files/sample.pdf", "rb") as f:
        response = client.post("/classify/", files={"file": ("sample.pdf", f, "application/pdf")})
    assert response.status_code == 200
    data = response.json()
    assert "document_type" in data
    assert "confidence" in data
    assert isinstance(data["document_type"], str)
    assert isinstance(data["confidence"], float)