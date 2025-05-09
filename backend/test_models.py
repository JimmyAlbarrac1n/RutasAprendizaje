from app import create_app
from app.models.user_model import UserModel

app = create_app()

with app.app_context():
    # Crear un usuario de prueba
    user_data = {
        "email": "admin@example.com",
        "password": "hashed_password",
        "role": "admin",
        "name": "Admin User"
    }
    result = UserModel.create_user(user_data)
    print(f"Usuario creado con ID: {result.inserted_id}")

    # Recuperar el usuario por email
    user = UserModel.get_user_by_email("admin@example.com")
    print("Usuario recuperado:", user)
