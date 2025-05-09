from flask import Blueprint, request, jsonify
from app.models.user_model import UserModel
from bson import ObjectId
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user_bp', __name__)

# GET all users
@user_bp.route('/', methods=['GET'])
def get_users():
    users = list(UserModel.get_all_users())
    for user in users:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
    return jsonify(users), 200

# POST create user
@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    result = UserModel.create_user(data)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201

# PUT update user
@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    result = UserModel.update_user(ObjectId(user_id), data)
    return jsonify({"matched": result.matched_count, "modified": result.modified_count}), 200

# DELETE user
@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = UserModel.delete_user(ObjectId(user_id))
    return jsonify({"deleted_count": result.deleted_count}), 200

# Ruta protegida
@user_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_profile():
    identity = get_jwt_identity()
    user = UserModel.get_user_by_email(identity['email'])
    user['_id'] = str(user['_id'])
    return jsonify(user), 200
