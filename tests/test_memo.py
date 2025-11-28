def test_create_task(client):
    response = client.post(
        "/memo/tasks",
        json={"title": "Test Task", "status": "todo", "attributes": {"priority": "high"}},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["status"] == "todo"
    assert data["attributes"]["priority"] == "high"

def test_read_tasks(client):
    client.post(
        "/memo/tasks",
        json={"title": "Task 1", "status": "todo"},
    )
    client.post(
        "/memo/tasks",
        json={"title": "Task 2", "status": "in_progress"},
    )

    response = client.get("/memo/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2

    # Test filtering
    response = client.get("/memo/tasks?status=in_progress")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Task 2"

def test_update_task(client):
    # Create
    create_res = client.post(
        "/memo/tasks",
        json={"title": "Old Title", "status": "todo"},
    )
    task_id = create_res.json()["id"]

    # Update
    response = client.patch(
        f"/memo/tasks/{task_id}",
        json={"title": "New Title", "status": "done"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["status"] == "done"

def test_get_context(client):
    client.post(
        "/memo/tasks",
        json={"title": "Active Task", "status": "in_progress"},
    )
    
    response = client.get("/memo/context")
    assert response.status_code == 200
    data = response.json()
    assert "markdown" in data
    assert "Active Task" in data["markdown"]
