from fastapi import APIRouter, HTTPException, status, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import EmailStr
from typing import Annotated
from user_logic import prepare_user_registration, confirm_user_email, authenticate_user
from models import UserLogin
from email_sender import send_confirmation_email

router = APIRouter()

# --- Endpoint de Registro (Modificado) ---
@router.post("/register", status_code=status.HTTP_202_ACCEPTED, tags=["Authentication"])
async def register_user_endpoint(
    request: Request,
    nombres: Annotated[str, Form()],
    apellidos: Annotated[str, Form()],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    confirm_password: Annotated[str, Form()],
    telefono: Annotated[str | None, Form()] = None
):
    if password != confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Las contraseñas no coinciden"
        )

    try:
        # Preparar registro (guarda temporalmente, devuelve token)
        user_info = prepare_user_registration(
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            password=password,
            telefono=telefono
        )

        # Construir URL de confirmación completa (corregida)
        # Cambiamos cómo se construye la URL para asegurar el formato correcto
        base_url = str(request.base_url).rstrip('/')
        confirmation_url = f"{base_url}/auth/confirm/{user_info['token']}"
        
        print(f"URL de confirmación generada: {confirmation_url}")

        # Enviar correo de confirmación
        email_sent = send_confirmation_email(
            to_email=user_info['email'],
            confirmation_url=confirmation_url
        )

        if not email_sent:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Se preparó el registro, pero no se pudo enviar el correo de confirmación."
            )

        return {"message": "Registro casi completo. Revisa tu correo electrónico para confirmar tu cuenta."}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Error inesperado durante el registro: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado en el servidor durante el registro."
        )

# --- Endpoint de Confirmación (Corregido) ---
@router.get("/confirm/{token}", tags=["Authentication"])
async def confirm_email_endpoint(token: str):
    print(f"Solicitud de confirmación recibida con token: {token}")
    confirmed = confirm_user_email(token)

    if confirmed:
        frontend_login_url = "http://localhost:5173/login?confirmed=true"
        return RedirectResponse(url=frontend_login_url)
    else:
        html_content = """
        <html>
            <head><title>Error de Confirmación</title></head>
            <body>
                <h1>Error en la Confirmación</h1>
                <p>El enlace de confirmación es inválido, ha expirado o ya ha sido utilizado.</p>
                <p>Por favor, intenta registrarte de nuevo o contacta con soporte si el problema persiste.</p>
            </body>
        </html>
        """
        return HTMLResponse(content=html_content, status_code=status.HTTP_400_BAD_REQUEST)

# --- Endpoint de Login ---
@router.post("/login", tags=["Authentication"])
async def login_user_endpoint(user_login: UserLogin):
    authenticated_user = authenticate_user(email=user_login.email, password=user_login.password)

    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas o email no confirmado.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "message": "Login exitoso",
        "user": {
            "email": authenticated_user["email"],
            "nombres": authenticated_user.get("nombres", ""),
            "apellidos": authenticated_user.get("apellidos", "")
        }
    }
