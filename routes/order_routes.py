from flask import Blueprint, request, jsonify
from models import Order, OrderItem, Product, User
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()
    product_orders = data.get('products')

    if not product_orders:
        return jsonify({"error": "No products to order"}), 400

    order = Order(user_id=user_id)
    db.session.add(order)
    db.session.commit()

    for product_order in product_orders:
        product = Product.query.get(product_order['product_id'])
        if product:
            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=product_order['quantity']
            )
            db.session.add(order_item)
        else:
            return jsonify({"error": f"Product with id {product_order['product_id']} not found"}), 400

    db.session.commit()
    return jsonify({"message": "Order created successfully"}), 201


@order_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify({
        "id": order.id,
        "user_id": order.user_id,
        "date": order.date,
        "order_items": [{
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product_name": item.product.name
        } for item in order.order_items]
    }), 200


@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def list_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": order.id,
        "date": order.date,
        "order_items": [{
            "product_id": item.product_id,
            "quantity": item.quantity,
            "product_name": item.product.name
        } for item in order.order_items]
    } for order in orders]), 200
