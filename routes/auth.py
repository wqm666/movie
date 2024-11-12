from flask import Blueprint, request, jsonify, session
from models import User
from utils import json_serializable, token_required
import bcrypt, jwt, datetime
from config import Config


auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Get user information from the request, including username, password, and email. The password is hashed and the user information is inserted into the database.
    If the registration is successful, a success message is returned. Otherwise, an error message is returned.
    """
    data = request.get_json()
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    user_data = {
        "username": data['username'],
        "password": hashed_password,
        "email": data['email']
    }
    User.insert_one(user_data)
    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    The user is logged in.
    Get the username and password from the request. Authenticate the user and, if successful, set up the session and return a token. Otherwise, an error message is returned.
    """
    data = request.get_json()
    user = User.find_by_username(data['username'])
    if user and bcrypt.checkpw(data['password'].encode('utf-8'), user['password']):
        session['user_id'] = str(user['_id'])
        session['is_admin'] = user.get('is_admin', False)
        token = jwt.encode({
            'user_id': session['user_id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }, Config.SECRET_KEY, algorithm='HS256')
        return jsonify({"token": token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout(current_user):
    """
    Log out the user and clear the session data.
    """
    session.clear()
    return jsonify({"message": "User logged out successfully"}), 200


@auth_bp.route('/user', methods=['GET'])
def get_user_info():
    """
    Get information about the current user.
    Checks to see if the user is logged in, and if so, returns the user's information (excluding the password) Otherwise, an unauthorized message is returned.
    """
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    user_id = session['user_id']
    user = User.find_by_id(user_id)
    if user:
        user = {k: v for k, v in user.items() if k != 'password'}  # 不返回密码
        user = json_serializable(user)  # 确保序列化
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404


@auth_bp.route('/update', methods=['PUT'])
@token_required
def update_user(current_user):
    """
    Update user information.
    Retrieve the user information (username, email, password) to update from the request. Update the user information in the database.
    """
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json()
    user_id = current_user
    user_data = {}
    
    if 'username' in data:
        user_data['username'] = data['username']
    
    if 'email' in data:
        user_data['email'] = data['email']
    
    if 'password' in data:
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
        user_data['password'] = hashed_password
    
    if user_data:
        User.update_one(user_id, user_data)
        return jsonify({"message": "User information updated successfully"}), 200
    else:
        return jsonify({"message": "No valid data provided to update"}), 400
    

@auth_bp.route('/delete_user', methods=['DELETE'])
@token_required
def delete_user(current_user):
    """
    Delete user accounts.
    """
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized"}), 401
    user_id = current_user
    User.delete_one(user_id)
    session.clear()
    return jsonify({"message": "User account deleted successfully"}), 200