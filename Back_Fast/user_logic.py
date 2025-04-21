import secrets
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from pydantic import EmailStr
from mongo_con import collection

# --- Seguridad: Sin hashing en la contraseña, porque no pude:c
def get_password_hash(password):
    """
    Simplemente devuelve la contraseña sin encriptar (no seguro para producción).
    """
    return password
    
def verify_password(plain_password, stored_password):
    """
    Simplemente compara las contraseñas directamente (no seguro para producción).
    """
    return plain_password == stored_password
# --- Fin Seguridad ---

# --- Lógica de Registro (Modificada) ---
def prepare_user_registration(nombres: str, apellidos: str, email: EmailStr, password: str, telefono: str | None):
    """
    Prepara los datos del usuario para el registro, genera token y expiración.
    Verifica si el email ya existe y está confirmado. Si existe pero no confirmado, actualiza.
    Devuelve los datos del usuario y el token si todo está bien, o lanza excepción.
    """
    existing_user = collection.find_one({"email": email})

    if existing_user and existing_user.get("is_email_confirmed", False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado y confirmado."
        )
    confirmation_token = secrets.token_urlsafe(32)
    # Asegurarse de usar timezone-aware datetime
    token_expiry = datetime.now(timezone.utc) + timedelta(hours=24)
    # Almacenar la contraseña sin encriptar, porque nuevamanete no pude
    plain_password = password

    user_data = {
        "nombres": nombres,
        "apellidos": apellidos,
        "email": email,
        "telefono": telefono,
        "password": plain_password,  
        "is_email_confirmed": False, 
        "confirmation_token": confirmation_token,
        "token_expiry": token_expiry
    }

    try:
        if existing_user:
            collection.update_one(
                {"_id": existing_user["_id"]},
                {"$set": user_data}
            )
            print(f"Usuario existente no confirmado actualizado: {email}")
        else:
            result = collection.insert_one(user_data)
            if not result.inserted_id:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="No se pudo registrar el usuario (error de inserción)"
                )
            print(f"Nuevo usuario pendiente de confirmación insertado: {email}")
        return {"email": email, "token": confirmation_token}

    except Exception as e:
        print(f"Error al preparar registro en MongoDB: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error en el servidor al preparar el registro: {e}"
        )

# --- Lógica de Confirmación (Nueva) ---
def confirm_user_email(token: str):
    """
    Confirma el email de un usuario basado en el token.
    """
    now = datetime.now(timezone.utc)
    user = collection.find_one({"confirmation_token": token})

    if not user:
        print(f"Intento de confirmación con token inválido: {token}")
        return False 
    # Verificar si el token ha expirado
    token_expiry = user.get("token_expiry")
    # Asegurarse de que token_expiry es timezone-aware si existe
    if token_expiry and isinstance(token_expiry, datetime) and token_expiry.tzinfo is None:
        token_expiry = token_expiry.replace(tzinfo=timezone.utc) # Hacerlo aware si no lo es

    if not token_expiry or token_expiry < now:
        print(f"Intento de confirmación con token expirado para email: {user.get('email')}")
        return False # Token expirado
    # Actualizar usuario: confirmar email y limpiar token/expiración
    try:
        result = collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {"is_email_confirmed": True},
                "$unset": {"confirmation_token": "", "token_expiry": ""} # Eliminar campos
            }
        )
        if result.modified_count == 1:
            print(f"Email confirmado exitosamente para: {user.get('email')}")
            return True
        else:
            # Esto no debería pasar si encontramos el usuario, pero por si acaso
            print(f"Error al actualizar el estado de confirmación para: {user.get('email')}")
            return False
    except Exception as e:
        print(f"Error al confirmar email en MongoDB para {user.get('email')}: {e}")
        return False

# --- Lógica de Autenticación (Modificada) ---
def authenticate_user(email: EmailStr, password: str):
    """
    Autentica un usuario buscando por email, verificando contraseña y estado de confirmación.
    Devuelve los datos del usuario si es exitoso, None si no.
    """
    db_user = collection.find_one({"email": email})
    if not db_user:
        return None # Usuario no encontrado
    # Verificar contraseña directamente
    if password != db_user.get("password", ""):
        return None # Contraseña incorrecta
    # Verificar si el email está confirmado
    if not db_user.get("is_email_confirmed", False):
        print(f"Intento de login fallido (email no confirmado): {email}")
        return None # Email no confirmado
    return db_user # Autenticación exitosa
# --- Fin Lógica de Autenticación ---

