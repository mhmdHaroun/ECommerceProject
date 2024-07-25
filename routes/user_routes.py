import re
from flask import Blueprint, request, jsonify
from models import User
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

def is_valid_email(email):
    """Check if the email is in a valid format."""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def is_strong_password(password):
    """Check if the password meets strength requirements."""
    if len(password) < 8:
        return False
    if not re.search(r'[A-Za-z]', password):  # Must contain letters
        return False
    if not re.search(r'[0-9]', password):  # Must contain numbers
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Must contain special characters
        return False
    return True



@user_bp.route('/register', methods=['POST'])
def register():
    print("Register endpoint hit")  
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    password = data.get('password')

    if not (first_name and last_name and email and phone_number and password):
        return jsonify({"error": "All fields are required"}), 400
    
    if not is_valid_email(email):
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered"}), 400
    
    if not is_strong_password(password):
        return jsonify({"error": "Enter stronger Password"}), 400

    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
    )
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if user:
        return jsonify({
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number
        }), 200
    else:
        return jsonify({"error": "User not found"}), 404
