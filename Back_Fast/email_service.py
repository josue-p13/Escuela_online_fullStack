import resend
import os

# --- Configuración de Resend ---
RESEND_API_KEY = ""
SENDER_EMAIL = "CrackSchool@hotmail.com"
# Configurar API key
resend.api_key = RESEND_API_KEY
def send_email(to_email, subject, html_content):
    """
    Función centralizada para enviar correos con Resend.
    Parámetros:
    - to_email: Email del destinatario
    - subject: Asunto del correo
    - html_content: Contenido HTML del corre
    Retorna:
    - True si el correo se envió correctamente
    - False si hubo un error
    """
    try:
        # Configurar los parámetros del correo
        params = {
            "from": SENDER_EMAIL,
            "to": [to_email] if isinstance(to_email, str) else to_email,
            "subject": subject,
            "html": html_content,
        }
        response = resend.Emails.send(params)
        # Verificar respuesta
        if response and response.get('id'):
            print(f"Correo enviado a {to_email}. ID: {response.get('id')}")
            return True
        else:
            print(f"Error: Respuesta de Resend sin ID: {response}")
            return False
    
    except Exception as e:
        print(f"Error al enviar correo a {to_email}: {str(e)}")
        return False
