import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from logger import logger

# NOTES: Replace the placeholders with your actual SendGrid API key, from email, and to email.
''' IMPORTANT : For securely storing credentials, you can use one of the following services:
1.HashiCorp Vault, 2.AWS Secrets Manager, 3.Azure Key Vault. 
Dont write the credantials here, which deploys to git.
'''

class EmailNotifier:
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        self.from_email = os.environ.get('FROM_EMAIL')
        self.to_email = os.environ.get('TO_EMAIL')

    def send_notification(self, subject, body):
        if not all([self.api_key, self.from_email, self.to_email]):
            logger.log("Email_Notification_Failed_Incomplete_Setup")
            return

        message = Mail(
            from_email=self.from_email,
            to_emails=self.to_email,
            subject=subject,
            html_content=body)

        try:
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            logger.log(f"Email_Notification_Sent_StatusCode_{response.status_code}")
        except Exception as e:
            logger.log(f"Email_Notification_Failed_{str(e)}")