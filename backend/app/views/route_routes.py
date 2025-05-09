from flask import Blueprint, request, jsonify, session
from app.models.route_model import LearningRouteModel
from bson import ObjectId
from datetime import datetime

route_bp = Blueprint('route_bp', __name__)

def check_professor():
    return 'role' in session and session['role'] == 'professor'

def format_route(route):
    route['_id'] = str(route['_id'])
    if 'created_by' in route:
        route['created_by'] = str(route['created_by'])
    if 'created_at' in route:
        route['created_at'] = route['created_at'].strftime('%Y-%m-%d') if hasattr(route['created_at'], 'strftime') else str(route['created_at'])
    if 'updated_at' in route:
        route['updated_at'] = route['updated_at'].strftime('%Y-%m-%d') if hasattr(route['updated_at'], 'strftime') else str(route['updated_at'])
    return route

# GET all routes
@route_bp.route('/', methods=['GET'])
def get_routes():
    try:
        routes = LearningRouteModel.get_all_routes()
        routes = [format_route(route) for route in routes]
        return jsonify({"status": "success", "data": routes}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# POST create route
@route_bp.route('/', methods=['POST'])
def create_route():
    try:
        if not check_professor():
            return jsonify({"status": "error", "message": "No autorizado. Se requiere rol de profesor"}), 403
        data = request.json
        if not data or 'name' not in data or 'description' not in data:
            return jsonify({"status": "error", "message": "Faltan campos obligatorios"}), 400
        data['created_by'] = session['user_id']
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = LearningRouteModel.create_route(data)
        return jsonify({"status": "success", "message": "Ruta creada exitosamente", "data": {"id": str(result.inserted_id)}}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# PUT update route
@route_bp.route('/<route_id>', methods=['PUT'])
def update_route(route_id):
    try:
        if not check_professor():
            return jsonify({"status": "error", "message": "No autorizado. Se requiere rol de profesor"}), 403
        data = request.json
        if not data:
            return jsonify({"status": "error", "message": "No se proporcionaron datos"}), 400
        data['updated_at'] = datetime.utcnow()
        result = LearningRouteModel.update_route(ObjectId(route_id), data)
        if result.matched_count == 0:
            return jsonify({"status": "error", "message": "Ruta no encontrada"}), 404
        return jsonify({"status": "success", "message": "Ruta actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# DELETE route
@route_bp.route('/<route_id>', methods=['DELETE'])
def delete_route(route_id):
    try:
        if not check_professor():
            return jsonify({"status": "error", "message": "No autorizado. Se requiere rol de profesor"}), 403
        result = LearningRouteModel.delete_route(ObjectId(route_id))
        if result.deleted_count == 0:
            return jsonify({"status": "error", "message": "Ruta no encontrada"}), 404
        return jsonify({"status": "success", "message": "Ruta eliminada exitosamente"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
