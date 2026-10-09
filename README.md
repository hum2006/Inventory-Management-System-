# Inventory Management System

This is a simple project built with Python and Flask.  
It allows you to manage items in an inventory (add, view, update, delete) and fetch product details from the OpenFoodFacts API.

## Features
- View all items
- View one item
- Add new item
- Update item
- Delete item
- Search products from OpenFoodFacts
- Import a product into inventory
- Command-line interface (CLI) to interact with the API
- Automated tests using Pytest

## Project Structure

inventory-management-system/
│
├── README.md          # Documentation
├── app.py             # Flask REST API
├── cli.py             # Command-line interface
├── inventory.json     # Sample inventory data
├── requirements.txt   # Dependencies
└── tests.py           # Automated tests

## Technologies Used
- Python – Main programming language
- Flask – REST API framework
- Requests – For external API calls
- Pytest – For testing
- OpenFoodFacts API– External product data
- JSON – Simple data storage
- Git/GitHub – Version control

## How to Run

1. Install dependencies:
"pip install -r requirements.txt"

2. Start the Flask API:
"python3 app.py"

3. Run the CLI:
"python3 cli.py"

4. Run tests:
"pytest tests.py"

## Example API Routes
1. GET /items → View all items
2. GET /items/1 → View one item
3. POST /items → Add new item
4. PATCH /items/1 → Update item
5. DELETE /items/1 → Delete item
6. GET /search/milk → Search OpenFoodFacts for “milk”

## What I Learned
This project helped me understand:
1. How to build a REST API with Flask
2. How CRUD operations work
3. How to connect to an external API
4. How to write simple automated tests
5. How to use Git and GitHub for version control