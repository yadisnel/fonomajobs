from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root_info():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"1": "Please check the documentation at v1/docs."}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "ok."}
