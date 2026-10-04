from flask import Flask, request, jsonify
import json
import requests

app = Flask(__name__)

INVENTORY_FILE = "inventory.json"


# Load inventory from JSON file
def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save inventory to JSON file
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


# Create item
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


# Update item
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


# Delete item
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


# Search OpenFoodFacts by product name
@app.route("/products/search", methods=["GET"])
def search_products():

    name = request.args.get("name")

    if not name:
        return jsonify({
            "error": "Product name is required"
        }), 400

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Could not search OpenFoodFacts"
            }), 500

        data = response.json()

        products = []

        for product in data.get("products", []):

            product_name = product.get("product_name")

            if product_name:
                products.append({
                    "name": product_name,
                    "brand": product.get("brands", "Unknown"),
                    "category": product.get(
                        "categories",
                        "Unknown"
                    ),
                    "quantity": product.get(
                        "quantity",
                        "Unknown"
                    )
                })

        return jsonify(products), 200

    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to OpenFoodFacts"
        }), 500


# Import product from OpenFoodFacts by name
@app.route("/products/import", methods=["POST"])
def import_product():

    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({
            "error": "Product name is required"
        }), 400

    name = data["name"]

    url = "https://world.openfoodfacts.org/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }

    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }

    try:
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Could not connect to OpenFoodFacts"
            }), 500

        data = response.json()

        products = data.get("products", [])

        # Remove products without names
        products = [
            product
            for product in products
            if product.get("product_name")
        ]

        if not products:
            return jsonify({
                "error": "Product not found"
            }), 404

        product = products[0]

        inventory = load_inventory()

        if inventory:
            new_id = max(
                item["id"] for item in inventory
            ) + 1
        else:
            new_id = 1

        new_item = {
            "id": new_id,
            "name": product.get(
                "product_name",
                "Unknown Product"
            ),
            "quantity": 1,
            "price": 0,
            "category": product.get(
                "categories",
                "Unknown"
            )
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