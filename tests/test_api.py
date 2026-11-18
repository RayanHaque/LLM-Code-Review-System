import os
from fastapi.testclient import TestClient
from app.main import app

def test_code_review_and_history(tmp_path, monkeypatch):
    monkeypatch.setenv("REVIEW_DB_PATH", str(tmp_path / "test.db"))
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with TestClient(app) as client:
        assert client.get("/health").json() == {"status": "ok"}
        r = client.post("/api/reviews", json={"language": "Python", "code": "try:\n pass\nexcept:\n pass"})
        assert r.status_code == 200
        record = r.json()
        assert record["mode"] == "demo"
        assert client.get(f'/api/reviews/{record["id"]}').status_code == 200
        assert len(client.get("/api/reviews").json()) == 1
        assert client.get("/api/reviews/missing").status_code == 404

def test_validation(tmp_path, monkeypatch):
    monkeypatch.setenv("REVIEW_DB_PATH", str(tmp_path / "db.sqlite"))
    with TestClient(app) as client:
        assert client.post("/api/reviews", json={"language": "Python", "code": ""}).status_code == 422
