# tests/test_audio.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stt_full_pipeline():
    with open("tests/test.wav", "rb") as f:
        response = client.post(
            "/api/v1/audio/stt",
            files={"file": ("test.wav", f, "audio/wav")}
        )

    data = response.json()

    assert response.status_code == 200
    assert "text" in data
    assert "analysis" in data
    assert "feedback" in data

    print(response.json())