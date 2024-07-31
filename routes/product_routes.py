from flask import Blueprint, request, jsonify
from models import Product
from extensions import db
from werkzeug.exceptions import NotFound
from flask_jwt_extended import jwt_required, get_jwt_identity

product_bp = Blueprint('product', __name__)


@product_bp.errorhandler(NotFound)
def not_found(error):
    return jsonify({"error": "Product not found"}), 400


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
    return jsonify({"message": "Product created successfully"}), 401



@product_bp.route('/products/<int:product_id>', methods=['PUT'])

def update_product(product_id):

    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200




@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200
