import requests

BASE_URL = "http://127.0.0.1:5000"

def main():
    while True:
        print("\n1. View all items")
        print("2. View one item")
        print("3. Add item")
        print("4. Update item")
        print("5. Delete item")
        print("6. Search OpenFoodFacts")
        print("7. Exit")

        choice = input("Choose: ")

        if choice == "1":
            items = requests.get(f"{BASE_URL}/items").json()
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
            item_id = input("Enter ID: ").strip()
            if not item_id:
                print("You must enter an ID.")
                continue

            try:
                response = requests.get(f"{BASE_URL}/items/{item_id}")
                if response.status_code == 200:
                    item = response.json()
                    print("{")
                    print(f'  "id": {item["id"]},')
                    print(f'  "name": "{item["name"]}",')
                    print(f'  "quantity": {item["quantity"]},')
                    print(f'  "price": {item["price"]},')
                    print(f'  "category": "{item["category"]}"')
                    print("}")
                else:
                    print(response.json())
            except Exception as e:
                print({"error": str(e)})

        elif choice == "3":
            name = input("Name: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            category = input("Category: ")
            data = {"name": name, "quantity": qty, "price": price, "category": category}
            print(requests.post(f"{BASE_URL}/items", json=data).json())

        elif choice == "4":
            item_id = input("Enter ID: ")
            qty = input("New Quantity (leave blank to skip): ")
            price = input("New Price (leave blank to skip): ")

            data = {}
            if qty:
                data["quantity"] = int(qty)
            if price:
                data["price"] = float(price)

            print(requests.patch(f"{BASE_URL}/items/{item_id}", json=data).json())

        elif choice == "5":
            item_id = input("Enter ID: ")
            print(requests.delete(f"{BASE_URL}/items/{item_id}").json())

        elif choice == "6":
            name = input("Product name: ")
            try:
                result = requests.get(f"{BASE_URL}/search/{name}")
                if result.status_code == 200:
                    print(result.json())
                else:
                    print(result.json())
            except Exception as e:
                print({"error": str(e)})

        elif choice == "7":
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
