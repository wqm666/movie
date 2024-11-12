from pymongo import MongoClient
import secrets

class Config:
    """
    Configuration classes, which store configuration information for the application.
    Attributes:
    SECRET_KEY (str) -The key used for session encryption
    MONGODB_URI (str): The URI to connect to the MongoDB database.
    DB_NAME (str): The name of the database
    """
    SECRET_KEY = secrets.token_hex(32)
    SESSION_COOKIE_SAMESITE='None' # Allow cookies to be sent in cross-origin requests
    SESSION_COOKIE_SECURE=False,     # In development, set this to False (use True in production)
    MONGODB_URI = "mongodb://localhost:27017/"
    DB_NAME = "hot_movie_guide_db"

def get_db():
    """
    A function to get a MongoDB database instance.
    Connect to a MongoDB database and return a database instance with the specified name.
    Returns:
    Database: A MongoDB database instance with the specified name.
    """
    client = MongoClient(Config.MONGODB_URI)
    return client[Config.DB_NAME]