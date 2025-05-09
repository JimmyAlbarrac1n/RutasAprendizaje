from app import mongo
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def create_user(user_data):
        # Hashear la contraseña antes de guardar
        if 'password' in user_data:
            user_data['password'] = generate_password_hash(user_data['password'])
        return mongo.db.users.insert_one(user_data)

    @staticmethod
    def get_user_by_id(user_id):
        return mongo.db.users.find_one({"_id": user_id})

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password'], password)

    @staticmethod
    def update_user(user_id, update_data):
        # Si se está actualizando la contraseña, hashearla
        if 'password' in update_data:
            update_data['password'] = generate_password_hash(update_data['password'])
        return mongo.db.users.update_one({"_id": user_id}, {"$set": update_data})

    @staticmethod
    def delete_user(user_id):
        return mongo.db.users.delete_one({"_id": user_id})

    @staticmethod
    def get_all_users():
        return mongo.db.users.find()
