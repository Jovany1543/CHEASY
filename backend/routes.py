from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, Item

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong from Flask with SQLAlchemy and JWT'})

@bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400
    existing = User.query.filter_by(username=username).first()
    if existing:
        return jsonify({'error': 'username already registered'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user registered', 'user': user.to_dict()}), 201

@bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'invalid credentials'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'access_token': token, 'user': user.to_dict()})

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@bp.route('/auth/protected', methods=['GET'])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'message': 'Access granted', 'user': user.to_dict()})

@bp.route('/items', methods=['GET'])
@jwt_required()
def get_items():
    items = Item.query.order_by(Item.created_at.desc()).all()
    return jsonify([item.to_dict() for item in items])

@bp.route('/items', methods=['POST'])
@jwt_required()
def create_item():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({'error': 'text required'}), 400

    item = Item(text=text)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201
