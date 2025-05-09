from flask import Blueprint, request, jsonify, session
from app.models.tag_model import TagModel
from bson import ObjectId

tag_bp = Blueprint('tag_bp', __name__)

def check_admin():
    if 'role' not in session or session['role'] != 'admin':
        return False
    return True

# GET all tags
@tag_bp.route('/', methods=['GET'])
def get_tags():
    try:
        tags = TagModel.get_all_tags()
        for tag in tags:
            tag['_id'] = str(tag['_id'])
        return jsonify({
            "status": "success",
            "data": tags
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# GET single tag
@tag_bp.route('/<tag_id>', methods=['GET'])
def get_tag(tag_id):
    try:
        tag = TagModel.get_tag_by_id(tag_id)
        if not tag:
            return jsonify({
                "status": "error",
                "message": "Etiqueta no encontrada"
            }), 404
        
        tag['_id'] = str(tag['_id'])
        return jsonify({
            "status": "success",
            "data": tag
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# POST create tag
@tag_bp.route('/', methods=['POST'])
def create_tag():
    try:
        if not check_admin():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de administrador"
            }), 403

        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        result = TagModel.create_tag(data)
        return jsonify({
            "status": "success",
            "message": "Etiqueta creada exitosamente",
            "data": {
                "id": str(result.inserted_id)
            }
        }), 201
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# PUT update tag
@tag_bp.route('/<tag_id>', methods=['PUT'])
def update_tag(tag_id):
    try:
        if not check_admin():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de administrador"
            }), 403

        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        result = TagModel.update_tag(tag_id, data)
        if result.matched_count == 0:
            return jsonify({
                "status": "error",
                "message": "Etiqueta no encontrada"
            }), 404

        return jsonify({
            "status": "success",
            "message": "Etiqueta actualizada exitosamente"
        }), 200
    except ValueError as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# DELETE tag
@tag_bp.route('/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    try:
        if not check_admin():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de administrador"
            }), 403

        result = TagModel.delete_tag(tag_id)
        if result.deleted_count == 0:
            return jsonify({
                "status": "error",
                "message": "Etiqueta no encontrada"
            }), 404

        return jsonify({
            "status": "success",
            "message": "Etiqueta eliminada exitosamente"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
