import pytest
from app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200

def test_add_item(client):
    r = client.post("/items", json={"name":"Juice","quantity":5,"price":50,"category":"Drinks"})
    assert r.status_code == 201
    assert r.get_json()["name"] == "Juice"

def test_get_items(client):
    r = client.get("/items")
    assert r.status_code == 200
    assert isinstance(r.get_json(), list)

def test_update_item(client):
    client.post("/items", json={"name":"Sugar","quantity":10,"price":100,"category":"Groceries"})
    r = client.patch("/items/1", json={"quantity":30})
    assert r.status_code == 200

def test_delete_item(client):
    client.post("/items", json={"name":"Tea","quantity":5,"price":40,"category":"Beverages"})
    r = client.delete("/items/1")
    assert r.status_code == 200
