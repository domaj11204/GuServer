def test_receive_chat(client):
    response = client.post(
        "/ffxiv/chat",
        json={"sender": "TestUser", "message": "Hello World", "chat_type": "Say"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "id" in data

def test_get_chat_logs(client):
    # First, create a chat log
    client.post(
        "/ffxiv/chat",
        json={"sender": "TestUser", "message": "Hello World", "chat_type": "Say"},
    )

    # Then, retrieve it
    response = client.get("/ffxiv/chat")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["sender"] == "TestUser"
    assert data[0]["message"] == "Hello World"
