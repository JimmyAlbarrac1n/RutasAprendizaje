from flask import Blueprint, request, jsonify, session
from app.models.material_model import MaterialModel
from bson import ObjectId

material_bp = Blueprint('material_bp', __name__)

def check_professor():
    """Verifica si el usuario actual es profesor"""
    if 'role' not in session or session['role'] != 'professor':
        return False
    return True

def format_material(material):
    """Formatea un material para la respuesta JSON"""
    material['_id'] = str(material['_id'])
    material['created_by'] = str(material['created_by'])
    material['tags'] = [str(tag_id) for tag_id in material['tags']]
    if 'prerequisites' in material:
        material['prerequisites'] = [str(tag_id) for tag_id in material['prerequisites']]
    return material

# GET all materials
@material_bp.route('/', methods=['GET'])
def get_materials():
    try:
        # Si es profesor, solo ver sus materiales
        if 'role' in session and session['role'] == 'professor':
            materials = MaterialModel.get_materials_by_professor(ObjectId(session['user_id']))
        else:
            materials = MaterialModel.get_all_materials()

        # Formatear respuesta
        materials = [format_material(material) for material in materials]
        return jsonify({
            "status": "success",
            "data": materials
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# GET single material
@material_bp.route('/<material_id>', methods=['GET'])
def get_material(material_id):
    try:
        material = MaterialModel.get_material_by_id(material_id)
        if not material:
            return jsonify({
                "status": "error",
                "message": "Material no encontrado"
            }), 404

        return jsonify({
            "status": "success",
            "data": format_material(material)
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# POST create material
@material_bp.route('/', methods=['POST'])
def create_material():
    try:
        if not check_professor():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de profesor"
            }), 403

        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        # Agregar ID del profesor que crea el material
        data['created_by'] = session['user_id']

        result = MaterialModel.create_material(data)
        return jsonify({
            "status": "success",
            "message": "Material creado exitosamente",
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

# PUT update material
@material_bp.route('/<material_id>', methods=['PUT'])
def update_material(material_id):
    try:
        if not check_professor():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de profesor"
            }), 403

        # Verificar que el material pertenece al profesor
        material = MaterialModel.get_material_by_id(material_id)
        if not material:
            return jsonify({
                "status": "error",
                "message": "Material no encontrado"
            }), 404

        if str(material['created_by']) != session['user_id']:
            return jsonify({
                "status": "error",
                "message": "No autorizado. Solo puedes modificar tus propios materiales"
            }), 403

        data = request.json
        if not data:
            return jsonify({
                "status": "error",
                "message": "No se proporcionaron datos"
            }), 400

        result = MaterialModel.update_material(material_id, data)
        return jsonify({
            "status": "success",
            "message": "Material actualizado exitosamente"
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

# DELETE material
@material_bp.route('/<material_id>', methods=['DELETE'])
def delete_material(material_id):
    try:
        if not check_professor():
            return jsonify({
                "status": "error",
                "message": "No autorizado. Se requiere rol de profesor"
            }), 403

        # Verificar que el material pertenece al profesor
        material = MaterialModel.get_material_by_id(material_id)
        if not material:
            return jsonify({
                "status": "error",
                "message": "Material no encontrado"
            }), 404

        if str(material['created_by']) != session['user_id']:
            return jsonify({
                "status": "error",
                "message": "No autorizado. Solo puedes eliminar tus propios materiales"
            }), 403

        result = MaterialModel.delete_material(material_id)
        return jsonify({
            "status": "success",
            "message": "Material eliminado exitosamente"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
