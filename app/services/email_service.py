from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from jinja2 import Template

from app.core.config import settings


class EmailService:
    """Email service for sending emails."""
    
    def __init__(self):
        """Initialize email service."""
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.mail_username,
            MAIL_PASSWORD=settings.mail_password,
            MAIL_FROM=settings.mail_from,
            MAIL_PORT=settings.mail_port,
            MAIL_SERVER=settings.mail_server,
            MAIL_STARTTLS=settings.mail_tls,
            MAIL_SSL_TLS=settings.mail_ssl,
            MAIL_FROM_NAME=settings.mail_from_name,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=False,
        )
        self.fastmail = FastMail(self.conf)
    
    async def send_verification_email(self, email: str, verification_url: str, user_name: str = None) -> bool:
        """Send email verification email."""
        try:
            html_template = """
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Подтверждение регистрации</title>
                <style>
                    body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                    .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                    .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
                    .content { padding: 20px; background-color: #f9f9f9; }
                    .button { display: inline-block; padding: 12px 24px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }
                    .footer { padding: 20px; text-align: center; color: #666; font-size: 12px; }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Добро пожаловать!</h1>
                    </div>
                    <div class="content">
                        <h2>Здравствуйте{% if user_name %}, {{ user_name }}{% endif %}!</h2>
                        <p>Спасибо за регистрацию в нашем сервисе аутентификации.</p>
                        <p>Для завершения регистрации и активации вашего аккаунта, пожалуйста, нажмите на кнопку ниже:</p>
                        <p style="text-align: center;">
                            <a href="{{ verification_url }}" class="button">Подтвердить регистрацию</a>
                        </p>
                        <p>Если кнопка не работает, скопируйте и вставьте эту ссылку в браузер:</p>
                        <p style="word-break: break-all; background-color: #eee; padding: 10px; border-radius: 3px;">
                            {{ verification_url }}
                        </p>
                        <p><strong>Важно:</strong> Эта ссылка действительна в течение 24 часов.</p>
                    </div>
                    <div class="footer">
                        <p>Если вы не регистрировались в нашем сервисе, просто проигнорируйте это письмо.</p>
                        <p>© 2024 Authentication Service</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            text_template = """
            Здравствуйте{% if user_name %}, {{ user_name }}{% endif %}!

            Спасибо за регистрацию в нашем сервисе аутентификации.

            Для завершения регистрации и активации вашего аккаунта, перейдите по ссылке:
            {{ verification_url }}

            Важно: Эта ссылка действительна в течение 24 часов.

            Если вы не регистрировались в нашем сервисе, просто проигнорируйте это письмо.

            С уважением,
            Authentication Service
            """
            
            html_content = Template(html_template).render(
                verification_url=verification_url,
                user_name=user_name
            )
            
            text_content = Template(text_template).render(
                verification_url=verification_url,
                user_name=user_name
            )
            
            message = MessageSchema(
                subject="Подтверждение регистрации",
                recipients=[email],
                body=html_content,
                subtype="html"
            )
            
            await self.fastmail.send_message(message)
            return True
            
        except Exception as e:
            print(f"Error sending verification email: {e}")
            return False


_email_service_instance = None

def get_email_service() -> EmailService:
    """Get email service instance (lazy initialization)."""
    global _email_service_instance
    if _email_service_instance is None:
        _email_service_instance = EmailService()
    return _email_service_instance
