from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient('YOUR_SENDGRID_API_KEY')

    def send_email(self, subject, content):
        message = Mail(
            from_email='from_email@example.com',
            to_emails='to_email@example.com',
            subject=subject,
            plain_text_content=content)
        self.client.send(message)
