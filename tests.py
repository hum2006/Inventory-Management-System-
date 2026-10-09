
import pytest
import app as inventory_app


# Create a test client and a separate inventory file for each test.
@pytest.fixture
def client(tmp_path, monkeypatch):
    file = tmp_path / "inventory.json"

    # Start each test with an empty inventory.
    file.write_text("[]")

    # Use the temporary file instead of the real inventory file.
    monkeypatch.setattr(
        inventory_app, "INVENTORY_FILE", str(file)
    )

    # Allow requests to be made directly to the Flask application.
    return inventory_app.app.test_client()


# Check that the API returns all items successfully.
def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    assert response.get_json() == []


# Check that a new item can be added.
def test_add_item(client):
    item = {
        "name": "Milk",
        "quantity": 10,
        "price": 80,
        "category": "Dairy"
    }

    response = client.post("/items", json=item)
    assert response.status_code in (200, 201)


# Check that an item's quantity can be changed.
def test_update_item(client):
    item = {
        "name": "Bread",
        "quantity": 5,
        "price": 60,
        "category": "Bakery"
    }

    # Add an item before attempting to update it.
    client.post("/items", json=item)

    response = client.patch(
        "/items/1", json={"quantity": 10}
    )
    assert response.status_code == 200


# Check that an item can be deleted.
def test_delete_item(client):
    item = {
        "name": "Sugar",
        "quantity": 4,
        "price": 150,
        "category": "Groceries"
    }

    # Add an item so there is something to delete.
    client.post("/items", json=item)

    response = client.delete("/items/1")
    assert response.status_code == 200