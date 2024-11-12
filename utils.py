from flask import session, request, jsonify
from models import User
import jwt
from functools import wraps
from config import Config

def is_admin():
    """
    Checks if the current user is an administrator.
    Get the user ID from the session, query for user information, and check the is_admin property for the user.
    Returns:
    bool: True if the user is an administrator Otherwise, it returns False.
    """
    user_id = session.get('user_id')
    if not user_id:
        return False
    user = User.find_by_id(user_id)
    return user and user.get('is_admin', False)

def is_user_logged_in():
    """
    Checks if the user is logged in.
    The user is logged in by checking for the presence of user_id in the session.
    Returns:
    bool: This returns True if the user is logged in Otherwise, it returns False.
    """
    return 'user_id' in session

def json_serializable(data):
    """
    Convert the objectiDs in the data to strings for JSON serialization.
    Parameters:
    data (dict or list) -The data to process
    Returns:
    dict or list: Transformed serialized data
    """
    if isinstance(data, list):
        for item in data:
            if '_id' in item:
                item['_id'] = str(item['_id'])
    elif isinstance(data, dict):
        if '_id' in data:
            data['_id'] = str(data['_id'])
    return data

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            current_user = data['user_id']
        except:
            return jsonify({'message': 'Token is invalid!'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated