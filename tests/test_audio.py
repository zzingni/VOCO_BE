# tests/test_audio.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stt():
    with open("tests/test.wav", "rb") as f:
        response = client.post(
            "/api/v1/audio/stt",
            files={"audio": ("test.wav", f, "audio/wav")}
        )

    assert response.status_code == 200
    assert "text" in response.json()