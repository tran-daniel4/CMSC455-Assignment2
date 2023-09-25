import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

def get_products():
    response = requests.get('http://127.0.0.1:5000/products')
    data = response.json()
    return data

def get_product(products_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{products_id}')
    data = response.json()
    return data

def create_product(name, price, quantity):
    new_product = {"name": name, "price": price, "quantity": quantity}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    data = response.json()
    return data

def get_cart(user_id):
    response = requests.get(f'http://127.0.0.1:5001/cart/{user_id}')
    if response.status_code == 200:
        data = response.json()
        return data.get("cart", {}) 
    else:
        return {}

def add_product(user_id, product_id, quantity):
    product_data = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    product_data = product_data.json()
    add_to_cart = {"id": product_id, "quantity": quantity}
    response = requests.post(f'http://127.0.0.1:5001/cart/{user_id}/add/{product_id}', json=add_to_cart)
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": "Failed to add product to cart"}

def remove_product(user_id, product_id):
    response = requests.post(f'http://127.0.0.1:5001/cart/{user_id}/remove/{product_id}')
    data = response.json()
    return data

if __name__ == '__main__':
    user_id = 123
    result = add_product(user_id, 2, 1)
    print(result)
    # get_cart(user_id)
    # all_products = get_products()
    # print("All Products:")
    # print(all_products)

    # product_id = 4
    # specific_product = get_product(product_id)
    # print(f"\nProduct {product_id}:")
    # print(specific_product)

    # created_product = create_product("a", 1, 1)
    # print(f"\nCreated product:")
    # print(created_product)


    # product_response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    
    # if product_response.status_code != 200:
    #     return {"error": f"Product Service returned status code {product_response.status_code}"}
    
    # product_data = product_response.json()
    
    # if "quantity" in product_data and product_data["quantity"] > 0:
    #     response = requests.post(f'http://127.0.0.1:5001/cart/{user_id}/add/{product_id}')
    #     data = response.json()
    #     return data
    # else:
    #     return {"error": "Product is not available"}