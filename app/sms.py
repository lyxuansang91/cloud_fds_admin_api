import os  # noqa
from twilio.client import Client  # noqa


def send_sms(to_phone, body):
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    from_ = os.environ.get('FROM_PHONE')
    client = Client(account_sid, auth_token)
    message = client.messages.create(body=body, from_=from_, to=to_phone)
    return message.sid
