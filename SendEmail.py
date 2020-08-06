# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class MyMail:
    from_email = os.environ.get('FROM_EMAIL')
    to_emails = os.environ.get('TO_EMAIL')
    
    @classmethod
    def send_mail(cls, subject, html_content):
        message = Mail(
            from_email=MyMail.from_email,
            to_emails=MyMail.to_emails,
            subject=subject,
            html_content=html_content)
        try:
            print(os.environ.get('SENDGRID_API_KEY'))
            print(os.environ.get('FROM_EMAIL'))
            print(os.environ.get('TO_EMAIL'))
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


# MyMail.send_mail('subject', 'hi')


