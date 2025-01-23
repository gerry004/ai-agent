from phi.utils.log import logger
from phi.tools import Toolkit
from phi.utils.log import logger

from dotenv import load_dotenv
load_dotenv()


class EmailTools(Toolkit):
    def __init__(
        self,
        sender_email: str = None,
        sender_name: str = None,
        sender_passkey: str = None,
    ):
        """
        Email Tool.

        :param sender_email (str): Email address of the sender
        :param sender_name (str): Name of the sender
        :param sender_passkey (str): Passkey of the sender's email address
        """
        super().__init__(name="email_tools")

        if not sender_name:
            return "error: No sender name provided"
        if not sender_email:
            return "error: No sender email provided"
        if not sender_passkey:
            return "error: No sender passkey provided"

        self.sender_email = sender_email
        self.sender_name = sender_name
        self.sender_passkey = sender_passkey
        self.register(self.send_email)

    def send_email(self, receiver: str, subject: str, body: str) -> str:
        """
        Send an email to a recipient with subject and body.

        Args:
            receiver (str): Email address of the recipient
            subject (str): Subject of the email
            body (str): Body of the email
        """
        try:
            import smtplib
            from email.message import EmailMessage
        except ImportError:
            logger.error("`smtplib` not installed")
            raise

        if not receiver:
            return "error: No receiver email provided"

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = f"{self.sender_name} <{self.sender_email}>"
        message["To"] = receiver
        message.set_content(body)

        logger.info(f"Sending Email to {receiver}")

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.sender_email, self.sender_passkey)
                smtp.send_message(message)
        except Exception as e:
            logger.error(f"Error sending email: {e}")
            return f"error: {e}"

        return "email sent successfully"
  
    def schedule_send_email(self, receiver: str, subject: str, body: str, time: str) -> str:
        """
        Schedule an email to be sent at a specific time.

        Args:
            receiver (str): Email address of the recipient
            subject (str): Subject of the email
            body (str): Body of the email
            time (str): Time to send the email
        """
        pass
    
    def list_unread_email(self, keywords: str) -> str:
        """
        Check email inbox for new messages related to certain keywords.

        Args:
            keywords (str): Keywords to search for in the email inbox
        """
        pass
    
    def archive_email(self, keywords: str) -> str:
        """
        Archive emails in inbox.

        Args:
            keywords (str): Keywords to search for in the email inbox
        """
        pass
