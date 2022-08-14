import json

def test_create_user(client):
    data = {"email": "testuser10@gmail.com", "password": "testuser7"}
    response = client.post("/users", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testuser10@gmail.com"
    assert response.json()["is_active"] == True


