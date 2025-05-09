from app import mongo
from bson import ObjectId
from datetime import datetime

class MaterialModel:
    @staticmethod
    def create_material(material_data):
        """
        Crea un nuevo material de estudio
        Args:
            material_data (dict): Datos del material incluyendo:
                - name: Nombre del material
                - description: Descripción del material
                - difficulty: Nivel de dificultad (1-5)
                - tags: Lista de IDs de etiquetas
                - prerequisites: Lista de IDs de etiquetas de conocimientos previos
                - file_url: URL del archivo (opcional)
                - created_by: ID del profesor que lo crea
        """
        # Validar datos requeridos
        required_fields = ['name', 'description', 'difficulty', 'tags', 'created_by']
        for field in required_fields:
            if field not in material_data:
                raise ValueError(f"El campo {field} es requerido")

        # Validar dificultad
        if not 1 <= material_data['difficulty'] <= 5:
            raise ValueError("La dificultad debe estar entre 1 y 5")

        # Agregar timestamp de creación
        material_data['created_at'] = datetime.utcnow()
        material_data['updated_at'] = datetime.utcnow()

        # Convertir IDs de etiquetas a ObjectId
        material_data['tags'] = [ObjectId(tag_id) for tag_id in material_data['tags']]
        if 'prerequisites' in material_data:
            material_data['prerequisites'] = [ObjectId(tag_id) for tag_id in material_data['prerequisites']]

        return mongo.db.materials.insert_one(material_data)

    @staticmethod
    def get_material_by_id(material_id):
        """Obtiene un material por su ID"""
        return mongo.db.materials.find_one({"_id": ObjectId(material_id)})

    @staticmethod
    def get_materials_by_professor(professor_id):
        """Obtiene todos los materiales creados por un profesor"""
        return list(mongo.db.materials.find({"created_by": ObjectId(professor_id)}))

    @staticmethod
    def get_materials_by_tags(tag_ids):
        """Obtiene materiales que contengan cualquiera de las etiquetas especificadas"""
        tag_ids = [ObjectId(tag_id) for tag_id in tag_ids]
        return list(mongo.db.materials.find({"tags": {"$in": tag_ids}}))

    @staticmethod
    def update_material(material_id, update_data):
        """
        Actualiza un material existente
        Args:
            material_id: ID del material a actualizar
            update_data: Datos a actualizar
        """
        # Validar dificultad si se está actualizando
        if 'difficulty' in update_data and not 1 <= update_data['difficulty'] <= 5:
            raise ValueError("La dificultad debe estar entre 1 y 5")

        # Convertir IDs de etiquetas a ObjectId si se están actualizando
        if 'tags' in update_data:
            update_data['tags'] = [ObjectId(tag_id) for tag_id in update_data['tags']]
        if 'prerequisites' in update_data:
            update_data['prerequisites'] = [ObjectId(tag_id) for tag_id in update_data['prerequisites']]

        # Actualizar timestamp
        update_data['updated_at'] = datetime.utcnow()

        return mongo.db.materials.update_one(
            {"_id": ObjectId(material_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete_material(material_id):
        """Elimina un material"""
        return mongo.db.materials.delete_one({"_id": ObjectId(material_id)})

    @staticmethod
    def get_all_materials():
        """Obtiene todos los materiales"""
        return list(mongo.db.materials.find())
