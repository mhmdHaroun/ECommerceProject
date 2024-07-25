from flask import Flask
from routes.user_routes import user_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp


def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(order_bp)
