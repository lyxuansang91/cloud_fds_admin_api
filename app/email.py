import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, From)


def send_email(subject, sender, recipients, html_body):

    message = Mail(from_email=From(sender, 'noreply'), to_emails=recipients, subject=subject, html_content=html_body)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
