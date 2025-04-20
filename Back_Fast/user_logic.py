\
# filepath: c:\\Users\\josue\\Desktop\\Escuela_online\\Back_Fast\\user_logic.py
from passlib.context import CryptContext
from fastapi import HTTPException, status
from pydantic import EmailStr

# Importar la colección de MongoDB
from mongo_con import collection

# --- Seguridad: Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Verifica una contraseña plana contra una hasheada."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """Genera el hash de una contraseña."""
    return pwd_context.hash(password)
# --- Fin Seguridad ---

# --- Lógica de Registro ---
def create_user(nombres: str, apellidos: str, email: EmailStr, password: str, telefono: str | None):
    """
    Crea un nuevo usuario en la base de datos.
    Verifica si el email ya existe, hashea la contraseña e inserta el usuario.
    """
    # Verificar si el usuario ya existe
    existing_user = collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )

    # Hashear la contraseña
    hashed_password = get_password_hash(password)

    # Crear el documento del usuario para MongoDB
    user_data = {
        "nombres": nombres,
        "apellidos": apellidos,
        "email": email,
        "telefono": telefono,
        "hashed_password": hashed_password
    }

    # Insertar en la base de datos
    try:
        result = collection.insert_one(user_data)
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No se pudo registrar el usuario (error de inserción)"
            )
        return result.inserted_id # O simplemente True si no necesitas el ID
    except Exception as e:
        # Loggear el error real en el servidor sería ideal aquí
        print(f"Error al insertar en MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error en el servidor sal registrar: {e}"
        )
# --- Fin Lógica de Registro ---


# --- Lógica de Autenticación ---
def authenticate_user(email: EmailStr, password: str):
    """
    Autentica un usuario buscando por email y verificando la contraseña.
    Devuelve los datos del usuario si es exitoso, None si no.
    """
     # Buscar usuario por email
    db_user = collection.find_one({"email": email})
    if not db_user:
        return None # Usuario no encontrado

    # Verificar contraseña
    if not verify_password(password, db_user.get("hashed_password", "")):
        return None # Contraseña incorrecta

    return db_user # Autenticación exitosa
# --- Fin Lógica de Autenticación ---

