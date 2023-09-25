import os
from flask import Flask, jsonify, request
import requests
app = Flask(__name__)

products = [
    {"id": 1, "name": "apple", "price": 3, "quantity": 29},
    {"id": 2, "name": "banana", "price": 4, "quantity": 30},
    {"id": 3, "name": "mango", "price": 5, "quantity": 30},
    {"id": 4, "name": "blueberry", "price": 5, "quantity": 30},
    {"id": 5, "name": "orange", "price": 4, "quantity": 30},
]

# Endpoint 1: Get all products
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products})

# Endpoint 2: Get a specific product by ID
@app.route('/products/<int:products_id>', methods=['GET'])
def get_product(products_id):
    product = next((product for product in products if product["id"] == products_id), None)
    if product:
        return jsonify({"product": product})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Create a new product
@app.route('/products', methods=['POST'])
def create_product():
    new_product = {
        "id": len(products) + 1,
        "name": request.json.get('name'),
        "price": request.json.get('price'),
        "quantity": request.json.get('quantity')
    }
    products.append(new_product)
    return jsonify({"message": "Product created", "product": new_product}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


#     def get_all_products():
#     response = requests.get('http://127.0.0.1:5000/products')
#     data = response.json()
#     return data

# def get_product(products_id):
#     response = requests.get(f'http://127.0.0.1:5000/products/{products_id}')
#     data = response.json()
#     return data

# def create_product(name, price, quantity):
#     new_product = {"name": name, "price": price, "quantity": quantity}
#     response = requests.post('http://127.0.0.1:5000/products', json=new_product)
#     data = response.json()
#     return data