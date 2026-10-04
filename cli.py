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
    print("6. Search OpenFoodFacts by name")
    print("7. Import product by name")
    print("8. Exit")
    print("==============================")


# View all items
def view_items():

    response = requests.get(f"{BASE_URL}/items")

    if response.status_code == 200:

        items = response.json()

        print("\nInventory")
        print("---------")

        if not items:
            print("Inventory is empty.")
            return

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


# View one item
def view_item():

    item_id = int(input("Enter item ID: "))

    response = requests.get(
        f"{BASE_URL}/items/{item_id}"
    )

    if response.status_code == 200:

        item = response.json()

        print("\nItem Details")
        print("------------")
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Quantity: {item['quantity']}")
        print(f"Price: {item['price']}")
        print(f"Category: {item['category']}")

    else:
        print("Item not found.")


# Add item
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

    response = requests.post(
        f"{BASE_URL}/items",
        json=item
    )

    if response.status_code == 201:

        print("\nItem added successfully.")
        print(response.json())

    else:
        print("Could not add item.")
        print(response.json())


# Update item
def update_item():

    item_id = int(input("Enter item ID to update: "))

    print("\nLeave a field empty if you do not want to change it.")

    name = input("Enter new name: ")
    quantity = input("Enter new quantity: ")
    price = input("Enter new price: ")
    category = input("Enter new category: ")

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


# Delete item
def delete_item():

    item_id = int(input("Enter item ID to delete: "))

    response = requests.delete(
        f"{BASE_URL}/items/{item_id}"
    )

    if response.status_code == 200:

        print("\nItem deleted successfully.")

    else:
        print("Could not delete item.")
        print(response.json())


# Search OpenFoodFacts
def search_product():

    name = input("Enter product name: ")

    response = requests.get(
        f"{BASE_URL}/products/search",
        params={"name": name}
    )

    if response.status_code == 200:

        products = response.json()

        if not products:
            print("No products found.")
            return

        print("\nOpenFoodFacts Results")
        print("---------------------")

        for number, product in enumerate(
            products,
            start=1
        ):

            print(f"\n{number}. {product['name']}")
            print(f"   Brand: {product['brand']}")
            print(f"   Category: {product['category']}")
            print(f"   Quantity: {product['quantity']}")

    else:

        print("Could not search OpenFoodFacts.")
        print(response.json())


# Import product
def import_product():

    name = input("Enter product name to import: ")

    response = requests.post(
        f"{BASE_URL}/products/import",
        json={"name": name}
    )

    if response.status_code == 201:

        data = response.json()

        print("\nProduct imported successfully.")
        print("Added to inventory:")
        print(data["item"])

    else:

        print("Could not import product.")
        print(response.json())


# Main program
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