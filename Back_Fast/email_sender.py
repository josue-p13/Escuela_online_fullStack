from email_service import send_email

# --- Función para Enviar Correo de Confirmación ---
def send_confirmation_email(to_email: str, confirmation_url: str):
    """
    Envía un correo de confirmación de cuenta usando el servicio centralizado.
    """
    subject = "Confirma tu cuenta en CrackSchool"
    html_content = f"""
    <html>
        <body>
            <h2>¡Bienvenido a CrackSchool!</h2>
            <p>Gracias por registrarte. Por favor, haz clic en el siguiente enlace para activar tu cuenta:</p>
            <p><a href="{confirmation_url}" target="_blank">Confirmar mi cuenta</a></p>
            <p>Si no te registraste en CrackSchool, puedes ignorar este correo.</p>
            <p>Este enlace expirará en 24 horas.</p>
            <br>
            <p>Saludos,</p>
            <p>El equipo de CrackSchool</p>
        </body>
    </html>
    """

    # Usar el servicio centralizado para enviar el correo
    success = send_email(to_email, subject, html_content)
    
    if success:
        print(f"Correo de confirmación enviado a {to_email}.")
    else:
        print(f"Error al enviar correo de confirmación a {to_email}.")
    
    return success
