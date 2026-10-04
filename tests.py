import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Test home route
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200

    data = response.get_json()

    assert data["message"] == "Inventory Management API"
    assert data["status"] == "running"


# Test getting all items
def test_get_items(client):
    response = client.get("/items")

    assert response.status_code == 200

    data = response.get_json()

    assert isinstance(data, list)


# Test getting one item
def test_get_item(client):
    response = client.get("/items/1")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == 1
    assert data["name"] == "Milk"


# Test item not found
def test_item_not_found(client):
    response = client.get("/items/9999")

    assert response.status_code == 404


# Test creating an item
def test_create_item(client):
    item = {
        "name": "Juice",
        "quantity": 10,
        "price": 100,
        "category": "Drinks"
    }

    response = client.post("/items", json=item)

    assert response.status_code == 201

    data = response.get_json()

    assert data["name"] == "Juice"
    assert data["quantity"] == 10
    assert data["price"] == 100
    assert data["category"] == "Drinks"


# Test creating an item with missing data
def test_create_item_missing_field(client):
    item = {
        "name": "Juice",
        "quantity": 10
    }

    response = client.post("/items", json=item)

    assert response.status_code == 400


# Test updating an item
def test_update_item(client):
    response = client.patch(
        "/items/1",
        json={"quantity": 50}
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["quantity"] == 50


# Test updating an item that does not exist
def test_update_missing_item(client):
    response = client.patch(
        "/items/9999",
        json={"quantity": 10}
    )

    assert response.status_code == 404


# Test deleting an item
def test_delete_item(client):
    # First create a temporary item
    response = client.post(
        "/items",
        json={
            "name": "Temporary Item",
            "quantity": 5,
            "price": 20,
            "category": "Test"
        }
    )

    assert response.status_code == 201

    item_id = response.get_json()["id"]

    # Delete the temporary item
    response = client.delete(f"/items/{item_id}")

    assert response.status_code == 200


# Test deleting an item that does not exist
def test_delete_missing_item(client):
    response = client.delete("/items/9999")

    assert response.status_code == 404


# Test OpenFoodFacts product search
def test_product_lookup(client, monkeypatch):

    class FakeResponse:

        status_code = 200

        def json(self):
            return {
                "status": 1,
                "product": {
                    "product_name": "Test Milk",
                    "brands": "Test Brand",
                    "categories": "Dairy",
                    "quantity": "500 ml",
                    "image_url": "test.jpg"
                }
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/products/123456789")

    assert response.status_code == 200

    data = response.get_json()

    assert data["name"] == "Test Milk"
    assert data["brand"] == "Test Brand"
    assert data["category"] == "Dairy"


# Test OpenFoodFacts product not found
def test_product_not_found(client, monkeypatch):

    class FakeResponse:

        status_code = 200

        def json(self):
            return {
                "status": 0
            }

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr("app.requests.get", fake_get)

    response = client.get("/products/123456789")

    assert response.status_code == 404