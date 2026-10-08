import requests

BASE_URL = "http://127.0.0.1:5000"

def show_menu():
    print("\n1. View all items")
    print("2. View one item")
    print("3. Add item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Search OpenFoodFacts")
    print("7. Exit")

def main():
    while True:
        show_menu()
        choice = input("Choose: ")

        if choice == "1":
            print(requests.get(f"{BASE_URL}/items").json())
        elif choice == "2":
            item_id = input("Enter ID: ")
            print(requests.get(f"{BASE_URL}/items/{item_id}").json())
        elif choice == "3":
            name = input("Name: ")
            qty = int(input("Quantity: "))
            price = float(input("Price: "))
            cat = input("Category: ")
            print(requests.post(f"{BASE_URL}/items", json={"name":name,"quantity":qty,"price":price,"category":cat}).json())
        elif choice == "4":
            item_id = input("Enter ID: ")
            qty = int(input("New Quantity: "))
            print(requests.patch(f"{BASE_URL}/items/{item_id}", json={"quantity":qty}).json())
        elif choice == "5":
            item_id = input("Enter ID: ")
            print(requests.delete(f"{BASE_URL}/items/{item_id}").json())
        elif choice == "6":
            name = input("Product name: ")
            print(requests.get(f"{BASE_URL}/search/{name}").json())
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
