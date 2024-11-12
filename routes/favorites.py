from flask import Blueprint, request, jsonify, session
from models import Favorite
from utils import is_user_logged_in


favorites_bp = Blueprint('favorites_bp', __name__)

def json_serializable(data):
    """
    Convert the ObjectId in the data to a string.
    """
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
            if 'user_id' in item:
                item['user_id'] = str(item['user_id'])
            if 'movie_id' in item:
                item['movie_id'] = str(item['movie_id'])
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
        if 'user_id' in data:
            data['user_id'] = str(data['user_id'])
        if 'movie_id' in data:
            data['movie_id'] = str(data['movie_id'])
    return data

@favorites_bp.route('/user', methods=['GET'])
def get_user_favorites():
    """
    Get a list of favorites for the current user.
    Check if the user is logged in, and if so, return a list of all their favorites. Otherwise, an unauthorized message is returned.
    """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"message": "User ID not found in session"}), 400
    favorites = Favorite.find_by_user_id(user_id)
    favorites = json_serializable(favorites)
    if not favorites:
        return jsonify({"message": "No favorites found for this user"}), 404
    return jsonify(favorites), 200

@favorites_bp.route('/', methods=['POST'])
def create_favorite():
    """
    Create a new collection.
    Check if the user is logged-in, and if so, insert the movie ID and user ID into the favorites; Otherwise, an unauthorized message is returned.
    """
    data = request.get_json()
    if not is_user_logged_in():
        return jsonify({"message": "Unauthorized"}), 401
    data['user_id'] = session.get('user_id')
    favorite_id = Favorite.insert_one(data)
    return jsonify({"message": "Favorite added successfully", "id": str(favorite_id)}), 201

@favorites_bp.route('/<favorite_id>', methods=['DELETE'])
def delete_favorite(favorite_id):
    """
    Delete favorites.
    Check whether the user is logged in, if so, delete the favorite data; Otherwise, an unauthorized message is returned.
    """
    if not is_user_logged_in():
        return jsonify({"message": "Unauthorized"}), 401
    Favorite.delete_one(favorite_id)
    return jsonify({"message": "Favorite deleted successfully"}), 200