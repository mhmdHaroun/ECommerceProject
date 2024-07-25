# from flask import Blueprint, request, jsonify
# from models import Product, User
# from extensions import db
# from flask_jwt_extended import jwt_required, get_jwt_identity

# product_bp = Blueprint('product', __name__)

# def is_admin(user_id):
#     """Check if the user has admin privileges."""
#     user = User.query.get(user_id)
#     return user and user.role == 'admin'

# @product_bp.route('/products', methods=['GET'])
# def list_products():
#     products = Product.query.all()
#     return jsonify([{
#         "id": product.id,
#         "name": product.name,
#         "description": product.description,
#         "price": product.price,
#         "stock": product.stock
#     } for product in products]), 200

# @product_bp.route('/products/<int:product_id>', methods=['GET'])
# def get_product(product_id):
#     product = Product.query.get_or_404(product_id)
#     return jsonify({
#         "id": product.id,
#         "name": product.name,
#         "description": product.description,
#         "price": product.price,
#         "stock": product.stock
#     }), 200

# @product_bp.route('/products', methods=['POST'])
# @jwt_required()
# def create_product():
#     user_id = get_jwt_identity()
#     if not is_admin(user_id):
#         return jsonify({"error": "Permission denied"}), 403

#     data = request.get_json()
#     name = data.get('name')
#     description = data.get('description')
#     price = data.get('price')
#     stock = data.get('stock')

#     if not (name and price and stock):
#         return jsonify({"error": "Name, price, and stock are required"}), 400

#     product = Product(name=name, description=description, price=price, stock=stock)
#     db.session.add(product)
#     db.session.commit()
#     return jsonify({"message": "Product created successfully"}), 201
















from flask import Blueprint, request, jsonify
from models import Product
from extensions import db

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    } for product in products]), 200

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock
    }), 200

@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock = data.get('stock')

    if not (name and price and stock):
        return jsonify({"error": "Name, price, and stock are required"}), 400

    product = Product(name=name, description=description, price=price, stock=stock)
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201
