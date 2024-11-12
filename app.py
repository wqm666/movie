from flask import Flask, request, jsonify
from flask_cors import CORS
from routes.auth import auth_bp
from routes.movies import movies_bp
from routes.favorites import favorites_bp
from routes.admin import admin_bp
from models import JSONEncoder, User
import bcrypt

app = Flask(__name__)
app.config.from_object('config.Config')
app.json_encoder = JSONEncoder
CORS(app, origins="http://localhost:4200", supports_credentials=True)  # 配置CORS

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(movies_bp, url_prefix='/movies')
app.register_blueprint(favorites_bp, url_prefix='/favorites')
app.register_blueprint(admin_bp, url_prefix='/admin')

def create_default_admin():
    """
    Create a default super administrator user if it doesn't exist.
    """
    print("Checking for existing admin user...")
    if not User.find_admin():
        print("No admin user found. Creating default admin user...")
        default_admin = {
            "username": "admin",
            "password": bcrypt.hashpw("adminpassword".encode('utf-8'), bcrypt.gensalt()),
            "email": "admin@example.com",
            "is_admin": True
        }
        User.insert_one(default_admin)
        print("Default admin user created")
    else:
        print("Admin user already exists.")

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:4200')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response

if __name__ == "__main__":
    create_default_admin()
    app.run(debug=True)
