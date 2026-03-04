def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["ok"] is True
    assert item["data"]["completed"] is False

    item_id = item["data"]["id"]

    r = client.put(f"/action-items/{item_id}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["ok"] is True
    assert done["data"]["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    resp = r.json()

    assert resp["ok"] is True
    assert "items" in resp["data"]
    assert "total" in resp["data"]
    assert "page" in resp["data"]
    assert "page_size" in resp["data"]
    assert len(resp["data"]["items"]) == 1


def test_list_action_items_pagination(client):
    # Create 3 items
    for i in range(3):
        client.post("/action-items/", json={"description": f"Task {i}"})

    # Default page returns all 3
    r = client.get("/action-items/")
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == 3

    # page_size=2 returns first 2
    r = client.get("/action-items/", params={"page_size": 2})
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["total"] == 3
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert len(data["items"]) == 2

    # page=2, page_size=2 returns last 1
    r = client.get("/action-items/", params={"page": 2, "page_size": 2})
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["total"] == 3
    assert data["page"] == 2
    assert data["page_size"] == 2
    assert len(data["items"]) == 1

    # page=3, page_size=2 returns empty
    r = client.get("/action-items/", params={"page": 3, "page_size": 2})
    assert r.status_code == 200
    data = r.json()["data"]
    assert data["total"] == 3
    assert len(data["items"]) == 0
