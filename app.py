from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
inventory = []

@app.route("/")
def home():
    return {"message": "Inventory API running"}

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(inventory)

@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            return jsonify(item)
    return {"error": "Not found"}, 404

@app.route("/items", methods=["POST"])
def add_item():
    data = request.json
    new_id = len(inventory) + 1
    item = {"id": new_id, "name": data["name"], "quantity": data["quantity"], "price": data["price"], "category": data["category"]}
    inventory.append(item)
    return jsonify(item), 201

@app.route("/items/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            item.update(request.json)
            return jsonify(item)
    return {"error": "Not found"}, 404

@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            return {"message": "Deleted"}
    return {"error": "Not found"}, 404

@app.route("/search/<name>", methods=["GET"])
def search_product(name):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {"search_terms": name, "json": 1}
    r = requests.get(url, params=params)

    if r.status_code == 200:
        try:
            return r.json()
        except Exception:
            return {"error": "Response was not JSON"}, 500
    else:
        return {"error": "Failed to reach OpenFoodFacts"}, r.status_code



if __name__ == "__main__":
    app.run(debug=True)
