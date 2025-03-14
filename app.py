from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from db import db

# Initialize app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-dev-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///revobank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
jwt = JWTManager(app)
db.init_app(app)

# Import route blueprints (after db is initialized to avoid circular imports)
from routes.user_routes import user_bp
from routes.account_routes import account_bp
from routes.transaction_routes import transaction_bp

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(account_bp, url_prefix='/accounts')
app.register_blueprint(transaction_bp, url_prefix='/transactions')

@app.route('/')
def index():
    return jsonify({
        'message': 'Welcome to RevoBank API',
        'version': '1.0.0',
        'documentation': '/docs'
    })

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True) 