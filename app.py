from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, migrate, bcrypt
from models import User, Product, Order, OrderItem
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt = JWTManager(app)
    register_blueprints(app)
    return app

app = create_app()

@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": str(error)}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
