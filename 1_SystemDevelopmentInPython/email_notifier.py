# email_notifier.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email_notification(to_email, subject, message):
    try:
        message = Mail(
            from_email='your_email@example.com',
            to_emails=to_email,
            subject=subject,
            html_content=message)
        sg = SendGridAPIClient('YOUR_SENDGRID_API_KEY')
        response = sg.send(message)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
