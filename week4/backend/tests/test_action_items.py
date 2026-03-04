def test_create_and_complete_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1

def test_get_completed_action_items(client):
    # Create two action items (both start as completed=False)
    r1 = client.post("/action-items/", json={"description": "Task 1"})
    r2 = client.post("/action-items/", json={"description": "Task 2"})

    assert r1.status_code == 201
    assert r2.status_code == 201

    item1 = r1.json()
    item2 = r2.json()

    # Complete only the second item
    r_complete = client.put(f"/action-items/{item2['id']}/complete")
    assert r_complete.status_code == 200
    assert r_complete.json()["completed"] is True

    # Call the completed endpoint
    response = client.get("/action-items/completed")
    assert response.status_code == 200

    data = response.json()

    # Only one completed item should be returned
    assert len(data) == 1
    assert data[0]["description"] == "Task 2"
    assert data[0]["completed"] is True