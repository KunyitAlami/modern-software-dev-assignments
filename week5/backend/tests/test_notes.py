def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["ok"] is True
    assert data["data"]["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    resp = r.json()

    assert resp["ok"] is True
    assert "items" in resp["data"]
    assert "total" in resp["data"]
    assert "page" in resp["data"]
    assert "page_size" in resp["data"]
    assert len(resp["data"]["items"]) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert items["ok"] is True
    assert len(items["data"]) >= 1


def test_create_note_title_too_short(client):
    payload = {"title": "Hi", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422
