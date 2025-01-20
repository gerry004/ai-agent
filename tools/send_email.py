from phi.utils.log import logger
from dotenv import load_dotenv

load_dotenv()

sender_email = "gerry04y@gmail.com"
sender_name = "Gerry Yang"
sender_passkey = "zqqdkqmcjpjqubif"


def send_email(receiver: str, subject: str, body: str) -> str:
    try:
        import smtplib
        from email.message import EmailMessage
    except ImportError:
        logger.error("`smtplib` not installed")
        raise

    if not receiver:
        return "error: No receiver email provided"
    if not sender_name:
        return "error: No sender name provided"
    if not sender_email:
        return "error: No sender email provided"
    if not sender_passkey:
        return "error: No sender passkey provided"

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = receiver
    message.set_content(body)

    logger.info(f"Sending Email to {receiver}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, sender_passkey)
            smtp.send_message(message)
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return f"error: {e}"

    return "email sent successfully"
