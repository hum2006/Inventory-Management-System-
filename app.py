
from flask import Flask, request, jsonify
import json
import requests

# Create the Flask application.
app = Flask(__name__)

# Name of the file where inventory data is stored.
INVENTORY_FILE = "inventory.json"


# Read the saved items from the JSON file.
def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as file:
            return json.load(file)
    # Return an empty list if the file is missing or invalid.
    except (FileNotFoundError, json.JSONDecodeError):
        return []


# Save the current inventory to the JSON file.
def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as file:
        json.dump(inventory, file, indent=4)


# Find the next available ID for a new item.
def next_id(inventory):
    return max(
        (item.get("id", 0) for item in inventory),
        default=0
    ) + 1


# Check that the API is running.
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Inventory API running"
    }), 200


# Return all items in the inventory.
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(load_inventory()), 200


# Find and return one item using its ID.
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    inventory = load_inventory()

    # Check each item until the matching ID is found.
    for item in inventory:
        if item.get("id") == item_id:
            return jsonify(item), 200

    # Return an error if the ID does not exist.
    return jsonify({"error": "Item not found"}), 404


# Add a new item to the inventory.
@app.route("/items", methods=["POST"])
def create_item():
    # Read the item details sent by the client.
    data = request.get_json(silent=True)

    # Make sure the request contains a JSON object.
    if not isinstance(data, dict):
        return jsonify({"error": "Valid JSON body required"}), 400

    # Check that all required fields have been provided.
    for field in ("name", "quantity", "price", "category"):
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    inventory = load_inventory()

    # Create the item and assign it a unique ID.
    item = {
        "id": next_id(inventory),
        "name": data["name"],
        "quantity": data["quantity"],
        "price": data["price"],
        "category": data["category"]
    }

    # Add the new item and save the updated inventory.
    inventory.append(item)
    save_inventory(inventory)

    # Return the new item with a successful creation status.
    return jsonify(item), 201


# Update selected details of an existing item.
@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    # Read the fields the client wants to change.
    data = request.get_json(silent=True)

    # Reject an empty or invalid request body.
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Valid JSON body required"}), 400

    inventory = load_inventory()

    # Find the item that needs to be updated.
    for item in inventory:
        if item.get("id") == item_id:

            # Change only the fields included in the request.
            
            for field in ("name", "quantity", "price", "category"):
                if field in data:
                    if field == "quantity":
                        if type(data[field]) is not int or data[field] < 0:
                            return jsonify({
                                "error": "Quantity must be a non-negative integer"
                            }), 400

                    item[field] = data[field]

                    item[field] = data[field]

            # Save the changes and return the updated item.
            save_inventory(inventory)
            return jsonify(item), 200

    # Return an error if no matching item exists.
    return jsonify({"error": "Item not found"}), 404


# Remove an item from the inventory.
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    inventory = load_inventory()

    # Search for the item using its ID.
    for item in inventory:
        if item.get("id") == item_id:

            # Remove the item and save the remaining items.
            inventory.remove(item)
            save_inventory(inventory)

            return jsonify({"message": "Deleted"}), 200

    # Return an error if the item cannot be found.
    return jsonify({"error": "Item not found"}), 404


# Search OpenFoodFacts for products by name.
@app.route("/search/<path:name>", methods=["GET"])
def search_products(name):
    # Remove unnecessary spaces from the search term.
    name = name.strip()


    # Make sure the user entered a product name.
    if not name:
        return jsonify({
            "error": "Product name is required"
        }), 400


    # OpenFoodFacts endpoint used to search for products.
    url = "https://world.openfoodfacts.org/cgi/search.pl"

    # Set the search term and limit the results to five products.
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5
    }


    # Identify the application making the request.
    headers = {
        "User-Agent": "InventoryManagementSystem/1.0"
    }


    try:
        # Send the search request to OpenFoodFacts.
        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )


        # Raise an error if the server returns an unsuccessful status.
        response.raise_for_status()

        # Convert the response from JSON into Python data.
        data = response.json()

    # Handle connection problems and unsuccessful HTTP responses.
    except requests.RequestException:
        return jsonify({
            "error": "Could not connect to OpenFoodFacts"
        }), 502


    # Handle responses that cannot be decoded as JSON.
    except ValueError:
        return jsonify({
            "error": "OpenFoodFacts returned invalid JSON"
        }), 502

    products = []

    # Extract useful details from the returned products.
    for product in data.get("products", []):
        name = (
            product.get("product_name")
            or product.get("generic_name")
        )

        # Skip products that do not have a usable name.
        if name:
            products.append({
                "name": name,
                "brand": product.get("brands") or "",
                "category": product.get("categories") or "",
                "quantity": product.get("quantity") or ""
            })

    # Return an error if no usable products were found.
    if not products:
        return jsonify({
            "error": "No products found"
        }), 404

    # Return the matching products to the client.
    return jsonify(products), 200


# Start the development server when this file is run directly.
if __name__ == "__main__":
    app.run(debug=True)