from app import mongo
from bson import ObjectId

class TagModel:
    @staticmethod
    def create_tag(tag_data):
        # Validar que el nombre no esté vacío
        if not tag_data.get('name'):
            raise ValueError("El nombre de la etiqueta es requerido")
            
        # Verificar si ya existe una etiqueta con el mismo nombre
        existing_tag = mongo.db.tags.find_one({"name": tag_data['name']})
        if existing_tag:
            raise ValueError("Ya existe una etiqueta con este nombre")
            
        return mongo.db.tags.insert_one(tag_data)

    @staticmethod
    def get_all_tags():
        return list(mongo.db.tags.find())

    @staticmethod
    def get_tag_by_id(tag_id):
        return mongo.db.tags.find_one({"_id": ObjectId(tag_id)})

    @staticmethod
    def update_tag(tag_id, update_data):
        if not update_data.get('name'):
            raise ValueError("El nombre de la etiqueta es requerido")
            
        # Verificar si el nuevo nombre ya existe en otra etiqueta
        existing_tag = mongo.db.tags.find_one({
            "name": update_data['name'],
            "_id": {"$ne": ObjectId(tag_id)}
        })
        if existing_tag:
            raise ValueError("Ya existe una etiqueta con este nombre")
            
        return mongo.db.tags.update_one(
            {"_id": ObjectId(tag_id)},
            {"$set": update_data}
        )

    @staticmethod
    def delete_tag(tag_id):
        return mongo.db.tags.delete_one({"_id": ObjectId(tag_id)})
