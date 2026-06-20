import logging
from threading import Thread
from typing import Any, Optional

logger = logging.getLogger(__name__)


class Message:
    def __init__(self, subject, recipients, body="", html="", sender=None):
        self.subject = subject
        self.recipients = recipients if isinstance(recipients, list) else [recipients]
        self.body = body
        self.html = html
        self.sender = sender


class Mailer:
    def __init__(self, app=None) -> None:
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        self.app = app
        if not self.is_configured:
            logger.warning("MAIL not configured. OTP emails will not be sent.")
            return

    @property
    def is_configured(self) -> bool:
        if not self.app:
            return False
        return bool(self.app.config.get("MAIL_SERVER") and self.app.config.get("MAIL_DEFAULT_SENDER"))

    def _send_message(self, msg: Any) -> None:
        self._send_smtp(msg)

    def _send_async(self, msg: Any) -> None:
        try:
            self._send_message(msg)
        except Exception as exc:
            logger.exception("Failed to send email: %s", exc)

    def _send_smtp(self, msg: Any) -> None:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        smtp_server = self.app.config.get("MAIL_SERVER", "")
        smtp_port = self.app.config.get("MAIL_PORT", 587)
        use_tls = self.app.config.get("MAIL_USE_TLS", True)
        username = self.app.config.get("MAIL_USERNAME", "")
        password = self.app.config.get("MAIL_PASSWORD", "")
        sender = self.app.config.get("MAIL_DEFAULT_SENDER") or username
        recipients = getattr(msg, "recipients", [])
        body = msg.body or ""
        html = getattr(msg, "html", None)
        subject = getattr(msg, "subject", "")
        if not self.is_configured:
            raise ValueError("MAIL_SERVER and MAIL_DEFAULT_SENDER are not configured")
        if not isinstance(recipients, list):
            recipients = [recipients]
        recipients = [recipient for recipient in recipients if recipient]
        if not recipients:
            raise ValueError("No email recipients provided")
        for recipient in recipients:
            mime_msg = MIMEMultipart("alternative")
            mime_msg["From"] = sender
            mime_msg["To"] = recipient
            mime_msg["Subject"] = subject
            mime_msg.attach(MIMEText(body, "plain"))
            if html:
                mime_msg.attach(MIMEText(html, "html"))
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_tls:
                    server.starttls()
                if username and password:
                    server.login(username, password)
                server.send_message(mime_msg)

    def _configured_message(self, subject: str, recipients, text_body: str = "", html_body: str = "", sender=None) -> Any:
        return Message(
            subject=subject,
            recipients=recipients if isinstance(recipients, list) else [recipients],
            body=text_body,
            html=html_body or text_body,
            sender=sender or self.app.config.get("MAIL_DEFAULT_SENDER"),
        )

    def send_email(self, subject: str, recipients, text_body: str = "", html_body: str = "", sender=None) -> bool:
        if not self.is_configured:
            logger.info("Email skipped (not configured): %s -> %s", subject, recipients)
            return False
        msg = self._configured_message(subject, recipients, text_body, html_body, sender)
        Thread(target=self._send_async, args=(msg,)).start()
        return True

    def send_email_sync(self, subject: str, recipients, text_body: str = "", html_body: str = "", sender=None) -> bool:
        if not self.is_configured:
            logger.info("Email skipped (not configured): %s -> %s", subject, recipients)
            return False
        msg = self._configured_message(subject, recipients, text_body, html_body, sender)
        self._send_message(msg)
        return True

    def send_otp(self, recipient_email: str, otp: str, *, template_context: Optional[dict] = None, async_send: bool = True) -> bool:
        subject = "ePaisa - One Time Password (OTP)"
        text_body = (
            f"Dear Customer,\n\n"
            f"Your OTP for ePaisa transaction is: {otp}\n\n"
            f"This OTP is valid for 5 minutes and can only be used once.\n\n"
            f"If you did not request this, please contact support immediately.\n\n"
            f"Regards,\nTeam ePaisa"
        )
        context = {"otp": otp}
        if template_context:
            context.update(template_context)
        try:
            from flask import render_template
            html_body = render_template("email/otp_email.html", **context)
        except Exception:
            html_body = text_body

        if async_send:
            return self.send_email(subject, recipient_email, text_body, html_body)
        return self.send_email_sync(subject, recipient_email, text_body, html_body)
