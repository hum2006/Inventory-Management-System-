import requests

BASE_URL = "http://127.0.0.1:5000"


def show_menu():
    print("\n==============================")
    print("   INVENTORY MANAGEMENT SYSTEM")
    print("==============================")
    print("1. View all items")
    print("2. View one item")
    print("3. Add item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Search OpenFoodFacts")
    print("7. Import product")
    print("8. Exit")
    print("==============================")


def view_items():
    response = requests.get(f"{BASE_URL}/items")

    if response.status_code == 200:
        items = response.json()

        if not items:
            print("Inventory is empty.")
            return

        print("\nCurrent Inventory:")
        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Quantity: {item['quantity']} | "
                f"Price: {item['price']} | "
                f"Category: {item['category']}"
            )
    else:
        print("Could not retrieve inventory.")


def view_item():
    item_id = input("Enter item ID: ")

    response = requests.get(f"{BASE_URL}/items/{item_id}")

    if response.status_code == 200:
        item = response.json()

        print("\nItem Details")
        print("----------------")
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Price: {item['price']}")
        print(f"Category: {item['category']}")
    else:
        print("Item not found.")


def add_item():
    name = input("Enter item name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))
    category = input("Enter category: ")

    item = {
        "name": name,
        "quantity": quantity,
        "price": price,
        "category": category
    }

    response = requests.post(f"{BASE_URL}/items", json=item)

    if response.status_code == 201:
        print("\nItem added successfully.")
        print(response.json())
    else:
        print("Could not add item.")
        print(response.json())


def update_item():
    item_id = input("Enter item ID: ")

    print("\nLeave a field empty if you do not want to change it.")

    name = input("New name: ")
    quantity = input("New quantity: ")
    price = input("New price: ")
    category = input("New category: ")

    data = {}

    if name:
        data["name"] = name

    if quantity:
        data["quantity"] = int(quantity)

    if price:
        data["price"] = float(price)

    if category:
        data["category"] = category

    response = requests.patch(
        f"{BASE_URL}/items/{item_id}",
        json=data
    )

    if response.status_code == 200:
        print("\nItem updated successfully.")
        print(response.json())
    else:
        print("Could not update item.")
        print(response.json())


def delete_item():
    item_id = input("Enter item ID: ")

    response = requests.delete(f"{BASE_URL}/items/{item_id}")

    if response.status_code == 200:
        print(response.json()["message"])
    else:
        print("Item not found.")


def search_product():
    barcode = input("Enter product barcode: ")

    response = requests.get(f"{BASE_URL}/products/{barcode}")

    if response.status_code == 200:
        product = response.json()

        print("\nProduct Information")
        print("-------------------")
        print(f"Name: {product['name']}")
        print(f"Brand: {product['brand']}")
        print(f"Category: {product['category']}")
        print(f"Quantity: {product['quantity']}")
        print(f"Barcode: {product['barcode']}")
    else:
        print("Product could not be found.")


def import_product():
    barcode = input("Enter product barcode: ")

    response = requests.post(
        f"{BASE_URL}/products/import/{barcode}"
    )

    if response.status_code == 201:
        data = response.json()

        print("\nProduct imported successfully.")
        print(data["item"])
    else:
        print("Could not import product.")
        print(response.json())


def main():
    while True:
        show_menu()
        choice = input("Choose an option: ")

        try:
            if choice == "1":
                view_items()

            elif choice == "2":
                view_item()

            elif choice == "3":
                add_item()

            elif choice == "4":
                update_item()

            elif choice == "5":
                delete_item()

            elif choice == "6":
                search_product()

            elif choice == "7":
                import_product()

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")

        except ValueError:
            print("Please enter a valid number.")

        except requests.RequestException:
            print("Could not connect to the Flask API.")
            print("Make sure app.py is running.")


if __name__ == "__main__":
    main()