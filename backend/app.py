import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from models import db, User, Item
from routes import bp as api_bp
from dashboard import dashboard_bp
from admin import init_admin

# Load environment variables from root .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cheasy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'super-secret-key-change-me')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

CORS(app)

db.init_app(app)
jwt = JWTManager(app)
Migrate(app, db)
init_admin(app, db, User, Item)

app.register_blueprint(api_bp)
app.register_blueprint(dashboard_bp)

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
