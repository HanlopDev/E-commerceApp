import json
from config import setting


def test_create_item(client, header_token):
    data = {"title": setting.TEST_ITEM, "description": setting.TEST_ITEM_DESC}
    response = client.post("/items", json.dumps(data), headers=header_token)
    assert response.status_code == 200


def test_retrieve_item_by_id(client):
    response = client.get("/item/1")
    assert response.status_code == 200
    assert response.json()["title"] == setting.TEST_ITEM
