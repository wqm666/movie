from flask import Blueprint, request, jsonify
from models import Movie
from utils import is_admin, is_user_logged_in, json_serializable, token_required


movies_bp = Blueprint('movies_bp', __name__)


@movies_bp.route('/', methods=['GET'])
def get_movies():
    """
    Get a list of all movies.
    Check if the user is logged in, and if so, return a list of all movies Otherwise, an unauthorized message is returned.
    """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    movies = Movie.find_all()
    movies = json_serializable(movies)
    return jsonify(movies), 200

@movies_bp.route('/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Get the movie information based on its ID.
    Check if the user is logged in, and if so, return the movie information. Otherwise, an unauthorized message is returned.
    """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    movie = Movie.find_by_id(movie_id)
    if movie:
        movie = json_serializable(movie)
        return jsonify(movie), 200
    else:
        return jsonify({"message": "Movie not found"}), 404
    
@movies_bp.route('/details/<movie_id>/<detail_id>', methods=['GET'])
def get_detail_by_ids(movie_id, detail_id):
    """
    Query the detail object by movie ID and detail ID.
    Parameters:
    movie_id (str): The ObjectId for the movie.
    detail_id (int) -the ID of the detail.
    Returns:
    dict: The matching detail object
    """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    detail = Movie.find_detail_by_ids(movie_id, int(detail_id))
    if detail:
        return jsonify(detail), 200
    return jsonify({"message": "Detail not found"}), 404

@movies_bp.route('/filter', methods=['POST'])
def filter_movies():
    """ Filter movies by criteria """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    criteria = request.get_json()
    movies = Movie.filter_movies(criteria)
    movies = json_serializable(movies)
    if movies:
        return jsonify(movies), 200
    return jsonify({"message": "Movies not found"}), 404

@movies_bp.route('/sort', methods=['POST'])
def sort_movies():
    """ Sort the movies by criteria """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    sort_criteria = request.get_json()
    movies = Movie.sort_movies(sort_criteria)
    movies = json_serializable(movies)
    return jsonify(movies), 200

@movies_bp.route('/aggregate', methods=['POST'])
def aggregate_movies():
    """ Summarize and aggregate movies by condition """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    pipeline = request.get_json()
    movies = Movie.aggregate_movies(pipeline)
    movies = json_serializable(movies)
    return jsonify(movies), 200

@movies_bp.route('/summarize', methods=['GET'])
def summarize_movies():
    """ Summarizing movie information """
    if not is_user_logged_in():
        return jsonify({'message': 'Unauthorized'}), 401
    summary = Movie.summarize_movies()
    summary = json_serializable(summary)
    return jsonify(summary), 200

@movies_bp.route('/', methods=['POST'])
@token_required
def create_movie(current_user):
    """
    Create a new movie.
    Check if the user is an administrator, and if so, insert the movie data. Otherwise, an unauthorized message is returned.
    """
    data = request.get_json()
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    movie_id =  Movie.insert_one(data)
    return jsonify({"message": "Movie added successfully", "id": str(movie_id)}), 201

@movies_bp.route('/<movie_id>', methods=['PUT'])
@token_required
def update_movie(current_user, movie_id):
    """
    Update movie information.
    Check if the user is an administrator, and if so, update the movie data. Otherwise, an unauthorized message is returned.
    """
    data = request.get_json()
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    result = Movie.update_one(movie_id, data)
    if result.matched_count > 0:
        return jsonify({"message": "Movie updated successfully", "id": movie_id}), 200
    else:
        return jsonify({"message": "Movie not found"}), 404

@movies_bp.route('/<movie_id>', methods=['DELETE'])
@token_required
def delete_movie(current_user, movie_id):
    """
    Delete a movie.
    Check if the user is an administrator, and if so, delete the movie data. Otherwise, an unauthorized message is returned.
    """
    if not is_admin():
        return jsonify({"message": "Unauthorized"}), 401
    result = Movie.delete_one(movie_id)
    if result.deleted_count > 0:
        return jsonify({"message": "Movie deleted successfully"}), 200
    else:
        return jsonify({"message": "Movie not found"}), 404