from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

INVENTORY_FILE = "inventory.json"


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Inventory Management API",
        "status": "running"
    })


# Get all items
@app.route("/items", methods=["GET"])
def get_items():
    inventory = load_inventory()
    return jsonify(inventory), 200


# Get one item
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    inventory = load_inventory()

    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404


# Add a new item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    required_fields = ["name", "quantity", "price", "category"]

    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400

    inventory = load_inventory()

    if inventory:
        new_id = max(item["id"] for item in inventory) + 1
    else:
        new_id = 1

    new_item = {
        "id": new_id,
        "name": data["name"],
        "quantity": data["quantity"],
        "price": data["price"],
        "category": data["category"]
    }

    inventory.append(new_item)
    save_inventory(inventory)

    return jsonify(new_item), 201


# Update an item
@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    inventory = load_inventory()

    for item in inventory:
        if item["id"] == item_id:

            if "name" in data:
                item["name"] = data["name"]

            if "quantity" in data:
                item["quantity"] = data["quantity"]

            if "price" in data:
                item["price"] = data["price"]

            if "category" in data:
                item["category"] = data["category"]

            save_inventory(inventory)

            return jsonify(item), 200

    return jsonify({"error": "Item not found"}), 404


# Delete an item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    inventory = load_inventory()

    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            save_inventory(inventory)

            return jsonify({
                "message": "Item deleted successfully"
            }), 200

    return jsonify({"error": "Item not found"}), 404


# Search for a product using OpenFoodFacts
@app.route("/products/<barcode>", methods=["GET"])
def get_product(barcode):

    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Product could not be found"
            }), 404

        data = response.json()

        if data.get("status") != 1:
            return jsonify({
                "error": "Product not found"
            }), 404

        product = data.get("product", {})

        return jsonify({
            "barcode": barcode,
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "category": product.get("categories", "Unknown"),
            "quantity": product.get("quantity", "Unknown"),
            "image": product.get("image_url")
        }), 200

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to OpenFoodFacts"
        }), 500


# Import a product from OpenFoodFacts into inventory
@app.route("/products/import/<barcode>", methods=["POST"])
def import_product(barcode):

    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Product could not be found"
            }), 404

        data = response.json()

        if data.get("status") != 1:
            return jsonify({
                "error": "Product not found"
            }), 404

        product = data.get("product", {})

        inventory = load_inventory()

        if inventory:
            new_id = max(item["id"] for item in inventory) + 1
        else:
            new_id = 1

        new_item = {
            "id": new_id,
            "name": product.get("product_name", "Unknown Product"),
            "quantity": 1,
            "price": 0,
            "category": product.get("categories", "Unknown")
        }

        inventory.append(new_item)
        save_inventory(inventory)

        return jsonify({
            "message": "Product imported successfully",
            "item": new_item
        }), 201

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to OpenFoodFacts"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)