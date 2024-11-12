from flask import Blueprint, request, jsonify
from models import User
from utils import is_admin, token_required

admin_bp = Blueprint('admin_bp', __name__)


def json_serializable(data):
    """
    Convert the ObjectId in the data to a string and exclude non-serializable fields like password.
    """
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
            if 'password' in item:
                del item['password']
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
        if 'password' in data:
            del data['password']
    return data

@admin_bp.route('/all_users', methods=['GET'])
@token_required
def get_all_users(current_user):
    """
    Get all user information.
    This action is only allowed by the current administrator.
    """
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    users = User.find_all()
    users = json_serializable(users)
    return jsonify(users), 200

@admin_bp.route('/admin_users', methods=['GET'])
@token_required
def get_admin_user(current_user):
    """
    Get the administrator user information.
    This action is only allowed by the current administrator.
    """
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    admin_user = User.find_admin()
    admin_user = json_serializable(admin_user)
    return jsonify(admin_user), 200

@admin_bp.route('/toggle_admin', methods=['POST'])
@token_required
def toggle_admin(current_user):
    """
    Toggles the user's administrator status.
    This action is only allowed by the current administrator.
    """
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID is required"}), 400
    user = User.find_by_id(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    current_is_admin = user.get('is_admin', False)
    User.update_one(user_id, {"is_admin": not current_is_admin})
    new_status = "admin" if not current_is_admin else "regular user"
    return jsonify({"message": f"User is now a {new_status}"}), 200