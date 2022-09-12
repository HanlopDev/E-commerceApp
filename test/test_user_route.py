import json
from config import setting


def test_create_user(client):
    data = {"email": "userme@example.com", "password": "userme"}
    response = client.post("/users", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "userme@example.com"
    assert response.json()["is_active"] == True
