import smtplib
import os
import string
import secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def generate_temp_password(length: int = 8) -> str:
    """Genera una contraseña temporal segura"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))


def send_recovery_email(recipient_email: str, temp_password: str) -> bool:
    """
    Envía un email de recuperación de contraseña al usuario
    
    Args:
        recipient_email: Email del usuario
        temp_password: Contraseña temporal generada
    
    Returns:
        bool: True si se envió correctamente, False en caso de error
    """
    try:
        # Obtener configuración de variables de entorno
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = int(os.getenv("SMTP_PORT", "587"))
        app_name = os.getenv("APP_NAME", "kaio")
        
        if not sender_email or not sender_password:
            print("Error: Credenciales de email no configuradas en .env")
            return False
        
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = f"Recupera tu contraseña - {app_name}"
        message["From"] = sender_email
        message["To"] = recipient_email
        
        # Contenido HTML del email
        html = f"""\
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
                    <h2 style="color: #2c3e50;">¡Hola!</h2>
                    <p>Hemos recibido una solicitud para recuperar tu contraseña en <strong>{app_name}</strong>.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin: 20px 0; border-radius: 3px;">
                        <p style="margin: 0; font-size: 14px;"><strong>Tu nueva contraseña temporal es:</strong></p>
                        <p style="margin: 10px 0 0 0; font-size: 20px; font-weight: bold; color: #007bff; font-family: 'Courier New', monospace;">
                            {temp_password}
                        </p>
                    </div>
                    
                    <p><strong>Instrucciones:</strong></p>
                    <ol>
                        <li>Inicia sesión con tu correo y esta contraseña temporal</li>
                        <li>Dirígete a tu panel de control</li>
                        <li>Cambia esta contraseña temporal por una que recuerdes fácilmente</li>
                    </ol>
                    
                    <p style="color: #666; font-size: 12px;">
                        <strong>Importante:</strong> Esta contraseña temporal es válida por un acceso. 
                        Por favor, cámbiala inmediatamente después de iniciar sesión.
                    </p>
                    
                    <hr style="margin: 20px 0; border: none; border-top: 1px solid #ddd;">
                    
                    <p style="text-align: center; color: #666; font-size: 12px;">
                        ¡Gracias por confiar en nosotros!<br>
                        <strong>{app_name}</strong>
                    </p>
                </div>
            </body>
        </html>
        """
        
        # Contenido de texto plano (fallback)
        text = f"""\
        ¡Hola!
        
        Hemos recibido una solicitud para recuperar tu contraseña en {app_name}.
        
        Tu nueva contraseña temporal es: {temp_password}
        
        Instrucciones:
        1. Inicia sesión con tu correo y esta contraseña temporal
        2. Dirígete a tu panel de control
        3. Cambia esta contraseña temporal por una que recuerdes fácilmente
        
        Importante: Esta contraseña temporal es válida por un acceso. 
        Por favor, cámbiala inmediatamente después de iniciar sesión.
        
        ¡Gracias por confiar en nosotros!
        {app_name}
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Conectar a servidor SMTP y enviar
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        
        return True
        
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        return False
