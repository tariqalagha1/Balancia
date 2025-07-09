import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from fastapi import BackgroundTasks

from ..config import settings

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.from_email = settings.EMAIL_FROM

    async def send_email(self, to_email: str, subject: str, body: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.from_email
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)

            logger.info(f"Email sent to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            raise


email_service = EmailService()


async def send_invite_email(
    email: str,
    token: str,
    inviter_name: str,
    background_tasks: Optional[BackgroundTasks] = None,
):
    invite_url = f"{settings.FRONTEND_URL}/invite/accept?token={token}"
    subject = f"You've been invited to join {settings.APP_NAME}"
    body = f"""
    <p>Hello,</p>
    <p>{inviter_name} has invited you to join {settings.APP_NAME}.</p>
    <p>Click <a href="{invite_url}">here</a> to accept the invitation.</p>
    <p>This link will expire in 7 days.</p>
    """

    if background_tasks:
        background_tasks.add_task(email_service.send_email, email, subject, body)
    else:
        await email_service.send_email(email, subject, body)
