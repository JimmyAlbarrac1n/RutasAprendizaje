from flask import Blueprint, request, jsonify, session
from app.models.user_model import UserModel
from bson import ObjectId

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            "status": "error",
            "message": "Email y contraseña son requeridos"
        }), 400

    user = UserModel.get_user_by_email(email)
    if not user or not UserModel.verify_password(user, password):
        return jsonify({
            "status": "error",
            "message": "Email o contraseña incorrectos"
        }), 401

    # Guardar información del usuario en la sesión
    session['user_id'] = str(user['_id'])
    session['role'] = user['role']
    session['email'] = user['email']

    return jsonify({
        "status": "success",
        "message": "Login exitoso",
        "data": {
            "user_id": str(user['_id']),
            "email": user['email'],
            "role": user['role']
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        "status": "success",
        "message": "Logout exitoso"
    }), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({
            "status": "error",
            "message": "No hay sesión activa"
        }), 401

    user = UserModel.get_user_by_id(ObjectId(session['user_id']))
    if not user:
        session.clear()
        return jsonify({
            "status": "error",
            "message": "Usuario no encontrado"
        }), 404

    user['_id'] = str(user['_id'])
    user.pop('password', None)  # No enviar la contraseña al cliente
    
    return jsonify({
        "status": "success",
        "data": user
    }), 200
