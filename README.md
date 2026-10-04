# Inventory Management System

## About the Project
This is a simple Inventory Management System built using Python and Flask.

The system allows a user to manage items in an inventory through a command-line interface (CLI). Users can add new items, view items, update them, and delete them.

For the external API requirement, the project connects to the OpenFoodFacts API. This allows the user to search for food products by name and import a product into the local inventory.

Although OpenFoodFacts is used for the external API feature, the main inventory system is not limited to food. Items such as electronics, clothes, books, stationery, and other products can also be added manually.

## What the System Can Do
The system supports the following:
* View all items in the inventory
* View a specific item
* Add a new item
* Update an existing item
* Delete an item
* Search for products using OpenFoodFacts
* Import a product from OpenFoodFacts into the inventory
* Store inventory data in a JSON file
* Run the system through a command-line interface
* Run automated tests using Pytest

## Technologies Used
The project was built using:
* **Python** – Main programming language
* **Flask** – Used to build the REST API
* **Requests** – Used to communicate with the external API
* **Pytest** – Used for testing
* **OpenFoodFacts API** – Used for external product information
* **JSON** – Used to store inventory data
* **Git and GitHub** – Used for version control and collaboration

## Project Structure
inventory-management-system/
│
├── README.md
├── app.py
├── cli.py
├── inventory.json
├── requirements.txt
└── tests.py

### What Each File Does
## app.py
Contains the Flask REST API and all the inventory routes.

## cli.py
Contains the command-line interface used to interact with the API.

## inventory.json
Stores the inventory items locally.

## tests.py
Contains the automated tests for the application.

## requirements.txt
Contains the Python packages needed to run the project.

## Getting Started

After running the project this is what it will look like

==============================
   INVENTORY MANAGEMENT SYSTEM
==============================
1. View all items
2. View one item
3. Add item
4. Update item
5. Delete item
6. Search OpenFoodFacts by name
7. Import product by name
8. Exit
==============================

## API Routes
### Home
This checks if the Flask API is running.

### View All Items
Returns all the items currently stored in the inventory.

### View One Item
Returns one item using its ID.

### Add an Item
The system automatically gives the new item an ID but you'll need to add the descriptions of the item.

### Update an Item
Items can be updated and only the information that needs to be changed has to be provided.

### Delete an Item
Removes the selected item from the inventory.

## OpenFoodFacts Integration

The project also demonstrates how an application can communicate with an external API.

### Search for a Product
The system sends the product name to OpenFoodFacts and displays information such as:

* Product name
* Brand
* Category
* Quantity

### Import a Product
The application searches OpenFoodFacts for the product and adds the first matching product to the local inventory.

The imported product is then saved in `inventory.json`.

## Inventory Data

The inventory is stored in a simple JSON file instead of using a database.


## Testing
The tests cover important features such as:
* Checking that the API is running
* Viewing inventory
* Viewing a single item
* Creating an item
* Updating an item
* Deleting an item
* Handling items that do not exist
* Searching the external API
* Importing products

## What I Learned
Overall, the project helped me understand how a simple backend application can be built, tested, and managed from development to completion.
