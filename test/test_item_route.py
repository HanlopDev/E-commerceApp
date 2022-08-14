import json

def test_create_item(client):
    data = {"title": "PC8", "description": "item nine"}
    response = client.post("/items", json.dumps(data))
    assert response.status_code == 200

def test_retrieve_item_by_id(client):
    response = client.get("/item/2")
    assert response.status_code == 200
    assert response.json()["title"] == "PC"
    


