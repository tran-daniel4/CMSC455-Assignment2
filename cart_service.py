import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

carts = [
    {"user_id": 123, "products": []},
    {"user_id": 321, "products": []},
]

# Endpoint 4: Get user cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    cart = next((cart for cart in carts if cart["user_id"] == user_id), None)
    if cart:
        return jsonify({"cart": cart})
    else:
        return jsonify({"error": "Cart not found"}), 404
    # search_cart = carts.get(user_id, {})
    # return jsonify({"cart": search_cart})

# Endpoint 5: Add new product
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_product(user_id, product_id, quantity):
    product_response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')

    if product_response.status_code == 200:
        product_data = product_response.json()
        if "quantity" in product_data and product_data["quantity"] >= request.json.get("quantity", quantity):
        # Find the user's cart
            user_cart = next((cart for cart in carts if cart["user_id"] == user_id), None)
        
            if user_cart:
                # Append the product to the user's cart
                user_cart["products"].append({
                    "product_id": product_id,
                    "quantity": quantity
                })
                return jsonify({"message": "Product added to cart"}), 201
            else:
                return jsonify({"error": "User's cart not found"}), 404
        else:
            return jsonify({"error": "Product quantity not sufficient"}), 400
    else:
        return {"error": "Product not found"}
    


# Endpoint 6: Remove product
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_cart(user_id, product_id, removing):
    user_cart = carts.get(user_id)
    if not user_cart:
        return jsonify({"error": "Cart not found"}), 404
    if product_id not in user_cart:
        return jsonify({"error": "Product not in cart"}), 404
    remove_quantity = request.json.get("quantity", removing)
    current = user_cart[product_id]["quantity"]
    if remove_quantity >= current:
        del user_cart[product_id]
    else:
        user_cart[product_id]["quantity"] -= remove_quantity
    return jsonify({"message": "Product removed from cart"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)