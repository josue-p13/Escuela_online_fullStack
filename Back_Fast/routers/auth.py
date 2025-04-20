\
# filepath: c:\\Users\\josue\\Desktop\\Escuela_online\\Back_Fast\\routers\\auth.py
from fastapi import APIRouter, HTTPException, status, Form
from pydantic import EmailStr
from typing import Annotated

# Importar lógica de usuario (cambiado a import absoluto)
from user_logic import create_user, authenticate_user
# Importar modelo Pydantic para login desde models.py
from models import UserLogin # Cambiado de 'principal' a 'models'

router = APIRouter()

# --- Endpoint de Registro ---
@router.post("/register", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
async def register_user_endpoint(
    nombres: Annotated[str, Form()],
    apellidos: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    telefono: Annotated[str | None, Form()] = None
):
    # Validación básica (ej. contraseñas coinciden)
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )

    # Llamar a la función de lógica de usuario para crear el usuario
    try:
        user_id = create_user(
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            password=password,
            telefono=telefono
        )
        return {"message": "Usuario registrado exitosamente"}
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error inesperado durante el registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado en el servidor: {e}"
        )

# --- Endpoint de Login ---
@router.post("/login", tags=["Authentication"])
async def login_user_endpoint(user_login: UserLogin):
    # Llamar a la función de lógica de usuario para autenticar
    authenticated_user = authenticate_user(email=user_login.email, password=user_login.password)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Devolver más datos del usuario (nombre, apellido, email)
    # Asegúrate de que estos campos existen en tu documento de MongoDB
    return {
        "message": "Login exitoso",
        "user": {
            "email": authenticated_user["email"],
            "nombres": authenticated_user.get("nombres", ""), # Usar .get con valor por defecto
            "apellidos": authenticated_user.get("apellidos", "") # Usar .get con valor por defecto
        }
        # Aquí normalmente generarías y devolverías un token JWT
    }
