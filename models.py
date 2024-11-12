from bson import ObjectId
from config import get_db
import json

class JSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder for converting objectids to strings.
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return super().default(o)

class User:
    """
    The user model class, which contains user-related database operations.
    """
    collection = get_db()['users']

    @classmethod
    def find_all(cls):
        """
        Finding all users
        Returns:
        list: A list of all users
        """
        return list(cls.collection.find())
    
    @classmethod
    def find_by_id(cls, user_id):
        """
        Find a user by their ID.
        Parameters:
        user_id (str): The user's ObjectId
        Returns:
        dict: user information
        """
        return cls.collection.find_one({"_id": ObjectId(user_id)})


    @classmethod
    def find_admin(cls):
        """
        Find the administrator user.
        Returns:
        dict: Administrator user information
        """
        return list(cls.collection.find({"is_admin": True}))

    @classmethod
    def update_one(cls, user_id, data):
        """
        Update user information.
        Parameters:
        user_id (str): The user's ObjectId
        data (dict) -the user information to update
        Returns:
        None
        """
        cls.collection.update_one({"_id": ObjectId(user_id)}, {"$set": data})

    @classmethod
    def find_by_username(cls, username):
        return cls.collection.find_one({"username": username})
    
    @classmethod
    def insert_one(cls, data):
        cls.collection.insert_one(data)

    @classmethod
    def delete_one(cls, user_id):
        """
        Delete the user.
        Parameters:
        user_id (str): The user's ObjectId
        Returns:
        None
        """
        cls.collection.delete_one({"_id": ObjectId(user_id)})


class Movie:
    """
    Movie model class, which contains database operations related to movies.
    """
    collection = get_db()['movies']

    @classmethod
    def find_all(cls):
        """
        Find all movies.
        Returns:
        list: A list of all the movies
        """
        return list(cls.collection.find())

    @classmethod
    def find_by_id(cls, movie_id):
        """
        Find a movie by its ID.
        Parameters:
        movie_id (str): The ObjectId for the movie.
        Returns:
        dict: movie information
        """
        return cls.collection.find_one({"_id": ObjectId(movie_id)})
    
    @classmethod
    def find_detail_by_ids(cls, movie_id, detail_id):
        """ Find the detail object based on the movie ID and detail ID. """
        movie = cls.collection.find_one(
            {"_id": ObjectId(movie_id), "details.id": detail_id},
            {"details.$": 1}
        )
        if movie and "details" in movie:
            return movie["details"][0]
        return None

    @classmethod
    def filter_movies(cls, criteria):
        """ Filter movies by criteria """
        return list(cls.collection.find(criteria))

    @classmethod
    def sort_movies(cls, sort_criteria):
        """ Sort the movies by criteria """
        return list(cls.collection.find().sort(sort_criteria))

    @classmethod
    def aggregate_movies(cls, pipeline):
        """ Summarize and aggregate movies by condition """
        return list(cls.collection.aggregate(pipeline))

    @classmethod
    def summarize_movies(cls):
        """ Summarizing movie information """
        pipeline = [
            {"$group": {
                "_id": { "$ifNull": ["$details.director", "Unknown"] },
                "total_movies": {"$sum": 1},
                "average_duration": {"$avg": "$duration"}
            }}
        ]
        return list(cls.collection.aggregate(pipeline))

    @classmethod
    def insert_one(cls, data):
        """
        Insert a new movie.
        Parameters:
        data (dict): Movie information
        Returns:
        None
        """
        result = cls.collection.insert_one(data)
        return result.inserted_id

    @classmethod
    def update_one(cls, movie_id, data):
        """
        Update movie information.
        Parameters:
        movie_id (str): The ObjectId for the movie.
        data (dict) -the movie information to update.
        Returns:
        None
        """
        result = cls.collection.update_one({"_id": ObjectId(movie_id)}, {"$set": data})
        return result

    @classmethod
    def delete_one(cls, movie_id):
        """
        Delete a movie.
        Parameters:
        movie_id (str): The ObjectId for the movie.
        Returns:
        None
        """
        result =cls.collection.delete_one({"_id": ObjectId(movie_id)})
        return result

class Favorite:
    """ The collection model class, which contains collection-related database operations. """
    collection = get_db()['favorites']

    @classmethod
    def find_all(cls):
        """ Find all the collections. Returns: list: A list of all favorites. """
        return list(cls.collection.find())

    @classmethod
    def find_by_movie_id(cls, movie_id):
        """ Find favorites by movie ID. Parameter: movie_id (str): The ObjectId of the movie. Return: list: A list of all favorites for the movie. """
        return list(cls.collection.find({"movie_id": ObjectId(movie_id)}))

    @classmethod
    def find_by_user_id(cls, user_id):
        """ Find favorites by user ID. Parameter: user_id (str): The user's ObjectId. Return: list: A list of all favorites for the user. """
        return list(cls.collection.find({"user_id": ObjectId(user_id)}))

    @classmethod
    def insert_one(cls, data):
        """ Insert a new collection. Parameter: data (dict): Favorites """
        data['user_id'] = ObjectId(data['user_id']) 
        data['movie_id'] = ObjectId(data['movie_id']) 
        result = cls.collection.insert_one(data)
        return result.inserted_id

    @classmethod
    def delete_one(cls, favorite_id):
        """ Delete favorites. Parameter: favorite_id (str): The ObjectId to collect. Return: None """
        cls.collection.delete_one({"_id": ObjectId(favorite_id)})