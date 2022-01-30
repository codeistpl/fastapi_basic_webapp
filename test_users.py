from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_list_users():
    resp = client.get("/users")
    assert resp.status_code == 200
