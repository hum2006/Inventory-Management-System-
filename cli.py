
import requests
import json

# Address of the Flask API running on your computer.
BASE_URL = "http://127.0.0.1:5000"


def main():
    # Keep showing the menu until the user chooses to exit.
    while True:
        print("\n1. View all items")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search OpenFoodFacts")
        print("7. Exit")

        # Get the user's menu choice.
        choice = input("Choose: ").strip()

        if choice == "1":
            # Request all inventory items from the API.
            try:
                items = requests.get(
                    f"{BASE_URL}/items", timeout=10
                ).json()
            except Exception as e:
                print({"error": str(e)})
                continue

            # Display the returned items in a readable format.
            if not items:
                print("[]")
            else:
                print("[")
                for i, item in enumerate(items):
                    print("  {")
                    print(f'    "id": {item["id"]},')
                    print(f'    "name": "{item["name"]}",')
                    print(f'    "quantity": {item["quantity"]},')
                    print(f'    "price": {item["price"]},')
                    print(f'    "category": "{item["category"]}"')
                    if i == len(items) - 1:
                        print("  }")
                    else:
                        print("  },")
                print("]")

        elif choice == "2":
            # Ask for an ID and request that specific item.
            item_id = input("Enter ID: ").strip()
            if not item_id:
                print("You must enter an ID.")
                continue
            try:
                r = requests.get(
                    f"{BASE_URL}/items/{item_id}", timeout=10
                )
                print(json.dumps(r.json(), indent=4))
            except Exception as e:
                print({"error": str(e)})

        elif choice == "3":
            # Collect details and send them to the API.
            try:
                name = input("Name: ").strip()
                qty = int(input("Quantity: ").strip())
                price = float(input("Price: ").strip())
                category = input("Category: ").strip()

                # Package the details as JSON data.
                data = {
                    "name": name,
                    "quantity": qty,
                    "price": price,
                    "category": category
                }

                r = requests.post(
                    f"{BASE_URL}/items", json=data, timeout=10
                )
                print(json.dumps(r.json(), indent=4))
            except ValueError:
                print({
                    "error": "Quantity must be integer and price must be number."
                })
            except Exception as e:
                print({"error": str(e)})

        elif choice == "4":
            # Ask which item should be updated.
            item_id = input("Enter ID: ").strip()
            if not item_id:
                print({"error": "You must enter an ID."})
                continue

            # Only include fields the user wants to change.
            data = {}
            qty = input("New Quantity (leave blank to skip): ").strip()
            price = input("New Price (leave blank to skip): ").strip()

            if qty:
                try:
                    data["quantity"] = int(qty)
                except ValueError:
                    print({"error": "Quantity must be integer."})
                    continue

            if price:
                try:
                    data["price"] = float(price)
                except ValueError:
                    print({"error": "Price must be number."})
                    continue

            # Send the selected changes using PATCH.
            try:
                r = requests.patch(
                    f"{BASE_URL}/items/{item_id}",
                    json=data,
                    timeout=10
                )
                print(json.dumps(r.json(), indent=4))
            except Exception as e:
                print({"error": str(e)})

        elif choice == "5":
            # Ask for the ID of the item to delete.
            item_id = input("Enter ID: ").strip()
            if not item_id:
                print({"error": "You must enter an ID."})
                continue
            try:
                # Send a DELETE request to the API.
                r = requests.delete(
                    f"{BASE_URL}/items/{item_id}", timeout=10
                )
                print(
                    json.dumps(r.json(), indent=4)
                    if r.text else {"message": "Deleted (no body)"}
                )
            except Exception as e:
                print({"error": str(e)})

        elif choice == "6":
            # Search OpenFoodFacts through the Flask API.
            name = input("Product name: ").strip()
            if not name:
                print({"error": "Product name required."})
                continue
            try:
                r = requests.get(
                    f"{BASE_URL}/search/{name}", timeout=10
                )
                print(json.dumps(r.json(), indent=4))
            except Exception as e:
                print({"error": str(e)})

        elif choice == "7":
            # End the program.
            break

        else:
            # Handle menu choices that are not listed.
            print("Invalid choice")


# Run the menu when this file is executed directly.
if __name__ == "__main__":
    main()