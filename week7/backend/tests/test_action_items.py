def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_create_action_item_with_note(client):
    # create a note first
    note_response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "Content"},
    )
    assert note_response.status_code == 201
    note_id = note_response.json()["id"]

    # create action item linked to note
    response = client.post(
        "/action-items/",
        json={"description": "Linked task", "note_id": note_id},
    )
    assert response.status_code == 201
    data = response.json()

    assert data["note_id"] == note_id
    assert data["description"] == "Linked task"