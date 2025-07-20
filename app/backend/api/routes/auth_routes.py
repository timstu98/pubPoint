from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
import datetime

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Check if required fields are present
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 409
    
    # Create new user
    new_user = User(
        email=data['email'],
        address=data.get('address', ''),
        first_name=data.get('firstName', ''),
        second_name=data.get('secondName', '')
    )
    new_user.set_password(data['password'])
    
    # Save to database
    db.session.add(new_user)
    db.session.commit()
    
    # Create JWT token
    access_token = create_access_token(
        identity=new_user.id,
        expires_delta=datetime.timedelta(days=1)
    )
    
    return jsonify({
        "message": "User registered successfully",
        "token": access_token,
        "user": new_user.get_as_dict()
    }), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Check if required fields are present
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400
    
    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    
    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Create JWT token
    access_token = create_access_token(
        identity=user.id,
        expires_delta=datetime.timedelta(days=1)
    )
    
    return jsonify({
        "token": access_token,
        "user": user.get_as_dict()
    }), 200

@auth_routes.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    # Get current user ID from JWT
    current_user_id = get_jwt_identity()
    
    # Find user in database
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({"user": user.get_as_dict()}), 200